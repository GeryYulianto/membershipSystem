from database import *
from flask import *
import datetime

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

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
        
        query_db('INSERT INTO members (name,no_hp,type) values (?,?,?)', (name, phone, type_))

        query_db('INSERT INTO attendance (nomor_kehadiran,date_time) values (?,?)', (0,formatted_time))
        return view_member(name=name)
    else:
        return render_template('register_page.html')

@app.route('/view_member')
def view_member(name=False):
    # query_db('INSERT INTO members (name,no_hp,type) VALUES(?,?,?)', ('Brian', '0811111111', 'bus'))
    members = query_db('SELECT * FROM members')
    return render_template('view_member_page.html', members=members, name=name)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        
    

        # save to db 
        # id, datetime
        
        return redirect(url_for('view_attendance'))
    return render_template('attendance_page.html')

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