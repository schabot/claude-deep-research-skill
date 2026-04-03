#!/usr/bin/env python3
"""Convert a research markdown report to styled HTML using the report template."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class SectionInfo:
    title: str
    anchor: str


@dataclass
class ParsedReport:
    metadata: dict
    body: str


def parse_report(markdown_text: str) -> ParsedReport:
    """Parse optional YAML-style frontmatter from the markdown report."""
    if not markdown_text.startswith("---\n"):
        return ParsedReport(metadata={}, body=markdown_text)

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", markdown_text, re.DOTALL)
    if not match:
        return ParsedReport(metadata={}, body=markdown_text)

    metadata_block, body = match.groups()
    metadata = {}
    for line in metadata_block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return ParsedReport(metadata=metadata, body=body)


def slugify(value: str) -> str:
    """Create stable anchor IDs from section titles."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def extract_title(markdown_text: str, metadata: dict) -> str:
    """Extract the title from metadata or the first H1."""
    if metadata.get("title"):
        return metadata["title"]

    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Research Report"


def extract_subtitle(markdown_text: str) -> str:
    """Extract a subtitle from the first non-heading paragraph after H1."""
    lines = markdown_text.splitlines()
    found_h1 = False
    buffer: List[str] = []

    for line in lines:
        stripped = line.strip()
        if not found_h1:
            if stripped.startswith("# "):
                found_h1 = True
            continue

        if not stripped:
            if buffer:
                break
            continue

        if stripped.startswith("#"):
            if buffer:
                break
            continue

        if stripped == "---":
            continue

        buffer.append(stripped)
        if len(" ".join(buffer)) > 220:
            break

    subtitle = " ".join(buffer).strip()
    return subtitle or "Deep research report"


def extract_date(metadata: dict) -> str:
    """Extract report date from metadata when present."""
    return metadata.get("date", "Undated")


def extract_mode_label(metadata: dict) -> str:
    """Extract mode label from metadata when present."""
    mode = metadata.get("mode")
    if mode:
        return f"{mode} Research Mode"
    return "Deep Research Report"


def extract_header_tag(metadata: dict) -> str:
    """Extract header tag from metadata when present."""
    classification = metadata.get("classification")
    if classification:
        return classification
    return "Deep Research Report"


def split_bibliography(markdown_text: str) -> Tuple[str, str]:
    """Split the markdown body into content and bibliography section body."""
    match = re.search(r"^## Bibliography\s*$", markdown_text, re.MULTILINE)
    if not match:
        return markdown_text, ""

    content = markdown_text[:match.start()].rstrip()
    bibliography = markdown_text[match.end():].lstrip("\n")
    return content, bibliography


def extract_bibliography_and_tail(markdown_text: str) -> Tuple[str, str, str]:
    """Split markdown into content, bibliography, and post-bibliography content."""
    content, bibliography_plus_tail = split_bibliography(markdown_text)
    if not bibliography_plus_tail:
        return content, "", ""

    next_section = re.search(r"^## (?!Bibliography\b)(.+)$", bibliography_plus_tail, re.MULTILINE)
    if not next_section:
        return content, bibliography_plus_tail.strip(), ""

    bibliography = bibliography_plus_tail[:next_section.start()].strip()
    tail = bibliography_plus_tail[next_section.start():].strip()
    return content, bibliography, tail


def extract_sections(markdown_text: str) -> List[SectionInfo]:
    """Extract top-level H2 sections for nav/sidebar generation."""
    sections = []
    for title in re.findall(r"^## (.+)$", markdown_text, re.MULTILINE):
        if title.strip().lower() == "bibliography":
            continue
        sections.append(SectionInfo(title=title.strip(), anchor=slugify(title)))
    return sections


def extract_metrics(markdown_text: str, max_metrics: int = 4) -> List[Tuple[str, str]]:
    """Extract a small set of metrics from the markdown body."""
    candidates = []
    metric_pattern = re.compile(
        r"(\$[\d–\-\.]+[TMBK]?|[\d]+(?:\.[\d]+)?%|[\d]+\s?(?:million|billion|trillion)|1 in \d+|[\d]+x)",
        re.IGNORECASE,
    )

    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "---":
            continue
        match = metric_pattern.search(stripped)
        if not match:
            continue
        number = match.group(1)
        label = stripped.replace(number, "").strip(" .:-")
        if not label:
            continue
        candidates.append((number, label[:80]))
        if len(candidates) >= max_metrics:
            break

    return candidates


def render_metrics_dashboard(metrics: List[Tuple[str, str]]) -> str:
    """Render the metrics dashboard."""
    if not metrics:
        return ""

    blocks = []
    for number, label in metrics:
        blocks.append(
            '<div class="metric">'
            f'<span class="metric-number">{html.escape(number)}</span>'
            f'<span class="metric-label">{html.escape(label)}</span>'
            '</div>'
        )
    return f'<div class="metrics-dashboard">{"".join(blocks)}</div>'


def render_nav_links(sections: List[SectionInfo]) -> str:
    """Render top navigation links."""
    return "".join(
        f'<a href="#{section.anchor}">{html.escape(shorten_nav_label(section.title))}</a>'
        for section in sections
    )


def shorten_nav_label(title: str) -> str:
    """Shorten verbose section names for the top nav."""
    cleaned = re.sub(r"^Section \d+:\s*", "", title).strip()
    return cleaned if len(cleaned) <= 28 else cleaned[:25].rstrip() + "..."


def render_sidebar_links(sections: List[SectionInfo]) -> str:
    """Render the sidebar table of contents."""
    items = "".join(
        f'<li><a href="#{section.anchor}">{html.escape(section.title)}</a></li>'
        for section in sections
    )
    return f"<ul>{items}</ul>"


def replace_inline_formatting(text: str) -> str:
    """Convert a limited markdown subset inside paragraphs."""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\[(\d+)\]", r'<span class="citation">[\1]</span>', escaped)
    return escaped


def convert_bibliography(markdown: str) -> str:
    """Convert bibliography lines to HTML."""
    if not markdown.strip():
        return ""

    entries = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "---":
            continue

        match = re.match(r"^\[(\d+)\]\s+(.+?)(https?://[^\s\)]+)\s*$", stripped)
        if not match:
            entries.append(f'<p>{replace_inline_formatting(stripped)}</p>')
            continue

        num, text, url = match.groups()
        text = replace_inline_formatting(text.strip())
        entries.append(
            f'<div class="bib-entry"><span class="bib-number">[{num}]</span> '
            f'{text} <a href="{html.escape(url)}" target="_blank">{html.escape(url)}</a></div>'
        )
    return f'<div class="bibliography-content">\n' + "\n".join(entries) + "\n</div>"


def convert_content(markdown: str) -> str:
    """Convert report content markdown to styled HTML."""
    lines = markdown.splitlines()
    result: List[str] = []
    paragraph_lines: List[str] = []
    list_stack: List[str] = []
    section_open = False
    callout_open = False

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if not paragraph_lines:
            return
        text = " ".join(part.strip() for part in paragraph_lines if part.strip())
        if text:
            result.append(f"<p>{replace_inline_formatting(text)}</p>")
        paragraph_lines = []

    def close_lists() -> None:
        nonlocal list_stack
        while list_stack:
            result.append(f"</{list_stack.pop()}>")

    def close_callout() -> None:
        nonlocal callout_open
        if callout_open:
            flush_paragraph()
            result.append("</div>")
            callout_open = False

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_lists()
            close_callout()
            continue

        if stripped == "---":
            flush_paragraph()
            close_lists()
            close_callout()
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            close_lists()
            close_callout()
            result.append("<pre><code>")
            continue

        if result and result[-1] == "<pre><code>":
            if stripped.startswith("```"):
                result.append("</code></pre>")
            else:
                result.append(html.escape(line))
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            close_lists()
            close_callout()
            if section_open:
                result.append("</section>")
            title = stripped[3:].strip()
            anchor = slugify(title)
            result.append(
                f'<section class="section" id="{anchor}">'
                f'<div class="section-kicker">Section</div>'
                f'<h2 class="section-title">{html.escape(title)}</h2>'
            )
            section_open = True
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            close_lists()
            close_callout()
            result.append(f'<h3 class="subsection-title">{html.escape(stripped[4:].strip())}</h3>')
            continue

        if stripped.startswith("#### "):
            flush_paragraph()
            close_lists()
            close_callout()
            result.append(f'<h4 class="subsubsection-title">{html.escape(stripped[5:].strip())}</h4>')
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            flush_paragraph()
            if not list_stack or list_stack[-1] != "ul":
                close_lists()
                list_stack.append("ul")
                result.append("<ul>")
            result.append(f"<li>{replace_inline_formatting(stripped[2:].strip())}</li>")
            continue

        if re.match(r"^\d+\.\s", stripped):
            flush_paragraph()
            if not list_stack or list_stack[-1] != "ol":
                close_lists()
                list_stack.append("ol")
                result.append("<ol>")
            content = re.sub(r"^\d+\.\s", "", stripped)
            result.append(f"<li>{replace_inline_formatting(content.strip())}</li>")
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            close_lists()
            close_callout()
            result.append(f"__TABLE_ROW__{line}")
            continue

        if stripped.startswith("**") and stripped.endswith(":**"):
            flush_paragraph()
            close_lists()
            close_callout()
            label = stripped[:-3].strip("*")
            result.append(f'<div class="callout"><span class="callout-label">{html.escape(label)}</span>')
            callout_open = True
            continue

        paragraph_lines.append(stripped)

    flush_paragraph()
    close_lists()
    close_callout()
    if section_open:
        result.append("</section>")

    html_lines = convert_tables(result)
    html_output = "\n".join(html_lines)
    html_output = html_output.replace(
        '<section class="section" id="executive-summary"><div class="section-kicker">Section</div><h2 class="section-title">Executive Summary</h2>',
        '<section class="section executive-summary" id="executive-summary"><div class="section-kicker">Section</div><h2 class="section-title">Executive Summary</h2>',
    )

    return html_output


def convert_tables(lines: List[str]) -> List[str]:
    """Convert placeholder-marked markdown tables into HTML tables."""
    converted: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("__TABLE_ROW__"):
            converted.append(line)
            i += 1
            continue

        raw_rows = []
        while i < len(lines) and lines[i].startswith("__TABLE_ROW__"):
            raw_rows.append(lines[i].replace("__TABLE_ROW__", "", 1))
            i += 1

        if len(raw_rows) < 2:
            converted.extend(raw_rows)
            continue

        header_cells = [replace_inline_formatting(cell.strip()) for cell in raw_rows[0].split("|")[1:-1]]
        body_rows = raw_rows[2:] if "---" in raw_rows[1] else raw_rows[1:]

        converted.append("<table>")
        converted.append("<thead><tr>")
        converted.extend(f"<th>{cell}</th>" for cell in header_cells)
        converted.append("</tr></thead>")
        converted.append("<tbody>")
        for row in body_rows:
            cells = [replace_inline_formatting(cell.strip()) for cell in row.split("|")[1:-1]]
            converted.append("<tr>")
            converted.extend(f"<td>{cell}</td>" for cell in cells)
            converted.append("</tr>")
        converted.append("</tbody></table>")

    return converted


def build_html_document(markdown_text: str, template_text: str) -> str:
    """Build the final HTML document from markdown and the template."""
    parsed = parse_report(markdown_text)
    title = extract_title(parsed.body, parsed.metadata)
    subtitle = extract_subtitle(parsed.body)
    date_value = extract_date(parsed.metadata)
    mode_label = extract_mode_label(parsed.metadata)
    header_tag = extract_header_tag(parsed.metadata)

    content_md, bibliography_md, tail_md = extract_bibliography_and_tail(parsed.body)
    if tail_md.strip():
        content_md = f"{content_md.rstrip()}\n\n{tail_md}\n"

    sections = extract_sections(content_md)
    metrics = extract_metrics(parsed.body)
    bibliography_html = convert_bibliography(bibliography_md)
    content_html = convert_content(content_md)

    source_count = len(re.findall(r"^\[\d+\]", bibliography_md, re.MULTILINE))
    replacements = {
        "{{TITLE}}": html.escape(title),
        "{{SUBTITLE}}": html.escape(subtitle),
        "{{DATE}}": html.escape(date_value),
        "{{MODE_LABEL}}": html.escape(mode_label),
        "{{HEADER_TAG}}": html.escape(header_tag),
        "{{SOURCE_COUNT}}": str(source_count),
        "{{SECTION_COUNT}}": str(len(sections)),
        "{{METRICS_DASHBOARD}}": render_metrics_dashboard(metrics),
        "{{NAV_LINKS}}": render_nav_links(sections),
        "{{SIDEBAR_LINKS}}": render_sidebar_links(sections),
        "{{CONTENT}}": content_html,
        "{{BIBLIOGRAPHY}}": bibliography_html,
    }

    html_document = template_text
    for placeholder, value in replacements.items():
        html_document = html_document.replace(placeholder, value)

    return html_document


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a markdown report to HTML",
        epilog="Example: python scripts/md_to_html.py report.md --output report.html",
    )
    parser.add_argument("markdown_file", type=Path, help="Path to markdown report")
    parser.add_argument("--output", "-o", type=Path, help="Output HTML path (default: input stem + .html)")
    args = parser.parse_args()

    if not args.markdown_file.exists():
        print(f"ERROR: File not found: {args.markdown_file}")
        return 1

    template_path = Path(__file__).resolve().parents[1] / "templates" / "mckinsey_report_template.html"
    if not template_path.exists():
        print(f"ERROR: Template not found: {template_path}")
        return 1

    output_path = args.output or args.markdown_file.with_suffix(".html")

    try:
        markdown_text = args.markdown_file.read_text(encoding="utf-8")
        template_text = template_path.read_text(encoding="utf-8")
        output_path.write_text(build_html_document(markdown_text, template_text), encoding="utf-8")
    except Exception as exc:
        print(f"ERROR: Failed to convert markdown: {exc}")
        return 1

    print(f"OK: wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
