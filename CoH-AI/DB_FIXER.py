import pandas as pd
import re

file_path = "/Users/erictech/Downloads/FosterCare.csv"

# Load file with comma delimiter
df = pd.read_csv(file_path, delimiter=",", encoding="utf-8")

# Drop the unwanted index column if it exists
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Cleaning function
def clean_text(s):
    if isinstance(s, str):
        # Remove all dash-like characters
        s = re.sub(r"[-–—•]", "", s)
        # Normalize smart quotes/apostrophes
        s = s.replace("“", '"').replace("”", '"').replace("’", "'")
        # Remove non-ASCII characters
        s = re.sub(r"[^\x00-\x7F]+", "", s)
        # Remove newlines and extra spaces
        s = s.replace("\n", " ").strip()
    return s

df = df.applymap(clean_text)

# Save final cleaned file
output_path = "/Users/erictech/Downloads/TEST5.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

output_path
