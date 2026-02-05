"""MarkdownFilterService - 마크다운 필터링 도메인 서비스"""

import re


class MarkdownFilterService:
    """마크다운 콘텐츠 필터링 및 정규화를 담당하는 도메인 서비스"""

    @staticmethod
    def _is_list_item(line: str) -> bool:
        """마크다운 줄이 리스트 항목인지 확인"""
        stripped_line = line.lstrip()
        if stripped_line.startswith(("- ", "* ", "+ ")):
            return True
        if stripped_line.find(". ") > 0:
            potential_number = stripped_line[:stripped_line.find(". ")]
            if potential_number.isdigit():
                return True
        return False

    @staticmethod
    def convert_indented_code_blocks(content: str) -> str:
        """들여쓰기 코드 블록을 펜스(백틱) 코드 블록으로 변환"""
        lines = content.splitlines()
        new_lines = []
        in_indented_code_block = False
        in_fenced_code_block = False
        indent_prefix = "    "
        num_lines = len(lines)

        for i, line in enumerate(lines):
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

            is_currently_indented_line = line.startswith(indent_prefix)
            current_line_is_just_whitespace = not line.strip()

            if not in_indented_code_block:
                if is_currently_indented_line and not MarkdownFilterService._is_list_item(line):
                    prev_line_justifies_code_block = (i == 0) or \
                                                     (not lines[i - 1].strip()) or \
                                                     (not lines[i - 1].startswith(indent_prefix) and not MarkdownFilterService._is_list_item(
                                                         lines[i - 1]))
                    if prev_line_justifies_code_block:
                        in_indented_code_block = True
                        new_lines.append("```")
                        new_lines.append(line[len(indent_prefix):])
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                if is_currently_indented_line:
                    new_lines.append(line[len(indent_prefix):])
                elif current_line_is_just_whitespace:
                    is_next_line_indented_code = False
                    if i + 1 < num_lines:
                        next_line = lines[i + 1]
                        if next_line.startswith(indent_prefix) and not MarkdownFilterService._is_list_item(next_line):
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

    @staticmethod
    def remove_style_tags(content: str) -> str:
        """<style> 태그와 내용 제거"""
        pattern = r"<style.*?>.*?</style>"
        return re.sub(pattern, "", content, flags=re.DOTALL | re.IGNORECASE)

    @staticmethod
    def ensure_ends_with_blank_line(content: str) -> str:
        """파일 끝이 하나의 빈 줄로 끝나도록 표준화"""
        if not content.strip():
            return ""
        processed_content = content.rstrip()
        if processed_content:
            processed_content += "\n\n"
        else:
            return ""
        return processed_content

    @staticmethod
    def fix_unclosed_img_tags(content: str) -> str:
        """닫히지 않은 이미지 태그를 자동으로 닫는 태그로 변환"""
        pattern = r'<img([^>]*?)(?<!/)>'
        replacement = r'<img\1 />'
        return re.sub(pattern, replacement, content)

    @staticmethod
    def replace_version_placeholder(content: str, version: str) -> str:
        """{{version}} 플레이스홀더를 지정된 버전으로 치환"""
        pattern = r'\{\{\s*version\s*\}\}'
        return re.sub(pattern, version, content)

    @staticmethod
    def remove_title_braces(content: str) -> str:
        """마크다운 제목 옆에 있는 중괄호와 그 내용을 제거"""
        pattern = r'^(#+\s+.+?)\s+\{[^}]*\}\s*$'
        lines = content.splitlines()
        result_lines = []

        for line in lines:
            match = re.match(pattern, line)
            if match:
                result_lines.append(match.group(1))
            else:
                result_lines.append(line)

        return "\n".join(result_lines)

    @staticmethod
    def standardize_callouts(content: str) -> str:
        """다양한 마크다운 콜아웃 형식을 통일"""
        pattern1 = r'^(\s*)>\s*\{(tip|note)\}\s*(.+)$'
        pattern2 = r'^(\s*)>\s*\[!(NOTE|WARNING|TIP)\]\s+([^\s].+)$'
        pattern3 = r'^(\s*)>\s*\*\*(note|warning|tip)\*\*\s*(.*)$'

        lines = content.splitlines()
        result_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]

            match1 = re.match(pattern1, line)
            if match1:
                indent, callout_type, message = match1.groups()
                callout_type = callout_type.upper()
                result_lines.append(f"{indent}> [!{callout_type}]")
                result_lines.append(f"{indent}> {message}")
                i += 1
                continue

            match2 = re.match(pattern2, line)
            if match2:
                indent, callout_type, message = match2.groups()
                result_lines.append(f"{indent}> [!{callout_type}]")
                result_lines.append(f"{indent}> {message}")
                i += 1
                continue

            match3 = re.match(pattern3, line, re.IGNORECASE)
            if match3:
                indent, callout_type, message = match3.groups()
                callout_type = callout_type.upper()
                result_lines.append(f"{indent}> [!{callout_type}]")
                if message:
                    result_lines.append(f"{indent}> {message}")
                i += 1
                continue

            result_lines.append(line)
            i += 1

        return "\n".join(result_lines)

    def filter(self, content: str, version: str | None = None) -> str:
        """마크다운 콘텐츠에 모든 필터를 적용"""
        content = self.convert_indented_code_blocks(content)
        content = self.remove_style_tags(content)
        content = self.fix_unclosed_img_tags(content)
        content = self.remove_title_braces(content)
        content = self.standardize_callouts(content)

        if version is not None:
            content = self.replace_version_placeholder(content, version)

        content = self.ensure_ends_with_blank_line(content)
        return content
