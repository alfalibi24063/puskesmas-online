from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user

from pasien import db
from pasien.models import Tpasien, Tdokter, Tpendaftaran, Tadmin
from admin import radmin
from admin.forms import LoginAdmin_F, Dokter_F
from pasien import bcrypt
from functools import wraps
from flask import session, redirect, url_for, flash



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_login"):
            flash("Silakan login terlebih dahulu", "warning")
            return redirect(url_for("radmin.login"))

        return f(*args, **kwargs)

    return decorated_function

@radmin.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginAdmin_F()

    if form.validate_on_submit():

        admin = Tadmin.query.filter_by(
            username=form.username.data
        ).first()

        if admin:
            print("Username DB :", admin.username)
            print("Hash Password :", admin.password)

        if admin and bcrypt.check_password_hash(
            admin.password,
            form.password.data
        ):

            session["admin_login"] = True
            session["admin_id"] = admin.id

            flash("Login berhasil", "success")
            return redirect(url_for("radmin.dashboard"))

        flash("Username atau Password salah", "danger")

    return render_template("login_admin.html", form=form)

    #     if admin and bcrypt.check_password_hash(
    #             admin.password,form.password.data):

    #         session["admin_login"] = True
    #         session["admin_id"] = admin.id

    #         flash("Login berhasil", "success")
    #         return redirect(url_for("radmin.dashboard"))

    #     flash("Username atau Password salah", "danger")

    # return render_template("login_admin.html", form=form)


# @radmin.route("/cekadmin")
# def cekadmin():
#     admins = Tadmin.query.all()

#     hasil = ""

#     for a in admins:
#         hasil += f"ID: {a.id}, Username: {a.username}, Password: {a.password}<br>"

#     if hasil == "":
#         hasil = "Tabel tadmin kosong"

#     return hasil

@radmin.route('/dashboard')
@admin_required
def dashboard():

    total_pasien = Tpasien.query.count()
    total_dokter = Tdokter.query.count()
    total_jadwal = Tpendaftaran.query.count()

    return render_template(
        'dashboard.html',
        total_pasien=total_pasien,
        total_dokter=total_dokter,
        total_jadwal=total_jadwal
    )


@radmin.route('/data_pasien')
@admin_required
def data_pasien():

    pasien = Tpasien.query.all()

    return render_template(
        'data_pasien.html',
        pasien=pasien
    )
    

@radmin.route('/detail_pasien/<int:id>')
@admin_required
def detail_pasien(id):

    pasien = Tpasien.query.get_or_404(id)

    return render_template(
        "detail_pasien.html",
        pasien=pasien
    )

@radmin.route('/data_dokter')
@admin_required
def data_dokter():

    dokter = Tdokter.query.all()

    return render_template(
        "data_dokter.html",
        dokter=dokter
    )
    
    
@radmin.route('/tambah_dokter', methods=['GET', 'POST'])
@admin_required
def tambah_dokter():

    form = Dokter_F()

    if form.validate_on_submit():

        dokter = Tdokter(
            nama_dokter=form.nama_dokter.data,
            spesialis=form.spesialis.data,
            jadwal=form.jadwal.data,
            no_telp=form.no_telp.data
        )

        db.session.add(dokter)
        db.session.commit()

        flash("Data dokter berhasil ditambahkan.", "success")
        return redirect(url_for("radmin.data_dokter"))

    return render_template(
        "tambah_dokter.html",
        form=form
    )

@radmin.route('/edit_dokter/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_dokter(id):

    dokter = Tdokter.query.get_or_404(id)

    form = Dokter_F(obj=dokter)

    if form.validate_on_submit():

        dokter.nama_dokter = form.nama_dokter.data
        dokter.spesialis = form.spesialis.data
        dokter.jadwal = form.jadwal.data
        dokter.no_telp = form.no_telp.data

        db.session.commit()

        flash("Data dokter berhasil diubah.", "success")
        return redirect(url_for("radmin.data_dokter"))

    return render_template(
        "edit_dokter.html",
        form=form
    )
    
    
@radmin.route('/hapus_dokter/<int:id>')
@admin_required
def hapus_dokter(id):

    dokter = Tdokter.query.get_or_404(id)

    db.session.delete(dokter)
    db.session.commit()

    flash("Data dokter berhasil dihapus.", "success")

    return redirect(url_for("radmin.data_dokter"))

@radmin.route('/jadwal_konsultasi')
@login_required
def jadwal_konsultasi():

    jadwal = Tpendaftaran.query.all()

    return render_template(
        'jadwal_konsultasi.html',
        jadwal=jadwal
    )


@radmin.route('/status_jadwal/<int:id>/<status>')
@admin_required
def status_jadwal(id, status):

    jadwal = Tpendaftaran.query.get_or_404(id)

    jadwal.status = status

    db.session.commit()

    flash("Status jadwal berhasil diubah.", "success")

    return redirect(url_for('radmin.jadwal_konsultasi'))


@radmin.route('/hapus_jadwal/<int:id>')
@login_required
def hapus_jadwal(id):

    jadwal = Tpendaftaran.query.get_or_404(id)

    db.session.delete(jadwal)
    db.session.commit()

    flash("Jadwal berhasil dihapus", "success")

    return redirect(url_for('radmin.jadwal_konsultasi'))

@radmin.route('/logout')
@admin_required
def logout():

    session.pop("admin_login", None)
    session.pop("admin_id", None)

    flash("Logout berhasil", "success")
    return redirect(url_for("radmin.login"))