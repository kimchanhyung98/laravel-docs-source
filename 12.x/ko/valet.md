# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 제공](#serving-sites)
    - ["Park" 명령어](#the-park-command)
    - ["Link" 명령어](#the-link-command)
    - [TLS로 사이트 보안 강화하기](#securing-sites)
    - [기본 사이트 제공](#serving-a-default-site)
    - [사이트별 PHP 버전 설정](#per-site-php-versions)
- [사이트 공유](#sharing-sites)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉토리 및 파일](#valet-directories-and-files)
    - [디스크 접근 권한](#disk-access)

<a name="introduction"></a>
## 소개

> [!NOTE]
> macOS 또는 Windows에서 Laravel 애플리케이션 개발을 더욱 쉽게 할 수 있는 방법을 찾고 계신가요? [Laravel Herd](https://herd.laravel.com)를 확인해보세요. Herd는 Valet, PHP, Composer 등 Laravel 개발에 필요한 모든 것을 포함하고 있습니다.

[Laravel Valet](https://github.com/laravel/valet)은 macOS 미니멀리스트를 위한 개발 환경입니다. Laravel Valet은 Mac이 시작될 때마다 백그라운드에서 항상 [Nginx](https://www.nginx.com/)가 실행되도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해 `*.test` 도메인으로의 모든 요청을 로컬에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7MB의 RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/{{version}}/sail)이나 [Homestead](/docs/{{version}}/homestead)의 완전한 대체품은 아니지만, 유연하면서도 빠른 기본 환경이 필요하거나 메모리가 제한된 머신을 사용하는 경우에 좋은 대안이 될 수 있습니다.

Valet은 기본적으로 다음과 같은 프레임워크를 지원합니다(이에 국한되지 않음):

<style>
    #valet-support > ul {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        line-height: 1.9;
    }
</style>

<div id="valet-support" markdown="1">

- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- 정적 HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

또한 [커스텀 드라이버](#custom-valet-drivers)를 통해 Valet을 확장할 수 있습니다.

<a name="installation"></a>
## 설치

> [!WARNING]
> Valet은 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx가 로컬 머신의 80번 포트에 바인딩되어 있지 않은지 확인하세요.

우선 Homebrew를 최신 상태로 업데이트합니다:

```shell
brew update
```

다음으로, Homebrew를 사용해 PHP를 설치합니다:

```shell
brew install php
```

PHP 설치 후, [Composer 패키지 관리자](https://getcomposer.org)를 설치할 준비가 됩니다. 또한, `$HOME/.composer/vendor/bin` 디렉토리가 시스템 "PATH"에 포함되어 있는지 확인하세요. Composer 설치가 끝나면, Laravel Valet을 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로 Valet의 `install` 명령어를 실행하세요. 이 명령은 Valet과 DnsMasq를 설정 및 설치합니다. 또한, Valet이 의존하는 데몬들이 시스템 시작 시 자동으로 실행되도록 설정됩니다:

```shell
valet install
```

Valet 설치가 완료되면, 터미널에서 `ping foobar.test`와 같이 어떠한 `*.test` 도메인에 핑을 보내보세요. 설치가 정상적으로 완료되었다면 해당 도메인이 `127.0.0.1`로 응답하는 것을 확인할 수 있습니다.

Valet은 머신이 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

> [!NOTE]
> 글로벌 PHP 버전을 수정하는 대신, `isolate` [명령어](#per-site-php-versions)를 통해 사이트별 PHP 버전을 지정할 수 있습니다.

Valet에서는 `valet use php@버전` 명령어로 PHP 버전을 전환할 수 있습니다. Homebrew를 통해 해당 PHP 버전이 설치되어 있지 않다면 Valet이 자동으로 설치해줍니다:

```shell
valet use php@8.2

valet use php
```

프로젝트의 루트에 `.valetrc` 파일을 생성하고, 해당 파일에 사이트가 사용할 PHP 버전을 명시할 수도 있습니다:

```shell
php=php@8.2
```

이 파일이 생성된 후에는 단순히 `valet use` 명령어를 실행하여 Valet이 파일을 읽어 사이트에 적합한 PHP 버전을 자동으로 적용합니다.

> [!WARNING]
> 여러 PHP 버전이 설치되어 있더라도, Valet은 한 번에 하나의 PHP 버전만 서비스를 제공합니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요한 경우, [DBngin](https://dbngin.com)을 확인해보세요. MySQL, PostgreSQL, Redis를 포함하는 무료 통합 DB 관리 도구입니다. DBngin 설치 후에는 `127.0.0.1`에서 `root` 사용자명과 비밀번호 없이 데이터베이스에 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet 설치가 원활히 동작하지 않으면, `composer global require laravel/valet` 명령 다음에 `valet install`을 실행해 설치를 재설정할 수 있습니다. 드물게, `valet uninstall --force`를 실행 후, 다시 `valet install`로 "강제 초기화"가 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet` 명령어를 실행하여 Valet을 최신 버전으로 업그레이드할 수 있습니다. 업그레이드 후에는 환경 설정 파일 등을 추가로 업그레이드 할 필요가 있을 수 있으니 `valet install` 명령을 실행하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드

Valet 3에서 4로 업그레이드하는 경우, 아래 단계들을 따라주세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전을 위해 `.valetphprc` 파일을 추가했다면, 각각 `.valetrc`로 이름을 바꾸고, 기존 내용 앞에 `php=`를 추가하세요.
- 모든 커스텀 드라이버를 새 드라이버 시스템의 네임스페이스, 확장자, 타입 힌트, 반환 타입에 맞게 업데이트하세요. 예시는 Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)를 참고하세요.
- PHP 7.1~7.4를 사용 중이더라도, Homebrew로 PHP 8.0 이상 버전도 함께 설치해야 합니다. Valet의 일부 스크립트는 기본 연결 버전이 아니더라도 해당 버전을 사용합니다.

</div>

<a name="serving-sites"></a>
## 사이트 제공

Valet 설치가 끝나면, 이제 Laravel 애플리케이션을 서비스할 수 있습니다. Valet은 애플리케이션 제공을 위해 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 머신에 애플리케이션이 들어있는 디렉토리를 등록합니다. 해당 디렉토리가 "park"되면, 그 안의 모든 하위 디렉토리는 `http://<directory-name>.test`로 웹 브라우저에서 접근할 수 있습니다:

```shell
cd ~/Sites

valet park
```

이제 "park"된 디렉토리 내부에 생성하는 모든 애플리케이션은 자동으로 `http://<디렉토리명>.test` 패턴으로 서비스됩니다. 예를 들어, "laravel"이라는 디렉토리가 있다면 `http://laravel.test`에서 접근할 수 있습니다. 또한, Valet은 와일드카드 서브도메인(`http://foo.laravel.test`) 접근도 자동으로 허용합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 디렉토리 전체가 아닌, 한 개의 사이트(프로젝트)만 개별적으로 서비스하고 싶을 때 사용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령으로 애플리케이션을 Valet에 등록했다면, 그 디렉토리명으로 접근할 수 있습니다. 즉, 위 예제에서는 `http://laravel.test`에서 접근이 가능합니다. 와일드카드 서브도메인 (`http://foo.laravel.test`)도 자동 지원됩니다.

다른 호스트네임으로 서비스하고 싶으면, `link` 명령어에 호스트네임을 인자로 넘길 수 있습니다. 예)

```shell
cd ~/Sites/laravel

valet link application
```

서브도메인으로도 연결할 수 있습니다:

```shell
valet link api.application
```

연결된 모든 디렉토리는 `links` 명령어로 확인할 수 있습니다:

```shell
valet links
```

사이트의 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용하세요:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 강화하기

Valet은 기본적으로 HTTP로 사이트를 제공합니다. 하지만, 암호화된 HTTP/2 및 TLS로 제공하고 싶다면 `secure` 명령어를 사용하세요. 예를 들어, `laravel.test` 도메인으로 서비스 중인 경우 아래처럼 실행합니다:

```shell
valet secure laravel
```

사이트의 보안을 해제하고 다시 HTTP로 돌아가고 싶다면 `unsecure` 명령어를 사용하세요. `secure`와 마찬가지로 호스트네임을 인자로 넘기면 됩니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 제공

알 수 없는 `test` 도메인 접근 시 `404` 대신 "기본" 사이트를 서비스하고 싶을 수 있습니다. 이럴 땐 `~/.config/valet/config.json` 설정 파일에 `default` 옵션을 추가하고, 기본 사이트의 경로를 지정하세요:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전 설정

기본적으로 Valet은 글로벌 PHP 설치된 버전을 사용합니다. 하지만 여러 사이트별로 각기 다른 PHP 버전이 필요하다면, `isolate` 명령어로 특정 사이트에 사용할 PHP 버전을 지정할 수 있습니다. `isolate` 명령은 현재 디렉토리의 사이트에 대해 설정합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트명이 디렉토리명과 다를 경우, `--site` 옵션을 사용해 명시할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

편의를 위해 다음 명령어로 현재 사이트의 PHP CLI 또는 도구를 프록시하여 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

`isolated` 명령으로 모든 "격리"된 사이트와 각 사이트의 PHP 버전을 확인할 수 있습니다:

```shell
valet isolated
```

사이트를 다시 Valet의 기본(글로벌) PHP 버전으로 돌리고 싶다면 해당 사이트 루트에서 `unisolate` 명령을 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유

Valet에는 모바일 기기나 팀원, 클라이언트와 사이트를 간편히 테스트 및 공유할 수 있는 명령어가 포함되어 있습니다.

Valet은 기본적으로 ngrok 또는 Expose를 통해 사이트 공유를 지원합니다. 사이트를 공유하기 전에 `share-tool` 명령으로 `ngrok`, `expose`, `cloudflared` 중 사용할 도구를 지정하세요:

```shell
valet share-tool ngrok
```

선택한 도구가 아직 설치되어 있지 않다면 (ngrok/clouldflared의 경우 Homebrew, Expose의 경우 Composer를 통해), Valet이 자동으로 설치를 안내합니다. 사이트 공유를 시작하기 전에 각각 ngrok이나 Expose 계정으로 인증해야 합니다.

사이트를 공유하려면, 터미널에서 해당 사이트 디렉토리로 이동 후 `share` 명령을 실행하세요. 그러면 공개 접근이 가능한 URL이 클립보드에 복사되어 바로 붙여넣기(브라우저 등 공유)할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중지하려면 `Control + C`를 누르세요.

> [!WARNING]
> 만약 커스텀 DNS 서버(예: `1.1.1.1`)를 사용 중이라면 ngrok 공유가 제대로 동작하지 않을 수 있습니다. 이 경우 맥 시스템 설정 → 네트워크 → 고급 → DNS 탭에서, `127.0.0.1`을 첫 번째 DNS 서버로 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok을 통한 사이트 공유

ngrok으로 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup) 및 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 인증 토큰을 받은 후, Valet 설정에 해당 토큰을 적용하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> `valet share --region=eu` 등과 같이 추가 ngrok 파라미터를 넘길 수 있습니다. 자세한 내용은 [ngrok 공식 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose를 통한 사이트 공유

Expose로 사이트를 공유하려면 [Expose 계정 생성](https://expose.dev/register) 및 [인증 토큰을 통한 인증](https://expose.dev/docs/getting-started/getting-your-token)이 필요합니다.

지원되는 추가 커맨드라인 파라미터 등 자세한 내용은 [Expose 공식 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

Valet은 기본적으로 개발 머신이 인터넷에 노출되어 보안 위협에 노출되지 않도록 내부 `127.0.0.1` 인터페이스의 트래픽만 허용합니다.

다른 로컬 네트워크 디바이스에서 머신의 IP(예: `192.168.1.10/application.test`)로 Valet 사이트에 접근하고 싶다면, 해당 사이트의 Nginx 설정 파일에서 포트 80, 443의 `listen` 지시어에서 `127.0.0.1:`를 제거해야 합니다.

`valet secure`를 실행하지 않은 경우(HTTP만 사용하는 경우), `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정하세요. HTTPS로 서비스 중인 경우(즉, `valet secure`를 실행한 경우)는 `~/.config/valet/Nginx/app-name.test` 파일을 수정하세요.

설정을 변경한 후, `valet restart` 명령을 실행해 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

일부 프레임워크 기반 애플리케이션은 서버 환경 변수에 의존하지만, 프로젝트 내에서 직접 지정하는 방법을 제공하지 않을 수 있습니다. Valet은 프로젝트 루트에 `.valet-env.php` 파일을 추가하여 사이트별 환경 변수를 지정할 수 있습니다. 이 파일은 각 사이트/환경 변수 쌍의 배열을 반환해야 하며, 지정된 각 사이트에 글로벌 `$_SERVER` 배열에 추가됩니다:

```php
<?php

return [
    // laravel.test 사이트에 대해 $_SERVER['key']를 "value"로 설정 ...
    'laravel' => [
        'key' => 'value',
    ],

    // 모든 사이트에 대해 $_SERVER['key']를 "value"로 설정 ...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## 서비스 프록시

때때로 Valet 도메인을 로컬 머신의 다른 서비스로 프록시하고 싶을 수 있습니다. 예를 들어, Valet을 사용하면서 동시에 Docker에서 다른 사이트를 띄워야 할 경우가 있습니다. 하지만 Valet과 Docker는 동시에 80번 포트를 사용할 수 없습니다.

이때, `proxy` 명령어로 프록시 설정을 만들 수 있습니다. 다음 예시는 모든 `http://elasticsearch.test` 트래픽을 `http://127.0.0.1:9200`로 프록시합니다:

```shell
# HTTP 프록시 ...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2 프록시 ...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 제거하려면 `unproxy` 명령어를 사용하세요:

```shell
valet unproxy elasticsearch
```

프록시된 모든 사이트 구성을 확인하려면 `proxies` 명령어를 실행하세요:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버

Valet이 기본적으로 지원하지 않는 프레임워크나 CMS의 PHP 애플리케이션을 서비스하고 싶다면 "드라이버"를 직접 작성할 수 있습니다. Valet 설치 시 `~/.config/valet/Drivers` 디렉토리에 `SampleValetDriver.php`가 생성되며, 커스텀 드라이버 작성 예제가 포함되어 있습니다. 커스텀 드라이버는 `serves`, `isStaticFile`, `frontControllerPath` 세 가지 메서드만 구현하면 됩니다.

이 세 메서드는 모두 `$sitePath`, `$siteName`, `$uri`를 인자로 받습니다. `$sitePath`는 사이트의 전체 경로(예: `/Users/Lisa/Sites/my-project`), `$siteName`은 도메인의 "호스트"/"사이트 이름"(`my-project`), `$uri`는 요청 URI(`/foo/bar`)입니다.

커스텀 드라이버 구현이 끝나면, `FrameworkValetDriver.php` 패턴(예: WordPress의 경우 `WordPressValetDriver.php`)으로 `~/.config/valet/Drivers`에 저장합니다.

각 메서드 예제를 살펴보겠습니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 해당 드라이버가 해당 요청을 처리해야 하는지 여부를 `true` 또는 `false`로 반환해야 합니다. 즉, 현재 `$sitePath`가 드라이버가 지원하는 프로젝트인지 확인하는 로직입니다.

예를 들어, WordPress 드라이버를 작성한다면 아래와 같을 수 있습니다:

```php
/**
 * 이 드라이버가 요청을 처리하는지 여부를 결정
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile`은 요청이 이미지, 스타일시트 등 "정적" 파일에 대한 것인지 확인합니다. 정적 파일일 경우, 해당 파일의 경로를 반환하고, 아니면 `false`를 반환합니다:

```php
/**
 * 들어오는 요청이 정적 파일인지 판단
 *
 * @return string|false
 */
public function isStaticFile(string $sitePath, string $siteName, string $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```

> [!WARNING]
> `isStaticFile` 메서드는 `serves`가 `true`를 반환하고, 요청 URI가 `/`가 아닐 때에만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath`는 애플리케이션의 "프론트 컨트롤러"(`index.php` 등)에 대한 전체 경로를 반환해야 합니다:

```php
/**
 * 애플리케이션 프론트 컨트롤러의 전체 경로 반환
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### 로컬 드라이버

단일 애플리케이션에 대해 커스텀 Valet 드라이버를 지정하려면, 애플리케이션 루트 디렉토리에 `LocalValetDriver.php` 파일을 만드세요. 이 때, 기본 `ValetDriver` 클래스나 특정 애플리케이션용 드라이버(예: `LaravelValetDriver`)를 상속할 수 있습니다:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * 이 드라이버가 요청을 처리하는지 여부를 결정
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * 애플리케이션 프론트 컨트롤러의 전체 경로 반환
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
## 기타 Valet 명령어

<div class="overflow-auto">

| 명령어 | 설명 |
| --- | --- |
| `valet list` | 모든 Valet 명령어 목록을 표시 |
| `valet diagnose` | Valet 문제 해결을 위한 진단 정보를 출력 |
| `valet directory-listing` | 디렉토리 나열 동작을 설정. 기본값은 "off"로, 디렉토리 접근 시 404 페이지 표시 |
| `valet forget` | 현재 "park"된 디렉토리에서 실행 시 목록에서 해당 디렉토리 제거 |
| `valet log` | Valet 서비스에서 기록한 로그 목록을 확인 |
| `valet paths` | "park"된 모든 경로 확인 |
| `valet restart` | Valet 데몬 재시작 |
| `valet start` | Valet 데몬 시작 |
| `valet stop` | Valet 데몬 중지 |
| `valet trust` | Brew 및 Valet 명령어 실행 시 암호 입력 없이 실행할 수 있도록 sudoers 파일 추가 |
| `valet uninstall` | Valet 제거: 수동 제거 방법 안내. `--force` 옵션을 주면 모든 리소스를 강제로 삭제 |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉토리 및 파일

Valet 환경에서 문제 해결 시 아래 디렉토리 및 파일 정보를 참고하세요:

#### `~/.config/valet`

Valet의 모든 설정 파일이 저장됩니다. 이 디렉토리를 백업하는 것이 좋습니다.

#### `~/.config/valet/dnsmasq.d/`

DNSMasq의 설정 파일이 저장됩니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버가 저장됩니다. 각 프레임워크/CMS의 서비스 방식을 결정합니다.

#### `~/.config/valet/Nginx/`

Valet이 관리하는 모든 Nginx 사이트 설정 파일이 저장됩니다. `install` 또는 `secure` 명령 실행 시 이 파일들이 재생성됩니다.

#### `~/.config/valet/Sites/`

[link 명령어](#the-link-command)로 연결된 프로젝트의 심볼릭 링크가 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 마스터 구성 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx에서 사용하는 PHP-FPM 소켓입니다. PHP가 정상 동작할 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류에 대한 사용자 로그입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류에 대한 사용자 로그입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 오류에 대한 시스템 로그입니다.

#### `/usr/local/var/log/nginx`

Nginx의 접근 및 에러 로그 디렉토리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

각종 PHP 설정(`*.ini`) 파일이 저장됩니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트의 SSL 인증서 생성을 위해 사용되는 기본 Nginx 설정 파일입니다.

<a name="disk-access"></a>
### 디스크 접근 권한

macOS 10.14 버전부터 [특정 파일 및 디렉토리에 대한 접근이 기본적으로 제한](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)됩니다. 이에는 데스크탑, 문서, 다운로드 디렉토리가 포함됩니다. 또한 네트워크 드라이브와 외장 저장장치 접근도 제한됩니다. 따라서, Valet에서는 사이트 폴더를 이 보호된 위치 외부에 두는 것을 권장합니다.

하지만 이러한 위치에서 사이트를 서비스하려면, Nginx에 "전체 디스크 접근(Full Disk Access)" 권한을 부여해야 합니다. 그렇지 않으면 정적 에셋 서빙 등에서 서버 오류나 예기치 못한 동작이 발생할 수 있습니다. 일반적으로 macOS에서 자동으로 권한 요청이 뜨지만, 수동으로도 `시스템 환경설정` > `보안 및 개인정보 보호` > `개인정보 보호`에서 `전체 디스크 접근` 항목에 들어가, 좌측에서 `nginx` 엔트리를 메인 창에서 활성화하면 됩니다.