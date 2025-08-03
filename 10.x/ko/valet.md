# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 서비스](#serving-sites)
    - [`park` 명령어](#the-park-command)
    - [`link` 명령어](#the-link-command)
    - [TLS로 사이트 보호하기](#securing-sites)
    - [기본 사이트 서비스](#serving-a-default-site)
    - [사이트별 PHP 버전](#per-site-php-versions)
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
## 소개 (Introduction)

> [!NOTE]  
> macOS에서 Laravel 애플리케이션 개발을 더 쉽게 하려면 [Laravel Herd](https://herd.laravel.com)를 확인해보세요. Herd는 Valet, PHP, Composer 등 Laravel 개발에 필요한 모든 것을 포함합니다.

[Laravel Valet](https://github.com/laravel/valet)는 macOS 사용자 중 미니멀리스트를 위한 개발 환경입니다. Valet는 Mac이 부팅될 때 항상 [Nginx](https://www.nginx.com/)를 백그라운드에서 실행하도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 `*.test` 도메인으로 오는 모든 요청을 로컬 머신에 설치된 사이트로 프록시 처리합니다.

즉, Valet는 약 7MB의 RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet는 [Sail](/docs/10.x/sail)이나 [Homestead](/docs/10.x/homestead)를 완전히 대체하지는 않지만, 기본에 충실하면서 극도의 속도를 원하거나 제한된 RAM 환경에서 작업하는 경우 훌륭한 대안이 됩니다.

기본적으로 Valet는 다음을 포함하여 여러 프레임워크를 지원합니다:

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

물론, [커스텀 드라이버](#custom-valet-drivers)로 Valet를 확장할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]  
> Valet는 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache 또는 Nginx 같은 다른 프로그램이 로컬 머신의 80번 포트를 사용하고 있지 않은지 확인하세요.

시작하려면 먼저 Homebrew를 최신 상태로 업데이트합니다:

```shell
brew update
```

다음으로 Homebrew를 사용하여 PHP를 설치하세요:

```shell
brew install php
```

PHP 설치 후에는 [Composer 패키지 관리자](https://getcomposer.org)를 설치해야 합니다. 추가로 `$HOME/.composer/vendor/bin` 디렉토리가 시스템 "PATH"에 포함되어 있는지 확인하세요. Composer가 설치되면 Laravel Valet를 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로 Valet의 `install` 명령어를 실행하세요. 이 명령어는 Valet와 DnsMasq를 구성 및 설치하며, Valet가 의존하는 데몬들이 시스템 시작 시 자동으로 실행되도록 설정합니다:

```shell
valet install
```

Valet가 제대로 설치되었는지 확인하려면 터미널에서 `ping foobar.test` 같은 명령어로 `*.test` 도메인에 핑을 보내보세요. 설치가 올바르게 되었다면 `127.0.0.1`에서 응답이 오는 것을 확인할 수 있습니다.

Valet는 머신이 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전 (PHP Versions)

> [!NOTE]  
> 전역 PHP 버전을 변경하는 대신, `isolate` [명령어](#per-site-php-versions)를 사용해 사이트별 PHP 버전을 지정할 수 있습니다.

Valet는 `valet use php@version` 명령어로 PHP 버전을 바꿀 수 있습니다. 지정한 PHP 버전이 설치되어 있지 않으면 Homebrew를 통해 설치합니다:

```shell
valet use php@8.1

valet use php
```

프로젝트 루트에 `.valetrc` 파일을 생성하여 사이트에 사용할 PHP 버전을 지정할 수도 있습니다:

```shell
php=php@8.1
```

이 파일이 생성된 후에는 단순히 `valet use` 명령어만 실행하면, 해당 파일을 읽어 사이트가 선호하는 PHP 버전을 자동으로 설정합니다.

> [!WARNING]  
> Valet는 한 번에 하나의 PHP 버전만 지원하며, 여러 버전이 설치되어 있어도 동시에 제공하지 않습니다.

<a name="database"></a>
#### 데이터베이스 (Database)

애플리케이션에 데이터베이스가 필요하다면, MySQL, PostgreSQL, Redis를 포함한 무료 통합 데이터베이스 관리 도구인 [DBngin](https://dbngin.com)을 확인해보세요. DBngin 설치 후 `127.0.0.1`에 `root` 사용자명과 빈 비밀번호로 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화 (Resetting Your Installation)

Valet 설치에 문제가 있을 경우, `composer global require laravel/valet` 명령어 실행 후 `valet install`을 다시 수행해 설치를 초기화하고 문제를 해결할 수 있습니다. 드물게는 `valet uninstall --force`로 "하드 리셋" 후 다시 설치해야 하는 경우도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드 (Upgrading Valet)

터미널에서 `composer global require laravel/valet` 명령어로 Valet를 업데이트할 수 있습니다. 업그레이드 후에는 `valet install` 명령어를 실행해 필요한 구성 파일 업데이트를 적용하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드하기 (Upgrading to Valet 4)

Valet 3에서 Valet 4로 업그레이드하려면 다음 단계를 따르세요:

<div class="content-list" markdown="1">

- 사이트의 PHP 버전을 커스텀하려 `.valetphprc` 파일을 사용했다면, 파일 이름을 `.valetrc`로 변경하고 내용 앞에 `php=`를 붙이세요.
- 커스텀 드라이버가 있다면 새로운 드라이버 시스템의 네임스페이스, 확장, 타입 힌트, 반환 타입 힌트에 맞게 수정하세요. Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)를 참고하세요.
- PHP 7.1~7.4 버전으로 사이트를 서비스하는 경우에도, Valet가 스크립트 실행에 PHP 8.0 이상 버전을 사용하므로 Homebrew로 PHP 8.0 이상 버전을 설치해야 합니다.

</div>

<a name="serving-sites"></a>
## 사이트 서비스 (Serving Sites)

Valet가 설치되면 Laravel 애플리케이션을 서비스할 준비가 된 것입니다. Valet는 애플리케이션을 서비스할 때 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션이 들어있는 디렉토리를 Valet에 등록합니다. 해당 디렉토리가 "park"되면 그 안의 모든 하위 디렉토리가 웹 브라우저에서 `http://<디렉토리-이름>.test` 주소로 접근할 수 있게 됩니다:

```shell
cd ~/Sites

valet park
```

이것만으로 충분합니다. 이제 "park"된 디렉토리 내에 새 애플리케이션을 만들면 자동으로 `http://<디렉토리-이름>.test` 규칙으로 서비스됩니다. 예를 들어 `laravel`이라는 디렉토리가 있으면 `http://laravel.test`로 접근할 수 있습니다. 그뿐만 아니라 Valet는 와일드카드 서브도메인(`http://foo.laravel.test`) 역시 자동으로 지원합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어를 사용하면 특정 디렉토리 단일 사이트만 서비스할 수 있습니다. 전체 디렉토리를 서비스하지 않고 하나의 사이트만 연결하려는 경우 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 사이트를 Valet에 연결하면 해당 디렉토리 이름으로 사이트에 접속할 수 있습니다. 위 예제의 경우 `http://laravel.test`로 접근 가능합니다. 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 접근할 수 있습니다.

다른 호스트 이름으로 서비스하고 싶다면 `link` 명령에 별도의 이름을 넘기세요. 예를 들어 `http://application.test`로 접속하려면 다음과 같이 합니다:

```shell
cd ~/Sites/laravel

valet link application
```

또한 `link` 명령어를 사용해 서브도메인으로 서비스할 수도 있습니다:

```shell
valet link api.application
```

링크된 모든 디렉토리 목록을 보고 싶으면 `links` 명령어를 실행하세요:

```shell
valet links
```

사이트의 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용합니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보호하기 (Securing Sites With TLS)

기본적으로 Valet는 HTTP로 사이트를 서비스하지만, TLS 암호화와 HTTP/2를 사용해 사이트를 보호하려면 `secure` 명령어를 사용하세요. 예를 들어 `laravel.test` 도메인으로 서비스 중인 사이트를 보호하려면 다음과 같이 실행합니다:

```shell
valet secure laravel
```

반대로 TLS를 해제하고 HTTP로 다시 서비스하려면 `unsecure` 명령어를 사용하세요. `secure` 명령과 동일하게 호스트 이름을 인수로 전달합니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 서비스 (Serving a Default Site)

알려지지 않은 `test` 도메인에 접속할 때 404 대신 기본 사이트를 서비스하도록 Valet를 설정할 수도 있습니다. 이를 위해 `~/.config/valet/config.json` 설정 파일에 기본 사이트 경로를 `default` 옵션으로 추가하세요:

```
"default": "/Users/Sally/Sites/example-site",
```

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전 (Per-Site PHP Versions)

기본적으로 Valet는 전역 PHP를 사용해 사이트를 서비스하지만, 여러 사이트에서 각기 다른 PHP 버전을 쓰고 싶을 수 있습니다. 이 경우 `isolate` 명령어로 특정 사이트에 적용할 PHP 버전을 지정할 수 있습니다. `isolate` 명령은 현재 작업 디렉토리 기준으로 해당 디렉토리 사이트에 PHP 버전을 적용합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉토리 이름과 다르면 `--site` 옵션으로 명시할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

사이트별 PHP 버전에 맞게 PHP CLI, Composer 등을 실행할 때는 `valet php`, `valet composer`, `valet which-php` 명령어를 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

현재 격리된 사이트와 각각의 PHP 버전을 보고 싶으면 `isolated` 명령어를 실행하세요:

```shell
valet isolated
```

특정 사이트를 전역 PHP 버전으로 되돌리려면 사이트 루트에서 `unisolate` 명령어를 실행합니다:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유 (Sharing Sites)

Valet는 로컬 사이트를 전 세계와 공유할 수 있는 기능을 제공합니다. 이를 통해 모바일 기기 테스트나 팀원, 클라이언트와의 공유가 간편해집니다.

기본적으로 Valet는 ngrok이나 Expose를 통한 사이트 공유를 지원합니다. 공유 전에 `share-tool` 명령어로 `ngrok` 또는 `expose` 중 사용할 도구를 설정하세요:

```shell
valet share-tool ngrok
```

도구가 설치되어 있지 않으면 Valet가 Homebrew(ngrok) 또는 Composer(Expose) 설치를 자동으로 안내합니다. 두 도구 모두 공유 전에 계정 인증이 필요합니다.

사이트를 공유하려면 터미널에서 사이트 디렉토리로 이동한 뒤 `share` 명령어를 실행하세요. 공개 가능한 URL이 클립보드에 복사되며, 이것을 브라우저에 붙여넣거나 팀과 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중단하려면 `Control + C`를 누르세요.

> [!WARNING]  
> 커스텀 DNS 서버(`1.1.1.1` 등)를 사용 중이면 ngrok 공유가 제대로 작동하지 않을 수 있습니다. 이 경우 Mac의 시스템 환경설정에서 네트워크 > 고급 > DNS 탭으로 이동해 `127.0.0.1`을 첫 번째 DNS 서버로 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok로 사이트 공유하기

ngrok 공유를 위해서는 [ngrok 계정 생성](https://dashboard.ngrok.com/signup) 및 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 인증 토큰을 얻은 후 다음 명령어로 Valet 설정을 업데이트하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]  
> `valet share --region=eu`처럼 ngrok 관련 추가 옵션을 전달할 수 있습니다. 자세한 내용은 [ngrok 문서](https://ngrok.com/docs)를 참조하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose로 사이트 공유하기

Expose를 사용하려면 [Expose 계정 생성](https://expose.dev/register) 및 [인증 토큰 인증](https://expose.dev/docs/getting-started/getting-your-token)이 필요합니다.

Expose가 지원하는 추가 명령줄 매개변수는 [Expose 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유하기 (Sharing Sites on Your Local Network)

Valet는 기본적으로 외부 인터넷으로부터 개발 머신 노출을 막기 위해 `127.0.0.1` 인터페이스만 요청을 허용합니다.

로컬 네트워크 내 다른 기기들이 머신의 IP 주소(예: `192.168.1.10/application.test`)를 통해 Valet 사이트에 접속하게 하려면, 해당 사이트의 Nginx 설정 파일에서 `listen` 지시어에 붙은 `127.0.0.1:` 접두사를 제거해야 합니다. 80번과 443번 포트에 모두 이 작업을 수행하세요.

`valet secure`를 실행하지 않은 프로젝트는 `/usr/local/etc/nginx/valet/valet.conf` 파일에서 네트워크 접근 설정을 수정할 수 있습니다. HTTPS로 서비스 중인 사이트(`valet secure` 실행한 경우)는 `~/.config/valet/Nginx/app-name.test` 파일을 편집하세요.

수정 후에는 `valet restart` 명령어로 Nginx 설정을 다시 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수 (Site Specific Environment Variables)

일부 다른 프레임워크 애플리케이션은 서버 환경 변수에 의존하지만 프로젝트 내에서 설정할 방법이 없을 수 있습니다. Valet는 프로젝트 루트에 `.valet-env.php` 파일을 두어 사이트별 환경 변수 설정을 지원합니다. 이 파일은 사이트별 혹은 모든 사이트에 추가할 환경 변수 쌍의 배열을 반환하며, 각 사이트에 대해 글로벌 `$_SERVER` 배열에 추가됩니다:

```
<?php

return [
    // laravel.test 사이트에서 $_SERVER['key']를 "value"로 설정...
    'laravel' => [
        'key' => 'value',
    ],

    // 모든 사이트에서 $_SERVER['key']를 "value"로 설정...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## 서비스 프록시 (Proxying Services)

경우에 따라 Valet 도메인을 로컬 머신 내 다른 서비스로 프록시 처리하고 싶을 수 있습니다. 예를 들어 Valet를 실행하면서 Docker 내 별도 사이트를 운영하면 둘 다 포트 80을 공유할 수 없어 문제가 발생합니다.

이럴 때 `proxy` 명령어를 사용해 프록시를 생성할 수 있습니다. 예를 들어 `http://elasticsearch.test`로 들어오는 트래픽을 `http://127.0.0.1:9200`으로 프록시할 수 있습니다:

```shell
# HTTP 프록시 생성...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2 프록시 생성...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 제거할 때는 `unproxy` 명령어를 사용하세요:

```shell
valet unproxy elasticsearch
```

프록시 설정된 모든 사이트를 보고 싶으면 `proxies` 명령어를 실행합니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버 (Custom Valet Drivers)

Valet가 기본 지원하지 않는 프레임워크나 CMS용 PHP 애플리케이션을 서비스하려면 직접 Valet "드라이버"를 작성할 수 있습니다. Valet 설치 시 `~/.config/valet/Drivers` 디렉토리에 `SampleValetDriver.php` 파일이 생성되며, 이 파일이 커스텀 드라이버 작성 방법의 샘플을 제공합니다.

드라이버는 `serves`, `isStaticFile`, `frontControllerPath` 세 가지 메서드를 구현해야 합니다.

세 메서드 모두 `$sitePath`, `$siteName`, `$uri` 세 인수를 받습니다.  
`$sitePath`는 머신 내 사이트 전체 경로(예: `/Users/Lisa/Sites/my-project`)입니다.  
`$siteName`은 도메인의 "호스트" 또는 "사이트 이름" 부분(`my-project`)이며,  
`$uri`는 들어오는 요청 URI(`/foo/bar`)입니다.

커스텀 드라이버를 완성하면 `~/.config/valet/Drivers` 디렉토리에 `FrameworkValetDriver.php` 형식으로 저장하세요. 예를 들어 WordPress용 드라이버는 `WordPressValetDriver.php`여야 합니다.

아래는 각 필수 메서드의 예시 구현입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 드라이버가 해당 요청을 처리할지 판단해 `true` 또는 `false`를 반환해야 합니다. 이 메서드에서 주어진 `$sitePath`에 목표하는 프로젝트 유형이 있는지 확인합니다.

예를 들어 `WordPressValetDriver` 기준 `serves` 메서드는 다음과 같을 수 있습니다:

```
/**
 * 요청을 처리할 수 있는지 판단합니다.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile`은 들어오는 요청이 이미지나 CSS 같은 "정적 파일" 요청인지 판단합니다. 정적 파일이면 풀 경로를 반환하고, 아니면 `false`를 반환합니다:

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
> `isStaticFile` 메서드는 `serves`가 해당 요청에 대해 `true`를 반환하고 요청이 루트(`"/"`)가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러" (예: `index.php`)의 풀 경로를 반환해야 합니다:

```
/**
 * 애플리케이션의 프론트 컨트롤러 경로를 반환합니다.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### 로컬 드라이버 (Local Drivers)

단일 애플리케이션에만 적용할 커스텀 Valet 드라이버를 정의하려면 애플리케이션 루트에 `LocalValetDriver.php` 파일을 생성하세요. 이 드라이버는 기본 `ValetDriver` 클래스를 상속하거나 `LaravelValetDriver` 같은 기존 드라이버를 확장할 수 있습니다:

```
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * 요청 처리 여부를 판단합니다.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * 프론트 컨트롤러 경로를 반환합니다.
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

명령어  | 설명
------------- | -------------
`valet list` | Valet의 모든 명령어 목록을 표시합니다.
`valet diagnose` | Valet 디버그를 위한 진단 정보를 출력합니다.
`valet directory-listing` | 디렉토리 목록 표시 동작을 결정합니다. 기본값은 "off"로, 디렉토리 접근 시 404 페이지를 렌더링합니다.
`valet forget` | "park"된 디렉토리에서 이 명령을 실행해 해당 디렉토리를 비활성화합니다.
`valet log` | Valet 서비스가 기록하는 로그 목록을 확인합니다.
`valet paths` | "park"된 모든 경로를 봅니다.
`valet restart` | Valet 데몬들을 재시작합니다.
`valet start` | Valet 데몬들을 시작합니다.
`valet stop` | Valet 데몬들을 중지합니다.
`valet trust` | Brew와 Valet용 sudoers 파일을 추가해 비밀번호 입력 없이 명령어 실행을 허용합니다.
`valet uninstall` | Valet를 제거합니다. 수동 제거 안내도 표시합니다. `--force` 옵션으로 모든 Valet 자원을 강제로 삭제할 수 있습니다.

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉토리 및 파일 (Valet Directories and Files)

Valet 환경 문제 해결 시 아래 디렉토리 및 파일 정보를 참고하면 도움이 됩니다.

#### `~/.config/valet`

Valet의 모든 설정이 담긴 디렉토리입니다. 백업 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DnsMasq 설정 파일이 위치합니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버가 위치하는 디렉토리입니다. 드라이버는 특정 프레임워크나 CMS 서비스 방식을 결정합니다.

#### `~/.config/valet/Nginx/`

Valet Nginx 사이트 설정 파일이 위치합니다. `install` 및 `secure` 명령어 실행 시 재생성됩니다.

#### `~/.config/valet/Sites/`

[link 명령어](#the-link-command)로 연결한 프로젝트들의 심볼릭 링크가 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 메인 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet Nginx에서 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류에 관한 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류에 관한 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 관련 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 오류 로그가 저장되는 디렉토리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

각종 PHP 설정용 `*.ini` 파일이 위치하는 디렉토리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 구성 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트 SSL 인증서 생성 시 기본으로 쓰이는 Nginx 설정 파일입니다.

<a name="disk-access"></a>
### 디스크 접근 권한 (Disk Access)

macOS 10.14 이후부터는 일부 파일 및 디렉토리에 대한 접근이 기본적으로 제한되어 있습니다. 제한 대상에는 데스크톱, 문서, 다운로드 디렉토리가 포함되며, 네트워크 볼륨 및 외장 볼륨 접근도 제한됩니다. 따라서 Valet는 사이트 폴더를 이러한 보호 대상 위치 밖에 두도록 권장합니다.

하지만 해당 위치에 사이트를 둬야 한다면, Nginx에 "전체 디스크 접근" 권한을 직접 부여해야 합니다. 그렇지 않으면 Nginx가 정적 자산을 서비스할 때 서버 오류나 예기치 않은 동작이 발생할 수 있습니다. 보통 macOS가 자동으로 접근 권한 부여를 요청하지만, 수동으로 하려면 `시스템 환경설정` > `보안 및 개인정보` > `개인정보 보호` 탭에서 `전체 디스크 접근`을 선택 후 Nginx 관련 항목을 활성화하세요.