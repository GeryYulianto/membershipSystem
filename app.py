from database import *
from flask import *
app = Flask(__name__)

@app.get("/")
def hello_world():
    return render_template('register_page.html')

@app.post('/register')
def register():
    email = request.form['email']
    username = request.form['username']
    password = hash(request.form['password'])
    res = query_db('INSERT INTO users (username, email, password) values (?, ?, ?)', (username, email, password))

    return res

@app.get('/setcookie')
def cookie():
    resp = make_response('Setting cookie...')
    resp.set_cookie('visit', '0')
    return resp

@app.get('/visit')
def visit():
    count = int(request.cookies.get('visit', 0))
    count += 1
    resp = make_response(f'You visit the website for: {count} times')
    resp.set_cookie('visit', str(count))
    return resp