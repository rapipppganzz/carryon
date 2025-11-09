#!/usr/bin/env python3
"""
Bot Traffic Generator - Versi Interaktif
Selamat datang di menu saya!
"""

import requests
import threading
import time
import logging
import sys
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except:
        return False

def send_bot_traffic(url, bot_id, requests_per_bot, delay):
    """Fungsi untuk satu 'bot' mengirim banyak request"""
    session = requests.Session()
    headers = {
        "User-Agent": f"Mozilla/5.0 (compatible; Bot-{bot_id}/1.0)"
    }
    for i in range(requests_per_bot):
        try:
            resp = session.get(url, headers=headers, timeout=10)
            logging.info(f"Bot-{bot_id:02d} → {url} | Status: {resp.status_code}")
            if delay > 0:
                time.sleep(delay)
        except Exception as e:
            logging.error(f"Bot-{bot_id:02d} → Gagal: {str(e)[:50]}")

def main():
    print("🤖 Selamat datang di menu saya!")
    print("=" * 40)

    # Input target
    while True:
        target = input("🔗 Masukkan target website (contoh: https://example.com): ").strip()
        if validate_url(target):
            break
        print("❌ URL tidak valid! Gunakan format: https:// atau http://")

    # Input jumlah bot & request
    try:
        num_bots = int(input("👾 Jumlah 'bot' (misal: 10): ") or "10")
        req_per_bot = int(input("📨 Request per bot (misal: 20): ") or "20")
        delay = float(input("⏱️  Delay antar request per bot (detik, misal: 0.2): ") or "0.2")
    except ValueError:
        print("⚠️  Input tidak valid. Menggunakan nilai default.")
        num_bots, req_per_bot, delay = 10, 20, 0.2

    print("\n🚀 Memulai serangan bot... (Ini hanya simulasi traffic biasa!)")
    print(f"🎯 Target: {target}")
    print(f"🧍 Jumlah bot: {num_bots} | Total request: {num_bots * req_per_bot}")
    print("-" * 50)

    # Jalankan bot dalam thread
    threads = []
    for bot_id in range(1, num_bots + 1):
        t = threading.Thread(
            target=send_bot_traffic,
            args=(target, bot_id, req_per_bot, delay)
        )
        threads.append(t)
        t.start()

    try:
        for t in threads:
            t.join()
        print("\n✅ Semua bot selesai bekerja.")
    except KeyboardInterrupt:
        print("\n🛑 Dihentikan oleh pengguna.")

if __name__ == "__main__":
    main()
