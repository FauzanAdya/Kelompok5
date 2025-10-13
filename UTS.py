# Sistem Pemesanan Tiket Online
# Menggunakan Stack (dengan list Python), Linear Search untuk pencarian ID,
# dan Selection Sort untuk mengurutkan berdasarkan waktu pemesanan (ascending).
# Waktu pemesanan otomatis diambil dari waktu real-time sistem saat memesan tiket.
# Fitur Baru: Tiket hangus (expired) jika melewati batas tenggat (1 jam setelah pemesanan).
# Tiket hilang (dihapus) jika sudah dipakai (validasi saat penggunaan).

from datetime import datetime, timedelta  # Untuk waktu real-time dan perhitungan tenggat

class TiketStack:
    def __init__(self):
        self.bookings = []  # Stack diimplementasikan dengan list (LIFO: append/pop dari akhir)
        self.tenggat_waktu = timedelta(hours=1)  # Batas tenggat: 1 jam (bisa diubah)
    
    def pesan_tiket(self, pesanan_id, nama):
        """Menambahkan pesanan baru ke stack (push). Waktu diambil otomatis dari real-time."""
        waktu_pemesanan = datetime.now()  # Simpan sebagai datetime object untuk perhitungan mudah
        self.bookings.append((pesanan_id, nama, waktu_pemesanan, 'active'))  # Status: active
        print(f"Tiket berhasil dipesan untuk {nama} dengan ID {pesanan_id} pada waktu real-time {waktu_pemesanan.strftime('%Y-%m-%d %H:%M')}.")
        print(f"Tenggat waktu: { (waktu_pemesanan + self.tenggat_waktu).strftime('%Y-%m-%d %H:%M') } (1 jam dari pemesanan).")
    
    def _cek_status_tiket(self, booking):
        """Internal: Cek apakah tiket masih valid (active dan belum expired)."""
        id_booking, nama, waktu_pemesanan, status = booking
        if status != 'active':
            return 'used' if status == 'used' else status
        waktu_habis = waktu_pemesanan + self.tenggat_waktu
        if datetime.now() > waktu_habis:
            return 'expired'  # Update status jika expired
        return 'active'
    
    def cari_berdasarkan_id(self, pesanan_id):
        """Linear Search: Mencari dari atas stack (terbaru) ke bawah (terlama), dengan cek status."""
        print(f"Mencari pesanan dengan ID: {pesanan_id}")
        found = False
        # Traverse dari akhir (top stack) ke awal untuk simulasi LIFO
        for i in range(len(self.bookings) - 1, -1, -1):
            booking = self.bookings[i]
            if booking[0] == pesanan_id:
                status = self._cek_status_tiket(booking)
                if status == 'expired':
                    print(f"Tiket ID {pesanan_id} sudah HANGUS (expired) sejak { (booking[2] + self.tenggat_waktu).strftime('%Y-%m-%d %H:%M') }.")
                elif status == 'used':
                    print(f"Tiket ID {pesanan_id} sudah DIPAKAI dan hilang dari sistem.")
                else:  # active
                    print(f"Ditemukan (masih valid): ID {booking[0]}, Nama {booking[1]}, Waktu Pemesanan {booking[2].strftime('%Y-%m-%d %H:%M')}, Status: Active")
                found = True
                break
        if not found:
            print("Pesanan dengan ID tersebut tidak ditemukan.")
    
    def gunakan_tiket(self, pesanan_id):
        """Gunakan tiket: Cari ID, cek valid, ubah status ke 'used' dan hapus dari stack (hilang)."""
        print(f"Mencoba menggunakan tiket dengan ID: {pesanan_id}")
        found_index = -1
        # Traverse dari akhir untuk LIFO
        for i in range(len(self.bookings) - 1, -1, -1):
            booking = self.bookings[i]
            if booking[0] == pesanan_id:
                status = self._cek_status_tiket(booking)
                if status == 'expired':
                    print(f"Tiket ID {pesanan_id} sudah HANGUS dan tidak bisa digunakan.")
                elif status == 'used':
                    print(f"Tiket ID {pesanan_id} sudah DIPAKAI sebelumnya.")
                else:  # active
                    # Hapus dari stack (pop simulasi, tapi sebenarnya remove)
                    del self.bookings[i]
                    print(f"Tiket ID {pesanan_id} berhasil DIPAKAI dan dihapus dari sistem.")
                found_index = i
                break
        
        if found_index == -1:
            print("Tiket dengan ID tersebut tidak ditemukan atau sudah hilang.")
    
    def urutkan_berdasarkan_waktu(self):
        """Selection Sort: Mengurutkan seluruh stack berdasarkan waktu pemesanan (ascending), hanya active."""
        # Filter hanya active dulu untuk sorting (expired/used tetap di stack tapi bisa ditampilkan terpisah)
        active_bookings = [b for b in self.bookings if self._cek_status_tiket(b) == 'active']
        n = len(active_bookings)
        if n <= 1:
            print("Tidak ada tiket active untuk diurutkan atau sudah terurut.")
            return
        
        # Selection Sort pada active_bookings
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if active_bookings[j][2] < active_bookings[min_idx][2]:  # Bandingkan datetime
                    min_idx = j
            active_bookings[i], active_bookings[min_idx] = active_bookings[min_idx], active_bookings[i]
        
        # Ganti stack dengan yang sudah diurutkan (hanya active; expired/used bisa ditangani terpisah)
        self.bookings = active_bookings  # Simulasi: hapus expired/used saat sort untuk kemurnian stack
        print("Stack berhasil diurutkan berdasarkan waktu pemesanan (ascending) untuk tiket active.")
    
    def tampilkan_semua(self):
        """Tampilkan semua pesanan dengan status (active/expired/used), dari terlama ke terbaru."""
        if not self.bookings:
            print("Belum ada pesanan.")
            return
        
        print("\nDaftar Pesanan (dari terlama ke terbaru, dengan status):")
        # Sort sementara untuk tampilan (ascending waktu)
        sorted_bookings = sorted(self.bookings, key=lambda b: b[2])
        for booking in sorted_bookings:
            id_booking, nama, waktu_pemesanan, status_awal = booking
            status = self._cek_status_tiket(booking)
            waktu_str = waktu_pemesanan.strftime('%Y-%m-%d %H:%M')
            tenggat_str = (waktu_pemesanan + self.tenggat_waktu).strftime('%Y-%m-%d %H:%M')
            if status == 'active':
                print(f"ID: {id_booking}, Nama: {nama}, Waktu: {waktu_str}, Tenggat: {tenggat_str}, Status: ACTIVE")
            elif status == 'expired':
                print(f"ID: {id_booking}, Nama: {nama}, Waktu: {waktu_str}, Tenggat: {tenggat_str}, Status: HANGUS (Expired)")
            else:  # used
                print(f"ID: {id_booking}, Nama: {nama}, Waktu: {waktu_str}, Status: DIPAKAI (Hilang)")
        print()

def main():
    stack = TiketStack()
    
    while True:
        print("\n=== Sistem Pemesanan Tiket Online ===")
        print("1. Pesan Tiket (waktu real-time otomatis, tenggat 1 jam)")
        print("2. Cari Pesanan berdasarkan ID (Linear Search, cek status)")
        print("3. Gunakan Tiket (hapus jika valid)")
        print("4. Urutkan Pesanan berdasarkan Waktu (Selection Sort, hanya active)")
        print("5. Tampilkan Semua Pesanan (dengan status)")
        print("6. Keluar")
        
        pilihan = input("Pilih menu (1-6): ").strip()
        
        if pilihan == '1':
            pesanan_id = input("Masukkan ID Pesanan: ").strip()
            nama = input("Masukkan Nama Pemesan: ").strip()
            stack.pesan_tiket(pesanan_id, nama)  # Waktu real-time otomatis
        
        elif pilihan == '2':
            pesanan_id = input("Masukkan ID Pesanan untuk dicari: ").strip()
            stack.cari_berdasarkan_id(pesanan_id)
        
        elif pilihan == '3':
            pesanan_id = input("Masukkan ID Tiket untuk digunakan: ").strip()
            stack.gunakan_tiket(pesanan_id)
        
        elif pilihan == '4':
            stack.tampilkan_semua()  # Tampilkan sebelum sort
            stack.urutkan_berdasarkan_waktu()
            stack.tampilkan_semua()  # Tampilkan setelah sort
        
        elif pilihan == '5':
            stack.tampilkan_semua()
        
        elif pilihan == '6':
            print("Terima kasih telah menggunakan sistem pemesanan tiket!")
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()