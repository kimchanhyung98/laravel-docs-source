#!/usr/bin/env python3
"""
마크다운 필터링 관련 유틸리티 함수 모듈
"""
import re


def is_list_item(line: str) -> bool:
    """마크다운 줄이 리스트 항목인지 확인

    Args:
        line: 확인할 마크다운 줄 문자열

    Returns:
        줄이 리스트 항목이면 True, 그렇지 않으면 False
    """
    stripped_line = line.lstrip()
    if stripped_line.startswith(("- ", "* ", "+ ")):
        return True
    if stripped_line.find(". ") > 0:  # 예: "1. ", "10. "
        potential_number = stripped_line[:stripped_line.find(". ")]
        if potential_number.isdigit():
            return True
    return False


def convert_indented_code_blocks(content: str) -> str:
    """마크다운 내용에서 들여쓰기 코드 블록을 펜스(백틱) 코드 블록으로 변환

    언어 태그 없이 단순 백틱(```)만을 사용

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        들여쓰기 코드 블록이 언어 태그 없는 펜스 코드 블록으로 변환된 마크다운 문자열
    """
    lines = content.splitlines()
    new_lines = []
    in_indented_code_block = False
    in_fenced_code_block = False
    indent_prefix = "    "
    num_lines = len(lines)

    for i, line in enumerate(lines):
        # 기존 펜스 코드 블록 처리
        if line.strip().startswith("```"):
            if not in_fenced_code_block:
                if in_indented_code_block:
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

        # 들여쓰기 코드 블록 처리
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
                    new_lines.append("```")  # 언어 태그 없이 바로 ``` 추가
                    new_lines.append(line[len(indent_prefix):])
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:  # 들여쓰기 코드 블록 내부
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
    """마크다운 내용에서 <style> 태그와 그 내부 내용을 모두 제거

    제거 시 추가적인 개행 문자나 빈 줄을 남기지 않고, 태그와 내용만 완전히 삭제

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        <style> 태그와 그 내용이 완전히 제거된 마크다운 문자열
    """
    pattern = r"<style.*?>.*?</style>"
    return re.sub(pattern, "", content, flags=re.DOTALL | re.IGNORECASE)


def ensure_ends_with_blank_line(content: str) -> str:
    """파일 끝이 하나의 빈 줄로 끝나도록 표준화

    - 파일에 내용이 있다면, 마지막 내용 줄 뒤에 두 개의 개행 문자(\\n\\n)를 두어
      하나의 빈 줄이 보이도록 함
    - 파일 끝의 여러 빈 줄이나 공백은 이 규칙에 맞게 조정
    - 파일이 완전히 비어있거나 공백으로만 이루어져 있다면 빈 문자열을 반환

    Args:
        content: 처리할 마크다운 원본 문자열

    Returns:
        파일 끝이 하나의 빈 줄로 표준화된 마크다운 문자열
    """
    if not content.strip():  # 내용이 전혀 없거나 공백만 있다면 빈 문자열 반환
        return ""

    # 문자열 끝의 모든 종류의 공백 문자(개행 포함) 제거
    processed_content = content.rstrip()

    # 내용이 있다면, 파일 끝에 두 개의 개행 문자 추가 (하나의 빈 줄 생성)
    if processed_content:  # 이 조건은 rstrip() 후에도 내용이 남아있는지 확인
        processed_content += "\n\n"
    else:  # rstrip() 후 내용이 모두 사라졌다면 (원래 공백만 있던 문자열)
        return ""

    return processed_content


def filter_markdown(content: str) -> str:
    """마크다운 내용에 여러 필터링 함수를 순차적으로 적용

    적용되는 필터:
    1. 들여쓰기 코드 블록을 펜스(백틱) 코드 블록으로 변환 (언어 태그 없음)
    2. HTML <style> 태그와 그 내용을 완전히 제거
    3. 파일 끝을 하나의 빈 줄로 표준화 (문서 중간의 빈 줄은 유지)

    Args:
        content: 필터링할 원본 마크다운 문자열

    Returns:
        모든 필터링이 적용된 마크다운 문자열
    """
    content = convert_indented_code_blocks(content)
    content = remove_style_tags(content)
    content = ensure_ends_with_blank_line(content)
    return content
