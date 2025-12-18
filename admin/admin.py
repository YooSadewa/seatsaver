from flask import Blueprint, render_template
import mysql.connector

# Perhatikan: template_folder menunjuk ke folder templates di dalam admin
admin_bp = Blueprint('admin_bp', __name__, 
                     template_folder='templates',
                     static_folder='static')

# Konfigurasi Database (Sesuaikan)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_reservasi'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Route Dashboard
# Nanti aksesnya jadi: localhost:5000/admin/dashboard
@admin_bp.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Hitung Harian
    cursor.execute("SELECT COUNT(*) as total FROM reservasi WHERE hari_reservasi = CURDATE()")
    daily = cursor.fetchone()['total']
    
    # 2. Hitung Bulanan
    cursor.execute("SELECT COUNT(*) as total FROM reservasi WHERE MONTH(hari_reservasi) = MONTH(CURDATE()) AND YEAR(hari_reservasi) = YEAR(CURDATE())")
    monthly = cursor.fetchone()['total']
    
    # 3. Data Tabel
    query_tabel = """
        SELECT 
            id_reservasi,
            nama_pelanggan,
            no_meja,
            jumlah_kursi,
            no_telp,
            hari_reservasi,
            TIME_FORMAT(jam_reservasi, '%H:%i') as jam_reservasi, -- INI YANG BIKIN DETIK HILANG
            status
        FROM reservasi 
        ORDER BY hari_reservasi DESC, jam_reservasi DESC 
        LIMIT 5
    """
    cursor.execute(query_tabel)
    reservations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', daily=daily, monthly=monthly, data=reservations)