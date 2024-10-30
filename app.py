from database import *
from flask import *
from datetime import datetime, timedelta

app = Flask(__name__)

## Global Variables
BUS = 100_000
TRAVEL = 50_000
JUMLAH_KEHADIRAN = 5

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

        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
        
        if type_ == 'travel' or type_ == 'bus':
            query_db('INSERT INTO members (name,no_hp,type) values (?,?,?)', (name, phone, type_))
            query_db('INSERT INTO attendance (nomor_kehadiran,date_time) values (?,?)', (0,formatted_time))            
            return view_member(name=name)
        else : 
            return render_template('register_page.html')       
        
    else:
        return render_template('register_page.html')

@app.route('/view_member')
def view_member(name=False):
    # query_db('INSERT INTO members (name,no_hp,type) VALUES(?,?,?)', ('Brian', '0811111111', 'bus'))
    members = query_db('SELECT * FROM members')
    return render_template('view_member_page.html', members=members)


## Attendance
def attendance_gap(new_datetime, last_datetime, min_gap_hours=0): # ganti waktu yang diinginkan disini, 0.001
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
                
                if new_kehadiran % JUMLAH_KEHADIRAN == 0:
                    type_ = query_db(f'SELECT type FROM members WHERE id="{id}";')
                    type_ = type_[0][0]
                    
                    alert = f'payment_{type_}' # sesuai type nya
                    
                    ## Payment
                    # sekalian masukin ke table payment disini
                    
                    if type_ == 'bus':
                        fee = JUMLAH_KEHADIRAN * BUS
                    elif type_ == 'travel':
                        fee = JUMLAH_KEHADIRAN * TRAVEL
                    
                    query_db('INSERT INTO payment (id,fee,date_time) values (?,?,?)', (id, fee, current_time))
                    return redirect(url_for('view_attendance', alert=alert))
                
                else: 
                    alert = 'success' # 
                
                return redirect(url_for('view_attendance', alert=alert))
            else : 
                alert = 'no_time_gap' # Alert belum memenuhi jangka waktu yang ditentukan
        
    return render_template('attendance_page.html', alert=alert)

@app.route('/view_attendance')
def view_attendance():
    alert = request.args.get('alert')  # mengambil alert dari query string
    attendances = query_db('SELECT * FROM attendance')
    return render_template('view_member_attendance.html', attendances=attendances, alert=alert)


@app.route('/payment')
def payment():
    spendings = query_db('SELECT * FROM payment')
    return render_template('view_spending.html', spendings=spendings)


## For testing only (insert mockup, etc)
@app.route('/test')
def test():
    # query_db('INSERT INTO attendance (id,nomor_kehadiran,date_time) VALUES(?,?,?)', ("1", "0", '2024-10-17 09:45'))
    # query_db('DELETE FROM members')
    # query_db('DELETE FROM attendance')
    # query_db('DELETE FROM payment')
    # query_db('DELETE FROM sqlite_sequence')
    return 

if __name__ == "__main__":
    app.run(debug=True)