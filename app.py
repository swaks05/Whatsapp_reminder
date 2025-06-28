from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect
import sqlite3
import threading
import os
from bot import reminder_bot  # Import your existing bot logic

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

    # Start the bot in a background thread
    bot_thread = threading.Thread(target=reminder_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)
