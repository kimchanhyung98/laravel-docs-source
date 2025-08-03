# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [설치](#laravel-breeze-installation)
    - [Breeze와 Blade](#breeze-and-blade)
    - [Breeze와 Livewire](#breeze-and-livewire)
    - [Breeze와 React / Vue](#breeze-and-inertia)
    - [Breeze와 Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록, 인증 및 애플리케이션 스타터 키트를 제공합니다. 이 키트들은 사용자 등록과 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 생성해 줍니다.

이 스타터 키트들은 자유롭게 사용할 수 있지만 필수는 아닙니다. 새 Laravel을 설치해 애플리케이션을 처음부터 직접 구축하는 것도 가능합니다. 어느 쪽을 선택하든 멋진 결과물을 만드시리라 확신합니다!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 [인증 기능](/docs/10.x/authentication)을 최소한으로 간단하게 구현한 패키지입니다. 또한, 사용자가 자신의 이름, 이메일 주소, 비밀번호를 수정할 수 있는 간단한 "프로필" 페이지도 포함합니다.

Laravel Breeze의 기본 뷰는 [Blade 템플릿](/docs/10.x/blade)으로 구성되며, [Tailwind CSS](https://tailwindcss.com)로 스타일링되어 있습니다. 또한 Breeze는 [Livewire](https://livewire.laravel.com)와 [Inertia](https://inertiajs.com)를 기반으로 한 스캐폴딩 옵션을 제공하며, Inertia 기반에서는 Vue 또는 React 중 하나를 선택할 수 있습니다.

<img src="https://laravel.com/img/docs/breeze-register.png" />

#### Laravel 부트캠프

Laravel이 처음이라면 [Laravel Bootcamp](https://bootcamp.laravel.com)를 이용해 보세요. Laravel Bootcamp에서는 Breeze를 사용해 Laravel 애플리케이션을 처음부터 만드는 과정을 단계별로 안내합니다. Laravel과 Breeze가 제공하는 모든 기능을 한눈에 살펴볼 수 있는 좋은 기회입니다.

<a name="laravel-breeze-installation"></a>
### 설치 (Installation)

먼저, [새 Laravel 애플리케이션을 생성](/docs/10.x/installation)하고, 데이터베이스를 설정한 후, [마이그레이션](/docs/10.x/migrations)을 실행하세요. 새 Laravel 앱을 만든 후, Composer를 사용해 Laravel Breeze를 설치할 수 있습니다:

```shell
composer require laravel/breeze --dev
```

Composer로 Laravel Breeze 패키지를 설치한 뒤에는 `breeze:install` Artisan 명령어를 실행하세요. 이 명령어는 인증 관련 뷰, 라우트, 컨트롤러 등 리소스를 애플리케이션에 게시합니다. Breeze의 모든 코드는 게시되어, 기능과 구현 방식을 직접 제어하고 확인할 수 있습니다.

`breeze:install` 명령어 실행 시 프론트엔드 스택과 테스트 프레임워크를 선택하는 안내가 표시됩니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
### Breeze와 Blade

기본 Breeze "스택"은 Blade 스택으로, 간단한 [Blade 템플릿](/docs/10.x/blade)을 이용해 애플리케이션의 프론트엔드를 렌더링합니다. Blade 스택은 `breeze:install` 명령어를 별도의 인수 없이 실행하고 Blade 프론트엔드 스택을 선택하면 설치할 수 있습니다. Breeze 스캐폴딩 설치 후에는 프론트엔드 자산도 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

이후 브라우저에서 애플리케이션의 `/login` 또는 `/register` URL에 접속할 수 있습니다. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

> [!NOTE]  
> CSS와 JavaScript 컴파일에 대해 더 알고 싶다면 Laravel의 [Vite 문서](/docs/10.x/vite#running-vite)를 확인하세요.

<a name="breeze-and-livewire"></a>
### Breeze와 Livewire

Laravel Breeze는 또한 [Livewire](https://livewire.laravel.com) 스캐폴딩도 제공합니다. Livewire는 PHP만으로 동적이고 반응적인 프론트엔드 UI를 만들 수 있는 강력한 방법입니다.

Livewire는 주로 Blade 템플릿을 사용하는 팀에게 적합하며, Vue나 React 같은 JavaScript SPA 프레임워크보다 더 간단한 대안을 찾는 곳에 이상적입니다.

Livewire 스택을 사용하려면 `breeze:install` Artisan 명령어 실행 시 Livewire 프론트엔드 스택을 선택하세요. 스캐폴딩 설치 후에는 데이터베이스 마이그레이션을 실행해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
### Breeze와 React / Vue

Laravel Breeze는 [Inertia](https://inertiajs.com) 기반 프론트엔드 구현을 통해 React와 Vue 스캐폴딩도 제공합니다. Inertia를 사용하면 기존 서버 사이드 라우팅과 컨트롤러를 유지하면서 최신 React 및 Vue 싱글 페이지 애플리케이션을 구축할 수 있습니다.

Inertia는 React와 Vue의 프론트엔드 강력함과 Laravel의 백엔드 생산성, 그리고 빠른 [Vite](https://vitejs.dev) 컴파일을 결합해 줍니다. Inertia 스택을 사용하려면 `breeze:install` 명령어 실행 시 Vue 또는 React 프론트엔드 스택을 선택하세요.

Vue 또는 React 스택 선택 시, Breeze 설치 프로그램은 [Inertia SSR](https://inertiajs.com/server-side-rendering) 또는 TypeScript 지원 여부를 묻습니다. 스캐폴딩 설치 후에는 프론트엔드 자산을 컴파일하는 것이 좋습니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

이후 브라우저에서 애플리케이션의 `/login` 또는 `/register` URL에 접속할 수 있습니다. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="breeze-and-next"></a>
### Breeze와 Next.js / API

Laravel Breeze는 Next.js, Nuxt 등 최신 JavaScript 애플리케이션을 인증할 준비가 된 인증 API 스캐폴딩도 지원합니다. 시작하려면 `breeze:install` Artisan 명령어 실행 시 API 스택을 선택하세요:

```shell
php artisan breeze:install

php artisan migrate
```

설치 과정에서 Breeze는 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 URL은 JavaScript 애플리케이션의 URL이어야 하며, 일반적으로 로컬 개발 중에는 `http://localhost:3000`이 됩니다. 또한 `APP_URL`이 `http://localhost:8000`로 설정되어 있어야 하며, 이는 기본적으로 `serve` Artisan 명령어가 사용하는 URL입니다.

<a name="next-reference-implementation"></a>
#### Next.js 참고 구현

마지막으로, 이 백엔드를 원하는 프론트엔드와 연결할 준비가 되었습니다. Breeze 프론트엔드의 Next.js 참고 구현이 [GitHub에서 제공됩니다](https://github.com/laravel/breeze-next). 이 프론트엔드는 Laravel이 직접 관리하며, 기존 Breeze가 제공하는 Blade 및 Inertia 스택과 동일한 사용자 인터페이스를 포함합니다.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Breeze가 간단하고 최소한의 시작점을 제공한다면, Jetstream은 더 강력한 기능과 추가 프론트엔드 기술 스택으로 확장합니다. **Laravel을 처음 접하는 분께는 Laravel Breeze를 숙지한 후 Laravel Jetstream으로 넘어갈 것을 권장합니다.**

Jetstream은 세련된 디자인의 Laravel 애플리케이션 스캐폴딩을 제공하며 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 선택적 팀 관리 기능을 포함합니다. Jetstream은 [Tailwind CSS](https://tailwindcss.com)를 사용하여 디자인되었고, [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com)를 기반으로 프론트엔드 스캐폴딩을 선택할 수 있습니다.

Laravel Jetstream 설치에 관한 완전한 문서는 [공식 Jetstream 문서](https://jetstream.laravel.com)에서 확인할 수 있습니다.