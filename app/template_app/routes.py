from flask import Blueprint, flash, jsonify, render_template, request

import bunker_mod as bk

template_page = Blueprint("template_app", __name__, template_folder="templates")


@template_page.route("/", methods=["GET", "POST"])
def template_app():
    if request.method == "POST":
        username = request.form.get("usr")
        pwd = request.form.get("pwd")

        try:
            table, session = bk.return_attendance(username, pwd)
        except:
            table = bk.return_attendance(username, pwd)

        if (
            table != "Invalid password"
            and table != "Try again after some time"
            and table != "Table is being updated"
        ):

            res = bk.data_json(table)

            courses = []
            total_class = []
            total_present = []
            specs = []
            subplot_titles = []

            for course in res:
                courses.append(course["name"])
                total_class.append(course["total_hours"])
                total_present.append(course["total_present"])
                specs.append([{"type": "domain"}])
                subplot_titles.append("Course Code " + course["name"])

            time_table = bk.return_timetable(session)

            cgpa_details = bk.return_cgpa(session)

            return render_template(
                "output.html",
                load=True,
                time_table=time_table,
                data=res,
                cgpa=cgpa_details,
            )
        else:
            return render_template("output.html", load=False, text=table)

    return render_template("home.html")
