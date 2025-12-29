from flask import Blueprint, render_template, redirect, url_for, session, request
from functools import wraps
import mysql.connector

admin_bp = Blueprint(
    'admin_bp',
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_login'):
            return redirect(url_for('login_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS total 
        FROM reservasi 
        WHERE hari_reservasi = CURDATE()
    """)
    daily = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) AS total 
        FROM reservasi 
        WHERE MONTH(hari_reservasi) = MONTH(CURDATE())
        AND YEAR(hari_reservasi) = YEAR(CURDATE())
    """)
    monthly = cursor.fetchone()['total']

    cursor.execute("""
        SELECT 
            id_reservasi,
            nama_pelanggan,
            no_meja,
            jumlah_kursi,
            no_telp,
            hari_reservasi,
            TIME_FORMAT(jam_reservasi, '%H:%i') AS jam_reservasi,
            status
        FROM reservasi
        ORDER BY hari_reservasi DESC, jam_reservasi DESC
        LIMIT 5
    """)
    reservations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        daily=daily,
        monthly=monthly,
        data=reservations
    )
@admin_bp.route('/update_status', methods=['POST'])
@login_required
def update_status():
    id_reservasi = request.form.get('id_reservasi')
    status = request.form.get('status')

    if status not in ['terima', 'tolak']:
        return redirect(url_for('admin_bp.dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reservasi 
        SET status = %s 
        WHERE id_reservasi = %s
    """, (status, id_reservasi))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_bp.dashboard'))
