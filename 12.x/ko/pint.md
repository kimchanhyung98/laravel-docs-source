# 라라벨 핀트 (Laravel Pint)

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [룰](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합(CI)](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 의견이 반영된(Opinionated) PHP 코드 스타일 자동 수정 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 하며, 코드 스타일을 깔끔하고 일관되게 유지할 수 있도록 돕습니다.

Pint는 모든 신규 Laravel 애플리케이션에 자동으로 설치되어 있으므로 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 Laravel의 의견이 반영된 코딩 스타일을 따라 코드 스타일 이슈를 자동으로 수정합니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 최근 버전의 Laravel 프레임워크에 기본 내장되어 있어 별도의 설치가 필요하지 않습니다. 하지만 구 버전 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다.

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

Pint로 코드 스타일 이슈를 자동으로 수정하려면, 프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 실행 파일을 사용하면 됩니다.

```shell
./vendor/bin/pint
```

향상된 성능을 위해 Pint를 병렬(parallel) 모드(실험적)로 실행하려면 `--parallel` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --parallel
```

병렬 모드에서는 `--max-processes` 옵션을 통해 실행할 최대 프로세스 수를 지정할 수 있습니다. 해당 옵션을 지정하지 않으면 Pint는 사용 가능한 모든 코어를 사용합니다.

```shell
./vendor/bin/pint --parallel --max-processes=4
```

특정 파일이나 디렉터리만 Pint로 검사하고 싶다면 아래와 같이 실행할 수 있습니다.

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트된 모든 파일의 목록을 자세하게 보여줍니다. 변경 내역에 대해 더 상세한 정보를 확인하려면, Pint 실행 시 `-v` 옵션을 추가하세요.

```shell
./vendor/bin/pint -v
```

파일을 실제로 수정하지 않고 스타일 오류만 검사하고 싶다면, `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다.

```shell
./vendor/bin/pint --test
```

Git과 연동하여 특정 브랜치와 다르게 변경된 파일만 수정하고 싶다면, `--diff=[branch]` 옵션을 사용할 수 있습니다. 이 옵션은 GitHub Actions와 같은 CI 환경에서 새로운 파일이나 수정된 파일만 검사할 때 유용합니다.

```shell
./vendor/bin/pint --diff=main
```

Git에서 커밋하지 않은 변경 사항이 있는 파일만 수정하고 싶다면, `--dirty` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 수정하면서, 오류가 실제로 수정된 경우 0이 아닌 종료 코드로 종료하고 싶다면, `--repair` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기 (Configuring Pint)

앞서 설명했듯이 Pint는 별도의 설정 없이도 동작합니다. 하지만 프리셋, 룰, 검사할 폴더 등을 커스터마이즈하고 싶다면, 프로젝트 루트에 `pint.json` 파일을 생성하여 지정할 수 있습니다.

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리의 `pint.json`을 사용하고 싶을 때는 Pint 실행 시 `--config` 옵션으로 설정 파일 경로를 지정할 수 있습니다.

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋 (Presets)

프리셋(Preset)은 코드 스타일 문제를 수정할 때 사용할 일련의 룰을 정의합니다. 기본적으로 Pint는 Laravel의 의견이 반영된 코딩 스타일을 따르는 `laravel` 프리셋을 사용합니다. 다른 프리셋을 사용하려면 Pint 실행 시 `--preset` 옵션으로 지정할 수 있습니다.

```shell
./vendor/bin/pint --preset psr12
```

원한다면, 프로젝트의 `pint.json` 파일에서도 프리셋을 지정할 수 있습니다.

```json
{
    "preset": "psr12"
}
```

Pint에서 현재 지원하는 프리셋은 다음과 같습니다: `laravel`, `per`, `psr12`, `symfony`, `empty`.

<a name="rules"></a>
### 룰 (Rules)

룰(Rule)은 Pint가 코드 스타일을 수정할 때 따르는 세부 지침입니다. 앞서 언급한 프리셋은 일반적으로 PHP 프로젝트에 적합하도록 여러 룰을 미리 묶어 둔 것이므로, 대부분의 경우 개별 룰을 신경 쓸 필요가 없습니다.

하지만 필요하다면, `pint.json` 파일에서 특정 룰을 직접 활성화하거나 비활성화할 수 있고, 또는 `empty` 프리셋을 사용해 완전히 사용자 정의 룰만으로 설정할 수도 있습니다.

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) 위에서 동작하므로, PHP CS Fixer의 모든 룰을 적용할 수 있습니다. 보다 다양한 룰 목록과 설정법은 [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)에서 확인할 수 있습니다.

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기 (Excluding Files / Folders)

기본적으로 Pint는 `vendor` 디렉터리를 제외하고 프로젝트 내의 모든 `.php` 파일을 검사합니다. 추가적으로 더 많은 폴더를 제외하고 싶을 경우 `exclude` 옵션을 설정할 수 있습니다.

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴이 포함된 모든 파일을 제외하고 싶다면, `notName` 옵션을 사용할 수 있습니다.

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로를 지정하여 특정 파일을 제외하고 싶을 때는, `notPath` 옵션을 사용할 수 있습니다.

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
### GitHub Actions

Laravel Pint로 프로젝트의 린팅(linting)을 자동화하려면, [GitHub Actions](https://github.com/features/actions)를 구성하여 코드가 새로 푸시될 때마다 Pint가 실행되도록 만들 수 있습니다. 먼저, GitHub 내 **Settings > Actions > General > Workflow permissions**에서 워크플로우에 "Read and write permissions" 권한을 부여해야 합니다. 그런 다음, 아래와 같이 `.github/workflows/lint.yml` 파일을 생성하세요.

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
