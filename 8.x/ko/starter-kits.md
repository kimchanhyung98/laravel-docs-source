# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [Laravel Breeze](#laravel-breeze)
    - [설치](#laravel-breeze-installation)
    - [Breeze와 Inertia](#breeze-and-inertia)
    - [Breeze와 Next.js / API](#breeze-and-next)
- [Laravel Jetstream](#laravel-jetstream)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션을 빠르게 시작할 수 있도록, 인증(authentication)과 애플리케이션 스타터 키트를 제공하고 있습니다. 이 키트들은 애플리케이션 사용자 등록과 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 스캐폴딩(기본 구조 생성)해 줍니다.

이 스타터 키트를 사용하셔도 좋고, 꼭 사용해야 하는 것은 아닙니다. Laravel을 새로 설치하여 처음부터 직접 애플리케이션을 구축하셔도 무방합니다. 어떤 경로를 선택하시든 멋진 애플리케이션을 만드실 것이라 믿습니다!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 등록, 비밀번호 초기화, 이메일 검증, 비밀번호 확인 등 Laravel의 모든 [인증 기능](/docs/{{version}}/authentication)을 최소한의 간단한 형태로 구현한 패키지입니다. Breeze의 기본 뷰 레이어는 [Tailwind CSS](https://tailwindcss.com)로 스타일된 간단한 [Blade 템플릿](/docs/{{version}}/blade)으로 구성되어 있습니다.

Breeze는 새로운 Laravel 애플리케이션을 처음부터 시작하기에 좋은 출발점이며, 나아가 Blade 템플릿을 [Laravel Livewire](https://laravel-livewire.com)를 통해 더욱 확장할 계획인 프로젝트에도 훌륭한 선택입니다.

<a name="laravel-breeze-installation"></a>
### 설치

먼저, [새로운 Laravel 애플리케이션을 생성](/docs/{{version}}/installation)하고 데이터베이스를 설정한 뒤, [마이그레이션](/docs/{{version}}/migrations)을 실행하세요:

```bash
curl -s https://laravel.build/example-app | bash

cd example-app

php artisan migrate
```

새 애플리케이션을 생성한 후, Composer를 사용해 Laravel Breeze를 설치할 수 있습니다:

```bash
composer require laravel/breeze:1.9.2 
```

Composer가 Breeze 패키지를 설치하면, `breeze:install` Artisan 명령어를 실행하세요. 이 명령어는 인증용 뷰, 라우트, 컨트롤러 등 필요한 리소스를 애플리케이션에 게시(publish)합니다. Laravel Breeze의 모든 코드는 애플리케이션 내에 게시되어, 기능과 구현 방식을 완벽하게 제어하고 확인할 수 있습니다. Breeze를 설치한 후에는 애셋(assets)을 컴파일하여 애플리케이션의 CSS 파일이 정상적으로 생성되도록 해야 합니다:

```nothing
php artisan breeze:install

npm install
npm run dev
php artisan migrate
```

그다음 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` URL에 접속할 수 있습니다. Breeze의 모든 라우트는 `routes/auth.php` 파일에 정의되어 있습니다.

> [!TIP]
> 애플리케이션의 CSS 및 JavaScript 컴파일 방법에 대해 더 알고 싶으면 [Laravel Mix 문서](/docs/{{version}}/mix#running-mix)를 참고하세요.

<a name="breeze-and-inertia"></a>
### Breeze와 Inertia

Laravel Breeze는 Vue 또는 React 기반의 [Inertia.js](https://inertiajs.com) 프론트엔드 구현도 제공합니다. Inertia 스택을 사용하려면 `breeze:install` 명령어 실행 시 원하는 스택으로 `vue` 또는 `react`를 지정하면 됩니다:

```nothing
php artisan breeze:install vue

// 또는...

php artisan breeze:install react

npm install
npm run dev
php artisan migrate
```

<a name="breeze-and-next"></a>
### Breeze와 Next.js / API

Laravel Breeze는 최신 JavaScript 애플리케이션(예: [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등)용 인증 API도 스캐폴딩할 수 있습니다. 시작하려면 `breeze:install` 명령어 실행 시 원하는 스택으로 `api`를 지정하세요:

```nothing
php artisan breeze:install api

php artisan migrate
```

설치 과정에서 Breeze는 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 URL은 JavaScript 애플리케이션의 주소이며, 일반적으로 로컬 개발 시에는 `http://localhost:3000`이 됩니다.

<a name="next-reference-implementation"></a>
#### Next.js 참고 구현체

마지막으로, 여러분의 백엔드와 함께 사용할 프론트엔드를 선택할 준비가 되었습니다. Breeze 프론트엔드의 Next 참조 구현체는 [GitHub에서 제공](https://github.com/laravel/breeze-next)됩니다. 이 프론트엔드는 Laravel에서 관리하며, Breeze가 제공하는 전통적인 Blade 및 Inertia 스택과 동일한 사용자 인터페이스를 포함하고 있습니다.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Breeze가 간단하고 최소한의 출발점을 제공한다면, Jetstream은 더 강력한 기능과 다양한 프론트엔드 기술 스택을 추가해서 확장합니다. **Laravel을 처음 접하는 분들은 Laravel Breeze로 기본기를 익힌 후 Laravel Jetstream으로 넘어가길 권장합니다.**

Jetstream은 세련된 애플리케이션 스캐폴딩을 제공하며 로그인, 등록, 이메일 검증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원 및 선택적 팀 관리 기능을 포함합니다. Jetstream은 [Tailwind CSS](https://tailwindcss.com)로 디자인되었으며, [Livewire](https://laravel-livewire.com) 또는 [Inertia.js](https://inertiajs.com)를 기반으로 한 프론트엔드 스캐폴딩을 선택할 수 있습니다.

Laravel Jetstream 설치에 관한 자세한 내용은 [공식 Jetstream 문서](https://jetstream.laravel.com/introduction.html)에서 확인할 수 있습니다.