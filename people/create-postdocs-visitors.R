# remove existing postdocs.qmd and visitors.qmd files
unlink(c("people/postdocs.qmd", "people/visitors.qmd"), force = TRUE)

# check if the postdoc/visitor directories contain entries
postdocs <- list.files("people/postdocs", full.names = TRUE)

postdocs_content <- paste0(
  "---\n",
  "title: \"Postdocs\"\n",
  "listing:\n",
  "  contents: postdocs\n",
  "  type: default\n",
  "  sort:\n",
  "    - 'priority'\n",
  "    - 'title'\n",
  "  image-align: left\n",
  "  image-height: 350px\n",
  "  image-placeholder: ../assets/UA-COLOUR-NARROW.png\n",
  "  max-description-length: 600\n",
  "---\n"
)

if (length(postdocs) == 0) {
  postdocs_content <- paste0(
    postdocs_content,
    "\n",
    "There are no postdoctoral researchers at the CCWJ currently."
  )
}

writeLines(postdocs_content, "people/postdocs.qmd")

# visitors
visitors <- list.files("people/visitors", full.names = TRUE)

visitors_content <- paste0(
  "---\n",
  "title: \"Visitors\"\n",
  "listing:\n",
  "  contents: visitors\n",
  "  type: default\n",
  "  sort:\n",
  "    - 'priority'\n",
  "    - 'title'\n",
  "  image-align: left\n",
  "  image-height: 350px\n",
  "  image-placeholder: ../assets/UA-COLOUR-NARROW.png\n",
  "  max-description-length: 600\n",
  "---\n"
)

if (length(visitors) == 0) {
  visitors_content <- paste0(
    visitors_content,
    "\n",
    "There are no visiting researchers at the CCWJ currently."
  )
}

writeLines(visitors_content, "people/visitors.qmd")
