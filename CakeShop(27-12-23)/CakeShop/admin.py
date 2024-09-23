from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector


def adminlogin():
    if request.method == "GET":
        return render_template("adminlogin.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        sql = "select count(*) from userinfo where username = %s and password=%s"
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        result = cursor.fetchone()
        con.close()
        print(result)
        if (int(result[0]) == 1):
            session["uname"] = uname
            return redirect("/AdminPage")
        else:
            return redirect(url_for("adminlogin"))
        

def adminLogout():
    session.clear()
    return redirect(url_for("adminlogin"))
    

def adminPage():
    if "uname" in session:
        return render_template("adminpage.html")
    else:
        return redirect(url_for("adminlogin"))