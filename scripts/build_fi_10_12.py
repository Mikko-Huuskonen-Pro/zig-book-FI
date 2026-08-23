#!/usr/bin/env python3
"""Build fi/Chapters/10-stack-project.qmd and 12-file-op.qmd from English source."""

import re
from pathlib import Path

CHAPTERS = {
    "Chapters/10-stack-project.qmd": {
        "out": Path("/workspace/fi/Chapters/10-stack-project.qmd"),
        "sha": "6ede476ddca6c23022a31edbd0e5cc7ae84a272bcdb16c3ca4a4a83bb96dbca5",
        "trans_module": "fi_10_translations_data",
    },
    "Chapters/12-file-op.qmd": {
        "out": Path("/workspace/fi/Chapters/12-file-op.qmd"),
        "sha": "eb56808d8146d276362c398d12969d98551463520b60c00b730ebcc26a61fe2e",
        "trans_module": "fi_12_translations_data",
    },
}

HEADER_TMPL = """---
translation:
  source: {source}
  source_sha256: {sha}
  status: complete
---

engine: knitr
knitr: true
syntax-definition: "../../Assets/zig.xml"
---

"""

KNITR = """```{r}
#| include: false
source("../../zig_engine.R")
knitr::opts_chunk$set(
    auto_main = FALSE,
    build_type = "lib"
)
```
"""


def split_prose_blocks(text: str) -> list[str]:
    text = re.sub(r"^---[\s\S]*?---\s*", "", text, count=1)
    text = re.sub(r"```\{r\}[\s\S]*?```\s*", "", text, count=1)
    blocks: list[str] = []
    pattern = re.compile(r"(```[\s\S]*?```)", re.MULTILINE)
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            b = text[last : m.start()]
            if b.strip():
                blocks.append(b)
        last = m.end()
    if last < len(text):
        b = text[last:]
        if b.strip():
            blocks.append(b)
    return blocks


def build_chapter(source_rel: str, meta: dict) -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        meta["trans_module"],
        Path(__file__).parent / f"{meta['trans_module']}.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    translations: dict[int, str] = mod.TRANSLATIONS

    src_path = Path("/workspace") / source_rel
    src = src_path.read_text()

    parts: list[str] = []
    pattern = re.compile(r"(```[\s\S]*?```)", re.MULTILINE)
    body = re.sub(r"^---[\s\S]*?---\s*", "", src, count=1)
    body = re.sub(r"```\{r\}[\s\S]*?```\s*", "", body, count=1)

    prose_blocks = split_prose_blocks(src)
    prose_idx = 0
    last = 0
    for m in pattern.finditer(body):
        if m.start() > last:
            prose = body[last : m.start()]
            if prose.strip():
                if prose_idx in translations:
                    leading = prose[: len(prose) - len(prose.lstrip())]
                    trailing = prose[len(prose.rstrip()) :]
                    parts.append(leading + translations[prose_idx].strip() + trailing)
                else:
                    parts.append(prose)
                    print(f"WARNING: missing translation block {prose_idx} in {source_rel}")
                prose_idx += 1
            else:
                parts.append(prose)
        parts.append(m.group(1))
        last = m.end()
    if last < len(body):
        prose = body[last:]
        if prose.strip():
            if prose_idx in translations:
                leading = prose[: len(prose) - len(prose.lstrip())]
                trailing = prose[len(prose.rstrip()) :]
                parts.append(leading + translations[prose_idx].strip() + trailing)
            else:
                parts.append(prose)
                print(f"WARNING: missing translation block {prose_idx} in {source_rel}")
            prose_idx += 1
        else:
            parts.append(prose)

    out = meta["out"]
    out.write_text(
        HEADER_TMPL.format(source=source_rel, sha=meta["sha"])
        + "\n"
        + KNITR
        + "\n\n"
        + "".join(parts).lstrip("\n")
    )
    lines = out.read_text().count("\n") + 1
    print(f"Wrote {out} ({lines} lines, {prose_idx} prose blocks)")


def main() -> None:
    for source_rel, meta in CHAPTERS.items():
        build_chapter(source_rel, meta)


if __name__ == "__main__":
    main()
