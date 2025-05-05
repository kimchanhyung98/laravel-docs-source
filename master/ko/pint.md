# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋(Presets)](#presets)
    - [규칙(Rules)](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합(Continuous Integration)](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 라라벨 스타일의 PHP 코드 스타일 자동 정리 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 구축되어, 코드 스타일을 깔끔하고 일관되게 유지하도록 돕습니다.

Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되므로 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 작동하며, Laravel의 권장 코딩 스타일을 따르면서 코드 스타일 문제를 자동으로 수정해줍니다.

<a name="installation"></a>
## 설치

Pint는 최근에 출시된 Laravel 프레임워크에 기본 포함되어 있어 별도의 설치가 필요하지 않습니다. 하지만, 구버전 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기

Pint를 통해 코드 스타일 문제를 고치고 싶다면, 프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 실행하면 됩니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉터리에 대해서만 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트한 모든 파일의 리스트를 상세하게 보여줍니다. `-v` 옵션을 추가로 주면, Pint의 변경 사항에 대해 더 많은 정보를 볼 수 있습니다:

```shell
./vendor/bin/pint -v
```

실제로 파일을 변경하지 않고 코드 스타일 오류만 검사하고 싶다면, `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git을 기준으로, 지정한 브랜치와 다른 파일만 수정하고 싶다면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이는 CI 환경(예: GitHub Actions)에서 새로 추가되거나 변경된 파일만 검사하는 데 유용합니다:

```shell
./vendor/bin/pint --diff=main
```

Git 기준으로 커밋되지 않은 변경 사항이 있는 파일만 수정하고 싶다면, `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 수정하되, 오류가 수정된 경우 0이 아닌 종료코드로 종료하고 싶다면 `--repair` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기

앞서 언급했듯이, Pint는 별도의 설정이 필요하지 않습니다. 하지만 프리셋, 규칙 또는 검사할 폴더를 커스터마이징하고 싶다면, 프로젝트 루트 디렉터리에 `pint.json` 파일을 생성하여 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리의 `pint.json`을 사용하고 싶다면, Pint 실행 시 `--config` 옵션을 통해 경로를 지정할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋(Presets)

프리셋은 코드 스타일 문제를 고치기 위해 적용할 규칙의 집합을 의미합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여, Laravel 권장 코딩 스타일에 따라 오류를 수정합니다. 하지만 필요에 따라 `--preset` 옵션으로 다른 프리셋을 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

또한, 프로젝트의 `pint.json` 파일에서도 프리셋을 지정할 수 있습니다:

```json
{
    "preset": "psr12"
}
```

현재 Pint가 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty`입니다.

<a name="rules"></a>
### 규칙(Rules)

규칙은 Pint가 코드 스타일 문제를 고치는 기준이 되는 스타일 가이드입니다. 앞서 언급한 프리셋은 여러 가지 규칙을 미리 그룹화해둔 것으로, 대부분의 PHP 프로젝트에 적합하므로 개별 규칙을 신경 쓸 필요가 거의 없습니다.

하지만, 원하는 경우 `pint.json` 파일에서 특정 규칙을 활성화/비활성화하거나, `empty` 프리셋을 사용해 규칙을 직접 정의할 수도 있습니다:

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으므로, 해당 도구의 모든 규칙을 적용할 수 있습니다: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기

기본적으로 Pint는 `vendor` 디렉터리를 제외한 프로젝트 내 모든 `.php` 파일을 검사합니다. 더 많은 폴더를 제외하고 싶다면 `exclude` 옵션을 사용할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 가진 파일을 모두 제외하고 싶다면, `notName` 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로를 통해 파일을 제외하고 싶다면, `notPath` 옵션을 사용할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 지속적 통합(Continuous Integration)

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Laravel Pint를 활용해 자동으로 프로젝트 코드를 린트하려면, [GitHub Actions](https://github.com/features/actions)에 Pint 작업을 구성하면 됩니다. 먼저, GitHub에서 **Settings > Actions > General > Workflow permissions** 메뉴에서 워크플로에 "읽기 및 쓰기 권한(Read and write permissions)"을 부여해야 합니다. 그리고 나서, 아래와 같이 `.github/workflows/lint.yml` 파일을 생성합니다:

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
