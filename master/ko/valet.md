# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 서비스](#serving-sites)
    - [`park` 명령어](#the-park-command)
    - [`link` 명령어](#the-link-command)
    - [TLS로 사이트 보안 설정](#securing-sites)
    - [기본 사이트 서비스](#serving-a-default-site)
    - [사이트별 PHP 버전 설정](#per-site-php-versions)
- [사이트 공유](#sharing-sites)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시 설정](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉토리 및 파일](#valet-directories-and-files)
    - [디스크 접근](#disk-access)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> macOS 또는 Windows에서 Laravel 애플리케이션을 더욱 쉽게 개발하고 싶으신가요? [Laravel Herd](https://herd.laravel.com)를 확인해 보세요. Herd는 Valet, PHP, Composer를 포함하여 Laravel 개발에 필요한 모든 것을 제공합니다.

[Laravel Valet](https://github.com/laravel/valet)는 macOS를 사용하는 미니멀리스트 개발자들을 위한 개발 환경입니다. Laravel Valet는 macOS 기계가 시작될 때 항상 백그라운드에서 [Nginx](https://www.nginx.com/)를 실행하도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 `*.test` 도메인으로 들어오는 모든 요청을 로컬 머신에 설치된 사이트로 프록시합니다.

즉, Valet는 약 7MB의 메모리를 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet는 [Sail](/docs/master/sail)이나 [Homestead](/docs/master/homestead)를 완전히 대체하지는 않지만, 기본 환경을 유연하게 다루고 싶거나, 속도가 매우 중요하거나, 메모리가 제한된 기계에서 작업할 때 훌륭한 대안입니다.

기본적으로 Valet는 다음과 같은 환경을 지원하지만 이에 국한되지 않습니다:

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
- Static HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

또한, Valet는 여러분만의 [커스텀 드라이버](#custom-valet-drivers)로 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Valet는 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx 같은 다른 프로그램이 로컬 머신의 80번 포트를 사용 중이지 않은지 확인해 주세요.

시작하려면 먼저 Homebrew가 최신 상태인지 `update` 명령어로 확인하세요:

```shell
brew update
```

다음으로 Homebrew를 사용해 PHP를 설치합니다:

```shell
brew install php
```

PHP가 설치되면 [Composer 패키지 매니저](https://getcomposer.org)를 설치할 준비가 된 것입니다. 또한 `$HOME/.composer/vendor/bin` 디렉토리가 시스템의 `PATH`에 포함되어 있는지 확인하세요. Composer를 설치한 후, Laravel Valet를 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로 Valet의 `install` 명령어를 실행하세요. 이 명령은 Valet와 DnsMasq를 설정 및 설치하며, Valet가 의존하는 데몬들을 시스템 시작 시 자동 실행하도록 구성합니다:

```shell
valet install
```

설치가 완료되면 터미널에서 `ping foobar.test` 같은 명령어로 임의의 `*.test` 도메인에 핑을 시도해 보세요. Valet가 정상적으로 설치되어 있다면 `127.0.0.1`에서 응답하는 것을 확인할 수 있습니다.

Valet는 기계가 부팅될 때마다 필요한 서비스들을 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

> [!NOTE]
> 글로벌 PHP 버전을 변경하는 대신, `isolate` [명령어](#per-site-php-versions)를 사용해 사이트별 PHP 버전을 지정할 수 있습니다.

Valet는 `valet use php@version` 명령어를 통해 PHP 버전을 전환할 수 있게 해줍니다. 만약 지정한 PHP 버전이 설치되어 있지 않으면 Homebrew가 자동으로 설치해 줍니다:

```shell
valet use php@8.2

valet use php
```

또한 프로젝트 루트에 `.valetrc` 파일을 만들어 해당 사이트가 사용할 PHP 버전을 지정할 수 있습니다:

```shell
php=php@8.2
```

이 파일이 생성되면 단순히 `valet use` 명령어를 실행하면 Valet가 파일의 내용을 읽어 사이트에 적합한 PHP 버전을 사용합니다.

> [!WARNING]
> Valet는 한 번에 하나의 PHP 버전만 서비스할 수 있습니다. 여러 버전이 설치되어 있더라도 동시에 사용할 수 없습니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요하다면, MySQL, PostgreSQL, Redis를 한 번에 관리할 수 있는 무료 도구인 [DBngin](https://dbngin.com)을 확인해 보세요. DBngin 설치 후에는 `127.0.0.1`에 `root` 사용자명과 빈 문자열의 비밀번호로 데이터베이스에 연결할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet가 제대로 작동하지 않을 경우, `composer global require laravel/valet` 명령어를 다시 실행한 뒤 `valet install` 명령어를 수행하면 설치가 재설정되어 여러 문제를 해결할 수 있습니다. 아주 드문 경우에는 `valet uninstall --force`를 강제 실행하고 다시 `valet install`을 실행하는 "하드 리셋"이 필요할 수 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet` 명령어를 실행해 Valet를 업데이트할 수 있습니다. 업그레이드 후에는 꼭 `valet install` 명령어도 실행하여 구성이 필요한 부분을 최신 상태로 적용하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드하기

Valet 3에서 Valet 4로 업그레이드하는 경우, 아래 단계를 따라 올바르게 업그레이드를 진행하세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전을 설정하는 `.valetphprc` 파일이 있다면, 각 파일 이름을 `.valetrc`로 변경하세요. 그리고 파일 내용 앞에 `php=`를 추가해 주세요.
- 커스텀 드라이버가 있다면 새 드라이버 시스템의 네임스페이스, 확장자, 타입 힌트 및 반환 타입 힌트를 반영하도록 업데이트해야 합니다. [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) 예제를 참고하세요.
- PHP 7.1 ~ 7.4 버전을 사용하여 사이트를 제공한다면, Valet가 일부 스크립트를 실행할 때는 Homebrew로 설치한 PHP 8.0 이상 버전을 함께 설치하여 사용해야 함을 유의하세요.

</div>

<a name="serving-sites"></a>
## 사이트 서비스 (Serving Sites)

Valet 설치가 완료되면 Laravel 애플리케이션을 서비스할 준비가 된 것입니다. Valet는 앱을 서비스할 때 사용할 수 있는 두 가지 명령어를 제공합니다: `park`와 `link`.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션이 위치한 디렉토리를 등록합니다. 한번 디렉토리를 `park` 하면, 그 안의 모든 하위 디렉토리는 브라우저에서 `http://<디렉토리명>.test` 형식으로 접근 가능해집니다:

```shell
cd ~/Sites

valet park
```

이게 전부입니다. 이제 'park'한 디렉토리 내에 있는 모든 앱은 `http://<디렉토리명>.test` 규칙에 따라 자동으로 서비스됩니다. 예를 들어 "laravel"이라는 디렉토리가 있으면, `http://laravel.test`로 접속할 수 있습니다. 또한, Valet는 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 허용합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 특정 디렉토리 내 단일 사이트만 서비스하고 싶을 때 사용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 Valet에 연결한 앱은 디렉토리명으로 접근 가능합니다. 위 예제에서 연결한 "laravel" 사이트는 `http://laravel.test`로 접속할 수 있습니다. 또한 이 명령어 역시 와일드카드 서브도메인(`http://foo.laravel.test`) 접근을 자동으로 지원합니다.

다른 호스트명으로 서비스하려면 `link` 명령어에 원하는 호스트명을 인수로 넘기면 됩니다. 예를 들어, `http://application.test`로 서비스를 하려면 다음과 같이 실행하세요:

```shell
cd ~/Sites/laravel

valet link application
```

물론 서브도메인도 가능합니다:

```shell
valet link api.application
```

현재 연결된 모든 디렉토리를 보려면, `links` 명령어를 실행하세요:

```shell
valet links
```

사이트에 대한 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용합니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 설정 (Securing Sites With TLS)

기본적으로 Valet는 HTTP를 통해 사이트를 서비스합니다. 그러나 HTTP/2를 지원하는 암호화된 TLS로 사이트를 제공하려면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인에서 서비스 중인 사이트를 안전하게 만들려면 다음 명령어를 실행하세요:

```shell
valet secure laravel
```

사이트를 비보안 상태(HTTP)로 되돌리려면 `unsecure` 명령어를 실행하면 됩니다. `secure` 명령어와 마찬가지로 호스트명을 인수로 받습니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 서비스 (Serving a Default Site)

알 수 없는 `test` 도메인을 접속했을 때 기본적으로 `404`가 뜨지만, 특정 사이트를 "기본(default)" 사이트로 서비스하고 싶을 때가 있습니다. 이 경우 `~/.config/valet/config.json` 설정 파일에 `default` 옵션을 추가하고 기본 사이트의 경로를 지정하세요:

```
"default": "/Users/Sally/Sites/example-site",
```

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전 설정 (Per-Site PHP Versions)

Valet는 기본적으로 글로벌 PHP 설치 버전을 사용해 사이트를 제공합니다. 그러나 사이트마다 다른 PHP 버전을 사용해야 할 경우 `isolate` 명령어로 특정 사이트에 PHP 버전을 지정할 수 있습니다. `isolate`는 현재 작업 중인 디렉토리의 사이트에 설정을 적용합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

프로젝트명과 디렉토리명이 다를 경우 `--site` 옵션을 사용해 명시할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

편리하게도, `valet php`, `valet composer`, `valet which-php` 명령어는 사이트별 PHP 설정에 맞춰 필요한 CLI 도구 호출을 프록시해 줍니다:

```shell
valet php
valet composer
valet which-php
```

현재 고립된 사이트들과 PHP 버전 목록을 보려면 `isolated` 명령어를 실행하세요:

```shell
valet isolated
```

사이트를 다시 글로벌 PHP 버전으로 되돌리려면 해당 사이트 루트에서 `unisolate` 명령어를 실행합니다:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유 (Sharing Sites)

Valet는 로컬 사이트를 외부에 쉽게 공유할 수 있는 명령어를 제공합니다. 모바일 기기나 팀원, 고객과 사이트를 간편히 테스트하거나 공유할 때 유용합니다.

Valet는 기본적으로 ngrok와 Expose를 지원합니다. 사이트 공유에 앞서 `share-tool` 명령어를 사용해 공유 도구를 `ngrok` 또는 `expose`로 설정하세요:

```shell
valet share-tool ngrok
```

선택한 도구가 Homebrew(ngrok) 또는 Composer(Expose)를 통해 설치되어 있지 않다면 Valet가 자동으로 설치를 유도합니다. 물론 두 도구 모두 계정을 인증해야 사이트 공유가 가능합니다.

사이트 디렉토리로 이동한 후 `share` 명령어를 실행하면, 공개 가능한 URL이 클립보드에 복사되어 바로 브라우저에 붙여넣거나 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중단하려면 `Control + C`를 누르세요.

> [!WARNING]
> 커스텀 DNS 서버(예: `1.1.1.1`)를 사용 중이라면 ngrok 공유가 제대로 작동하지 않을 수 있습니다. 이 경우 macOS 시스템 설정 > 네트워크 > 고급 > DNS 탭으로 가서 가장 먼저 DNS 서버로 `127.0.0.1`을 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### ngrok로 사이트 공유하기

ngrok를 사용하려면 [ngrok 계정을 생성](https://dashboard.ngrok.com/signup)하고 [인증 토큰을 설정](https://dashboard.ngrok.com/get-started/your-authtoken)해야 합니다. 인증 토큰을 얻었으면 다음 명령어로 Valet 설정에 추가하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> `valet share --region=eu` 등의 추가 ngrok 파라미터를 전달할 수 있습니다. 자세한 내용은 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose로 사이트 공유하기

Expose로 사이트를 공유하려면 [Expose 계정을 생성](https://expose.dev/register)하고 [인증 토큰으로 인증](https://expose.dev/docs/getting-started/getting-your-token)해야 합니다.

추가 명령행 파라미터에 관해선 [Expose 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유 (Sharing Sites on Your Local Network)

기본적으로 Valet는 내부 `127.0.0.1` 인터페이스에서만 트래픽을 받도록 제한하여 개발 머신이 인터넷 위험에 노출되지 않게 합니다.

로컬 네트워크 내 다른 기기에서 머신 IP(`192.168.1.10/application.test` 등)로 접근하려면, 해당 사이트의 Nginx 설정 파일에서 `listen` 지시어에 있는 `127.0.0.1:` 접두사를 제거해야 합니다. 80번과 443번 포트 모두 적용하세요.

만약 `valet secure` 명령어를 실행하지 않았다면 `/usr/local/etc/nginx/valet/valet.conf`를 수정하여 HTTPS를 사용하지 않는 모든 사이트에 대해 네트워크 접근을 열 수 있습니다. 그러나 HTTPS로 서비스 중이라면(즉, `valet secure`를 수행했다면) `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

Nginx 설정 수정 후에는 `valet restart` 명령어로 변경 사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수 (Site Specific Environment Variables)

다른 프레임워크를 사용하는 일부 애플리케이션은 서버 환경 변수에 의존하지만 프로젝트 내에서 이를 설정할 방법을 제공하지 않을 수 있습니다. Valet는 각 사이트별 환경 변수를 `.valet-env.php` 파일을 프로젝트 루트에 추가하여 설정할 수 있도록 지원합니다. 이 파일은 사이트 및 환경 변수 쌍의 배열을 반환하며, 배열에 명시된 변수들은 해당 사이트의 글로벌 `$_SERVER` 배열에 추가됩니다:

```php
<?php

return [
    // laravel.test 사이트에서 $_SERVER['key'] 값을 "value"로 설정...
    'laravel' => [
        'key' => 'value',
    ],

    // 모든 사이트에 대해 $_SERVER['key'] 값을 "value"로 설정...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## 서비스 프록시 설정 (Proxying Services)

때로는 Valet 도메인을 로컬 머신의 다른 서비스에 프록시해야 할 때가 있습니다. 예를 들어, Docker로 별도 사이트를 실행하면서 Valet도 함께 실행해야 하는 상황에서 둘 다 동시에 80번 포트에 바인딩할 수 없을 때입니다.

이럴 때는 `proxy` 명령어를 사용해 프록시를 생성할 수 있습니다. 예를 들어, `http://elasticsearch.test`로 들어오는 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하려면 다음과 같이 입력하세요:

```shell
# HTTP 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 삭제하려면 `unproxy` 명령어를 사용합니다:

```shell
valet unproxy elasticsearch
```

현재 설정된 모든 프록시 사이트 구성을 보려면 `proxies` 명령어를 실행하세요:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버 (Custom Valet Drivers)

Valet가 기본 지원하지 않는 프레임워크나 CMS로 구동되는 PHP 애플리케이션을 서비스하려면 직접 Valet "드라이버"를 작성할 수 있습니다. Valet 설치 시 `~/.config/valet/Drivers` 디렉토리가 생성되며, 여기에는 샘플 드라이버 구현 (`SampleValetDriver.php`) 파일이 포함되어 있습니다. 이 파일은 커스텀 드라이버를 작성하는 방법을 보여줍니다.

드라이버 작성 시, 반드시 세 가지 메서드 `serves`, `isStaticFile`, `frontControllerPath`를 구현해야 합니다.

세 메서드 모두 `$sitePath`, `$siteName`, `$uri` 인수를 받습니다. `$sitePath`는 `/Users/Lisa/Sites/my-project` 같은 머신 상의 사이트 절대 경로이고, `$siteName`은 도메인의 "호스트"/"사이트명" 부분(`my-project`)이며, `$uri`는 들어오는 요청 URI(`/foo/bar`)입니다.

커스텀 Valet 드라이버를 완성했으면, `~/.config/valet/Drivers` 폴더에 `FrameworkValetDriver.php` 형식으로 저장하세요. 예를 들어 WordPress용 드라이버라면 `WordPressValetDriver.php`로 파일명을 지정하면 됩니다.

다음은 커스텀 Valet 드라이버가 반드시 구현해야 하는 메서드 샘플입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 현재 요청을 해당 드라이버가 처리할지 여부를 `true` 또는 `false`로 반환합니다. 이 메서드 안에서 주어진 `$sitePath`가 해당 프로젝트 유형인지 판단하면 됩니다.

예를 들어, `WordPressValetDriver`의 `serves` 메서드는 다음과 같을 수 있습니다:

```php
/**
 * Determine if the driver serves the request.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile` 메서드는 요청된 URI가 이미지, 스타일시트 등 "정적" 파일인지 판단합니다. 정적 파일이면 완전한 디스크 경로를 반환하고, 아니라면 `false`를 반환해야 합니다:

```php
/**
 * Determine if the incoming request is for a static file.
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
> `isStaticFile` 메서드는 `serves` 메서드가 `true`를 반환하고 요청 URI가 `/`가 아닌 경우에만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러" 즉, 보통 `index.php` 파일의 절대 경로를 반환해야 합니다:

```php
/**
 * Get the fully resolved path to the application's front controller.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### 로컬 드라이버 (Local Drivers)

특정 애플리케이션에 대해서만 커스텀 Valet 드라이버를 정의하고 싶다면, 애플리케이션 루트에 `LocalValetDriver.php` 파일을 생성하세요. 이 커스텀 드라이버는 기본 `ValetDriver` 클래스를 상속하거나, `LaravelValetDriver` 같은 기존 앱 전용 드라이버를 확장할 수 있습니다:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
## 기타 Valet 명령어 (Other Valet Commands)

<div class="overflow-auto">

| 명령어 | 설명 |
| --- | --- |
| `valet list` | Valet가 제공하는 모든 명령어 목록 출력 |
| `valet diagnose` | Valet 디버깅에 도움이 되는 진단 정보 출력 |
| `valet directory-listing` | 디렉토리 목록 표시 동작 결정. 기본값은 "off"로 디렉토리 접근 시 404 페이지 출력 |
| `valet forget` | "park"한 디렉토리에서 실행하여 해당 디렉토리를 관리 목록에서 제거 |
| `valet log` | Valet 서비스가 기록한 로그 목록 확인 |
| `valet paths` | "park"한 모든 경로 확인 |
| `valet restart` | Valet 데몬 재시작 |
| `valet start` | Valet 데몬 시작 |
| `valet stop` | Valet 데몬 정지 |
| `valet trust` | Brew 및 Valet 명령어를 비밀번호 입력 없이 실행할 수 있도록 sudoers 파일 추가 |
| `valet uninstall` | Valet 제거: 수동 제거 방법 안내. `--force` 옵션을 사용하면 Valet 관련 모든 리소스를 강제 삭제 |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉토리 및 파일 (Valet Directories and Files)

Valet 환경 문제를 해결할 때 아래 디렉토리 및 파일 정보가 도움이 될 수 있습니다:

#### `~/.config/valet`

Valet 설정 파일들이 위치한 디렉토리입니다. 백업을 유지하는 것이 좋습니다.

#### `~/.config/valet/dnsmasq.d/`

DnsMasq 구성 파일이 들어있는 디렉토리입니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버가 위치하는 디렉토리입니다. 드라이버는 특정 프레임워크/CMS가 어떻게 서비스되는지 결정합니다.

#### `~/.config/valet/Nginx/`

Valet의 모든 Nginx 사이트 설정 파일들이 위치합니다. `install` 및 `secure` 명령어 실행 시 재생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)의 모든 심볼릭 링크가 저장되어 있습니다.

#### `~/.config/valet/config.json`

Valet의 주요 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx에서 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 에러 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 에러 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 액세스 및 에러 로그 디렉토리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

다양한 PHP 설정을 위한 `*.ini` 파일이 위치한 디렉토리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트 SSL 인증서 구성 시 기본 Nginx 설정에 사용됩니다.

<a name="disk-access"></a>
### 디스크 접근 (Disk Access)

macOS 10.14 이상부터는 [일부 파일 및 디렉토리 접근이 기본적으로 제한됩니다](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). 이 제한 대상에는 데스크톱, 문서, 다운로드 폴더 등이 포함되며 네트워크 및 외장 볼륨 접근도 제한됩니다. 따라서, Valet는 사이트 폴더를 이러한 보호 대상 위치 외부에 두는 것을 권장합니다.

그럼에도 불구하고 보호된 위치에서 사이트를 서비스하려면 Nginx에 "전체 디스크 접근 권한"을 부여해야 합니다. 그렇지 않으면 정적 자산 서비스 시 서버 오류나 예기치 않은 문제가 발생할 수 있습니다. 보통 macOS가 자동으로 Nginx에 권한을 요청하지만, 수동으로 설정하려면 `시스템 환경설정 > 보안 및 개인 정보 보호 > 개인 정보 보호`에서 `전체 디스크 접근`을 선택한 후, 메인창에서 `nginx` 관련 항목을 활성화하세요.