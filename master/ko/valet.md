# 라라벨 Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 제공](#serving-sites)
    - [“Park” 명령어](#the-park-command)
    - [“Link” 명령어](#the-link-command)
    - [TLS로 사이트 보안 적용](#securing-sites)
    - [기본 사이트 제공](#serving-a-default-site)
    - [사이트별 PHP 버전](#per-site-php-versions)
- [사이트 공유](#sharing-sites)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉터리 및 파일](#valet-directories-and-files)
    - [디스크 접근](#disk-access)

<a name="introduction"></a>
## 소개

> [!참고]
> macOS 또는 Windows에서 라라벨 애플리케이션을 더욱 쉽게 개발할 수 있는 방법을 찾고 계신가요? [Laravel Herd](https://herd.laravel.com)를 확인해보세요. Herd는 Valet, PHP, Composer 등 라라벨 개발에 필요한 모든 것을 포함합니다.

[Laravel Valet](https://github.com/laravel/valet)은 macOS 미니멀리스트를 위한 개발 환경입니다. Valet은 Mac이 부팅될 때마다 [Nginx](https://www.nginx.com/)를 백그라운드에서 항상 실행하도록 구성합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해, `*.test` 도메인에 대한 모든 요청을 로컬에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7MB의 RAM만 사용하는 매우 빠른 라라벨 개발 환경입니다. Valet은 [Sail](/docs/{{version}}/sail)이나 [Homestead](/docs/{{version}}/homestead)를 완전히 대체하지는 않지만, 유연한 기본 환경과 빠른 속도를 선호하거나 제한된 RAM을 가진 기기에서 작업할 때 훌륭한 대안이 됩니다.

Valet은 기본적으로 다음과 같은 프레임워크 및 CMS를 지원합니다(지원 목록이 이에 국한되지는 않습니다):

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

또한 [커스텀 드라이버](#custom-valet-drivers)를 통해 Valet을 확장할 수도 있습니다.

<a name="installation"></a>
## 설치

> [!경고]
> Valet은 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache 또는 Nginx와 같이 로컬 포트 80에 바인딩하는 다른 프로그램이 없는지 확인하세요.

먼저 Homebrew의 최신 상태를 `update` 명령어로 확인하세요:

```shell
brew update
```

그 다음, Homebrew를 이용해 PHP를 설치합니다:

```shell
brew install php
```

PHP 설치가 끝났으면 [Composer 패키지 관리자](https://getcomposer.org)를 설치하세요. 그리고 `$HOME/.composer/vendor/bin` 디렉터리가 시스템 “PATH”에 포함되어 있는지 확인해야 합니다. Composer 설치 후, Laravel Valet을 전역 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로, Valet의 `install` 명령어를 실행하세요. 이 명령어는 Valet과 DnsMasq를 구성 및 설치하며, Valet이 의존하는 데몬을 시스템 시작 시 자동으로 실행하도록 설정합니다:

```shell
valet install
```

Valet 설치가 완료되면, 터미널에서 `ping foobar.test`와 같이 임의의 `*.test` 도메인을 ping 테스트해보세요. Valet이 정상적으로 설치되었다면 해당 도메인에서 `127.0.0.1`으로 응답하는 것을 볼 수 있습니다.

Valet은 컴퓨터 부팅 시마다 필요한 서비스가 자동으로 시작됩니다.

<a name="php-versions"></a>
#### PHP 버전

> [!참고]
> 글로벌 PHP 버전을 직접 수정하는 대신, [사이트별 PHP 버전](#per-site-php-versions)을 `isolate` 명령어로 지정할 수 있습니다.

Valet은 `valet use php@버전` 명령어로 PHP 버전을 변경할 수 있습니다. 해당 버전의 PHP가 설치되어 있지 않다면 Homebrew로 자동 설치합니다:

```shell
valet use php@8.2

valet use php
```

프로젝트 루트에 `.valetrc` 파일을 생성해 사용할 PHP 버전을 지정할 수도 있습니다:

```shell
php=php@8.2
```

이후, `valet use` 명령어를 실행하면, 해당 파일을 읽어 사이트에 맞는 PHP 버전을 사용하게 됩니다.

> [!경고]
> 여러 PHP 버전을 설치했더라도, Valet은 한 번에 하나의 PHP 버전만 제공합니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에서 데이터베이스가 필요하다면, MySQL, PostgreSQL, Redis를 모두 지원하는 무료 통합 데이터베이스 관리 도구 [DBngin](https://dbngin.com)을 추천합니다. DBngin 설치 후에는 `127.0.0.1`에서 `root` 사용자와 비밀번호 없는 상태로 데이터베이스에 연결할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet 설치가 제대로 동작하지 않을 경우, `composer global require laravel/valet` 명령어를 실행한 다음 `valet install`을 재실행하면 설치가 초기화되며 문제를 해결할 수 있습니다. 드물게, `valet uninstall --force` 후 `valet install`을 실행하여 "강제 초기화"가 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet` 명령어로 Valet을 업그레이드할 수 있습니다. 업그레이드 후에는 `valet install` 명령어를 한 번 더 실행하여 필요한 경우 구성 파일에 추가 업그레이드를 적용하세요.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드

Valet 3에서 Valet 4로 업그레이드할 때는 다음 단계를 순서대로 진행하세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전 커스터마이징용 `.valetphprc` 파일이 있다면 `.valetrc`로 이름을 바꾼 후, `php=`를 앞에 붙여주세요.
- 커스텀 드라이버 사용 중이라면, 네임스페이스, 확장자, 타입힌트 및 반환값 타입 등의 새 드라이버 시스템에 맞게 업데이트하세요. 예시는 Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)를 참고하세요.
- 사이트 제공에 PHP 7.1~7.4를 사용한다면, Homebrew를 통해 PHP 8.0 이상 버전도 설치되어 있는지 확인하세요. Valet은 일부 스크립트 실행 시 주 링크된 버전이 아니더라도 8.0 이상 버전을 사용합니다.

</div>

<a name="serving-sites"></a>
## 사이트 제공

Valet 설치가 완료되면 이제 라라벨 애플리케이션을 바로 제공할 수 있습니다. Valet은 `park`와 `link` 두 가지 명령어를 통해 애플리케이션 제공을 돕습니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 여러 애플리케이션이 들어 있는 디렉터리를 등록하는 명령어입니다. 디렉터리가 Valet에 "주차(park)"되면, 그 안에 있는 각 디렉터리들은 웹 브라우저에서 `http://<디렉터리명>.test` 형식으로 접근할 수 있습니다:

```shell
cd ~/Sites

valet park
```

이게 전부입니다. 이제 "주차"된 디렉터리 안에 생성하는 모든 애플리케이션은 자동으로 `http://<디렉터리명>.test` 주소로 제공됩니다. 예를 들어, `laravel`이라는 디렉터리가 있으면, 해당 애플리케이션은 `http://laravel.test`에서 접근할 수 있습니다. 또한, Valet은 와일드카드 서브도메인(`http://foo.laravel.test`)으로도 자동 접근을 허용합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어로 하나의 디렉터리(사이트)만 따로 제공할 수도 있습니다. 전체 디렉터리가 아니라 단일 사이트만 제공할 때 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 Valet에 등록된 애플리케이션은 디렉터리명을 그대로 사용해 접근할 수 있습니다. 위의 예시에서는 `http://laravel.test`로 접근합니다. 또한, 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 활성화됩니다.

다른 호스트명으로 사이트를 제공하고 싶다면 hostname을 `link` 명령어에 인자로 전달합니다. 예를 들어, 애플리케이션을 `http://application.test`에서 제공하려면 다음과 같이 합니다:

```shell
cd ~/Sites/laravel

valet link application
```

물론 `link` 명령어로 서브도메인 사이트 제공도 가능합니다:

```shell
valet link api.application
```

등록된 모든 링크는 `links` 명령어로 확인할 수 있습니다:

```shell
valet links
```

사이트의 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용하세요:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 적용

Valet은 기본적으로 HTTP로 사이트를 제공합니다. 하지만, 암호화된 TLS와 HTTP/2를 사용해 안전하게 서비스를 원한다면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인을 보안 적용하려면:

```shell
valet secure laravel
```

사이트의 보안 적용을 해제해 일반 HTTP로 되돌리고 싶으면 `unsecure` 명령어를 사용합니다. 이때도 도메인명을 인자로 넘깁니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 제공

알 수 없는 `test` 도메인에 접근 시 404 대신 "기본" 사이트를 설정하고 싶다면, `~/.config/valet/config.json` 구성 파일에 기본 사이트 경로를 지정하는 `default` 옵션을 추가하면 됩니다:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

Valet은 기본적으로 시스템 전체의 PHP 버전을 사용하지만, 다양한 사이트별로 서로 다른 PHP 버전을 사용해야 할 때는 `isolate` 명령어로 각 사이트에 맞는 PHP 버전을 지정할 수 있습니다. `isolate` 명령어는 현재 디렉터리의 사이트에 대해 설정합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉터리명과 다르면 `--site` 옵션으로 지정할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

편의를 위해 `valet php`, `composer`, `which-php` 명령어를 통해 각 사이트 설정에 맞는 PHP CLI 또는 도구를 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

등록된 모든 사이트별 PHP 버전 목록은 `isolated` 명령어로 확인할 수 있습니다:

```shell
valet isolated
```

사이트를 전역 Valet PHP 버전으로 되돌리려면, 사이트 루트에서 `unisolate` 명령어를 실행합니다:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유

Valet은 로컬 사이트를 외부와 공유할 수 있는 명령어를 제공하여, 모바일 기기 테스트나 팀원·클라이언트에게 공유할 때 편리합니다.

기본적으로 Valet은 ngrok 또는 Expose를 이용한 사이트 공유를 지원합니다. 먼저 `share-tool` 명령어로 사용할 툴을 `ngrok` 또는 `expose`로 설정하세요:

```shell
valet share-tool ngrok
```

툴이 설치되어 있지 않다면, (ngrok의 경우 Homebrew, Expose의 경우 Composer를 통해) Valet에서 자동으로 설치 안내를 표시합니다. 두 서비스 모두 계정 인증이 필요하니, 공유 전 인증을 완료해주세요.

사이트를 공유하려면 터미널에서 해당 디렉터리로 이동한 뒤 `share` 명령을 실행하세요. 공개용 URL이 클립보드에 복사되어 브라우저나 팀 채팅 등 원하는 곳에 바로 붙여넣어 사용할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중단하려면 `Control + C`를 누르세요.

> [!경고]
> 커스텀 DNS 서버(예: `1.1.1.1`)를 사용하는 경우 ngrok 공유가 제대로 동작하지 않을 수 있습니다. 이런 경우에는 Mac 시스템 설정에서 네트워크로 이동 → 고급 설정 → DNS 탭에서 DNS 서버 목록의 맨 위에 `127.0.0.1`를 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok를 통한 사이트 공유

ngrok를 사용해 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup) 및 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 토큰을 얻은 후 다음과 같이 Valet 구성에 적용합니다:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!참고]
> `valet share --region=eu`처럼 추가 ngrok 파라미터를 share 명령에 전달할 수도 있습니다. 자세한 내용은 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose를 통한 사이트 공유

Expose로 사이트를 공유하려면 [Expose 계정 등록](https://expose.dev/register) 후, [인증 토큰](https://expose.dev/docs/getting-started/getting-your-token)으로 인증해야 합니다.

지원되는 추가 명령행 옵션 등 상세 내용은 [Expose 공식 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

Valet은 기본적으로 개발 머신이 외부 인터넷에 노출되는 것을 막기 위해, 내부 `127.0.0.1` 인터페이스로만 트래픽을 제한합니다.

하지만 동일 네트워크 내 다른 기기에서 Valet 사이트에 IP 주소(예: `192.168.1.10/application.test`)로 접근하고 싶다면, 각 사이트의 Nginx 설정을 직접 수정해야 합니다. 80번, 443번 포트의 `listen` 항목에서 `127.0.0.1:` 프리픽스를 지우세요.

프로젝트에 대해 `valet secure`를 실행하지 않았다면 `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정하면 모든 HTTP 사이트 접근을 허용할 수 있습니다. 이미 HTTPS로 서비스 중(`valet secure` 실행함)이라면 `~/.config/valet/Nginx/app-name.test` 파일을 수정하세요.

설정 변경 후에는 `valet restart`로 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

다른 프레임워크 기반 애플리케이션 중에는 서버 환경 변수에 의존하지만 프로젝트에서 직접 설정할 방법이 없는 경우가 있습니다. Valet은 프로젝트 루트에 `.valet-env.php` 파일을 두어 사이트별 환경 변수 설정을 지원합니다. 이 파일은 사이트/환경변수 쌍의 배열을 반환해야 하며, 각 설정은 해당 사이트의 글로벌 `$_SERVER` 배열에 추가됩니다:

```php
<?php

return [
    // laravel.test 사이트에 대해 $_SERVER['key']를 "value"로 설정...
    'laravel' => [
        'key' => 'value',
    ],

    // 모든 사이트에 대해 $_SERVER['key']를 "value"로 설정...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## 서비스 프록시

가끔 Valet 도메인을 로컬의 다른 서비스로 프록시해야 할 수도 있습니다. 예를 들어, Valet을 실행하면서 동시에 Docker에서 별도의 사이트를 구동해야 할 경우, Valet과 Docker가 포트 80에서 충돌할 수 있습니다.

이때는 `proxy` 명령어로 프록시를 생성할 수 있습니다. 예를 들어, `http://elasticsearch.test` 트래픽을 `http://127.0.0.1:9200`로 모두 프록시하려면:

```shell
# HTTP로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 제거하려면 `unproxy` 명령어를 사용합니다:

```shell
valet unproxy elasticsearch
```

프록시된 사이트 목록은 `proxies` 명령어로 확인할 수 있습니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버

Valet에서 기본적으로 지원하지 않는 프레임워크나 CMS의 PHP 애플리케이션을 제공하고 싶을 때는 직접 Valet “드라이버”를 작성할 수 있습니다. Valet 설치 시 `~/.config/valet/Drivers` 디렉터리가 생성되며, 그 안에 `SampleValetDriver.php` 샘플이 들어 있습니다. 커스텀 드라이버를 작성하려면 `serves`, `isStaticFile`, `frontControllerPath` 세 메서드만 구현하면 됩니다.

이 세 메서드는 모두 `$sitePath`, `$siteName`, `$uri` 값을 인자로 받습니다. `$sitePath`는 머신 내에서 사이트가 위치한 전체 경로(예: `/Users/Lisa/Sites/my-project`), `$siteName`은 도메인의 호스트/사이트명 부분(`my-project`), `$uri`는 요청 URI(`/foo/bar`)를 의미합니다.

작성이 끝난 드라이버는 `~/.config/valet/Drivers`에 `FrameworkValetDriver.php` 형태의 이름으로 두어야 합니다. 예를 들어 워드프레스용 드라이버라면 파일명은 `WordPressValetDriver.php`이어야 합니다.

각 메서드 구현 예시는 다음과 같습니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves`는 드라이버가 이 요청을 처리해야 하면 `true`, 아니면 `false`를 반환해야 합니다. 이 메서드 내부에서 `$sitePath`가 자신이 처리하려는 프로젝트 타입에 해당하는지 판별하세요.

예를 들어 워드프레스 드라이버라면 다음과 같이 구현할 수 있습니다:

```php
/**
 * 드라이버가 요청을 처리하는지 결정합니다.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile`에서는 현재 요청이 이미지, 스타일시트 등 “정적” 파일에 대한 요청인지 판단합니다. 정적 파일이면 파일 전체 경로를 반환하고, 아니면 `false`를 반환합니다:

```php
/**
 * 요청이 정적 파일에 대한 것인지 판별합니다.
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

> [!경고]
> `isStaticFile` 메서드는 `serves`가 `true`를 반환하고, 요청 URI가 `/`가 아닌 경우만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 “프론트 컨트롤러”(보통 index.php)의 전체 경로를 반환해야 합니다:

```php
/**
 * 애플리케이션 프론트 컨트롤러의 전체 경로를 반환합니다.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### 로컬 드라이버

단일 애플리케이션에만 사용할 커스텀 Valet 드라이버를 정의하려면, 해당 애플리케이션 루트에 `LocalValetDriver.php` 파일을 생성하세요. 커스텀 드라이버는 기본 `ValetDriver`를 상속하거나, `LaravelValetDriver`처럼 기존 응용 전용 드라이버를 상속할 수 있습니다:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * 드라이버가 요청을 처리하는지 판별
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
| `valet list` | 모든 Valet 명령어 목록을 표시합니다. |
| `valet diagnose` | Valet 디버깅을 위한 진단 출력을 표시합니다. |
| `valet directory-listing` | 디렉터리 목록 보기 동작 여부를 확인(기본값 "off"로, 디렉터리는 404로 처리). |
| `valet forget` | "주차"된 디렉터리에서 실행 시, 주차 목록에서 제거합니다. |
| `valet log` | Valet 서비스별로 기록된 로그 목록을 확인합니다. |
| `valet paths` | "주차"된 모든 경로를 확인합니다. |
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 정지합니다. |
| `valet trust` | brew와 Valet 명령을 비밀번호 없이 실행할 수 있도록 sudoers 파일을 추가합니다. |
| `valet uninstall` | Valet을 삭제(수동 삭제 안내 표시). `--force` 옵션으로 모든 리소스를 강제 삭제. |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉터리 및 파일

Valet 환경의 문제 해결 시 참고할 만한 주요 디렉터리 및 파일 정보는 다음과 같습니다:

#### `~/.config/valet`

Valet의 모든 설정이 저장됩니다. 이 디렉터리는 백업해둘 것을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DNSMasq 설정 파일이 들어 있는 디렉터리입니다.

#### `~/.config/valet/Drivers/`

Valet의 드라이버가 들어있습니다. 드라이버는 각 프레임워크/CMS 사용 방식을 결정합니다.

#### `~/.config/valet/Nginx/`

모든 Valet Nginx 사이트 설정이 저장됩니다. `install`, `secure` 명령을 실행하면 이 파일들이 다시 생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)의 모든 심볼릭 링크가 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 마스터 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet Nginx용 PHP-FPM 소켓 파일입니다. PHP가 정상적으로 실행 중일 때만 생성됩니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 에러의 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 에러의 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 에러의 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 액세스 및 에러 로그 디렉터리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

여러 PHP 설정을 위한 `*.ini` 파일이 저장됩니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트의 SSL 인증서 생성을 위한 기본 Nginx 구성 파일입니다.

<a name="disk-access"></a>
### 디스크 접근

macOS 10.14 이후로는 [일부 파일 및 디렉터리의 접근이 기본적으로 제한됩니다](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). 이 제한에는 데스크탑, 문서, 다운로드 폴더가 포함되며, 네트워크 드라이브 및 이동식 디스크 접근도 제한됩니다. 따라서, Valet 사용 시 사이트 폴더를 이러한 보호된 위치 외부에 두는 것이 좋습니다.

하지만 반드시 보호 위치 내에서 사이트를 제공하고자 한다면, Nginx에 “전체 디스크 접근” 권한을 부여해야 합니다. 그렇지 않으면 정적 에셋 서비스 등에서 예기치 못한 오류가 발생할 수 있습니다. 일반적으로 macOS에서 Nginx에 해당 권한 요청을 자동으로 안내하나, 수동으로 부여하려면 `시스템 환경설정` > `보안 및 개인정보` > `개인정보 보호`에서 “전체 디스크 접근”을 선택하고 주요 창에서 `nginx`를 활성화하면 됩니다.