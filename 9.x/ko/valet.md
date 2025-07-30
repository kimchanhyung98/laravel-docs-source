# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 서빙](#serving-sites)
    - [`park` 명령어](#the-park-command)
    - [`link` 명령어](#the-link-command)
    - [TLS로 사이트 보안 설정](#securing-sites)
    - [기본 사이트 서빙](#serving-a-default-site)
    - [사이트별 PHP 버전](#per-site-php-versions)
- [사이트 공유](#sharing-sites)
    - [Ngrok로 사이트 공유](#sharing-sites-via-ngrok)
    - [Expose로 사이트 공유](#sharing-sites-via-expose)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉토리 및 파일](#valet-directories-and-files)
    - [디스크 접근 권한](#disk-access)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Valet](https://github.com/laravel/valet)는 macOS 사용자를 위한 미니멀한 개발 환경입니다. Laravel Valet는 Mac이 시작할 때 백그라운드에서 항상 [Nginx](https://www.nginx.com/)를 실행하도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 `*.test` 도메인에서 들어오는 모든 요청을 로컬 머신에 설치된 사이트로 프록시합니다.

즉, Valet는 약 7MB 정도의 메모리만 사용하는 빠른 Laravel 개발 환경입니다. Valet는 [Sail](/docs/9.x/sail)이나 [Homestead](/docs/9.x/homestead)를 완전히 대체하지는 않지만, 기본적인 환경이 유연하고 속도가 극도로 빠른 개발 환경을 원하거나 RAM이 제한적인 머신에서 작업하는 경우 훌륭한 대안이 됩니다.

기본 설치로 지원하는 프레임워크 및 CMS는 다음과 같습니다.


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

필요에 따라 [커스텀 드라이버](#custom-valet-drivers)를 통해 Valet를 확장할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Valet는 macOS와 [Homebrew](https://brew.sh/)를 필요로 합니다. 설치 전 Apache나 Nginx 같은 다른 프로그램이 로컬 머신의 80번 포트를 점유하고 있지 않은지 확인해야 합니다.

먼저, Homebrew가 최신 상태인지 확인합니다. 다음 명령어를 실행하세요:

```shell
brew update
```

그다음, Homebrew로 PHP를 설치합니다:

```shell
brew install php
```

PHP 설치 후 [Composer 패키지 매니저](https://getcomposer.org)를 설치해야 합니다. 그리고 `~/.composer/vendor/bin` 디렉토리가 시스템 PATH에 추가되어 있는지 확인하세요. Composer 설치가 완료되면 Laravel Valet를 전역 Composer 패키지로 설치합니다:

```shell
composer global require laravel/valet
```

마지막으로 Valet의 `install` 명령어를 실행합니다. 이 명령어는 Valet와 DnsMasq를 구성 및 설치하며, 시스템 시작 시 자동으로 실행되는 데몬도 설정합니다:

```shell
valet install
```

설치가 완료되면 터미널에서 `ping foobar.test` 같은 명령어로 `*.test` 도메인이 올바르게 `127.0.0.1`로 응답하는지 확인하세요.

Valet는 머신이 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전 관리

Valet는 `valet use php@version` 명령어로 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 아직 설치되어 있지 않다면 Homebrew를 통해 자동 설치됩니다:

```shell
valet use php@7.2

valet use php
```

또한, 프로젝트 루트에 `.valetphprc` 파일을 만들어 사이트가 사용할 PHP 버전을 지정할 수 있습니다:

```shell
php@7.2
```

이 파일을 만든 후에는 간단히 `valet use` 명령어를 실행하면 해당 파일을 읽어서 사이트에 적합한 PHP 버전을 자동으로 사용합니다.

> [!WARNING]
> Valet는 한 번에 한 가지 PHP 버전만 서빙할 수 있습니다. 여러 버전이 설치되어 있어도 단일 버전만 활성화됩니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요하다면, MySQL, PostgreSQL, Redis 등을 포함한 무료 올인원 데이터베이스 관리 툴인 [DBngin](https://dbngin.com)을 추천합니다. DBngin 설치 후에는 `127.0.0.1` 주소를 사용해 `root` 사용자명과 빈 비밀번호로 데이터베이스에 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet 설치에 문제가 생긴 경우, 다음 두 명령어를 순서대로 실행하면 설치를 초기화할 수 있습니다:

```shell
composer global require laravel/valet
valet install
```

드문 경우지만, 완전 초기화가 필요하다면 `valet uninstall --force`를 실행해 완전히 제거 후 다시 설치할 수 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet` 명령어로 Valet를 업그레이드할 수 있습니다. 업그레이드 후에는 `valet install` 명령어를 실행해 설정 파일이 최신 상태로 업데이트됐는지 확인하는 것이 좋습니다.

<a name="serving-sites"></a>
## 사이트 서빙 (Serving Sites)

Valet가 설치되면 Laravel 애플리케이션을 서빙할 준비가 완료된 것입니다. Valet는 애플리케이션을 서빙하는 데 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 당신의 머신에 있는 애플리케이션들이 들어 있는 디렉터리를 등록합니다. 디렉터리를 "park" 하면, 그 디렉터리 내 모든 하위 디렉터리가 브라우저에서 `http://<디렉토리명>.test` 형식으로 접근 가능합니다:

```shell
cd ~/Sites

valet park
```

이게 전부입니다. 이제 "parked" 디렉터리 내에 새 애플리케이션을 만들어 두면 자동으로 `http://<디렉토리명>.test` 로 접속할 수 있습니다. 예를 들어, "laravel"이라는 디렉터리가 있다면 `http://laravel.test`로 접근할 수 있습니다. 또한, Valet는 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 지원합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 단일 디렉터리만 서빙할 때 유용합니다. 전체 디렉터리를 서빙하지 않고 특정 사이트 하나만 서빙하고 싶을 때 사용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 연결한 애플리케이션은 연결된 디렉터리 이름으로 접근할 수 있습니다. 위 예제에서 `http://laravel.test`로 접근할 수 있습니다. `park`와 마찬가지로  와일드카드 서브도메인(`http://foo.laravel.test`)도 지원합니다.

다른 호스트명으로 서빙하고 싶다면, `link` 명령어에 호스트명을 인수로 전달할 수 있습니다. 예를 들어, 아래 명령어는 `http://application.test` 도메인으로 사이트를 서빙합니다:

```shell
cd ~/Sites/laravel

valet link application
```

물론 서브도메인으로 애플리케이션을 서빙할 수도 있습니다:

```shell
valet link api.application
```

`links` 명령어로 현재 링크된 모든 디렉터리 목록을 확인할 수 있습니다:

```shell
valet links
```

사이트 연결을 해제하려면 `unlink` 명령어를 사용합니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 설정

기본적으로 Valet는 HTTP로 사이트를 서빙합니다. HTTPS와 HTTP/2를 사용하는 암호화된 TLS 프로토콜로 서빙하려면 `secure` 명령어를 사용하세요. 예를 들어 Valet가 `laravel.test` 도메인으로 서빙 중이라면 다음 명령어를 실행해 보안을 설정합니다:

```shell
valet secure laravel
```

반대로, TLS 보안을 해제하고 다시 평문 HTTP로 서빙하려면 `unsecure` 명령어를 사용합니다. `secure` 명령어처럼 도메인 이름을 인수로 넘겨야 합니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 서빙

알 수 없는 `test` 도메인에 접근할 때 `404` 대신 특정 사이트를 기본 사이트로 서빙하려면, `~/.config/valet/config.json` 설정 파일에 다음과 같이 `default` 옵션을 추가하세요. 경로는 기본 사이트가 될 프로젝트 경로입니다:

```
"default": "/Users/Sally/Sites/example-site",
```

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

기본적으로 Valet는 전역 PHP 설치 버전을 사용해 사이트를 서빙합니다. 그러나 사이트별로 다른 PHP 버전을 지원해야 한다면 `isolate` 명령어를 사용해 해당 사이트에서 사용할 PHP 버전을 지정할 수 있습니다. 현재 작업 중인 디렉터리 위치에서 다음과 같이 실행합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉터리 이름과 다르면 `--site` 옵션으로 사이트명을 명시하세요:

```shell
valet isolate php@8.0 --site="site-name"
```

사이트별 PHP 버전으로 적절한 PHP CLI나 도구를 호출하려면 `valet php`, `valet composer`, `valet which-php` 명령어를 사용하면 편리합니다:

```shell
valet php
valet composer
valet which-php
```

`isolated` 명령어로 격리된 사이트와 각 사이트의 PHP 버전 목록을 확인할 수 있습니다:

```shell
valet isolated
```

사이트를 다시 전역 PHP 버전으로 복원하려면 해당 사이트 루트에서 `unisolate` 명령어를 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유 (Sharing Sites)

Valet는 로컬 사이트를 외부에 쉽게 공유할 수 있게 해 주는 명령어도 제공합니다. 이를 통해 모바일 기기에서 테스트하거나 동료, 고객과 사이트를 공유할 수 있습니다.

<a name="sharing-sites-via-ngrok"></a>
### Ngrok로 사이트 공유

공유하려는 사이트 디렉터리로 이동 후 `share` 명령어를 실행하면, 공개 URL이 클립보드에 복사되어 바로 브라우저에 붙여넣기 하거나 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 종료하려면 `Control + C`를 누르세요. Ngrok를 사용한 공유는 [Ngrok 계정](https://dashboard.ngrok.com/signup) 생성과 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다.

> [!NOTE]
> `valet share` 명령에 추가 Ngrok 매개변수를 전달할 수 있습니다. 예: `valet share --region=eu`. 자세한 정보는 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
### Expose로 사이트 공유

[Expose](https://expose.dev)가 설치되어 있으면, 터미널에서 사이트 디렉터리로 이동 후 `expose` 명령어를 실행해 사이트를 공유할 수 있습니다. 지원하는 추가 명령 행 매개변수에 관한 정보는 [Expose 문서](https://expose.dev/docs)를 참고하세요. 공유 되면 Expose가 사용할 공유 가능한 URL을 표시해 줍니다:

```shell
cd ~/Sites/laravel

expose
```

공유를 중단하려면 `Control + C`를 누르세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

기본적으로 Valet는 보안상 이유로 내부 인터페이스인 `127.0.0.1`만 트래픽을 허용합니다.

로컬 네트워크 내 다른 장치가 머신의 IP 주소(예: `192.168.1.10/application.test`)로 Valet 사이트에 접속하도록 허용하려면, 해당 사이트 Nginx 설정 파일에서 `listen` 지시어의 `127.0.0.1:` 접두어를 제거해야 합니다. 80번과 443번 포트에 대해 모두 수정하세요.

만약 해당 프로젝트에 대해 `valet secure`를 실행하지 않았다면, 모든 비 HTTPS 사이트에 대해 네트워크 접근 허용을 위해 `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정하면 됩니다. 하지만 HTTPS를 사용하는 사이트(즉, `valet secure`를 실행한 경우)라면 `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

Nginx 설정을 수정한 후에는 `valet restart` 명령어를 실행해 변경사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

다른 프레임워크를 사용한 애플리케이션 중에는 프로젝트 내부에서 서버 환경 변수를 설정하는 방법이 없지만, 특정 서버 환경 변수를 요구하는 경우가 있습니다. Valet에서는 프로젝트 루트에 `.valet-env.php` 파일을 추가해 사이트별 환경 변수를 설정할 수 있습니다. 이 파일은 사이트명과 환경 변수의 연관 배열을 반환하며, 이 값은 각 사이트에 대해 전역 `$_SERVER` 배열에 추가됩니다:

```
<?php

return [
    // laravel.test 사이트에 대해 $_SERVER['key'] 값을 "value"로 설정...
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
## 서비스 프록시 (Proxying Services)

가끔 Valet 도메인을 로컬 머신에서 실행 중인 다른 서비스로 프록시하고 싶을 때가 있습니다. 예를 들어, Valet를 사용하는 동시에 Docker에서 별도 사이트를 실행해야 하는데 두 서비스 모두 포트 80을 사용할 수 없는 경우가 있습니다.

이럴 때는 `proxy` 명령어로 프록시를 생성할 수 있습니다. 예를 들어, `http://elasticsearch.test`의 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하려면 다음과 같이 실행하세요:

```shell
# HTTP 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

`unproxy` 명령어로 프록시를 삭제할 수 있습니다:

```shell
valet unproxy elasticsearch
```

`proxies` 명령어는 설정된 모든 프록시 사이트 구성을 보여줍니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버

Valet는 기본적으로 지원하지 않는 프레임워크나 CMS로 실행되는 PHP 애플리케이션을 서빙하도록 직접 Valet 드라이버를 작성할 수 있습니다. Valet 설치 시 홈 디렉터리의 `~/.config/valet/Drivers` 경로에 `SampleValetDriver.php` 파일이 생성됩니다. 이 샘플 파일은 커스텀 드라이버를 작성하는 방법을 보여주는 예제입니다. 드라이버를 작성하려면 `serves`, `isStaticFile`, `frontControllerPath` 세 메서드를 구현하면 됩니다.

각 메서드는 `$sitePath`, `$siteName`, `$uri` 인수를 받습니다. `$sitePath`는 `/Users/Lisa/Sites/my-project` 같은 사이트의 절대 경로, `$siteName`은 도메인의 호스트명(예: `my-project`), `$uri`는 들어오는 요청 URI(`/foo/bar`)입니다.

작성한 커스텀 드라이버는 `FrameworkValetDriver.php` 형식으로 `~/.config/valet/Drivers` 디렉터리에 배치합니다. 예를 들어 WordPress용 드라이버라면 `WordPressValetDriver.php`로 저장합니다.

아래는 각 메서드의 예제 구현입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 해당 드라이버가 들어오는 요청을 처리할 수 있는지 판단해 `true` 또는 `false`를 반환해야 합니다. 이 메서드 안에서는 주어진 `$sitePath`가 해당 프로젝트 타입인지 감지해야 합니다.

예를 들어 WordPress용 드라이버라면 다음처럼 쓸 수 있습니다:

```
/**
 * Determine if the driver serves the request.
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
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile` 메서드는 요청이 이미지나 스타일시트 같이 "정적(static)" 파일을 위한 것인지 판단합니다. 정적 파일이면 해당 파일의 절대 경로를 반환하고, 그렇지 않으면 `false`를 반환해야 합니다:

```
/**
 * Determine if the incoming request is for a static file.
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
```

> [!WARNING]
> `isStaticFile` 메서드는 `serves` 메서드가 들어오는 요청에 대해 `true`를 반환했을 때, 그리고 요청 URI가 `/`가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"인 주로 `index.php` 파일의 절대 경로를 반환해야 합니다:

```
/**
 * Get the fully resolved path to the application's front controller.
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
```

<a name="local-drivers"></a>
### 로컬 드라이버

특정 애플리케이션용 커스텀 Valet 드라이버를 만들고 싶을 때는 애플리케이션 루트에 `LocalValetDriver.php` 파일을 생성하세요. 이 커스텀 드라이버는 기본 `ValetDriver` 클래스를 확장하거나 `LaravelValetDriver` 같은 이미 존재하는 애플리케이션별 드라이버를 상속할 수 있습니다:

```
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
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
     * Get the fully resolved path to the application's front controller.
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
```

<a name="other-valet-commands"></a>
## 기타 Valet 명령어

| 명령어 | 설명 |
|-------------|-------------|
| `valet list` | 모든 Valet 명령어 목록 표시 |
| `valet forget` | "parked" 디렉터리에서 실행하면 해당 디렉터리를 parked 목록에서 제거 |
| `valet log` | Valet 서비스가 기록한 로그 목록 확인 |
| `valet paths` | 모든 "parked" 경로 확인 |
| `valet restart` | Valet 데몬 재시작 |
| `valet start` | Valet 데몬 시작 |
| `valet stop` | Valet 데몬 중지 |
| `valet trust` | Brew와 Valet용 sudoers 파일 추가, 비밀번호 입력 없이 Valet 명령 실행 가능하게 함 |
| `valet uninstall` | Valet 제거: 수동 제거 안내 표시. `--force` 옵션으로 모든 Valet 리소스 강제 삭제 |

<a name="valet-directories-and-files"></a>
## Valet 디렉토리 및 파일

Valet 환경 문제 해결 시 다음 디렉터리 및 파일 위치가 도움이 될 수 있습니다:

#### `~/.config/valet`

Valet 설정이 모두 들어있는 디렉터리입니다. 백업을 유지하는 것을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DNSMasq 설정이 저장된 디렉터리입니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버가 저장된 디렉터리로, 각 드라이버는 특정 프레임워크나 CMS를 어떻게 서빙할지 결정합니다.

#### `~/.config/valet/Extensions/`

커스텀 Valet 확장 및 명령어가 저장되는 디렉터리입니다.

#### `~/.config/valet/Nginx/`

Valet의 Nginx 사이트 설정 파일들이 저장되어 있습니다. `install` 및 `secure` 명령어 실행 시 재생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)의 심볼릭 링크가 저장된 디렉터리입니다.

#### `~/.config/valet/config.json`

Valet의 주 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx 설치에서 사용되는 PHP-FPM 소켓 파일입니다. PHP가 정상적으로 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류에 관한 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류에 관한 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 오류와 관련된 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 오류 로그가 저장된 디렉터리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

여러 PHP 설정을 위한 `*.ini` 파일들이 있는 디렉터리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 구성 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트용 SSL 인증서를 생성하는 데 사용되는 기본 Nginx 설정 파일입니다.

<a name="disk-access"></a>
### 디스크 접근 권한

macOS 10.14 이후 버전부터[일부 파일과 디렉터리에 대한 접근 권한이 기본적으로 제한](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)됩니다. 이 제한에는 데스크톱, 문서, 다운로드 폴더뿐 아니라 네트워크 볼륨 및 외장 볼륨도 포함됩니다. 따라서 Valet는 이러한 보호 폴더 외부에 사이트 폴더를 위치할 것을 권장합니다.

하지만 이들 위치 내에서 사이트를 서빙해야 한다면, Nginx에 "전체 디스크 접근(Full Disk Access)" 권한을 부여해야 합니다. 그렇지 않으면 Nginx가 정적 자산을 서빙할 때 서버 오류나 예측 불가한 문제가 발생할 수 있습니다. 일반적으로 macOS가 자동으로 Nginx에 권한 부여를 요청하지만, 수동으로도 설정할 수 있습니다:

`시스템 환경설정` > `보안 및 개인정보 보호` > `개인정보 보호` 탭에서 `전체 디스크 접근`을 선택한 후, 메인 창에 있는 Nginx 항목에 체크하면 됩니다.