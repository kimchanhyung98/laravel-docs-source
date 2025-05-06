# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 서비스하기](#serving-sites)
    - [“Park” 명령어](#the-park-command)
    - [“Link” 명령어](#the-link-command)
    - [TLS로 사이트 보안 적용하기](#securing-sites)
    - [기본 사이트 서비스](#serving-a-default-site)
    - [사이트별 PHP 버전](#per-site-php-versions)
- [사이트 공유하기](#sharing-sites)
    - [Ngrok을 통한 사이트 공유](#sharing-sites-via-ngrok)
    - [Expose를 통한 사이트 공유](#sharing-sites-via-expose)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉터리 & 파일](#valet-directories-and-files)
    - [디스크 접근](#disk-access)

<a name="introduction"></a>
## 소개

[Laravel Valet](https://github.com/laravel/valet)은 macOS 미니멀리스트를 위한 개발 환경입니다. Laravel Valet은 [Nginx](https://www.nginx.com/)를 Mac이 부팅될 때 항상 백그라운드에서 실행되도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 모든 `*.test` 도메인 요청을 로컬에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7MB의 RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/{{version}}/sail)이나 [Homestead](/docs/{{version}}/homestead)를 완전히 대체하지는 않지만, 유연한 기본 환경이 필요하거나 속도가 최우선이거나 RAM이 제한된 컴퓨터를 사용할 때 뛰어난 대안이 될 수 있습니다.

기본적으로 Valet은 다음을 포함하나 이에 국한되지 않습니다:

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

또한, 직접 [커스텀 드라이버](#custom-valet-drivers)로 Valet을 확장할 수 있습니다.

<a name="installation"></a>
## 설치

> **경고**  
> Valet은 macOS와 [Homebrew](https://brew.sh/)를 필요로 합니다. 설치 전에 Apache나 Nginx와 같은 다른 프로그램이 로컬 머신의 80번 포트를 이미 사용 중이지 않은지 확인하세요.

먼저, Homebrew가 최신 버전인지 `update` 명령어로 확인하세요:

```shell
brew update
```

그 다음, Homebrew를 이용해 PHP를 설치하세요:

```shell
brew install php
```

PHP 설치 후 [Composer 패키지 관리자](https://getcomposer.org)를 설치하세요. 또한, `~/.composer/vendor/bin` 디렉터리가 시스템의 "PATH"에 포함되어 있는지 확인해야 합니다. Composer 설치 후 Laravel Valet을 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로, Valet의 `install` 명령어를 실행하세요. 이 과정에서 Valet과 DnsMasq가 설정 및 설치됩니다. 또한, Valet이 사용하는 데몬들이 시스템이 시작될 때 자동으로 실행될 수 있도록 설정됩니다:

```shell
valet install
```

Valet 설치가 완료되면, 터미널에서 `*.test` 도메인(`ping foobar.test` 등)에 핑을 보내보세요. 올바르게 설치되었다면, 해당 도메인이 `127.0.0.1`로 응답하는 것을 볼 수 있습니다.

Valet은 시스템이 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

Valet은 `valet use php@version` 명령어를 사용하여 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 Homebrew에 설치되어 있지 않다면 자동으로 설치해줍니다:

```shell
valet use php@7.2

valet use php
```

또한 프로젝트 루트에 `.valetphprc` 파일을 생성할 수 있습니다. 이 파일에는 사이트에서 사용할 PHP 버전을 입력합니다:

```shell
php@7.2
```

이 파일을 만든 후에는 `valet use` 명령어를 실행하면 알아서 해당 파일을 읽어 사이트의 PHP 버전을 설정해줍니다.

> **경고**  
> 여러 PHP 버전을 설치했더라도 Valet은 한 번에 하나의 PHP 버전만 사용할 수 있습니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요하다면, [DBngin](https://dbngin.com)을 확인해보세요. MySQL, PostgreSQL, Redis를 포함한 올인원 데이터베이스 관리 도구로, 무료입니다. 설치 후 `127.0.0.1`에서 접속하고, 사용자명은 `root`, 비밀번호는 빈 문자열로 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet이 정상적으로 동작하지 않을 경우, `composer global require laravel/valet` 명령어와 이어서 `valet install` 명령어를 실행하면 설치가 초기화되고 다양한 문제를 해결할 수 있습니다. 드물게, `valet uninstall --force` 후 `valet install`을 통해 강제 초기화가 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet` 명령어를 실행하여 Valet을 업데이트할 수 있습니다. 업그레이드 후에는 `valet install` 명령어를 실행하여 추가로 필요한 설정 파일 업그레이드가 이루어지도록 하는 것이 좋습니다.

<a name="serving-sites"></a>
## 사이트 서비스하기

Valet 설치가 완료되면 Laravel 애플리케이션 서비스를 시작할 준비가 끝났습니다. Valet은 애플리케이션 서비스를 도와주는 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션이 들어있는 디렉터리를 등록합니다. 디렉터리가 Valet에 "park"되면, 해당 디렉터리 안에 있는 모든 하위 디렉터리가 `http://<directory-name>.test`라는 주소로 웹 브라우저에서 접근할 수 있게 됩니다:

```shell
cd ~/Sites

valet park
```

이제, "park"된 디렉터리에 새 애플리케이션을 생성하면 자동으로 `http://<directory-name>.test` 규칙에 따라 서비스됩니다. 예를 들어 "laravel" 디렉터리가 있으면, `http://laravel.test`으로 접근할 수 있습니다. 또한, 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동 지원됩니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 특정 디렉터리의 단일 사이트만 서비스하고 싶을 때 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 Valet에 등록하면, 디렉터리 이름으로 사이트에 접속할 수 있습니다. 위의 예시에서는 `http://laravel.test`으로 접근할 수 있습니다. 마찬가지로, 와일드카드 서브도메인도 지원됩니다(`http://foo.laravel.test`).

다른 호스트명으로 애플리케이션을 서비스하려면, `link` 명령어에 호스트명을 추가로 전달하세요. 예를 들어 다음과 같이 `http://application.test`에서 접근 가능하게 할 수 있습니다:

```shell
cd ~/Sites/laravel

valet link application
```

서브도메인도 지원됩니다:

```shell
valet link api.application
```

모든 연결된 디렉터리 목록은 `links` 명령어로 확인할 수 있습니다:

```shell
valet links
```

`unlink` 명령어로 사이트 심볼릭 링크를 제거할 수 있습니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 적용하기

기본적으로 Valet은 HTTP로 사이트를 서비스합니다. 하지만 HTTP/2 및 TLS로 암호화된 사이트를 서비스하려면 `secure` 명령어를 쓰면 됩니다. 만약 `laravel.test` 도메인에 대해 Valet이 서비스 중이라면, 아래 명령어로 보안을 적용할 수 있습니다:

```shell
valet secure laravel
```

사이트를 HTTP로 다시 되돌리려면 `unsecure` 명령어를 사용하세요:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 서비스

알 수 없는 `test` 도메인 방문 시 `404` 대신 "기본" 사이트를 서비스하고 싶을 경우, `~/.config/valet/config.json` 파일에 `default` 옵션을 추가하여 기본 사이트의 경로를 지정할 수 있습니다:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

Valet은 기본적으로 글로벌 PHP 설치본을 사용합니다. 하지만 여러 사이트에서 다양한 PHP 버전을 지원해야 한다면, `isolate` 명령어로 특정 사이트에 사용할 PHP 버전을 지정할 수 있습니다. 아래 명령어처럼 현재 작업 중인 디렉터리에서 실행하세요:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

만약 사이트 명이 디렉터리명과 다르다면 `--site` 옵션을 사용해 명시할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

사이트별로 설정된 PHP 버전에 따라, `valet php`, `composer`, `which-php` 명령어를 통해 적절한 PHP CLI 또는 툴을 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

사이트별로 격리된 목록과 PHP 버전은 `isolated` 명령어로 확인할 수 있습니다:

```shell
valet isolated
```

사이트를 Valet의 글로벌 PHP 버전으로 되돌리고 싶으면 사이트 루트에서 `unisolate` 명령어를 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유하기

Valet은 로컬 사이트를 외부에 공유할 수 있는 명령어도 제공합니다. 이를 통해 모바일 기기에서 테스트하거나 팀원과 공유하기에 매우 편리합니다.

<a name="sharing-sites-via-ngrok"></a>
### Ngrok을 통한 사이트 공유

사이트를 공유하려면 터미널에서 사이트 디렉터리로 이동한 후 Valet의 `share` 명령어를 실행하세요. 공개 접속 가능한 URL이 클립보드에 복사되며, 브라우저나 팀원과 바로 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중지하려면 `Control + C`를 누릅니다. Ngrok으로 사이트를 공유하려면 [Ngrok 계정 가입](https://dashboard.ngrok.com/signup)과 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다.

> **참고**  
> 추가적인 Ngrok 매개변수(예: `valet share --region=eu`)를 전달할 수 있습니다. 자세한 내용은 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
### Expose를 통한 사이트 공유

[Expose](https://expose.dev)가 설치된 경우, 사이트 디렉터리에서 `expose` 명령어를 실행해 사이트를 공유할 수 있습니다. 지원되는 추가 명령줄 옵션은 [Expose 문서](https://expose.dev/docs)에서 확인하세요. 공유 후, Expose가 공유 가능한 URL을 표시하며, 이를 통해 다른 기기나 팀원과 사이트를 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

expose
```

공유를 중지하려면 `Control + C`를 누르세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

Valet은 기본적으로 개발 머신을 인터넷 보안 위험으로부터 보호하기 위해, 수신 트래픽을 `127.0.0.1` 내부 인터페이스로 제한합니다.

만약 동일 네트워크 내 다른 기기에서 Valet 사이트에 머신의 IP(예: `192.168.1.10/application.test`)로 접근하고 싶다면, 해당 사이트의 Nginx 설정 파일에서 `listen` 지시어의 `127.0.0.1:` 접두사를 포트 80, 443에 대해 삭제해야 합니다.

`valet secure`를 실행하지 않은 일반 HTTP 사이트라면 `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정하면 됩니다. HTTPS로 서비스 중이라면 (`valet secure` 실행 시) 해당 사이트의 `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

Nginx 설정 변경 후에는 `valet restart` 명령어로 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

일부 프레임워크에서는 서버 환경 변수를 프로젝트 내부에서 직접 설정할 수 없는 경우가 있습니다. 이럴 때, 프로젝트 루트에 `.valet-env.php` 파일을 추가하여 사이트별 환경 변수를 지정할 수 있습니다. 이 파일은 사이트/환경 변수 쌍을 배열로 반환해야 하며, 각 사이트별로 글로벌 `$_SERVER` 배열에 추가됩니다:

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

가끔씩 Valet 도메인을 다른 로컬 서비스로 프록시할 필요가 있습니다. 예를 들어, Docker로 별도의 사이트를 실행하면서 Valet을 동시에 사용해야 할 때가 있습니다. 이 경우 Valet과 Docker가 모두 80번 포트를 사용할 수 없습니다.

이럴 땐 `proxy` 명령어로 프록시를 생성하세요. 예를 들어, `http://elasticsearch.test`에서 오는 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하는 방법입니다:

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

설정된 모든 프록시 목록은 `proxies` 명령어로 확인할 수 있습니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버

Valet이 기본적으로 지원하지 않는 프레임워크나 CMS를 구동하기 위해 직접 "드라이버"를 작성할 수 있습니다. Valet을 설치하면 `~/.config/valet/Drivers` 디렉터리에 `SampleValetDriver.php` 파일이 생성됩니다. 이 파일은 커스텀 드라이버 작성 샘플을 제공합니다. 드라이버는 세 가지 메서드(`serves`, `isStaticFile`, `frontControllerPath`)만 구현하면 됩니다.

세 메서드는 모두 `$sitePath`, `$siteName`, `$uri` 인자를 받습니다. `$sitePath`는 사이트의 절대 경로(`/Users/Lisa/Sites/my-project` 등), `$siteName`은 도메인의 호스트/사이트명(`my-project`), `$uri`는 요청 URI(`/foo/bar`)입니다.

커스텀 드라이버를 완성한 후엔, `FrameworkValetDriver.php` 네이밍 규칙에 맞춰 `~/.config/valet/Drivers` 디렉터리에 추가하세요. 예를 들어 WordPress용 드라이버라면 파일명을 `WordPressValetDriver.php`로 해야 합니다.

다음은 커스텀 Valet 드라이버가 구현해야 할 각 메서드의 예시입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 이 드라이버가 해당 요청을 처리해야 할 경우 `true`를 반환해야 합니다. 그렇지 않으면 `false`를 반환합니다. 이 메서드에서 `$sitePath`가 특정 프로젝트 타입을 포함하고 있는지를 확인하세요.

예를 들어, `WordPressValetDriver`라면 다음처럼 작성할 수 있습니다:

    /**
     * 요청을 처리할 드라이버인지 확인
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return bool
     */
    public function serves($sitePath, $siteName, $uri)
    {
        return is_dir($sitePath.'/wp-admin');
    }

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile` 메서드는 들어오는 요청이 이미지나 스타일시트와 같은 정적 파일을 요청하는지 확인해야 합니다. 만약 정적 파일이라면 디스크 상의 정적 파일 전체 경로를 반환하고, 아니라면 `false`를 반환합니다:

    /**
     * 요청이 정적 파일인지 확인
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string|false
     */
    public function isStaticFile($sitePath, $siteName, $uri)
    {
        if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
            return $staticFilePath;
        }

        return false;
    }

> **경고**  
> `isStaticFile` 메서드는 `serves` 메서드가 `true`를 반환하고, 요청 URI가 `/`가 아닌 경우에만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"(일반적으로 "index.php")의 전체 경로를 반환해야 합니다:

    /**
     * 앱의 프론트 컨트롤러 전체 경로 반환
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string
     */
    public function frontControllerPath($sitePath, $siteName, $uri)
    {
        return $sitePath.'/public/index.php';
    }

<a name="local-drivers"></a>
### 로컬 드라이버

특정 애플리케이션에만 커스텀 Valet 드라이버를 정의하려면, 애플리케이션 루트에 `LocalValetDriver.php` 파일을 만들면 됩니다. 이 드라이버는 기본 `ValetDriver` 클래스를 상속하거나, `LaravelValetDriver`와 같은 앱별 드라이버를 상속할 수 있습니다:

    use Valet\Drivers\LaravelValetDriver;

    class LocalValetDriver extends LaravelValetDriver
    {
        /**
         * 요청을 처리할 드라이버인지 확인
         *
         * @param  string  $sitePath
         * @param  string  $siteName
         * @param  string  $uri
         * @return bool
         */
        public function serves($sitePath, $siteName, $uri)
        {
            return true;
        }

        /**
         * 앱의 프론트 컨트롤러 전체 경로 반환
         *
         * @param  string  $sitePath
         * @param  string  $siteName
         * @param  string  $uri
         * @return string
         */
        public function frontControllerPath($sitePath, $siteName, $uri)
        {
            return $sitePath.'/public_html/index.php';
        }
    }

<a name="other-valet-commands"></a>
## 기타 Valet 명령어

명령어  | 설명
------------- | -------------
`valet list` | 모든 Valet 명령어 목록 표시
`valet forget` | "park"된 디렉터리에서 실행 시, 주차된 디렉터리 목록에서 제거
`valet log` | Valet 서비스에서 기록하는 로그 목록 보기
`valet paths` | 모든 "park"된 경로 보기
`valet restart` | Valet 데몬 재시작
`valet start` | Valet 데몬 시작
`valet stop` | Valet 데몬 중지
`valet trust` | 비밀번호 요구 없이 Valet 명령어 실행을 위해 Brew와 Valet의 sudoers 파일 추가
`valet uninstall` | Valet 제거: 수동 제거 안내 표시. `--force` 옵션 사용 시 Valet의 모든 리소스를 강제로 삭제

<a name="valet-directories-and-files"></a>
## Valet 디렉터리 & 파일

Valet 환경에서 문제를 해결할 때 다음 디렉터리와 파일 정보가 유용할 수 있습니다:

#### `~/.config/valet`

Valet의 모든 설정을 포함합니다. 이 디렉터리의 백업을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DnsMasq의 설정 파일이 존재합니다.

#### `~/.config/valet/Drivers/`

Valet의 드라이버가 들어있습니다. 드라이버는 특정 프레임워크/CMS가 어떻게 서비스되는지를 결정합니다.

#### `~/.config/valet/Extensions/`

커스텀 Valet 확장/명령어가 들어있는 디렉터리입니다.

#### `~/.config/valet/Nginx/`

Valet의 모든 Nginx 사이트 설정이 들어있습니다. `install`, `secure` 명령어 실행 시 재생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)의 심볼릭 링크가 들어있습니다.

#### `~/.config/valet/config.json`

Valet의 마스터 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx에서 사용하는 PHP-FPM 소켓 파일입니다. PHP가 제대로 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류용 사용자별 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류용 사용자별 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

시스템 차원의 PHP-FPM 오류 로그입니다.

#### `/usr/local/var/log/nginx`

Nginx의 액세스 및 오류 로그가 들어있는 디렉터리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

다양한 PHP 설정을 위한 `*.ini` 파일이 존재하는 디렉터리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트용 SSL 인증서 생성을 위한 기본 Nginx 설정 파일입니다.

<a name="disk-access"></a>
### 디스크 접근

macOS 10.14부터 [일부 파일 및 디렉터리에 기본 접근 제한이 적용](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)되었습니다. 데스크탑, 문서, 다운로드 디렉터리가 여기에 포함됩니다. 네트워크 볼륨, 이동식 볼륨 접근도 제한됩니다. 그래서 Valet은 사이트 폴더가 이러한 보호 위치 외부에 있도록 권장합니다.

그러나 꼭 해당 위치에서 서비스를 원한다면 Nginx에 "전체 디스크 접근" 권한을 부여해야 합니다. 그렇지 않으면 정적 자산 서비스 시 서버 오류 등 예기치 못한 동작이 발생할 수 있습니다. 보통 macOS가 자동으로 Nginx의 접근 권한을 요청하지만, `시스템 환경설정` > `보안 및 개인정보 보호` > `개인정보 보호`에서 수동으로 `전체 디스크 접근`을 선택하고 메인 창에서 `nginx` 항목을 활성화할 수도 있습니다.