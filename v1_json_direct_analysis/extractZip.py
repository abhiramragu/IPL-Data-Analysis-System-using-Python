import zipfile
from pathlib import Path

SRC=Path("data\\raw\\ipl_json.zip")
DST=Path("data\\raw\\ipl_json_files")

DST.mkdir(exist_ok='True')

with zipfile.ZipFile(SRC, "r") as z:
    z.extractall(DST)
print("Extraction completed")