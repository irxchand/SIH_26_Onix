"""
BrowserAPIFree Interactive Test
Step 1: Cookie login — launches browser, loads cookies, verifies ChatGPT auth
Step 2: Send message — sends your message and prints the reply
"""
import subprocess, json, sys, os

PYTHON = r"E:\Python\BrowserAPIFree\venv\Scripts\python.exe"
CLI    = r"E:\Python\BrowserAPIFree\cli.py"
CHAT   = "https://chatgpt.com/c/6a92fff8-d234-83e9-988e-5e04ab074efb"


def run_cli(payload: dict) -> dict:
    """Run the BrowserAPIFree CLI and return parsed JSON output."""
    raw = json.dumps(payload)
    result = subprocess.run(
        [PYTHON, CLI, "--input", raw],
        capture_output=True, text=True
    )
    if result.stderr:
        for line in result.stderr.strip().splitlines():
            print(f"  [log] {line}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"  [raw] {result.stdout}")
        return {"success": False, "error": "Could not parse CLI output"}


def step_cookie_login():
    """Step 1: Initialize session with cookies and verify login."""
    print("\n" + "="*50)
    print("STEP 1: Cookie Login")
    print("="*50)

    cookies_path = r"E:\Python\BrowserAPIFree\cookies.json"
    if not os.path.exists(cookies_path):
        print(f"❌ cookies.json not found at {cookies_path}")
        print("   Export your ChatGPT cookies first.")
        return False

    with open(cookies_path, "r") as f:
        cookies = json.load(f)
    print(f"  Found {len(cookies)} cookies in cookies.json")

    # Check for key auth cookies
    cookie_names = {c.get("name", "") for c in cookies}
    has_session = any("session" in n.lower() or "token" in n.lower() or "__Secure" in n for n in cookie_names)
    print(f"  Auth-related cookies present: {'✅ Yes' if has_session else '⚠️  Not obvious'}")

    print("\n  Launching browser & loading cookies...")
    out = run_cli({
        "command": "INITIALIZE",
        "sessionId": "cookie_test",
        "headless": False,
    })

    if out.get("success") and out["data"]["status"] == "READY":
        print(f"\n  ✅ Browser session READY — cookies loaded successfully")
        return True
    else:
        print(f"\n  ❌ Session failed: {out.get('error', 'unknown')}")
        return False


def step_send_message():
    """Step 2: Send a message to the target chat."""
    print("\n" + "="*50)
    print("STEP 2: Send Message")
    print("="*50)

    msg = input("  Your message (Enter for default): ").strip()
    if not msg:
        msg = "Connection test from SIH project — please confirm you can see this."

    print(f"\n  >> Sending: {msg}")
    print("  Waiting for ChatGPT response...\n")

    out = run_cli({
        "command": "SEND_CHAT",
        "headless": False,
        "targetUrl": CHAT,
        "message": msg,
    })

    if out.get("success"):
        data = out["data"]
        print(f"  ✅ ChatGPT replied:")
        print(f"  {data['message']}")
        m = data.get("metrics", {})
        print(f"\n  TTFT: {m.get('t_ttft', 0):.0f}ms | Stream: {m.get('t_streaming', 0):.0f}ms")
    else:
        print(f"  ❌ Failed: {out.get('error')}")


if __name__ == "__main__":
    print("BrowserAPIFree — Interactive Test")
    print(f"Target chat: {CHAT}")

    # Step 1
    if not step_cookie_login():
        sys.exit(1)

    # Step 2
    step_send_message()

    print("\n✅ Test complete.")
