library(here)
library(bib2df)
library(dplyr)
library(stringr)
library(glue)

papers <- bib2df(here("publications/references.bib")) |>
  rename_with(tolower) |>
  filter(category == "INPROCEEDINGS") |>
  select(c(author, title, year, booktitle)) |>
  rename(conference = "booktitle") |>
  mutate(
    author = sapply(author, function(x) paste(x, collapse = ", ")),
    title = str_remove_all(title, "\\{|\\}"),
    conference = str_remove_all(conference, "\\{|\\}"),

    # remove single backslashes
    title = str_remove_all(title, "\\\\"),
    conference = str_remove_all(conference, "\\\\"),
    file_id = row_number()
  )

create_conference <- function(title, author, conference, year, file_id) {
  output <- c(
    "---",
    glue('title: "{title}"'),
    glue('author: "{author}"'),
    glue('conference: "{conference}"'),
    glue("year: {year}"),
    "---"
  )

  filename <- paste0("proceedings-", file_id, ".qmd")
  file_path <- here("publications", "publications-proceedings", filename)
  file.create(file_path)
  writeLines(output, file_path)
}

msg <-
  list.files(here("publications/publications-proceedings"), full.names = TRUE) |>
  file.remove()

for (i in 1:nrow(papers)) {
  meta <- as.list(papers[i,])
  do.call(create_conference, meta)
}
