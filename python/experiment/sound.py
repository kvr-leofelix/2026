import requests
from playsound import playsound
import os

# 1. The URL of the sound
url = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
local_filename = "temp_audio.mp3"

# 2. Download the file locally (so MCI doesn't crash)
print("Downloading sound...")
response = requests.get(url)
with open(local_filename, 'wb') as f:
    f.write(response.content)

# 3. Get the absolute path (Fixes the OneDrive/Path error)
path = os.path.abspath(local_filename)

try:
    print(f"Playing: {path}")
    playsound(path)
finally:
    # Optional: Clean up the file after playing
    if os.path.exists(local_filename):
        os.remove(local_filename)