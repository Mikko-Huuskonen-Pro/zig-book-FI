#!/usr/bin/env Rscript
# Tarkista build-ympäristön perusasiat ennen quarto render -ajoa.

args <- commandArgs(trailingOnly = TRUE)
repo_root <- if (length(args) > 0) normalizePath(args[[1]]) else normalizePath(".")

stopifnot(file.exists(file.path(repo_root, "zig_engine.R")))
stopifnot(file.exists(file.path(repo_root, "fi", "_quarto.yml")))

cat("Repository root:", repo_root, "\n")

setwd(file.path(repo_root, "fi", "Chapters"))
source(file.path(repo_root, "zig_engine.R"))

shop_list <- normalizePath(
  file.path(find_repo_root(), "ZigExamples", "file-io", "shop-list.txt"),
  mustWork = TRUE
)
foo_txt_dir <- file.path(find_repo_root(), "ZigExamples", "file-io")
if (!dir.exists(foo_txt_dir)) {
  stop("Missing ZigExamples/file-io directory")
}
cat("shop-list.txt:", shop_list, "\n")

chapter_code <- 'const path = "../ZigExamples/file-io/shop-list.txt";'
root_code <- 'const path = "ZigExamples/file-io/foo.txt";'

if (get_zig_workdir(chapter_code) != file.path(find_repo_root(), "Chapters")) {
  stop("get_zig_workdir() should use Chapters/ for ../ZigExamples paths")
}
if (get_zig_workdir(root_code) != find_repo_root()) {
  stop("get_zig_workdir() should use repo root for ZigExamples/ paths")
}
cat("Zig working-directory logic: OK\n")

setwd(file.path(repo_root, "fi"))
source(file.path(repo_root, "Scripts", "zig-quarto-versions.R"))
cat("zig-quarto-versions.R from fi/: OK\n")

zig_cmd <- Sys.which("zig")
if (nzchar(zig_cmd)) {
  zig_code <- paste(
    "const std = @import(\"std\");",
    "",
    "fn read_file(path: []const u8, buffer: []u8, io: std.Io) !usize {",
    "    const file = try std.Io.Dir.cwd().openFile(io, path, .{});",
    "    defer file.close(io);",
    "    return try file.readPositionalAll(io, buffer[0..], 0);",
    "}",
    "",
    "pub fn main(init: std.process.Init) !void {",
    "    var gpa = std.heap.DebugAllocator(.{}){};",
    "    defer _ = gpa.deinit();",
    "    const allocator = gpa.allocator();",
    "    var file_buffer = try allocator.alloc(u8, 1024);",
    "    defer allocator.free(file_buffer);",
    "    @memset(file_buffer[0..], 0);",
    "    const path = \"../ZigExamples/file-io/shop-list.txt\";",
    "    const nbytes = try read_file(path, file_buffer[0..], init.io);",
    "    std.debug.print(\"{s}\", .{file_buffer[0..nbytes]});",
    "}",
    sep = "\n"
  )

  output <- with_zig_workdir(zig_code, {
    file_path <- tempfile(fileext = ".zig")
    writeLines(zig_code, file_path)
    on.exit(unlink(file_path), add = TRUE)
    zig_compile_file(file_path, "run")
  })
  cat("Sample Zig execution from fi/Chapters cwd: OK\n")
  cat(paste(tail(output, 2), collapse = "\n"), "\n")
} else {
  cat("Zig not installed locally; skipped live Zig execution test.\n")
}

cat("All build prerequisite checks passed.\n")
