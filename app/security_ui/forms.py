from flask import flash
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    RadioField,
    TextField,
    PasswordField,
    TextAreaField,
    HiddenField,
    BooleanField,
)
from wtforms.validators import Length, DataRequired


class FlashingForm(FlaskForm):
    def validate_on_submit(self):
        result = super(FlashingForm, self).validate_on_submit()

        if not result:
            for field, errors in self.errors.items():
                for error in errors:
                    flash(
                        "Error in the {} field - {}".format(
                            getattr(self, field).label.text, error
                        ),
                        "error",
                    )
        return result


class LoginForm(FlashingForm):
    username = StringField("UHL Username", validators=[Length(max=100)])
    password = PasswordField("UHL Password", validators=[Length(max=50)])
