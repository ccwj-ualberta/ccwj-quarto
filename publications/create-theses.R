library(here)
library(bib2df)
library(dplyr)
library(stringr)
library(glue)

theses <- bib2df(here("publications/references.bib")) |>
  rename_with(tolower) |>
  filter(category %in% c("PHDTHESIS", "MASTERSTHESIS")) |>
  select(c(author, school, title, year)) |>
  mutate(
    author = sapply(author, function(x) paste(x, collapse = ", ")),
    title = str_remove_all(title, "\\{|\\}"),
    title = str_remove_all(title, "\\\\"),
    school = str_remove_all(school, "\\{|\\}"),
    school = str_remove_all(school, "\\\\"),
    school = if_else(is.na(school), "", school)
  )

create_thesis <- function(author, school, title, year) {
  output <- c(
    "---",
    glue('title: "{title}"'),
    glue('author: "{author}"'),
    glue('school: "{school}"'),
    glue("year: {year}"),
    "---"
  )

  filename <- tolower(title)
  filename <- str_sub(filename, 1, 50)
  filename <- gsub(" ", "-", filename)
  filename <- gsub("[^[:alnum:]-]", "", filename)
  filename <- gsub("--", "-", filename)
  filename <- gsub(",", "", filename)
  filename <- paste0(filename, ".qmd")

  file_path <- here("publications", "publications-theses", filename)
  file.create(file_path)
  writeLines(output, file_path)
}

msg <-
  list.files(here("publications/publications-theses"), full.names = TRUE) |>
  file.remove()

for (i in 1:nrow(theses)) {
  meta <- as.list(theses[i,])
  do.call(create_thesis, meta)
}
