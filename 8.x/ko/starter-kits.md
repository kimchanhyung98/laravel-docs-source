# 스타터 키트

- [소개](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [설치 방법](#laravel-breeze-installation)
    - [Breeze & Inertia](#breeze-and-inertia)
    - [Breeze & Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션을 빠르게 구축할 수 있도록, 인증 및 애플리케이션 스타터 키트를 제공합니다. 이 키트들은 회원가입 및 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 작성해줍니다.

이 스타터 키트는 선택 사항이며 사용하지 않아도 됩니다. Laravel의 새 복사본을 설치하는 것만으로 직접 애플리케이션을 구축할 수도 있습니다. 어떤 방식이든 여러분만의 멋진 작품을 만들 수 있을 것이라 믿습니다!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 초기화, 이메일 인증, 비밀번호 확인 등 Laravel의 [인증 기능](/docs/{{version}}/authentication) 전체를 최소하고 심플하게 구현한 번들입니다. Breeze의 기본 뷰 레이어는 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com) 스타일로 구성되어 있습니다.

Breeze는 새 Laravel 애플리케이션을 시작하기에 훌륭한 출발점이 되며, [Laravel Livewire](https://laravel-livewire.com) 등으로 Blade 템플릿을 한 단계 더 발전시키려는 프로젝트에도 적합합니다.

<a name="laravel-breeze-installation"></a>
### 설치 방법

먼저, [새 Laravel 애플리케이션을 생성](/docs/{{version}}/installation)하고, 데이터베이스를 설정한 뒤 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행하세요.

```bash
curl -s https://laravel.build/example-app | bash

cd example-app

php artisan migrate
```

새 Laravel 애플리케이션을 생성한 후 Composer를 통해 Breeze를 설치할 수 있습니다.

```bash
composer require laravel/breeze:1.9.2 
```

Composer로 Breeze 패키지가 설치되면, `breeze:install` Artisan 명령어를 실행하세요. 이 명령어는 인증 관련 뷰, 라우트, 컨트롤러 등 리소스를 애플리케이션에 게시합니다. Breeze는 모든 코드를 여러분의 프로젝트에 게시하므로, 모든 기능과 구현 방식에 대한 완전한 제어와 가시성을 확보할 수 있습니다. 설치 후에는 CSS 파일을 사용할 수 있도록 애셋도 컴파일해야 합니다.

```nothing
php artisan breeze:install

npm install
npm run dev
php artisan migrate
```

이후 웹 브라우저에서 `/login` 또는 `/register` 경로로 접속해보면 됩니다. Breeze에서 제공하는 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

> {tip} 애플리케이션의 CSS 및 JavaScript를 컴파일하는 방법은 [Laravel Mix 문서](/docs/{{version}}/mix#running-mix)를 참고하세요.

<a name="breeze-and-inertia"></a>
### Breeze & Inertia

Laravel Breeze는 또한 Vue 혹은 React로 구동되는 [Inertia.js](https://inertiajs.com) 기반 프론트엔드를 제공합니다. Inertia 스택을 사용하려면, `breeze:install` 명령어 실행 시 원하는 스택을 `vue` 또는 `react`로 지정하세요.

```nothing
php artisan breeze:install vue

// 또는...

php artisan breeze:install react

npm install
npm run dev
php artisan migrate
```

<a name="breeze-and-next"></a>
### Breeze & Next.js / API

Laravel Breeze는 [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등 최신 자바스크립트 애플리케이션을 인증할 수 있는 API 인증 스캐폴딩도 지원합니다. 시작하려면 `breeze:install` 명령어 실행 시 `api` 스택을 지정하세요.

```nothing
php artisan breeze:install api

php artisan migrate
```

설치 과정에서 Breeze는 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 값은 자바스크립트 애플리케이션의 URL이어야 하며, 로컬 개발 환경에서는 보통 `http://localhost:3000`이 됩니다.

<a name="next-reference-implementation"></a>
#### Next.js 참고 구현

마지막으로, 원하는 프론트엔드와 백엔드를 연결할 준비가 되었습니다. Breeze 프론트엔드의 Next.js 참고 구현이 [GitHub에서 제공](https://github.com/laravel/breeze-next)됩니다. 이 프론트엔드는 Laravel에서 관리하며, Breeze가 제공하는 전통적인 Blade, Inertia 스택과 동일한 사용자 인터페이스를 가지고 있습니다.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Breeze는 간단하고 미니멀한 출발점을 제공하는 데 반해, Jetstream은 더 강력한 기능과 다양한 프론트엔드 스택을 갖추고 있습니다. **Laravel을 처음 접한다면 Breeze부터 익힌 뒤 Jetstream으로 넘어가시는 것을 추천합니다.**

Jetstream은 아름답게 디자인된 Laravel용 애플리케이션 스캐폴딩을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 선택적 팀 관리까지 포함하고 있습니다. Jetstream은 [Tailwind CSS](https://tailwindcss.com)로 디자인되었으며, [Livewire](https://laravel-livewire.com) 또는 [Inertia.js](https://inertiajs.com) 기반 프론트엔드 중 선택하여 사용할 수 있습니다.

Jetstream 설치에 대한 자세한 문서는 [공식 Jetstream 문서](https://jetstream.laravel.com/introduction.html)에서 확인하실 수 있습니다.