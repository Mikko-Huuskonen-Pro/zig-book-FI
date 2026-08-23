library(stringr)

find_zig_engine <- function() {
  candidates <- c(
    file.path(getwd(), "zig_engine.R"),
    file.path(getwd(), "..", "zig_engine.R")
  )

  if (requireNamespace("knitr", quietly = TRUE)) {
    input_dir <- tryCatch(knitr::current_input(dir = TRUE), error = function(e) NULL)
    if (!is.null(input_dir) && nzchar(input_dir)) {
      candidates <- c(
        file.path(input_dir, "zig_engine.R"),
        file.path(input_dir, "..", "zig_engine.R"),
        candidates
      )
    }
  }

  for (path in unique(candidates)) {
    if (file.exists(path)) {
      return(normalizePath(path))
    }
  }

  stop("zig_engine.R not found")
}

source(find_zig_engine())


find_quarto_ <- function() {
  p <- Sys.which("quarto")
  return(p)
}

zig_cmd_path <- find_zig_()
quarto_cmd_path <- find_quarto_()
zig_version <- system2(
  zig_cmd_path,
  "version",
  stdout = TRUE
)

quarto_version <- system2(
  quarto_cmd_path,
  "-v",
  stdout = TRUE
)

regex <- "[0-9]{2}[.][0-9]{2}[.][0-9]{1}-[a-zA-Z]*"
sys_info <- Sys.info()
sys_version <- str_extract(sys_info["version"], regex)
bullets <- c(
  "- System version: %s, %s, %s, %s.",
  "- Zig version: %s.",
  "- Quarto version: %s."
)
bullets <- paste(bullets, sep = "", collapse = "\n")
versions_string <- sprintf(
  bullets,
  sys_info["sysname"],
  sys_info["release"],
  sys_version,
  sys_info["machine"],
  zig_version,
  quarto_version
)




cat(versions_string)
