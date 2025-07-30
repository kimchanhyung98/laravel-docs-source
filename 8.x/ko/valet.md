# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 서비스](#serving-sites)
    - [`park` 명령어](#the-park-command)
    - [`link` 명령어](#the-link-command)
    - [TLS로 사이트 보안 설정](#securing-sites)
    - [기본 사이트 서비스](#serving-a-default-site)
- [사이트 공유](#sharing-sites)
    - [Ngrok을 통한 사이트 공유](#sharing-sites-via-ngrok)
    - [Expose를 통한 사이트 공유](#sharing-sites-via-expose)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록싱](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉토리 및 파일](#valet-directories-and-files)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Valet](https://github.com/laravel/valet)는 macOS를 사용하는 미니멀리스트 개발자를 위한 개발 환경입니다. Laravel Valet는 기계가 시작될 때마다 백그라운드에서 항상 [Nginx](https://www.nginx.com/)를 실행하도록 Mac을 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여 `*.test` 도메인에 대한 모든 요청을 로컬 컴퓨터에 설치된 사이트로 프록시합니다.

즉, Valet는 약 7MB의 메모리만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet는 [Sail](/docs/{{version}}/sail)이나 [Homestead](/docs/{{version}}/homestead)를 완전히 대체하지는 않지만, 유연한 기본 기능을 원하거나 극도의 속도를 선호하거나 메모리 제한이 있는 머신에서 작업할 때 훌륭한 대안이 됩니다.

기본적으로 Valet는 다음과 같은 여러 프레임워크와 플랫폼을 지원합니다:



<div id="valet-support" markdown="1">

- [Laravel](https://laravel.com)
- [Lumen](https://lumen.laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [Concrete5](https://www.concrete5.org/)
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

물론, 자신의 [커스텀 드라이버](#custom-valet-drivers)를 만들어 Valet를 확장할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!NOTE]
> Valet는 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx 같은 다른 프로그램이 로컬 기기의 80번 포트를 사용 중이지 않은지 확인하세요.

시작하려면 먼저 `update` 명령어로 Homebrew를 최신 상태로 만드세요:

```
brew update
```

그 다음, Homebrew를 사용해 PHP를 설치하세요:

```
brew install php
```

PHP를 설치한 후에는 [Composer 패키지 관리자](https://getcomposer.org)를 설치할 준비가 된 것입니다. 또한, 시스템의 "PATH"에 `~/.composer/vendor/bin` 디렉토리가 포함되어 있는지 확인하세요. Composer가 설치되면, Laravel Valet를 전역 Composer 패키지로 설치할 수 있습니다:

```
composer global require laravel/valet
```

마지막으로, Valet의 `install` 명령어를 실행하세요. 이 명령어는 Valet와 DnsMasq를 구성 및 설치하며, Valet에서 사용하는 데몬들을 시스템 시작 시 자동 실행되도록 설정합니다:

```
valet install
```

Valet가 설치되면 터미널에서 `ping foobar.test`와 같은 명령어로 `*.test` 도메인에 핑을 보내 보세요. Valet가 정상적으로 설치되었다면 `127.0.0.1`에서 해당 도메인이 응답하는 것을 확인할 수 있습니다.

Valet는 기계가 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전 관리

Valet는 `valet use php@version` 명령어를 사용하여 PHP 버전을 전환할 수 있게 해줍니다. 지정한 PHP 버전이 시스템에 설치되어 있지 않으면 Valet가 Homebrew를 통해 설치합니다:

```
valet use php@7.2

valet use php
```

또한, 프로젝트 루트에 `.valetphprc` 파일을 만들어 사이트가 사용할 PHP 버전을 설정할 수 있습니다:

```
php@7.2
```

이 파일이 있으면 `valet use` 명령어만 실행해도 파일을 읽어 사이트에 맞는 PHP 버전을 자동으로 선택합니다.

> [!NOTE]
> Valet는 한 번에 하나의 PHP 버전만 서비스합니다. 여러 PHP 버전이 설치되어 있어도 마찬가지입니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요하다면 [DBngin](https://dbngin.com)을 확인해보세요. DBngin은 MySQL, PostgreSQL, Redis를 모두 포함하는 무료 올인원 데이터베이스 관리 도구입니다. DBngin을 설치한 후에는 사용자명 `root`, 빈 문자열 비밀번호로 `127.0.0.1`에 데이터베이스를 연결할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet 설치가 제대로 작동하지 않을 경우, 터미널에서 `composer global update` 명령어를 실행한 후 `valet install`을 실행하면 설치가 초기화되고 다양한 문제를 해결할 수 있습니다. 드물게, `valet uninstall --force`로 강제 제거한 뒤 `valet install`로 재설치하는 "하드 리셋"이 필요할 수 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드 (Upgrading Valet)

터미널에서 `composer global update` 명령어를 실행해 Valet를 업데이트할 수 있습니다. 업데이트 후에는 `valet install` 명령어를 실행해 필요에 따라 구성 파일을 추가로 업그레이드하는 것이 좋습니다.

<a name="serving-sites"></a>
## 사이트 서비스 (Serving Sites)

Valet가 설치되면 Laravel 애플리케이션을 서비스할 준비가 된 것입니다. Valet는 애플리케이션 서비스를 쉽게 도와주는 두 가지 명령어인 `park`와 `link`를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 머신에 있는 여러 애플리케이션이 들어있는 디렉토리를 등록합니다. 이 디렉토리를 Valet에 등록하면 그 하위의 모든 디렉토리가 웹브라우저에서 `http://<directory-name>.test` 형식으로 접근 가능해집니다:

```
cd ~/Sites

valet park
```

이게 전부입니다. 이제 "park"된 디렉토리 안에 새 애플리케이션을 만들면 자동으로 `http://<directory-name>.test` URL 형식으로 서비스됩니다. 예를 들어 "laravel"이라는 디렉토리가 있다면 해당 디렉토리에 있는 애플리케이션은 `http://laravel.test`로 접근할 수 있습니다. 또한, Valet는 와일드카드 서브도메인(`http://foo.laravel.test`)으로도 사이트 접속을 지원합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어도 Laravel 애플리케이션을 서비스하는 데 사용됩니다. 이 명령어는 전체 디렉토리가 아닌 특정 하나의 사이트만 서비스하려고 할 때 유용합니다:

```
cd ~/Sites/laravel

valet link
```

`link` 명령어로 사이트를 등록하면, 해당 디렉토리 이름으로 앱에 접근할 수 있습니다. 위 예제라면 `http://laravel.test`로 접근 가능합니다. 마찬가지로 와일드카드 서브도메인(`http://foo.laravel.test`)도 가능합니다.

만약 다른 호스트명으로 사이트를 서비스하고 싶다면 `link` 명령어에 호스트명을 인수로 넘기면 됩니다. 예를 들어, 아래 명령은 `http://application.test`에서 애플리케이션에 접근 가능하도록 합니다:

```
cd ~/Sites/laravel

valet link application
```

`links` 명령어를 실행하면 연결된 모든 디렉토리 목록을 확인할 수 있습니다:

```
valet links
```

사이트의 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용하세요:

```
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 설정 (Securing Sites With TLS)

기본적으로 Valet는 HTTP로 사이트를 서비스합니다. 그러나, 사이트를 HTTP/2 기반의 암호화된 TLS로 서비스하려면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인에서 사이트가 서비스 중이라면 아래 명령어로 보안 설정을 할 수 있습니다:

```
valet secure laravel
```

사이트의 보안 설정을 해제하고 일반 HTTP로 되돌리려면 `unsecure` 명령어를 사용하세요. 이 명령어 또한 언시큐어할 호스트명을 인수로 받습니다:

```
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 서비스 (Serving A Default Site)

가끔 존재하지 않는 `test` 도메인에 접근 시 404가 아닌 특정 기본 사이트를 보여주고 싶을 때가 있습니다. 이럴 경우, `~/.config/valet/config.json` 구성 파일에 `default` 옵션을 추가해 기본 사이트의 경로를 지정할 수 있습니다:

```
"default": "/Users/Sally/Sites/foo",
```

<a name="sharing-sites"></a>
## 사이트 공유 (Sharing Sites)

Valet는 터미널 명령어 하나로 로컬 사이트를 외부에 공유할 수 있는 기능도 제공합니다. 이 기능을 통해 모바일 기기에서 손쉽게 사이트를 테스트하거나 동료 및 클라이언트와 공유할 수 있습니다.

<a name="sharing-sites-via-ngrok"></a>
### Ngrok을 통한 사이트 공유 (Sharing Sites Via Ngrok)

사이트를 공유하려면, 터미널에서 공유할 사이트가 위치한 디렉토리로 이동한 뒤 `share` 명령어를 실행하세요. 그러면 공개 접근 가능한 URL이 클립보드에 복사되어 브라우저에 붙여넣거나 팀과 바로 공유할 수 있습니다:

```
cd ~/Sites/laravel

valet share
```

사이트 공유를 종료하려면 `Control + C`를 누르세요. Ngrok로 사이트를 공유하려면 [Ngrok 계정 생성](https://dashboard.ngrok.com/signup)과 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다.

> [!TIP]
> `valet share --region=eu`와 같이 추가 Ngrok 파라미터를 전달할 수 있습니다. 자세한 정보는 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
### Expose를 통한 사이트 공유 (Sharing Sites Via Expose)

[Expose](https://expose.dev)가 설치되어 있다면, 터미널에서 사이트 디렉토리로 이동한 뒤 `expose` 명령어를 실행해 사이트를 공유할 수 있습니다. Expose가 지원하는 추가 명령어 옵션은 [Expose 문서](https://expose.dev/docs)를 확인하세요. 공유가 시작되면 Expose가 공유 가능한 URL을 출력합니다. 이 URL을 다른 장치나 팀에 공유할 수 있습니다:

```
cd ~/Sites/laravel

expose
```

공유를 중단하려면 `Control + C`를 누르세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유 (Sharing Sites On Your Local Network)

기본적으로 Valet는 외부 인터넷의 보안 위험으로부터 개발 머신을 보호하기 위해 127.0.0.1 내부 인터페이스로 들어오는 트래픽만 허용합니다.

로컬 네트워크의 다른 장치가 머신의 IP 주소(예: `192.168.1.10/application.test`)를 통해 Valet 사이트에 접근하려면, 해당 사이트의 Nginx 설정 파일을 수동으로 편집해 `listen` 지시어의 `127.0.0.1:` 접두사를 제거해야 합니다. 특히 포트 80과 443의 `listen` 지시어에서 변경이 필요합니다.

만약 해당 프로젝트에서 `valet secure` 명령어를 실행해 HTTPS를 사용하지 않았다면, `/usr/local/etc/nginx/valet/valet.conf` 파일을 편집해 모든 비-HTTPS 사이트의 네트워크 접근을 열 수 있습니다. 하지만, HTTPS로 사이트를 서빙 중이라면 `~/.config/valet/Nginx/app-name.test` 파일을 편집해야 합니다.

설정 변경 후 `valet restart` 명령어로 데몬을 재시작해 변경 사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수 (Site Specific Environment Variables)

다른 프레임워크를 사용하는 애플리케이션은 서버 환경 변수를 필요로 하지만 프로젝트 내에서 직접 환경 변수를 설정하는 방법이 제공되지 않을 수 있습니다. Valet는 프로젝트 루트에 `.valet-env.php` 파일을 생성하여 사이트별 환경 변수를 설정할 수 있도록 지원합니다. 이 파일은 사이트별 / 환경 변수 배열을 반환하며, 지정한 각 사이트에 대해 전역 `$_SERVER` 배열에 추가됩니다:

```
<?php

return [
    // 'laravel.test' 사이트에 대해 $_SERVER['key']를 "value"로 설정...
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
## 서비스 프록싱 (Proxying Services)

종종 Valet 도메인을 로컬 머신의 다른 서비스로 프록시하려는 경우가 있습니다. 예를 들어, Valet를 사용하면서 별도로 Docker에서 사이트를 구동할 경우, Valet와 Docker가 동시에 포트 80을 바인딩할 수 없습니다.

이를 해결하기 위해 `proxy` 명령어를 사용해 프록시를 생성할 수 있습니다. 예를 들어, `http://elasticsearch.test`로 오는 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시할 수 있습니다:

```bash
// HTTP로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

// TLS + HTTP/2로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 제거하려면 `unproxy` 명령어를 사용하세요:

```
valet unproxy elasticsearch
```

프록시된 모든 사이트 구성을 확인하려면 `proxies` 명령어를 사용합니다:

```
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버 (Custom Valet Drivers)

Valet가 기본적으로 지원하지 않는 프레임워크나 CMS용 PHP 애플리케이션을 서비스하려면 자신의 Valet "드라이버"를 작성할 수 있습니다. Valet를 설치하면 `~/.config/valet/Drivers` 디렉토리가 생성되며, 여기에는 사용자 정의 드라이버 작성 방법을 보여주는 `SampleValetDriver.php` 파일이 있습니다. 드라이버는 `serves`, `isStaticFile`, `frontControllerPath` 세 가지 메서드만 구현하면 됩니다.

세 메서드는 모두 `$sitePath`, `$siteName`, `$uri` 인자를 받습니다. `$sitePath`는 머신에서 서비스 중인 사이트의 전체 경로(예: `/Users/Lisa/Sites/my-project`)이며, `$siteName`은 도메인의 "호스트" 혹은 "사이트 이름" 부분(`my-project`), `$uri`는 들어오는 요청 URI(`/foo/bar`)입니다.

커스텀 Valet 드라이버를 완성하면 `~/.config/valet/Drivers` 디렉토리에 `FrameworkValetDriver.php` 형식으로 저장하세요. 예를 들어 WordPress용 드라이버라면 파일명을 `WordPressValetDriver.php`로 해야 합니다.

아래에서 각 메서드의 예시 구현을 살펴보겠습니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 해당 드라이버가 들어오는 요청을 처리해야 하는지 판단해 `true` 또는 `false`를 반환해야 합니다. 즉, 명시된 `$sitePath`가 이 드라이버가 지원하는 프로젝트인지 판단하는 역할입니다.

예를 들어, WordPressValetDriver의 `serves` 메서드는 아래와 같을 수 있습니다:

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

`isStaticFile` 메서드는 요청이 이미지나 스타일시트 같은 "정적" 파일에 대한 것인지 판단합니다. 정적 파일이면 파일 시스템의 정적 파일 경로를 문자열로 반환하고, 아니면 `false`를 반환해야 합니다:

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

> [!NOTE]
> `isStaticFile` 메서드는 `serves` 메서드가 해당 요청에 대해 `true`를 반환하고, 요청 URI가 `/`가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"—대부분 `index.php` 파일—의 전체 경로를 반환해야 합니다:

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
### 로컬 드라이버 (Local Drivers)

하나의 애플리케이션에 커스텀 Valet 드라이버를 정의하려면 애플리케이션 루트에 `LocalValetDriver.php` 파일을 생성하세요. 이 커스텀 드라이버는 기본 `ValetDriver` 클래스를 확장하거나 `LaravelValetDriver`처럼 특정 애플리케이션용 드라이버를 상속할 수 있습니다:

```
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
## 기타 Valet 명령어 (Other Valet Commands)

명령어  | 설명
------------- | -------------
`valet forget` | "park"된 디렉토리에서 실행해 해당 디렉토리를 park 목록에서 제거합니다.
`valet log` | Valet 서비스가 기록한 로그 목록을 확인합니다.
`valet paths` | park된 모든 경로를 확인합니다.
`valet restart` | Valet 데몬을 재시작합니다.
`valet start` | Valet 데몬을 시작합니다.
`valet stop` | Valet 데몬을 중지합니다.
`valet trust` | Brew와 Valet를 위한 sudoers 파일을 추가하여 비밀번호 입력 없이 Valet 명령어를 실행할 수 있게 합니다.
`valet uninstall` | Valet를 제거합니다: 수동 제거 안내를 보여줍니다. `--force` 옵션을 붙이면 Valet 관련 리소스를 강제로 모두 삭제합니다.

<a name="valet-directories-and-files"></a>
## Valet 디렉토리 및 파일 (Valet Directories & Files)

Valet 환경 문제 해결 시 다음 디렉토리와 파일 정보를 참고하면 도움이 됩니다:

#### `~/.config/valet`

Valet의 모든 구성 파일을 담고 있습니다. 백업을 관리하는 것을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DnsMasq의 구성 파일이 있는 디렉토리입니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버들이 담긴 폴더로, 프레임워크 또는 CMS가 어떻게 서비스되는지 결정합니다.

#### `~/.config/valet/Extensions/`

커스텀 Valet 확장 또는 명령어가 위치합니다.

#### `~/.config/valet/Nginx/`

Valet Nginx 사이트 구성 파일이 위치한 곳입니다. `install`, `secure`, `tld` 명령 실행 시 이 파일들이 재생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)의 심볼릭 링크들이 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 주요 구성 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx 설치가 사용할 PHP-FPM 소켓 파일입니다. PHP가 정상 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 오류 로그가 담긴 디렉토리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

PHP 설정의 `*.ini` 파일들이 위치한 디렉토리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 구성 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트의 SSL 인증서 생성에 사용되는 기본 Nginx 구성 파일입니다.