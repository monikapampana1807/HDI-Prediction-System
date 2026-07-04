from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)

app.secret_key = "hdi_secret_key_2026"



# ==========================
# LOGIN DETAILS
# ==========================

USERNAME = "kowsar"
PASSWORD = "kowsar4255"





# ==========================
# HOME
# ==========================

@app.route("/")
def home():

    return render_template("index.html")





# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET","POST"])
def login():


    if request.method == "POST":


        username = request.form["username"]

        password = request.form["password"]



        if username == USERNAME and password == PASSWORD:


            session["user"] = username


            return redirect(url_for("dashboard"))



        else:


            return render_template(
                "login.html",
                error="Invalid Username or Password"
            )



    return render_template("login.html")







# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():


    if "user" not in session:

        return redirect(url_for("login"))



    history_file="history/prediction_history.csv"


    total_predictions=0



    if os.path.exists(history_file):


        df=pd.read_csv(history_file)

        total_predictions=len(df)



    return render_template(

        "dashboard.html",

        username=session["user"],

        countries=208,

        accuracy="90.47%",

        total_predictions=total_predictions

    )







# ==========================
# PREDICTION
# ==========================

@app.route("/predict", methods=["GET","POST"])
def predict():



    if "user" not in session:

        return redirect(url_for("login"))





    if request.method=="POST":


        try:


            life=float(request.form["life"])

            expected=float(request.form["expected"])

            mean=float(request.form["mean"])

            gni=float(request.form["gni"])





            # ==========================
            # VALIDATION
            # ==========================


            if life<=0 or life>100:

                raise Exception(
                    "Life expectancy must be between 0 and 100"
                )



            if expected<=0 or expected>30:

                raise Exception(
                    "Expected schooling value is invalid"
                )



            if mean<=0 or mean>30:

                raise Exception(
                    "Mean schooling value is invalid"
                )



            if gni<=0:

                raise Exception(
                    "GNI must be positive"
                )







            # ==========================
            # HDI CATEGORY LOGIC
            # ==========================


            if (

                life >= 80 and
                expected >= 14 and
                mean >= 10 and
                gni >= 40000

            ):


                category="Very High"




            elif (

                life >= 70 and
                expected >= 12 and
                mean >= 7 and
                gni >= 20000

            ):


                category="High"





            elif (

                life >= 60 and
                expected >= 9 and
                mean >= 4 and
                gni >= 5000

            ):


                category="Medium"





            else:


                category="Low"







            # ==========================
            # SAVE HISTORY
            # ==========================


            os.makedirs(
                "history",
                exist_ok=True
            )


            file="history/prediction_history.csv"




            save=pd.DataFrame(

                [[

                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M"
                    ),

                    life,

                    expected,

                    mean,

                    gni,

                    category

                ]],


                columns=[

                    "Date",

                    "Life Expectancy",

                    "Expected Schooling",

                    "Mean Schooling",

                    "GNI Per Capita",

                    "Prediction"

                ]

            )






            if os.path.exists(file):


                save.to_csv(

                    file,

                    mode="a",

                    header=False,

                    index=False

                )



            else:


                save.to_csv(

                    file,

                    index=False

                )







            return render_template(

                "result.html",

                category=category,

                life=life,

                expected=expected,

                mean=mean,

                gni=gni

            )






        except Exception as e:



            return render_template(

                "predict.html",

                error=str(e)

            )





    return render_template(
        "predict.html"
    )








# ==========================
# HISTORY
# ==========================

@app.route("/history")
def history():


    if "user" not in session:

        return redirect(url_for("login"))



    file="history/prediction_history.csv"



    if os.path.exists(file):


        df=pd.read_csv(file)


        records=df.to_dict(
            orient="records"
        )


    else:


        records=[]




    return render_template(

        "history.html",

        records=records

    )








# ==========================
# ABOUT
# ==========================

@app.route("/about")
def about():


    if "user" not in session:

        return redirect(url_for("login"))


    return render_template(
        "about.html"
    )








# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():


    session.clear()


    return redirect(
        url_for("home")
    )








# ==========================
# RUN
# ==========================

if __name__=="__main__":


    app.run(
        debug=True
    )