from PIL import Image
import os

folder = "known_faces"

for file in os.listdir(folder):
    if file.endswith(".jpg") or file.endswith(".png"):
        path = os.path.join(folder, file)
        img = Image.open(path).convert("RGB")  # force RGB
        img.save(path)  # overwrite with clean RGB version