stack = []  # Menyimpang kata2
print("Hallo")
print("Masukkan kata untuk menambahkan teks, 'UNDO' menghapus, atau 'EXIT' keluar.")
while True:
    user_input = input("\nMasukkan input: ").strip()  # Ambil input dan hapus spasi ekstra
    
    if user_input.upper() == "EXIT":
        print("Program selesai. Teks akhir:", " ".join(stack))
        break
    elif user_input.upper() == "UNDO":
        if stack:
            popped_word = stack.pop()  # Pop elemen terakhir (LIFO)
            print(f"Undo dilakukan: '{popped_word}' dihapus.")
        else:
            print("Stack kosong, tidak ada yang bisa di-undo.")
    else:
        # Asumsikan input adalah kata, push ke stack
        stack.append(user_input)
        print(f"Kata '{user_input}' ditambahkan.")
    
    # Tampilkan isi stack sebagai teks saat ini
    current_text = " ".join(stack) if stack else "Teks kosong"
    print(f"Teks saat ini: {current_text}")
