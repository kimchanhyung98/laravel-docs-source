#!/usr/bin/env python3
import os
import openai
import dotenv

def main():
    # .env 파일 로드
    dotenv.load_dotenv()

    # 파일 경로 설정
    input_file = "logging.md"
    output_file = "logging-openai.md"

    # OpenAI API 키 가져오기
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY가 설정되지 않았습니다.")
        return

    # 파일 읽기
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # OpenAI 번역
    openai.api_key = api_key
    client = openai.OpenAI()

    # 시스템 프롬프트 설정
    system_prompt = f"""당신은 전문 번역가입니다. EN에서 ko로 마크다운 문서를 번역해주세요.

중요한 지침:
1. 코드 블록, HTML 태그, 링크 URL은 번역하지 마세요.
2. 마크다운 형식을 유지하세요.
3. 전문 용어는 적절하게 번역하세요.
"""

    response = client.chat.completions.create(
        model=os.environ.get("TRANSLATION_MODEL", "gpt-4.1"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"다음 마크다운 문서를 번역해주세요:\n\n{content}"}
        ]
    )

    # 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)

    print(f"번역 완료: {output_file}")

if __name__ == "__main__":
    main()
