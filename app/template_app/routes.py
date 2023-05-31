from flask import Blueprint, flash, jsonify, render_template, request
from app.exceptions import (
    AttendanceUpdateInProcessException,
    InvalidUsernameOrPasswordException,
    NoTimeTableDataException,
    ScrappingError,
)
from app.services.ecampus_web_scrapper import AttendanceWebScrapper

import bunker_mod as bk

template_page = Blueprint("template_app", __name__, template_folder="templates")


@template_page.route("/", methods=["GET", "POST"])
def template_app():
    if request.method == "POST":
        username = request.form.get("usr")
        pwd = request.form.get("pwd")

        try:
            awc = AttendanceWebScrapper(user_name=username, password=pwd)
            try:
                time_table = awc.fetch_time_table()
            except NoTimeTableDataException as error:
                time_table = None

            try:
                attendance = awc.fetch_attendance()
            except AttendanceUpdateInProcessException as error:
                attendance = None

            cgpa_details = bk.return_cgpa(awc.session)
            
            return render_template(
                "output.html",
                load=True,
                time_table=time_table,
                data=attendance,
                cgpa=cgpa_details,
            )

        except (ScrappingError, InvalidUsernameOrPasswordException) as error:
            return render_template("output.html", load=False, text=error.message)

    return render_template("home.html")
