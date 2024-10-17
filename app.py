from database import *
from flask import *
from datetime import datetime, timedelta

app = Flask(__name__)

## Index
@app.route('/')
def homepage():
    return render_template('homepage.html')


## Register 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form['phone']
        name = request.form['name']
        type_ = request.form['type_']
        
        # save to db 
        # id, phone, name, type_
        
        if type_ == 'travel' or type_ == 'bus':
            return redirect(url_for('view_member'))
    return render_template('register_page.html')

@app.route('/view_member')
def view_member():
    # query_db('INSERT INTO members (name,no_hp,type) VALUES(?,?,?)', ('Brian', '0811111111', 'bus'))
    members = query_db('SELECT * FROM members')
    return render_template('view_member_page.html', members=members)


## Attendance
def attendance_gap(new_datetime, last_datetime, min_gap_hours=0.001): # ganti waktu yang diinginkan disini
    if isinstance(new_datetime, str):
        new_datetime = datetime.strptime(new_datetime, '%Y-%m-%d %H:%M')
    if isinstance(last_datetime, str):
        last_datetime = datetime.strptime(last_datetime, '%Y-%m-%d %H:%M')
    
    min_gap = timedelta(hours=min_gap_hours)
    time_difference = new_datetime - last_datetime
    
    if time_difference < min_gap:
        return False
    return True

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    alert = None
    if request.method == 'POST':
        id = request.form['id']
        
        # save to db 
        # id, datetime
        search_attendance = query_db(f'SELECT * FROM attendance WHERE id="{id}";')
        # [['1', '0', '2024-10-17 09:45']]
        
        if search_attendance == []:
            alert = 'no_id' # Alert Id tidak ditemukan
        else:
            current_time = datetime.now()
            current_time = current_time.strftime("%Y-%m-%d %H:%M")
            
            check = attendance_gap(current_time, search_attendance[0][-1])
            if check is True:
                new_kehadiran = int(search_attendance[0][1]) + 1
                query_db('UPDATE attendance SET nomor_kehadiran = ?, date_time = ? WHERE id = ?', 
                         (new_kehadiran, current_time, id))
                
                if new_kehadiran % 5 == 0:
                    type_ = query_db(f'SELECT type FROM members WHERE id="{id}";')
                    type_ = type_[0][0]
                    return render_template('fee_member.html', id=id, type_=type_)
                else: 
                    alert = 'success' # alert berhasil
                
                return redirect(url_for('view_attendance'))
            else : 
                alert = 'no_time_gap' # Alert belum memenuhi jangka waktu yang ditentukan
        
    return render_template('attendance_page.html', alert=alert)

@app.route('/view_attendance')
def view_attendance():
    attendances = query_db('SELECT * FROM attendance')
    return render_template('view_member_attendance.html', attendances=attendances)


## Spending
@app.route('/view_spending')
def view_spending():
    spendings = query_db('SELECT * FROM spendings')
    return render_template('view_spending.html', spendings=spendings)


## For testing only (insert mockup, etc)
@app.route('/test')
def test():
    # query_db('INSERT INTO attendance (id,nomor_kehadiran,date_time) VALUES(?,?,?)', ("1", "0", '2024-10-17 09:45'))
    # query_db('DELETE FROM attendance WHERE id = ?', (1,))
    return 

if __name__ == "__main__":
    app.run(debug=True)