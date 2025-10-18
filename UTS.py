from datetime import datetime, timedelta

class TiketStack:
    def __init__(self):
        self.bookings = []  # Stack list (LIFO)
        self.data = {}      # Dict untuk akses cepat berdasarkan ID
        self.tenggat_waktu = timedelta(hours=1)

    def _cek_status(self, booking):
        _, _, waktu_pemesanan, status = booking
        if status != 'active':
            return status
        return 'expired' if datetime.now() > waktu_pemesanan + self.tenggat_waktu else 'active'

    def pesan_tiket(self, pesanan_id, nama):
        if pesanan_id in self.data:
            print(f"ID {pesanan_id} sudah digunakan.")
            return
        waktu_pemesanan = datetime.now()
        booking = (pesanan_id, nama, waktu_pemesanan, 'active')
        self.bookings.append(booking)
        self.data[pesanan_id] = booking
        tenggat = waktu_pemesanan + self.tenggat_waktu
        print(f"Tiket berhasil dipesan untuk {nama} dengan ID {pesanan_id} pada {waktu_pemesanan:%Y-%m-%d %H:%M}.")
        print(f"Tenggat: {tenggat:%Y-%m-%d %H:%M}.")

    def cari_berdasarkan_id(self, pesanan_id):
        print(f"Mencari pesanan ID: {pesanan_id}")
        booking = self.data.get(pesanan_id)
        if not booking:
            print("Pesanan tidak ditemukan.")
            return

        status = self._cek_status(booking)
        waktu_pesan = booking[2]
        tenggat = waktu_pesan + self.tenggat_waktu

        if status == 'expired':
            print(f"Tiket ID {pesanan_id} sudah hangus sejak {tenggat:%Y-%m-%d %H:%M}.")
        elif status == 'used':
            print(f"Tiket ID {pesanan_id} sudah digunakan dan hilang.")
        else:
            print(f"Ditemukan: ID {booking[0]}, Nama {booking[1]}, Waktu {waktu_pesan:%Y-%m-%d %H:%M}, Status: ACTIVE")

    def gunakan_tiket(self, pesanan_id):
        print(f"Menggunakan tiket ID: {pesanan_id}")
        booking = self.data.get(pesanan_id)
        if not booking:
            print("Tiket tidak ditemukan.")
            return

        status = self._cek_status(booking)
        if status == 'expired':
            print("Tiket sudah hangus dan tidak bisa digunakan.")
        elif status == 'used':
            print("Tiket sudah digunakan sebelumnya.")
        else:
            self.bookings.remove(booking)
            self.data.pop(pesanan_id, None)
            print("Tiket berhasil digunakan dan dihapus.")

    def urutkan_berdasarkan_waktu(self):
        # Hanya urutkan tiket aktif berdasarkan waktu pemesanan
        self.bookings = sorted(
            [b for b in self.bookings if self._cek_status(b) == 'active'],
            key=lambda b: b[2]
        )
        # Update ulang dictionary agar sinkron
        self.data = {b[0]: b for b in self.bookings}
        print("Stack diurutkan berdasarkan waktu untuk tiket aktif.")

    def tampilkan_semua(self):
        if not self.bookings:
            print("Belum ada pesanan.")
            return

        print("\nDaftar Pesanan (terlama ke terbaru):")
        for id_b, nama, waktu, status_awal in sorted(self.bookings, key=lambda b: b[2]):
            status = self._cek_status((id_b, nama, waktu, status_awal))
            tenggat = waktu + self.tenggat_waktu
            waktu_str = waktu.strftime('%Y-%m-%d %H:%M')
            tenggat_str = tenggat.strftime('%Y-%m-%d %H:%M')

            if status == 'active':
                print(f"ID: {id_b}, Nama: {nama}, Waktu: {waktu_str}, Tenggat: {tenggat_str}, Status: ACTIVE")
            elif status == 'expired':
                print(f"ID: {id_b}, Nama: {nama}, Waktu: {waktu_str}, Tenggat: {tenggat_str}, Status: HANGUS")
            else:
                print(f"ID: {id_b}, Nama: {nama}, Waktu: {waktu_str}, Status: DIPAKAI")
        print()


def main():
    stack = TiketStack()
    while True:
        print("\n=== Sistem Pemesanan Tiket ===")
        print("1. Pesan Tiket")
        print("2. Cari Pesanan (ID)")
        print("3. Gunakan Tiket")
        print("4. Urutkan berdasarkan Waktu")
        print("5. Tampilkan Semua")
        print("6. Keluar")
        pilihan = input("Pilih (1-6): ").strip()

        if pilihan == '1':
            stack.pesan_tiket(input("ID Pesanan: ").strip(), input("Nama: ").strip())
        elif pilihan == '2':
            stack.cari_berdasarkan_id(input("ID untuk cari: ").strip())
        elif pilihan == '3':
            stack.gunakan_tiket(input("ID untuk gunakan: ").strip())
        elif pilihan == '4':
            stack.urutkan_berdasarkan_waktu()
        elif pilihan == '5':
            stack.tampilkan_semua()
        elif pilihan == '6':
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
