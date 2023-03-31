# Online Job-Seeker Portal Project using Flask - Python Framework
live at https://amwata.pythonanywhere.com/


<b>-------- Project Tree Structure---------</b>

<pre>
├── main.py (Main module that runs the project Application)
├── OraApp (Job Portal Application package)
│   ├── admin (Admin Package with routes module)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── applicants (Applicants Package with routes module)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── employers (Employers Package with routes module)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── errors (Errors Package with handlers module for custom errors)
│   │   ├── handlers.py
│   │   └── __init__.py
│   ├── forms.py (Forms Module with Flask Forms Class for generating html forms)
│   ├── __init__.py
│   ├── jobs (Jobs Package with routes module)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main (Main Package with routes module)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models.py (Modules for creating relational database tables)
│   |
│   ├── static (DIR for including external css, javascript or images)
│   │   ├── admin
│   │   ├── applicant
│   │   ├── css
│   │   ├── employer
│   │   ├── img
│   │   └── js
│   ├── templates (DIR for sub-directories and files with html contents)
│   │   ├── about.html
│   │   ├── admin
│   │   ├── applicants
│   │   ├── base.html
│   │   ├── email.html
│   │   ├── employers
│   │   ├── errors
│   │   ├── forgot_password.html
│   │   ├── index.html
│   │   ├── jobs
│   │   ├── job-search.html
│   │   ├── mail-styles.html
│   │   └── reset_password.html
│   └── utils.py (a module for additional python functions)
├── oracom-env (Project Virtual Environment with installed Flask App requirements)
├── README.md
└── requirements.txt (List of Packages and Modules required for the Application)
</pre>
