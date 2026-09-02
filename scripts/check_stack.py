import urllib.request
import json
import sys

print("==================================================")
print("   ONIX-QML FULL-STACK DIAGNOSTIC & HEALTH CHECK   ")
print("==================================================")

# 1. FastAPI Backend Check
try:
    with urllib.request.urlopen("http://localhost:8000/health", timeout=3) as resp:
        data = json.loads(resp.read().decode())
        print(f"[OK] [1/4] FastAPI Backend (Port 8000): HEALTHY ({data.get('message', '')})")
except Exception as e:
    print(f"[FAIL] [1/4] FastAPI Backend (Port 8000): DOWN ({e})")

# 2. Quantum Circuit API Check
try:
    with urllib.request.urlopen("http://localhost:8000/api/v1/quantum/circuit/ascii", timeout=3) as resp:
        data = json.loads(resp.read().decode())
        if data.get("status") == "success":
            print(f"[OK] [2/4] Quantum Circuit API: HEALTHY (Active circuit: {data.get('selected')})")
        else:
            print("[WARN] [2/4] Quantum Circuit API: UNEXPECTED RESPONSE")
except Exception as e:
    print(f"[FAIL] [2/4] Quantum Circuit API: DOWN ({e})")

# 3. Next.js Frontend Check
try:
    with urllib.request.urlopen("http://localhost:3000", timeout=3) as resp:
        if resp.status == 200:
            print("[OK] [3/4] Next.js Frontend (Port 3000): HEALTHY (200 OK)")
        else:
            print(f"[WARN] [3/4] Next.js Frontend (Port 3000): Status {resp.status}")
except Exception as e:
    print(f"[FAIL] [3/4] Next.js Frontend (Port 3000): DOWN ({e})")

# 4. Chrome CDP & ChatGPT Session Check
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        chat_found = False
        chat_url = ""
        for ctx in b.contexts:
            for pg in ctx.pages:
                if "chatgpt.com" in pg.url:
                    chat_found = True
                    chat_url = pg.url
                    break
        if chat_found:
            print(f"[OK] [4/4] Chrome CDP (Port 9222): HEALTHY (Active ChatGPT tab: {chat_url})")
        else:
            print("[WARN] [4/4] Chrome CDP (Port 9222): Connected, but ChatGPT tab is missing!")
            print("       -> Auto-opening ChatGPT target tab in Chrome...")
            ctx = b.contexts[0] if b.contexts else b.new_context()
            new_page = ctx.new_page()
            new_page.goto("https://chatgpt.com/c/6a92fff8-d234-83e9-988e-5e04ab074efb", wait_until="domcontentloaded")
            print("       -> ChatGPT target tab opened successfully!")
except Exception as e:
    print(f"[FAIL] [4/4] Chrome CDP (Port 9222): DOWN ({e})")

print("==================================================")
