# filtering.py
import re


def is_list_item(line: str) -> bool:
    """Checks if a line looks like a markdown list item."""
    stripped_line = line.lstrip()
    if stripped_line.startswith(("- ", "* ", "+ ")):
        return True
    if stripped_line.find(". ") > 0:
        potential_number = stripped_line[:stripped_line.find(". ")]
        if potential_number.isdigit():
            return True
    return False


def convert_indented_code_blocks(content: str) -> str:
    """
    Converts indented code blocks in markdown content to fenced (backtick) code blocks.
    """
    lines = content.splitlines()
    new_lines = []
    in_indented_code_block = False
    in_fenced_code_block = False  # To track existing ``` blocks
    indent_prefix = "    "
    output_language_tag = "php"  # 또는 비워두려면 ""
    num_lines = len(lines)

    for i, line in enumerate(lines):
        # 1. Handle existing fenced code blocks first
        if line.strip().startswith("```"):
            if not in_fenced_code_block:
                if in_indented_code_block:  # Close pending indented block
                    new_lines.append("```")
                    in_indented_code_block = False
                in_fenced_code_block = True
            else:
                in_fenced_code_block = False
            new_lines.append(line)
            continue

        if in_fenced_code_block:
            new_lines.append(line)
            continue

        # 2. Process lines for potential indented code blocks
        is_currently_indented_line = line.startswith(indent_prefix)
        current_line_is_just_whitespace = not line.strip()

        if not in_indented_code_block:
            if is_currently_indented_line and not is_list_item(line):
                prev_line_justifies_code_block = (i == 0) or \
                                                 (not lines[i - 1].strip()) or \
                                                 (not lines[i - 1].startswith(indent_prefix) and not is_list_item(
                                                     lines[i - 1]))
                if prev_line_justifies_code_block:
                    in_indented_code_block = True
                    tag_to_add = f"```{output_language_tag}" if output_language_tag else "```"
                    new_lines.append(tag_to_add)
                    new_lines.append(line[len(indent_prefix):])
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:  # We are IN an indented_code_block
            if is_currently_indented_line:
                new_lines.append(line[len(indent_prefix):])
            elif current_line_is_just_whitespace:
                is_next_line_indented_code = False
                if i + 1 < num_lines:
                    next_line = lines[i + 1]
                    if next_line.startswith(indent_prefix) and not is_list_item(next_line):
                        is_next_line_indented_code = True

                if is_next_line_indented_code:
                    new_lines.append("")
                else:
                    new_lines.append("```")
                    in_indented_code_block = False
                    new_lines.append(line)
            else:
                new_lines.append("```")
                in_indented_code_block = False
                new_lines.append(line)

    if in_indented_code_block:
        new_lines.append("```")

    return "\n".join(new_lines)


def remove_style_tags(content: str) -> str:
    """
    Removes <style>...</style> tags and their content from the markdown.
    """
    pattern = r"<style.*?>.*?</style>"
    return re.sub(pattern, "", content, flags=re.DOTALL | re.IGNORECASE)


def normalize_excessive_blank_lines(content: str) -> str:
    """
    Replaces three or more consecutive newlines (which form two or more blank lines)
    with exactly two newlines (forming a single blank line).
    This preserves single blank lines and content lines.
    """
    if not content.strip():  # If content is all whitespace or empty
        return ""

    # 3개 이상의 연속된 개행을 정확히 2개의 개행으로 변경
    # \n\n\n (두 개의 빈 줄) -> \n\n (하나의 빈 줄)
    # \n\n\n\n (세 개의 빈 줄) -> \n\n (하나의 빈 줄) 등
    # \s*는 중간에 공백만 있는 줄도 빈 줄로 취급하기 위함.
    return re.sub(r"(\n\s*){3,}", "\n\n", content)


def filter_markdown(content: str) -> str:
    """
    Applies a series of filtering functions to the markdown content.
    """
    # 단계 1: 들여쓰기 코드 블록을 백틱 코드 블록으로 변환
    content = convert_indented_code_blocks(content)

    # 단계 2: <style> 태그 제거
    content = remove_style_tags(content)

    # 단계 3: 3줄 이상의 빈 줄을 2줄(하나의 빈 줄)로 통합
    content = normalize_excessive_blank_lines(content)

    return content
