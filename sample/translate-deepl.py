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

# deepl 라이브러리 설치 확인 및 자동 설치
try:
    import deepl
except ImportError:
    print("deepl 라이브러리가 설치되어 있지 않습니다. 설치를 시도합니다...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "deepl"])
        import deepl

        print("deepl 설치 완료!")
    except Exception as e:
        print(f"deepl 설치 실패: {e}")
        print("수동으로 설치해주세요: pip install deepl")
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


def main():
    # .env 파일 로드
    dotenv.load_dotenv()

    # 번역할 파일 경로 설정 (여기에서 직접 수정하세요)
    input_file = "logging.md"  # 번역할 파일 경로
    output_file = "logging-deepl.md"  # 번역 결과를 저장할 파일 경로
    source_lang = "EN"  # 원본 언어 코드 (EN: 영어, DE: 독일어 등)
    target_lang = "ko"  # 대상 언어 코드 (ko: 한국어, ja: 일본어, zh: 중국어 등)

    # API 키 확인 (.env 파일에서 가져오기)
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        print("오류: DEEPL_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 생성하고 다음 내용을 추가하세요:")
        print("DEEPL_API_KEY=your_api_key_here")

        # .env 파일 자동 생성 예시
        if not os.path.exists("../.env"):
            try:
                with open("../.env", "w") as f:
                    f.write("DEEPL_API_KEY=\n")
                print(".env 파일이 생성되었습니다. API 키를 추가하고 다시 실행하세요.")
            except Exception as e:
                print(f".env 파일 생성 실패: {e}")
        return

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
            shutil.copy2(input_file, output_file)
            return

        # DeepL API로 번역
        print(f"DeepL API를 사용하여 '{source_lang}'에서 '{target_lang}'로 번역 중...")
        deepl_client = deepl.DeepLClient(api_key)
        result = deepl_client.translate_text(
            translatable_text,
            target_lang=target_lang.upper(),
            source_lang=source_lang.upper(),
            preserve_formatting=True
        )
        translated_text = result.text

        # 번역된 텍스트와 번역되지 않은 원본 줄을 합쳐서 최종 결과 생성
        final_content = merge_translations(translated_text, translatable_lines, non_translatable_lines, original_lines)

        # 번역된 내용 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"번역 완료! 결과가 '{output_file}'에 저장되었습니다.")
        print(f"번역된 텍스트 크기: {len(final_content)} 바이트")
        print(f"청구된 문자 수: {result.billed_characters}")

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    main()
