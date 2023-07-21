from flask import Blueprint, flash, jsonify, render_template, request
from app.exceptions import (
    AttendanceUpdateInProcessException,
    InvalidUsernameOrPasswordException,
    NoTimeTableDataException,
    ScrappingError,
)
from app.services.ecampus_web_scrapper import AttendanceWebScrapper

from .utils import map_course_name_with_code, get_last_updated_date

template_page = Blueprint("template_app", __name__, template_folder="templates")


@template_page.route("/", methods=["GET", "POST"])
def template_app():
    if request.method == "POST":
        username = request.form.get("usr")
        pwd = request.form.get("pwd")

        try:
            awc = AttendanceWebScrapper(user_name=username, password=pwd)
            try:
                time_table = map_course_name_with_code(awc.fetch_time_table())
            except NoTimeTableDataException as error:
                time_table = None

            try:
                attendance = awc.fetch_attendance()
                last_date_updated = get_last_updated_date(attendance)
            except AttendanceUpdateInProcessException as error:
                attendance = None

            return render_template(
                "output.html",
                load=True,
                time_table=time_table,
                data=attendance,
                last_date_updated=last_date_updated,
            )

        except (ScrappingError, InvalidUsernameOrPasswordException) as error:
            return render_template("output.html", load=False, text=error.message)

    return render_template("home.html")
