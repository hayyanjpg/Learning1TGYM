from flask import Flask, render_template, request, redirect, url_for, flash, session 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TekkomGym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

db = SQLAlchemy(app)


# Model untuk User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Model untuk Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
   

# Model untuk Membership
class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)

# Model untuk Admin
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    

# Inisialisasi database
with app.app_context():
    db.create_all()

# Halaman Home
@app.route("/")
def home():
    return render_template("index.html")

# Halaman Login Pengguna
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=name).first()

        if user and check_password_hash(user.password, password):
            flash("Login berhasil. Selamat datang, {}!".format(user.username), "success")
            return redirect(url_for("market"))
        else:
            flash("Username atau password salah", "danger")
            return render_template("login.html")

    return render_template("login.html")

# Halaman Registrasi Pengguna
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Cek apakah username atau email sudah terdaftar
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username atau email sudah terdaftar", "danger")
            return render_template("register.html")

        # Hash password dan simpan pengguna baru
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registrasi berhasil! Silakan login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Halaman Market
@app.route("/market")
def market():
    return render_template("market.html")

# Halaman Login Admin
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session["admin_id"] = admin.id  # Simpan admin ID di session
            flash("Login berhasil!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Username atau password salah!", "danger")

    return render_template("admin_login.html")


# Halaman Dashboard Admin
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        flash("Silakan login terlebih dahulu!", "danger")
        return redirect(url_for("admin_login"))

    products = Product.query.all()
    memberships = Membership.query.all()
    admins = Admin.query.all()  # Menampilkan daftar admin di dashboard
    return render_template(
        "admin_dashboard.html", products=products, memberships=memberships, admins=admins
    )
# Tambah Produk
@app.route("/admin/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        
        # Pastikan harga adalah angka valid
        try:
            price = float(price)
        except ValueError:
            flash("Harga produk harus berupa angka", "danger")
            return render_template("admin_dashboard.html")

        # Tambahkan produk baru ke database
        new_product = Product(name=name, description=description, price=price)
        db.session.add(new_product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_dashboard.html")


# Update Produk
@app.route("/admin/update_product/<int:product_id>", methods=["POST"])
def update_product(product_id):
    product = Product.query.get(product_id)
    product.name = request.form .get("name")
    product.description = request.form.get("description")
    product.price = request.form.get("price")

    db.session.commit()
    flash("Product updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))

# Hapus Produk
@app.route("/admin/delete_product/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/add_membership", methods=["GET", "POST"])
def add_membership():
    if request.method == "POST":
        membership_id = request.form.get("membership_id")
        membership_type = request.form.get("type")
        duration = request.form.get("duration")
        price = request.form.get("price")
        status = request.form.get("status")

        # Pastikan harga adalah angka valid
        try:
            price = float(price)
        except ValueError:
            flash("Harga membership harus berupa angka", "danger")
            return redirect(url_for("admin_dashboard"))

        # Tambahkan membership baru ke database
        new_membership = Membership(id=membership_id, type=membership_type, price=price, description=duration, status=status)
        db.session.add(new_membership)
        db.session.commit()

        flash("Membership added successfully!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_dashboard.html")


# Update Membership
@app.route("/admin/update_membership/<int:membership_id>", methods=["POST"])
def update_membership(membership_id):
    membership = Membership.query.get(membership_id)
    membership.type = request.form.get("type")
    membership.price = request.form.get("price")
    membership.description = request.form.get("description")

    db.session.commit()
    flash("Membership updated successfully!", "success")
    return redirect(url_for("admin_dashboard"))

# Hapus Membership
@app.route("/admin/delete_membership/<int:membership_id>")
def delete_membership(membership_id):
    membership = Membership.query.get(membership_id)
    db.session.delete(membership)
    db.session.commit()
    flash("Membership deleted successfully!", "success")
    return redirect(url_for("admin_dashboard"))

 # Tambah Admin
@app.route("/admin/add_admin", methods=["GET", "POST"])
def add_admin():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        # Periksa apakah username atau email sudah terdaftar
        existing_admin = Admin.query.filter((Admin.username == username) | (Admin.email == email)).first()
        if existing_admin:
            flash("Username atau email sudah terdaftar", "danger")
            return render_template("admin_dashboard.html")

        # Hash password untuk keamanan
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        # Tambahkan admin baru ke database
        new_admin = Admin(username=username, email=email, phone=phone, password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        flash("Admin berhasil ditambahkan!", "success")
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_dashboard.html")


# Inisialisasi database dan admin default
with app.app_context():
    db.create_all()

    # Periksa apakah admin sudah ada
    existing_admin = Admin.query.filter_by(username="defaultadmin").first()
    if not existing_admin:
        # Jika tidak ada, buat admin default
        hashed_password = generate_password_hash("defaultpassword", method="pbkdf2:sha256")
        default_admin = Admin(username="defaultadmin", email="admin@example.com", password=hashed_password)
        db.session.add(default_admin)
        db.session.commit()
        print("Admin default berhasil dibuat dengan username 'defaultadmin' dan password 'defaultpassword'")

    # Tambahkan admin manual (hanya jika diperlukan)
    manual_admin = Admin.query.filter_by(username="admin").first()
    if not manual_admin:
        hashed_password = generate_password_hash("password", method="pbkdf2:sha256")
        admin = Admin(username="admin", email="admin@gmail.com", password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        print("Admin tambahan berhasil dibuat.")


if __name__ == "__main__":
    app.run(debug=True, port=5001)# Tambah Admin