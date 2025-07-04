# 라라벨 Pint (Laravel Pint)

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일 / 폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합(CI)](#continuous-integration)
    - [GitHub Actions에서 테스트 실행](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[라라벨 Pint](https://github.com/laravel/pint)는 미니멀리스트 개발자를 위한 라라벨의 권장 PHP 코드 스타일 자동화 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으며, 여러분의 코드 스타일을 깔끔하고 일관되게 관리할 수 있도록 돕습니다.

Pint는 최신 라라벨 애플리케이션에 기본으로 포함되어 있어서, 별도의 설치 없이 바로 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이도 작동하며, 라라벨에서 권장하는 코드 스타일을 자동으로 적용하여 코드 스타일 문제를 해결합니다.

<a name="installation"></a>
## 설치

Pint는 최근 버전의 라라벨 프레임워크에 포함되어 있으므로, 보통은 별도의 설치가 필요하지 않습니다. 하지만 이전 버전의 애플리케이션이라면 Composer를 통해 라라벨 Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기

프로젝트의 `vendor/bin` 디렉토리에 있는 `pint` 바이너리를 실행하면 코드 스타일 문제를 자동으로 수정할 수 있습니다.

```shell
./vendor/bin/pint
```

더 나은 성능을 위해 Pint를 병렬 모드(실험적)로 실행하고 싶다면 `--parallel` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --parallel
```

특정 파일이나 디렉터리에만 Pint를 적용하고 싶다면 다음과 같이 지정할 수 있습니다.

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 수정된 모든 파일의 목록을 자세하게 보여줍니다. 보다 상세한 변경 내역을 확인하고 싶다면 Pint 실행 시 `-v` 옵션을 추가할 수 있습니다.

```shell
./vendor/bin/pint -v
```

실제 파일을 변경하지 않고 코드 스타일 오류만 검사하고 싶다면 `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다.

```shell
./vendor/bin/pint --test
```

Git을 기준으로 지정한 브랜치와 비교하여 변경된 파일만 Pint가 수정하도록 하려면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이 기능은 GitHub Actions와 같은 CI 환경에서 새로운 파일이나 수정된 파일만 검사할 때 유용합니다.

```shell
./vendor/bin/pint --diff=main
```

Git에서 커밋되지 않은 변경이 있는 파일만 Pint로 검사하고 싶다면 `--dirty` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --dirty
```

코드 스타일 문제를 가진 파일을 수정하되, 문제가 실제로 수정되었을 때 0이 아닌 종료 코드로 바로 종료하고 싶다면 `--repair` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기

앞서 언급했듯이, 기본적으로 Pint는 별도의 구성이 필요 없습니다. 하지만 프리셋, 규칙 또는 검사할 폴더 등을 원하는 대로 커스터마이즈하고 싶다면, 프로젝트 루트 디렉터리에 `pint.json` 파일을 만들어 설정할 수 있습니다.

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리에 있는 `pint.json` 파일을 사용하고 싶다면 Pint 실행 시 `--config` 옵션으로 경로를 지정할 수 있습니다.

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋

프리셋은 코드 스타일 문제를 자동으로 수정해주는 규칙 묶음입니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여 라라벨의 권장 스타일을 따릅니다. 하지만 원한다면 `--preset` 옵션을 통해 다른 프리셋을 지정해 Pint를 실행할 수 있습니다.

```shell
./vendor/bin/pint --preset psr12
```

또는, 프로젝트의 `pint.json` 파일에서 프리셋을 설정할 수도 있습니다.

```json
{
    "preset": "psr12"
}
```

현재 Pint에서 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty` 입니다.

<a name="rules"></a>
### 규칙

규칙은 Pint가 코드 스타일을 고칠 때 기준이 되는 세부 스타일 가이드입니다. 앞에서 설명했듯이, 프리셋은 대부분의 PHP 프로젝트에 적합하도록 미리 묶여있는 규칙 집합이므로, 일반적으로는 각 규칙을 직접 관리할 필요가 없습니다.

하지만 필요하다면, `pint.json` 파일에서 특정 규칙을 개별적으로 활성화하거나 비활성화할 수 있고, `empty` 프리셋을 사용하여 규칙을 처음부터 직접 정의할 수도 있습니다.

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 동작하기 때문에, PHP CS Fixer에서 제공하는 모든 규칙을 사용할 수 있습니다. 자세한 규칙 목록은 [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)에서 확인할 수 있습니다.

<a name="excluding-files-or-folders"></a>
### 파일 / 폴더 제외하기

기본적으로 Pint는 `vendor` 디렉터리를 제외한 모든 `.php` 파일을 검사합니다. 추가로 제외하고 싶은 폴더가 있다면 `exclude` 설정 옵션을 활용합니다.

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 가진 파일을 모두 제외하고 싶을 때는 `notName` 설정 옵션을 사용할 수 있습니다.

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로로 개별 파일을 지정해서 제외하려면 `notPath` 설정 옵션을 사용하면 됩니다.

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
### GitHub Actions에서 테스트 실행

프로젝트의 코드 스타일 자동 점검을 자동화하려면, [GitHub Actions](https://github.com/features/actions)를 통해 코드가 GitHub로 푸시될 때마다 Pint를 실행할 수 있습니다. 먼저, GitHub의 **Settings > Actions > General > Workflow permissions** 메뉴에서 워크플로에 "Read and write permissions" 권한을 부여하세요. 그런 다음, 아래와 같은 내용을 담은 `.github/workflows/lint.yml` 파일을 생성합니다.

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