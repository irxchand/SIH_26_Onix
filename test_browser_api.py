import sys
import os
import json
import subprocess

cli_input = {
    "command": "SEND_CHAT",
    "headless": False,
    "targetUrl": "https://chatgpt.com/c/6a92fff8-d234-83e9-988e-5e04ab074efb",
    "message": "Hello from python script!"
}

tmp_path = "test_llm.json"
with open(tmp_path, "w") as f:
    json.dump(cli_input, f)

python_exe = r"E:\Python\BrowserAPIFree\venv\Scripts\python.exe"
cli_script = r"E:\Python\BrowserAPIFree\cli.py"

with open(tmp_path, "r") as f:
    raw_json = f.read()

print("Running BrowserAPIFree...")
result = subprocess.run(
    [python_exe, cli_script, "--input", raw_json],
    capture_output=True,
    text=True
)

print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")

os.remove(tmp_path)
