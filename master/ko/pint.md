# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일 / 폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 의견 있는 PHP 코드 스타일 고정기입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으며, 코드 스타일을 깔끔하고 일관되게 유지하는 작업을 간단하게 만들어 줍니다.

Pint는 모든 새 Laravel 애플리케이션에 자동으로 설치되어 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 Laravel의 의견 있는 코딩 스타일을 따르며 코드 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 최근 Laravel 프레임워크 버전에 기본 포함되어 있어 대개 별도 설치가 필요하지 않습니다. 다만, 이전 버전의 애플리케이션에서는 Composer를 사용해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 실행 파일을 호출해서 Pint로 코드 스타일 문제를 고칠 수 있습니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉터리에 대해서만 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 수정한 모든 파일 목록을 자세히 출력합니다. `-v` 옵션을 추가해 실행하면 변경사항에 대해 더 상세한 정보를 볼 수 있습니다:

```shell
./vendor/bin/pint -v
```

코드를 실제로 변경하지 않고 스타일 오류만 검사하고 싶다면 `--test` 옵션을 사용하세요. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git의 특정 브랜치와 다른 파일만 수정하고 싶다면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이는 GitHub Actions 같은 CI 환경에서 새로 추가되거나 변경된 파일만 검사해 시간을 절약하는 데 유용합니다:

```shell
./vendor/bin/pint --diff=main
```

커밋되지 않은 변경 사항이 있는 파일만 검사하려면 `--dirty` 옵션을 사용하세요:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 수정하되, 오류가 수정되었다면 0이 아닌 종료 코드로 종료하도록 하려면 `--repair` 옵션을 사용하세요:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기 (Configuring Pint)

앞서 언급했듯이 Pint는 기본적으로 설정이 필요 없습니다. 하지만 프리셋, 규칙, 검사할 폴더 등을 직접 제어하고 싶다면 프로젝트 루트에 `pint.json` 파일을 생성하여 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리의 `pint.json` 설정 파일을 사용하고 싶을 경우, Pint 실행 시 `--config` 옵션을 지정할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋 (Presets)

프리셋은 코드 스타일 문제를 고치는 데 사용할 규칙 집합입니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하며, Laravel의 의견 있는 코딩 스타일을 따릅니다. 그러나 필요에 따라 `--preset` 옵션으로 다른 프리셋을 지정할 수도 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

원하는 경우 프로젝트의 `pint.json` 파일에서도 프리셋을 설정할 수 있습니다:

```json
{
    "preset": "psr12"
}
```

Pint에서 현재 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty`입니다.

<a name="rules"></a>
### 규칙 (Rules)

규칙은 Pint가 코드 스타일 문제를 고칠 때 따르는 스타일 가이드라인입니다. 앞서 설명했듯이, 프리셋은 대부분 PHP 프로젝트에 적합한 규칙 그룹을 미리 정해둔 것이므로 보통은 개별 규칙을 걱정할 필요가 없습니다.

다만, 원한다면 `pint.json` 파일에서 특정 규칙을 활성화하거나 비활성화할 수 있으며, `empty` 프리셋을 선택하고 직접 규칙을 처음부터 정의할 수도 있습니다:

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌습니다. 따라서 [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)에서 제공하는 모든 규칙을 활용하여 코드 스타일 문제를 수정할 수 있습니다.

<a name="excluding-files-or-folders"></a>
### 파일 / 폴더 제외하기 (Excluding Files / Folders)

기본적으로 Pint는 프로젝트 내 모든 `.php` 파일을 검사하지만 `vendor` 디렉터리 내 파일은 제외합니다. 추가로 제외하고 싶은 폴더가 있다면 `exclude` 설정 옵션을 사용하세요:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 포함하는 모든 파일을 제외하려면 `notName` 설정 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

특정 파일을 정확한 경로로 지정해 제외하려면 `notPath` 설정 옵션을 이용하세요:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 지속적 통합 (Continuous Integration)

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Laravel Pint로 프로젝트의 린트를 자동화하려면, 새로운 코드가 GitHub에 푸시될 때 Pint가 실행되도록 [GitHub Actions](https://github.com/features/actions)를 설정할 수 있습니다. 먼저 GitHub에서 **Settings > Actions > General > Workflow permissions** 메뉴로 가서 워크플로에 "읽기 및 쓰기 권한(Read and write permissions)"을 부여하세요. 그런 다음 `.github/workflows/lint.yml` 파일을 다음 내용으로 생성합니다:

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