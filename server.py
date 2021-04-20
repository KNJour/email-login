from flask import Flask, render_template, request, session,redirect, flash
from mysqlconnection  import connectToMySQL
import re
app = Flask(__name__)
app.secret_key = "Benny Bob wuz heer."
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route('/submit', methods=['POST'])
def submit():
    is_valid = True
    if len(request.form['email']) < 1:
        is_valid = False
        flash("**Please enter an email**")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    if not is_valid:
        return redirect ('/')

    else:
        flash("User Successfully added!")
        query = "INSERT INTO table1 (email, created_at, updated_at) VALUES (%(email)s,NOW(),NOW());"
        data = {
            'email' : request.form['email'],
            }

        print(query)
        emails = connectToMySQL("Emails").query_db(query, data)
        
        return redirect ('/result')
        
@app.route('/result')
def result():
    query = "SELECT * FROM table1;"
    emails = connectToMySQL("Emails").query_db(query)
    return render_template("display.html", emails = emails)

@app.route('/')
def newUser():
    
    return render_template("email.html")

if __name__=="__main__":
    app.run(debug=True)