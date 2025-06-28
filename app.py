from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB = 'reminders.db'

# Setup DB
def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reminders
                        (id INTEGER PRIMARY KEY, message TEXT, datetime TEXT)''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.form['message']
        datetime_str = request.form['datetime']  # Format: YYYY-MM-DDTHH:MM

        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO reminders (message, datetime) VALUES (?, ?)", (msg, datetime_str))
            conn.commit()

        return redirect('/')

    with sqlite3.connect(DB) as conn:
        reminders = conn.execute("SELECT id, message, datetime FROM reminders ORDER BY datetime").fetchall()

    return render_template('index.html', reminders=reminders)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
