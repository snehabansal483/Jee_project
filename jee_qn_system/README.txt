JEE Main Question-Answer Management System
==========================================

This is a simple, beginner-friendly web application to manage and practice JEE questions.
It is built using Python (Flask), MySQL, HTML, and CSS.

Folder Structure
----------------
jee_qn_system/
  |-- app.py              (The main Python backend code)
  |-- database.sql        (SQL script to set up the database)
  |-- templates/          (HTML files)
  |   |-- login.html
  |   |-- admin_dashboard.html
  |   |-- add_question.html
  |   |-- edit_question.html
  |   |-- student_dashboard.html
  |   |-- practice.html
  |-- static/             (CSS file)
      |-- style.css

Prerequisites
-------------
1. Python installed (Add to PATH during installation).
2. MySQL Server installed (e.g., MySQL Workbench or XAMPP).
3. VS Code (Visual Studio Code).

Step 1: Install Required Python Libraries
-----------------------------------------
Open your terminal (Command Prompt or VS Code Terminal) and run:

    pip install flask mysql-connector-python

Step 2: Database Setup
----------------------
1. Open your MySQL tool (MySQL Workbench or phpMyAdmin if using XAMPP).
2. Open the file `database.sql` provided in this folder.
3. Run the script to create the `jee_db` database, `users` table, and `questions` table.
   It also inserts some dummy data for you.

Step 3: Configure Database Connection
-------------------------------------
1. Open `app.py` in VS Code.
2. Look for the `db_config` section (lines 7-12).
3. Change the 'user' and 'password' fields to match your MySQL installation.
   - Default user is often 'root'.
   - Default password might be empty or 'root' or 'password'.

   Example:
   db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': 'your_mysql_password',
       'database': 'jee_db'
   }

Step 4: Run the Application
---------------------------
1. In VS Code, open the terminal in the `jee_qn_system` folder.
2. Run the command:

    can python app.py

3. You will see output like `Running on http://127.0.0.1:5000`.
4. Open your Chrome browser and go to `http://127.0.0.1:5000`.

Step 5: How to Use
------------------
1. Login Page:
   - Admin Login: Username `admin`, Password `admin123`
   - Student Login: Username `student`, Password `student123`

2. Admin Dashboard:
   - Click "Add New Question" to add physics/math/chem questions.
   - View the list of all questions.
   - Edit or Delete questions using the buttons.

3. Student Dashboard:
   - Select a subject or choose "Start Practice" for mixed questions.
   - In the practice view, try to solve the question.
   - Click "Show Answer" to reveal the correct option.

Troubleshooting
---------------
- If you see "Database connection failed!", check your username/password in `app.py`.
- If you see "Module not found", make sure you ran `pip install ...`.
