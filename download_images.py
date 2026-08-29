import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    'real_xray_normal.png': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Chest_Xray_PA_3-8-2010.png/512px-Chest_Xray_PA_3-8-2010.png',
    'real_xray_anomaly.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Chest_X-ray_of_a_patient_with_pneumonia.jpg/512px-Chest_X-ray_of_a_patient_with_pneumonia.jpg',
    'real_xray_anomaly2.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Cardiomegaly.jpg/512px-Cardiomegaly.jpg',
    'real_xray_normal2.jpg': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Normal_posteroanterior_%28PA%29_chest_radiograph_%28X-ray%29.jpg/512px-Normal_posteroanterior_%28PA%29_chest_radiograph_%28X-ray%29.jpg'
}

for name, url in urls.items():
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Downloading {name}...")
    try:
        with urllib.request.urlopen(req, context=ctx) as r, open(f"data/uploads/{name}", 'wb') as f:
            f.write(r.read())
        print(f"Success: {name}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
