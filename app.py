from database import *
from flask import *

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form['phone']
        name = request.form['name']
        type_ = request.form['type_']
        
        # save to db Member
        # id, phone, name, type_
        
        return redirect(url_for('view_member'))
    return render_template('register_page.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        
        # save to db Member
        # id, phone, name, type_
        
        return redirect(url_for('view_attendance'))
    return render_template('attendance_page.html')

@app.route('/view_member')
def view_member():
    # query_db('INSERT INTO members (name,no_hp,type) VALUES(?,?,?)', ('Brian', '0811111111', 'bus'))
    members = query_db('SELECT * FROM members')
    return render_template('view_member_page.html', members=members)

@app.route('/view_attendance')
def view_attendance():
    attendances = query_db('SELECT * FROM attendance')
    return render_template('view_member_attendance.html', attendances = attendances)

@app.route('/view_spending')
def view_spending():
    spendings = query_db('SELECT * FROM payment')
    return render_template('view_spending.html', spendings=spendings)

if __name__ == "__main__":
    app.run(debug=True)