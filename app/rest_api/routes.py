import math

from flask import Blueprint, jsonify, request

import bunker_mod as bk

rest_api = Blueprint("rest_api", __name__, template_folder="templates")


@rest_api.route("/send_attendance/<username>/<pwd>", methods=["POST"])
def send_attendance(username: str, pwd: str):
    if request.method == "POST":
        try:
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

                return jsonify(res)
            else:
                res = {"error": "Invalid details try again"}
                return jsonify(res)

        except:
            response = {"error": "Given input details does not match up!!"}
            return jsonify(response)


@rest_api.route("/senddata_attendance", methods=["POST"])
def senddata_attendance():
    try:
        input_json = request.get_json(force=True)
        courses = input_json["class_code"]
        total_class = input_json["total_hours"]
        total_present = input_json["total_present"]
        threshold = int(input_json["threshold"])
        threshold = threshold / 100

        if (
            (len(courses) == len(total_class))
            and (len(total_present) == len(total_class))
            and (len(total_present) == len(courses))
        ):
            response_data = {}
            for item in range(len(courses)):
                temp = {}
                temp["total_hours"] = int(total_class[item])
                temp["total_present"] = int(total_present[item])
                percentage_of_attendance = temp["total_present"] / temp["total_hours"]
                percentage_of_attendance = round(percentage_of_attendance, 2)

                temp["percentage_of_attendance"] = percentage_of_attendance
                if (percentage_of_attendance) <= (threshold):
                    temp["class_to_attend"] = math.ceil(
                        ((threshold * temp["total_hours"]) - temp["total_present"])
                        / (1 - threshold)
                    )

                else:
                    temp["class_to_bunk"] = math.floor(
                        (temp["total_present"] - (threshold * temp["total_hours"]))
                        / (threshold)
                    )

                response_data[courses[item]] = temp

            return jsonify(response_data)

        else:
            response = {"error": "check input details!!"}
            return jsonify(response)

    except:
        response = {"error": "Given input details does not match up!!"}
        return jsonify(response)
