from flask import Flask,render_template,redirect, request,url_for
import mysql.connector
from flask_mail import Mail,Message
app=Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'prathambathla'
app.config['MYSQL_PASSWORD'] = '0101'
app.config['MYSQL_DB'] = 'jobportal'

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
    "MAIL_USERNAME": "prathamsautomatedmails@gmail.com",
    "MAIL_PASSWORD": "",
    "MAIL_DEFAULT_SENDER" :"prathamsautomatedmails@gmail.com"
}

app.config.update(mail_config)
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user-login')
def login():
    return render_template('user-login.html')


@app.route('/user-login', methods=['POST','GET'])
def login1():

    username = request.form['username']
    password = request.form['password']

    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    

    #Check for suspended acoount
    
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()

    cursor.execute ("SELECT status FROM users WHERE username = %s",(username,))
    suspended_user=cursor.fetchone()


    cursor.close()
    connection.close()

    if suspended_user and suspended_user['status'] == 'suspended':
        return "Your account is suspended "


    elif user:
        # Successful login, you can redirect to a dashboard or another page

        return render_template("user-dashboard.html",username=username)
        
    else:
        # Invalid credentials, redirect back to the login page
        return "username or password is incorrect"



@app.route('/user-signup')
def signup():
    return render_template('user-signup.html')


@app.route("/user-signup",methods=["POST","GET"])
def signup1():
    username = request.form['username']
    password = request.form['password']

    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Check if the username is already taken
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Username already exists, handle accordingly (e.g., display an error message)
        return "Username already exists. Please choose a different username."

    # If the username is unique, insert the new user into the database
    cursor.execute('INSERT INTO users (username,password) VALUES (%s, %s)', (username, password))
    connection.commit()

    cursor.close()
    connection.close()

    # Successful signup, you can redirect to a login page or another page
    return render_template("user-half-step.html",username=username)

@app.route('/user-update-profile')
def upd():
    return render_template("user-update-profile.html")

@app.route('/user-update-profile', methods=['GET','POST'])
def update():
    
    connection = get_mysql_connection()
    cursor = connection.cursor()
    username = request.form['username']
    password = request.form['password']
    #name = request.form['name']
    
    # Update the user in the database
    update_query = "UPDATE users SET password=%s WHERE username=%s"
    cursor.execute(update_query, (password, username))
    connection.commit()
    connection.commit()
    
    return "Password Updated successfully !! \n Go back to login page"


@app.route('/employeer-login')
def emp_login():
    return render_template('employeer-login.html')


@app.route('/employeer-login', methods=['POST','GET'])
def emp_login1():

    username = request.form['username']
    password = request.form['password']

    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT username FROM employers WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        # Successful login, you can redirect to a dashboard or another page

        return render_template("employeer-dashboard.html",username=username)
        
    else:
        # Invalid credentials, redirect back to the login page
        return "username or password is incorrect"



@app.route('/employeer-signup')
def empsignup():
    return render_template('employeer-signup.html')


@app.route("/employeer-signup",methods=["POST","GET"])
def empsignup1():
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
    if request.method == "POST":
        connection = get_mysql_connection()
        cursor = connection.cursor()

        job_title= request.form["jobTitle"]
        HR_name= request.form["employerName"]
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
        return "Job Created Successfully !!!"
    return render_template("create-job.html")


@app.route("/update-job")
def jfr():
    return render_template("update-job.html")

@app.route('/update-job',methods=['GET','POST'])
def uj():
    try :
        if request.method == "POST":
            connection = get_mysql_connection()
            cursor = connection.cursor()

            job_title= request.form["jobTitle"]
            HR_name= request.form["employerName"]
            job_desc= request.form["jobDescription"]
            option = request.form.get('checkbox')


            if option is None :
                option = "Vacant"
            else:
                option="Filled"

        
            cursor.execute("UPDATE jobportal.jobs SET job_description = %s, job_status = %s WHERE emp_name = %s AND job_title = %s", (job_desc,option, HR_name, job_title))
            connection.commit()
            cursor.close()
            connection.close()

            return "updation successful"
        
    except mysql.connector.Error as error:
        print("Error updating database: {}".format(error))  
    
   
@app.route("/delete-job")
def dj():
    return render_template("delete-job.html")

@app.route('/delete-job',methods=['GET','POST'])
def dj1():
    if request.method == "POST":
        connection = get_mysql_connection()
        cursor = connection.cursor()

        job_title= request.form["jobTitle"]
    
        
        cursor.execute("DELETE FROM jobs WHERE job_title = %s", (job_title,))
        connection.commit()
        cursor.close()
        connection.close()
        return "deletion successful"
    

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


app.run(debug=True)
