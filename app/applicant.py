from app import app

@app.route("/applicant/<name>")
@app.route("/applicant")
@app.route("/applicant/dashboard")
def applicant(name):
    return f"<h1>applicant dashboard<br>{name}<?h1>"

@app.route("/applicant/profile")
@app.route("/applicant/profile/<name>")
def applicantProfile(name):
    return f"<h1>Applicant profile<br>{name}<?h1>"

@app.route("/applicant/login")
def applicantLogin():
    return "<h1>Applicant sign in<?h1>"

@app.route("/applicant/logout")
def applicantLogout():
    return "<h1>Applicant log out<?h1>"