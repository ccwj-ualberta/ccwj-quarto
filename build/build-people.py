import os
import pandas as pd
from pyhere import here
from excel2markdown import people2markdown


# execute
df = pd.read_excel(here("CCWJ_Website.xlsx"), sheet_name="People")
df = df.iloc[:, 0:16]
df.columns = [
  "Timestamp",
  "Email",
  "ID",
  "Given Name",
  "Family Name",
  "Degree",
  "Involvement",
  "Stream",
  "Prior Degrees",
  "Project Description",
  "Photo URL",
  "Bio",
  "Thesis Title",
  "Thesis Description",
  "Thesis photo",
  "LinkedIn"
]

# remove duplicated ids (keeping newest)
df = df.sort_values("Timestamp").groupby("ID").last().reset_index()

involvement = {
  "mscs": "Master's student",
  "staff": "Staff",
  "bscs": "Bachelor's student",
  "phds": "PhD student",
  "alumn": "Alumn",
  "alumn-visitors": "Alumn (Visitor)",
  "alumn-ug": "Alumn (UG)"
}

for k, v in involvement.items():
  folder = here("people", k)
  os.makedirs(folder, exist_ok=True)

  for f in folder.glob("*.qmd"):
    f.unlink()

  df_sel = df[df.loc[:, "Involvement"] == v].reset_index(drop=True)
  
  for i, member in df_sel.iterrows():
    meta = {
      "id": member["ID"],
      "name_given": member["Given Name"],
      "name_family": member["Family Name"],
      "email": member["Email"],
      "prior_degrees": member["Prior Degrees"],
      "project": member["Project Description"],
      "project_title": member["Thesis Title"],
      "project_desc": member["Thesis Description"],
      "linkedin": member["LinkedIn"],
      "bio": member["Bio"],
      "stream": member["Stream"]
    }
    people2markdown(folder, **meta)
