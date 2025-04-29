#!/usr/bin/env python3
import os
import shutil
import subprocess


def run_command(command, cwd=None):
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
        cwd=cwd
    )
    return result.stdout.strip()


def main():
    repo_url = "https://github.com/laravel/docs.git"
    branches = ["master", "12.x", "11.x", "10.x", "9.x", "8.x"]

    # 작업 디렉토리 설정
    work_dir = os.path.join(os.getcwd(), "laravel-docs-temp")
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)

    run_command(f"git clone {repo_url} {work_dir}")
    for branch in branches:
        print(f"\n브랜치 : {branch}")
        run_command(f"git checkout {branch}", cwd=work_dir)

        # en 디렉토리 설정 및 생성
        en_target_dir = os.path.join(os.getcwd(), f"{branch}/en")
        os.makedirs(en_target_dir, exist_ok=True)

        # ko 디렉토리 설정 및 생성
        ko_target_dir = os.path.join(os.getcwd(), f"{branch}/ko")
        os.makedirs(ko_target_dir, exist_ok=True)

        # 최상위 디렉토리의 마크다운 파일만 가져오기
        for file in os.listdir(work_dir):
            if file.endswith(".md"):
                source_path = os.path.join(work_dir, file)

                # en 디렉토리에 파일 복사
                en_target_path = os.path.join(en_target_dir, file)
                shutil.copy2(source_path, en_target_path)

                # ko 디렉토리에 동일한 파일 복사
                ko_target_path = os.path.join(ko_target_dir, file)
                shutil.copy2(source_path, ko_target_path)

        print(f"{branch} 복사")

    print("\n작업 디렉토리 정리")
    shutil.rmtree(work_dir)


if __name__ == "__main__":
    main()
