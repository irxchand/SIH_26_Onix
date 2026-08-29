import subprocess
import sys

with open('test_llm.json') as f:
    data = f.read()

result = subprocess.run([sys.executable, r'E:\Python\BrowserAPIFree\cli.py', '--input', data], capture_output=True, text=True)
print(result.stdout)
print(result.stderr, file=sys.stderr)
