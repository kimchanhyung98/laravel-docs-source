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

새로운 Laravel 애플리케이션을 빠르게 시작할 수 있도록, 인증(authentication)과 애플리케이션 스타터 키트를 제공하고 있습니다. 이 키트들은 애플리케이션 사용자 등록과 인증에 필요한 라우트(routes), 컨트롤러(controllers), 뷰(views)를 자동으로 생성해 줍니다.

이 스타터 키트들은 자유롭게 사용할 수 있지만 필수는 아닙니다. Laravel을 처음부터 직접 설치하여 자체적으로 애플리케이션을 구축해도 무방합니다. 어떤 선택을 하시든 멋진 애플리케이션을 완성할 것이라 믿습니다!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze)는 Laravel의 모든 [인증 기능](/docs/11.x/authentication)을 간단하고 최소한으로 구현한 패키지입니다. 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등이 포함되며, 사용자 이름, 이메일 주소, 비밀번호를 변경할 수 있는 간단한 "프로필" 페이지도 제공합니다.

Laravel Breeze의 기본 뷰 레이어는 간단한 [Blade 템플릿](/docs/11.x/blade)과 [Tailwind CSS](https://tailwindcss.com) 스타일을 사용해 만들어집니다. 또한 Breeze는 [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com)를 기반으로 한 스캐폴딩 옵션을 제공하며, Inertia 기반에서는 Vue 또는 React 중 선택 가능합니다.

<img src="https://laravel.com/img/docs/breeze-register.png" />

#### Laravel 부트캠프

Laravel이 처음이라면, [Laravel Bootcamp](https://bootcamp.laravel.com)를 참고하세요. Bootcamp는 Breeze를 사용해 처음 Laravel 애플리케이션을 구축하는 과정을 안내해 줍니다. Laravel과 Breeze의 전반적인 기능을 익히기에 아주 좋은 방법입니다.

<a name="laravel-breeze-installation"></a>
### 설치 (Installation)

먼저, [새로운 Laravel 애플리케이션을 생성](/docs/11.x/installation)하세요. [Laravel 설치 프로그램](/docs/11.x/installation#creating-a-laravel-project)을 통해 애플리케이션을 만들면 설치 과정에서 Laravel Breeze를 설치할지 묻습니다. 그렇지 않은 경우, 아래 수동 설치 절차를 따르셔야 합니다.

이미 스타터 키트 없이 Laravel 애플리케이션을 만들었다면, Composer를 통해 Laravel Breeze를 수동 설치할 수 있습니다:

```shell
composer require laravel/breeze --dev
```

Composer가 Laravel Breeze 패키지를 설치한 뒤에는, `breeze:install` Artisan 명령어를 실행해야 합니다. 이 명령어는 인증 뷰, 라우트, 컨트롤러 및 기타 자원을 애플리케이션에 배포(publish)합니다. Laravel Breeze는 모든 코드를 애플리케이션 내에 배포함으로써 완전한 제어와 구현 내용을 확인할 수 있게 합니다.

`breeze:install` 명령어는 사용자의 프론트엔드 스택과 테스트 프레임워크 선호도를 묻는 프롬프트를 보여줍니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
### Breeze와 Blade

기본 Breeze "스택"은 Blade 스택으로, 간단한 [Blade 템플릿](/docs/11.x/blade)을 사용하여 애플리케이션의 프론트엔드를 렌더링합니다. Blade 스택은 추가 인수 없이 `breeze:install` 명령어를 실행하고 Blade 프론트엔드 스택을 선택하면 설치됩니다. Breeze 스캐폴딩 설치 후에는 애플리케이션의 프론트엔드 자산을 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

설치가 완료되면, 웹 브라우저에서 애플리케이션의 `/login` 또는 `/register` URL로 접속할 수 있습니다. Breeze의 모든 라우트는 `routes/auth.php` 파일 내에 정의되어 있습니다.

> [!NOTE]  
> 애플리케이션 CSS와 JavaScript의 컴파일 방법에 관해서는 Laravel의 [Vite 문서](/docs/11.x/vite#running-vite)를 참고하세요.

<a name="breeze-and-livewire"></a>
### Breeze와 Livewire

Laravel Breeze는 또한 [Livewire](https://livewire.laravel.com) 스캐폴딩을 제공합니다. Livewire는 PHP만으로 동적이고 반응형 프론트엔드 UI를 구성할 수 있는 강력한 도구입니다.

Blade 템플릿을 주로 사용하며, JavaScript 중심의 SPA 프레임워크(Vue, React 등)보다 단순한 대안을 찾는 팀에 적합합니다.

Livewire 스택을 사용하려면 `breeze:install` Artisan 명령어 실행 시 Livewire 프론트엔드 스택을 선택하세요. 스캐폴딩 설치 후에는 데이터베이스 마이그레이션을 실행해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
### Breeze와 React / Vue

Laravel Breeze는 또한 [Inertia](https://inertiajs.com)를 활용해 React와 Vue 스캐폴딩을 지원합니다. Inertia는 전통적인 서버 사이드 라우팅과 컨트롤러를 유지하면서 현대적인 React 및 Vue 기반 싱글 페이지 애플리케이션을 구축하게 해줍니다.

Inertia 덕분에 React와 Vue의 프론트엔드 강력함과 Laravel의 뛰어난 백엔드 생산성, 그리고 빠른 [Vite](https://vitejs.dev) 컴파일을 동시에 경험할 수 있습니다. Inertia 스택을 사용하려면 `breeze:install` 실행 시 Vue 또는 React 프론트엔드 스택 중 하나를 선택하세요.

Vue 또는 React 프론트엔드를 선택하면, Breeze 설치 프로그램이 [Inertia SSR](https://inertiajs.com/server-side-rendering) 사용 여부와 TypeScript 지원 여부도 묻습니다. 스캐폴딩이 설치된 후 애플리케이션 프론트엔드 자산을 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

마지막으로, 웹 브라우저에서 `/login` 또는 `/register` URL로 접속할 수 있습니다. 모든 Breeze 경로는 `routes/auth.php` 파일 내에 정의되어 있습니다.

<a name="breeze-and-next"></a>
### Breeze와 Next.js / API

Laravel Breeze는 또한 [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등 최신 JavaScript 애플리케이션과 인증 연동이 가능한 API 인증 스캐폴딩을 제공합니다. 시작하려면 `breeze:install` Artisan 명령어를 실행할 때 API 스택을 선택하세요:

```shell
php artisan breeze:install

php artisan migrate
```

설치 과정에서 Breeze는 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경 변수를 추가합니다. 이 URL은 JavaScript 애플리케이션의 주소가 되어야 하며, 보통 로컬 개발 시에는 `http://localhost:3000`입니다. 또한 `APP_URL`이 `http://localhost:8000`으로 설정되어 있는지 확인해야 합니다. 이는 `serve` Artisan 명령어에서 기본으로 사용하는 URL입니다.

<a name="next-reference-implementation"></a>
#### Next.js 참조 구현

이제 원하는 프론트엔드와 이 백엔드를 연결할 준비가 되었습니다. Breeze 프론트엔드의 Next 참조 구현은 [GitHub에서 제공됩니다](https://github.com/laravel/breeze-next). 이 프론트엔드는 Laravel이 공식적으로 관리하며, 기존의 Blade와 Inertia 스택과 동일한 사용자 인터페이스를 포함합니다.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Breeze가 간단하고 최소한의 시작점을 제공한다면, Jetstream은 보다 강력한 기능과 추가 프론트엔드 기술 스택을 갖춘 확장된 솔루션입니다. **Laravel을 처음 접하는 분들께는 Laravel Breeze로 기본을 익힌 후 Laravel Jetstream으로 넘어가길 권장합니다.**

Jetstream은 깔끔하게 디자인된 애플리케이션 스캐폴딩을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 통한 API 지원, 선택적 팀 관리 등을 포함합니다. Tailwind CSS로 설계되었고 [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com) 기반의 프론트엔드 스캐폴딩 중 선택할 수 있습니다.

Laravel Jetstream 설치 관련 상세 문서는 [공식 Jetstream 문서](https://jetstream.laravel.com)에서 확인할 수 있습니다.