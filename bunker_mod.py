import math

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def data_json(data):
    """
    here we convert the data to json format calculate the amount days we have to take leave.
    """
    response_data = []
    threshold = 0.75

    for item in range(1, len(data)):
        item = data[item]
        temp = {}

        # Extract data
        temp["name"] = item[0]

        temp["total_hours"] = int(item[1])
        temp["exception_hour"] = int(item[2])

        temp["total_present"] = int(item[4])

        temp["percentage_of_attendance"] = int(item[5])
        # temp["percentage_of_attendance_with_exemp"] = int(item[6])
        # temp["percentage_of_attendance_with_med_exemp"] = int(item[7])

        temp["attendance_from"] = item[8]
        temp["attendance_to"] = item[9]

        # temp["med_exception_hour"] = math.floor(
        #     (
        #         (temp["percentage_of_attendance_with_med_exemp"] / 100)
        #         * temp["total_hours"]
        #     )
        #     - temp["total_present"]
        # )
        # temp["total_present_with_exemp"] = (
        #     temp["total_present"] + temp["exception_hour"] + temp["med_exception_hour"]
        # )

        # Calculate bunker functionality
        if temp['percentage_of_attendance'] <= 75:
            temp['class_to_attend'] = math.ceil((threshold*temp['total_hours'] - temp['total_present'])/(1-threshold))
        
        else:
            temp['class_to_bunk'] = math.floor((temp['total_present']-(threshold*temp['total_hours']))/(threshold))
            
        response_data.append(temp)

    return response_data


def return_attendance(username, pwd):
    try:
        session = requests.Session()
        r = session.get("https://ecampus.psgtech.ac.in/studzone2/")
        loginpage = session.get(r.url)
        soup = BeautifulSoup(loginpage.text, "html.parser")

        viewstate = soup.select("#__VIEWSTATE")[0]["value"]
        eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]
        viewstategen = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]

        item_request_body = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstategen,
            "__EVENTVALIDATION": eventvalidation,
            "rdolst": "S",
            "txtusercheck": username,
            "txtpwdcheck": pwd,
            "abcd3": "Login",
        }

        response = session.post(
            url=r.url, data=item_request_body, headers={"Referer": r.url}
        )
        val = response.url

        if response.status_code == 200:
            defaultpage = "https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx"

            page = session.get(defaultpage)
            soup = BeautifulSoup(page.text, "html.parser")

            data = []
            column = []
            table = soup.find("table", attrs={"class": "cssbody"})

            if table == None:
                message = str(soup.find("span", attrs={"id": "Message"}))
                if "On Process" in message:
                    return "Table is being updated"

            try:
                rows = table.find_all("tr")
                for index, row in enumerate(rows):
                    cols = row.find_all("td")
                    cols = [ele.text.strip() for ele in cols]
                    # Get rid of empty val
                    data.append([ele for ele in cols if ele])

                # df = pd.DataFrame(data, columns=column)
                # res = df.to_json(orient="split")
                # return res
                return data, session
            except:
                return "Invalid password"
        else:
            return "Try again after some time"

    except:
        return "Try again after some time"


def return_timetable(session):
    defaultpage = "https://ecampus.psgtech.ac.in/studzone2/AttWfStudTimtab.aspx"

    page = session.get(defaultpage)
    soup = BeautifulSoup(page.text, "html.parser")

    data = []
    table = soup.find("table", attrs={"id": "TbCourDesc"})

    if table == None:
        return {"error": "no data"}

    try:
        rows = table.find_all("tr")
        for index, row in enumerate(rows):
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        class_id = {}
        for i in range(1, len(data)):
            class_id[data[i][0]] = data[i][1]

        return class_id
    except:
        return {"error": "no data"}


def gradeMap(grade):
    grade_score_map = {
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

    if grade not in grade_score_map.keys():
        return 0

    return grade_score_map[grade]


def return_cgpa(session):
    resultspage = "https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx"

    page = session.get(resultspage)
    soup = BeautifulSoup(page.text, "html.parser")

    latest_sem_data = []
    table = soup.find("table", attrs={"id": "DgResult"})

    if table != None:
        try:
            rows = table.find_all("tr")
            for index, row in enumerate(rows):
                cols = row.find_all("td")
                cols = [ele.text for ele in cols]
                latest_sem_data.append([ele for ele in cols if ele])
        except:
            print("No results available !!")

    coursepage = "https://ecampus.psgtech.ac.in/studzone2/AttWfStudCourseSelection.aspx"

    page = session.get(coursepage)
    soup = BeautifulSoup(page.text, "html.parser")

    data = []
    table = soup.find("table", attrs={"id": "PDGCourse"})

    if table != None:
        try:
            rows = table.find_all("tr")
            for index, row in enumerate(rows):
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
        except:
            print("No Course Info available !!")
    else:
        print("No Course Info available !!")

    if len(data) == 0 and len(latest_sem_data) == 0:
        return {"error": "No data"}

    global df
    global latest_sem_records

    # Preprocess latest sem results if available
    if len(latest_sem_data) != 0:
        latest_sem_data.pop(0)
        # print(latest_sem_data)
        latest_sem_records = pd.DataFrame(
            latest_sem_data,
            columns=[
                "COURSE SEM",
                "COURSE CODE",
                "COURSE TITLE",
                "CREDITS",
                "GRADE",
                "RESULT",
            ],
        )
        # print(latest_sem_records)
        latest_sem_records["GRADE"] = latest_sem_records["GRADE"].str.split().str[-1]
        # print(latest_sem_records["COURSE SEM"])
        latest_sem_records["COURSE SEM"] = latest_sem_records["COURSE SEM"].replace(
            r"^\s*$", np.nan, regex=True
        )
        # print(latest_sem_records["COURSE SEM"])
        latest_sem_records["COURSE SEM"].fillna(method="ffill", inplace=True)
        # print(latest_sem_records["COURSE SEM"])

    try:
        cols = data.pop(0)
        df = pd.DataFrame(data, columns=cols)

        # Add latest sem results if available
        if len(latest_sem_data) != 0:
            df = df.append(latest_sem_records, ignore_index=True)
            df.drop_duplicates(subset="COURSE CODE", keep="last", inplace=True)
    except:
        df = latest_sem_records.copy()

    # CPGA calculation
    latest_sem = df["COURSE SEM"].max()
    df["CREDITS"] = df["CREDITS"].astype(int)
    df["GRADE"] = df["GRADE"].apply(gradeMap)
    df["COURSE SCORE"] = df["GRADE"] * df["CREDITS"]
    latest_cgpa = df["COURSE SCORE"].sum() / df["CREDITS"].sum()

    res = {"lastest_sem": latest_sem, "latest_sem_cgpa": round(latest_cgpa, 3)}

    return res
