#!/usr/bin/env python3
"""
공통 유틸리티 함수 모듈
"""
import subprocess
import time
from functools import wraps


def retry(max_attempts=3, delay=3, backoff=2, exceptions=(Exception,)):
    """예외 발생 시 함수를 재시도하는 데코레이터

    Args:
        max_attempts: 최대 시도 횟수
        delay: 초기 대기 시간(초)
        backoff: 대기 시간 증가 요소(다음 시도에서는 delay * backoff)
        exceptions: 재시도할 예외 클래스 튜플
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    error_type = type(e).__name__
                    if attempt >= max_attempts:
                        print(f"최대 시도 횟수 초과. 오류: {error_type} - {e}")
                        raise

                    print(f"오류: {error_type} - {e}")
                    print(f"재시도 중... ({attempt}/{max_attempts})")
                    time.sleep(current_delay)
                    current_delay *= backoff

            return None  # 이 코드는 실행되지 않지만 형식적으로 필요

        return wrapper

    return decorator


def timeout(seconds=420):
    """함수 실행 시 타임아웃을 적용하는 데코레이터

    Args:
        seconds: 타임아웃 시간(초)
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal

            def handler(signum, frame):
                raise TimeoutError(f"함수 실행이 {seconds}초를 초과했습니다.")

            # 타임아웃 설정
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
                signal.alarm(0)  # 타이머 재설정
                return result
            except TimeoutError as e:
                print(f"타임아웃: {e}")
                raise
            finally:
                signal.alarm(0)  # 타이머 재설정

        return wrapper

    return decorator


def run_command(command, cwd=None):
    """명령어를 실행하고 결과를 반환

    Args:
        command: 실행할 명령어
        cwd: 명령어를 실행할 디렉토리 (기본값: None)

    Returns:
        str: 명령어 실행 결과
    """
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
        cwd=cwd
    )
    return result.stdout.strip()
