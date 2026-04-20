from flask import Flask,render_template,redirect, request,url_for, session
import mysql.connector
from flask_mail import Mail,Message
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)
app.secret_key = 'projob_portal_secret_key'


app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = str(os.environ.get("MYSQL_PASSWORD"))
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")

def get_mysql_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )



# Email configuration 
mail_config = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465 ,
    "MAIL_USE_TLS": False,  
    "MAIL_USE_SSL":True,
    "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
    "MAIL_DEFAULT_SENDER" :"prathamsautomatedmails@gmail.com"
}

app.config.update(mail_config)
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)
        
        #Check for suspended acoount
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        cursor.execute("SELECT status FROM users WHERE username = %s", (username,))
        suspended_user = cursor.fetchone()

        cursor.close()
        connection.close()

        if suspended_user and suspended_user['status'] == 'suspended':
            return "Your account is suspended "
        elif user:
            # Successful login, redirect to dashboard
            session['username'] = username
            session['role'] = 'user'
            return redirect(url_for('user_dashboard'))
        else:
            # Invalid credentials, redirect back to the login page
            return "username or password is incorrect"

    return render_template('user-login.html')



@app.route('/user-signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Check if the username is already taken
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Username already exists, handle accordingly (e.g., display an error message)
            cursor.close()
            connection.close()
            return "Username already exists. Please choose a different username."

        # If the username is unique, insert the new user into the database
        cursor.execute('INSERT INTO users (username,password) VALUES (%s, %s)', (username, password))
        connection.commit()

        cursor.close()
        connection.close()

        # Successful signup, you can redirect to a login page or another page
        return render_template("user-half-step.html", username=username)

    return render_template('user-signup.html')

@app.route('/user-update-profile', methods=['GET', 'POST'])
def update():
    if 'username' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
        
    if request.method == 'GET':
        return render_template("user-update-profile.html")
        
    if request.method == 'POST':
        connection = get_mysql_connection()
        cursor = connection.cursor()
        username = session['username']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return "Passwords do not match. Please try again."
        
        # Update the user in the database
        update_query = "UPDATE users SET password=%s WHERE username=%s"
        cursor.execute(update_query, (password, username))
        connection.commit()
        cursor.close()
        connection.close()
        
        return "Password Updated successfully !! <br> Go back to <a href='/user-dashboard'>dashboard</a>"


@app.route('/employeer-login', methods=['POST','GET'])
def emp_login1():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute('SELECT username FROM employers WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            # Successful login, redirect to dashboard
            session['username'] = username
            session['role'] = 'employer'
            return redirect(url_for('employeer_dashboard'))
            
        else:
            # Invalid credentials, redirect back to the login page
            return "username or password is incorrect"
    return render_template('employeer-login.html')    



@app.route("/employeer-signup",methods=["POST","GET"])
def empsignup1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Check if the username is already taken
        cursor.execute('SELECT * FROM employers WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Username already exists, handle accordingly (e.g., display an error message)
            return "Username already exists. Please choose a different username."

        # If the username is unique, insert the new user into the database
        cursor.execute('INSERT INTO employers (username,password) VALUES (%s, %s)', (username, password))
        connection.commit()

        cursor.close()
        connection.close()

        # Successful signup, you can redirect to a login page or another page
        return render_template("employeer-half-step.html",username=username)

    return render_template('employeer-signup.html')


@app.route('/create-user-profile/<username>')
def dele(username):
    return render_template('create-user-profile.html',username=username)

@app.route('/create-user-profile/<username>', methods=['POST'])
def add_profile(username):
    connection = get_mysql_connection()
    cursor = connection.cursor()

    name = request.form['name']
    image = request.files['image']
    if image:
        image.save("static/images/user" + image.filename)
        image_path = "static/images/uer" + image.filename
        cursor.execute("UPDATE profiles SET name = %s, image = %s WHERE username = %s", (name, image_path, username))

        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('user_signedup'))

    
@app.route('/user-signedup')
def user_signedup():
    return render_template("user-signedup.html")


@app.route('/create-employeer-profile/<username>', methods=['GET','POST'])
def add_profile1(username):
    connection = get_mysql_connection()
    cursor = connection.cursor()

    nam = request.form ['name']
    image = request.files['image']
    if image:
        image.save("static/images/emp" + image.filename)
        image_path = "static/images/emp" + image.filename
        cursor.execute("UPDATE employeers_profiles SET name = %s, image = %s WHERE username = %s", (nam, image_path, username))

        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('employeer-signedup.html'))

@app.route('/employeer-signedup')
def emp_signedup():
    return render_template("employeer-signedup.html")


@app.route('/user-profile-search', methods=['GET', 'POST'])
def ups():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        search_query = request.form["profile"]
        cursor.execute("SELECT username FROM users WHERE username = %s", (search_query,))
        results = cursor.fetchall()
        connection.close()
        return render_template('user-profile-search-RES.html', results=results, query=search_query)
    else:
        return render_template('user-profile-search.html') 
    
@app.route('/user-job-search')
def ujs():
    return render_template("user-job-search.html")


@app.route('/user-job-search', methods=['GET', 'POST'])
def ujs1():
    connection = get_mysql_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        search_query = request.form["job"]

        connection = get_mysql_connection()
        if not connection:
            return "Error connecting to database"

        cursor = connection.cursor()

        try:
            query = "SELECT job_title, emp_name, job_description, job_status,stipend FROM jobs WHERE job_title LIKE %s"  # Use LIKE for partial matches
            cursor.execute(query, ("%{}%".format(search_query),))
            results = cursor.fetchall()

            return render_template('user-job-search-RES.html', results=results, query=search_query)
        except mysql.connector.Error as err:
            print("Error during job search:", err)
            return "Error searching for jobs"
        finally:
            cursor.close()
            connection.close()

    return render_template('user-job-search.html')  # Assuming a search form template exists


@app.route('/create-job',methods=["GET","POST"])
def cj():
    if 'username' not in session or session.get('role') != 'employer':
        return redirect(url_for('emp_login'))

    if request.method == "POST":
        connection = get_mysql_connection()
        cursor = connection.cursor()

        job_title= request.form["jobTitle"]
        HR_name= session['username']
        job_desc= request.form["jobDescription"]
        stipend= str(request.form["stipend"])
        option = request.form.get('checkbox')

        if option is None:
            option = "Filled"
        else:
            option="vacant"

        cursor.execute("INSERT INTO jobs (emp_name,job_title,job_description,job_status,stipend) VALUES ( %s ,%s, %s , %s, %s)",(HR_name,job_title,job_desc,option,stipend))
        connection.commit()

        cursor.close()
        connection.close()
        return "Job Created Successfully !!! <br> Go back to <a href='/employeer-dashboard'>dashboard</a>"

    return render_template("create-job.html")


@app.route("/edit-job/<int:id>", methods=['GET','POST'])
def edit_job(id):
    if 'username' not in session or session.get('role') != 'employer':
        return redirect(url_for('emp_login'))
        
    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == "POST":
        job_title = request.form["jobTitle"]
        job_desc = request.form["jobDescription"]
        stipend = str(request.form["stipend"])
        option = request.form.get('checkbox')
        if option is None:
            option = "Vacant"
        else:
            option = "Filled"
            
        cursor.execute("UPDATE jobs SET job_title = %s, job_description = %s, stipend = %s, job_status = %s WHERE id = %s AND emp_name = %s", 
                       (job_title, job_desc, stipend, option, id, session['username']))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('employeer_dashboard'))
        
    cursor.execute("SELECT * FROM jobs WHERE id = %s AND emp_name = %s", (id, session['username']))
    job = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if not job:
        return "Job not found", 404
        
    return render_template("edit-job.html", job=job)

@app.route('/delete-job/<int:id>', methods=['POST'])
def delete_job(id):
    if 'username' not in session or session.get('role') != 'employer':
        return redirect(url_for('emp_login'))
        
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = %s AND emp_name = %s", (id, session['username']))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('employeer_dashboard'))
    

@app.route("/apply-for-job")
def afj():
    return render_template("apply-for-job.html")

@app.route("/apply-for-job",methods=["GET",'POST'])
def afj1():
    if request.method == "POST":
        username=request.form["username"]
        email=request.form["email"]
        phone=request.form["phone"]
        #description=request.form["description"]
        resume=request.form["resume"]

        msg = Message("New Job application from " + username,
                      #sender=["prathamsautomatedmails@gmail.com"],
                  recipients=["prathamsautomatedmails@gmail.com"])
        msg.body = resume + "\n" + phone + '\n' + email

        mail.send(msg)

        return "Application successful "



@app.route("/view-profile/<query>")
def view_profile(query):
    connection = get_mysql_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM profiles where username = %s",(query,))
    profiles = cursor.fetchall()
    return render_template('view-profile.html', profiles=profiles)

@app.route("/suspend-account")
def sa():
    return render_template("suspend-account.html")

@app.route("/suspend-account", methods=['GET','POST'])
def sa1():
    if request.method == "POST":
        username = request.form.get("username")
        connection = get_mysql_connection()
        cursor = connection.cursor()
        query = "UPDATE users SET status = 'suspended' WHERE username = %s"
        cursor.execute(query, (username,))
        connection.commit()
        cursor.close()
        connection.close()
        return "Account suspended"


@app.route('/user-dashboard')
def user_dashboard():
    if 'username' in session and session.get('role') == 'user':
        return render_template("user-dashboard.html", username=session['username'])
    return redirect(url_for('login'))

@app.route('/employeer-dashboard')
def employeer_dashboard():
    if 'username' in session and session.get('role') == 'employer':
        username = session['username']
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs WHERE emp_name = %s", (username,))
        jobs = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("employeer-dashboard.html", username=username, jobs=jobs)
    return redirect(url_for('emp_login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
