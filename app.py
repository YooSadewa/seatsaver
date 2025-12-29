from flask import Flask, render_template_string, request, jsonify
from admin.login import login_bp
from admin.admin import admin_bp
import mysql.connector
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = 'seatsaver_secret_key'

app.register_blueprint(login_bp, url_prefix='/admin')
app.register_blueprint(admin_bp, url_prefix='/admin')

# Konfigurasi Database - DIGUNAKAN
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_reservasi',
    'connection_timeout': 10
}

@contextmanager
def get_db_connection():
    """Context manager untuk koneksi database - otomatis close"""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        yield connection
    except Exception as e:
        print(f"Database Error: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SeatSaver - Smart Restaurant Booking System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #d4a574;
            --dark: #2c2c2c;
            --light: #f8f9fa;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .hero {
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                        url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=1200') center/cover;
            height: 100vh;
            color: white;
            display: flex;
            align-items: center;
            text-align: center;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        
        .hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
        }
        
        .btn-primary {
            background-color: var(--primary);
            border: none;
            padding: 12px 35px;
            font-size: 1.1rem;
            transition: all 0.3s;
        }
        
        .btn-primary:hover {
            background-color: #c89960;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(212, 165, 116, 0.4);
        }
        
        .section-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 3rem;
            color: var(--dark);
        }
        
        .feature-box {
            padding: 2rem;
            text-align: center;
            transition: transform 0.3s;
        }
        
        .feature-box:hover {
            transform: translateY(-10px);
        }
        
        .feature-box i {
            font-size: 3rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }
        
        .reservation-form {
            background: white;
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .form-control:focus, .form-select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 0.2rem rgba(212, 165, 116, 0.25);
        }
        
        footer {
            background-color: var(--dark);
            color: white;
            padding: 2rem 0;
        }
        
        .menu-item {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .menu-item:hover {
            transform: scale(1.05);
        }
        
        .menu-item img {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="#"><i class="fas fa-utensils me-2"></i>SeatSaver</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
                    <li class="nav-item"><a class="nav-link" href="#menu">Menu</a></li>
                    <li class="nav-item"><a class="nav-link" href="#reservasi">Reservasi</a></li>
                    <li class="nav-item"><a class="nav-link" href="#kontak">Kontak</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="container">
            <h1>SeatSaver</h1>
            <p>Aplikasi reservasi meja restoran berbasis web <br> 
                untuk memudahkan pelanggan memesan meja secara cepat, efisien, dan tanpa kontak langsung</p>
            <a href="#reservasi" class="btn btn-primary btn-lg">
                <i class="fas fa-calendar-plus me-2"></i>Reservasi Sekarang</a>
        </div>
    </section>

    <!-- Features Section -->
    <section class="py-5 bg-light">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <div class="feature-box">
                        <i class="fas fa-calendar-check"></i>
                        <h4>Reservasi Online</h4>
                        <p>Pelanggan dapat melakukan pemesanan meja secara digital</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-box">
                        <i class="fas fa-user-shield"></i>
                        <h4>Tanpa Kontak Langsung</h4>
                        <p>Reservasi dilakukan tanpa perlu datang ke restoran</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-box">
                        <i class="fas fa-globe"></i>
                        <h4>Akses Kapan Saja</h4>
                        <p>Dapat digunakan kapan saja dan dimana saja</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Menu Section -->
    <section id="menu" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">Menu Spesial Kami</h2>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="menu-item">
                        <img src="https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400" alt="Nasi Goreng">
                        <div class="p-3">
                            <h5>Nasi Goreng Special</h5>
                            <p class="text-muted">Nasi goreng dengan bumbu rahasia</p>
                            <strong class="text-primary">Rp 35.000</strong>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="menu-item">
                        <img src="https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=400" alt="Sate">
                        <div class="p-3">
                            <h5>Sate Ayam</h5>
                            <p class="text-muted">Sate ayam dengan bumbu kacang</p>
                            <strong class="text-primary">Rp 45.000</strong>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="menu-item">
                        <img src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400" alt="Soup">
                        <div class="p-3">
                            <h5>Soto Ayam</h5>
                            <p class="text-muted">Soto ayam khas dengan kuah hangat</p>
                            <strong class="text-primary">Rp 30.000</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Reservation Section -->
    <section id="reservasi" class="py-5 bg-light">
        <div class="container">
            <h2 class="section-title text-center">Reservasi Meja Online</h2>
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="reservation-form">
                        <form id="reservationForm">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label">Nama Lengkap <span class="text-danger">*</span></label>
                                    <input type="text" class="form-control" id="nama_pelanggan" placeholder="Masukkan nama lengkap" required>
                                </div>
                                
                                <div class="col-md-6">
                                    <label class="form-label">No. Telepon <span class="text-danger">*</span></label>
                                    <input type="tel" class="form-control" id="no_telp" placeholder="08xxxxxxxxxx" pattern="[0-9]{10,13}" required>
                                </div>
                                
                                <div class="col-md-6">
                                    <label class="form-label">No. Meja <span class="text-danger">*</span></label>
                                    <select class="form-select" id="no_meja" required>
                                        <option value="">Pilih Nomor Meja...</option>
                                        <option value="1">Meja 1</option>
                                        <option value="2">Meja 2</option>
                                        <option value="3">Meja 3</option>
                                        <option value="4">Meja 4</option>
                                        <option value="5">Meja 5</option>
                                        <option value="6">Meja 6</option>
                                        <option value="7">Meja 7</option>
                                        <option value="8">Meja 8</option>
                                        <option value="9">Meja 9</option>
                                        <option value="10">Meja 10</option>
                                    </select>
                                </div>
                                
                                <div class="col-md-6">
                                    <label class="form-label">Jumlah Kursi <span class="text-danger">*</span></label>
                                    <select class="form-select" id="jumlah_kursi" required>
                                        <option value="">Pilih...</option>
                                        <option value="1">1 Kursi</option>
                                        <option value="2">2 Kursi</option>
                                        <option value="3">3 Kursi</option>
                                        <option value="4">4 Kursi</option>
                                        <option value="5">5 Kursi</option>
                                        <option value="6">6 Kursi</option>
                                    </select>
                                </div>
                                
                                <div class="col-md-6">
                                    <label class="form-label">Tanggal Reservasi <span class="text-danger">*</span></label>
                                    <input type="date" class="form-control" id="hari_reservasi" required>
                                </div>
                                
                                <div class="col-md-6">
                                    <label class="form-label">Waktu <span class="text-danger">*</span></label>
                                    <input type="time" class="form-control" id="jam_reservasi" required>
                                </div>
                                
                                <div class="col-12">
                                    <label class="form-label">Total DP</label>
                                    <div class="input-group">
                                        <span class="input-group-text">Rp</span>
                                        <input type="number" class="form-control" id="total_dp" placeholder="50000" min="0" value="0">
                                    </div>
                                    <small class="text-muted">Minimal Rp 50.000 atau kosongkan jika bayar di tempat</small>
                                </div>
                                <div class="col-12">
                                    <button type="submit" class="btn btn-primary w-100">
                                        <i class="fas fa-calendar-check me-2"></i>Konfirmasi Reservasi
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="kontak" class="py-5">
        <div class="container">
            <h2 class="section-title text-center">Hubungi Kami</h2>
            <div class="row justify-content-center">
                <div class="col-md-4 text-center">
                    <i class="fas fa-map-marker-alt fa-2x text-primary mb-3"></i>
                    <h5>Alamat</h5>
                    <p>Jl. Kuliner No. 123<br>Batam, Kepulauan Riau</p>
                </div>
                <div class="col-md-4 text-center">
                    <i class="fas fa-phone fa-2x text-primary mb-3"></i>
                    <h5>Telepon</h5>
                    <p>+62 778 123 4567<br>+62 812 3456 7890</p>
                </div>
                <div class="col-md-4 text-center">
                    <i class="fas fa-envelope fa-2x text-primary mb-3"></i>
                    <h5>Email</h5>
                    <p>info@restoranusantara.com<br>reservasi@restoranusantara.com</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="text-center">
        <div class="container">
            <p class="mb-0">&copy; 2025 SeatSaver - Smart Restaurant Booking System</p>
        </div>
    </footer>

    <!-- Toast Notification -->
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
        <div id="successToast" class="toast" role="alert">
            <div class="toast-header bg-success text-white">
                <i class="fas fa-check-circle me-2"></i>
                <strong class="me-auto">Berhasil!</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                Reservasi Anda telah berhasil dikonfirmasi. Kami akan menghubungi Anda segera.
            </div>
        </div>
        
        <div id="errorToast" class="toast" role="alert">
            <div class="toast-header bg-danger text-white">
                <i class="fas fa-exclamation-circle me-2"></i>
                <strong class="me-auto">Error!</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                Terjadi kesalahan. Silakan coba lagi.
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('hari_reservasi').min = new Date().toISOString().split('T')[0];
        
        document.getElementById('reservationForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const dpValue = document.getElementById('total_dp').value.trim();
            const dpNumber = parseInt(dpValue) || 0;
            
            if (dpNumber > 0 && dpNumber < 50000) {
                const errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
                document.getElementById('errorToast').querySelector('.toast-body').textContent = 
                    'DP minimal Rp 50.000 atau kosongkan jika bayar di tempat';
                errorToast.show();
                return;
            }
            
            const formData = {
                nama_pelanggan: document.getElementById('nama_pelanggan').value.trim(),
                no_telp: document.getElementById('no_telp').value.trim(),
                no_meja: document.getElementById('no_meja').value,
                jumlah_kursi: document.getElementById('jumlah_kursi').value,
                hari_reservasi: document.getElementById('hari_reservasi').value,
                jam_reservasi: document.getElementById('jam_reservasi').value,
                total_dp: dpNumber.toString()
            };
            
            try {
                const response = await fetch('/api/reservasi', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    const toast = new bootstrap.Toast(document.getElementById('successToast'));
                    toast.show();
                    document.getElementById('reservationForm').reset();
                } else {
                    const errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
                    document.getElementById('errorToast').querySelector('.toast-body').textContent = 
                        result.message || 'Terjadi kesalahan. Silakan coba lagi.';
                    errorToast.show();
                }
            } catch (error) {
                const errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
                document.getElementById('errorToast').querySelector('.toast-body').textContent = 
                    'Tidak dapat terhubung ke server: ' + error.message;
                errorToast.show();
            }
        });
        
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/reservasi', methods=['POST'])
def create_reservation():
    try:
        data = request.json
        
        # Validasi digabung - lebih efisien
        required = ['nama_pelanggan', 'no_telp', 'no_meja', 'jumlah_kursi', 'hari_reservasi', 'jam_reservasi']
        for field in required:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} harus diisi'}), 400
        
        # Konversi tipe data
        no_meja = int(data['no_meja'])
        jumlah_kursi = int(data['jumlah_kursi'])
        total_dp = str(data.get('total_dp', '0'))
        
        # Gunakan context manager - otomatis close
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                INSERT INTO reservasi 
                (nama_pelanggan, no_meja, jumlah_kursi, no_telp, hari_reservasi, jam_reservasi, total_dp, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                data['nama_pelanggan'],
                no_meja,
                jumlah_kursi,
                data['no_telp'],
                data['hari_reservasi'],
                data['jam_reservasi'],
                total_dp,
                'pending'
            )
            
            cursor.execute(query, values)
            conn.commit()
            reservation_id = cursor.lastrowid
            cursor.close()
        
        return jsonify({
            'success': True, 
            'message': 'Reservasi berhasil dibuat',
            'reservation_id': reservation_id
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'message': f'Format data tidak valid: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=True)