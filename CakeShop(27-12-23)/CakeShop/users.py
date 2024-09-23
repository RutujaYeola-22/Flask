from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
from datetime import datetime

def homepage():
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    sql = "select * from cake"
    cursor = con.cursor()
    cursor.execute(sql)
    cakes = cursor.fetchall()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("homepage.html",cakes = cakes,cats=cats)

def showCakes(cid):
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    sql = "select * from cake where cat_id=%s"
    val = (cid,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    cakes = cursor.fetchall()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("homepage.html",cakes = cakes,cats=cats)

def ViewDetails(cake_id):
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    sql = "select * from cake where cakeid=%s"
    val = (cake_id,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    cake = cursor.fetchone()
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    con.close()
    return render_template("ViewDetails.html",cake = cake,cats=cats)

def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        sql = "select count(*) from userinfo where username = %s and password=%s and role='user'"
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        result = cursor.fetchone()
        con.close()        
        if (int(result[0]) == 1):
            session["uname"] = uname
            return redirect("/")
        else:
            return redirect(url_for("login"))

def checkDuplicate(uname):
    sql = "select count(*) from userinfo where username = %s and role='user'"
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    val = (uname,)
    cursor = con.cursor()
    cursor.execute(sql,val)
    result = cursor.fetchone()
    con.close()        
    if (int(result[0]) == 1):
        return True
    else:
        return False

def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        email = request.form["email"]
        result = checkDuplicate(uname)
        if(result):
            return render_template("signup.html", message="User Already Present,please user different user!!")
        else:
            sql = "insert into userinfo values (%s,%s,%s,'user')"
            con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
            val = (uname,pwd,email)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
            con.close()  
            return redirect("/")
    
def logout():
    session.clear()
    return redirect("/")

def addToCart():
    if "uname" in session:
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        cursor = con.cursor()
        
        uname = session["uname"]
        cakeid = request.form["cakeid"]
        qty = request.form["qty"]
        #Check for duplicate
        sql = "select count(*) from mycart where username=%s and cake_id=%s"
        val = (uname,cakeid)
        cursor.execute(sql,val)
        result = cursor.fetchone()[0]
        if(int(result) >= 1):
            return "Item already in cart"
        else:
            sql = "insert into mycart (username,cake_id,qty) values (%s,%s,%s)"
            val = (uname,cakeid,qty)
            cursor.execute(sql,val)
            con.commit()
        con.close()  
        return redirect("/")        
    else:
        return redirect("/login")
    
def ShowCart():
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    cursor = con.cursor()
    if request.method == "GET":        
        sql = "select * from mycart_vw where username=%s"
        val = (session["uname"],)        
        cursor.execute(sql,val)
        result = cursor.fetchall()
        sql = "select sum(subtotal) from mycart_vw where username=%s"
        val = (session["uname"],)
        cursor.execute(sql,val)
        sum = cursor.fetchone()[0]
        session["total"] = sum
        sql = "select * from category"
        cursor = con.cursor()
        cursor.execute(sql)
        cats = cursor.fetchall()
        return render_template("ShowCart.html",cakes=result,sum = sum,cats=cats)
    else:        
        action = request.form["action"]
        cakeid = request.form["cakeid"]
        uname = session["uname"]
        if(action == "delete"):           
            sql = "delete from mycart where cake_id=%s and username=%s"
            val = (cakeid,uname)
            
        else:
            qty = request.form["qty"]
            sql = "update mycart set qty=%s where cake_id=%s and username=%s"
            val = (qty,cakeid,uname)
            
        cursor.execute(sql,val)    
        con.commit()
        con.close()
        return redirect(url_for("ShowCart"))

def MakePayment():
    if request.method == "GET":
        message = request.args.get("message")
        return render_template("MakePayment.html",message = message) 
    else:
        uname= request.form["uname"]
        cardno = request.form["cardno"]
        cvv = request.form["cvv"]
        expiry = request.form["expiry"]
        sql = "select count(*) from mypayment where uname=%s and cardno=%s and cvv=%s and expiry=%s"
        val = (uname,cardno,cvv,expiry)
        con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
        cursor = con.cursor()
        cursor.execute(sql,val)
        data = cursor.fetchone()
        if int(data[0]) == 1:
            #Check for insufficient balance
            sql = "select balance from mypayment where uname=%s and cardno=%s and cvv=%s and expiry=%s"
            val = (uname,cardno,cvv,expiry)
            con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
            cursor = con.cursor()
            cursor.execute(sql,val)
            data = cursor.fetchone()
            if float(data[0] < session["total"]):
                message = "Insufficent balance"                
                return redirect(url_for("MakePayment",message=message))
            else:
                buyer = "update mypayment set balance=balance - %s where cardno=%s and cvv=%s"
                owner = "update mypayment set balance=balance + %s where cardno=444 and cvv=444"
                val1 = (session["total"],cardno,cvv)
                val2 = (session["total"],)
                cursor.execute(buyer,val1)
                cursor.execute(owner,val2)
                con.commit()
                updateorderMaster()
                return redirect("/")

        else:
            return redirect(url_for("MakePayment"))


def updateorderMaster():
    uname = session["uname"]
    sql = "select cake_id,qty from mycart where username=%s"
    val = (uname,)
    con = mysql.connector.connect(host="localhost",user="root",password="vaishali",database="cakeshopdb")
    cursor = con.cursor()
    cursor.execute(sql,val)
    result = cursor.fetchall()
    data = []
    for cake in result:
        cake = str(cake[0])+","+str(cake[1])
        data.append(cake)
    
    data = "|".join(data)
    sql = "insert into ordermaster (username,description,date_of_order,amount) values (%s,%s,%s,%s)"
    dd = datetime.now().strftime("%Y-%m-%d")
    val = (uname,data,dd,session["total"])
    cursor.execute(sql,val)
    con.commit()

    # Update Cake Table
    for cake in result:
        sql = "update cake set quantity = quantity-%s where cakeid=%s"
        val = (cake[1],cake[0])
        cursor.execute(sql,val)
    con.commit()

    sql = "delete from mycart where username=%s"
    val = (session["uname"],)
    cursor.execute(sql,val)
    con.commit()



        