from app import app
@app.route("/employer")
@app.route("/employer/dashboard")
def employer():
    return "<h1>Employer dashboard<?h1>"

@app.route("/employer/profile")
def employerProfile():
    return "<h1>Employer profile<?h1>"

@app.route("/employer/login")
def employerLogin():
    return "<h1>Employer sign in<?h1>"

@app.route("/employer/logout")
def employerLogout():
    return "<h1>Employer log out<?h1>"