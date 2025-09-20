from flask import Flask, jsonify, render_template, request, redirect, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from google.cloud.firestore_v1.base_query import FieldFilter
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import timedelta

app = Flask(__name__)

cred = credentials.Certificate("cert.json") # Replace with your key file path
firebase_admin.initialize_app(cred)
db = firestore.client()
secure_key = "supersecretkey" # Replace with your secure key
app.secret_key = secure_key
app.permanent_session_lifetime=timedelta(minutes=20)
@app.before_request
def make_session_permanent():
    session.permanent = True





def getvalues(query):
    username=""
    password=""
    for data in query:
        username=data.to_dict()['username'] 
        password=data.to_dict()['password']


    return [username,password]

def checkUsernameExists(username,password):
    users_ref = db.collection('user')
    query = users_ref.where(filter=FieldFilter('username', '==', username))
    querys = query.stream()

    if any(querys):
        values = getvalues(query.stream())
       
        check=check_password_hash(values[1], password)
        if check:
            return True
        else:
            return False
    else:
        return False
def getrole(username):
    users_ref = db.collection('user')
    query = users_ref.where(filter=FieldFilter('username', '==', username))
    querys = query.stream()
    user=[]
    for data in querys:
        userdata=data.to_dict()
        userdata['id']=data.id
        user.append(userdata)
    return user[0]['role']
      



@app.route('/dash')
def home():

    if "username" in session:
       return render_template("dash.html") # Redirect to dashboard if logged in
    else:
       return redirect(url_for('login')) # Redirect to login if not logged in
      
    

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if checkUsernameExists(username,password):
        print(" User with role logged in successfully")
        
        session['username'] = username
        session['role'] = getrole(username)
        
        
        return redirect(url_for('home'))
    else:
        print("Username does not exist")
      
    return render_template('login.html')

#logout route   
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


#Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if password is not None:
            hashed_password = generate_password_hash(password)
        else:
            return render_template('register.html', error="Password is required")
        
        users_ref = db.collection('user')
        query = users_ref.where(filter=FieldFilter('username', '==', username))
        querys = query.stream()

        if any(querys):
            print("Username already exists")
        else:
            doc_ref = db.collection('user').document()
            doc_ref.set({
                'username': username,
                'password': hashed_password
            })
            print("User registered successfully")
            return redirect(url_for('login'))
    
    return render_template('login.html')


#getALL users route
@app.route('/users', methods=['GET'])
def get_all_users():
    users_ref = db.collection('user')
    docs = users_ref.stream()
    if "username" in session:
        users = []
        keys = ['id', 'username', 'password']
        for doc in docs:
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users.append(user_data)
            role=session['role']
        print(users)
        #print (jsonify(users))
        return render_template("users.html",users=users,keys=keys,role=role) # Render users if logged in
    else:
        return render_template("login.html") # Redirect to login if not logged in

@app.route('/deleteUser', methods=['POST','GET']) # Change to POST for better practice
def deleteUser():
    print("Delete user endpoint hit")   
    if request.method == 'POST':
        data=request.get_json()
        
        print(f"Request to delete user: {data}")
        username=data.get("username")
        print("Delete user function called")
        ref=db.collection('user')
        query=ref.where("username","==",username)
        for doc in query.stream():
            doc.reference.delete()
            print(f"User {username} deleted successfully")
    return redirect(url_for('get_all_users'))


if __name__ == '__main__':
    app.run(debug=True) # Enable debug mode for development 