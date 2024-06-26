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
    hospital=db.execute(f"select name,phone_number,mail,image,description from hospital ");
    dic = {}
    return render_template("home.html",stocks=dic)

@app.route("/hospital")
def hospital():
    
    return render_template("hospital.html")



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
    print(password,confirm_password)
    if not (name or password or confirm_Password):
      return ("Try filling all")
    if password != confirm_password:
      return ("Passwords do not match")
    if request.form.get("type")=="user":
      db.execute("INSERT INTO user (name, mail, phone_number,hash,age,gender) VALUES(?,?,?,?,?,?)",
                 name, 
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

        session["user_id"] = rows[0]["id"]
        return redirect("/hospital")

  
    return render_template("login.html")
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/login")
@app.route("/show_preview",methods=["GET","POST"])

def show_preview():
    if request.method =="GET":
        return ("sorry error")
    image_url = request.form.get("image")
    hospital = db.execute("select * from hospital where image=?",image)

    
    return render_template("preview.html",hospital=hospital[0])
 
