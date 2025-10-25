import os
import re
import pandas as pd
from pathlib import Path
from pyhere import here


def people2markdown(folder, **kwargs):
    """Create a markdown file for a person
    Parameters
    ----------
    folder : pathlib.Path
      The folder to write the markdown file to
    **kwargs : dict
      The keyword arguments passed to the function
    """

    name = " ".join([kwargs["name_given"], kwargs["name_family"]])
    markdown_fp = folder.joinpath(name + ".qmd")
    subtitle = kwargs["stream"]

    # find a file starting with the ID
    search_path = Path("assets", "member-photos")

    for f in search_path.glob(kwargs["id"] + "*"):
        image_path = str(f)
        break

    try:
        image_path = os.path.join("..", "..", image_path)
    except NameError:
        image_path = None

    # delete the file if it exists
    if markdown_fp.exists():
        markdown_fp.unlink()

    # write the file
    with open(markdown_fp, "w") as f:
        f.write("---\n")
        f.write("title: {}\n".format(name))

        if image_path is not None:
            f.write("image: {}\n".format(image_path))

        f.write("subtitle: {}\n".format(subtitle))
        f.write("about:\n")
        f.write("  template: solana\n")

        if image_path is not None:
            f.write("  image: {}\n".format(image_path))

        f.write("  links:\n")
        f.write("    - icon: email\n")
        f.write("      text: {}\n".format(kwargs["email"]))
        f.write("      href: mailto:{}\n".format(kwargs["email"]))

        if not pd.isna(kwargs["linkedin"]):
            linkedin_full = kwargs["linkedin"]
            linkedin_short = linkedin_full.rstrip("/").split("/")[-1]

            f.write("    - icon: linkedin\n")
            f.write("      text: {}\n".format(linkedin_short))
            f.write("      href: {}\n".format(linkedin_full))

        f.write("---\n")

        if not pd.isna(kwargs["prior_degrees"]) and kwargs["prior_degrees"] != "none":
            f.write("**Prior Degrees:** {}".format(kwargs["prior_degrees"]))
            f.write("\n")

        f.write("\n")
        f.write("{}\n".format(kwargs["bio"]))
        f.write("\n")

        if not pd.isna(kwargs["project"]) or not pd.isna(kwargs["project_title"]):
            f.write("#### Project\n")
            f.write("\n")

            if not pd.isna(kwargs["project_title"]):
                f.write("*{}*\n".format(kwargs["project_title"]))
                f.write("\n")
                f.write("{}\n".format(kwargs["project_desc"]))
            else:
                f.write(kwargs["project"])

    return None


def equipment2markdown(folder, **kwargs):
    """
    Create a markdown file for an equipment item
    """
    if kwargs["Include on website"] == "Yes":
        equip = str(kwargs["Equipment"])
        desc = str(kwargs["Description"])
        code = str(kwargs["Code"])

        markdown_name = (
            equip.lower()
            .replace(" ", "_")
            .replace("/", "-")
            .replace("(", "")
            .replace(")", "")
            .replace("#", "_")
            .replace("-", "_")
        )

        markdown_fp = folder.joinpath(markdown_name + ".qmd")

        # find the photo file starting with the Code
        search_path = here("assets", "about-us", "equipment-photos")

        for f in search_path.glob(code + "*"):
            image_path = f.relative_to(here())
            break

        try:
            image_path = Path("..", "..").joinpath(image_path)
        except NameError:
            image_path = None

        # delete the file if it exists
        if markdown_fp.exists():
            markdown_fp.unlink()

        # write the file
        with open(markdown_fp, "w") as f:
            f.write("---\n")
            f.write("title: {}\n".format(equip))
            f.write("categories: [{}]\n".format(kwargs["Category"]))

            if image_path is not None:
                f.write("image: {}\n".format(image_path))

            f.write("about:\n")
            f.write("  template: solana\n")

            if image_path is not None:
                f.write("  image: {}\n".format(image_path))

            f.write("---\n")
            f.write(desc)


def sponsors2markdown(folder, **kwargs):
    """
    Create a markdown file for a sponsor
    """
    company = str(kwargs["Company"])
    category = str(kwargs["Sponsors"])
    code = str(kwargs["Code"])

    markdown_name = (
        company.lower()
        .replace(" ", "_")
        .replace("/", "-")
        .replace("(", "")
        .replace(")", "")
        .replace("#", "_")
        .replace("-", "_")
        .replace("+", "_")
        .replace("&", "and")
    )

    markdown_name = re.sub("_+", "_", markdown_name)
    markdown_name = re.sub("[//.]$", "", markdown_name)
    markdown_fp = folder.joinpath(markdown_name + ".qmd")

    # find the photo file starting with the Code
    search_path = here("assets", "about-us", "sponsors-logos")

    for f in search_path.glob(code + "*"):
        image_path = f.relative_to(here())
        break

    try:
        image_path = Path("..", "..").joinpath(image_path)
    except NameError:
        image_path = None

    # delete the file if it exists
    if markdown_fp.exists():
        markdown_fp.unlink()

    # write the file
    with open(markdown_fp, "w") as f:
        f.write("---\n")
        f.write("title: {}\n".format(company))
        f.write("categories: [{}]\n".format(category))

        if image_path is not None:
            f.write("image: {}\n".format(image_path))

        f.write("about:\n")
        f.write("  template: solana\n")

        if image_path is not None:
            f.write("  image: {}\n".format(image_path))

        f.write("---\n")
