from datetime import datetime
from pasien import db
from datetime import datetime
from flask_login import UserMixin



class Tpasien(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    jenis_kelamin = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    telepon = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Tpasien('{self.nik}','{self.nama}','{self.jenis_kelamin}','{self.alamat}','{self.telepon}','{self.email}','{self.password}')"


class Tdokter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_dokter = db.Column(db.String(100), nullable=False)
    spesialis = db.Column(db.String(100), nullable=False)
    jadwal = db.Column(db.String(100), nullable=False)
    no_telp = db.Column(db.String(15))
    
    
    def __repr__(self):
        return f"Tdokter('{self.nama_dokter}','{self.spesialis}','{self.jadwal}')"


class Tpendaftaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    tanggal = db.Column(db.String(20))
    tanggal_konsultasi = db.Column(db.String(20))
    jam_konsultasi = db.Column(db.String(20))
    keluhan = db.Column(db.Text)

    pasien_id = db.Column(
        db.Integer,
        db.ForeignKey('tpasien.id')
    )

    dokter_id = db.Column(
        db.Integer,
        db.ForeignKey('tdokter.id')
    )

    pasien = db.relationship(
        'Tpasien',
        backref='pendaftaran'
    )

    dokter = db.relationship(
        'Tdokter',
        backref='pendaftaran'
    )


class Tadmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(200))