from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
from werkzeug.utils import secure_filename

def showAllCakes():
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    sql = "select c.cakeid,c.cake_name,c.price,c.description,c.image_url,c.quantity,t.cname from cake c inner join category t on c.cat_id = t.cid"
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    con.close()
    return render_template("showAllCakes.html",cakes = result)

def addCake():
    if request.method == "GET":
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        con.close()
        return render_template("addNewCake.html",cats=result)
    else:
        cname = request.form["cname"]
        price = request.form["price"]
        desc = request.form["desc"]
        qty = request.form["qty"]
        cid = request.form["cat"]
        f = request.files['image_url'] 
        filename = secure_filename(f.filename)
        filename = "static/Images/"+f.filename
        #This will save the file to the specified location
        f.save(filename)   
        filename = "Images/"+f.filename
        
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        sql = "insert into Cake(cake_name,price,description,image_url,quantity,cat_id) values (%s,%s,%s,%s,%s,%s)"
        val = (cname,price,desc,filename,qty,cid)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()        
        return redirect(url_for('showAllCakes'))
        
        
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




