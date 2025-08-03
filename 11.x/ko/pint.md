# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [룰](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 의견 기반 PHP 코드 스타일 자동 수정기입니다. Pint는 PHP-CS-Fixer 위에 구축되었으며, 코드 스타일을 깔끔하고 일관되게 유지하는 것을 쉽게 만들어 줍니다.

Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되어 바로 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 Laravel의 의견 기반 코딩 스타일을 따르며 코드 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 Laravel 프레임워크의 최신 버전에 기본 포함되어 있어 별도의 설치가 보통 필요하지 않습니다. 하지만, 오래된 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

`vendor/bin` 디렉터리에 있는 `pint` 실행 파일을 호출하여 코드 스타일 문제를 수정하도록 Pint를 실행할 수 있습니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉터리에서 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 수정한 모든 파일 목록을 자세히 보여줍니다. 더 상세한 변경 사항을 확인하고 싶다면 `-v` 옵션을 추가하여 실행하세요:

```shell
./vendor/bin/pint -v
```

파일을 실제로 수정하지 않고 코드 스타일 오류를 검사만 하려면 `--test` 옵션을 사용할 수 있습니다. 오류가 발견되면 Pint가 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git 기준 특정 브랜치와 차이가 있는 파일만 수정하려면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이를 CI 환경(GitHub Actions 등)에서 새로 추가되거나 변경된 파일만 검사해 시간을 절약할 때 활용할 수 있습니다:

```shell
./vendor/bin/pint --diff=main
```

커밋되지 않은 변경사항이 있는 파일만 수정하려면 `--dirty` 옵션을 사용하세요:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 모두 수정하되, 오류를 수정한 경우 0이 아닌 종료 코드도 반환하려면 `--repair` 옵션을 사용하세요:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기 (Configuring Pint)

앞서 말한 바와 같이 Pint는 설정이 없어도 동작합니다. 하지만 프리셋, 룰, 검사할 폴더를 커스터마이즈하고자 하면 프로젝트 루트 경로에 `pint.json` 파일을 만들어 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리의 `pint.json`을 사용하고 싶으면 Pint 실행 시 `--config` 옵션을 지정할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋 (Presets)

프리셋은 코드 스타일 문제를 수정하기 위해 사용할 규칙 집합을 정의합니다. 기본값은 Laravel의 의견 기반 코딩 스타일을 따르는 `laravel` 프리셋입니다. 하지만 `--preset` 옵션으로 다른 프리셋을 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

프로젝트의 `pint.json`에도 프리셋을 설정할 수 있습니다:

```json
{
    "preset": "psr12"
}
```

Pint가 현재 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty`입니다.

<a name="rules"></a>
### 룰 (Rules)

룰은 Pint가 코드 스타일 문제를 수정할 때 참고하는 스타일 가이드라인입니다. 위에서 언급했듯이 프리셋은 대부분의 PHP 프로젝트에 적합하도록 미리 정의된 룰 그룹이므로 보통은 개별 룰을 직접 다룰 필요가 없습니다.

하지만 원한다면 `pint.json`에서 특정 룰을 활성화하거나 비활성화할 수 있습니다. 또는 `empty` 프리셋을 사용해 룰을 처음부터 직접 정의할 수도 있습니다:

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

Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌습니다. 따라서 프로젝트의 코드 스타일 문제를 수정하기 위해 PHP-CS-Fixer의 룰을 모두 사용할 수 있습니다: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기 (Excluding Files / Folders)

기본적으로 Pint는 프로젝트 내 모든 `.php` 파일을 검사하지만 `vendor` 디렉터리 내 파일은 제외합니다. 추가로 제외할 폴더가 있다면 `exclude` 설정을 사용할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

파일명 패턴에 따라 모든 해당 파일을 제외하려면 `notName` 설정을 사용하세요:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로를 지정해 특정 파일을 제외하려면 `notPath` 설정을 사용합니다:

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

Laravel Pint로 자동 검사(lint)를 실행하려면, [GitHub Actions](https://github.com/features/actions)를 구성해 GitHub에 새로운 코드가 푸시될 때마다 Pint가 실행되도록 할 수 있습니다. 먼저 GitHub에서 **Settings > Actions > General > Workflow permissions**로 가서 워크플로우에 "읽기 및 쓰기 권한(Read and write permissions)"이 부여되어 있는지 확인하세요. 그 다음 `.github/workflows/lint.yml` 파일을 아래와 같이 만듭니다:

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