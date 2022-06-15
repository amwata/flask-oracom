from app import app
@app.route("/admin")
@app.route("/admin/dashboard")
def admin():
    return "<h1>Admin dashboard<?h1>"

@app.route("/admin/profile")
def adminProfile():
    return "<h1>Admin profile<?h1>"

@app.route("/admin/login")
def adminLogin():
    return "<h1>Admin sign in<?h1>"

@app.route("/admin/logout")
def adminLogout():
    return "<h1>Admin log out<?h1>"