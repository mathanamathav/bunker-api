from flask import Flask, request, render_template,jsonify
import bunker_mod as bk
import requests


app = Flask(__name__)




# @app.route('/',methods=['GET'])
# def home():
#     return render_template('home.html')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
        username = request.form.get("usr")
        pwd = request.form.get("pwd")
        table = bk.return_attendance(username,pwd)
        res = bk.data_json(table)

        return render_template("output.html",table = res)
        return str(bk.return_attendance(username,pwd))
        
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



