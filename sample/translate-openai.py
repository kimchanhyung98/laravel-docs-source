#!/usr/bin/env python3
import os
import sys
import subprocess

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

def main():
    # .env 파일 로드
    dotenv.load_dotenv()

    # 번역할 파일 경로 설정 (여기에서 직접 수정하세요)
    input_file = "logging.md"  # 번역할 파일 경로
    # 출력 파일명을 {원본파일명}-openai.md 형식으로 자동 생성
    output_file = f"{os.path.splitext(input_file)[0]}-openai.md"  # 번역 결과를 저장할 파일 경로
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
    client = openai.OpenAI()

    # 입력 파일 확인
    if not os.path.exists(input_file):
        print(f"오류: 입력 파일 '{input_file}'이 존재하지 않습니다.")
        return

    try:
        # 원본 파일 읽기
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"파일 '{input_file}'을 읽었습니다. (크기: {len(content)} 바이트)")

        # 시스템 프롬프트 설정
        system_prompt = f"""당신은 전문 번역가입니다. {source_lang}에서 {target_lang}로 마크다운 문서를 번역해주세요.

중요한 지침:
1. 코드 블록, HTML 태그, 링크 URL은 번역하지 마세요.
2. 마크다운 형식을 유지하세요.
3. 전문 용어는 적절하게 번역하세요.
"""

        # OpenAI API로 번역
        print(f"OpenAI API를 사용하여 '{source_lang}'에서 '{target_lang}'로 번역 중...")

        # API 요청 파라미터 설정
        params = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"다음 마크다운 문서를 {target_lang}로 번역해주세요:\n\n{content}"}
            ]
        }

        # API 호출
        response = client.chat.completions.create(**params)

        # 번역 결과 추출
        translated_content = response.choices[0].message.content

        # 토큰 사용량 출력
        print(f"사용된 토큰: {response.usage.total_tokens}")

        # 번역된 내용 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)

        print(f"번역 완료! 결과가 '{output_file}'에 저장되었습니다.")
        print(f"번역된 텍스트 크기: {len(translated_content)} 바이트")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
