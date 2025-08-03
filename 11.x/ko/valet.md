# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 서빙](#serving-sites)
    - [`park` 명령어](#the-park-command)
    - [`link` 명령어](#the-link-command)
    - [TLS로 사이트 보안 설정](#securing-sites)
    - [기본 사이트 서빙](#serving-a-default-site)
    - [사이트별 PHP 버전 설정](#per-site-php-versions)
- [사이트 공유](#sharing-sites)
    - [로컬 네트워크 내 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시 설정](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉터리 및 파일](#valet-directories-and-files)
    - [디스크 접근 권한](#disk-access)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]  
> macOS 또는 Windows에서 Laravel 애플리케이션 개발을 더 쉽게 하고 싶으신가요? [Laravel Herd](https://herd.laravel.com)를 확인해 보세요. Herd는 Valet, PHP, Composer를 포함하여 Laravel 개발에 필요한 모든 것을 포함합니다.

[Laravel Valet](https://github.com/laravel/valet)는 macOS 사용자를 위한 최소한의 개발 환경입니다. Laravel Valet는 Mac을 구성해 시스템이 시작될 때 항상 백그라운드에서 [Nginx](https://www.nginx.com/)를 실행하게 합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해 `*.test` 도메인을 로컬 머신에 설치된 사이트로 프록시합니다.

즉, Valet는 약 7MB의 메모리만 사용하면서도 매우 빠른 Laravel 개발 환경을 제공합니다. Valet는 [Sail](/docs/11.x/sail)이나 [Homestead](/docs/11.x/homestead)를 완전히 대체하지는 않지만, 기본적인 유연성과 극도의 속도, 또는 제한된 RAM을 가진 머신에서 작업할 때 훌륭한 대안입니다.

Valet는 기본적으로 다음을 포함하여 다양한 프레임워크 및 CMS를 지원합니다:



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

또한, [커스텀 드라이버](#custom-valet-drivers)를 통해 Valet를 확장할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]  
> Valet는 macOS 및 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx 같은 다른 프로그램이 로컬 머신의 포트 80을 사용 중인지 확인하세요.

설치를 시작하려면 먼저 Homebrew를 최신 상태로 업데이트해야 합니다:

```shell
brew update
```

다음으로 Homebrew를 사용해 PHP를 설치하세요:

```shell
brew install php
```

PHP를 설치한 후에는 [Composer 패키지 관리자](https://getcomposer.org)를 설치해야 합니다. 또한, `$HOME/.composer/vendor/bin` 디렉터리가 시스템의 "PATH"에 포함되어 있는지 확인해야 합니다. Composer가 설치되면 Laravel Valet를 전역 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로 Valet의 `install` 명령어를 실행하세요. 이 작업은 Valet와 DnsMasq 설정 및 설치를 완료하며, 필수 데몬들이 시스템 시작 시 자동으로 실행되도록 구성합니다:

```shell
valet install
```

Valet가 설치된 후 터미널에서 `ping foobar.test`와 같은 명령으로 `*.test` 도메인에 핑을 시도해 보세요. Valet가 올바르게 설치되었다면 이 도메인이 `127.0.0.1`로 응답할 것입니다.

Valet는 시스템 부팅 시마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전 (PHP Versions)

> [!NOTE]  
> 전역 PHP 버전을 변경하는 대신 `isolate` [명령어](#per-site-php-versions)를 통해 사이트별 PHP 버전을 지정할 수 있습니다.

Valet는 `valet use php@version` 명령어로 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 설치되어 있지 않으면 Homebrew를 통해 자동으로 설치합니다:

```shell
valet use php@8.2

valet use php
```

또한 프로젝트 루트에 `.valetrc` 파일을 만들어 서브할 PHP 버전을 지정할 수 있습니다:

```shell
php=php@8.2
```

이 파일을 생성한 후에는 `valet use` 명령을 실행하면 자동으로 이 파일을 읽어 해당 사이트의 선호 PHP 버전을 반영합니다.

> [!WARNING]  
> Valet는 한 번에 하나의 PHP 버전만 서빙합니다. 여러 PHP 버전을 설치해도 동시에 사용할 수 없습니다.

<a name="database"></a>
#### 데이터베이스 (Database)

애플리케이션에 데이터베이스가 필요하다면, MySQL, PostgreSQL, Redis가 모두 포함된 무료 올인원 데이터베이스 도구인 [DBngin](https://dbngin.com)을 추천합니다. DBngin을 설치한 후에는 `127.0.0.1`에서 사용자명 `root`와 빈 비밀번호로 데이터베이스에 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화 (Resetting Your Installation)

Valet 설치가 제대로 동작하지 않을 경우, `composer global require laravel/valet`를 다시 실행한 후, `valet install`을 수행하여 설치를 리셋하면 많은 문제를 해결할 수 있습니다. 드문 경우지만 `valet uninstall --force`로 강제 제거 후 `valet install`을 다시 수행하는 "하드 리셋"이 필요할 수 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드 (Upgrading Valet)

터미널에서 `composer global require laravel/valet` 명령어를 실행하여 Valet 설치를 업데이트할 수 있습니다. 업그레이드 후에는 `valet install` 명령어를 실행해 구성 파일 업데이트 등 추가 작업을 해주는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4 업그레이드 (Upgrading to Valet 4)

Valet 3에서 Valet 4로 업그레이드 할 때는 다음 절차를 통해 올바르게 마이그레이션하세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전을 커스터마이즈하기 위해 `.valetphprc` 파일을 추가했다면, 각 `.valetphprc` 파일 이름을 `.valetrc`로 변경하세요. 그리고 기존 파일 내용 앞에 `php=`를 붙이세요.
- 기존 커스텀 드라이버가 있다면 네임스페이스, 확장명, 타입 힌트 및 반환 타입 힌트가 새 드라이버 시스템과 일치하도록 업데이트하세요. Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)를 참고할 수 있습니다.
- PHP 7.1부터 7.4 버전으로 사이트를 서빙 중이라도, Valet가 사용하는 일부 스크립트 실행을 위해 최소 PHP 8.0 이상이 Homebrew에 설치되어 있어야 합니다. 설치되어 있지 않다면 반드시 설치하세요.

</div>

<a name="serving-sites"></a>
## 사이트 서빙 (Serving Sites)

Valet를 설치했다면 이제 Laravel 애플리케이션 서빙을 시작할 준비가 된 것입니다. Valet는 애플리케이션 서빙을 도와주는 두 가지 명령어, `park`과 `link`를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션들이 위치한 디렉터리를 머신에 등록합니다. 한번 디렉터리가 Valet에 "주차(park)"되면, 해당 디렉터리 내 모든 하위 디렉터리가 웹 브라우저에서 `http://<디렉터리명>.test` 형태로 접근 가능해집니다:

```shell
cd ~/Sites

valet park
```

이게 전부입니다. 이제 "주차된" 디렉터리에 새 애플리케이션을 생성하면 자동으로 `http://<디렉터리명>.test` URL로 서빙됩니다. 예를 들어 주차된 디렉터리에 `laravel` 폴더가 있다면, 해당 애플리케이션은 `http://laravel.test`로 접근할 수 있습니다. 또한, Valet는 와일드카드 서브도메인(`http://foo.laravel.test`) 접근도 자동으로 허용합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 단일 디렉터리 내 특정 사이트만 서빙하고 싶을 때 유용합니다. 디렉터리 전체를 주차하지 않아도 됩니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 애플리케이션을 Valet에 연결하면 해당 디렉터리명을 호스트명으로 사용해 사이트에 접근할 수 있습니다. 위 예시에서는 `http://laravel.test`가 됩니다. 또한 `park`과 마찬가지로 와일드카드 서브도메인도 지원됩니다(`http://foo.laravel.test`).

다른 호스트명으로 서빙하고 싶다면 `link` 명령어 뒤에 원하는 이름을 붙이면 됩니다. 예를 들어 다음과 같이 실행하면 `http://application.test`로 서비스를 제공합니다:

```shell
cd ~/Sites/laravel

valet link application
```

서브도메인도 지정 가능합니다:

```shell
valet link api.application
```

링크된 프로젝트 목록을 보고 싶으면 `links` 명령어를 실행하세요:

```shell
valet links
```

사이트의 심볼릭 링크를 제거하고 싶다면 `unlink` 명령어를 사용합니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 설정 (Securing Sites With TLS)

기본적으로 Valet는 HTTP를 통해 사이트를 서빙합니다. 사이트를 TLS 암호화와 HTTP/2 프로토콜로 서빙하려면 `secure` 명령어를 사용하세요. 예를 들어 `laravel.test` 도메인에 대해 보안 설정을 하려면 다음을 실행합니다:

```shell
valet secure laravel
```

사이트를 다시 평문 HTTP로 되돌리려면 `unsecure` 명령어를 사용하세요. `secure`와 마찬가지로 호스트명을 인자로 받습니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 서빙 (Serving a Default Site)

알 수 없는 `*.test` 도메인 방문 시 404 대신 기본 사이트를 서빙하도록 Valet를 설정할 수 있습니다. `~/.config/valet/config.json` 설정 파일에 `default` 옵션을 추가해 기본 사이트 경로를 지정하세요:

```
"default": "/Users/Sally/Sites/example-site",
```

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전 설정 (Per-Site PHP Versions)

Valet는 기본적으로 전역 설치된 PHP로 사이트를 서빙합니다. 여러 PHP 버전을 사용해야 한다면, `isolate` 명령어로 특정 사이트가 사용할 PHP 버전을 설정할 수 있습니다. 현재 작업 중인 디렉터리에 대해 해당 PHP 버전을 지정합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉터리명과 다를 경우 `--site` 옵션으로 지정할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

편리하게도 `valet php`, `valet composer`, `valet which-php` 명령어들은 사이트 설정된 PHP 버전에 맞게 CLI 호출을 중계합니다:

```shell
valet php
valet composer
valet which-php
```

설정된 사이트와 PHP 버전 목록을 보고 싶으면 `isolated` 명령어를 실행하세요:

```shell
valet isolated
```

사이트를 다시 전역 설치 PHP 버전으로 되돌리려면 사이트 루트에서 `unisolate` 명령어를 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유 (Sharing Sites)

Valet는 로컬 사이트를 외부에 공유하는 기능을 내장해 팀원이나 클라이언트와 쉽게 테스트 URL을 공유하거나 모바일 기기에서 테스트할 수 있습니다.

기본적으로, Valet는 ngrok 및 Expose를 통한 공유를 지원합니다. 먼저 `share-tool` 명령어로 사용하는 공유 도구를 설정하세요:

```shell
valet share-tool ngrok
```

선택한 도구가 Homebrew(ngrok) 또는 Composer(Expose)를 통해 설치되어 있지 않으면 Valet가 자동으로 설치를 권장합니다. 단, 두 도구 모두 사이트 공유를 시작하기 전에 계정 인증이 필요합니다.

사이트 디렉터리로 이동한 후 `share` 명령어를 실행하면 공개 URL이 클립보드에 복사되어 브라우저에 붙여넣거나 공유할 준비가 됩니다:

```shell
cd ~/Sites/laravel

valet share
```

사이트 공유를 중단하려면 `Control + C`를 누르세요.

> [!WARNING]  
> 만약 `1.1.1.1` 같은 커스텀 DNS 서버를 사용 중이라면 ngrok 공유가 제대로 동작하지 않을 수 있습니다. 이 경우 Mac의 시스템 설정 > 네트워크 설정 > 고급 > DNS 탭에서 첫 번째 DNS 서버로 `127.0.0.1`을 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### ngrok를 통한 사이트 공유

ngrok를 통해 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup) 및 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 인증 토큰을 얻으면 다음 명령으로 Valet 구성에 토큰을 설정합니다:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]  
> `valet share --region=eu`와 같이 ngrok에 추가 파라미터를 전달할 수 있습니다. 자세한 내용은 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose를 통한 사이트 공유

Expose 공유도 마찬가지로 [Expose 계정 생성](https://expose.dev/register)과 [인증 토큰 인증](https://expose.dev/docs/getting-started/getting-your-token)이 필요합니다.

Expose가 지원하는 추가 명령줄 옵션은 [Expose 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크 내 사이트 공유 (Sharing Sites on Your Local Network)

Valet는 기본적으로 외부 인터넷으로부터 개발 머신을 보호하기 위해 내부 인터페이스 `127.0.0.1`로만 트래픽을 제한합니다.

만약 같은 로컬 네트워크 내 다른 기기가 머신 IP 주소(`192.168.1.10/application.test` 등)로 Valet 사이트에 접근하려면, 해당 사이트의 Nginx 설정 파일에서 `listen` 지시어의 `127.0.0.1:` 접두사를 제거해야 합니다.

`valet secure` 명령어를 실행하지 않은 프로젝트라면 `/usr/local/etc/nginx/valet/valet.conf` 파일을 편집해 모든 비-HTTPS 사이트의 네트워크 접근을 열 수 있습니다. HTTPS 사이트라면 `~/.config/valet/Nginx/app-name.test` 파일을 직접 수정해야 합니다.

설정을 변경한 후에는 `valet restart` 명령어를 실행해 Nginx를 재시작하여 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수 (Site Specific Environment Variables)

다른 프레임워크 애플리케이션 중에는 서버 환경 변수를 프로젝트 내에서 설정하는 기능이 없는 경우가 있습니다. Valet는 프로젝트 루트에 `.valet-env.php` 파일을 추가해 사이트별 환경 변수를 설정할 수 있도록 지원합니다. 이 파일은 사이트별 또는 전역 `$_SERVER` 배열에 할당할 키-값 배열을 반환해야 합니다:

```
<?php

return [
    // 'laravel.test' 사이트에 대해 $_SERVER['key'] 값을 지정...
    'laravel' => [
        'key' => 'value',
    ],

    // 모든 사이트에 대해 $_SERVER['key'] 값을 지정...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## 서비스 프록시 설정 (Proxying Services)

가끔 Valet 도메인을 로컬 머신 내 다른 서비스에 프록시해야 할 때가 있습니다. 예를 들어, Valet와 Docker가 동시에 포트 80을 사용할 수 없을 때 이 방법을 쓸 수 있습니다.

`proxy` 명령어를 활용해 프록시를 생성할 수 있습니다. 예를 들어 `http://elasticsearch.test`로 들어오는 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하세요:

```shell
# HTTP 프로토콜로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

생성한 프록시를 제거하려면 `unproxy` 명령어를 사용하세요:

```shell
valet unproxy elasticsearch
```

프록시된 사이트 목록을 보고 싶으면 `proxies` 명령어를 실행합니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버 (Custom Valet Drivers)

Valet가 기본적으로 지원하지 않는 프레임워크나 CMS를 위한 맞춤 드라이버를 작성할 수 있습니다. Valet 설치 시 `~/.config/valet/Drivers` 디렉터리가 생성되며, 여기에는 샘플 드라이버 구현체 `SampleValetDriver.php`가 포함되어 있습니다. 커스텀 드라이버를 작성하려면 `serves`, `isStaticFile`, `frontControllerPath` 세 가지 메서드를 구현해야 합니다.

이 세 메서드에는 `$sitePath`, `$siteName`, `$uri` 인자가 전달됩니다. `$sitePath`는 로컬 머신 내 사이트의 절대 경로(예: `/Users/Lisa/Sites/my-project`), `$siteName`은 도메인의 호스트명 부분 (`my-project`), `$uri`는 들어오는 요청 URI(`/foo/bar`)입니다.

완성한 커스텀 드라이버는 `FrameworkValetDriver.php` 형식으로 `~/.config/valet/Drivers` 디렉터리에 저장하세요. 예를 들어 WordPress용 드라이버라면 파일명은 `WordPressValetDriver.php`가 되어야 합니다.

아래는 각 메서드 예시 코드입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 드라이버가 요청을 처리할지 여부를 `true`/`false`로 반환해야 합니다. 이 메서드 내에서 `$sitePath`가 해당 프로젝트 타입인지를 판단해야 합니다.

예를 들어 WordPress에 대해 작성하면 다음과 같습니다:

```
/**
 * 요청을 처리할지 판단합니다.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile` 메서드는 요청이 이미지, 스타일시트 같은 "정적 파일"인지 검사합니다. 정적 파일이라면 디스크 내 절대 경로를 반환하고, 아니라면 `false`를 반환해야 합니다:

```
/**
 * 요청이 정적 파일인지 판단합니다.
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
> `isStaticFile` 메서드는 `serves` 메서드가 요청에 대해 `true`를 반환하고 요청 URI가 `/`가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러" 경로(보통 `index.php`)를 반환해야 합니다:

```
/**
 * 애플리케이션 프론트 컨트롤러의 절대 경로를 반환합니다.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### 로컬 드라이버 (Local Drivers)

특정 애플리케이션에 대해 커스텀 드라이버를 정의할 수도 있습니다. 프로젝트 루트에 `LocalValetDriver.php` 파일을 생성하고, 기본 `ValetDriver` 클래스를 확장하거나 기존 앱 전용 드라이버(`LaravelValetDriver` 등)를 확장하면 됩니다:

```
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * 요청을 처리할지 판단합니다.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * 애플리케이션 프론트 컨트롤러의 절대 경로를 반환합니다.
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
| `valet list` | 사용 가능한 모든 Valet 명령어 목록을 표시합니다. |
| `valet diagnose` | Valet 문제 해결에 도움이 되는 진단 정보를 출력합니다. |
| `valet directory-listing` | 디렉터리 목록 표시 동작을 결정합니다. 기본값은 "off"로, 디렉터리 요청 시 404 페이지를 렌더링합니다. |
| `valet forget` | "주차된" 디렉터리에서 실행하여 주차 목록에서 해당 디렉터리를 제거합니다. |
| `valet log` | Valet 서비스가 기록하는 로그 목록을 봅니다. |
| `valet paths` | 모든 "주차된" 경로 목록을 봅니다. |
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 중지합니다. |
| `valet trust` | Brew 및 Valet 관련 sudoers 파일을 추가하여 명령 실행 시 비밀번호 입력 없이 실행 가능하게 합니다. |
| `valet uninstall` | Valet를 제거합니다: 수동 제거 방법을 안내하며, `--force` 옵션을 지정하면 Valet 모든 리소스를 강제로 삭제합니다. |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉터리 및 파일 (Valet Directories and Files)

Valet 환경 문제 해결에 도움이 될 주요 디렉터리와 파일은 다음과 같습니다:

#### `~/.config/valet`

Valet의 모든 구성 설정이 저장된 디렉터리입니다. 백업을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DnsMasq 관련 구성 파일들이 있는 디렉터리입니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버 파일들이 위치한 디렉터리입니다. 드라이버는 특정 프레임워크/ CMS를 어떻게 서빙할지 결정합니다.

#### `~/.config/valet/Nginx/`

Valet가 관리하는 Nginx 사이트 구성 파일들이 있는 디렉터리입니다. `install` 및 `secure` 명령어 실행 시 파일이 다시 생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)에 대한 모든 심볼릭 링크가 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 마스터 구성 파일입니다.

#### `~/.config/valet/valet.sock`

Valet가 사용하는 PHP-FPM 소켓 파일로, PHP가 정상적으로 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 에러 관련 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 에러 관련 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 에러 로그가 저장된 디렉터리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

여러 PHP 설정을 담은 `*.ini` 파일들이 위치한 디렉터리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀(Pool) 구성 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트 SSL 인증서 생성 시 기본적으로 사용하는 Nginx 구성 파일입니다.

<a name="disk-access"></a>
### 디스크 접근 권한 (Disk Access)

macOS 10.14 이후부터 [일부 파일 및 디렉터리 접근이 기본 제한됩니다](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). 여기에는 데스크톱, 문서, 다운로드 디렉터리뿐만 아니라 네트워크 및 외장 볼륨도 포함됩니다. 따라서, Valet는 사이트 폴더를 이러한 보호된 위치 밖에 두는 것을 권장합니다.

하지만 해당 위치 내에서 사이트를 서빙해야 한다면 Nginx에 "전체 디스크 접근 권한(Full Disk Access)"을 부여해야 합니다. 그렇지 않으면 서버 에러나 정적 자원 서빙 중 예상치 못한 문제가 발생할 수 있습니다. macOS는 보통 Nginx가 접근 권한을 요청할 때 자동으로 알림을 표시하지만, 수동으로도 `시스템 환경설정` > `보안 및 개인정보` > `개인정보 보호`에서 `전체 디스크 접근 권한`을 부여할 수 있습니다. 이때 메인 창에서 `nginx` 항목을 찾아 활성화하세요.