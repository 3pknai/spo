from flask import Flask, render_template, url_for, request, flash, session, redirect, send_from_directory
import os
from database_connect import *
import hashlib
from data_validate import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "d1u292ueh2192uidJDWJIODJO!*@*@Y@*!HU@DH@*"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=["GET", "POST"])
def index():
    if "userLogged" in session and request.method == "GET":
        return render_template("index.html", name=session["userLogged"])
    elif "userLogged" in session and request.method == "POST":
        print(session["userLogged"])
        del session["userLogged"]
        return redirect(url_for("home"))
    else:
        return render_template("index.html", name="")
    
@app.route("/analyze/search", methods=["GET", "POST"])
def analyze_search():
    if "userLogged" in session and request.method == "GET":
        return render_template("analyzes_search.html", name=session["userLogged"], tests=tests_info("%", "", ""))
    elif "userLogged" in session and request.method == "POST":
        req = request.form
        analyzename = req["analyzename"]
        cost_l = req["cost_l"]
        cost_r = req["cost_r"]
        return render_template("analyzes_search.html", name=session["userLogged"], tests=tests_info(f"%{analyzename}%", cost_l, cost_r), cost_l=cost_l, cost_r=cost_r, analyzename=analyzename)
    else:
        return redirect(url_for("home"))

@app.route("/analyze/create/<int:test_id>", methods=["GET", "POST"])
def analyze_create(test_id):
    if "userLogged" in session and request.method == "GET":
        if role(session["userLogged"]) == "Пациент":
            test = test_info(test_id)
            return render_template("analyze_create.html", name=session["userLogged"], test=test, id=test_id)
        else:
            return redirect(url_for("homehistory"))
    elif "userLogged" in session and request.method == "POST":
        if role(session["userLogged"]) == "Пациент":
            req = request.form
            date = req["date"]
            create_analyze(session["userLogged"], test_id, date)
        return redirect(url_for("homehistory"))
    else:
        return redirect(url_for("home"))
    
@app.route("/analyze/update/<int:id>", methods=["GET", "POST"])
def analyze_update(id):
    if "userLogged" in session and request.method == "GET" and user_have_analyze(session["userLogged"], id):
        if role(session["userLogged"]) == "Пациент":
            info = analyze_info(id)
            return render_template("analyze_update.html", name=session["userLogged"], date=info["date"], nameanalyze=info["name"], cost=info["cost"], id=id)
        else:
            return redirect(url_for("homehistory"))
    elif "userLogged" in session and request.method == "POST" and user_have_analyze(session["userLogged"], id):
        if role(session["userLogged"]) == "Пациент":
            req = request.form
            date = req["date"]
            update_analyze_info(id, date)
            return redirect(url_for("homehistory"))
        else:
            return redirect(url_for("homehistory"))
    else:
        return redirect(url_for("homehistory"))

@app.route("/analyze/delete/<int:id>", methods=["GET", "POST"])
def analyze_delete(id):
    if "userLogged" in session and request.method == "GET" and user_have_analyze(session["userLogged"], id):
        if role(session["userLogged"]) == "Пациент":
            delete_analyze_info(id)
    return redirect(url_for("homehistory"))


@app.route("/home", methods=["GET", "POST"])
def home():
    if "userLogged" in session and request.method == "GET":
        info = user_large_info(session["userLogged"])
        print(info)
        return render_template("home.html", name=session["userLogged"], role=role(session["userLogged"]), fullname=info["full_name"], address=info["address"], birth=info["birth_date"], gender=info["gender"], interes=info["interests"], vk=info["vk_profile"], blood=info["blood_type"], rz=info["rh_factor"])
    elif "userLogged" in session and request.method == "POST":
        del session["userLogged"]
        return redirect(url_for("auth"))
    else:
        return redirect(url_for("auth"))
    
@app.route("/home/history", methods=["GET", "POST"])
def homehistory():
    if "userLogged" in session and request.method == "GET":
        if role(session["userLogged"]) == "Пациент":
            return render_template("home_history.html", name=session["userLogged"], sicks=user_history_sickleaves(session["userLogged"]), analyzes=user_history_analyzes(session["userLogged"]))
        else:
            return render_template("home_history.html", name=session["userLogged"])
    elif "userLogged" in session and request.method == "POST" and role(session["userLogged"]) != "Пациент":
        None
    else:
        return redirect(url_for("auth"))
    
@app.route("/home/update", methods=["GET", "POST"])
def homeupdate():
    users = user_list()
    print(users)

    if "userLogged" in session and request.method == "GET":
        if role(session["userLogged"]) == "Пациент":
            info = user_info(session["userLogged"])
            print(info)

            return render_template("home_update.html", name=session["userLogged"], address=info["address"], gender=info["gender"], interes=info["interests"], vk=info["vk_profile"], blood=info["blood_type"], rz=info["rh_factor"])
        else:
            return render_template("home_update.html", name=session["userLogged"], address=info["address"], gender=info["gender"], interes=info["interests"], vk=info["vk_profile"], blood=info["blood_type"], rz=info["rh_factor"])
    elif "userLogged" in session and request.method == "POST" and role(session["userLogged"]) == "Пациент":
        req = request.form

        password = req["password"]
        address = req["address"]
        gender = req["gender"]
        interes = req["interes"]
        vk = req["vk"]
        blood = req["blood"]
        rz = req["rz"]

        if len(password) >= 6 and big_lat(password) and small_lat(password) and spec(password) and digit(password) and not rus(password):
            save_user_info(session["userLogged"], password, address, gender, interes, vk, blood, rz)
            info = user_info(session["userLogged"])
            print(info)
            return render_template("home_update.html", name=session["userLogged"], address=info["address"], gender=info["gender"], interes=info["interests"], vk=info["vk_profile"], blood=info["blood_type"], rz=info["rh_factor"])
        else:
            info = user_info(session["userLogged"])
            print(info)
            return render_template("home_update.html", name=session["userLogged"], warning_password=True, address=info["address"], gender=info["gender"], interes=info["interests"], vk=info["vk_profile"], blood=info["blood_type"], rz=info["rh_factor"])
    else:
        return redirect(url_for("auth"))

@app.route("/home/delete", methods=["GET"])
def homedelete():
    if "userLogged" in session and role(session["userLogged"]) == "Пациент":
        delete_user(session["userLogged"])
        del session["userLogged"]
    return redirect(url_for("auth"))


@app.route("/auth", methods=["POST", "GET"])
def auth():
    users = user_list()
    print(users)
    if "userLogged" in session:
        return redirect(url_for("home"))
    elif request.method == "POST" and request.form["username"] in users and hashlib.sha256(request.form["password"].encode()).hexdigest() == users[request.form["username"]]:
        session["userLogged"] = request.form["username"]
        return redirect(url_for("home"))
    elif request.method == "POST":
        return render_template("auth.html", name="", not_correct_data=True)
    else:
        return render_template("auth.html", name="")
    
@app.route("/reg", methods=["POST", "GET"])
def reg():
    users = user_list()
    print(users)
    if "userLogged" in session:
        return redirect(url_for("home"))
    elif request.method == "POST":
        req = request.form

        fullname = req["fullname"]
        login = req["username"]
        password = req["password"]
        date = req["databirth"]
        address = req["address"]
        gender = req["gender"]
        interes = req["interes"]
        vk = req["vk"]
        blood = req["blood"]
        rz = req["rz"]

        print(gender)
        g = {"Male": "Мужской", "Female": "Женский", 'None': "---"}

        if len(password) >= 6 and big_lat(password) and small_lat(password) and spec(password) and digit(password) and not rus(password):
            if login not in users:
                reg_user(fullname, login, password, date, address, gender, interes, vk, blood, rz)
                session["userLogged"] = login
                return redirect(url_for("home"))
            else:
                return render_template("reg.html", name="", user_already=True, fullname=fullname, username=login, databirth=date, address=address, gender=g[gender], interes=interes, vk=vk, blood=blood, rz=rz)
        else:
            return render_template("reg.html", name="", warning_password=True, fullname=fullname, username=login, databirth=date, address=address, gender=g[gender], interes=interes, vk=vk, blood=blood, rz=rz)
    else:
        return render_template("reg.html", name="")

@app.errorhandler(404)
def pageNotFount(error):
    return render_template("page404.html", title="Страница не найдена")

if __name__ == "__main__":
    app.run(debug=True)