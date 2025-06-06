from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CorrespondenceForm(FlaskForm):
    date_received = DateField("Data otrzymania", format='%Y-%m-%d', validators=[DataRequired()])
    sender = StringField("Nadawca", validators=[DataRequired(), Length(max=100)])
    receiver = StringField("Odbiorca", validators=[DataRequired(), Length(max=100)])
    subject = StringField("Temat", validators=[DataRequired(), Length(max=200)])
    notes = TextAreaField("Uwagi", validators=[Length(max=500)])
    submit = SubmitField("Zapisz")
