import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
page=0
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///list.db")

@app.route("/")
def index():
   return redirect("/login")

@app.route("/home")
def home():
    try:
       hospitals=db.execute("select name,phone_number,mail,image,description from hospital ")

    except Exception as e:
       hospitals = []
    return render_template("home.html",hospitals=hospitals)


@app.route("/hospital")
def hospital():
    hospital_id=session["hospital_id"]
    hospital=db.execute("select * from hospital where id=?",hospital_id)
    hname=hospital[0]["name"]
    appiontments=db.execute("select * from appiontment where hname=?",hname)

    return render_template("hospital.html",hospital=hospital[0],appiontments=appiontments)



@app.route("/hospital_details",methods=["GET","POST"])
def hospital_details():
    
    if request.method =="GET":
        return ("sorry error")
    if request.method =="POST":
          gmail = request.form.get("mail")
          hospital = db.execute("select * from hospital where mail=?",gmail)
          
    return render_template("hospital_details.html",hospital=hospital[0])

@app.route("/appiontment", methods=["GET", "POST"])
def appiontment():
  if request.method == "GET":
    return("sorry error")
  if request.method == "POST":
    hname = request.form.get("hname")
    himage = request.form.get("himage")


    user=session["user_id"]
    
    name = request.form.get("username")
    gmail = request.form.get("mail")
    phone_number = request.form.get("phone_number")
    age = request.form.get("age")
    gender = request.form.get("gender")
    problem= request.form.get("problem")
    appointment_time = request.form['appointment_time']
    db.execute("INSERT INTO appiontment (name, mail, phone_number,problem,age,gender,hname,by_user,himage , time ) VALUES(?,?,?,?,?,?,?,?,?,?)",
                 name, 
                 gmail, 
                 phone_number, 
                 problem,
                  age,
                  gender,
                  hname,
                  user,
                  himage,
                  appointment_time
                  
                  )
    return redirect("/home")
  
  return render_template("appiontment.html")



@app.route("/register", methods=["GET", "POST"])
def register():
  """Register user_completed"""
  if request.method == "GET":
    return render_template("register.html")
  if request.method == "POST":
    name = request.form.get("username")
    gmail = request.form.get("mail")
    phone_number = request.form.get("phone_number")
    age = request.form.get("age")
    gender = request.form.get("gender")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_Password")
    image = request.form.get("image")
    if not (name or password or confirm_Password):
      return ("Try filling all")
    if password != confirm_password:
      return ("Passwords do not match")
    if request.form.get("type")=="user":
      db.execute("INSERT INTO user (name,image , mail, phone_number,hash,age,gender) VALUES(?,?,?,?,?,?,?)",
                 name, 
                 image,
                 gmail, 
                 phone_number, 
                 generate_password_hash(password),
                  age,
                  gender
                  )
                  
    else:
         
            db.execute("INSERT INTO hospital (name, mail, phone_number,hash) VALUES(?,?,?,?)",
                 name, 
                 gmail, 
                 phone_number, 
                 generate_password_hash(password)
                   )
        
    return redirect("/login")
  
  return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """LOG USER IN"""
    session.clear()
    page=0
    if request.method == "POST":
       if not request.form.get("mail"):
          return ("Enter username",403)
       elif not request.form.get("password"):
          return ("Enter password",403)
        
       if request.form.get("type")=="user":
          rows = db.execute("SELECT * FROM user WHERE mail = ?", request.form.get("mail"))
        
          if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("Invalid username and/or password",403)

          session["user_id"] = rows[0]["id"]
          return redirect("/home")
          
          
    
       else:
        rows = db.execute("SELECT * FROM hospital WHERE mail = ?", request.form.get("mail")
          )

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
          return ("Invalid username and/or password",403)
        

        session["hospital_id"] = rows[0]["id"]
        return redirect("/hospital")

  
    return render_template("login.html")
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")

@app.route("/appiontment_",methods=["GET","POST"])
def appiontment_():
    if request.method == "POST":
       mail=request.form.get("mail")
       hospital = db.execute("select * from hospital where mail=?",mail)
       return render_template("appiontment.html",hospital=hospital[0])

@app.route("/meeting")
def meeting():
    user_id=session["user_id"]
    appiontments=db.execute("select * from appiontment where by_user=?",user_id)
    return render_template("meeting.html",appiontments=appiontments)

  




 
