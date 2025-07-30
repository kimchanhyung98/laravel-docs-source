# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)는 최소주의자를 위한 의견이 반영된 PHP 코드 스타일 수정기입니다. Pint는 PHP-CS-Fixer 위에 구축되어, 코드 스타일을 깔끔하고 일관되게 유지하는 것을 간단하게 만들어 줍니다.

Pint는 새 Laravel 애플리케이션과 함께 자동으로 설치되며, 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이 Laravel의 의견이 반영된 코딩 스타일을 따라 코드 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 최근 Laravel 프레임워크 버전에 포함되어 있어 보통 별도의 설치가 필요 없습니다. 다만, 이전 버전 프로젝트에서는 다음과 같이 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

프로젝트의 `vendor/bin` 디렉토리에 있는 `pint` 바이너리를 실행하여 Pint가 코드 스타일 문제를 수정하도록 할 수 있습니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉토리에 대해 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 수정한 모든 파일 목록을 상세하게 보여줍니다. 수정 내역을 더 구체적으로 보고 싶다면 Pint 실행 시 `-v` 옵션을 추가하세요:

```shell
./vendor/bin/pint -v
```

파일을 실제로 변경하지 않고 스타일 오류만 검사하려면 `--test` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --test
```

Git 기준으로 커밋되지 않은 변경 사항이 있는 파일만 수정하고 싶다면 `--dirty` 옵션을 사용하세요:

```shell
./vendor/bin/pint --dirty
```

<a name="configuring-pint"></a>
## Pint 설정하기 (Configuring Pint)

앞서 언급했듯, Pint는 기본적으로 별도의 설정 없이 사용 가능합니다. 하지만 프리셋, 규칙, 검사할 폴더 등을 커스터마이징하고 싶다면 프로젝트 루트에 `pint.json` 파일을 만들어 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한 특정 디렉토리에 있는 `pint.json`을 사용하고 싶다면, Pint 실행 시 `--config` 옵션으로 설정 파일 경로를 지정할 수 있습니다:

```shell
pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋 (Presets)

프리셋은 코드 스타일 문제를 해결하기 위해 사용할 규칙 집합을 정의합니다. 기본적으로 Pint는 Laravel의 의견이 반영된 코딩 스타일을 따르는 `laravel` 프리셋을 사용합니다. 하지만 `--preset` 옵션으로 다른 프리셋을 지정할 수도 있습니다:

```shell
pint --preset psr12
```

프로젝트의 `pint.json` 파일에서도 프리셋을 설정할 수 있습니다:

```json
{
    "preset": "psr12"
}
```

현재 Pint에서 지원하는 프리셋은 `laravel`, `psr12`, `symfony`입니다.

<a name="rules"></a>
### 규칙 (Rules)

규칙은 Pint가 코드 스타일 문제를 수정할 때 적용하는 스타일 가이드입니다. 앞서 설명한 프리셋은 대부분의 PHP 프로젝트에 적합한 규칙 모음으로, 개별 규칙에 신경 쓸 필요는 없습니다.

하지만 필요하다면 `pint.json` 파일에서 특정 규칙을 활성화하거나 비활성화할 수 있습니다:

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

Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌기 때문에, PHP-CS-Fixer의 모든 규칙을 사용해 코드 스타일 문제를 해결할 수 있습니다: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기 (Excluding Files / Folders)

기본적으로 Pint는 `vendor` 디렉토리를 제외한 프로젝트 내 모든 `.php` 파일을 검사합니다. 추가로 제외할 폴더가 있다면 `exclude` 옵션을 통해 설정할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴이 포함된 파일을 모두 제외하고 싶다면 `notName` 옵션을 사용할 수도 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

또는 정확한 경로를 지정해 파일을 제외할 때는 `notPath` 옵션을 사용하세요:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```