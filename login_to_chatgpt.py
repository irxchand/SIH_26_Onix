import sys
import os
import json
import time

# Add BrowserAPIFree to path so we can import its modules
sys.path.insert(0, r"E:\Python\BrowserAPIFree")
try:
    from framework.browser_session import BrowserSession
except ImportError:
    print("Failed to import BrowserSession. Please run this script using E:\\Python\\BrowserAPIFree\\venv\\Scripts\\python.exe")
    sys.exit(1)

def do_login():
    print("="*60)
    print("  ChatGPT Login & Cookie Update")
    print("="*60)
    
    session = BrowserSession(session_id="login_session", headless=False, hidden_headful=False)
    page = session.start()
    
    print("\nNavigating to ChatGPT...")
    page.goto("https://chatgpt.com/")
    
    print("\n" + "*"*60)
    print(" PLEASE LOG IN TO CHATGPT IN THE BROWSER WINDOW.")
    print(" Verify that the account is 'Ishaan Chand'.")
    print(" Once you are fully logged in and can see the chat interface,")
    print(" press ENTER here in the console to save cookies.")
    print("*"*60 + "\n")
    
    input("Press ENTER when you are logged in... ")
    
    # Save the cookies to cookies.json
    cookies = session.context.cookies()
    cookies_path = r"E:\Python\BrowserAPIFree\cookies.json"
    
    with open(cookies_path, "w") as f:
        json.dump(cookies, f, indent=2)
        
    print(f"\n✅ Saved {len(cookies)} cookies to {cookies_path}")
    session.stop()
    print("Browser closed. You can now run 'python test_browser_quick.py' to test sending a message.")

if __name__ == "__main__":
    do_login()
