import qrcode

BASE_URL = "http://192.168.1.9:5000"  # replace with your real IP

for table in range(1, 21):
    url = f"{BASE_URL}/table/{table}"
    img = qrcode.make(url)
    img.save(f"table_{table}.png")
    print(f"Generated QR for Table {table}: {url}")

print("Done!")