from wtforms import Form, StringField, PasswordField, validators, SelectField, EmailField, SubmitField, ValidationError

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=25)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    role = SelectField('Role', choices=[('Admin','Admin'), ('platform_user', 'platform_user')], validators=[validators.DataRequired()])
    submit= SubmitField('Submit')

    def validate_username(self, username):
        if len(username.data) < 3:
            raise ValidationError('Username must be at least 3 characters long')