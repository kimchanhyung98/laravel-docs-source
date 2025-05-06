# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 제공](#serving-sites)
    - ["Park" 명령어](#the-park-command)
    - ["Link" 명령어](#the-link-command)
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
    - [디스크 접근 권한](#disk-access)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> macOS 또는 Windows에서 더욱 간편하게 Laravel 애플리케이션을 개발하고 싶으신가요? [Laravel Herd](https://herd.laravel.com)를 확인해 보세요. Herd에는 Valet, PHP, Composer 등 Laravel 개발을 바로 시작하는 데 필요한 모든 것이 포함되어 있습니다.

[Laravel Valet](https://github.com/laravel/valet)은 macOS 미니멀리스트를 위한 개발 환경입니다. Laravel Valet은 Mac이 부팅될 때마다 항상 [Nginx](https://www.nginx.com/)가 백그라운드에서 실행되도록 구성합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여, Valet은 모든 `*.test` 도메인으로의 요청을 로컬에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7 MB RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/{{version}}/sail) 또는 [Homestead](/docs/{{version}}/homestead)를 완전히 대체하는 것은 아니지만, 유연한 기본 기능을 원하거나, 극한의 속도를 선호하거나, RAM이 제한된 머신에서 작업할 때 훌륭한 대안이 될 수 있습니다.

기본적으로 Valet이 지원하는 프레임워크 및 CMS는 다음과 같습니다(이에 국한되지 않음):

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

또한, 직접 [커스텀 드라이버](#custom-valet-drivers)를 추가하여 Valet을 확장할 수도 있습니다.

<a name="installation"></a>
## 설치

> [!WARNING]  
> Valet은 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전, Apache나 Nginx 등 다른 프로그램이 로컬 머신의 80 포트를 사용하고 있지 않은지 확인하세요.

먼저, Homebrew를 최신 상태로 업데이트하세요:

```shell
brew update
```

다음으로, Homebrew를 사용하여 PHP를 설치하세요:

```shell
brew install php
```

PHP 설치가 완료되면, [Composer 패키지 관리자](https://getcomposer.org)를 설치할 준비가 된 것입니다. 또한, 시스템의 "PATH" 환경변수에 `$HOME/.composer/vendor/bin` 디렉터리가 포함되어 있는지 확인하세요. Composer 설치 후, Laravel Valet을 전역 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로, Valet의 `install` 명령어를 실행하세요. 이 명령어는 Valet과 DnsMasq를 설정하고 설치합니다. 그리고 Valet이 의존하는 데몬을 시스템이 부팅될 때 자동으로 시작하도록 구성합니다:

```shell
valet install
```

Valet이 설치된 후, 터미널에서 `ping foobar.test`와 같은 명령어를 실행하여 `*.test` 도메인이 응답하는지 확인하세요. 설치가 올바르게 완료되었다면 해당 도메인이 `127.0.0.1`에서 응답하는 것을 볼 수 있습니다.

Valet은 머신이 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

> [!NOTE]  
> 글로벌 PHP 버전을 바꾸지 않고도, `isolate` [명령어](#per-site-php-versions)를 통해 사이트별 PHP 버전을 지정할 수 있습니다.

Valet은 `valet use php@version` 명령어로 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 설치되어 있지 않다면 Homebrew를 통해 자동으로 설치합니다:

```shell
valet use php@8.2

valet use php
```

또한, 프로젝트 루트에 `.valetrc` 파일을 생성하여 사이트별로 사용할 PHP 버전을 지정할 수 있습니다:

```shell
php=php@8.2
```

이 파일이 생성된 후에는 `valet use` 명령어를 단순히 실행하면, 해당 파일을 읽어 사이트의 선호 PHP 버전을 결정합니다.

> [!WARNING]  
> 여러 PHP 버전이 설치되어 있어도, Valet은 한 번에 하나의 PHP 버전만 제공합니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에서 데이터베이스가 필요한 경우, MySQL, PostgreSQL, Redis를 포함한 무료 통합 DB 관리 툴인 [DBngin](https://dbngin.com)을 참고하세요. 설치 후, `127.0.0.1`에서 `root` 사용자와 비밀번호 없이 데이터베이스에 연결할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet 설치에 문제가 있다면, `composer global require laravel/valet` 명령어와 그 뒤이어 `valet install`을 실행하여 설치를 재설정할 수 있습니다. 드물게, `valet uninstall --force` 후 다시 `valet install`을 실행하여 완전 초기화가 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet`를 실행하면 Valet을 최신 버전으로 업그레이드할 수 있습니다. 업그레이드 후에는 `valet install`을 실행하여 추가 구성이 필요한 경우 자동으로 적용하도록 하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드

Valet 3에서 Valet 4로 업그레이드하려면 아래 절차를 따라야 합니다:

<div class="content-list" markdown="1">

- 사이트의 PHP 버전을 커스터마이징하기 위해 `.valetphprc` 파일을 사용했다면, 모든 `.valetphprc` 파일을 `.valetrc`로 이름을 변경한 후, 기존 파일 내용에 `php=`를 앞에 붙이세요.
- 커스텀 드라이버를 사용하는 경우, 네임스페이스, 확장자, 타입힌트 및 반환 타입힌트가 새로운 드라이버 시스템에 맞는지 확인하세요. Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) 예제를 참고할 수 있습니다.
- 사이트 제공에 PHP 7.1 ~ 7.4를 사용 중이라면, Homebrew로 PHP 8.0 이상 버전도 설치되어 있어야 Valet이 자체 스크립트 실행을 위해 해당 버전을 사용할 수 있습니다.

</div>

<a name="serving-sites"></a>
## 사이트 제공

Valet을 설치하면 이제 Laravel 애플리케이션을 제공할 준비가 완료된 것입니다. Valet은 애플리케이션 제공을 돕는 두 가지 명령어, `park`와 `link`를 지원합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션이 포함된 디렉터리를 등록합니다. 디렉터리를 Valet에 "파킹"하면, 해당 디렉터리 내의 모든 하위 디렉터리를 웹브라우저에서 `http://<디렉터리-이름>.test`와 같은 주소로 바로 접근할 수 있습니다:

```shell
cd ~/Sites

valet park
```

이로써, "파킹" 디렉터리 내에 생성한 모든 애플리케이션이 `http://<디렉터리-이름>.test` 형식으로 자동 제공됩니다. 예를 들어, "laravel"이라는 디렉터리가 있으면, 해당 애플리케이션에 `http://laravel.test`로 접근할 수 있습니다. 또한, Valet은 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 허용합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 특정 디렉터리에서 단일 사이트만 제공하고 싶을 때 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```

이렇게 링크된 애플리케이션은 디렉터리 이름으로 접근 가능합니다. 위 예시로 링크된 사이트는 `http://laravel.test`에서 접근할 수 있습니다. 마찬가지로, 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동 허용됩니다.

다른 호스트네임으로 제공하고 싶으면, `link` 명령어에 호스트네임을 인자로 전달하세요. 예를 들어, 아래 명령어로 `http://application.test`에서 접속하도록 할 수 있습니다:

```shell
cd ~/Sites/laravel

valet link application
```

또한, 다음과 같이 서브도메인으로도 제공할 수 있습니다:

```shell
valet link api.application
```

`links` 명령어로 모든 링크된 디렉터리 목록을 확인할 수 있습니다:

```shell
valet links
```

사이트 링크를 해제하려면 `unlink` 명령어를 사용하세요:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 적용

기본적으로 Valet은 HTTP로 사이트를 제공합니다. 하지만, HTTP/2 기반의 암호화된 TLS로 제공하고 싶다면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인을 보안 적용하려면 다음을 실행하세요:

```shell
valet secure laravel
```

보안을 해제하고 HTTP로 되돌리려면 `unsecure` 명령어를 사용하면 됩니다. 이 명령어 역시 해제할 호스트네임을 인자로 받습니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 제공

알 수 없는 `test` 도메인에 접속했을 때, `404` 대신 "기본" 사이트로 연결되도록 Valet을 설정할 수도 있습니다. 이를 위해 `~/.config/valet/config.json` 파일에 아래와 같이 `default` 옵션을 추가하세요:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

Valet은 기본적으로 글로벌 PHP 설치로 사이트를 제공합니다. 하지만, 여러 사이트에서 각각 다른 PHP 버전을 지원하려면, `isolate` 명령어로 특정 사이트에서 사용할 PHP 버전을 지정할 수 있습니다. 이 명령어는 현재 작업 디렉터리에 있는 사이트에 대해 PHP 버전을 설정합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉터리명과 다르면, `--site` 옵션으로 사이트명을 지정할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

또한, `valet php`, `composer`, `which-php` 명령어로 사이트에 설정된 PHP 버전에 맞는 CLI 또는 툴을 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

`isolated` 명령어로 모든 격리된 사이트와 PHP 버전을 확인할 수 있습니다:

```shell
valet isolated
```

사이트를 다시 Valet의 글로벌 PHP 버전으로 되돌리려면, 사이트 루트에서 `unisolate` 명령어를 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유

Valet은 로컬 사이트를 외부에 손쉽게 공유할 수 있는 명령어를 제공합니다. 모바일 기기에서 테스트하거나, 팀원/클라이언트에게 공유해야 할 때 유용합니다.

기본적으로 Valet은 ngrok 또는 Expose를 통한 사이트 공유를 지원합니다. 공유하기 전에 `share-tool` 명령어로 `ngrok` 또는 `expose`를 지정해 설정을 갱신하세요:

```shell
valet share-tool ngrok
```

도구를 선택했으나 아직 Homebrew(ngrok) 또는 Composer(Expose)로 설치되어 있지 않으면 Valet에서 자동으로 설치를 안내합니다. 두 도구 모두 공유를 시작하기 전에 각각의 계정 인증이 필요합니다.

공유할 사이트의 디렉터리로 이동하여 `share` 명령어를 실행하면, 외부에서 접속 가능한 공개 URL이 복사됩니다. 이 URL을 브라우저에 붙여넣거나 팀원과 공유하면 됩니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중지하려면 `Control + C`를 누르세요.

> [!WARNING]  
> 커스텀 DNS 서버(예: `1.1.1.1`)를 사용하는 경우, ngrok 공유가 제대로 동작하지 않을 수 있습니다. 이런 경우 시스템 설정 > 네트워크 설정 > 고급 설정 > DNS 탭에서 `127.0.0.1`을 첫 번째 DNS 서버로 추가해 주세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok를 통한 사이트 공유

ngrok로 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup)과 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 토큰을 얻었다면 Valet 설정에 추가하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]  
> `valet share --region=eu`처럼 ngrok 명령어에 추가 파라미터를 전달할 수 있습니다. 자세한 사항은 [ngrok 공식 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose를 통한 사이트 공유

Expose로 사이트를 공유하려면 [Expose 계정 생성](https://expose.dev/register)과 [인증 토큰으로 인증](https://expose.dev/docs/getting-started/getting-your-token)이 필요합니다.

지원하는 추가 커맨드라인 파라미터 등 자세한 정보는 [Expose 공식 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

기본적으로 Valet은 외부로부터의 보안 위협을 차단하기 위해 인바운드 트래픽을 내부 `127.0.0.1` 인터페이스로 제한합니다.

만약 동일한 네트워크 내의 다른 기기에서 Valet 사이트에 접근하고 싶다면(예시: `192.168.1.10/application.test`), 해당 사이트의 Nginx 설정 파일에서 포트 80, 443에 대한 `listen` 지시문에서 `127.0.0.1:` 접두사를 제거해야 합니다.

프로젝트에서 `valet secure`를 실행하지 않았다면, `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정해 모든 HTTP 사이트에 대해 네트워크 접속을 허용할 수 있습니다. 프로젝트 사이트를 HTTPS로 제공 중이라면(`valet secure` 실행 후), `~/.config/valet/Nginx/app-name.test` 파일을 수정하세요.

설정을 변경했다면 `valet restart`로 변경사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

일부 프레임워크 기반 애플리케이션은 서버 환경 변수에 의존하지만, 프로젝트 내에서 이를 설정하는 기능을 제공하지 않을 수 있습니다. Valet은 프로젝트 루트에 `.valet-env.php` 파일을 추가하여 사이트별 환경 변수를 설정할 수 있습니다. 이 파일은 사이트별/환경별 변수 쌍의 배열을 반환해야 하며, 배열에 명시된 각 사이트에 대해 글로벌 `$_SERVER` 배열에 변수가 추가됩니다:

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

<a name="proxying-services"></a>
## 서비스 프록시

Valet 도메인을 로컬 머신의 다른 서비스로 프록시해야 할 때가 있습니다. 예를 들어, Docker에서 별도의 사이트를 실행하고 싶으나, Valet과 Docker가 동시에 포트 80을 사용할 수 없을 때가 해당됩니다.

이럴 때 `proxy` 명령어를 사용해 프록시를 설정할 수 있습니다. 예를 들어, `http://elasticsearch.test`에서의 모든 요청을 `http://127.0.0.1:9200`으로 프록시하려면:

```shell
# HTTP 프록시
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2 프록시
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 해제하려면 `unproxy` 명령어를 사용하세요:

```shell
valet unproxy elasticsearch
```

모든 프록시된 사이트 구성을 확인하려면 `proxies` 명령어를 사용하세요:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버

Valet에서 기본적으로 지원하지 않는 프레임워크나 CMS의 PHP 애플리케이션을 제공하려면 직접 Valet "드라이버"를 작성할 수 있습니다. Valet 설치 시 `~/.config/valet/Drivers` 디렉터리가 생성되며, 이 안에 예시용 `SampleValetDriver.php` 파일이 포함되어 있습니다. 드라이버 작성 시 `serves`, `isStaticFile`, `frontControllerPath` 메서드 3가지만 구현하면 됩니다.

세 메서드 모두 `$sitePath`, `$siteName`, `$uri` 값을 인수로 받습니다. `$sitePath`는 사이트의 절대 경로, `$siteName`은 도메인의 "호스트/사이트명" 부분, `$uri`는 요청 URI를 의미합니다.

작성한 드라이버는 `FrameworkValetDriver.php`와 같이 네이밍하여 `~/.config/valet/Drivers`에 두어야 합니다. 예를 들면 WordPress용 드라이버는 `WordPressValetDriver.php`로 저장합니다.

아래는 각 메서드의 샘플 구현입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 해당 드라이버가 요청을 처리해야 하는 경우 `true`를 반환해야 합니다. 그렇지 않으면 `false`를 반환하세요. 이 메서드에서는 주어진 `$sitePath`가 특정 프로젝트(예: WordPress)가 맞는지 판단하게 됩니다.

예를 들어 `WordPressValetDriver`를 작성한다면, 아래와 같이 구현할 수 있습니다:

    /**
     * 해당 요청을 드라이버가 처리해야 하는지 판별.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return is_dir($sitePath.'/wp-admin');
    }

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile`은 요청이 이미지나 스타일시트 같은 "정적 파일"에 대한 것인지 판별합니다. 정적 파일이면 해당 파일의 전체 경로를 반환하고, 아니라면 `false`를 반환하세요:

    /**
     * 요청이 정적 파일에 대한 것인지 판별.
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

> [!WARNING]  
> `serves` 메서드가 `true`를 반환하고, 요청 URI가 `/`가 아닐 때만 `isStaticFile`이 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath`는 애플리케이션의 "프론트 컨트롤러"(주로 "index.php" 등)의 전체 경로를 반환해야 합니다:

    /**
     * 애플리케이션의 프론트 컨트롤러 경로 반환.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public/index.php';
    }

<a name="local-drivers"></a>
### 로컬 드라이버

단일 애플리케이션만을 위한 커스텀 Valet 드라이버를 정의하려면, 애플리케이션 루트 디렉터리에 `LocalValetDriver.php` 파일을 생성하세요. 이 커스텀 드라이버는 기본 `ValetDriver` 클래스를 확장하거나, 앱별 드라이버(예: `LaravelValetDriver`)를 상속할 수 있습니다:

    use Valet\Drivers\LaravelValetDriver;

    class LocalValetDriver extends LaravelValetDriver
    {
        /**
         * 해당 요청을 드라이버가 처리해야 하는지 판별.
         */
        public function serves(string $sitePath, string $siteName, string $uri): bool
        {
            return true;
        }

        /**
         * 애플리케이션의 프론트 컨트롤러 경로 반환.
         */
        public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
        {
            return $sitePath.'/public_html/index.php';
        }
    }

<a name="other-valet-commands"></a>
## 기타 Valet 명령어

<div class="overflow-auto">

| 명령어 | 설명 |
| --- | --- |
| `valet list` | 모든 Valet 명령어 목록을 표시합니다. |
| `valet diagnose` | Valet 디버깅을 위한 진단 정보를 출력합니다. |
| `valet directory-listing` | 디렉터리 목록 표시 여부를 결정합니다. 기본값은 "off"로, 디렉터리에 404 페이지가 표시됩니다. |
| `valet forget` | 현재 "파킹"된 디렉터리에서 실행하면, 파킹 디렉터리 목록에서 제거합니다. |
| `valet log` | Valet 서비스가 기록한 로그 목록을 봅니다. |
| `valet paths` | 모든 "파킹"된 경로를 봅니다. |
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 중지합니다. |
| `valet trust` | Brew와 Valet 명령을 암호 입력 없이 실행할 수 있도록 sudoers 파일을 추가합니다. |
| `valet uninstall` | Valet을 제거합니다: 수동 제거 안내를 표시합니다. `--force` 옵션을 사용하면 모든 Valet 리소스를 강제로 삭제합니다. |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉터리 및 파일

Valet 환경에서 문제를 해결할 때 다음 디렉터리 및 파일 정보가 도움이 될 수 있습니다:

#### `~/.config/valet`

Valet의 모든 설정이 저장됩니다. 이 디렉터리의 백업을 유지하는 것이 좋습니다.

#### `~/.config/valet/dnsmasq.d/`

DnsMasq 설정이 저장된 디렉터리입니다.

#### `~/.config/valet/Drivers/`

Valet의 드라이버가 저장된 디렉터리입니다. 프레임워크/CMS 제공 방식을 결정합니다.

#### `~/.config/valet/Nginx/`

Valet의 모든 Nginx 사이트 설정이 들어 있습니다. `install` 및 `secure` 명령 실행 시 재빌드됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)의 모든 심볼릭 링크가 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 마스터 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx에서 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류용 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류용 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 오류용 시스템 로그입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 오류 로그가 저장된 디렉터리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

다양한 PHP 설정을 위한 `*.ini` 파일이 들어있는 디렉터리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트 SSL 인증서 생성을 위한 기본 Nginx 설정 파일입니다.

<a name="disk-access"></a>
### 디스크 접근 권한

macOS 10.14 이상에서는 [일부 파일 및 디렉터리 접근이 기본적으로 제한](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)됩니다. 이에는 데스크탑, 문서, 다운로드 폴더 등이 포함되며, 네트워크/이동식 볼륨 접근도 제한됩니다. 따라서 Valet은 사이트 폴더가 이 보호 위치 밖에 있도록 권장합니다.

하지만, 해당 위치에서 사이트를 제공해야 할 경우, Nginx에 "전체 디스크 접근 권한"을 부여해야 합니다. 그렇지 않으면, 서버 오류나 정적 자산 제공 시 예기치 않은 문제가 발생할 수 있습니다. 일반적으로 macOS는 자동으로 접근 권한 요청을 안내하지만, 직접 `시스템 환경설정 > 보안 및 개인 정보 보호 > 개인 정보 보호 > 전체 디스크 접근`에서 `nginx` 항목을 활성화해 부여할 수 있습니다.