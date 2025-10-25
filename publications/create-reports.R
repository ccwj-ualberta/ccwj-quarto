library(here)
library(bib2df)
library(dplyr)
library(stringr)
library(glue)

reports <- bib2df(here("publications/references.bib")) |>
  rename_with(tolower) |>
  filter(category == "TECHREPORT") |>
  select(c(author, institution, title, year)) |>
  mutate(
    author = sapply(author, function(x) paste(x, collapse = ", ")),
    title = str_remove_all(title, "\\{|\\}"),
    title = str_remove_all(title, "\\\\"),
    institution = str_remove_all(institution, "\\{|\\}"),
    institution = str_remove_all(institution, "\\\\"),
    institution = if_else(is.na(institution), "", institution),
    file_id = row_number()
  )

create_report <- function(author, institution, title, year, file_id) {
  output <- c(
    "---",
    glue('title: "{title}"'),
    glue('author: "{author}"'),
    glue('institution: "{institution}"'),
    glue("year: {year}"),
    "---"
  )

  filename <- paste0("report-", file_id, ".qmd")
  file_path <- here("publications", "publications-reports", filename)
  file.create(file_path)
  writeLines(output, file_path)
}

msg <-
  list.files(here("publications", "publications-reports"), full.names = TRUE) |>
  file.remove()

for (i in 1:nrow(reports)) {
  meta <- as.list(reports[i,])
  do.call(create_report, meta)
}
