# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 서비스](#serving-sites)
    - [“Park” 명령어](#the-park-command)
    - [“Link” 명령어](#the-link-command)
    - [TLS로 사이트 보안](#securing-sites)
    - [기본 사이트 서비스](#serving-a-default-site)
- [사이트 공유](#sharing-sites)
    - [Ngrok을 통한 사이트 공유](#sharing-sites-via-ngrok)
    - [Expose를 통한 사이트 공유](#sharing-sites-via-expose)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시](#proxying-services)
- [사용자 정의 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉터리 및 파일](#valet-directories-and-files)

<a name="introduction"></a>
## 소개

[Laravel Valet](https://github.com/laravel/valet)는 macOS 미니멀리스트를 위한 개발 환경입니다. Laravel Valet은 Mac이 시작될 때마다 [Nginx](https://www.nginx.com/)가 백그라운드에서 항상 실행되도록 구성합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용하여, Valet은 모든 `*.test` 도메인 요청을 로컬 머신에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7MB의 RAM만 차지하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/{{version}}/sail)이나 [Homestead](/docs/{{version}}/homestead)를 완전히 대체하지는 않지만, 유연한 기본 설정을 원하거나 매우 빠른 속도를 선호하거나 메모리가 제한된 기기에서 작업하는 경우 훌륭한 대안입니다.

기본적으로 Valet은 다음과 같은 다양한 프로젝트를 지원합니다(이에만 국한되지 않음):

<style>
    #valet-support > ul {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        line-height: 1.9;
    }
</style>

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
- 정적 HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

또한, 직접 [사용자 정의 드라이버](#custom-valet-drivers)를 추가하여 Valet을 확장할 수 있습니다.

<a name="installation"></a>
## 설치

> {note} Valet은 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전, Apache나 Nginx 같은 프로그램이 로컬 머신의 80번 포트를 사용하고 있지 않은지 반드시 확인하십시오.

먼저 Homebrew를 최신 버전으로 업데이트해야 합니다. 다음 명령어를 사용하세요:

    brew update

다음으로 Homebrew를 사용하여 PHP를 설치합니다:

    brew install php

PHP 설치 후, [Composer 패키지 관리자](https://getcomposer.org)를 설치할 준비가 되었습니다. 또한, `~/.composer/vendor/bin` 디렉터리가 시스템의 "PATH"에 포함되어 있는지 확인하세요. Composer 설치가 끝나면, Laravel Valet을 글로벌 Composer 패키지로 설치할 수 있습니다:

    composer global require laravel/valet

마지막으로 Valet의 `install` 명령어를 실행하세요. 이 명령어는 Valet과 DnsMasq를 구성 및 설치합니다. 또한, Valet이 의존하는 데몬들이 시스템 시작 시 자동으로 실행되도록 설정됩니다:

    valet install

Valet 설치 후, 터미널에서 `ping foobar.test`와 같은 명령어로 어떤 `*.test` 도메인을 핑 해보세요. Valet이 제대로 설치되었다면 `127.0.0.1` 주소로 응답합니다.

Valet은 컴퓨터가 부팅될 때마다 자동으로 필요한 서비스를 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

Valet은 `valet use php@버전` 명령어로 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 설치되어 있지 않으면 Homebrew를 통해 설치됩니다:

    valet use php@7.2

    valet use php

프로젝트 루트에 `.valetphprc` 파일을 생성하여 사이트에서 사용할 PHP 버전을 명시할 수도 있습니다:

    php@7.2

이 파일을 만든 후 `valet use` 명령어를 실행하면, 해당 파일을 읽어 사이트별로 선호하는 PHP 버전을 자동으로 적용합니다.

> {note} 여러 PHP 버전이 설치되어 있어도 Valet은 한 번에 하나의 PHP 버전만 서비스할 수 있습니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에서 데이터베이스가 필요하다면, [DBngin](https://dbngin.com)을 살펴보세요. DBngin은 MySQL, PostgreSQL, Redis를 포함하는 무료 통합 데이터베이스 관리 툴입니다. DBngin 설치 후, `127.0.0.1`에서 사용자명 `root`와 빈 문자열을 비밀번호로 데이터베이스에 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet 설치가 제대로 작동하지 않을 경우, `composer global update` 명령어에 이어 `valet install`을 실행하면 설치를 초기화할 수 있습니다. 드물게, `valet uninstall --force` 후 `valet install`을 실행하는 "강제 초기화"가 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

Valet을 업그레이드하려면 터미널에서 `composer global update`를 실행하세요. 업그레이드 후에는 `valet install` 명령어를 실행하여, 필요시 구성이 추가로 업데이트될 수 있도록 하는 것이 좋습니다.

<a name="serving-sites"></a>
## 사이트 서비스

Valet이 설치되면, Laravel 애플리케이션 서비스를 시작할 준비가 완료된 것입니다. Valet은 애플리케이션 서비스를 위한 두 가지 명령어, `park`와 `link`,를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션이 들어있는 디렉터리를 등록합니다. 디렉터리를 Valet에 "파킹"하면, 하위의 모든 디렉터리에 웹브라우저로 `http://<디렉터리-이름>.test` 형태로 접근할 수 있습니다:

    cd ~/Sites

    valet park

이것으로 끝입니다. 이제 "파킹"된 디렉터리에 새 애플리케이션을 만들면, 자동으로 `http://<디렉터리-이름>.test` 규칙으로 서비스됩니다. 예를 들어, "laravel"이라는 디렉터리가 있다면 `http://laravel.test`으로 접속할 수 있습니다. 또한, Valet은 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 허용합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어도 Laravel 애플리케이션을 서비스할 때 사용할 수 있습니다. 이 명령어는 특정 사이트(디렉터리)만 서비스하고 싶을 때 유용합니다:

    cd ~/Sites/laravel

    valet link

이렇게 연결한 뒤에는 디렉터리 이름을 이용해 `http://laravel.test`로 접속할 수 있습니다. 마찬가지로, 와일드카드 서브도메인(`http://foo.laravel.test`)도 지원됩니다.

다른 호스트 이름으로 서비스를 원한다면, `link` 명령어에 호스트 이름을 지정할 수 있습니다. 예를 들어, 아래와 같이 하면 `http://application.test`로 접속할 수 있습니다:

    cd ~/Sites/laravel

    valet link application

연결된 모든 디렉터리 목록을 보려면 `links` 명령어를 사용하세요:

    valet links

사이트의 심볼릭 링크를 삭제하려면 `unlink` 명령어를 사용합니다:

    cd ~/Sites/laravel

    valet unlink

<a name="securing-sites"></a>
### TLS로 사이트 보안

기본적으로 Valet은 HTTP로 사이트를 서비스합니다. 그러나 암호화된 TLS(HTTP/2)로 사이트를 서비스하고 싶다면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 사이트를 보호하려면 다음 명령어를 실행합니다:

    valet secure laravel

사이트의 보안을 해제하고 다시 평문 HTTP로 되돌리려면 `unsecure` 명령어를 사용합니다. 아래와 같이 도메인을 지정하세요:

    valet unsecure laravel

<a name="serving-a-default-site"></a>
### 기본 사이트 서비스

알 수 없는 `test` 도메인으로 접속했을 때 `404` 대신 "기본" 사이트가 서비스되도록 Valet을 설정할 수 있습니다. 이를 위해 `~/.config/valet/config.json` 설정 파일에 기본 사이트의 경로를 나타내는 `default` 옵션을 추가하세요:

    "default": "/Users/Sally/Sites/foo",

<a name="sharing-sites"></a>
## 사이트 공유

Valet에는 로컬 사이트를 전 세계에 공유할 수 있는 명령어가 포함되어 있습니다. 이를 통해 모바일 기기에서 사이트를 테스트하거나, 팀원 및 고객에게 쉽게 공유할 수 있습니다.

<a name="sharing-sites-via-ngrok"></a>
### Ngrok을 통한 사이트 공유

사이트를 공유하려면, 터미널에서 사이트의 디렉터리로 이동한 후 Valet의 `share` 명령어를 실행하세요. 공개 접근 가능한 URL이 클립보드에 복사되어 붙여넣기 하거나 팀과 공유할 수 있습니다:

    cd ~/Sites/laravel

    valet share

공유를 중지하려면 `Control + C`를 누르세요. Ngrok를 이용해 사이트를 공유하려면 [Ngrok 계정 생성](https://dashboard.ngrok.com/signup) 및 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다.

> {tip} `valet share --region=eu`처럼 share 명령어에 추가 Ngrok 매개변수를 전달할 수 있습니다. 자세한 내용은 [ngrok 공식 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
### Expose를 통한 사이트 공유

[Expose](https://expose.dev)가 설치된 경우, 터미널에서 사이트 디렉터리로 이동 후 `expose` 명령어를 실행해 사이트를 공유할 수 있습니다. 추가 명령줄 매개변수는 [Expose 공식 문서](https://expose.dev/docs)를 참고하세요. 공유 후, Expose가 공유 가능한 URL을 출력해주는데, 이를 다른 기기나 팀원과 공유하면 됩니다:

    cd ~/Sites/laravel

    expose

공유를 중지하려면 `Control + C`를 누르세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

Valet은 기본적으로 로컬 개발 머신이 외부에 노출되어 보안 위험이 초래되지 않도록, 내부 `127.0.0.1` 인터페이스로 들어오는 트래픽만 허용합니다.

로컬 네트워크 내 다른 기기에서 Valet 사이트에 접속하려면(예: `192.168.1.10/application.test`), 해당 사이트의 Nginx 설정 파일에서 `listen` 디렉티브의 `127.0.0.1:` 접두사를 제거하여 제한을 해제해야 합니다.

프로젝트에서 `valet secure`를 실행하지 않은 경우, `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정하여 모든 HTTP(비HTTPS) 사이트의 네트워크 접근을 열 수 있습니다. 만약 해당 사이트를 HTTPS로 서빙 중이라면(`valet secure` 실행됨), `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

Nginx 설정을 수정한 후에는 `valet restart` 명령어로 변경 사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

다른 프레임워크를 사용하는 일부 애플리케이션은 서버 환경 변수에 의존하지만, 프로젝트 내에서 해당 변수를 구성할 수 없는 경우가 많습니다. Valet은 프로젝트 루트에 `.valet-env.php` 파일을 추가하여 사이트별 환경 변수를 설정할 수 있게 해줍니다. 이 파일은 각 사이트명/환경 변수 쌍의 배열을 반환해야 하며, 배열에 지정된 각 사이트에 대해 글로벌 `$_SERVER` 배열에 추가됩니다:

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

때로는 Valet 도메인을 로컬 머신 내 다른 서비스로 프록시하고 싶을 수 있습니다. 예를 들어, 별도의 사이트를 Docker에서 실행해야 하는 상황이 있을 수 있지만, Valet과 Docker가 동시에 80번 포트를 사용할 수는 없습니다.

이럴 때는 `proxy` 명령어로 프록시를 설정할 수 있습니다. 예를 들어, `http://elasticsearch.test`의 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하려면:

```bash
// HTTP로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

// TLS + HTTP/2로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 제거하려면 `unproxy` 명령어를 사용하세요:

    valet unproxy elasticsearch

프록시된 모든 사이트 구성을 보려면 `proxies` 명령어를 사용하세요:

    valet proxies

<a name="custom-valet-drivers"></a>
## 사용자 정의 Valet 드라이버

Valet이 기본적으로 지원하지 않는 프레임워크나 CMS로 작성된 PHP 애플리케이션을 서비스할 수 있도록, 직접 Valet “드라이버”를 작성할 수 있습니다. Valet 설치 시, `~/.config/valet/Drivers` 디렉터리가 생성되며 이곳에는 예시 드라이버인 `SampleValetDriver.php`가 포함되어 있습니다. 커스텀 드라이버 작성 시 세 가지 메서드(`serves`, `isStaticFile`, `frontControllerPath`)를 구현하면 됩니다.

세 메서드 모두 `$sitePath`, `$siteName`, `$uri`를 인수로 받습니다. `$sitePath`는 서비스 중인 사이트의 전체 경로(예: `/Users/Lisa/Sites/my-project`), `$siteName`은 도메인의 "호스트"/"사이트 이름" 부분(`my-project`), `$uri`는 요청 URI(`/foo/bar`)입니다.

사용자 정의 Valet 드라이버를 완성했다면, `~/.config/valet/Drivers` 디렉터리에 `FrameworkValetDriver.php` 패턴의 파일명으로 저장하세요. 예를 들면, WordPress용 드라이버라면 `WordPressValetDriver.php`입니다.

아래는 각 메서드의 샘플 구현입니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 드라이버가 들어오는 요청을 처리해야 하는지 `true`/`false`를 반환합니다. 이 메서드에서 `$sitePath`에 해당 프레임워크/프로젝트가 있는지 판별하면 됩니다.

예를 들어, `WordPressValetDriver`에서 `serves` 메서드는 이렇게 작성할 수 있습니다:

    /**
     * 드라이버가 요청을 처리해야 하는지 결정합니다.
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

`isStaticFile` 메서드는 요청이 "정적" 파일(이미지나 스타일시트 등)인지 판별합니다. 정적 파일이라면 해당 파일의 전체 경로를 반환하고, 아니라면 `false`를 반환합니다:

    /**
     * 요청이 정적 파일인지 판별합니다.
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

> {note} `isStaticFile` 메서드는 요청이 `/`가 아니고, `serves`가 `true`를 반환할 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"(`index.php` 등)의 전체 경로를 반환해야 합니다:

    /**
     * 애플리케이션의 프론트 컨트롤러 전체 경로를 반환
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

특정 애플리케이션만 위한 커스텀 Valet 드라이버를 정의하려면, 애플리케이션 루트에 `LocalValetDriver.php` 파일을 만드세요. 베이스 `ValetDriver` 클래스를 확장하거나, `LaravelValetDriver` 같은 기존 드라이버를 상속할 수 있습니다:

    class LocalValetDriver extends LaravelValetDriver
    {
        /**
         * 드라이버가 요청을 처리해야 하는지 판별
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
         * 애플리케이션의 프론트 컨트롤러 전체 경로를 반환
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

Command  | 설명
------------- | -------------
`valet forget` | "파킹"된 디렉터리에서 실행하여 파킹 디렉터리 목록에서 제거합니다.
`valet log` | Valet 서비스가 기록한 로그 목록을 봅니다.
`valet paths` | 모든 "파킹"된 경로를 출력합니다.
`valet restart` | Valet 데몬을 재시작합니다.
`valet start` | Valet 데몬을 시작합니다.
`valet stop` | Valet 데몬을 중지합니다.
`valet trust` | Valet 명령어를 실행할 때 비밀번호 입력 없이 실행할 수 있도록 Brew와 Valet용 sudoers 파일을 추가합니다.
`valet uninstall` | Valet을 제거합니다: 수동 삭제 안내를 표시합니다. `--force` 옵션을 추가하면 Valet의 모든 리소스를 강제로 삭제합니다.

<a name="valet-directories-and-files"></a>
## Valet 디렉터리 및 파일

Valet 환경에서 발생하는 문제를 해결할 때 다음 디렉터리 및 파일 정보가 도움될 수 있습니다:

#### `~/.config/valet`

Valet의 모든 설정이 저장되어 있습니다. 백업해두는 것을 추천합니다.

#### `~/.config/valet/dnsmasq.d/`

DNSMasq의 설정 파일이 들어 있습니다.

#### `~/.config/valet/Drivers/`

Valet의 드라이버가 저장되어 있습니다. 드라이버는 각 프레임워크/CMS 서비스 방식을 결정합니다.

#### `~/.config/valet/Extensions/`

사용자가 만든 Valet 확장/명령어가 저장됩니다.

#### `~/.config/valet/Nginx/`

Valet의 모든 Nginx 사이트 설정 파일이 있습니다. `install`, `secure`, `tld` 명령 시 이 파일들이 다시 빌드됩니다.

#### `~/.config/valet/Sites/`

[링크한 프로젝트](#the-link-command)에 대한 모든 심볼릭 링크가 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 마스터 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx가 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상 작동할 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 에러에 대한 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 에러에 대한 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 에러의 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 로그와 에러 로그가 저장되어 있습니다.

#### `/usr/local/etc/php/X.X/conf.d`

PHP 설정을 위한 `*.ini` 파일들이 저장되는 디렉터리입니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트의 SSL 인증서 생성을 위해 사용되는 기본 Nginx 설정 파일입니다.