# 라라벨 핀트 (Laravel Pint)

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합(CI)](#continuous-integration)
    - [GitHub Actions 자동화](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 주관적인(opinionated) PHP 코드 스타일 자동 수정 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으며, 여러분의 코드 스타일이 깔끔하고 일관된 상태로 유지되도록 쉽게 도와줍니다.

Pint는 모든 신규 라라벨 애플리케이션에 자동으로 포함되어 있으므로 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정을 요구하지 않으며, 라라벨의 주관적인 코딩 스타일을 따라 여러분의 코드 스타일 문제를 자동으로 수정해 줍니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 최신 버전의 라라벨 프레임워크에는 기본 포함되어 있으므로, 별도의 설치가 필요하지 않은 경우가 많습니다. 그러나 구버전 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 실행하여 코드 스타일 문제를 자동으로 수정할 수 있습니다:

```shell
./vendor/bin/pint
```

향상된 성능을 위해 Pint를 병렬(parallel) 모드(실험적)로 실행하고 싶다면, `--parallel` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --parallel
```

병렬 모드에서는 추가로, `--max-processes` 옵션을 통해 최대 실행 프로세스 수를 지정할 수 있습니다. 이 옵션을 생략할 경우, Pint는 시스템의 모든 사용 가능한 코어를 사용합니다:

```shell
./vendor/bin/pint --parallel --max-processes=4
```

특정 파일이나 디렉터리에 Pint를 적용하고 싶다면 아래와 같이 실행할 수 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 수정한 모든 파일 목록을 자세하게 출력해줍니다. `-v` 옵션을 추가하면, Pint의 변경 내용에 대한 더 상세한 정보를 확인할 수 있습니다:

```shell
./vendor/bin/pint -v
```

코드를 실제로 수정하지 않고, 스타일 오류만 점검(리포트)하고 싶다면 `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git 상에서 특정 브랜치와의 차이(diff)가 있는 파일만 Pint로 수정하고 싶다면, `--diff=[branch]` 옵션을 활용할 수 있습니다. 이 옵션은 CI 환경(예: GitHub Actions)에서 새 파일이나 수정된 파일만 점검하도록 하여 시간을 절약할 수 있습니다:

```shell
./vendor/bin/pint --diff=main
```

Git 기준으로 커밋되지 않은 변경사항이 있는 파일만 Pint가 수정하도록 하려면 `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 자동 수정하는 동시에, 오류가 하나라도 수정되었으면 0이 아닌 종료코드로 종료하도록 하려면 `--repair` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기 (Configuring Pint)

앞서 언급한 것처럼, Pint는 별도의 설정 없이 바로 사용할 수 있습니다. 하지만, 프리셋, 규칙, 또는 검사 대상 폴더를 커스터마이즈하고 싶다면 프로젝트 루트 디렉터리에 `pint.json` 파일을 만들어 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

추가로, 특정 디렉터리 안의 `pint.json` 파일을 사용하고 싶다면, Pint 실행 시 `--config` 옵션으로 경로를 지정할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋 (Presets)

프리셋은 코드 스타일 문제를 자동으로 수정할 때 사용할 규칙 집합을 정의합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여, 라라벨의 주관적인 코딩 스타일을 적용합니다. 하지만 필요하다면 `--preset` 옵션으로 다른 프리셋을 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

원한다면, 프로젝트의 `pint.json` 파일에 프리셋을 지정할 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

현재 Pint가 지원하는 프리셋은 다음과 같습니다: `laravel`, `per`, `psr12`, `symfony`, `empty`.

<a name="rules"></a>
### 규칙 (Rules)

규칙은 Pint가 코드 스타일을 자동으로 수정할 때 적용하는 세부 스타일 가이드입니다. 앞에서 설명한 것처럼, 프리셋은 일반적으로 대부분의 PHP 프로젝트에 적합한 규칙 집합을 미리 정의해두었으므로, 개별 규칙을 신경 쓸 필요가 없습니다.

하지만 필요하다면, `pint.json` 파일에서 특정 규칙을 직접 켜거나 끌 수도 있고, `empty` 프리셋을 선택하여 필요한 규칙만 직접 정의할 수도 있습니다:

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "array_indentation": false,
        "new_with_parentheses": {
            "anonymous_class": true,
            "named_class": true
        }
    }
}
```

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 제작되었습니다. 따라서, PHP CS Fixer의 모든 규칙을 적용할 수 있습니다: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기 (Excluding Files / Folders)

기본적으로 Pint는 `vendor` 디렉터리를 제외한 프로젝트 내 모든 `.php` 파일을 검사합니다. 추가로 폴더를 제외하고 싶다면, `exclude` 설정 옵션을 사용할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴이 포함된 모든 파일을 제외하고 싶다면, `notName` 설정 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 파일 경로로 파일을 제외하고 싶을 경우에는, `notPath` 옵션을 사용할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 지속적 통합(CI) (Continuous Integration)

<a name="running-tests-on-github-actions"></a>
### GitHub Actions 자동화

라라벨 Pint를 사용하여 프로젝트의 코드 린트(linting)를 자동화하고자 한다면, [GitHub Actions](https://github.com/features/actions)를 활용해 새로운 코드가 GitHub에 푸시될 때마다 Pint를 실행할 수 있습니다. 먼저, **Settings > Actions > General > Workflow permissions**에서 워크플로에 "읽기 및 쓰기 권한(Read and write permissions)"을 부여해야 합니다. 그리고 `.github/workflows/lint.yml` 파일을 생성하여 아래와 같이 설정할 수 있습니다:

```yaml
name: Fix Code Style

on: [push]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        php: [8.4]

    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: json, dom, curl, libxml, mbstring
          coverage: none

      - name: Install Pint
        run: composer global require laravel/pint

      - name: Run Pint
        run: pint

      - name: Commit linted files
        uses: stefanzweifel/git-auto-commit-action@v6
```