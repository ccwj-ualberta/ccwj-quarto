library(here)
library(bib2df)
library(dplyr)
library(stringr)
library(glue)

journals <- bib2df(here("publications/references.bib")) |>
  rename_with(tolower) |>
  filter(category == "ARTICLE") |>
  select(c(author, title, journal, year, volume, number, pages, doi)) |>
  mutate(
    author = sapply(author, function(x) paste(x, collapse = ", ")),
    title = str_remove_all(title, "\\{|\\}"),
    pages = str_replace_all(pages, "--", "-"),
    doi = if_else(
      !is.na(doi),
      paste0("https://doi.org/", doi),
      doi
    ),
    file_id = row_number()
  )

create_article <- function(title, author, journal, year, volume, number, pages, doi, file_id) {
  output <- c(
    "---",
    glue("title: '{title}'"),
    glue("year: {year}"),
    glue("author: '{author}'"),
    glue("doi: {doi}"),
    glue("journ: '{journal}'"),
    glue("volume: {volume}"),
    glue("number: {number}"),
    glue("pages: '{pages}'"),
    "---"
  )

  filename <- paste0("article-", file_id, ".qmd")
  file_path <- here("publications", "publications-articles", filename)
  file.create(file_path)
  writeLines(output, file_path)
}

msg <-
  list.files(here("publications/publications-articles"), full.names = TRUE) |>
  file.remove()

for (i in 1:nrow(journals)) {
  meta <- as.list(journals[i,])
  do.call(create_article, meta)
}
