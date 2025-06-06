from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CorrespondenceForm(FlaskForm):
    date_received = DateField("Data", validators=[DataRequired()])
    sender = StringField("Od kogo")
    receiver = StringField("Do kogo")
    subject = StringField("Temat", validators=[DataRequired()])
    notes = TextAreaField("Uwagi")
    reference_number = StringField("Nr sygnatury", validators=[Length(max=50)])
    direction = RadioField(
    "Rodzaj korespondencji",
    choices=[('incoming', 'Przyszła'), ('outgoing', 'Wychodząca')],
    default='incoming',
    validators=[DataRequired()]
    )
    submit = SubmitField("Zapisz")