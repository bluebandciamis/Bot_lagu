# Bot Lirik Lagu

Bot Python untuk menampilkan lirik lagu yang sedang diputar di Windows. Bot membaca lagu aktif melalui Windows Media Control, lalu mencari lirik di LRCLIB. Jika lirik tersinkron tersedia, baris lirik akan mengikuti posisi lagu.

## Persyaratan

- Windows 10 atau Windows 11
- Python 3.8 atau lebih baru (disarankan Python 3.10–3.12)
- Koneksi internet untuk mencari lirik di LRCLIB
- Pemutar musik/browser yang menampilkan lagu melalui Windows Media Control, misalnya Spotify atau browser

## Instalasi dan menjalankan

Buka **PowerShell** atau **Terminal**, lalu jalankan:

```powershell
# Clone repositori
git clone https://github.com/bluebandciamis/Bot_lagu.git
cd Bot_lagu

# Buat dan aktifkan virtual environment
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Pasang dependensi Windows SDK untuk Python
python -m pip install --upgrade pip
python -m pip install winsdk

# Jalankan bot
python Botlagu.py
```

Kalau PowerShell menolak aktivasi virtual environment karena kebijakan eksekusi, jalankan perintah berikut di terminal tersebut, lalu aktifkan ulang:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Pengaturan ini hanya berlaku selama jendela PowerShell tersebut terbuka. Alternatifnya, tanpa mengaktifkan environment, jalankan instalasi dan bot melalui path Python di environment:

```powershell
.\.venv\Scripts\python.exe -m pip install winsdk
.\.venv\Scripts\python.exe Botlagu.py
```

## Cara menggunakan

1. Putar lagu di Spotify atau browser dan pastikan Windows menampilkan informasinya di media control.
2. Jalankan `python Botlagu.py` dari folder proyek.
3. Biarkan terminal tetap terbuka. Bot akan menampilkan lirik dan memperbarui baris aktif jika lirik tersinkron tersedia.
4. Tekan `Ctrl+C` untuk menghentikan bot.

## Troubleshooting

- **`No module named 'winsdk'`**: pastikan virtual environment aktif, lalu jalankan `python -m pip install winsdk` di terminal yang sama.
- **Bot terus menunggu lagu**: pastikan lagu sedang diputar dan pemutar/browser mengirim informasi media ke Windows Media Control.
- **Lirik tidak ditemukan**: cek koneksi internet. Tidak semua lagu memiliki lirik di LRCLIB.
- **Perintah `py` tidak dikenal**: instal Python dari [python.org](https://www.python.org/downloads/windows/) dan aktifkan opsi **Add Python to PATH** saat instalasi, lalu buka terminal baru.

## Dependensi

Bot memakai pustaka standar Python dan paket [`winsdk`](https://pypi.org/project/winsdk/) untuk mengakses Windows Media Control. Tidak perlu memasang paket terpisah untuk HTTP atau JSON.