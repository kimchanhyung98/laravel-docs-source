# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋(Presets)](#presets)
    - [규칙(Rules)](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합(CI)](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 규칙 기반 PHP 코드 스타일 자동화 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 하며, 코딩 스타일을 깨끗하고 일관되게 유지하도록 돕습니다.

Pint는 모든 신규 Laravel 애플리케이션에 자동으로 설치되므로 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 라라벨의 의견이 반영된 코딩 스타일을 따라 코드 스타일 문제를 자동으로 교정합니다.

<a name="installation"></a>
## 설치

Pint는 최신 라라벨 프레임워크에 기본 포함되어 있으므로, 별도의 설치가 필요하지 않습니다. 그러나 구버전 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다.

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기

Pint는 프로젝트의 `vendor/bin` 디렉토리에 위치한 `pint` 바이너리를 통해 코드 스타일 문제를 교정할 수 있습니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉터리에서도 Pint를 실행할 수 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트된 모든 파일 목록을 자세히 출력합니다. 더 자세한 변경 사항을 확인하려면 `-v` 옵션을 사용하세요:

```shell
./vendor/bin/pint -v
```

파일을 실제로 수정하지 않고 코드 스타일 오류만 점검하려면 `--test` 옵션을 사용하세요. 코드 스타일 오류가 발견되면 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git 기준 브랜치와 달라진 파일만 수정하려면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이 옵션은 GitHub Actions와 같은 CI 환경에서 변경된 파일만 검사할 때 유용합니다:

```shell
./vendor/bin/pint --diff=main
```

Git 상에서 커밋되지 않은 변경사항이 있는 파일만 검사하려면 `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 수정하되, 하나라도 오류가 수정되었다면 0이 아닌 종료 코드로 종료하고 싶다면 `--repair` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기

앞서 언급했듯이 Pint는 기본적으로 별도의 설정이 필요 없습니다. 하지만 프리셋, 규칙, 검사 폴더 등을 사용자화하고 싶다면 프로젝트 루트에 `pint.json` 파일을 생성하여 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

특정 디렉터리의 `pint.json` 파일을 사용하고 싶다면 Pint 실행 시 `--config` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋(Presets)

프리셋은 코드 스타일 문제를 교정하는 규칙 집합을 정의합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여, 라라벨의 코딩 스타일을 따릅니다. 다른 프리셋을 사용하고 싶다면 Pint 실행 시 `--preset` 옵션으로 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

`pint.json` 파일에 프리셋을 설정할 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

현재 Pint에서 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty`입니다.

<a name="rules"></a>
### 규칙(Rules)

규칙은 Pint가 코드 스타일 문제를 교정할 때 사용할 세부 지침입니다. 앞서 다룬 프리셋은 적절하게 조합된 규칙 모음이므로 대부분의 PHP 프로젝트에서는 프리셋만으로 충분합니다.

하지만 필요에 따라 `pint.json`에서 개별 규칙을 켜거나 끌 수 있고, 또는 `empty` 프리셋을 사용해 자신만의 규칙 세트를 구성할 수 있습니다:

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 하므로, 프로젝트 내 코드 스타일 교정을 위해 그 규칙들을 그대로 사용할 수 있습니다. 자세한 규칙 목록은 [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)를 참고하세요.

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기

기본적으로 Pint는 `vendor` 디렉토리를 제외한 모든 `.php` 파일을 검사합니다. 특정 폴더를 검사 대상에서 제외하려면, `exclude` 옵션을 설정할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 포함하는 모든 파일을 제외하려면 `notName` 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 파일 경로로 파일을 제외하려면 `notPath` 옵션을 사용할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 지속적 통합(CI)

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Laravel Pint를 활용해 프로젝트 코드 스타일 검사를 자동화하려면 [GitHub Actions](https://github.com/features/actions)를 구성할 수 있습니다. 새 코드를 GitHub에 푸시할 때 마다 Pint가 실행됩니다. 먼저 GitHub에서 **Settings > Actions > General > Workflow permissions**에서 워크플로에 "읽기 및 쓰기 권한(Read and write permissions)"을 부여하세요. 이후 다음 내용을 가진 `.github/workflows/lint.yml` 파일을 만듭니다:

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
        uses: actions/checkout@v4

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
        uses: stefanzweifel/git-auto-commit-action@v5
```
