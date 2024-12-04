// Fungsi untuk menampilkan halaman login
function showLogin() {
    window.location.href = 'login.html'; // Arahkan ke halaman login
}

// Fungsi untuk menampilkan halaman registrasi
function showRegister() {
    window.location.href = 'register.html'; // Arahkan ke halaman registrasi
}

// Event listener untuk form login
document.getElementById('loginForm')?.addEventListener('submit', function(event) {
    event.preventDefault(); // Mencegah pengiriman form secara default
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    // Logika untuk memproses login (misalnya, validasi pengguna)
    if (username === "user" && password === "password") {
        alert('Login berhasil!'); // Contoh alert
        // Arahkan ke halaman utama setelah login berhasil
        window.location.href = 'market.html'; // Ganti dengan halaman yang sesuai
    } else {
        alert('Username atau password salah!');
    }
});

// Event listener untuk form registrasi
document.getElementById('registerForm')?.addEventListener('submit', function(event) {
    event.preventDefault(); // Mencegah pengiriman form secara default
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    // Logika untuk memproses registrasi (misalnya, menyimpan data pengguna)
    // Di sini Anda bisa menambahkan validasi dan penyimpanan data
    alert(`Registrasi berhasil untuk ${username}!`); // Contoh alert

    // Setelah registrasi berhasil, arahkan ke halaman login
    window.location.href = 'login.html';
});

// Fungsi untuk menampilkan formulir pembelian membership
function showMembershipForm(type) {
    document.getElementById('membership_type').value = type; // Set tipe membership
    document.getElementById('membershipForm').style.display = 'block'; // Tampilkan formulir
}

// Event listener untuk tombol "Beli" pada Membership
document.addEventListener('DOMContentLoaded', function() {
    const buyMonthlyButton = document.getElementById("buyMonthly");
    const buyVIPButton = document.getElementById("buyVIP");
    const membershipForm = document.getElementById("membershipForm");
    const membershipTypeInput = document.getElementById("membership_type");

    // Tombol Membership Bulanan
    if (buyMonthlyButton) {
        buyMonthlyButton.addEventListener("click", function () {
            membershipTypeInput.value = "Membership Bulanan";
            membershipForm.style.display = "block"; // Tampilkan formulir
        });
    }

    // Tombol Membership VIP
    if (buyVIPButton) {
        buyVIPButton.addEventListener("click", function () {
            membershipTypeInput.value = "Membership VIP Bulanan";
            membershipForm.style.display = "block"; // Tampilkan formulir
        });
    }

    // Event listener untuk formulir pembelian
    const purchaseForm = document.getElementById('purchaseForm');
    if (purchaseForm) {
        purchaseForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Mencegah pengiriman form secara default
            alert('Formulir berhasil dikirim!'); // Contoh alert
            membershipForm.style.display = 'none'; // Sembunyikan formulir setelah pengiriman
        });
    }
});
