# Laravel Pint

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일/폴더 제외하기](#excluding-files-or-folders)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 주관적인 PHP 코드 스타일 자동 수정 도구입니다. Pint는 PHP-CS-Fixer 위에 구축되었으며, 코드 스타일을 깔끔하고 일관되게 유지할 수 있도록 간편하게 만들어줍니다.

Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되므로 즉시 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이, Laravel의 주관적인 코딩 스타일을 따라 코드 스타일 이슈를 자동으로 수정합니다.

<a name="installation"></a>
## 설치

Pint는 최신 버전의 Laravel 프레임워크에 기본 포함되어 있으므로 별도의 설치가 필요하지 않습니다. 하지만 기존(구버전) 애플리케이션의 경우, Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기

`pint` 바이너리를 프로젝트의 `vendor/bin` 디렉터리에서 실행하여 코드 스타일 이슈를 자동으로 수정할 수 있습니다:

```shell
./vendor/bin/pint
```

특정 파일이나 디렉터리만 대상으로 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트된 모든 파일의 목록을 상세하게 출력합니다. Pint의 변경 내역을 좀 더 자세히 확인하려면, `-v` 옵션을 이용할 수 있습니다:

```shell
./vendor/bin/pint -v
```

파일을 실제로 수정하지 않고 스타일 에러만 점검하고 싶다면, `--test` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --test
```

Git에서 커밋되지 않은 변경 사항이 있는 파일만 수정하고 싶다면, `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

<a name="configuring-pint"></a>
## Pint 설정하기

앞서 언급했듯이, Pint는 별도의 설정 없이 사용할 수 있습니다. 그러나 프리셋, 규칙, 검사할 폴더 등 맞춤 설정을 원한다면, 프로젝트 루트 디렉터리에 `pint.json` 파일을 만들어 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리에 위치한 `pint.json` 설정을 사용하고 싶을 경우, Pint 실행 시 `--config` 옵션을 지정할 수 있습니다:

```shell
pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋

프리셋은 코드 스타일 이슈를 수정할 때 사용할 규칙들의 집합을 정의합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여, Laravel의 주관적인 코딩 스타일에 따라 이슈를 수정합니다. 다른 프리셋을 사용하고 싶다면, Pint 실행 시 `--preset` 옵션을 지정할 수 있습니다:

```shell
pint --preset psr12
```

원한다면, 프로젝트의 `pint.json` 파일에서 프리셋을 설정할 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

Pint에서 현재 지원하는 프리셋은 다음과 같습니다: `laravel`, `per`, `psr12`, `symfony`.

<a name="rules"></a>
### 규칙

규칙은 Pint가 코드 스타일 이슈를 수정할 때 따르는 스타일 지침입니다. 앞서 언급했듯이, 프리셋은 여러 규칙을 미리 정의해 놓은 집합이므로 대부분의 PHP 프로젝트에서는 개별 규칙을 신경 쓸 필요가 없습니다.

하지만, 원한다면 `pint.json` 파일에서 특정 규칙을 활성화 또는 비활성화할 수 있습니다:

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

Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 합니다. 따라서, PHP-CS-Fixer의 모든 규칙을 프로젝트에 적용할 수 있습니다: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외하기

기본적으로 Pint는 `vendor` 디렉터리를 제외한 프로젝트 내 모든 `.php` 파일을 검사합니다. 추가로 제외하고 싶은 폴더가 있다면, `exclude` 설정 옵션을 사용할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴이 포함된 모든 파일을 제외하고 싶다면, `notName` 설정 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

파일의 정확한 경로를 지정해 제외하고 싶다면, `notPath` 옵션을 사용할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```