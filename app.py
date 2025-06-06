from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from forms import CorrespondenceForm
from models import CorrespondenceEntry, db
from datetime import date
from utils import login_required

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
            return redirect(url_for('dashboard'))
        else:
            error = "Nieprawidłowy login lub hasło"
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/')
@login_required
def dashboard():
    today = date.today()
    incoming = CorrespondenceEntry.query.filter_by(direction='incoming', date_received=today).all()
    outgoing = CorrespondenceEntry.query.filter_by(direction='outgoing', date_received=today).all()
    return render_template('dashboard.html', incoming=incoming, outgoing=outgoing)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    form = CorrespondenceForm()
    if form.validate_on_submit():
        entry = CorrespondenceEntry(
            date_received=form.date_received.data,
            sender=form.sender.data,
            receiver=form.receiver.data,
            subject=form.subject.data,
            notes=form.notes.data,
            reference_number=form.reference_number.data,
            direction=form.direction.data
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_entry.html', form=form)

@app.route('/entries')
@login_required
def entries():

    all_entries = CorrespondenceEntry.query.order_by(CorrespondenceEntry.date_received.desc()).all()
    return render_template('entries.html', entries=all_entries)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = CorrespondenceEntry.query.get_or_404(id)
    form = CorrespondenceForm(obj=entry)  

    if form.validate_on_submit():
        form.populate_obj(entry)  
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit_entry.html', form=form, entry=entry)

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):

    entry = CorrespondenceEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('entries'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

