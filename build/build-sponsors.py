import os
import pandas as pd
from pyhere import here
from excel2markdown import sponsors2markdown


df = pd.read_excel(here("CCWJ_Website.xlsx"), sheet_name="About_Sponsors")
df = df.iloc[2:, ]
df = df.dropna(how="all")

df["Sponsors"] = df["Sponsors"].ffill()
df["Sponsors"].unique()

df.loc[df["Sponsors"] == "Lab equipment, consumables, etc.", "Sponsors"] = "Lab equipment and consumables"
df.loc[df["Sponsors"] == "Weldco / Industry Chair", "Sponsors"] = "Welco industry chair"

folder = here("about", "sponsors")
os.makedirs(folder, exist_ok=True)

existing = folder.glob("*.qmd")

for f in existing:
    f.unlink()

for _, data in df.iterrows():
    kwargs = data.to_dict()
    sponsors2markdown(folder, **kwargs)
