#!/usr/bin/env python3
import os
import shutil
import subprocess


def run_command(command, cwd=None):
    """명령어를 실행하고 결과를 반환하는 함수"""
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
        cwd=cwd
    )
    return result.stdout.strip()


def get_git_changes():
    """
    git을 사용하여 현재 프로젝트의 변경사항을 확인하는 함수
    """
    try:
        # git status 명령어 실행
        status_output = run_command("git status --porcelain", cwd=os.getcwd())

        # 변경된 파일만 필터링
        changed_files = []

        for line in status_output.split('\n'):
            if not line.strip():
                continue

            file_path = line[3:].strip()

            # 마크다운 파일만 처리
            if file_path.endswith('.md'):
                # 파일 경로에서 브랜치 정보 추출
                path_parts = file_path.split('/')
                if len(path_parts) >= 3 and path_parts[1] == 'en':
                    changed_files.append(file_path)

        return sorted(changed_files)
    except subprocess.CalledProcessError:
        # git 명령어 실패 시 빈 목록 반환
        return []


def main():
    """Laravel 원본 문서를 현재 프로젝트에 덮어쓰는 함수"""
    # 원본 저장소 URL 및 작업 디렉토리 설정
    original_repo = "https://github.com/laravel/docs.git"
    temp_dir = "laravel-docs-temp"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]

    # 임시 디렉토리 삭제 후 새로 클론
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    run_command(f"git clone {original_repo} {temp_dir}")

    # 각 브랜치별 문서 업데이트
    for branch in branches:
        # 브랜치 체크아웃
        run_command(f"git checkout {branch}", cwd=temp_dir)

        # 현재 프로젝트의 해당 브랜치 디렉토리 확인
        branch_dir = os.path.join(os.getcwd(), branch)
        en_dir = os.path.join(branch_dir, "en")
        ko_dir = os.path.join(branch_dir, "ko")

        # 디렉토리가 없으면 생성
        os.makedirs(en_dir, exist_ok=True)
        os.makedirs(ko_dir, exist_ok=True)

        # 원본 저장소의 마크다운 파일 목록 가져오기
        md_files = [f for f in os.listdir(temp_dir) if f.endswith(".md")]

        # 각 마크다운 파일 복사
        for file in md_files:
            source_path = os.path.join(temp_dir, file)
            en_target_path = os.path.join(en_dir, file)
            ko_target_path = os.path.join(ko_dir, file)

            # en 디렉토리에 파일 복사
            shutil.copy2(source_path, en_target_path)

            # ko 디렉토리에 파일 복사 (없을 경우에만)
            if not os.path.exists(ko_target_path):
                shutil.copy2(source_path, ko_target_path)

        # 변경사항을 git에 추가
        run_command(f"git add {branch}/en/*.md", cwd=os.getcwd())

        # 브랜치 업데이트 완료 메시지
        print(f"{branch} 브랜치 업데이트 완료")

    # 작업 완료 후 임시 디렉토리 삭제
    shutil.rmtree(temp_dir)

    # 모든 브랜치 처리가 끝난 후 변경사항 확인
    print("\n변경 사항")
    changed_files = get_git_changes()

    # 변경 사항 출력
    if changed_files:
        for file in changed_files:
            print(f"- {file}")
    else:
        print("- 변경 사항 없음")


if __name__ == "__main__":
    main()
