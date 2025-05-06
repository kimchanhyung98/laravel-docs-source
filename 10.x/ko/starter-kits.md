# 스타터 킷

- [소개](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [설치](#laravel-breeze-installation)
    - [Breeze와 Blade](#breeze-and-blade)
    - [Breeze와 Livewire](#breeze-and-livewire)
    - [Breeze와 React / Vue](#breeze-and-inertia)
    - [Breeze와 Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션을 빠르게 시작할 수 있도록, 인증 및 애플리케이션 스타터 킷을 제공합니다. 이 킷들은 회원 등록과 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 생성해줍니다.

이러한 스타터 킷을 사용하는 것은 권장되지만 필수는 아닙니다. Laravel의 새로운 복사본만 설치하여 처음부터 애플리케이션을 직접 개발하실 수도 있습니다. 어떤 방법을 선택하셔도 멋진 결과를 만들어내실 것이라 확신합니다!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 [인증 기능](/docs/{{version}}/authentication) 전체를 간결하게 구현한 최소한의 스타터 킷입니다. 또한, 사용자가 자신의 이름, 이메일 주소, 비밀번호를 업데이트할 수 있는 간단한 "프로필" 페이지도 포함되어 있습니다.

Laravel Breeze의 기본 뷰 레이어는 [Tailwind CSS](https://tailwindcss.com)가 적용된 간단한 [Blade 템플릿](/docs/{{version}}/blade)으로 구성되어 있습니다. 또한, Breeze는 [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com)를 기반으로 한 스캐폴딩 옵션을 제공하며, Inertia 기반 스택에서는 Vue 또는 React 중에서 선택할 수 있습니다.

<img src="https://laravel.com/img/docs/breeze-register.png">

#### Laravel 부트캠프

Laravel이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)를 따라가며 Breeze를 사용하여 첫 Laravel 애플리케이션을 만들어 보는 것도 좋습니다. 이 부트캠프는 Laravel과 Breeze가 제공하는 모든 주요 기능을 한눈에 체험할 수 있는 좋은 기회입니다.

<a name="laravel-breeze-installation"></a>
### 설치

먼저, [새 Laravel 애플리케이션을 생성](/docs/{{version}}/installation)하고, 데이터베이스를 설정한 뒤 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행하세요. 새로운 Laravel 애플리케이션을 만든 후, Composer를 사용하여 Laravel Breeze를 설치할 수 있습니다:

```shell
composer require laravel/breeze --dev
```

Composer가 Laravel Breeze 패키지를 설치한 후에는 `breeze:install` Artisan 명령어를 실행할 수 있습니다. 이 명령은 인증 뷰, 라우트, 컨트롤러 등 각종 리소스를 프로젝트에 게시합니다. Breeze는 모든 코드를 애플리케이션에 직접 게시하므로, 기능과 구현 방식에 대해 완전히 제어할 수 있습니다.

`breeze:install` 명령을 실행하면 원하는 프론트엔드 스택과 테스트 프레임워크를 선택할 수 있습니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
### Breeze와 Blade

Breeze의 기본 "스택"은 Blade 스택으로, 간단한 [Blade 템플릿](/docs/{{version}}/blade)를 사용해 프론트엔드를 렌더링합니다. 추가 인자 없이 `breeze:install` 명령을 실행하고 Blade 프론트엔드 스택을 선택하면 설치할 수 있습니다. Breeze의 스캐폴딩을 설치한 후, 프론트엔드 에셋도 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

이제 웹 브라우저에서 `/login` 또는 `/register` URL로 이동해보세요. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

> [!NOTE]  
> 애플리케이션의 CSS와 JavaScript 컴파일에 대해 더 자세히 알고 싶다면, Laravel의 [Vite 문서](/docs/{{version}}/vite#running-vite)를 참고하세요.

<a name="breeze-and-livewire"></a>
### Breeze와 Livewire

Laravel Breeze는 [Livewire](https://livewire.laravel.com) 기반의 스캐폴딩도 제공합니다. Livewire는 오직 PHP만으로 동적이고 반응적인 프론트엔드 UI를 쉽게 구축할 수 있는 강력한 도구입니다.

Blade 템플릿을 주로 사용하는 팀이나, Vue, React 같은 JavaScript 기반 SPA 프레임워크보다 더 간단한 대안을 찾는 팀에게 Livewire는 훌륭한 선택입니다.

Livewire 스택을 사용하려면, `breeze:install` Artisan 명령을 실행할 때 Livewire 프론트엔드 스택을 선택하세요. Breeze의 스캐폴딩을 설치한 후, 데이터베이스 마이그레이션을 실행하면 됩니다:

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
### Breeze와 React / Vue

Laravel Breeze는 [Inertia](https://inertiajs.com) 프론트엔드 구현을 통해 React 및 Vue 기반의 스캐폴딩도 제공합니다. Inertia를 사용하면 전통적인 서버사이드 라우팅과 컨트롤러를 기반으로 현대적인 단일 페이지 React 또는 Vue 애플리케이션을 구축할 수 있습니다.

Inertia를 사용하면 React, Vue의 프론트엔드 혁신성과 Laravel의 생산성, 빠른 [Vite](https://vitejs.dev) 컴파일러를 함께 활용할 수 있습니다. Inertia 스택을 사용하려면, `breeze:install` 명령 실행 시 Vue 또는 React 프론트엔드 스택을 선택하세요.

Vue 또는 React 프론트엔드 스택을 선택하면, Breeze 설치 프로그램이 [Inertia SSR](https://inertiajs.com/server-side-rendering)이나 TypeScript 지원도 사용할지 물어봅니다. Breeze의 스캐폴딩을 설치한 뒤에는 프론트엔드 에셋을 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

이제 웹 브라우저에서 `/login` 또는 `/register` URL로 이동해보세요. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="breeze-and-next"></a>
### Breeze와 Next.js / API

Laravel Breeze는 [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등과 같은 최신 자바스크립트 애플리케이션에서 사용할 인증 API를 스캐폴딩할 수도 있습니다. 시작하려면 `breeze:install` 명령 실행 시 API 스택을 선택하세요:

```shell
php artisan breeze:install

php artisan migrate
```

설치 과정에서 Breeze는 앱의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 URL은 자바스크립트 애플리케이션의 주소이어야 하며, 로컬 개발 중에는 보통 `http://localhost:3000`이 됩니다. 또한, `APP_URL`이 `http://localhost:8000`(기본 `artisan serve` 명령으로 사용하는 URL)으로 설정되어 있는지 확인하세요.

<a name="next-reference-implementation"></a>
#### Next.js 참고 구현

마지막으로, 백엔드와 원하는 프론트엔드를 연동할 준비가 되었습니다. Breeze 프론트엔드의 Next 참고 구현은 [GitHub](https://github.com/laravel/breeze-next)에서 확인할 수 있습니다. 이 프론트엔드는 Laravel에서 공식적으로 관리하며, Breeze의 기존 Blade 및 Inertia 스택과 동일한 사용자 인터페이스를 제공합니다.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Breeze가 간단하고 미니멀한 시작점을 제공한다면, Jetstream은 여기에 더 탄탄한 기능과 다양한 프론트엔드 기술 스택을 추가해줍니다. **Laravel을 처음 접한다면, Jetstream에 입문하기 전에 먼저 Breeze로 학습하는 것을 권장합니다.**

Jetstream은 깔끔하게 디자인된 Laravel 애플리케이션 스캐폴딩을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 선택적으로 팀 관리 기능까지 포함합니다. Jetstream은 [Tailwind CSS](https://tailwindcss.com)로 설계되었으며, [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com) 기반 프론트엔드 스캐폴딩을 선택할 수 있습니다.

Laravel Jetstream 설치에 관한 전체 문서는 [공식 Jetstream 문서](https://jetstream.laravel.com)에서 확인할 수 있습니다.