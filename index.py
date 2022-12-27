from flask import Flask, request, render_template,jsonify,flash
import bunker_mod as bk
# import requests
import pandas as pd
# import plotly
import math
# import plotly.express as px
# import plotly.graph_objects as go



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        username = request.form.get("usr")
        pwd = request.form.get("pwd")

        try:
            table,session = bk.return_attendance(username,pwd)
        except:
            table = bk.return_attendance(username,pwd)



        if table != "Invalid password" and table != "Try again after some time" and table != "Table is being updated":
            
            res = bk.data_json(table)

            courses = []
            total_class = []
            total_present = []
            specs = []
            subplot_titles = []
            labels = ['total_hours','total_present']

            for course in res:

                courses.append(course['name'])
                total_class.append(course['total_hours'])
                total_present.append(course['total_present'])
                specs.append([{'type':'domain'}])
                subplot_titles.append("Course Code "+course['name'])
                

            time_table = bk.return_timetable(session)


            # graphJSON = bk.line_chart(courses,total_class,total_present,"Bar plot -- (Total Class VS present)")
            
            # graphJSON2 = bk.pie_chart(courses,total_class,"Distribution of Classes")

            # graphJSON3 = bk.pie_chart(courses,total_present,"Distribution of Attendance")

            # graphJSON4 = bk.many_pieplot(res,specs,subplot_titles,labels,total_class,total_present)


            return render_template("output.html",load=True,time_table=time_table,data=res)
            # return render_template("output.html",load=True,time_table=time_table,data=res,graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4)
        else:
            return render_template("output.html",load=False,text=table)
        
    return render_template("home.html")

@app.route('/send_attendance/<username>/<pwd>',methods=['POST'])
def send_attendance(username,pwd):
    if request.method == "POST":
        try: 
            try:
                table,session = bk.return_attendance(username,pwd)
            except:
                table = bk.return_attendance(username,pwd)

            if table != "Invalid password" and table != "Try again after some time" and table != "Table is being updated":
                res = bk.data_json(table)

                return jsonify(res)
            else:
                res = {"error" : "Invalid details try again"}
                return jsonify(res)
        
        except:
            response = {"error" : "Given input details does not match up!!"}
            return jsonify(response)


@app.route('/senddata_attendance',methods=['POST'])
def senddata_attendance():
    try : 
        input_json = request.get_json(force=True)
        courses = input_json['class_code']
        total_class = input_json['total_hours']
        total_present = input_json['total_present']
        threshold = int(input_json['threshold'])
        threshold = (threshold/100)


        if (len(courses) == len(total_class)) and (len(total_present) == len(total_class)) and (len(total_present) == len(courses)):
            response_data = {}
            for item in range(len(courses)):
                temp = {}
                temp['total_hours'] = int(total_class[item])
                temp['total_present'] = int(total_present[item])
                percentage_of_attendance = temp['total_present']/temp['total_hours']
                percentage_of_attendance = round(percentage_of_attendance,2)

                temp['percentage_of_attendance'] = percentage_of_attendance
                if (percentage_of_attendance) <= (threshold):
                    temp['class_to_attend'] = math.ceil(((threshold*temp['total_hours']) - temp['total_present'])/(1-threshold))
                
                else:
                    temp['class_to_bunk'] = math.floor((temp['total_present']-(threshold*temp['total_hours']))/(threshold))

                response_data[courses[item]] = temp

            return jsonify(response_data)
        
        else:
            response = {"error" : "check input details!!"}
            return jsonify(response)

        
    except:
        response = {"error" : "Given input details does not match up!!"}
        return jsonify(response)








    

    








if __name__=="__main__":
    app.run(host='0.0.0.0',port=4000,debug=True)



