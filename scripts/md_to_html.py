#!/usr/bin/env python3
"""Convert a research markdown report to HTML."""

import argparse
import re
from pathlib import Path
from typing import Tuple


def convert_markdown_to_html(markdown_text: str) -> Tuple[str, str]:
    """Convert markdown to HTML in two parts: content and bibliography."""
    parts = markdown_text.split('## Bibliography')
    content_md = parts[0]
    bibliography_md = parts[1] if len(parts) > 1 else ""
    return _convert_content_section(content_md), _convert_bibliography_section(bibliography_md)


def _convert_content_section(markdown: str) -> str:
    html = markdown

    lines = html.split('\n')
    processed_lines = []
    skip_until_first_section = True
    for line in lines:
        if skip_until_first_section:
            if line.startswith('## ') and not line.startswith('### '):
                skip_until_first_section = False
                processed_lines.append(line)
            continue
        processed_lines.append(line)
    html = '\n'.join(processed_lines)

    html = re.sub(r'^## (.+)$', r'<div class="section"><h2 class="section-title">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3 class="subsection-title">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4 class="subsubsection-title">\1</h4>', html, flags=re.MULTILINE)

    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    html = _convert_lists(html)
    html = _convert_tables(html)
    html = _convert_paragraphs(html)
    html = _close_sections(html)

    html = html.replace(
        '<h2 class="section-title">Executive Summary</h2>',
        '<div class="executive-summary"><h2 class="section-title">Executive Summary</h2>'
    )
    if '<div class="executive-summary">' in html:
        html = html.replace('</h2>\n<div class="section">', '</h2></div>\n<div class="section">', 1)

    return html


def _convert_bibliography_section(markdown: str) -> str:
    if not markdown.strip():
        return ""

    html = markdown
    html = re.sub(
        r'\[(\d+)\]\s*(.+?)\s*-\s*(https?://[^\s\)]+)',
        r'<div class="bib-entry"><span class="bib-number">[\1]</span> <a href="\3" target="_blank">\2</a></div>',
        html
    )
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    return f'<div class="bibliography-content">{html}</div>'


def _convert_lists(html: str) -> str:
    lines = html.split('\n')
    result = []
    in_list = False
    list_level = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result.append('<ul>')
                in_list = True
                list_level = len(line) - len(line.lstrip())
            result.append(f'<li>{stripped[2:]}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list:
                result.append('<ol>')
                in_list = True
                list_level = len(line) - len(line.lstrip())
            ordered_content = re.sub(r'^\d+\.\s', '', stripped)
            result.append(f'<li>{ordered_content}</li>')
        else:
            if in_list:
                current_level = len(line) - len(line.lstrip())
                if current_level > list_level and stripped:
                    if result[-1].endswith('</li>'):
                        result[-1] = result[-1][:-5] + ' ' + stripped + '</li>'
                    continue
                result.append('</ul>' if '<ul>' in '\n'.join(result[-10:]) else '</ol>')
                in_list = False
                list_level = 0
            result.append(line)

    if in_list:
        result.append('</ul>' if '<ul>' in '\n'.join(result[-10:]) else '</ol>')

    return '\n'.join(result)


def _convert_tables(html: str) -> str:
    lines = html.split('\n')
    result = []
    in_table = False

    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                result.append('<table>')
                in_table = True
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                result.append('<thead><tr>')
                result.extend([f'<th>{cell}</th>' for cell in cells])
                result.append('</tr></thead>')
                result.append('<tbody>')
            elif '---' in line:
                continue
            else:
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                result.append('<tr>')
                result.extend([f'<td>{cell}</td>' for cell in cells])
                result.append('</tr>')
        else:
            if in_table:
                result.append('</tbody></table>')
                in_table = False
            result.append(line)

    if in_table:
        result.append('</tbody></table>')

    return '\n'.join(result)


def _convert_paragraphs(html: str) -> str:
    lines = html.split('\n')
    result = []
    in_paragraph = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append(line)
            continue

        is_html_like = (
            (stripped.startswith('<') and stripped.endswith('>'))
            or stripped.startswith('</')
            or '<h' in stripped
            or '<div' in stripped
            or '<ul' in stripped
            or '<ol' in stripped
            or '<li' in stripped
            or '<table' in stripped
            or '</div>' in stripped
            or '</ul>' in stripped
            or '</ol>' in stripped
        )

        if is_html_like:
            if in_paragraph:
                result.append('</p>')
                in_paragraph = False
            result.append(line)
            continue

        if not in_paragraph:
            result.append('<p>' + line)
            in_paragraph = True
        else:
            result.append(line)

    if in_paragraph:
        result.append('</p>')

    return '\n'.join(result)


def _close_sections(html: str) -> str:
    lines = html.split('\n')
    result = []
    section_open = False

    for line in lines:
        if '<div class="section">' in line:
            if section_open:
                result.append('</div>')
            section_open = True
        result.append(line)

    if section_open:
        result.append('</div>')

    return '\n'.join(result)


def _extract_title(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return 'Research Report'


def _build_html_document(markdown_text: str) -> str:
    content_html, bib_html = convert_markdown_to_html(markdown_text)
    title = _extract_title(markdown_text)
    return f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>{title}</title>
</head>
<body>
  <main class=\"content\">\n{content_html}\n  </main>
  <section class=\"bibliography\">\n{bib_html}\n  </section>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Convert a markdown report to HTML',
        epilog='Example: python scripts/md_to_html.py report.md --output report.html'
    )
    parser.add_argument('markdown_file', type=Path, help='Path to markdown report')
    parser.add_argument('--output', '-o', type=Path, help='Output HTML path (default: input stem + .html)')
    args = parser.parse_args()

    if not args.markdown_file.exists():
        print(f'ERROR: File not found: {args.markdown_file}')
        return 1

    output_path = args.output or args.markdown_file.with_suffix('.html')
    try:
        markdown_text = args.markdown_file.read_text(encoding='utf-8')
        output_path.write_text(_build_html_document(markdown_text), encoding='utf-8')
    except Exception as exc:
        print(f'ERROR: Failed to convert markdown: {exc}')
        return 1

    print(f'OK: wrote {output_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
