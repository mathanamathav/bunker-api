from flask import Flask, request, render_template,jsonify,flash
import bunker_mod as bk
import requests
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'




# @app.route('/',methods=['GET'])
# def home():
#     return render_template('home.html')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        username = request.form.get("usr")
        pwd = request.form.get("pwd")
        table = bk.return_attendance(username,pwd)
        if table != "Invalid password" and table != "Try again after some time":
            print(table)
            res = bk.data_json(table)

            courses = []
            total_class = []
            total_present = []

            for course in res:
                courses.append(course)
                total_class.append(res[course]['total_hours'])
                total_present.append(res[course]['total_present'])


            graphJSON = bk.line_chart(courses,total_class,total_present,"Bar plot -- (Total Class VS present)")
            
            graphJSON2 = bk.pie_chart(courses,total_class,"Distribution of Classes")

            graphJSON3 = bk.pie_chart(courses,total_present,"Distribution of Attendance")




            return render_template("output.html",load=True,data=res,graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3)
            return str(bk.return_attendance(username,pwd))
        else:
            return render_template("output.html",load=False)
        
    return render_template("home.html")

@app.route('/send_attendance/<username>/<pwd>',methods=['POST'])
def send_attendance(username,pwd):
    if request.method == "POST":
        print(username,pwd)
        table = bk.return_attendance(username,pwd)
        res = bk.data_json(table)

        return jsonify(res)






if __name__=="__main__":
    app.run(host='0.0.0.0',port=4000,debug=True)



