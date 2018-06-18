from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length


class TodoForm(FlaskForm):
    title = StringField(
        'What needs to be done?', validators=[Required(), Length(1, 128)]
    )
    submit = SubmitField('Submit')