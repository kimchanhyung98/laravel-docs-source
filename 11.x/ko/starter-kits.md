# 스타터 키트

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

새로운 Laravel 애플리케이션을 빠르게 구축할 수 있도록, 인증 및 애플리케이션 스타터 키트를 제공합니다. 이 키트들은 회원 가입 및 인증에 필요한 라우트, 컨트롤러, 뷰를 자동으로 스캐폴딩해줍니다.

이러한 스타터 키트를 자유롭게 사용할 수 있지만, 반드시 사용해야 하는 것은 아닙니다. Laravel의 새 복사본을 설치하여 처음부터 직접 애플리케이션을 구축할 수도 있습니다. 어떤 방식을 선택하든 멋진 결과를 만들어 내실 수 있을 것입니다!

<a name="laravel-breeze"></a>
## Laravel Breeze

[Laravel Breeze](https://github.com/laravel/breeze)는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 [인증 기능](/docs/{{version}}/authentication)을 최소한의 구현으로 제공합니다. 또한, 사용자가 이름, 이메일, 비밀번호를 수정할 수 있는 간단한 "프로필" 페이지도 포함되어 있습니다.

Laravel Breeze의 기본 뷰 레이어는 간단한 [Blade 템플릿](/docs/{{version}}/blade)과 [Tailwind CSS](https://tailwindcss.com)로 스타일링되어 있습니다. 추가로, [Livewire](https://livewire.laravel.com) 기반 또는 [Inertia](https://inertiajs.com) 기반(Vue 또는 React 선택 가능) 스캐폴딩 옵션도 제공합니다.

<img src="https://laravel.com/img/docs/breeze-register.png">

#### Laravel 부트캠프

Laravel을 처음 접하신다면, [Laravel 부트캠프](https://bootcamp.laravel.com)에 참여해 보세요. 부트캠프에서는 Breeze를 사용하여 첫 Laravel 애플리케이션을 만드는 과정을 단계별로 안내합니다. Laravel과 Breeze의 다양한 기능을 둘러보기에 좋은 방법입니다.

<a name="laravel-breeze-installation"></a>
### 설치

우선, [새로운 Laravel 애플리케이션을 생성](/docs/{{version}}/installation)해야 합니다. [Laravel 설치 프로그램](/docs/{{version}}/installation#creating-a-laravel-project)을 사용하여 애플리케이션을 생성하면, 설치 과정 중 Laravel Breeze를 설치할 것인지 묻는 안내를 받게 됩니다. 그렇지 않은 경우에는 아래의 수동 설치 지침에 따라 진행하면 됩니다.

만약 스타터 키트 없이 이미 새 Laravel 애플리케이션을 생성했다면, Composer를 사용하여 Laravel Breeze를 수동으로 설치할 수 있습니다:

```shell
composer require laravel/breeze --dev
```

Composer로 Laravel Breeze 패키지를 설치한 후, `breeze:install` Artisan 명령어를 실행해야 합니다. 이 명령어는 인증 뷰, 라우트, 컨트롤러 등 여러 리소스를 애플리케이션에 퍼블리시합니다. Laravel Breeze의 모든 코드를 애플리케이션에 퍼블리시하기 때문에, 기능과 구현 방식을 완전히 제어하고 직접 확인할 수 있습니다.

`breeze:install` 명령은 원하는 프론트엔드 스택과 테스트 프레임워크를 선택하도록 안내합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

<a name="breeze-and-blade"></a>
### Breeze와 Blade

Breeze의 기본 스택은 Blade 스택으로, 간단한 [Blade 템플릿](/docs/{{version}}/blade)을 사용해 프론트엔드를 렌더링합니다. Blade 스택은 추가 인수 없이 `breeze:install` 명령어를 실행한 뒤 Blade 프론트엔드 스택을 선택하면 설치할 수 있습니다. Breeze 스캐폴딩 설치 후, 프론트엔드 에셋도 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

이제 웹 브라우저로 애플리케이션의 `/login` 또는 `/register` URL에 접속해 보세요. Breeze의 모든 라우트는 `routes/auth.php` 파일에서 정의됩니다.

> [!NOTE]  
> 애플리케이션의 CSS와 JavaScript를 컴파일하는 방법에 대한 자세한 내용은 Laravel의 [Vite 문서](/docs/{{version}}/vite#running-vite)를 참조하세요.

<a name="breeze-and-livewire"></a>
### Breeze와 Livewire

Laravel Breeze는 [Livewire](https://livewire.laravel.com) 스캐폴딩도 제공합니다. Livewire는 PHP만으로 동적이고 반응성이 뛰어난 프론트엔드 UI를 구축할 수 있는 강력한 도구입니다.

Livewire는 주로 Blade 템플릿을 사용하며, Vue나 React와 같은 자바스크립트 기반 SPA 프레임워크보다 더 단순한 대안을 원하는 팀에게 적합합니다.

Livewire 스택을 사용하려면 `breeze:install` Artisan 명령어 실행 시 Livewire 프론트엔드 스택을 선택하십시오. Breeze 스캐폴딩 설치 후에는 데이터베이스 마이그레이션을 실행해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
```

<a name="breeze-and-inertia"></a>
### Breeze와 React / Vue

Laravel Breeze는 [Inertia](https://inertiajs.com) 프론트엔드 구현을 통해 React와 Vue 스캐폴딩도 지원합니다. Inertia를 사용하면 서버 사이드 라우팅과 컨트롤러를 그대로 유지하면서 모던 싱글 페이지 React나 Vue 애플리케이션을 쉽게 만들 수 있습니다.

Inertia를 통해 React와 Vue의 강력한 프론트엔드 기능과 함께, Laravel의 생산성 그리고 빠른 [Vite](https://vitejs.dev) 컴파일 속도를 누릴 수 있습니다. Inertia 스택을 사용하려면 `breeze:install` Artisan 명령어 실행 시 Vue 또는 React 프론트엔드 스택을 선택하십시오.

Vue나 React 프론트엔드 스택을 선택하면, Breeze 설치 도중 [Inertia SSR](https://inertiajs.com/server-side-rendering) 또는 TypeScript 지원 여부도 함께 묻게 됩니다. Breeze 스캐폴딩 설치 후에는 프론트엔드 에셋을 컴파일해야 합니다:

```shell
php artisan breeze:install

php artisan migrate
npm install
npm run dev
```

이제 웹 브라우저로 애플리케이션의 `/login` 또는 `/register` URL에 접속해 보세요. Breeze의 모든 라우트는 `routes/auth.php` 파일에서 정의됩니다.

<a name="breeze-and-next"></a>
### Breeze와 Next.js / API

Laravel Breeze는 [Next](https://nextjs.org), [Nuxt](https://nuxt.com) 등 최신 자바스크립트 애플리케이션과 연동할 수 있는 인증용 API 스캐폴딩도 지원합니다. 시작하려면 `breeze:install` Artisan 명령어 실행 시 API 스택을 선택하세요:

```shell
php artisan breeze:install

php artisan migrate
```

설치 중 Breeze는 애플리케이션의 `.env` 파일에 `FRONTEND_URL` 환경변수를 추가합니다. 이 URL은 자바스크립트 애플리케이션의 URL이어야 하며, 로컬 개발 환경에서는 일반적으로 `http://localhost:3000`이 됩니다. 또한 `APP_URL`이 `http://localhost:8000`(기본 `serve` Artisan 명령어 사용하는 주소)로 설정되어 있는지 반드시 확인하세요.

<a name="next-reference-implementation"></a>
#### Next.js 참고 구현

이제 백엔드를 원하는 프론트엔드와 연동할 준비가 되었습니다. Breeze 프론트엔드의 Next 참고 구현은 [GitHub에서 확인할 수 있습니다](https://github.com/laravel/breeze-next). 이 프론트엔드는 Laravel에서 공식적으로 관리하며, Breeze가 제공하는 Blade·Inertia 스택과 동일한 사용자 인터페이스를 포함하고 있습니다.

<a name="laravel-jetstream"></a>
## Laravel Jetstream

Laravel Breeze가 Laravel 애플리케이션 구축을 위한 단순하고 최소한의 시작점을 제공한다면, Jetstream은 더 강력한 기능과 다양한 프론트엔드 기술 스택으로 이를 확장한 도구입니다. **Laravel을 처음 접하시는 분들은 Jetstream을 사용하기 전에 Laravel Breeze로 기본 개념부터 익히실 것을 추천합니다.**

Jetstream은 아름답게 디자인된 애플리케이션 스캐폴딩을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum 기반 API 지원, 그리고 선택적 팀 관리 기능까지 포함하고 있습니다. Jetstream은 [Tailwind CSS](https://tailwindcss.com)로 제작되었으며, [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com) 기반의 프론트엔드 스캐폴딩을 선택할 수 있습니다.

Laravel Jetstream 설치에 관한 전체 문서는 [공식 Jetstream 문서](https://jetstream.laravel.com)에서 확인하실 수 있습니다.