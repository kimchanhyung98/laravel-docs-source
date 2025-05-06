# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행](#running-pint)
- [Pint 설정](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일/폴더 제외](#excluding-files-or-folders)
- [지속적인 통합](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 견해가 담긴(opinionated) PHP 코드 스타일 자동 수정기입니다. Pint는 PHP-CS-Fixer 위에 구축되었으며, 코드 스타일을 간결하고 일관되게 유지할 수 있도록 도와줍니다.

Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되어 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 동작하며, Laravel의 견해가 담긴 코딩 스타일을 따르면서 코드 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
## 설치

Pint는 최근 버전의 Laravel 프레임워크에 기본으로 포함되어 있으므로 일반적으로 별도의 설치가 필요하지 않습니다. 그러나 구 버전의 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행

프로젝트의 `vendor/bin` 디렉토리에 있는 `pint` 실행 파일을 통해 Pint로 코드 스타일 문제를 자동으로 수정할 수 있습니다:

```shell
./vendor/bin/pint
```

Pint를 특정 파일이나 디렉토리에만 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트된 모든 파일 목록을 자세하게 출력합니다. `-v` 옵션을 사용하면 Pint의 변경 사항을 더 자세히 확인할 수 있습니다:

```shell
./vendor/bin/pint -v
```

코드를 실제로 변경하지 않고 스타일 오류만 점검하고 싶다면 `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git에서 제공한 브랜치와 비교하여 변경된 파일만 수정하고 싶다면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이는 GitHub Actions와 같은 CI 환경에서 새로운 파일이나 변경된 파일만 검사하여 시간을 절약하는 데 효과적입니다:

```shell
./vendor/bin/pint --diff=main
```

Git 기준으로 커밋되지 않은 변경 사항이 있는 파일만 수정하고 싶다면 `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 수정하면서, 동시에 오류가 수정되었을 때 0이 아닌 종료 코드로 종료하고 싶다면 `--repair` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정

앞서 언급한 것처럼, Pint는 별도의 설정 없이 사용할 수 있습니다. 그러나 프리셋, 규칙, 검사할 폴더 등을 커스터마이즈하고 싶다면 프로젝트 루트 디렉토리에 `pint.json` 파일을 생성하여 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉토리의 `pint.json`을 사용하려면 Pint 실행 시 `--config` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋

프리셋은 코드 스타일 문제를 해결하기 위해 적용할 규칙의 집합입니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여 Laravel의 코딩 스타일을 따릅니다. 하지만 `--preset` 옵션을 통해 다른 프리셋을 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

프리셋은 프로젝트의 `pint.json` 파일에도 지정할 수 있습니다:

```json
{
    "preset": "psr12"
}
```

Pint에서 현재 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty`입니다.

<a name="rules"></a>
### 규칙

규칙은 Pint가 코드 스타일 문제를 해결할 때 적용하는 스타일 지침입니다. 위에서 언급했듯, 프리셋은 미리 정의된 규칙들의 그룹이며, 대부분의 PHP 프로젝트에 적합하게 설정되어 있어 개별 규칙을 신경 쓰지 않아도 됩니다.

하지만, 필요하다면 `pint.json` 파일에서 특정 규칙을 활성화하거나 비활성화할 수 있습니다. 또는 `empty` 프리셋을 사용해 처음부터 규칙을 직접 정의할 수도 있습니다:

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

Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) 위에 구축되었습니다. 따라서, 프로젝트의 코드 스타일 문제를 해결하기 위해 PHP-CS-Fixer의 모든 규칙을 사용할 수 있습니다: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외

기본적으로 Pint는 `vendor` 디렉토리를 제외한 모든 `.php` 파일을 검사합니다. 추가로 폴더를 제외하고 싶다면 `exclude` 설정 옵션을 사용할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 포함하는 모든 파일을 제외하고 싶다면 `notName` 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

파일의 정확한 경로를 지정하여 제외하고 싶다면 `notPath` 옵션을 사용할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 지속적인 통합

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Laravel Pint로 프로젝트 린트(lint)를 자동화하기 위해 [GitHub Actions](https://github.com/features/actions)를 설정해 새로운 코드가 GitHub에 푸시될 때마다 Pint를 실행할 수 있습니다. 먼저 **설정 > Actions > 일반 > 워크플로 권한**(Settings > Actions > General > Workflow permissions)에서 워크플로에 "읽기 및 쓰기 권한"을 부여해야 합니다. 그 다음, 아래와 같은 내용을 담은 `.github/workflows/lint.yml` 파일을 생성합니다:

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
