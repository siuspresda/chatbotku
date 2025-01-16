#BLOOM+EXCEL 2 FILE+KATA

import telepot
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import threading

# Ganti dengan token bot Telegram Anda
TELEGRAM_API_TOKEN = '7947083353:AAE5fyGFLdT-YcCuFCU44Nk4X5EJLD6wmi4'

# Inisialisasi model Bloom
model_name = "bigscience/bloom-560m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Fungsi untuk menghasilkan jawaban dengan model Bloom
def generate_bloom_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model.generate(inputs["input_ids"], max_length=50, num_return_sequences=1, temperature=0.9, top_p=0.95, top_k=50)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response_cleaned = response.replace("<extra_id_0>", "").strip()
    return response_cleaned

# Fungsi untuk membaca data produk dari Excel
def read_product_data(filename):
    try:
        df = pd.read_excel(filename)
        return df
    except Exception as e:
        print(f"Error membaca file: {e}")
        return None

# Fungsi untuk membaca profil perusahaan dari Excel
def read_company_profile(filename):
    try:
        df = pd.read_excel(filename)
        return df
    except Exception as e:
        print(f"Error membaca file: {e}")
        return None

# Fungsi untuk menanggapi pencarian produk berdasarkan kata kunci
def get_filtered_product_details(df, keywords):
    print(f"Kata kunci yang diterima untuk produk: {keywords}")
    if df is None:
        return None

    filtered_data = df.copy()
    filter_applied = False

    # Filter kategori produk
    if 'laptop' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('laptop', case=False, na=False)]
        filter_applied = True
    elif 'komputer' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('komputer', case=False, na=False)]
        filter_applied = True
    elif 'server' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('server', case=False, na=False)]
        filter_applied = True
    elif 'aksesori' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('aksesori', case=False, na=False)]
        filter_applied = True

    # Filter kategori produk
    if 'acer' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('acer', case=False, na=False)]
        filter_applied = True
    elif 'asus' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('asus', case=False, na=False)]
        filter_applied = True
    elif 'zyrex' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('zyrex', case=False, na=False)]
        filter_applied = True
    elif 'mybook' in keywords:
        filtered_data = filtered_data[filtered_data['Nama Produk'].str.contains('mybook', case=False, na=False)]
        filter_applied = True

    # Filter prosesor
    if 'i3' in keywords:
        filtered_data = filtered_data[filtered_data['Processor'].str.contains('i3', case=False, na=False)]
        filter_applied = True
    if 'i5' in keywords:
        filtered_data = filtered_data[filtered_data['Processor'].str.contains('i5', case=False, na=False)]
        filter_applied = True
    if 'i7' in keywords:
        filtered_data = filtered_data[filtered_data['Processor'].str.contains('i7', case=False, na=False)]
        filter_applied = True
    if 'i9' in keywords:
        filtered_data = filtered_data[filtered_data['Processor'].str.contains('i9', case=False, na=False)]
        filter_applied = True
    if 'ryzen' in keywords:
        filtered_data = filtered_data[filtered_data['Processor'].str.contains('ryzen', case=False, na=False)]
        filter_applied = True

    # Filter RAM
    if '4gb' in keywords:
        filtered_data = filtered_data[filtered_data['RAM'].str.contains('4GB', case=False, na=False)]
        filter_applied = True
    if '8gb' in keywords:
        filtered_data = filtered_data[filtered_data['RAM'].str.contains('8GB', case=False, na=False)]
        filter_applied = True
    if '16gb' in keywords:
        filtered_data = filtered_data[filtered_data['RAM'].str.contains('16GB', case=False, na=False)]
        filter_applied = True
    if '32gb' in keywords:
        filtered_data = filtered_data[filtered_data['RAM'].str.contains('32GB', case=False, na=False)]
        filter_applied = True

    # Filter storage
    if 'ssd' in keywords:
        filtered_data = filtered_data[filtered_data['Storage'].str.contains('SSD', case=False, na=False)]
        filter_applied = True
    if 'hdd' in keywords:
        filtered_data = filtered_data[filtered_data['Storage'].str.contains('HDD', case=False, na=False)]
        filter_applied = True

    # Filter TKDN
    if 'tkdn' in keywords:
        filtered_data = filtered_data[filtered_data['Jenis Produk'].str.contains('TKDN', case=False, na=False)]
        filter_applied = True
    if 'pdn' in keywords:
        filtered_data = filtered_data[filtered_data['Jenis Produk'].str.contains('PDN', case=False, na=False)]
        filter_applied = True

    # Filter harga
    if 'murah' in keywords:
        filtered_data = filtered_data[filtered_data['Harga Tayang'] < 10000000]
        filter_applied = True
    if '3 juta' in keywords and '5 juta' in keywords:
        filtered_data = filtered_data[(filtered_data['Harga Tayang'] >= 3000000) & (filtered_data['Harga Tayang'] <= 5000000)]
        filter_applied = True
    if '5 juta' in keywords and '7 juta' in keywords:
        filtered_data = filtered_data[(filtered_data['Harga Tayang'] >= 5000000) & (filtered_data['Harga Tayang'] <= 7000000)]
        filter_applied = True

    # Jika tidak ada filter yang diterapkan, atau data kosong
    if not filter_applied or filtered_data.empty:
        print("Tidak ada data yang cocok dengan filter.")
        return None

    # Menyusun detail produk yang sesuai
    details = ""
    for index, row in filtered_data.iterrows():
        details += f"{row['Nama Produk']} - {row['Processor']} - {row['RAM']} - {row['Jenis Produk']} - {row['Storage']} - Harga: {row['Harga Tayang']}\n"

    return details


# Fungsi untuk menanggapi pencarian profil perusahaan berdasarkan kata kunci
def get_filtered_company_details(df, keywords):
    print(f"Kata kunci yang diterima untuk profil perusahaan: {keywords}")
    if df is None:
        return None

    filtered_data = df.copy()
    filter_applied = False
    details = ""

    # Menampilkan hanya kolom yang relevan berdasarkan kata kunci
    keywords = [k.lower() for k in keywords]  # Menjadikan semua kata kunci huruf kecil

    if 'profil' in keywords or 'perusahaan' in keywords or 'cemerlang' in keywords:
        if 'Profil Perusahaan' in df.columns:
            details = f"Profil Perusahaan: {df['Profil Perusahaan'].iloc[0]}\n"
        filter_applied = True
    elif 'kontak' in keywords:
        if 'Kontak' in df.columns:
            details = f"Kontak: {df['Kontak'].iloc[0]}\n"
        filter_applied = True
    elif 'alamat' in keywords:
        if 'Alamat' in df.columns:
            details = f"Alamat: {df['Alamat'].iloc[0]}\n"
        filter_applied = True
    elif 'website' in keywords:
        if 'Website' in df.columns:
            details = f"Website: {df['Website'].iloc[0]}\n"
        filter_applied = True
    elif 'email' in keywords:
        if 'Email' in df.columns:
            details = f"Email: {df['Email'].iloc[0]}\n"
        filter_applied = True
    elif 'jenis produk' in keywords:
        if 'Jenis Produk' in df.columns:
            details = f"Jenis Produk: {df['Jenis Produk'].iloc[0]}\n"
        filter_applied = True

    # Jika tidak ada filter yang diterapkan, atau data kosong
    if not filter_applied or not details:
        print("Tidak ada data yang cocok untuk profil perusahaan.")
        return None

    return details


# Fungsi untuk menangani pesan yang diterima
def handle_message(msg):
    chat_id = msg['chat']['id']
    message_text = msg.get('text', '').lower()  # Menjaga agar tidak peka terhadap huruf besar/kecil

    # Menangani pesan sapaan
    if 'halo' in message_text or 'hai' in message_text or 'assalamualaikum' in message_text or 'hallo' in message_text or 'selamat pagi' in message_text or 'selamat siang' in message_text or 'selamat sore' in message_text or 'selamat malam' in message_text:
        bot.sendMessage(chat_id, "Halo! Ada yang bisa saya bantu?,silahkan tulisakan jenis barang elektronik atau spesifikasi yang anda cari")
        return

    # Jika mengandung kata kunci produk
    product_keywords = ['laptop', 'komputer', 'server', 'aksesori', 'acer', 'asus', 'zyrex', 'mybook', 'i3', 'i5', 'i7','i9', 'ryzen', '4gb', '8gb','16gb','32gb', 'ssd', 'hdd', 'tkdn', 'pdn', 'murah', '3 juta', '5 juta', '7 juta']
    if any(keyword in message_text for keyword in product_keywords):
        product_details = get_filtered_product_details(products_df, message_text.split())
        if product_details:
            bot.sendMessage(chat_id, product_details)
        else:
            bot.sendMessage(chat_id, "Tidak ada produk yang ditemukan dengan kriteria yang Anda cari.")
        return

    # Jika mengandung kata kunci profil perusahaan
    company_keywords = ['profil', 'perusahaan', 'kontak', 'alamat', 'website', 'email', 'jenis produk']
    if any(keyword in message_text for keyword in company_keywords):
        company_details = get_filtered_company_details(company_profile_df, message_text.split())
        if company_details:
            bot.sendMessage(chat_id, company_details)
        else:
            bot.sendMessage(chat_id, "Tidak ada informasi profil perusahaan yang ditemukan.")
        return

    # Jika tidak ada kata kunci yang dikenali, jawab dengan Bloom
    bloom_response = generate_bloom_response(message_text)
    bot.sendMessage(chat_id, bloom_response)

# Inisialisasi bot Telegram
bot = telepot.Bot(TELEGRAM_API_TOKEN)

# Membaca data produk dan profil perusahaan
products_df = read_product_data('cac-dataf.xlsx')
company_profile_df = read_company_profile('Profil-Perusahaan.xlsx')

# Menjalankan bot Telegram dan menunggu pesan
bot.message_loop(handle_message)
print("Bot Telegram siap menerima pesan...")

# Menjaga bot tetap berjalan
while True:
    time.sleep(10)
