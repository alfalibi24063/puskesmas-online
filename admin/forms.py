from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginAdmin_F(FlaskForm):

    username = StringField(
        'Username',
        validators=[DataRequired()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Login')


class Dokter_F(FlaskForm):

    nama_dokter = StringField(
        'Nama Dokter',
        validators=[DataRequired()]
    )

    spesialis = StringField(
        'Spesialis',
        validators=[DataRequired()]
    )

    jadwal = StringField(
        'Jadwal',
        validators=[DataRequired()]
    )

    no_telp = StringField(
        'No Telepon',
        validators=[DataRequired()]
    )

    submit = SubmitField('Simpan')