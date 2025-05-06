# 스타터 키트

- [소개](#introduction)
- [라라벨 브리즈](#laravel-breeze)
    - [설치](#laravel-breeze-installation)
    - [브리즈 & 블레이드](#breeze-and-blade)
    - [브리즈 & React / Vue](#breeze-and-inertia)
    - [브리즈 & Next.js / API](#breeze-and-next)
- [라라벨 젯스트림](#laravel-jetstream)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션을 보다 빠르게 구축할 수 있도록, 인증 및 애플리케이션 스타터 키트를 제공합니다. 이 키트는 애플리케이션의 사용자 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 스캐폴딩해줍니다.

이 스타터 키트는 선택 사항이며, 반드시 사용해야 하는 것은 아닙니다. Laravel의 새 복사본을 설치하고 원하는 방식으로 애플리케이션을 처음부터 직접 만들 수도 있습니다. 어떤 방법을 선택하든, 훌륭한 결과물을 만들 수 있을 것이라 믿습니다!

<a name="laravel-breeze"></a>
## 라라벨 브리즈

[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 [인증 기능](/docs/{{version}}/authentication) 전체를 최소한의 간결한 구현으로 제공합니다. 또한 사용자가 이름, 이메일 주소, 비밀번호를 변경할 수 있는 간단한 "프로필" 페이지도 포함되어 있습니다.

Laravel Breeze의 기본 뷰 레이어는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. 또한, Breeze는 Vue 또는 React와 [Inertia](https://inertiajs.com)를 활용하여 애플리케이션을 스캐폴딩할 수도 있습니다.

Breeze는 새로운 Laravel 애플리케이션의 시작점으로 훌륭하며, [Laravel Livewire](https://laravel-livewire.com)와 함께 Blade 템플릿을 더욱 발전시키고자 하는 프로젝트에도 탁월한 선택입니다.

<img src="https://laravel.com/img/docs/breeze-register.png">

#### 라라벨 부트캠프

Laravel이 처음이라면 [라라벨 부트캠프](https://bootcamp.laravel.com)에서 시작해 보세요. 라라벨 부트캠프는 Breeze를 활용하여 첫 Laravel 애플리케이션을 만드는 과정을 안내해줍니다. Laravel과 Breeze가 제공하는 모든 기능을 체험해볼 수 있는 좋은 방법입니다.

<a name="laravel-breeze-installation"></a>
### 설치

먼저 [새로운 Laravel 애플리케이션을 생성](/docs/{{version}}/installation)하고, 데이터베이스를 설정한 뒤, [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행하세요. 새로운 Laravel 애플리케이션을 만든 후, Composer를 사용하여 Laravel Breeze를 설치할 수 있습니다:

```shell
composer require laravel/breeze --dev
```

Breeze가 설치되면, 아래 문서에서 설명하는 Breeze의 "스택" 중 하나로 애플리케이션을 스캐폴딩할 수 있습니다.

<a name="breeze-and-blade"></a>
### 브리즈 & 블레이드

Composer로 Laravel Breeze 패키지를 설치한 후, `breeze:install` 아티즌 명령을 실행할 수 있습니다. 이 명령은 인증 뷰, 라우트, 컨트롤러, 기타 리소스를 애플리케이션에 퍼블리시합니다. Laravel Breeze는 모든 코드를 애플리케이션 내에 퍼블리시하여, 모든 기능 및 구현을 완전히 제어하고 확인할 수 있습니다.

기본 Breeze "스택"은 Blade 스택으로, 간단한 [Blade 템플릿](/docs/{{version}}/blade)을 사용하여 프론트엔드를 렌더링합니다. `breeze:install` 명령을 추가 인수 없이 실행하면 Blade 스택이 설치됩니다. Breeze 스캐폴딩 설치 후에는 프론트엔드 에셋도 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

이제 웹 브라우저에서 `/login` 또는 `/register` URL로 이동해볼 수 있습니다. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="dark-mode"></a>
#### 다크 모드

프론트엔드를 스캐폴딩할 때 Breeze가 "다크 모드"를 지원하도록 하려면, `breeze:install` 명령 실행 시 `--dark` 옵션을 추가해 주세요:

```shell
php artisan breeze:install --dark
```

> **참고**
> 애플리케이션의 CSS 및 JavaScript 컴파일에 관해 더 알아보고 싶다면, Laravel의 [Vite 문서](/docs/{{version}}/vite#running-vite)를 참고하세요.

<a name="breeze-and-inertia"></a>
### 브리즈 & React / Vue

Laravel Breeze는 [Inertia](https://inertiajs.com) 프론트엔드 구현을 통해 React 및 Vue의 스캐폴딩도 제공합니다. Inertia를 사용하면, 기존 서버 사이드 라우팅과 컨트롤러를 활용하며 현대적인 싱글 페이지 React와 Vue 애플리케이션을 만들 수 있습니다.

Inertia는 React와 Vue의 강력한 프론트엔드 기능은 물론, Laravel의 놀라운 백엔드 생산성과 초고속 [Vite](https://vitejs.dev) 컴파일을 모두 누릴 수 있게 해줍니다. Inertia 스택을 사용하려면, `breeze:install` 아티즌 명령 실행 시 원하는 스택을 `vue` 또는 `react`로 지정하세요. Breeze 스캐폴딩 설치 후에는 프론트엔드 에셋도 컴파일해야 합니다:

```shell
php artisan breeze:install vue

# 또는...

php artisan breeze:install react

php artisan migrate
npm install
npm run dev
```

이제 웹 브라우저에서 `/login` 또는 `/register` URL로 이동해볼 수 있습니다. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

<a name="server-side-rendering"></a>
#### 서버 사이드 렌더링

[Inertia SSR](https://inertiajs.com/server-side-rendering) 지원도 Breeze에서 스캐폴딩할 수 있습니다. `breeze:install` 명령 실행 시 `ssr` 옵션을 추가하면 됩니다:

```shell
php artisan breeze:install vue --ssr
php artisan breeze:install react --ssr
```

<a name="breeze-and-next"></a>
### 브리즈 & Next.js / API

Laravel Breeze는 [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등 최신 JavaScript 애플리케이션과 연동 가능한 인증 API 스캐폴딩도 지원합니다. 시작하려면, `breeze:install` 아티즌 명령 실행 시 원하는 스택으로 `api`를 지정하세요:

```shell
php artisan breeze:install api

php artisan migrate
```

설치 과정에서 Breeze가 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 URL은 JavaScript 애플리케이션의 URL이어야 하며, 로컬 개발 시 보통 `http://localhost:3000`이 됩니다. 또한, `APP_URL`이 `http://localhost:8000`(기본 `serve` 아티즌 명령 사용 시의 URL)으로 설정되어 있는지 꼭 확인하세요.

<a name="next-reference-implementation"></a>
#### Next.js 레퍼런스 구현체

이제 원하는 프론트엔드와 백엔드를 연결할 준비가 되었습니다. Breeze 프론트엔드의 Next 레퍼런스 구현은 [GitHub에서 확인](https://github.com/laravel/breeze-next)할 수 있습니다. 이 프론트엔드는 Laravel이 직접 관리하며, Breeze의 전통적인 Blade 및 Inertia 스택과 동일한 사용자 인터페이스를 제공합니다.

<a name="laravel-jetstream"></a>
## 라라벨 젯스트림

Laravel Breeze가 간단하고 최소한의 시작점을 제공한다면, Jetstream은 더 강력한 기능과 추가 프론트엔드 기술 스택을 제공합니다. **Laravel을 처음 접하는 경우, 먼저 Laravel Breeze로 기본을 익힌 후 Jetstream을 사용하는 것을 권장합니다.**

Jetstream은 멋지게 디자인된 애플리케이션 스캐폴딩을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum 기반의 API 지원, 선택적인 팀 관리 기능을 포함합니다. Jetstream은 [Tailwind CSS](https://tailwindcss.com)로 디자인되었으며, [Livewire](https://laravel-livewire.com) 또는 [Inertia](https://inertiajs.com) 기반 프론트엔드 스캐폴딩 중 원하는 방식을 선택할 수 있습니다.

Laravel Jetstream 설치에 대한 전체 문서는 [공식 Jetstream 문서](https://jetstream.laravel.com/introduction.html)에서 확인할 수 있습니다.