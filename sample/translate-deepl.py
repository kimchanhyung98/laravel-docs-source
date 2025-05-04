#!/usr/bin/env python3
import os
import deepl
import dotenv

def main():
    # .env 파일 로드
    dotenv.load_dotenv()

    # 파일 경로 설정
    input_file = "logging.md"
    output_file = f"{os.path.splitext(input_file)[0]}-deepl.md"

    # DeepL API 키 가져오기
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        print("DEEPL_API_KEY가 설정되지 않았습니다.")
        return

    # 파일 읽기
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # DeepL 번역
    translator = deepl.Translator(api_key)
    result = translator.translate_text(
        content,
        source_lang="EN",
        target_lang="KO",
        tag_handling="html",
        ignore_tags=["code", "pre", "a"]
    )

    # 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.text)

    print(f"번역 완료: {output_file}")

if __name__ == "__main__":
    main()
