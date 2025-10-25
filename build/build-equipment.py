import os
import pandas as pd
from pyhere import here
from excel2markdown import equipment2markdown


df = pd.read_excel(here("CCWJ_Website.xlsx"), sheet_name="About_Lab_Equipment")
df["Category"] = df["Category"].fillna("Computer / Software")

folder = here("about", "equipment")
os.makedirs(folder, exist_ok=True)

existing = folder.glob("*.qmd")

for f in existing:
    f.unlink()

for _, data in df.iterrows():
    kwargs = data.to_dict()
    equipment2markdown(folder, **kwargs)
