from datetime import datetime, timedelta

class TiketStack:
    def __init__(self):
        self.bookings = []  # Stack menggunakan list (LIFO)
        self.tenggat_waktu = timedelta(hours=1)  # Tenggat 1 jam
    
    def pesan_tiket(self, pesanan_id, nama):
        waktu_pemesanan = datetime.now()
        self.bookings.append((pesanan_id, nama, waktu_pemesanan, 'active'))
        print(f"Tiket berhasil dipesan untuk {nama} dengan ID {pesanan_id} pada {waktu_pemesanan.strftime('%Y-%m-%d %H:%M')}.")
        print(f"Tenggat: {(waktu_pemesanan + self.tenggat_waktu).strftime('%Y-%m-%d %H:%M')}.")

    def _cek_status(self, booking):
        id_booking, nama, waktu_pemesanan, status = booking
        if status != 'active':
            return status
        if datetime.now() > waktu_pemesanan + self.tenggat_waktu:
            return 'expired'
        return 'active'
    
    def _cari_booking(self, pesanan_id):
        for i in range(len(self.bookings) - 1, -1, -1):
            if self.bookings[i][0] == pesanan_id:
                return i, self._cek_status(self.bookings[i])
        return -1, None

    def cari_berdasarkan_id(self, pesanan_id):
        print(f"Mencari pesanan ID: {pesanan_id}")
        index, status = self._cari_booking(pesanan_id)
        if index == -1:
            print("Pesanan tidak ditemukan.")
            return
        booking = self.bookings[index]
        if status == 'expired':
            print(f"Tiket ID {pesanan_id} sudah hangus sejak {(booking[2] + self.tenggat_waktu).strftime('%Y-%m-%d %H:%M')}.")
        elif status == 'used':
            print(f"Tiket ID {pesanan_id} sudah digunakan dan hilang.")
        else:
            print(f"Ditemukan: ID {booking[0]}, Nama {booking[1]}, Waktu {booking[2].strftime('%Y-%m-%d %H:%M')}, Status: Active")

    def gunakan_tiket(self, pesanan_id):
        print(f"Menggunakan tiket ID: {pesanan_id}")
        index, status = self._cari_booking(pesanan_id)
        if index == -1:
            print("Tiket tidak ditemukan.")
            return
        if status == 'expired':
            print(f"Tiket sudah hangus dan tidak bisa digunakan.")
        elif status == 'used':
            print(f"Tiket sudah digunakan sebelumnya.")
        else:
            del self.bookings[index]
            print(f"Tiket berhasil digunakan dan dihapus.")

    def urutkan_berdasarkan_waktu(self):
        active_bookings = [b for b in self.bookings if self._cek_status(b) == 'active']
        n = len(active_bookings)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if active_bookings[j][2] < active_bookings[min_idx][2]:
                    min_idx = j
            active_bookings[i], active_bookings[min_idx] = active_bookings[min_idx], active_bookings[i]
        self.bookings = active_bookings
        print("Stack diurutkan berdasarkan waktu untuk tiket active.")

    def tampilkan_semua(self):
        if not self.bookings:
            print("Belum ada pesanan.")
            return
        print("\nDaftar Pesanan (terlama ke terbaru):")
        sorted_bookings = sorted(self.bookings, key=lambda b: b[2])
        for booking in sorted_bookings:
            id_b, nama, waktu, status_awal = booking
            status = self._cek_status(booking)
            waktu_str = waktu.strftime('%Y-%m-%d %H:%M')
            if status == 'active':
                tenggat_str = (waktu + self.tenggat_waktu).strftime('%Y-%m-%d %H:%M')
                print(f"ID: {id_b}, Nama: {nama}, Waktu: {waktu_str}, Tenggat: {tenggat_str}, Status: ACTIVE")
            elif status == 'expired':
                tenggat_str = (waktu + self.tenggat_waktu).strftime('%Y-%m-%d %H:%M')
                print(f"ID: {id_b}, Nama: {nama}, Waktu: {waktu_str}, Tenggat: {tenggat_str}, Status: HANGUS")
            else:
                print(f"ID: {id_b}, Nama: {nama}, Waktu: {waktu_str}, Status: DIPAKAI")
        print()

def main():
    stack = TiketStack()
    while True:
        print("\n=== Sistem Pemesanan Tiket ===")
        print("1. Pesan Tiket")
        print("2. Menampilkan Semua")
        print("3. Cari Tiket (ID)")
        print("4. Gunakan Tiket")
        print("5. Keluar")
        pilihan = input("Pilih (1-5): ").strip()

        if pilihan == '1':
            pesanan_id = input("ID Pesanan: ").strip()
            nama = input("Nama: ").strip()
            stack.pesan_tiket(pesanan_id, nama)
        elif pilihan == '2':
            stack.tampilkan_semua()
        elif pilihan == '3':
            pesanan_id = input("ID untuk cari: ").strip()
            stack.cari_berdasarkan_id(pesanan_id)
        elif pilihan == '4':
            pesanan_id = input("ID untuk gunakan: ").strip()
            stack.gunakan_tiket(pesanan_id)
        elif pilihan == '5':
            print("Terima kasih!")
            break
        else:
            print("Pilihan invalid.")

if __name__ == "__main__":
    main()
