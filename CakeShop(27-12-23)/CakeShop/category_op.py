from flask import Flask,render_template,request,redirect
import mysql.connector

def showAllCategories():
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    con.close()
    return render_template("showAllCategories.html",cats = result)

def addCategory():
    if request.method == "GET":
        return render_template("addNewCategory.html")
    else:
        cname = request.form["cname"]
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        sql = "insert into Category (cname) values (%s)"
        val = (cname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()        
        return redirect("/ShowAllCategories")

def editCategory(cid):
    if request.method == "GET":
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        sql = "select * from category where cid=%s"
        val = (cid,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        result = cursor.fetchone()
        con.close()
        return render_template("editCategory.html",cat=result)
    else:
        cname = request.form["cname"]
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        sql = "update Category set cname=%s where cid=%s"
        val = (cname,cid)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()        
        return redirect("/ShowAllCategories")

def deleteCategory(cid):
    if request.method == "GET":
        return render_template("deleteConfirm.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
            sql = "delete from category where cid=%s"
            val = (cid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/ShowAllCategories")




