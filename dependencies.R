install.packages(
  c(
    "readr",
    "knitr",
    "rmarkdown",
    "stringr",
    "gt",
    "tibble"
  ),
  repos = Sys.getenv("RSPM", unset = "https://cloud.r-project.org")
)
