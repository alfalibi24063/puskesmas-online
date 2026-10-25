from flask import Blueprint, render_template, flash, redirect, url_for, request
from pasien.forms import LoginPasien_F, Pasien_F, Pendaftaran_F
from pasien.models import Tpasien, Tpendaftaran, Tdokter
from pasien import db, bcrypt
from flask_login import login_user, current_user, login_required
from pasien import bcrypt
from flask_login import logout_user
from datetime import datetime




rpasien = Blueprint('rpasien', __name__)

@rpasien.route('/')
def home():
    return render_template('home.html')


@rpasien.route('/visi_misi')
def visi_misi():
    return render_template('visi_misi.html')



@rpasien.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        pasien = Tpasien.query.filter_by(email=email).first()

        if pasien and bcrypt.check_password_hash(
                pasien.password,
                password):

            login_user(pasien)
            return redirect(url_for('rpasien.akun_pasien'))

        flash('Email atau Password salah', 'danger')

    return render_template('login_pasien.html')



@rpasien.route('/register', methods=['GET', 'POST'])
def register():
    form = Pasien_F()

    print("Method:", request.method)

    if form.validate_on_submit():
        print("Form Valid")

        pass_hash = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        add_pasien = Tpasien(nik=form.nik.data,nama=form.nama.data,jenis_kelamin=form.jenis_kelamin.data,alamat=form.alamat.data,telepon=form.telepon.data,email=form.email.data,password=pass_hash)
        db.session.add(add_pasien)
        db.session.commit()

        print("Data berhasil disimpan")

        flash('Registrasi berhasil.', 'success')
        return redirect(url_for('rpasien.login'))

    print(form.errors)

    return render_template('registrasi.html', form=form)





@rpasien.route('/pendaftaran', methods=['GET', 'POST'])
@login_required
def pendaftaran():
    form = Pendaftaran_F()

    # Mengambil data dokter
    dokter = Tdokter.query.all()

    # Mengisi pilihan dokter pada formulir
    form.dokter.choices = [
        (d.id, d.nama_dokter) for d in dokter
    ]

    # Mengambil jadwal konsultasi milik pasien yang login
    jadwal = Tpendaftaran.query.filter_by(
        pasien_id=current_user.id
    ).order_by(Tpendaftaran.id.desc()).all()

    if form.validate_on_submit():
        try:
            daftar = Tpendaftaran(
                tanggal=datetime.now().date(),
                keluhan=form.keluhan.data,
                tanggal_konsultasi=form.tanggal_konsultasi.data,
                jam_konsultasi=form.jam_konsultasi.data,
                pasien_id=current_user.id,
                dokter_id=int(form.dokter.data)
            )

            db.session.add(daftar)
            db.session.commit()

            flash('Pendaftaran konsultasi berhasil!', 'success')

            # Kembali ke halaman pendaftaran
            # agar data terbaru muncul di tabel bawah
            return redirect(url_for('rpasien.pendaftaran'))

        except Exception as e:
            db.session.rollback()
            print("ERROR PENDAFTARAN:", repr(e))
            flash(
                'Pendaftaran gagal disimpan. Periksa terminal Flask.',
                'danger'
            )

    elif form.is_submitted():
        print("ERROR VALIDASI FORM:", form.errors)
        flash(
            'Pendaftaran belum berhasil. Periksa kembali formulir.',
            'warning'
        )

    return render_template(
        'pendaftaran.html',
        form=form,
        dokter=dokter,
        jadwal=jadwal
    )



@rpasien.route('/jadwal_dokter')
@login_required
def jadwal_dokter():

    dokter = Tdokter.query.all()

    return render_template(
        "pendaftaran.html",
        dokter=dokter
    )

@rpasien.route('/akun_pasien')
@login_required
def akun_pasien():

    return render_template(
        'akun_pasien.html'
    )

    
@rpasien.route('/jadwal_konsultasi')
@login_required
def jadwal_konsultasi():

    print("Current User ID :", current_user.id)

    semua = Tpendaftaran.query.all()

    for j in semua:
        print(
            "ID:", j.id,
            "Pasien ID:", j.pasien_id,
            "Dokter:", j.dokter.nama_dokter
        )

    jadwal = Tpendaftaran.query.filter_by(
        pasien_id=current_user.id
    ).all()

    print("Jumlah jadwal :", len(jadwal))

    return render_template(
        "jadwal_konsultasi.html",
        jadwal=jadwal
    )



@rpasien.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('rpasien.home'))


@rpasien.route('/admin')
def admin():
    return render_template('admin.html')