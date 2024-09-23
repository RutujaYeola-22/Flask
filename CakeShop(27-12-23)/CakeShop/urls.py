from main import app
import category_op as ct
import cake_op as ck
import admin as ad
import users as us
#-----------Category Urls=----------------------
#1st pameter is url,2nd parameter is function name
app.add_url_rule('/ShowAllCategories', view_func=ct.showAllCategories)
app.add_url_rule("/addCategory",view_func=ct.addCategory,methods=["GET","POST"])
app.add_url_rule("/edit_cat/<cid>",view_func=ct.editCategory,methods=["GET","POST"])
app.add_url_rule("/delete_cat/<cid>",view_func=ct.deleteCategory,methods=["GET","POST"])

#---------------Cake Urls --------------------
app.add_url_rule("/AddCake",view_func=ck.addCake,methods=["GET","POST"])
app.add_url_rule("/ShowAllCakes",view_func=ck.showAllCakes)

#-----------------------------------------------------------
app.add_url_rule("/adminLogin",view_func=ad.adminlogin,methods=["GET","POST"])
app.add_url_rule("/AdminPage",view_func=ad.adminPage)
app.add_url_rule("/AdminLogout",view_func=ad.adminLogout)

#----------------------------------------------------------------
app.add_url_rule("/",view_func=us.homepage)
app.add_url_rule("/ShowCakes/<cid>",view_func=us.showCakes)
app.add_url_rule("/ViewDetails/<cake_id>",view_func=us.ViewDetails)
app.add_url_rule("/login",view_func=us.login,methods=["GET","POST"])
app.add_url_rule("/signup",view_func=us.signup,methods=["GET","POST"])
app.add_url_rule("/logout",view_func=us.logout,methods=["GET","POST"])
app.add_url_rule("/addToCart",view_func=us.addToCart,methods=["POST"])
app.add_url_rule("/ShowCart",view_func=us.ShowCart,methods=["GET","POST"])
app.add_url_rule("/MakePayment",view_func=us.MakePayment,methods=["GET","POST"])
