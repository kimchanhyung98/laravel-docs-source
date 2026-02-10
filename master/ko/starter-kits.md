# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [스타터 키트를 이용한 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [인증](#authentication)
    - [기능 활성화 및 비활성화](#enabling-and-disabling-features)
    - [사용자 생성 및 비밀번호 재설정 커스터마이징](#customizing-actions)
    - [2단계 인증](#two-factor-authentication)
    - [요청 제한(Rate Limiting)](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트는 회원가입 및 인증 기능에 필요한 라우트(routes), 컨트롤러(controllers), 뷰(views)를 모두 포함하고 있어 여러분의 Laravel 프로젝트를 빠르게 구축할 수 있게 도와줍니다. 스타터 키트는 인증 기능을 제공하기 위해 [Laravel Fortify](/docs/master/fortify)를 사용합니다.

이 스타터 키트를 사용하는 것은 필수가 아니며, 원한다면 Laravel의 빈 프로젝트만 설치해 직접 모든 구성을 할 수도 있습니다. 어떤 방법을 선택하시든, 여러분은 멋진 애플리케이션을 만들 수 있을 것입니다!

<a name="creating-an-application"></a>
## 스타터 키트를 이용한 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 키트로 새로운 Laravel 애플리케이션을 만들려면, 먼저 [PHP 및 Laravel CLI 도구 설치](/docs/master/installation#installing-php)가 필요합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 이용해 Laravel 인스톨러 CLI 도구를 설치하세요.

```shell
composer global require laravel/installer
```

그 다음, Laravel 인스톨러 CLI를 사용해 새 Laravel 애플리케이션을 생성할 수 있습니다. 애플리케이션 생성 시, 적용할 스타터 키트를 선택하라는 안내가 나옵니다.

```shell
laravel new my-app
```

애플리케이션을 생성한 후에는, NPM으로 프런트엔드 의존성을 설치하고 개발 서버를 실행하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버가 실행되면, [http://localhost:8000](http://localhost:8000)에서 브라우저로 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 활용해 React 프런트엔드와 함께 Laravel 애플리케이션을 구축하기 위한 견고하고 현대적인 시작점을 제공합니다.

Inertia를 사용하면 서버 사이드 라우팅 및 컨트롤러 방식을 그대로 유지하면서, React의 현대적인 싱글 페이지 애플리케이션을 만들 수 있습니다. 즉, React의 강력한 프런트엔드 기능은 물론 Laravel의 뛰어난 백엔드 생산성과 초고속 Vite 빌드까지 모두 경험할 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 기반으로 Vue 프런트엔드와 함께 Laravel 애플리케이션을 빠르게 시작할 수 있도록 설계되었습니다.

Inertia를 사용하면 서버 사이드 라우팅과 컨트롤러를 유지하고, Vue 기반의 현대적인 싱글 페이지 애플리케이션을 제작할 수 있습니다. Vue의 강력한 프런트엔드 기능, Laravel의 생산성, 그리고 Vite의 초고속 빌드를 모두 누릴 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 활용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프런트엔드를 사용해 Laravel 애플리케이션을 개발하는 데 완벽한 시작점을 제공합니다.

Livewire는 복잡한 자바스크립트 SPAs(싱글 페이지 애플리케이션) 프레임워크 없이, PHP만으로도 동적이고 반응적인 프런트엔드 UI를 제작할 수 있는 강력한 방식입니다. Blade 템플릿을 주로 사용하는 팀에게 쉽고 단순한 대안이 될 수 있습니다.

Livewire 스타터 키트는 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com) 기반으로 만들어졌습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프런트엔드 코드가 모두 프로젝트 내에 포함되어 있어 자유롭게 커스터마이징할 수 있습니다.

프런트엔드 코드 대부분은 `resources/js` 디렉토리에 위치해 있습니다. 애플리케이션의 외관 및 동작을 원하는 대로 수정할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React hooks
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn 컴포넌트를 사용하려면, [원하는 컴포넌트를 찾고](https://ui.shadcn.com), 아래 명령어로 컴포넌트를 발행(publish)합니다.

```shell
npx shadcn@latest add switch
```

위 예시에서는 Switch 컴포넌트가 `resources/js/components/ui/switch.tsx`에 생성됩니다. 컴포넌트가 발행되면, 원하는 페이지에서 바로 사용할 수 있습니다.

```jsx
import { Switch } from "@/components/ui/switch"

const MyPage = () => {
  return (
    <div>
      <Switch />
    </div>
  );
};

export default MyPage;
```

<a name="react-available-layouts"></a>
#### 사용 가능한 레이아웃

React 스타터 키트에는 "sidebar" 레이아웃과 "header" 레이아웃, 두 가지 주 레이아웃이 포함되어 있습니다. 기본값은 sidebar 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일의 import 구문을 수정해 header 레이아웃으로 쉽게 변경할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

sidebar 레이아웃에는 기본 sidebar, "inset" 변형, "floating" 변형 등 세 가지 버전이 제공됩니다. `resources/js/components/app-sidebar.tsx` 파일에서 원하는 variant로 변경하면 됩니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트에 포함된 로그인, 회원가입 등 인증 관련 페이지는 "simple", "card", "split" 3가지 레이아웃을 선택할 수 있습니다.

인증 레이아웃을 변경하려면 `resources/js/layouts/auth-layout.tsx` 파일의 import 구문을 수정하세요.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 기반으로 만들어졌습니다. 모든 스타터 키트와 동일하게, 백엔드와 프런트엔드 모든 코드를 완전히 커스터마이징할 수 있습니다.

프런트엔드 코드는 대부분 `resources/js` 디렉토리에 위치합니다. 원하는 대로 애플리케이션의 모습과 동작을 변경할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 컴포저블 및 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn-vue 컴포넌트가 필요하다면, [원하는 컴포넌트를 찾고](https://www.shadcn-vue.com), 아래 명령어로 컴포넌트를 발행하세요.

```shell
npx shadcn-vue@latest add switch
```

예를 들어, 위 명령어를 실행하면 Switch 컴포넌트가 `resources/js/components/ui/Switch.vue`에 생성됩니다. 생성된 컴포넌트는 아래처럼 바로 페이지에서 사용할 수 있습니다.

```vue
<script setup lang="ts">
import { Switch } from '@/components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```

<a name="vue-available-layouts"></a>
#### 사용 가능한 레이아웃

Vue 스타터 키트 역시 "sidebar" 레이아웃, "header" 레이아웃 두 가지가 있습니다. 기본값은 sidebar 레이아웃이며, `resources/js/layouts/AppLayout.vue` 파일에서 import 구문을 수정하면 header 레이아웃으로 변경할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

sidebar 레이아웃에는 기본 sidebar, "inset" 변형, "floating" 변형 등 세 가지가 있습니다. `resources/js/components/AppSidebar.vue` 파일에서 variant 속성 값을 수정할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트의 로그인, 회원가입 등 인증 관련 페이지 역시 "simple", "card", "split" 3가지 레이아웃 중 선택할 수 있습니다.

이를 변경하려면, `resources/js/layouts/AuthLayout.vue` 파일의 import 구문을 수정하세요.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 4, Tailwind, [Flux UI](https://fluxui.dev/)를 기반으로 합니다. 모든 스타터 키트와 동일하게, 백엔드와 프런트엔드 코드를 자유롭게 커스터마이징할 수 있습니다.

프런트엔드 코드는 대부분 `resources/views` 디렉토리에 있습니다. 본인의 애플리케이션에 맞게 모든 코드를 수정할 수 있습니다.

```text
resources/views
├── components            # 재사용 가능한 컴포넌트
├── flux                  # 커스터마이징된 Flux 컴포넌트
├── layouts               # 애플리케이션 레이아웃
├── pages                 # Livewire 페이지
├── partials              # 재사용 가능한 Blade partials
├── dashboard.blade.php   # 인증된 사용자 대시보드
├── welcome.blade.php     # 게스트(비회원)용 환영 페이지
```

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 키트 역시 "sidebar" 레이아웃, "header" 레이아웃 두 가지를 제공합니다. 기본값은 sidebar이며, `resources/views/layouts/app.blade.php`에서 사용되는 레이아웃을 변경할 수 있습니다. 추가로, main Flux 컴포넌트에 `container` 속성을 추가해야 레이아웃이 정상적으로 적용됩니다.

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트의 로그인, 회원가입 등 인증 관련 페이지에도 "simple", "card", "split" 3가지 레이아웃이 제공됩니다.

인증 레이아웃을 변경하려면 `resources/views/layouts/auth.blade.php` 파일에서 레이아웃 컴포넌트를 변경하세요.

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 인증 (Authentication)

모든 스타터 키트는 인증을 처리하기 위해 [Laravel Fortify](/docs/master/fortify)를 사용합니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 인증에 필요한 라우트, 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에서 활성화한 기능에 따라 아래와 같은 인증 라우트를 자동으로 등록합니다.

| 라우트                              | 메서드  | 설명                                 |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`    | 로그인 양식 표시                    |
| `/login`                           | `POST`   | 사용자 인증                         |
| `/logout`                          | `POST`   | 로그아웃                            |
| `/register`                        | `GET`    | 회원가입 양식 표시                  |
| `/register`                        | `POST`   | 새로운 사용자 등록                  |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 양식 표시      |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 전송           |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 양식 표시           |
| `/reset-password`                  | `POST`   | 비밀번호 갱신                       |
| `/email/verify`                    | `GET`    | 이메일 인증 안내 표시               |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 주소 인증                    |
| `/email/verification-notification` | `POST`   | 인증 이메일 재발송                  |
| `/user/confirm-password`           | `GET`    | 비밀번호 확인 양식 표시             |
| `/user/confirm-password`           | `POST`   | 비밀번호 확인                       |
| `/two-factor-challenge`            | `GET`    | 2FA(2단계 인증) 도전 양식 표시      |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 인증                       |

애플리케이션의 모든 라우트는 `php artisan route:list` Artisan 명령어로 출력해볼 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화 (Enabling and Disabling Features)

어떤 Fortify 기능을 활성화할지는 `config/fortify.php` 설정 파일의 'features' 배열에서 관리할 수 있습니다.

```php
use Laravel\Fortify\Features;

'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
    Features::twoFactorAuthentication([
        'confirm' => true,
        'confirmPassword' => true,
    ]),
],
```

특정 기능을 비활성화하려면 해당 항목을 주석 처리하거나 배열에서 삭제하세요. 예를 들어, 공개 회원가입을 비활성화하고 싶다면 `Features::registration()`을 제거하면 됩니다.

[React](#react) 또는 [Vue](#vue) 스타터 키트 사용 시에는, 프런트엔드 코드 내에서도 비활성화한 기능의 라우트 관련 코드(임포트, 링크 등)를 반드시 함께 제거해야 합니다. 이런 스타터 키트들은 타입 안전 라우팅을 위해 Wayfinder를 사용하며, 빌드 시점에 라우트 정의를 생성합니다. 존재하지 않는 라우트가 참조되면 빌드 실패가 발생하니 주의하세요.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이징 (Customizing User Creation and Password Reset)

사용자가 회원가입하거나 비밀번호를 재설정할 때, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉토리 내 액션 클래스를 호출합니다.

| 파일                          | 설명                                |
| ----------------------------- | ----------------------------------- |
| `CreateNewUser.php`           | 신규 사용자 유효성 검증 및 생성     |
| `ResetUserPassword.php`       | 비밀번호 유효성 검증 및 업데이트    |
| `PasswordValidationRules.php` | 비밀번호 유효성 검증 규칙 정의      |

예를 들어, 회원가입 로직을 커스터마이즈하려면 `CreateNewUser` 액션을 수정하면 됩니다.

```php
public function create(array $input): User
{
    Validator::make($input, [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'max:255', 'unique:users'],
        'phone' => ['required', 'string', 'max:20'], // [tl! add]
        'password' => $this->passwordRules(),
    ])->validate();

    return User::create([
        'name' => $input['name'],
        'email' => $input['email'],
        'phone' => $input['phone'], // [tl! add]
        'password' => Hash::make($input['password']),
    ]);
}
```

<a name="two-factor-authentication"></a>
### 2단계 인증 (Two-Factor Authentication)

스타터 키트에는 2단계 인증(2FA) 기능이 내장되어 있어, 사용자가 TOTP 호환 인증 앱을 통해 계정 보안을 강화할 수 있습니다. 2FA는 기본적으로 `config/fortify.php`의 `Features::twoFactorAuthentication()`를 통해 활성화되어 있습니다.

`confirm` 옵션은 2FA 활성화 전 인증 코드를 한 번 더 확인하도록 하며, `confirmPassword` 옵션은 2FA 활성화/비활성화 시 비밀번호 재확인을 요구합니다. 세부 내용은 [Fortify의 2단계 인증 문서](/docs/master/fortify#two-factor-authentication)를 참고하세요.

<a name="rate-limiting"></a>
### 요청 제한(Rate Limiting)

요청 제한(Rate Limiting)을 통해 무차별 대입 공격이나 반복 로그인 시도를 방지할 수 있습니다. Fortify의 요청 제한 동작은 `FortifyServiceProvider`에서 아래와 같이 커스터마이즈할 수 있습니다.

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 스타터 키트에서는 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 추가로, 각 스타터 키트별로 [WorkOS AuthKit](https://authkit.com) 기반 버전도 제공하고 있습니다. WorkOS 버전에서는 다음과 같은 인증 기능을 제공합니다:

<div class="content-list" markdown="1">

- 소셜 인증(Google, Microsoft, GitHub, Apple)
- 패스키(생체/디바이스 기반) 인증
- 이메일 기반 "Magic Auth"
- SSO(기업용 싱글 사인온)

</div>

WorkOS를 인증 공급자로 사용하려면 [WorkOS 계정](https://workos.com)이 필요합니다. WorkOS는 월간 액티브 유저 100만명까지 무료로 인증 서비스를 제공합니다.

WorkOS AuthKit을 인증 시스템으로 사용하려면, `laravel new` 실행 시 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트로 애플리케이션을 생성 후, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 아래와 같이 설정해야 합니다. 각 값은 WorkOS 대시보드에서 제공받은 정보를 사용합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션 홈페이지 URL도 등록해야 합니다. 이 주소는 사용자가 로그아웃 성공 시 리디렉션되는 URL입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트에서는, 애플리케이션의 WorkOS AuthKit 설정에서 "이메일+비밀번호" 인증 방식을 비활성화하고, 소셜 인증, 패스키, Magic Auth, SSO만 허용하는 것을 권장합니다. 이렇게 하면 서버에서 비밀번호를 아예 다루지 않게 되어 보안을 강화할 수 있습니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

WorkOS AuthKit의 세션 비활성화(사용자 미사용) 타임아웃도 Laravel 애플리케이션의 세션 만료 시간(일반적으로 2시간)과 일치하도록 설정하는 것을 권장합니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React, Vue 스타터 키트는 Inertia의 [서버사이드 렌더링(Server-Side Rendering)](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. Inertia SSR과 호환되는 번들을 빌드하려면 아래와 같이 실행하세요.

```shell
npm run build:ssr
```

또한, `composer dev:ssr` 명령어를 통해 SSR 번들 빌드 후 곧바로 Laravel 개발 서버와 Inertia SSR 서버를 동시에 띄울 수 있습니다. 덕분에 로컬 환경에서 서버사이드 렌더링 동작을 편하게 테스트할 수 있습니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 키트 (Community Maintained Starter Kits)

Laravel 인스톨러로 새 애플리케이션 생성 시, `--using` 플래그에 Packagist에 공개된 커뮤니티 유지 스타터 키트의 이름을 지정하여 설치할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 제작 및 배포

직접 제작한 스타터 키트를 다른 사람도 사용할 수 있게 하려면, [Packagist](https://packagist.org)에 패키지를 등록하세요. 스타터 키트의 `.env.example` 파일에 필요한 환경 변수들을 명시하고, 필요한 post-install 명령어가 있다면 `composer.json`의 `post-create-project-cmd` 배열에도 추가하면 됩니다.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 업그레이드는 어떻게 하나요?

모든 스타터 키트는 새로운 프로젝트를 시작하기에 아주 좋은 기초 구조를 제공합니다. 모든 코드를 여러분이 직접 소유하고 있으므로, 원하는 만큼 자유롭게 수정·확장할 수 있습니다. 별도로 스타터 키트 자체를 따로 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

이메일 인증 기능을 추가하려면, `App/Models/User.php` 모델에서 `MustVerifyEmail` import 주석을 해제하고, 모델이 `MustVerifyEmail` 인터페이스를 구현하게 만드세요.

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
// ...

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```

이제 가입한 사용자에게 인증 이메일이 발송됩니다. 사용자의 이메일 인증 여부에 따라 일부 라우트 접근을 제한하려면, 해당 라우트에 `verified` 미들웨어를 추가하세요.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 기반 스타터 키트에서는 이메일 인증이 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

애플리케이션 브랜딩에 맞게 기본 이메일 템플릿을 커스터마이징하고 싶을 수 있습니다. 아래 명령어로 이메일 뷰를 애플리케이션에 발행해 보세요.

```
php artisan vendor:publish --tag=laravel-mail
```

`resources/views/vendor/mail` 디렉터리에 다양한 파일이 생성되며, 이 파일들과 `resources/views/vendor/mail/themes/default.css` 파일을 직접 수정해 이메일 템플릿의 디자인을 원하는 대로 바꿀 수 있습니다.
