from typing import List

import requests
import re
import math
from bs4 import BeautifulSoup

from app.exceptions import (
    AttendanceUpdateInProcessException,
    InvalidUsernameOrPasswordException,
    ScrappingError,
    NoTimeTableDataException,
    NoSemResultsAvailable,
)
from app.models import AttendanceModel, TimeTableModel, SemMarkModel
from .constants import GRADE_SCORE_MAP


class AttendanceWebScrapper:
    ECAMPUS_URL = "https://ecampus.psgtech.ac.in/studzone2/"
    ATTENDANCE_PAGE_URL = "https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx"
    TIMETABLE_PAGE_URL = "https://ecampus.psgtech.ac.in/studzone2/AttWfStudTimtab.aspx"
    SEM_EXAM_RESULTS_PAGE_URL = (
        "https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx"
    )
    COURSE_DETAILS_PAGE_URL = (
        "https://ecampus.psgtech.ac.in/studzone2/AttWfStudCourseSelection.aspx"
    )

    def __init__(self, user_name, password):
        self.session = requests.Session()
        login_page = self.session.get(self.ECAMPUS_URL)
        soup = BeautifulSoup(login_page.text, "html.parser")
        item_request_body = self.generate_login_request_body(soup, user_name, password)
        response = self.session.post(
            url=login_page.url,
            data=item_request_body,
            headers={"Referer": login_page.url},
        )

        if response.status_code != 200:
            raise ScrappingError
        soup = BeautifulSoup(response.text, "html.parser")
        message = soup.find(string=re.compile("Invalid"))
        if message and "Invalid" in message:
            raise InvalidUsernameOrPasswordException

    def convert_data_to_json(self):
        pass

    @staticmethod
    def grade_score(grade: str) -> int:
        grades = {
            "O": 10,
            "A+": 9,
            "A": 8,
            "B+": 7,
            "B": 6,
            "C+": 5,
            "C": 4,
            "W": 0,
            "RA": 0,
            "SA": 0,
        }
        return grades.get(grade, 0)

    @staticmethod
    def apply_the_bunker_formula(
        percentage_of_attendance: int,
        total_hours: int,
        total_present: int,
        threshold=0.75,
    ) -> dict:
        res = {}
        if percentage_of_attendance <= 75:
            res["class_to_attend"] = math.ceil(
                (threshold * total_hours - total_present) / (1 - threshold)
            )
        else:
            res["class_to_bunk"] = math.floor(
                (total_present - (threshold * total_hours)) / (threshold)
            )
        return res

    @staticmethod
    def generate_login_request_body(
        soup: BeautifulSoup, user_name: str, password: str
    ) -> dict:
        view_state = soup.select("#__VIEWSTATE")[0]["value"]
        event_validation = soup.select("#__EVENTVALIDATION")[0]["value"]
        view_state_gen = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]

        item_request_body = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": view_state_gen,
            "__EVENTVALIDATION": event_validation,
            "rdolst": "S",
            "txtusercheck": user_name,
            "txtpwdcheck": password,
            "abcd3": "Login",
        }
        return item_request_body

    @staticmethod
    def parse_table_data_as_attendance_models(data: list) -> List[AttendanceModel]:
        return [
            AttendanceModel(
                course_code=d[0],
                total_hours=int(d[1]),
                exemption_hours=int(d[2]),
                total_absent=int(d[3]),
                total_present=int(d[4]),
                percentage_of_attendance=int(d[5]),
                percentage_with_exemp=int(d[6]),
                percentage_with_exemp_med=int(d[7]),
                attendance_percentage_from=d[8],
                attendance_percentage_to=d[9],
                remark=AttendanceWebScrapper.apply_the_bunker_formula(
                    percentage_of_attendance=int(d[5]),
                    total_hours=int(d[1]),
                    total_present=int(d[4]),
                ),
            )
            for d in data[1:]
        ]

    @staticmethod
    def parse_table_data_as_timetable_models(data: list) -> List[TimeTableModel]:
        return [
            TimeTableModel(
                course_code=d[0], course_title=d[1], programme=d[2], sem_no=d[3]
            )
            for d in data[1:]
        ]

    @staticmethod
    def parse_sem_marks(data: list) -> SemMarkModel:
        CUM_GRADE_X_CREDIT = 0
        CUM_CREDIT = 0
        for d in data[1:]:
            GRADE, CREDIT = GRADE_SCORE_MAP[d[6]], int(d[7])
            CUM_GRADE_X_CREDIT += GRADE * CREDIT
            CUM_CREDIT += CREDIT
        return SemMarkModel(
            latest_sem_no=data[1][4],
            latest_sem_cgpa=round(CUM_GRADE_X_CREDIT / CUM_CREDIT, 3),
        )

    @staticmethod
    def parse_table(table: BeautifulSoup) -> list:
        data = []
        rows = table.find_all("tr")
        for index, row in enumerate(rows):
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

    def fetch_attendance(self):
        attendance_page = self.session.get(self.ATTENDANCE_PAGE_URL)
        soup = BeautifulSoup(attendance_page.text, "html.parser")
        table = soup.find("table", attrs={"class": "cssbody"})
        if table is None:
            message = str(soup.find("span", attrs={"id": "Message"}))
            if "On Process" in message:
                raise AttendanceUpdateInProcessException

        return AttendanceWebScrapper.parse_table_data_as_attendance_models(
            self.parse_table(table)
        )

    def fetch_time_table(self) -> List[TimeTableModel]:
        time_table_page = self.session.get(self.TIMETABLE_PAGE_URL)
        soup = BeautifulSoup(time_table_page.text, "html.parser")
        table = soup.find("table", attrs={"id": "TbCourDesc"})
        if table is None:
            raise NoTimeTableDataException

        return AttendanceWebScrapper.parse_table_data_as_timetable_models(
            self.parse_table(table)
        )

    def fetch_current_sem_exam_results(self):
        sem_exam_results_page = self.session.get(self.SEM_EXAM_RESULTS_PAGE_URL)
        soup = BeautifulSoup(sem_exam_results_page.text, "html.parser")
        table = soup.find("table", attrs={"id": "DgResult"})
        if table is None:
            raise NoSemResultsAvailable

        return self.parse_table(table)

    def fetch_all_previous_semester_exam_results(self):
        course_details_page = self.session.get(self.COURSE_DETAILS_PAGE_URL)
        soup = BeautifulSoup(course_details_page.text, "html.parser")
        table = soup.find("table", attrs={"id": "PDGCourse"})
        if table is None:
            raise ScrappingError

        return AttendanceWebScrapper.parse_sem_marks(self.parse_table(table))

    def fetch_previous_semester_exam_results(self):
        pass


if __name__ == "__main__":
    awc = AttendanceWebScrapper(user_name="abcde", password="1234")
    print(awc.fetch_attendance())
    print(awc.fetch_time_table())
    print(awc.fetch_previous_semester_exam_results())
