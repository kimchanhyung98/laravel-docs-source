# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 구성하기](#configuring-pint)
    - [프리셋(Presets)](#presets)
    - [규칙(Rules)](#rules)
    - [파일 및 폴더 제외하기](#excluding-files-or-folders)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)은 미니멀리스트를 위한 의견이 강한 PHP 코드 스타일 수정 도구입니다. Pint는 PHP-CS-Fixer 위에 구축되었으며, 코드 스타일을 깔끔하고 일관되게 유지하는 작업을 쉽게 합니다.

Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되므로 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정이 필요 없으며 Laravel의 의견이 반영된 코딩 스타일에 따라 코드 스타일 문제를 수정합니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 최근 Laravel 프레임워크 버전에 기본 포함되어 있어 별도의 설치가 보통 필요하지 않습니다. 그러나 구버전 애플리케이션의 경우, Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 실행해 Pint에게 코드 스타일 문제를 수정하도록 지시할 수 있습니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉터리에서만 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 수정한 모든 파일을 상세히 표시합니다. Pint가 적용한 변경 사항을 더 자세히 보고 싶다면, 호출 시 `-v` 옵션을 추가하세요:

```shell
./vendor/bin/pint -v
```

파일을 변경하지 않고 코드 스타일 오류만 검사하고 싶다면 `--test` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --test
```

Git 기준으로 커밋되지 않은 변경 사항이 있는 파일만 수정하고 싶다면 `--dirty` 옵션을 사용하세요:

```shell
./vendor/bin/pint --dirty
```

<a name="configuring-pint"></a>
## Pint 구성하기 (Configuring Pint)

앞서 언급했듯이 Pint는 별도의 설정 없이도 동작합니다. 하지만 프리셋, 규칙, 검사할 폴더를 커스터마이즈하고 싶다면, 프로젝트 루트에 `pint.json` 파일을 만들어 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리의 `pint.json`을 사용하려면 Pint 실행 시 `--config` 옵션으로 경로를 지정할 수 있습니다:

```shell
pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋 (Presets)

프리셋은 코드 스타일 문제를 수정하기 위한 규칙 집합을 정의합니다. 기본적으로 Pint는 Laravel의 의견이 반영된 코딩 스타일을 따르는 `laravel` 프리셋을 사용합니다. 하지만 `--preset` 옵션으로 다른 프리셋을 지정할 수 있습니다:

```shell
pint --preset psr12
```

원한다면 프로젝트의 `pint.json` 파일 내에 프리셋을 설정할 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

현재 Pint에서 지원하는 프리셋은 `laravel`, `per`, `psr12`, 그리고 `symfony`입니다.

<a name="rules"></a>
### 규칙 (Rules)

규칙은 Pint가 코드 스타일 문제를 고치기 위해 사용하는 스타일 가이드입니다. 위에서 설명한 프리셋은 대부분의 PHP 프로젝트에 적합하도록 미리 정의된 규칙들의 모음이기 때문에, 개별 규칙에 대해서는 신경 쓰지 않아도 됩니다.

하지만 필요에 따라 `pint.json`에서 특정 규칙을 활성화하거나 비활성화할 수 있습니다:

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "braces": false,
        "new_with_braces": {
            "anonymous_class": false,
            "named_class": false
        }
    }
}
```

Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) 위에 구축되어 있기 때문에, PHP-CS-Fixer의 규칙이라면 어떤 것이든 프로젝트 내 코드 스타일 문제 해결에 사용할 수 있습니다: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일 및 폴더 제외하기 (Excluding Files / Folders)

기본적으로 Pint는 프로젝트 내 모든 `.php` 파일을 검사하지만, `vendor` 디렉터리에 있는 파일은 제외합니다. 추가로 제외할 폴더가 있다면 `exclude` 설정 옵션을 사용합니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴이 포함된 모든 파일을 제외하고 싶으면 `notName` 옵션을 사용하세요:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로로 특정 파일을 제외하고 싶을 때는 `notPath` 옵션을 사용합니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```