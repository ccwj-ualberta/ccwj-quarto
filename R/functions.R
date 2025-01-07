create_values_box <- function(value, icon, text) {
  tags$div(
    class = "col-lg-4 px-0",
    tags$div(
      class = "value-block value-feature",
      h3(class = "value-text",
         tags$i(class = icon), value),
      p(text)
    )
  )
}
