#!/usr/bin/env python3
import os
import re
import subprocess
import sys

# python-dotenv 라이브러리 설치 확인 및 자동 설치
try:
    import dotenv
except ImportError:
    print("python-dotenv 라이브러리가 설치되어 있지 않습니다. 설치를 시도합니다...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        import dotenv

        print("python-dotenv 설치 완료!")
    except Exception as e:
        print(f"python-dotenv 설치 실패: {e}")
        print("수동으로 설치해주세요: pip install python-dotenv")
        sys.exit(1)

# openai 라이브러리 설치 확인 및 자동 설치
try:
    import openai
except ImportError:
    print("openai 라이브러리가 설치되어 있지 않습니다. 설치를 시도합니다...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
        import openai

        print("openai 설치 완료!")
    except Exception as e:
        print(f"openai 설치 실패: {e}")
        print("수동으로 설치해주세요: pip install openai")
        sys.exit(1)


# 마크다운 파일을 줄 단위로 처리하여 번역해야 할 부분과 보존해야 할 부분을 구분하는 함수
def extract_translatable_content(markdown_text):
    # 줄 단위로 분리
    lines = markdown_text.split('\n')
    translatable_lines = []
    non_translatable_lines = []
    in_code_block = False

    # 각 줄을 처리
    for i, line in enumerate(lines):
        # 코드 블록 시작/종료 확인
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            non_translatable_lines.append((i, line))
            continue

        # 코드 블록 내부인 경우 번역하지 않음
        if in_code_block:
            non_translatable_lines.append((i, line))
            continue

        # HTML 태그나 링크만 있는 줄 처리
        if re.match(r'^<[^>]+>$', line.strip()) or \
                re.match(r'^\[.*\]\(.*\)$', line.strip()) or \
                re.match(r'^\s*$', line.strip()) or \
                line.strip().startswith('> [!') or \
                line.strip().startswith('- [') or \
                line.strip().startswith('# ') or \
                line.strip().startswith('## ') or \
                line.strip().startswith('### ') or \
                line.strip().startswith('#### ') or \
                line.strip().startswith('##### ') or \
                line.strip().startswith('###### '):
            non_translatable_lines.append((i, line))
            continue

        # 번역해야 할 줄
        translatable_lines.append((i, line))

    # 번역할 줄만 모아서 하나의 텍스트로 합치기
    translatable_text = '\n'.join([line for _, line in translatable_lines])

    print(f"\n번역할 줄: {len(translatable_lines)}")
    print(f"번역하지 않을 줄: {len(non_translatable_lines)}")

    return translatable_text, translatable_lines, non_translatable_lines


# 번역된 텍스트와 번역되지 않은 원본 줄을 합쳐서 최종 결과를 생성하는 함수
def merge_translations(translated_text, translatable_lines, non_translatable_lines, original_lines):
    # 번역된 텍스트를 줄 단위로 분리
    translated_lines = translated_text.split('\n')

    # 번역할 줄 개수와 번역된 줄 개수가 다르면 오류 처리
    if len(translated_lines) != len(translatable_lines):
        print(f"\n경고: 번역된 줄 개수({len(translated_lines)})가 번역할 줄 개수({len(translatable_lines)})와 다릅니다.")
        # 더 적은 개수를 기준으로 처리
        min_lines = min(len(translated_lines), len(translatable_lines))
        translatable_lines = translatable_lines[:min_lines]
        translated_lines = translated_lines[:min_lines]

    # 번역된 줄과 번역되지 않은 원본 줄을 합쳐서 최종 결과 생성
    result_lines = original_lines.copy()  # 원본 전체 줄 복사

    # 번역된 줄 삽입
    for i, (original_line_num, _) in enumerate(translatable_lines):
        result_lines[original_line_num] = translated_lines[i]

    # 최종 결과 합치기
    return '\n'.join(result_lines)


# OpenAI API를 사용하여 텍스트 번역
def translate_with_openai(text, target_lang="ko", source_lang="EN", model="o1"):
    client = openai.OpenAI()

    # 번역 요청 생성 - 상세한 지침 추가
    system_prompt = f"""당신은 전문 번역가입니다. {source_lang}에서 {target_lang}로 텍스트를 번역해주세요.

중요한 지침:
1. 원본 텍스트의 줄바꿈과 형식을 정확히 유지하세요. 추가 줄바꿈을 삽입하지 마세요.
2. 코드 블록, HTML 태그, 링크, 마크다운 구문은 절대 번역하지 마세요.
3. 텍스트만 번역하고, 텍스트 이외의 요소는 그대로 유지하세요.
4. 원본 텍스트의 줄 수와 번역된 텍스트의 줄 수가 정확히 일치해야 합니다.
"""

    try:
        # o1 모델은 temperature 매개변수를 지원하지 않음
        params = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"다음 텍스트를 {target_lang}로 번역해주세요. 원본 형식을 정확히 유지해주세요:\n\n{text}"}
            ]
        }

        # o1 모델이 아닌 경우에만 temperature 설정
        if not model.startswith('o1'):
            params["temperature"] = 0.3  # 낮은 온도로 일관된 번역 결과 유도

        response = client.chat.completions.create(**params)

        # 번역 결과 반환
        translated_text = response.choices[0].message.content

        # 토큰 사용량 출력
        print(f"사용된 토큰: {response.usage.total_tokens}")

        return translated_text

    except Exception as e:
        print(f"OpenAI API 오류: {e}")
        return text  # 오류 발생 시 원본 텍스트 반환


def main():
    # .env 파일 로드
    dotenv.load_dotenv()

    # 번역할 파일 경로 설정 (여기에서 직접 수정하세요)
    input_file = "logging.md"  # 번역할 파일 경로
    output_file = "logging-openai.md"  # 번역 결과를 저장할 파일 경로
    source_lang = "EN"  # 원본 언어 코드 (EN: 영어, DE: 독일어 등)
    target_lang = "ko"  # 대상 언어 코드 (ko: 한국어, ja: 일본어, zh: 중국어 등)

    # 모델 설정
    model = os.environ.get("TRANSLATION_MODEL", "o1")

    # API 키 확인 (.env 파일에서 가져오기)
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("오류: OPENAI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 생성하고 다음 내용을 추가하세요:")
        print("OPENAI_API_KEY=your_api_key_here")
        return

    # OpenAI 클라이언트 설정
    openai.api_key = api_key

    # 입력 파일 확인
    if not os.path.exists(input_file):
        print(f"오류: 입력 파일 '{input_file}'이 존재하지 않습니다.")
        return

    try:
        # 원본 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"파일 '{input_file}'을 읽었습니다. (크기: {len(content)} 바이트)")

        # 원본 파일을 줄 단위로 분리
        original_lines = content.split('\n')

        # 번역해야 할 부분과 보존해야 할 부분 구분
        translatable_text, translatable_lines, non_translatable_lines = extract_translatable_content(content)

        # 번역할 텍스트가 없으면 원본 그대로 저장
        if not translatable_text.strip():
            print("번역할 텍스트가 없습니다. 원본 파일을 그대로 복사합니다.")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return

        # 텍스트가 너무 길면 청크로 나누기
        max_chunk_size = 4000  # 약 4000자 단위로 나누기
        chunks = []

        if len(translatable_text) > max_chunk_size:
            # 문단 단위로 청크 나누기 (빈 줄을 기준으로 문단 구분)
            paragraphs = []
            current_paragraph = []

            for line in translatable_text.split('\n'):
                if line.strip() == '':
                    if current_paragraph:
                        paragraphs.append('\n'.join(current_paragraph))
                        current_paragraph = []
                    paragraphs.append('')  # 빈 줄 추가
                else:
                    current_paragraph.append(line)

            if current_paragraph:  # 마지막 문단 추가
                paragraphs.append('\n'.join(current_paragraph))

            # 문단을 청크로 묶기
            current_chunk = []
            current_size = 0

            for paragraph in paragraphs:
                paragraph_size = len(paragraph) + 1  # \n 문자 포함

                if current_size + paragraph_size > max_chunk_size and current_chunk:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = [paragraph]
                    current_size = paragraph_size
                else:
                    current_chunk.append(paragraph)
                    current_size += paragraph_size

            if current_chunk:  # 마지막 청크 추가
                chunks.append('\n'.join(current_chunk))

            print(f"텍스트를 {len(chunks)}개의 청크로 나누었습니다.")
        else:
            chunks = [translatable_text]

        # 각 청크 번역
        translated_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"청크 {i + 1}/{len(chunks)} 번역 중... (크기: {len(chunk)} 자)")
            translated_chunk = translate_with_openai(
                chunk,
                target_lang=target_lang,
                source_lang=source_lang,
                model=model
            )
            translated_chunks.append(translated_chunk)

        # 번역된 청크 합치기
        translated_text = '\n'.join(translated_chunks)

        # 번역된 텍스트와 번역되지 않은 원본 줄을 합쳐서 최종 결과 생성
        final_content = merge_translations(translated_text, translatable_lines, non_translatable_lines, original_lines)

        # 번역된 내용 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"번역 완료! 결과가 '{output_file}'에 저장되었습니다.")
        print(f"번역된 텍스트 크기: {len(final_content)} 바이트")

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()
