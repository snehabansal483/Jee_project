from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Database Connection Configuration
# CHANGE THESE VALUES TO MATCH YOUR MYSQL SETUP
db_config = {
    'host': 'localhost',
    'user': 'root',      # Default MySQL username
    'password': 'Sneha@28',      # Default MySQL password (often empty or 'password')
    'database': 'jee_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('index'))
    else:
        flash('Database connection failed!', 'error')
        return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return render_template('signup.html')
            
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('signup.html')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Username already exists! Please choose a different one.', 'error')
                cursor.close()
                conn.close()
                return render_template('signup.html')
            
            # Insert new user (default role is student)
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                         (username, password, 'student'))
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Registration successful! Please login with your credentials.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Database connection failed!', 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- Admin Routes ---

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    questions = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM questions ORDER BY id DESC") # Newest first
        questions = cursor.fetchall()
        cursor.close()
        conn.close()
        
    return render_template('admin_dashboard.html', questions=questions)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        question_text = request.form['question_text']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_answer = request.form['correct_answer']
        difficulty = request.form['difficulty']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            sql = """INSERT INTO questions 
                     (subject, chapter, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (subject, chapter, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            flash('Question added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

    return render_template('add_question.html')

@app.route('/edit_question/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))

    conn = get_db_connection()
    if not conn:
        return "DB Error"

    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        question_text = request.form['question_text']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_answer = request.form['correct_answer']
        difficulty = request.form['difficulty']

        sql = """UPDATE questions SET 
                 subject=%s, chapter=%s, question_text=%s, 
                 option_a=%s, option_b=%s, option_c=%s, option_d=%s, 
                 correct_answer=%s, difficulty=%s 
                 WHERE id=%s"""
        val = (subject, chapter, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty, id)
        
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    # GET request - fetch existing data
    cursor.execute("SELECT * FROM questions WHERE id = %s", (id,))
    question = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('edit_question.html', question=question)

@app.route('/delete_question/<int:id>')
def delete_question(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Question deleted successfully!', 'success')
        
    return redirect(url_for('admin_dashboard'))

# --- Student Routes ---

@app.route('/student_dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('index'))
    
    # Get unique subjects and chapters for filtering
    conn = get_db_connection()
    subjects = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT subject FROM questions")
        subjects = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
    return render_template('student_dashboard.html', subjects=subjects)

@app.route('/practice', methods=['GET'])
def practice():
    if 'role' not in session or session['role'] != 'student':
        return redirect(url_for('index'))
        
    subject = request.args.get('subject')
    conn = get_db_connection()
    questions = []
    
    if conn:
        cursor = conn.cursor(dictionary=True)
        if subject:
             # If a subject is selected, filter by it
            cursor.execute("SELECT * FROM questions WHERE subject = %s", (subject,))
        else:
            # Otherwise show all
            cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        cursor.close()
        conn.close()
        
    return render_template('practice.html', questions=questions, subject=subject)

if __name__ == '__main__':
    app.run(debug=True)
