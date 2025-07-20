#!/usr/bin/env python3
"""
대용량 마크다운 파일 분할 관련 유틸리티 함수 모듈
"""
import re
import time


def _is_header(line: str) -> bool:
    """마크다운 헤더인지 확인

    Args:
        line: 확인할 마크다운 줄 문자열

    Returns:
        주어진 줄이 헤더(H1-H4)이면 True, 아니면 False
    """
    return bool(re.match(r"^#{1,4}\s+", line.strip()))


def split_markdown_into_chunks(content: str, target_chunk_size: int = 800) -> list[str]:
    """마크다운 내용을 적절한 크기로 분할

    헤더를 기준으로 분할하며, 각 청크가 target_chunk_size에 가까운 크기가 되도록 함

    Args:
        content: 분할할 마크다운 전체 내용 문자열
        target_chunk_size: 목표 청크 크기 (줄 수)

    Returns:
        분할된 마크다운 청크들의 리스트 (각 청크는 문자열)
    """
    lines = content.splitlines()
    if not lines:
        return []

    # 파일이 작으면 분할하지 않고 그대로 반환
    if len(lines) <= target_chunk_size:
        return [content]

    # 헤더 위치 찾기
    header_positions = []
    for i, line in enumerate(lines):
        if _is_header(line):
            header_positions.append(i)

    # 헤더가 없으면 적절한 크기로 분할
    if not header_positions:
        chunks = []
        for i in range(0, len(lines), target_chunk_size):
            chunk = "\n".join(lines[i:i + target_chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    # 청크 분할 - 개선된 알고리즘
    chunks = []

    # 파일을 더 큰 청크로 분할하기 위해 적절한 분할 지점 찾기
    split_points = []

    # 파일 최대 크기를 목표의 1.5배로 제한
    max_chunk_size = int(target_chunk_size * 1.5)

    # 헤더 위치를 기준으로 분할 지점 찾기
    current_size = 0
    last_good_header = 0

    for i, pos in enumerate(header_positions):
        if i == 0:
            continue  # 첫 번째 헤더는 건너뜀 (파일 제목일 가능성 높음)

        current_size = pos - last_good_header

        # 현재 청크가 목표 크기에 가까운 경우 분할 지점으로 선택
        if current_size >= target_chunk_size * 0.7:
            split_points.append(pos)
            last_good_header = pos
        # 현재 청크가 최대 크기를 초과하는 경우 반드시 분할
        elif current_size >= max_chunk_size:
            split_points.append(pos)
            last_good_header = pos

    # 분할 지점이 없으면 적절한 크기로 강제 분할
    if not split_points and len(lines) > max_chunk_size:
        for i in range(max_chunk_size, len(lines), max_chunk_size):
            split_points.append(i)

    # 분할 지점을 기준으로 청크 생성
    start_idx = 0

    for split_point in split_points:
        chunk = "\n".join(lines[start_idx:split_point])
        if chunk.strip():
            chunks.append(chunk)
        start_idx = split_point

    # 마지막 청크 추가
    if start_idx < len(lines):
        chunk = "\n".join(lines[start_idx:])
        if chunk.strip():
            chunks.append(chunk)

    return chunks


def orchestrate_chunk_translation(
        content: str,
        source_lang: str,
        target_lang: str,
        original_filename_for_logging: str,
        translate_api_call_func: callable
) -> str:
    """마크다운 내용을 조각내어 번역하고 결과를 합침

    Args:
        content: 번역할 전체 마크다운 텍스트
        source_lang: 원본 언어 코드
        target_lang: 대상 언어 코드
        original_filename_for_logging: 로깅용 원본 파일명 (파일명만)
        translate_api_call_func: 단일 청크 번역 API 호출 함수
                                 (text_to_translate: str, system_prompt: str) -> str

    Returns:
        번역되고 합쳐진 전체 마크다운 텍스트

    Raises:
        FileNotFoundError: 'translation_prompt.txt' 파일을 찾을 수 없는 경우
        Exception: 'translation_prompt.txt' 파일 읽기 중 다른 오류 발생 시
    """
    try:
        with open("translation_prompt.txt", 'r', encoding='utf-8') as f:
            system_prompt_template = f.read()
    except Exception as e:
        print(f"오류: '{original_filename_for_logging}' - 프롬프트 파일 오류: {e}")
        raise

    system_prompt_base = system_prompt_template.format(source_lang=source_lang, target_lang=target_lang)

    # 목표 청크 크기를 1000줄로 설정하여 분할
    chunks = split_markdown_into_chunks(content, target_chunk_size=1000)

    if not chunks:
        print(f"정보: '{original_filename_for_logging}' - 단일 청크로 처리")
        if not content.strip():
            return ""
        try:
            system_prompt_for_single_chunk = f"{system_prompt_base}\nThis is the entire document (or a small single chunk) named '{original_filename_for_logging}'."
            return translate_api_call_func(content, system_prompt_for_single_chunk)
        except Exception as e:
            print(f"오류: '{original_filename_for_logging}' - 단일 청크 번역 실패 ({type(e).__name__}: {e})")
            return content

    print(f"정보: '{original_filename_for_logging}' - {len(chunks)}개 청크로 분할")
    translated_chunks = []
    total_chunks = len(chunks)

    for i, chunk_content in enumerate(chunks):
        system_prompt_for_chunk = f"{system_prompt_base}\nThis is chunk {i + 1} of {total_chunks} from the document '{original_filename_for_logging}'. Please translate it while maintaining context with other parts of the document."

        current_chunk_line_count = len(chunk_content.splitlines())
        print(f"정보: '{original_filename_for_logging}' - {i + 1}/{total_chunks} 청크, 번역 시작 ({current_chunk_line_count}줄)")

        if not chunk_content.strip():
            translated_chunks.append("")
            print(f"정보: '{original_filename_for_logging}' - {i + 1}/{total_chunks} 청크, (빈 청크) 건너뜀")
            continue

        if current_chunk_line_count > 800:
            print(
                f"경고: '{original_filename_for_logging}' - {i + 1}/{total_chunks} 청크, ({current_chunk_line_count}줄) 매우 김")

        try:
            translated_chunk = translate_api_call_func(chunk_content, system_prompt_for_chunk)
            translated_chunks.append(translated_chunk)
            print(f"정보: '{original_filename_for_logging}' - {i + 1}/{total_chunks} 청크, 번역 완료")
        except Exception as e:
            print(f"오류: '{original_filename_for_logging}' - {i + 1}/{total_chunks} 청크, 번역 실패 ({type(e).__name__}: {e})")
            print(f"정보: '{original_filename_for_logging}' - {i + 1}/{total_chunks} 청크, 원본으로 대체")
            translated_chunks.append(chunk_content)

        if i < total_chunks - 1:
            time.sleep(30)

    processed_translated_chunks = []
    for tc in translated_chunks:
        stripped_tc = tc.strip() if tc is not None else ""
        if stripped_tc:
            processed_translated_chunks.append(stripped_tc)

    reassembled_content = "\n\n".join(processed_translated_chunks)

    print(f"정보: '{original_filename_for_logging}' - 모든 청크 번역 및 병합 완료")

    return reassembled_content
