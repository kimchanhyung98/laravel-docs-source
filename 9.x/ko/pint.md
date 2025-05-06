# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 구성하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 Laravel의 의견이 반영된 PHP 코드 스타일 자동 정리 도구입니다. Pint는 PHP-CS-Fixer 위에 구축되었으며, 코드 스타일을 깔끔하고 일관되게 유지하는 것을 매우 간단하게 만들어줍니다.

Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되어 있어 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 Laravel의 권장 코드 스타일에 따라 코드 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
## 설치

Pint는 최신 Laravel 프레임워크 릴리즈에 포함되어 있으므로, 일반적으로 별도의 설치가 필요하지 않습니다. 그러나 구버전 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기

프로젝트의 `vendor/bin` 디렉토리에 있는 `pint` 바이너리를 실행하여 코드 스타일 문제를 자동으로 수정할 수 있습니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉터리에 대해서만 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트한 모든 파일의 상세 목록을 표시합니다. 더 자세한 변경 내역을 확인하려면 Pint 실행 시 `-v` 옵션을 추가할 수 있습니다:

```shell
./vendor/bin/pint -v
```

파일을 실제로 변경하지 않고 코드 스타일 오류만 검사하고 싶다면 `--test` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --test
```

Git에서 커밋되지 않은 변경이 있는 파일만 수정하고 싶을 때는 `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

<a name="configuring-pint"></a>
## Pint 구성하기

앞서 언급한 것처럼, Pint는 별도의 설정이 필요 없습니다. 그러나 프리셋, 규칙, 검사할 폴더 등을 사용자 정의하고 싶다면, 프로젝트의 루트 디렉터리에 `pint.json` 파일을 생성하여 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리의 `pint.json`을 사용하고 싶다면 Pint 실행 시 `--config` 옵션을 지정할 수 있습니다:

```shell
pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋

프리셋은 코드 스타일 문제를 고치기 위한 규칙 세트를 정의합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하며, Laravel의 권장 코드 스타일에 따라 문제를 수정합니다. 하지만 `--preset` 옵션으로 다른 프리셋을 지정할 수도 있습니다:

```shell
pint --preset psr12
```

원한다면 프로젝트의 `pint.json` 파일에서도 프리셋을 지정할 수 있습니다:

```json
{
    "preset": "psr12"
}
```

Pint에서 현재 지원하는 프리셋은: `laravel`, `psr12`, `symfony`입니다.

<a name="rules"></a>
### 규칙

규칙은 Pint가 코드 스타일 문제를 수정할 때 적용하는 스타일 가이드라인입니다. 앞서 언급했듯이, 프리셋은 일반적으로 PHP 프로젝트에 적합한 사전 정의된 규칙 모음이므로, 개별 규칙을 직접 설정하지 않아도 됩니다.

하지만 필요하다면, `pint.json` 파일에서 특정 규칙을 활성화 또는 비활성화할 수 있습니다:

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

Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌기 때문에, PHP-CS-Fixer의 모든 규칙도 사용할 수 있습니다: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기

기본적으로 Pint는 `vendor` 디렉터리를 제외한 모든 `.php` 파일을 검사합니다. 더 많은 폴더를 제외하고 싶다면, `exclude` 설정 옵션을 사용할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 포함하는 모든 파일을 제외하고 싶다면, `notName` 설정 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로로 파일을 지정하여 제외하고 싶다면, `notPath` 설정 옵션을 사용할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```