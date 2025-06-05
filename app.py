from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from models import CorrespondenceEntry, db
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///correspondence.db'
db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('username')
        password_input = request.form.get('password')

        if (login_input == os.getenv("LOGIN") and 
            password_input == os.getenv("PASSWORD")):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "Nieprawidłowy login lub hasło"
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        date_received_str = request.form.get('date_received')
        date_received = datetime.strptime(date_received_str, '%Y-%m-%d').date()
        sender = request.form.get('sender')
        receiver = request.form.get('receiver')
        subject = request.form.get('subject')
        notes = request.form.get('notes')

        new_entry = CorrespondenceEntry(
            date_received=date_received,
            sender=sender,
            receiver=receiver,
            subject=subject,
            notes=notes
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_entry.html')

@app.route('/entries')
def entries():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    all_entries = CorrespondenceEntry.query.order_by(CorrespondenceEntry.date_received.desc()).all()
    return render_template('entries.html', entries=all_entries)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

