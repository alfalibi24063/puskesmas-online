from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pasien.models import Tpasien
from wtforms import SelectField


class Pasien_F(FlaskForm):
    nik = StringField('NIK', validators=[DataRequired(), Length(min=16, max=16)])
    nama = StringField('Nama Pasien', validators=[DataRequired()])
    jenis_kelamin = SelectField('Jenis Kelamin',choices=[('L', 'Laki-laki'),('P', 'Perempuan') ],validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telepon = StringField('No. Telepon', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    konf_pass = PasswordField('Konfirmasi Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Daftar')
    
    
    # cek NIK
    def validate_nik(self, nik):
        ceknik = Tpasien.query.filter_by(nik=nik.data).first()
        if ceknik:
            raise ValidationError('NIK sudah terdaftar, gunakan NIK yang lain.')

    # cek email
    def validate_email(self, email):
        cekemail = Tpasien.query.filter_by(email=email.data).first()
        if cekemail:
            raise ValidationError('Email sudah terdaftar, gunakan Email yang lain.' )


class LoginPasien_F(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')
    
class Pendaftaran_F(FlaskForm):
    tanggal = StringField('Tanggal Pendaftaran', validators=[DataRequired()])
    keluhan = TextAreaField('Keluhan', validators=[DataRequired()])

    dokter = SelectField(
        'Pilih Dokter',
        choices=[],
        coerce=int
    )

    tanggal_konsultasi = StringField(
        'Tanggal Konsultasi',
        validators=[DataRequired()]
    )

    jam_konsultasi = SelectField(
        'Jam Konsultasi',
        choices=[
            ('08:00', '08:00'),
            ('09:00', '09:00'),
            ('10:00', '10:00'),
            ('11:00', '11:00'),
            ('13:00', '13:00'),
            ('14:00', '14:00')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Daftar')