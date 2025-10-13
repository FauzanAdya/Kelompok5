from collections import deque  # Import deque untuk queue efisien
# Implementasi Queue sederhana menggunakan deque
queue = deque()  # Queue kosong untuk menyimpan nama pelanggan 
print("Simulasi Antrian Penyewaan PS")
print("Masukkan nama pelanggan untuk bergabung antrian, 'LAYANI' untuk melayani pelanggan pertama, atau 'EXIT' untuk keluar.")
while True:
    user_input = input("\nMasukkan input: ").strip()  # Ambil input dan hapus spasi ekstra
    
    if user_input.upper() == "EXIT":
        print("Program selesai. Antrian akhir:", list(queue))
        break
    elif user_input.upper() == "LAYANI":
        if queue:
            served_customer = queue.popleft()  # Dequeue pelanggan pertama (FIFO)
            print(f"Pelanggan '{served_customer}' dilayani.")
        else:
            print("Queue kosong, tidak ada pelanggan untuk dilayani.")
    else:
        # Asumsikan input adalah nama pelanggan, enqueue ke queue
        queue.append(user_input)
        print(f"Pelanggan '{user_input}' bergabung antrian.")
    
    # Tampilkan isi queue sebagai daftar antrian saat ini
    if queue:
        print("Daftar antrian saat ini:")
        for i, customer in enumerate(queue, start=1):
            print(f"{i}. {customer}")
    else:
        print("Antrian kosong.")