# converter.py
import os
import subprocess
from PIL import Image

def process_conversion(input_path, output_path, ext, temp_dir):
    if ext in ["png", "jpg", "jpeg", "bmp"]:
        img = Image.open(input_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_path, "PDF")
    elif ext in ["docx", "doc", "hwp", "txt"]:
        subprocess.run([
            "lowriter", "--headless", "--convert-to", "pdf",
            "--outdir", temp_dir, input_path
        ], check=True)
    else:
        raise ValueError("지원하지 않는 형식입니다.")
