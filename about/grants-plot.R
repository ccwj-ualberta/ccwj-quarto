library(here)
library(glue)
library(echarts4r)

research_grants <- read.csv(here("about/CCWJ-research-grants.csv"))

# Data preprocessing
# Convert date columns to Date format
research_grants$Start <- as.Date(research_grants$Start)
research_grants$End <- as.Date(research_grants$End)
research_grants$Start_Year <- as.numeric(format(research_grants$Start, "%Y"))

# Create summary by year
yearly_summary <- aggregate(
  research_grants[c("Total")],
  by = list(Year = research_grants$Start_Year),
  FUN = function(x) c(total_funding = sum(x), count = length(x))
)

yearly_data <- data.frame(
  Year = yearly_summary$Year,
  Total_Funding = yearly_summary$Total[, 1],
  Grant_Count = yearly_summary$Total[, 2]
)

yearly_data$Cumulative_Funding <- cumsum(yearly_data$Total_Funding)

# Create the echarts4r plot
year_start <- min(yearly_data$Year)
year_end <- max(yearly_data$Year)
total_funding_million <- round(max(yearly_data$Cumulative_Funding) / 1000000, 1)
fill_color <- "#2eab8cff"

p_grants <- yearly_data |>
  e_charts(Year) |>
  e_area(
    Cumulative_Funding,
    name = "Cumulative Funding",
    itemStyle = list(color = fill_color),
    lineStyle = list(width = 2, color = fill_color),
    symbol = "circle",
    symbolSize = 20,
    showSymbol = TRUE,
    label = list(
      show = TRUE,
      position = "top",
      fontSize = 14,
      fontWeight = "bold",
      color = fill_color
    )
  ) |>
  e_x_axis(
    name = "Year",
    splitLine = list(
      show = TRUE,
      lineStyle = list(type = "dashed", color = "lightgray")
    ),
    min = year_start,
    max = year_end,
    axisLabel = list(
      formatter = htmlwidgets::JS("function(value) {return value.toString();}")
    )
  ) |>
  e_labels(
    formatter = htmlwidgets::JS("function(d) {return '$' + (d.value[1]/1000000).toFixed(1) + 'M';}"),
    textStyle = list(color = fill_color, fontWeight = "bold", fontSize = 11),
    offset = c(0, -7)
  ) |>
  e_y_axis(show = FALSE) |>
  e_title(
    text = "Cumulative Research Grant Funding",
    subtext = glue("Total funding has reached ${total_funding_million}M with accelerated growth since {year_start}."),
    textStyle = list(fontSize = 18, fontWeight = "bold"),
    subtextStyle = list(fontSize = 14)
  ) |> 
  e_legend(show = FALSE)
