# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [설치](#laravel-breeze-installation)
    - [Breeze & Blade](#breeze-and-blade)
    - [Breeze & React / Vue](#breeze-and-inertia)
    - [Breeze & Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록, 인증과 애플리케이션 스타터 키트를 제공하고 있습니다. 이 키트들은 사용자 등록과 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 구성해줍니다.

물론 이 스타터 키트를 사용하지 않고, Laravel을 새로 설치해 처음부터 직접 애플리케이션을 만들어도 무방합니다. 어느 쪽이든 멋진 결과물을 만드실 수 있을 거라 확신합니다!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 [인증 기능](/docs/9.x/authentication)을 최소한으로 간단하게 구현한 패키지입니다. 또한 Breeze에는 사용자 이름, 이메일 주소, 비밀번호를 업데이트할 수 있는 간단한 "프로필" 페이지도 포함되어 있습니다.

Laravel Breeze의 기본 뷰 레이어는 [Tailwind CSS](https://tailwindcss.com)로 스타일링된 단순한 [Blade 템플릿](/docs/9.x/blade)으로 구성되어 있습니다. 또는 Breeze를 이용해 Vue나 React와 [Inertia](https://inertiajs.com) 기반으로 애플리케이션을 구성할 수도 있습니다.

Breeze는 새 Laravel 애플리케이션 시작점으로 훌륭하며, Blade 템플릿을 [Laravel Livewire](https://laravel-livewire.com)로 한 단계 업그레이드하려는 프로젝트에도 적합한 선택입니다.

<img src="https://laravel.com/img/docs/breeze-register.png" />

#### Laravel 부트캠프

Laravel이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)를 활용해 보세요. Laravel Bootcamp는 Breeze를 사용해 첫 Laravel 애플리케이션을 만드는 과정을 단계별로 안내합니다. Laravel과 Breeze가 제공하는 모든 기능을 체험하기 좋은 방법입니다.

<a name="laravel-breeze-installation"></a>
### 설치 (Installation)

먼저, [새 Laravel 애플리케이션을 생성](/docs/9.x/installation)하고 데이터베이스 설정과 [마이그레이션 실행](/docs/9.x/migrations)을 완료하세요. 그 다음 Composer로 Laravel Breeze를 설치할 수 있습니다:

```shell
composer require laravel/breeze --dev
```

Breeze가 설치되면 아래 문서에서 다루는 여러 Breeze "스택" 중 하나를 골라 애플리케이션을 자동 구성할 수 있습니다.

<a name="breeze-and-blade"></a>
### Breeze & Blade

Composer를 통해 Laravel Breeze 패키지를 설치한 뒤에는 `breeze:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 인증 뷰와 라우트, 컨트롤러, 기타 리소스를 애플리케이션으로 퍼블리시합니다. Laravel Breeze는 모든 코드를 애플리케이션에 직접 복사하여, 기능과 구현에 대한 완전한 제어와 투명성을 제공합니다.

기본 Breeze "스택"은 Blade 스택이며, 단순한 [Blade 템플릿](/docs/9.x/blade)로 프런트엔드를 렌더링합니다. Blade 스택은 추가 인수 없이 `breeze:install` 명령어만 실행해도 설치할 수 있습니다. Breeze 자동 구성 후에는 프런트엔드 자산도 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

다음으로 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` URL로 접속해 보세요. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="dark-mode"></a>
#### 다크 모드

Breeze를 사용해 애플리케이션 프런트엔드를 구성할 때 "다크 모드" 지원을 포함하고 싶다면, `breeze:install` 명령 실행 시 `--dark` 옵션을 추가하면 됩니다:

```shell
php artisan breeze:install --dark
```

> [!NOTE]
> 애플리케이션의 CSS와 JavaScript 컴파일 방법에 대해 더 알고 싶다면 Laravel의 [Vite 문서](/docs/9.x/vite#running-vite)를 참고하세요.

<a name="breeze-and-inertia"></a>
### Breeze & React / Vue

Laravel Breeze는 [Inertia](https://inertiajs.com)를 활용한 React와 Vue 프런트엔드 스캐폴딩도 지원합니다. Inertia는 전통적인 서버 라우트 및 컨트롤러를 사용하면서도 최신의 단일 페이지 React와 Vue 애플리케이션을 만들 수 있게 도와줍니다.

Inertia 덕분에 React와 Vue의 프런트엔드 강력함을 Laravel의 뛰어난 백엔드 생산성과 빠른 [Vite](https://vitejs.dev) 자산 컴파일과 결합할 수 있습니다. Inertia 스택을 사용하려면 `breeze:install` Artisan 명령에 원하는 스택으로 `vue` 혹은 `react`를 지정하세요. Breeze 구성 완료 후에는 역시 프런트엔드 자산을 컴파일해야 합니다:

```shell
php artisan breeze:install vue

# 또는

php artisan breeze:install react

php artisan migrate
npm install
npm run dev
```

그다음 웹 브라우저에서 애플리케이션 `/login` 또는 `/register` URL에 접속하세요. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의됩니다.

<a name="server-side-rendering"></a>
#### 서버 사이드 렌더링

Breeze가 [Inertia SSR](https://inertiajs.com/server-side-rendering)을 지원하도록 구성하려면, `breeze:install` 명령어 실행 시 `ssr` 옵션을 더해주면 됩니다:

```shell
php artisan breeze:install vue --ssr
php artisan breeze:install react --ssr
```

<a name="breeze-and-next"></a>
### Breeze & Next.js / API

Laravel Breeze는 Next.js, Nuxt와 같은 최신 자바스크립트 애플리케이션을 인증할 수 있는 API를 스캐폴딩할 수도 있습니다. 시작하려면 `breeze:install` Artisan 명령에 `api` 스택을 지정하세요:

```shell
php artisan breeze:install api

php artisan migrate
```

설치 과정에서 Breeze는 애플리케이션 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 변수에는 JavaScript 애플리케이션 URL을 입력해야 하며, 보통 로컬 개발 시 `http://localhost:3000`이 됩니다. 또한 `APP_URL`은 Artisan `serve` 명령어의 기본 URL인 `http://localhost:8000`으로 설정되어 있는지 확인해야 합니다.

<a name="next-reference-implementation"></a>
#### Next.js 참조 구현

마지막으로, 원하는 프런트엔드와 이 백엔드를 연결할 준비가 된 것입니다. Breeze 프런트엔드의 Next.js 참조 구현은 [GitHub에서 확인할 수 있습니다](https://github.com/laravel/breeze-next). 이 프런트엔드는 Laravel에서 공식 유지 관리하며, 기존의 Blade와 Inertia 스택과 동일한 사용자 인터페이스를 제공합니다.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Breeze가 간단하고 최소한의 시작점을 제공하는 반면, Jetstream은 좀 더 강력한 기능과 다양한 프런트엔드 기술 스택을 추가로 제공합니다. **Laravel을 처음 접하는 분이라면, Laravel Breeze로 기본기를 다진 후 Jetstream으로 넘어가는 것을 권장합니다.**

Jetstream은 세련된 디자인의 애플리케이션 스캐폴딩을 제공하며 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 선택적 팀 관리 기능을 포함합니다. Tailwind CSS로 설계되었고, 프런트엔드 스캐폴딩은 [Livewire](https://laravel-livewire.com) 또는 [Inertia](https://inertiajs.com) 중 원하는 방식을 선택할 수 있습니다.

Laravel Jetstream 설치에 관한 완전한 문서는 [공식 Jetstream 문서](https://jetstream.laravel.com/introduction.html)에서 확인할 수 있습니다.