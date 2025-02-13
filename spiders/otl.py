# %% IMPORTS

import csv
import shutil
from pathlib import Path

# %% CONFIGS

ROOT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = ROOT_FOLDER / "data" / "otl"
OUTPUT_FOLDER = DATA_FOLDER / "records"
INPUT_FILE = DATA_FOLDER / "otl.csv"
FAQ_FILE = DATA_FOLDER / "faq.txt"
INCLUDE_FIELDS = [
    "OTL ID",
    "Title",
    "Copyright Year",
    "Contributors",
    "library URL",
    "Publisher",
    "License",
    "Description",
]

# %% INITIALIZES

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
shutil.copyfile(FAQ_FILE, OUTPUT_FOLDER / FAQ_FILE.name)

# %% TRANSFORMATIONS

with open(INPUT_FILE, "r") as reader:
    for row in csv.DictReader(reader):
        file_name = f"{row['OTL ID']}.txt"
        with open(OUTPUT_FOLDER / file_name, "w") as writer:
            for field in INCLUDE_FIELDS:
                val = row.get(field)
                if not val:
                    continue
                writer.write(f"- {field}: {val}\n")
            print(".", end="")
