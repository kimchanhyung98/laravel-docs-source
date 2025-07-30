# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 구성하기](#configuring-pint)
    - [프리셋](#presets)
    - [룰](#rules)
    - [파일 / 폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 의견이 명확한 PHP 코드 스타일 자동 수정기입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으며, 코드 스타일을 깔끔하고 일관되게 유지하는 작업을 간편하게 수행할 수 있게 해줍니다.

Pint는 모든 새 Laravel 애플리케이션과 함께 자동으로 설치되므로 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정이 필요 없으며, Laravel의 의견이 명확한 코딩 스타일을 따라 코드 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 Laravel 프레임워크 최신 버전에 기본 포함되어 있어 보통 별도의 설치가 필요하지 않습니다. 다만, 오래된 애플리케이션의 경우 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

`vendor/bin` 디렉토리에 있는 `pint` 실행 파일을 호출하여 코드 스타일 문제를 수정하도록 Pint를 실행할 수 있습니다:

```shell
./vendor/bin/pint
```

성능 향상을 위한 병렬 실행(실험적)을 원한다면 `--parallel` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --parallel
```

특정 파일이나 디렉토리만 대상으로 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 수정한 모든 파일 목록을 자세히 보여줍니다. 더 세부적인 변경 내용을 확인하려면 `-v` 옵션을 붙여 실행하세요:

```shell
./vendor/bin/pint -v
```

단순히 스타일 오류를 검사만 하고 실제 파일은 변경하지 않으려면 `--test` 옵션을 사용하세요. 스타일 오류가 발견되면 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git 기준으로 특정 브랜치와 다른 파일만 수정하고 싶다면 `--diff=[branch]` 옵션을 사용하세요. 이는 GitHub Actions 같은 CI 환경에서 새로 추가되거나 수정된 파일만 검사하여 시간을 절약하는 데 유용합니다:

```shell
./vendor/bin/pint --diff=main
```

커밋되지 않은 변경사항이 있는 파일만 고치려면 `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

수정 작업을 수행하되, 만약 오류가 수정되었다면 0이 아닌 종료 코드를 반환하도록 하려면 `--repair` 옵션을 사용하세요:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 구성하기 (Configuring Pint)

앞서 언급한 대로 Pint는 기본적으로 설정 없이도 작동합니다. 하지만 프리셋, 룰, 검사할 폴더를 사용자 정의하고 싶다면 프로젝트 루트 디렉토리에 `pint.json` 파일을 생성하여 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

특정 경로에 있는 `pint.json`을 사용하려면 Pint 실행 시 `--config` 옵션에 파일 경로를 지정하세요:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋 (Presets)

프리셋은 코드 스타일 문제를 수정하기 위해 적용할 룰 세트를 정의합니다. 기본적으로 Pint는 Laravel의 의견이 명확한 코딩 스타일을 따르는 `laravel` 프리셋을 사용합니다. 그러나 `--preset` 옵션을 통해 다른 프리셋을 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

또는 프로젝트의 `pint.json` 파일에 지정할 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

현재 Pint가 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, 그리고 `empty`입니다.

<a name="rules"></a>
### 룰 (Rules)

룰은 Pint가 코드 스타일 문제를 수정할 때 적용하는 스타일 가이드입니다. 앞서 말했듯 프리셋은 대부분의 PHP 프로젝트에 적합하게 미리 정의된 룰 모음이므로, 별도로 룰을 신경 쓸 필요가 없습니다.

하지만 원하는 경우 `pint.json` 파일에서 특정 룰을 활성화하거나 비활성화할 수 있으며, `empty` 프리셋을 사용해 룰을 처음부터 직접 정의할 수도 있습니다:

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 하므로, PHP CS Fixer에서 지원하는 모든 룰을 사용할 수 있습니다: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일 / 폴더 제외하기 (Excluding Files / Folders)

기본적으로 Pint는 프로젝트 내 `vendor` 디렉토리를 제외한 모든 `.php` 파일을 검사합니다. 추가로 제외할 폴더가 있다면 `exclude` 설정을 통해 지정할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 포함하는 파일을 모두 제외하고 싶다면 `notName` 설정에 패턴을 추가하세요:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로를 지정해 특정 파일만 제외하려면 `notPath` 설정을 사용합니다:

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

Laravel Pint로 프로젝트 린팅을 자동화하려면, GitHub에 새 코드를 푸시할 때마다 Pint가 실행되도록 [GitHub Actions](https://github.com/features/actions)를 설정할 수 있습니다. 먼저 GitHub에서 **Settings > Actions > General > Workflow permissions**에 들어가 워크플로우에 "읽기 및 쓰기 권한(Read and write permissions)"을 부여해야 합니다. 그 후 `.github/workflows/lint.yml` 파일을 다음 내용과 같이 생성하세요:

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