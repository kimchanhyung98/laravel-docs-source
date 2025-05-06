# Laravel Valet

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
- [서비스 프록싱](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉터리 및 파일](#valet-directories-and-files)
    - [디스크 접근](#disk-access)

<a name="introduction"></a>
## 소개

> [!NOTE]
> macOS 또는 Windows에서 더욱 쉬운 방법으로 Laravel 애플리케이션을 개발하고 싶으신가요? [Laravel Herd](https://herd.laravel.com)를 참고하세요. Herd에는 Laravel 개발을 시작하는 데 필요한 모든 것이 포함되어 있으며, Valet, PHP, Composer가 포함되어 있습니다.

[Laravel Valet](https://github.com/laravel/valet)은 macOS 사용자, 그 중에서도 미니멀리스트를 위한 개발 환경입니다. Laravel Valet은 Mac이 시작될 때마다 [Nginx](https://www.nginx.com/)를 백그라운드에서 항상 실행되도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용하여, `*.test` 도메인의 모든 요청을 로컬 머신에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7MB의 RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/{{version}}/sail)이나 [Homestead](/docs/{{version}}/homestead)를 완전히 대체하는 것은 아니지만, 기본적인 기능만 필요하거나, 매우 빠른 환경을 선호하거나, RAM이 제한된 장치에서 작업 중인 경우 훌륭한 대안이 될 수 있습니다.

Valet은 기본적으로 다음과 같은 프레임워크를 지원하며, 이것에 국한되지 않습니다:

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

또한, [커스텀 드라이버](#custom-valet-drivers)를 통해 Valet을 확장할 수도 있습니다.

<a name="installation"></a>
## 설치

> [!WARNING]
> Valet을 사용하려면 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전, Apache나 Nginx 등 다른 프로그램이 로컬 머신의 80번 포트를 사용하고 있지 않은지 반드시 확인하세요.

시작하려면 먼저 Homebrew가 최신 상태인지 `update` 명령어로 확인하세요:

```shell
brew update
```

다음으로, Homebrew를 이용해 PHP를 설치하세요:

```shell
brew install php
```

PHP 설치 후, [Composer 패키지 매니저](https://getcomposer.org)를 설치할 차례입니다. 또한, `$HOME/.composer/vendor/bin` 디렉터리가 시스템 "PATH"에 포함되어 있는지 확인해야 합니다. Composer 설치 이후, Laravel Valet을 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로, Valet의 `install` 명령어를 실행합니다. 이 명령은 Valet과 DnsMasq를 설정 및 설치합니다. 또한, Valet이 필요로 하는 데몬들을 시스템이 시작될 때 자동으로 실행되도록 설정합니다:

```shell
valet install
```

Valet이 설치되면, 터미널에서 `ping foobar.test` 같은 명령어로 `*.test` 도메인을 핑(ping)해보세요. 올바르게 설치되었다면 해당 도메인이 `127.0.0.1`에서 응답하는 것을 볼 수 있습니다.

Valet은 컴퓨터가 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

> [!NOTE]
> 전역 PHP 버전을 변경하는 대신, Valet에서 `isolate` [명령어](#per-site-php-versions)를 사용해 사이트별 PHP 버전을 지정할 수 있습니다.

Valet은 `valet use php@version` 명령어를 이용해 PHP 버전을 전환할 수 있도록 지원합니다. Homebrew에 해당 PHP 버전이 설치되어 있지 않다면 자동으로 설치됩니다:

```shell
valet use php@8.2

valet use php
```

또한, 프로젝트의 루트에 `.valetrc` 파일을 생성할 수 있습니다. 이 파일에는 사이트에서 사용할 PHP 버전을 지정합니다:

```shell
php=php@8.2
```

이 파일이 생성되면, `valet use` 명령어를 실행하면 파일을 읽어 사이트에 적합한 PHP 버전을 자동으로 적용합니다.

> [!WARNING]
> 여러 PHP 버전을 설치했더라도, Valet은 한 번에 하나의 PHP 버전만 제공할 수 있습니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에서 데이터베이스가 필요하다면 [DBngin](https://dbngin.com)을 살펴보세요. DBngin은 MySQL, PostgreSQL, Redis를 포함하는 무료 올인원 데이터베이스 관리 도구입니다. DBngin 설치 후에는 `127.0.0.1`에서 `root` 사용자명과 빈 비밀번호로 데이터베이스에 연결할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 재설정

Valet 설치에 문제가 있다면, `composer global require laravel/valet` 명령어와 `valet install`을 차례로 실행하여 설치를 재설정할 수 있고, 다양한 문제를 해결할 수 있습니다. 매우 드물지만, 문제가 심각한 경우 `valet uninstall --force`와 `valet install` 명령어로 "강제 초기화"를 진행해야 할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet` 명령어를 실행하여 Valet을 최신 버전으로 업데이트할 수 있습니다. 업데이트 후, `valet install` 명령어를 실행해 필요한 경우 추가 구성이 반영되도록 하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드

Valet 3에서 Valet 4로 업그레이드하려면 다음 절차를 따르세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전을 지정하기 위해 `.valetphprc` 파일을 추가했다면, 각 파일을 `.valetrc`로 이름 변경하세요. 그리고 파일 내용 앞에 반드시 `php=`를 붙이세요.
- 커스텀 드라이버가 있다면 새로운 드라이버 시스템의 네임스페이스, 확장자, 타입 힌트, 반환 타입 힌트와 일치하도록 업데이트하세요. Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) 예시를 참고할 수 있습니다.
- PHP 7.1–7.4를 사용해 사이트를 제공하는 경우에도, 여전히 Homebrew로 PHP 8.0 이상을 설치해야 하며, Valet은 일부 스크립트 실행 시 기본 연결 버전이 아니더라도 이를 사용합니다.

</div>

<a name="serving-sites"></a>
## 사이트 제공

Valet 설치가 완료되면, 이제 Laravel 애플리케이션을 제공할 준비가 된 것입니다. Valet은 애플리케이션 제공을 위한 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 여러 애플리케이션이 들어있는 디렉터리를 등록합니다. 디렉터리를 Valet에 ‘주차(park)’하면 그 하위 폴더에 있는 모든 디렉터리를 웹 브라우저에서 `http://<디렉터리명>.test` 형식으로 접근할 수 있습니다:

```shell
cd ~/Sites

valet park
```

이것이 전부입니다. 이제 "주차(Parked)"된 디렉터리 내에 생성하는 모든 애플리케이션이 자동으로 `http://<디렉터리명>.test` 규칙에 따라 제공됩니다. 예를 들어, "laravel"이라는 하위 폴더가 있다면, 그 안의 애플리케이션은 `http://laravel.test` 주소로 접근할 수 있습니다. 또한 Valet은 와일드카드 서브도메인(`http://foo.laravel.test`) 접근도 자동으로 지원합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어도 Laravel 애플리케이션을 제공하는 데 사용할 수 있습니다. 이 명령어는 특정 디렉터리 하나의 사이트만 제공하고 싶을 때 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 애플리케이션을 Valet에 연결하면, 디렉터리 이름으로 해당 애플리케이션에 접속할 수 있습니다. 위 예시의 경우 `http://laravel.test`에서 사이트를 볼 수 있습니다. 또한 Valet은 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 지원합니다.

다른 호스트명으로 애플리케이션을 제공하려면 `link` 명령에 호스트명을 인자로 전달할 수도 있습니다. 예를 들어, 아래 명령어를 실행하면 `http://application.test`에서 접근할 수 있습니다:

```shell
cd ~/Sites/laravel

valet link application
```

물론, `link` 명령을 통해 서브도메인도 제공할 수 있습니다:

```shell
valet link api.application
```

`links` 명령어를 실행하면 모든 연결된 디렉터리 목록을 볼 수 있습니다:

```shell
valet links
```

사이트의 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용합니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 적용

기본적으로 Valet은 HTTP로 사이트를 제공합니다. 그러나 암호화된 TLS(HTTP/2)로 사이트를 제공하기 원한다면, `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인에서 제공 중이라면 다음 명령을 실행하여 보안을 적용할 수 있습니다:

```shell
valet secure laravel
```

"보안 해제(unsecure)"로 사이트 트래픽을 일반 HTTP로 되돌리려면 `unsecure` 명령어를 사용하세요. `secure` 명령과 마찬가지로, 이 명령에도 해제하려는 호스트명을 인자로 전달합니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 제공

알 수 없는 `test` 도메인에 접근했을 때 `404` 대신 "기본" 사이트를 제공하도록 Valet을 설정하고 싶을 때가 있습니다. 이를 위해서는 `~/.config/valet/config.json` 설정 파일에 `default` 옵션을 추가하고, 기본으로 제공할 사이트의 경로를 입력하세요:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

기본적으로 Valet은 사이트를 제공할 때 전역 PHP 설치를 사용합니다. 그러나 여러 사이트에서 각기 다른 PHP 버전이 필요하다면, `isolate` 명령어로 특정 사이트에 사용할 PHP 버전을 지정할 수 있습니다. 이 명령어는 현재 작업 디렉터리의 사이트에 대해 지정한 PHP 버전 사용을 설정합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉터리명과 다를 경우, `--site` 옵션으로 이름을 별도로 지정할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

편의를 위해, `valet php`, `composer`, `which-php` 명령어를 사용하여 사이트에 설정된 PHP 버전에 맞게 CLI나 도구를 사용할 수도 있습니다:

```shell
valet php
valet composer
valet which-php
```

`isolated` 명령어로 모든 격리된 사이트와 PHP 버전 목록을 확인할 수 있습니다:

```shell
valet isolated
```

사이트를 글로벌 PHP 버전으로 되돌리려면 사이트 루트에서 `unisolate` 명령어를 사용하면 됩니다:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유

Valet은 로컬 사이트를 외부에 공유할 수 있는 명령어를 제공합니다. 이를 통해 모바일 기기에서 사이트를 테스트하거나 팀 구성원, 클라이언트와 손쉽게 사이트를 공유할 수 있습니다.

기본적으로 Valet은 ngrok 또는 Expose를 통한 공유를 지원합니다. 사이트를 공유하기 전에 `share-tool` 명령어로 `ngrok`이나 `expose` 중 하나를 지정하여 Valet 설정을 업데이트해야 합니다:

```shell
valet share-tool ngrok
```

도구를 선택했을 때 Homebrew(ngrok) 또는 Composer(Expose)를 통해 설치되지 않았다면, Valet이 자동으로 설치를 안내합니다. 두 도구 모두 사이트 공유 전 ngrok 또는 Expose 계정 인증이 필요합니다.

사이트를 공유하려면 터미널에서 해당 디렉터리로 이동 후 Valet의 `share` 명령어를 실행하세요. 공개 접근 가능한 URL이 클립보드에 복사되어 브라우저에 바로 붙여넣거나 팀에 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

사이트 공유를 중지하려면 `Control + C`를 누르세요.

> [!WARNING]
> 커스텀 DNS 서버(예: `1.1.1.1`)를 사용 중이라면 ngrok 공유가 제대로 동작하지 않을 수 있습니다. 이럴 경우, Mac의 시스템 설정에서 네트워크 -> 고급 -> DNS 탭에서 `127.0.0.1`을 첫 번째 DNS 서버로 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok을 통한 사이트 공유

ngrok을 사용하여 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup) 및 [인증 토큰 등록](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 인증 토큰을 얻은 뒤 Valet 설정에 등록하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> `valet share --region=eu`와 같이 ngrok 명령에 추가 파라미터를 전달할 수 있습니다. 더 자세한 내용은 [ngrok 공식 문서](https://ngrok.com/docs)를 확인하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose를 통한 사이트 공유

Expose로 사이트를 공유하려면 [Expose 계정 생성](https://expose.dev/register) 후, [토큰으로 인증](https://expose.dev/docs/getting-started/getting-your-token)이 필요합니다.

지원하는 커맨드라인 파라미터 등, 자세한 사항은 [Expose 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

Valet은 개발 머신이 인터넷으로부터 보안 위험에 노출되지 않도록, 기본적으로 `127.0.0.1` 인터페이스로 외부 트래픽을 제한합니다.

로컬 네트워크의 다른 장치에서 Valet 사이트에 접근하려면(예: `192.168.1.10/application.test`), 해당 사이트에 대한 Nginx 설정 파일에서 `listen` 지시어의 `127.0.0.1:` 접두어를 삭제해야 합니다. 80, 443 포트의 `listen` 지시어에서 이 작업이 필요합니다.

프로젝트에 대해 `valet secure`를 실행하지 않았다면, `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정해 모든 비-HTTPS 사이트의 네트워크 접근을 열 수 있습니다. HTTPS로 사이트를 제공하고 있다면(`valet secure` 실행), `~/.config/valet/Nginx/app-name.test` 파일을 수정하세요.

Nginx 설정 파일을 수정했다면, `valet restart` 명령어로 변경 사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

다른 프레임워크로 만든 일부 애플리케이션은 서버 환경변수에 의존하지만, 프로젝트 내에서 그 값을 지정할 방법을 제공하지 않을 수 있습니다. Valet은 프로젝트 루트에 `.valet-env.php` 파일을 추가하여 사이트별 환경변수를 설정할 수 있습니다. 이 파일은 각 사이트에 대해 글로벌 `$_SERVER` 배열에 추가될 변수 쌍을 반환해야 합니다:

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
## 서비스 프록싱

Valet 도메인 트래픽을 로컬 머신 내의 다른 서비스로 프록시해야 할 때가 있습니다. 예를 들어, Docker에서 별도 사이트를 실행 중일 때 Valet과 Docker 둘 다 포트 80을 사용할 수는 없습니다.

이럴 경우, `proxy` 명령어로 프록시를 생성할 수 있습니다. 예를 들어, `http://elasticsearch.test`의 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하려면:

```shell
# HTTP로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 제거하려면 `unproxy` 명령어를 사용하세요:

```shell
valet unproxy elasticsearch
```

`proxies` 명령어로 프록싱된 모든 사이트 설정 목록을 확인할 수 있습니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버

Valet에서 기본적으로 지원하지 않는 프레임워크나 CMS에도 적용될 수 있도록 직접 Valet “드라이버”를 작성할 수 있습니다. Valet 설치 시 `~/.config/valet/Drivers` 디렉터리가 생성되며, 이곳에 `SampleValetDriver.php` 파일이 들어 있습니다. 이 파일은 커스텀 드라이버 작성 방법을 보여줍니다. 드라이버를 작성하려면 세 가지 메서드만 구현하면 됩니다: `serves`, `isStaticFile`, `frontControllerPath`.

세 메서드는 모두 `$sitePath`, `$siteName`, `$uri` 인자를 받습니다. `$sitePath`는 머신에서 해당 사이트의 전체 경로(예: `/Users/Lisa/Sites/my-project`)이고, `$siteName`은 도메인의 "호스트"/"사이트명"(예: `my-project`), `$uri`는 요청 URI(예: `/foo/bar`)입니다.

커스텀 Valet 드라이버를 완성했다면, `FrameworkValetDriver.php` 형식의 파일명으로 `~/.config/valet/Drivers` 디렉터리에 저장하세요. 예를 들어 WordPress용 드라이버를 만들었다면 파일명을 `WordPressValetDriver.php`로 지정해야 합니다.

이제 각 메서드를 구현하는 샘플 코드를 살펴보겠습니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 이 드라이버가 요청을 처리해야 할 경우 `true`를, 그렇지 않은 경우 `false`를 반환해야 합니다. 즉, 이 메서드에서 전달받은 `$sitePath`에 처리 대상 프로젝트가 있는지 확인하면 됩니다.

예를 들어, `WordPressValetDriver`를 만든다고 가정하면 다음과 같이 구현할 수 있습니다:

```php
/**
 * 드라이버가 요청을 처리하는지 여부 판단.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile`은 요청이 CSS나 이미지처럼 "정적" 파일에 대한 것인지 판단해야 합니다. 정적 파일이라면 그 파일의 전체 경로를 반환하고, 아니라면 `false`를 반환하세요:

```php
/**
 * 요청이 정적 파일에 대한 것인지 확인.
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
> `isStaticFile` 메서드는 `serves`가 `true`를 반환하고 요청 URI가 `/`가 아니어야 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"(주로 "index.php")의 전체 경로를 반환해야 합니다:

```php
/**
 * 애플리케이션 프론트 컨트롤러의 전체 경로 반환.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### 로컬 드라이버

특정 애플리케이션에 대해 맞춤형 Valet 드라이버가 필요하다면, 애플리케이션 루트에 `LocalValetDriver.php` 파일을 생성하세요. 커스텀 드라이버는 기본 `ValetDriver` 클래스를 확장하거나, `LaravelValetDriver`와 같은 앱 전용 드라이버를 상속하여 만들 수 있습니다:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * 드라이버가 요청을 처리하는지 여부 판단.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * 애플리케이션 프론트 컨트롤러의 전체 경로 반환.
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
| `valet diagnose` | Valet 디버깅에 도움이 되는 진단 정보를 출력합니다. |
| `valet directory-listing` | 디렉터리 목록 동작을 결정합니다. 기본값은 "off"로, 디렉터리에 대해 404 페이지를 렌더링합니다. |
| `valet forget` | "주차"된 디렉터리에서 실행하여 해당 디렉터리를 목록에서 제거합니다. |
| `valet log` | Valet 서비스에서 기록된 로그 목록을 조회합니다. |
| `valet paths` | "주차"된 모든 경로를 조회합니다. |
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 중지합니다. |
| `valet trust` | sudoers 파일을 추가하여 Valet 명령어 실행 시 비밀번호 입력 없이 가능한 권한을 부여합니다. |
| `valet uninstall` | Valet을 제거합니다. 수동 제거 안내를 표시하며, `--force` 옵션을 주면 모든 리소스를 강제로 삭제합니다. |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉터리 및 파일

Valet 환경에서 문제를 해결할 때 다음 디렉터리 및 파일 정보를 참고할 수 있습니다:

#### `~/.config/valet`

Valet의 모든 설정이 저장된 디렉터리입니다. 백업해 둘 것을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

이 디렉터리에는 DNSMasq 설정 파일이 포함되어 있습니다.

#### `~/.config/valet/Drivers/`

Valet의 드라이버들이 저장된 디렉터리입니다. 각 프레임워크/CMS 제공 방식을 결정합니다.

#### `~/.config/valet/Nginx/`

Valet의 Nginx 사이트 설정 파일이 모두 들어있는 디렉터리입니다. `install`, `secure` 명령 실행 시 파일이 재생성됩니다.

#### `~/.config/valet/Sites/`

[link 명령어](#the-link-command)를 통해 생성된 모든 심볼릭 링크가 보관됩니다.

#### `~/.config/valet/config.json`

Valet의 주요 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx 설치에서 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상 동작 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

시스템 PHP-FPM 오류 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 오류 로그가 저장되는 디렉터리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

여러 PHP 설정을 위한 `*.ini` 파일이 위치한 디렉터리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

SSL 인증서 생성을 위해 기본적으로 사용되는 Nginx 설정 파일입니다.

<a name="disk-access"></a>
### 디스크 접근

macOS 10.14부터는 [일부 파일 및 디렉터리에 기본적으로 접근이 제한](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)됩니다. 여기에는 데스크탑, 문서, 다운로드 디렉터리가 포함되며, 네트워크 볼륨 및 이동식 볼륨 접근도 제한됩니다. 따라서, Valet 사이트 폴더는 이러한 보호 위치 밖에 두는 것을 권장합니다.

하지만 보호된 위치에서 사이트를 제공해야 한다면 Nginx에 "전체 디스크 접근 권한"을 부여해야 합니다. 그렇지 않으면 정적 파일을 제공할 때 서버 오류 또는 예측 불가한 동작이 발생할 수 있습니다. 일반적으로 macOS는 이러한 위치 접근 시 자동으로 Nginx 전체 접근 권한 요청을 표시합니다. 또는 `시스템 환경설정` > `보안 및 개인정보` > `개인정보 보호`에서 "전체 디스크 접근"을 수동으로 활성화할 수 있습니다. 이후, 주창구에 표시되는 `nginx` 항목을 활성화하세요.