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
- [서비스 프록시](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉토리와 파일](#valet-directories-and-files)
    - [디스크 접근 권한](#disk-access)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> macOS에서 Laravel 애플리케이션을 더 쉬운 방법으로 개발하고 싶으신가요? [Laravel Herd](https://herd.laravel.com)를 확인해보세요. Herd에는 Valet, PHP, Composer 등 Laravel 개발에 필요한 모든 것이 포함되어 있습니다.

[Laravel Valet](https://github.com/laravel/valet)는 macOS 미니멀리스트를 위한 개발 환경입니다. Laravel Valet은 Mac이 부팅될 때 항상 [Nginx](https://www.nginx.com/)가 백그라운드에서 동작하도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여, Valet은 모든 `*.test` 도메인에 대한 요청을 로컬에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7MB의 RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/{{version}}/sail)이나 [Homestead](/docs/{{version}}/homestead)를 완전히 대체하지는 않지만, 유연한 기본 환경이 필요하거나, 극한의 속도를 원하거나, RAM이 제한된 기기에서 작업해야 할 때 훌륭한 대안이 됩니다.

Valet은 기본적으로 다음과 같은 프레임워크를 지원합니다(단, 이 외에도 확장 가능합니다):

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

또한, [커스텀 드라이버](#custom-valet-drivers)를 통해 Valet을 확장할 수 있습니다.

<a name="installation"></a>
## 설치

> [!WARNING]  
> Valet은 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에, Apache나 Nginx 같은 다른 프로그램이 로컬 머신의 80번 포트를 바인딩하고 있지 않은지 확인해야 합니다.

먼저 Homebrew를 최신 상태로 업데이트하세요:

```shell
brew update
```

다음으로 Homebrew를 사용하여 PHP를 설치해야 합니다:

```shell
brew install php
```

PHP 설치가 완료되면, [Composer 패키지 관리자](https://getcomposer.org)를 설치하세요. 또한, `$HOME/.composer/vendor/bin` 디렉토리가 시스템 “PATH”에 포함되어 있는지 확인해야 합니다. Composer 설치 후 Laravel Valet을 전역 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로 Valet의 `install` 명령어를 실행합니다. 이 명령어는 Valet과 DnsMasq를 설정 및 설치하며, Valet이 의존하는 데몬도 시스템 시작 시 자동으로 실행되도록 설정됩니다.

```shell
valet install
```

Valet이 설치된 후 터미널에서 `ping foobar.test`와 같이 아무 `*.test` 도메인에 핑을 보내보세요. 설치가 제대로 완료되었다면 해당 도메인이 `127.0.0.1`로 응답합니다.

Valet은 머신이 부팅될 때마다 자동으로 필요한 서비스를 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

> [!NOTE]  
> 글로벌 PHP 버전을 변경하는 대신, `isolate` [명령어](#per-site-php-versions)를 통해 사이트별 PHP 버전을 사용할 수 있습니다.

Valet은 `valet use php@버전` 명령어를 사용하여 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 설치되어 있지 않은 경우 Homebrew를 통해 자동으로 설치합니다:

```shell
valet use php@8.1

valet use php
```

또한 프로젝트 루트에 `.valetrc` 파일을 생성할 수 있습니다. 이 파일에 해당 사이트가 사용할 PHP 버전을 명시하세요:

```shell
php=php@8.1
```

파일이 생성된 후 `valet use` 명령어를 실행하면, 이 파일을 참고하여 적절한 PHP 버전을 자동으로 적용합니다.

> [!WARNING]  
> 여러 PHP 버전이 설치되어 있어도 Valet은 한 번에 하나의 PHP 버전만 서비스를 제공합니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에서 데이터베이스가 필요하다면 [DBngin](https://dbngin.com)을 추천합니다. DBngin은 MySQL, PostgreSQL, Redis가 포함된 무료의 올인원 데이터베이스 관리 툴입니다. 설치 후, `127.0.0.1`에서 `root` 사용자와 빈 비밀번호로 데이터베이스에 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet 설치에 문제가 발생하면, `composer global require laravel/valet` 명령어 후에 `valet install`을 실행하여 설치를 초기화할 수 있으며, 다양한 문제가 해결될 수 있습니다. 매우 드물게는, `valet uninstall --force`를 실행한 후 다시 `valet install`을 실행하여 “강제 초기화”가 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet`를 실행하여 Valet을 최신 버전으로 업데이트 할 수 있습니다. 업그레이드 후에는 `valet install` 명령어를 실행해, 필요시에 설정 파일에 추가 업그레이드가 적용되도록 하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드

Valet 3에서 Valet 4로 업그레이드 할 경우, 다음 절차를 따라주세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전을 커스터마이징하기 위해 `.valetphprc` 파일을 사용했다면, 각 파일의 이름을 `.valetrc`로 변경한 뒤, 기존 내용 앞에 `php=`를 붙이세요.
- 커스텀 드라이버가 있는 경우, 네임스페이스, 확장자, 타입힌트, 리턴 타입힌트를 새 드라이버 시스템과 일치하도록 수정해야 합니다. 자세한 내용은 Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)를 참고하세요.
- PHP 7.1~7.4로 사이트를 서비스하는 경우에도 Homebrew를 통해 PHP 8.0 이상의 버전을 설치해야 합니다. Valet이 일부 내부 스크립트 실행 시 주 버전이 아니더라도 이 버전을 사용하기 때문입니다.

</div>

<a name="serving-sites"></a>
## 사이트 제공

Valet 설치가 완료되면, Laravel 애플리케이션을 서비스할 준비가 된 것입니다. Valet은 `park`와 `link` 두 가지 명령어로 애플리케이션 제공을 도와줍니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 여러 애플리케이션이 들어있는 디렉토리를 등록합니다. 디렉토리가 Valet에 “파킹(parking)”되면, 해당 디렉토리 내 모든 폴더는 `http://<폴더-이름>.test`로 웹에서 접근할 수 있습니다:

```shell
cd ~/Sites

valet park
```

이제 “파킹”된 디렉토리 안에 새 애플리케이션을 만들면, 자동으로 `http://<폴더-이름>.test` 주소로 서비스됩니다. 예를 들어 “laravel” 디렉토리가 있다면, 해당 애플리케이션은 `http://laravel.test`로 접근할 수 있습니다. 또한, 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 지원됩니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어 또한 Laravel 애플리케이션을 서비스하는 데 사용할 수 있습니다. 원하는 개별 디렉토리만 서비스할 경우에 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 애플리케이션을 등록하면, 해당 디렉토리의 이름으로 `http://laravel.test` 주소로 접근할 수 있습니다. 역시 서브도메인(`http://foo.laravel.test`)도 자동 지원됩니다.

다른 호스트네임으로 서비스하려면 `link` 명령어에 호스트네임을 인수로 전달할 수 있습니다:

```shell
cd ~/Sites/laravel

valet link application
```

서브도메인도 지정할 수 있습니다:

```shell
valet link api.application
```

`links` 명령어로 등록된 모든 심볼릭 링크 목록을 확인할 수 있습니다:

```shell
valet links
```

`unlink` 명령어는 해당 사이트의 심볼릭 링크를 제거합니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 적용

기본적으로 Valet은 HTTP로 사이트를 서비스합니다. 그러나 TLS(HTTP/2)를 사용해 암호화된 서버로 서비스하려면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인에서 사이트가 서비스 중이라면:

```shell
valet secure laravel
```

사이트를 “unsecure”하여 HTTP로 되돌리려면 `unsecure` 명령어를 사용합니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 제공

알 수 없는 `test` 도메인에 방문할 때 `404` 대신 “기본” 사이트가 서비스되도록 하려면, `~/.config/valet/config.json` 설정 파일에 “default” 옵션을 추가하세요:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

기본적으로 Valet은 글로벌 PHP 설치를 사용합니다. 여러 사이트에서 다양한 PHP 버전을 지원해야 한다면, `isolate` 명령어로 각 사이트별 PHP 버전을 지정할 수 있습니다. 현재 위치의 디렉토리에 대해 다음과 같이 설정하세요:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉토리 이름과 다를 경우, `--site` 옵션을 사용할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

편의상 `valet php`, `valet composer`, `valet which-php` 명령어로 각 사이트에 맞는 PHP CLI 및 도구를 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

`isolated` 명령어로 모든 분리(isolated)된 사이트와 PHP 버전 목록을 볼 수 있습니다:

```shell
valet isolated
```

사이트를 다시 Valet의 글로벌 PHP 버전으로 되돌리려면 사이트 루트에서 `unisolate` 명령어를 실행하면 됩니다:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유

Valet에는 로컬 사이트를 외부로 쉽게 공유할 수 있는 명령어가 포함되어 있습니다. 이를 통해 모바일 기기에서 테스트하거나 팀원 및 클라이언트와 사이트를 쉽게 공유할 수 있습니다.

Valet은 기본적으로 ngrok 또는 Expose를 통해 사이트 공유를 지원합니다. 공유 전 `share-tool` 명령어로 사용할 도구를 선택하세요(ngrok 또는 expose):

```shell
valet share-tool ngrok
```

도구를 지정했지만 Homebrew(ngrok) 또는 Composer(Expose)로 설치되어 있지 않으면, Valet이 자동으로 설치 안내를 합니다. 두 도구 모두 사이트를 공유하기 전에 ngrok 또는 Expose 계정 인증이 필요합니다.

사이트를 공유하려면 터미널에서 해당 사이트 디렉토리로 이동해, Valet의 `share` 명령어를 실행하세요. 공개된 URL이 클립보드에 복사되어 브라우저에 붙여넣거나 팀원과 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

사이트 공유를 중지하려면 `Control + C`를 누르세요.

> [!WARNING]  
> 커스텀 DNS 서버(예: `1.1.1.1`)를 사용하는 경우, ngrok 공유가 정상 동작하지 않을 수 있습니다. 이 경우 Mac의 시스템 설정에서 네트워크→고급→DNS를 열어 `127.0.0.1`을 첫 번째 DNS 서버로 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok으로 사이트 공유

ngrok으로 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup) 및 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 토큰 발급 후 Valet 설정에 추가하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]  
> `valet share --region=eu`와 같이 share 명령어에 추가 ngrok 파라미터를 전달할 수 있습니다. 더 자세한 내용은 [ngrok 공식 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose로 사이트 공유

Expose를 통한 공유는 [Expose 계정 생성](https://expose.dev/register) 및 [토큰 인증](https://expose.dev/docs/getting-started/getting-your-token)이 필요합니다.

지원하는 추가 커맨드라인 옵션은 [Expose 공식 문서](https://expose.dev/docs)에서 확인할 수 있습니다.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

기본적으로 Valet은 개발 머신이 인터넷에 노출되어 보안 위험에 노출되지 않도록 내부 `127.0.0.1` 인터페이스로만 트래픽을 제한합니다.

그러나 같은 네트워크 상의 다른 기기가 Valet 사이트에 접속할 수 있도록 하려면(NAT IP로 `192.168.1.10/application.test` 형태 등), 해당 사이트의 Nginx 설정 파일을 수동으로 편집해 `listen` 지시문의 `127.0.0.1:` 접두사를 제거해야 합니다.

`valet secure`를 실행하지 않은 프로젝트의 경우 `/usr/local/etc/nginx/valet/valet.conf` 파일을 편집하세요. HTTPS로 사이트를 서비스 중이라면 (`valet secure`를 실행한 경우) `~/.config/valet/Nginx/app-name.test` 파일을 수정하세요.

설정 변경 후 `valet restart` 명령어로 변경 사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

일부 프레임워크는 서버 환경 변수에 의존하지만, 프로젝트 내부에서 쉽게 설정방법을 제공하지 않기도 합니다. Valet은 프로젝트 루트에 `.valet-env.php` 파일을 생성해 사이트별 환경 변수를 설정할 수 있습니다. 이 파일은 사이트/환경변수 쌍의 배열을 반환하며, 해당 값이 글로벌 `$_SERVER` 배열에 추가됩니다:

    <?php

    return [
        // laravel.test 사이트에 대해 $_SERVER['key']를 "value"로 설정
        'laravel' => [
            'key' => 'value',
        ],

        // 모든 사이트에 대해 $_SERVER['key']를 "value"로 설정
        '*' => [
            'key' => 'value',
        ],
    ];

<a name="proxying-services"></a>
## 서비스 프록시

때로는 Valet 도메인을 로컬 머신의 다른 서비스(예: Docker 컨테이너 등)로 프록시하고 싶을 때가 있습니다. 예를 들어, Valet과 Docker 모두 80번 포트를 사용할 수 없으므로 Valet을 실행하면서 별도의 사이트를 Docker로 구동할 때가 있습니다.

이럴 때, `proxy` 명령어로 프록시 설정을 할 수 있습니다. 예를 들어, `http://elasticsearch.test` 트래픽을 `http://127.0.0.1:9200`으로 프록시하려면:

```shell
# HTTP 프록시
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2 프록시
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시 설정을 제거하려면 `unproxy` 명령어를 사용합니다:

```shell
valet unproxy elasticsearch
```

모든 프록시된 사이트 설정을 보려면 `proxies` 명령어를 사용하세요:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버

Valet이 기본적으로 지원하지 않는 프레임워크/ CMS도 직접 “드라이버”를 작성해 서비스할 수 있습니다. Valet 설치 시 생성되는 `~/.config/valet/Drivers` 디렉토리 안에 `SampleValetDriver.php` 파일이 함께 제공되며, 커스텀 드라이버 구현 예시를 확인할 수 있습니다. 드라이버는 3가지 메서드만 구현하면 됩니다: `serves`, `isStaticFile`, `frontControllerPath`.

세 메서드는 `$sitePath`, `$siteName`, `$uri`를 인자로 받으며, 각각 서비스 대상 사이트의 전체 경로, 사이트(호스트) 이름, 요청 URI입니다(`my-project`, `/foo/bar` 등).

커스텀 드라이버 작성이 끝나면, `FrameworkValetDriver.php` 패턴으로 위 디렉토리에 파일을 두면 됩니다. 예를 들어, 워드프레스용 드라이버를 만들면 `WordPressValetDriver.php`가 됩니다.

아래는 각 메서드의 구현 예시입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 해당 드라이버가 요청을 처리해야 하면 `true`를, 아니면 `false`를 반환합니다. 예를 들어 “워드프레스” 드라이버의 경우, 프로젝트에 `wp-admin` 디렉토리가 있다면 처리 대상으로 볼 수 있습니다:

    /**
     * 드라이버가 이 요청을 처리해야 하는지 판단
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return is_dir($sitePath.'/wp-admin');
    }

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile` 메서드는 요청된 파일이 이미지, 스타일시트 등 “정적” 파일이라면 파일의 전체 경로를 반환합니다. 정적 파일이 아니라면 `false` 반환:

    /**
     * 요청 파일이 정적 파일인지 확인
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
> `isStaticFile` 메서드는 `serves`가 true를 반환하고, 요청 URI가 `/`가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 “프론트 컨트롤러”(보통 `index.php`)의 전체 경로를 반환해야 합니다:

    /**
     * 앱의 프론트 컨트롤러의 전체 경로 반환
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public/index.php';
    }

<a name="local-drivers"></a>
### 로컬 드라이버

특정 애플리케이션만을 위한 커스텀 Valet 드라이버를 만들고 싶다면, 애플리케이션 루트에 `LocalValetDriver.php`를 생성하세요. 커스텀 드라이버는 기본 `ValetDriver` 클래스를 상속하거나, `LaravelValetDriver` 등 특정 프레임워크 드라이버를 상속할 수 있습니다:

    use Valet\Drivers\LaravelValetDriver;

    class LocalValetDriver extends LaravelValetDriver
    {
        /**
         * 드라이버가 요청을 처리해야 하는지 확인
         */
        public function serves(string $sitePath, string $siteName, string $uri): bool
        {
            return true;
        }

        /**
         * 앱의 프론트 컨트롤러의 전체 경로 반환
         */
        public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
        {
            return $sitePath.'/public_html/index.php';
        }
    }

<a name="other-valet-commands"></a>
## 기타 Valet 명령어

<div class="overflow-auto">

명령어  | 설명
------------- | -------------
`valet list` | 모든 Valet 명령어 목록 표시
`valet diagnose` | Valet 문제 해결을 위한 진단 정보 출력
`valet directory-listing` | 디렉토리 리스트 출력 동작 설정(기본은 “off”로, 디렉토리에 404 페이지 표시)
`valet forget` | “파킹”된 디렉토리에서 실행 시 파킹 디렉토리 목록에서 제거
`valet log` | Valet 서비스가 기록한 로그 목록 확인
`valet paths` | 파킹된 경로 전체 확인
`valet restart` | Valet 데몬 재시작
`valet start` | Valet 데몬 시작
`valet stop` | Valet 데몬 중지
`valet trust` | Brew와 Valet에 대한 sudoers 파일 추가(비밀번호 요청 없이 Valet 명령 실행 허용)
`valet uninstall` | Valet 제거(수동 제거 안내 표시, `--force` 옵션으로 모든 리소스 강제 삭제)

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉토리와 파일

Valet 환경에서 문제를 해결할 때 다음 디렉토리 및 파일 정보를 참고할 수 있습니다:

#### `~/.config/valet`

Valet의 모든 설정이 들어 있습니다. 백업을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DnsMasq 설정 파일이 들어 있습니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버가 들어 있습니다. 각 드라이버는 프레임워크/ CMS 서비스 방식을 결정합니다.

#### `~/.config/valet/Nginx/`

Valet의 Nginx 사이트 설정 파일이 들어 있습니다. 이 파일들은 `install`, `secure` 명령어 실행 시 재생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)를 위한 심볼릭 링크가 들어 있습니다.

#### `~/.config/valet/config.json`

Valet의 마스터 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx 설치에서 사용하는 PHP-FPM 소켓 파일입니다(PHP가 정상 구동 중일 때만 존재).

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 에러에 대한 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 에러에 대한 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 에러에 대한 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 에러 로그가 저장된 디렉토리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

여러 PHP 설정(`*.ini`) 파일이 저장된 디렉토리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트 SSL 인증서 생성을 위한 기본 Nginx 설정 파일입니다.

<a name="disk-access"></a>
### 디스크 접근 권한

macOS 10.14부터 [일부 파일 및 디렉토리는 기본적으로 접근이 제한](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)되어 있습니다. 여기에는 바탕화면, 문서, 다운로드 폴더가 포함되며, 네트워크 볼륨 및 이동식 볼륨 접근도 제한됩니다. 따라서 Valet은 사이트 폴더를 이러한 보호된 위치 바깥에 두는 것을 권장합니다.

하지만 이들 위치에서 사이트를 제공하려면 Nginx에 “전체 디스크 접근 권한(Full Disk Access)”을 부여해야 합니다. 그렇지 않으면 정적 자산 서비스 등에서 예상치 못한 서버 에러가 발생할 수 있습니다. 보통 macOS가 해당 위치 접근 시 자동으로 권한 요청을 표시합니다. 직접 부여하려면 ‘시스템 환경설정’→‘보안 및 개인정보 보호’→‘개인정보’에서 ‘전체 디스크 접근’을 선택 후, 메인 창에서 `nginx`를 활성화하세요.