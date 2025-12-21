from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector

login_bp = Blueprint(
    'login_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_reservasi'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session.get('admin_login'):
            return redirect(url_for('admin_bp.dashboard'))

        error = None

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM admin WHERE username = %s",
                (username,)
            )
            admin = cursor.fetchone()

            cursor.close()
            conn.close()

            if admin is None:
                error = 'User tidak ditemukan'
            elif admin['password'] != password:
                error = 'Password salah'
            else:
                session['admin_login'] = True
                session['admin_id'] = admin['id_admin']
                session['admin_name'] = admin['username']
                return redirect(url_for('admin_bp.dashboard'))

        return render_template('login.html', error=error)

    except Exception as e:
        return f"<h3>LOGIN ERROR:</h3><pre>{e}</pre>"



@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_bp.login'))
