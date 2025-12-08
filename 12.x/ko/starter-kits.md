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
    - [이중 인증(2FA)](#two-factor-authentication)
    - [요청 제한](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 더욱 빠르게 시작할 수 있도록 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트는 여러분의 다음 Laravel 애플리케이션을 신속하게 개발할 수 있게 하며, 사용자 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰를 모두 포함합니다. 이 스타터 키트들은 인증을 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다.

이 스타터 키트는 반드시 사용해야 하는 것은 아닙니다. 원한다면 Laravel의 새 복사본을 설치하여 처음부터 직접 애플리케이션을 구축할 수도 있습니다. 어떤 방법을 사용하더라도, 여러분이 훌륭한 결과를 만들어낼 것이라 믿습니다!

<a name="creating-an-application"></a>
## 스타터 키트를 이용한 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 키트를 활용하여 새로운 Laravel 애플리케이션을 생성하려면, 먼저 [PHP 및 Laravel CLI 도구 설치](/docs/12.x/installation#installing-php)가 필요합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer로 Laravel 인스톨러 CLI 도구를 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

그런 다음, Laravel 인스톨러 CLI를 사용하여 새로운 Laravel 애플리케이션을 생성합니다. Laravel 인스톨러는 선호하는 스타터 키트를 선택하라는 프롬프트를 표시합니다.

```shell
laravel new my-app
```

Laravel 애플리케이션 생성 후, NPM으로 프론트엔드 의존성을 설치하고 Laravel 개발 서버를 시작하세요.

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버가 시작되면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)에서 애플리케이션에 접근할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 활용하여 React 프론트엔드와 함께 Laravel 애플리케이션을 구축할 수 있는 강력하고 현대적인 출발점을 제공합니다.

Inertia를 활용하면, 전통적인 서버사이드 라우팅과 컨트롤러를 사용하면서 React로 싱글 페이지 애플리케이션을 손쉽게 개발할 수 있습니다. 즉, React의 프론트엔드 파워와 함께 Laravel의 강력한 백엔드 생산성, 그리고 빠른 Vite 컴파일을 모두 경험할 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 사용하여 Vue 프론트엔드와 함께 Laravel 애플리케이션을 쉽게 시작할 수 있도록 해줍니다.

Inertia를 통해 전통적 서버사이드 라우팅과 컨트롤러 구조를 활용하면서 현대적인 Vue 기반 싱글 페이지 애플리케이션을 개발할 수 있으며, Vue의 프론트엔드 능력과 Laravel의 백엔드 생산성, Vite 컴파일 환경을 모두 누릴 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드로 Laravel 애플리케이션을 개발하기에 완벽한 출발점을 제공합니다.

Livewire는 순수 PHP만으로도 동적이고 반응형 프론트엔드 UI를 만들 수 있는 강력한 도구입니다. Blade 템플릿을 위주로 개발하는 팀이나 React, Vue와 같은 JavaScript 기반 SPA 프레임워크의 복잡성을 피하고 싶은 개발자에게 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 활용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)로 구축되어 있습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드의 전체 코드가 여러분의 애플리케이션 내부에 포함되어 있어 자유롭게 커스터마이징할 수 있습니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉토리에 위치하고 있습니다. 원하는 대로 코드를 수정하여 애플리케이션의 모양과 동작을 커스터마이징할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn 컴포넌트를 적용하려면, 먼저 [사용할 컴포넌트를 확인](https://ui.shadcn.com)한 후, `npx` 명령어로 컴포넌트를 등록하세요.

```shell
npx shadcn@latest add switch
```

이 예시에서 명령어는 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx` 경로에 생성합니다. 해당 컴포넌트가 등록된 후에는 원하는 페이지에서 자유롭게 사용할 수 있습니다.

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

React 스타터 키트에는 "sidebar" 레이아웃과 "header" 레이아웃, 두 가지 주요 레이아웃이 제공됩니다. 기본값은 sidebar 레이아웃이지만, 원하는 경우 `resources/js/layouts/app-layout.tsx` 파일 상단에서 import되는 레이아웃을 변경해 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

sidebar 레이아웃에는 기본 sidebar, "inset", "floating" 세 가지 변형이 포함되어 있습니다. `resources/js/components/app-sidebar.tsx` 컴포넌트에서 변형 값을 수정해 원하는 스타일을 적용할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트의 인증 페이지(로그인·회원가입 등) 역시 "simple", "card", "split" 세 가지 레이아웃 변형을 지원합니다.

인증 페이지 레이아웃을 변경하려면 `resources/js/layouts/auth-layout.tsx`의 import 부분을 수정하세요.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 스타터 키트와 마찬가지로, 백엔드 및 프론트엔드 코드는 애플리케이션 내에서 자유롭게 커스터마이징할 수 있습니다.

프론트엔드 코드 대부분은 `resources/js` 디렉토리에 위치합니다. 사용자 인터페이스의 동작 및 디자인을 입맛에 맞게 변경할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 콤포저블/훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

shadcn-vue 추가 컴포넌트는 [공식 사이트에서 원하는 컴포넌트 확인](https://www.shadcn-vue.com) 후, 아래와 같이 등록할 수 있습니다.

```shell
npx shadcn-vue@latest add switch
```

이렇게 하면 Switch 컴포넌트가 `resources/js/components/ui/Switch.vue`에 생성됩니다. 컴포넌트가 등록된 후에는 원하는 페이지에서 아래와 같이 사용할 수 있습니다.

```vue
<script setup lang="ts">
import { Switch } from '@/Components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```

<a name="vue-available-layouts"></a>
#### 사용 가능한 레이아웃

Vue 스타터 키트에는 "sidebar" 레이아웃과 "header" 레이아웃, 두 가지 주요 레이아웃이 제공됩니다. 기본값은 sidebar 레이아웃이며, `resources/js/layouts/AppLayout.vue` 상단의 import 문을 수정해 header 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

sidebar 레이아웃은 기본 sidebar, "inset", "floating" 형태의 세 가지 변형이 있습니다. 원하는 변형을 `resources/js/components/AppSidebar.vue`에서 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트의 인증 페이지(로그인·회원가입 등)는 "simple", "card", "split"의 세 가지 레이아웃을 지원합니다.

인증 레이아웃을 변경하려면 `resources/js/layouts/AuthLayout.vue`의 import 부분을 수정하세요.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 3, Tailwind, [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 다른 스타터 키트와 마찬가지로, 백엔드와 프론트엔드의 모든 코드를 자유롭게 커스터마이즈할 수 있습니다.

#### Livewire와 Volt

프론트엔드 코드는 주로 `resources/views` 디렉토리에 위치합니다. 원하는 대로 UI 또는 동작을 수정하여 맞춤형 애플리케이션을 만들 수 있습니다.

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # 재사용 가능한 Blade 파셜
├── dashboard.blade.php   # 인증 사용자의 대시보드
├── welcome.blade.php     # 게스트 사용자 환영 페이지
```

#### 전통적인 Livewire 컴포넌트

프론트엔드 코드는 `resources/views`에, 해당 Livewire 컴포넌트의 백엔드 로직은 `app/Livewire` 디렉토리에 각각 위치합니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 키트에는 "sidebar" 레이아웃, "header" 레이아웃 두 가지 주요 레이아웃이 있습니다. 기본값은 sidebar 레이아웃이며, header 레이아웃을 사용하려면 `resources/views/components/layouts/app.blade.php` 파일에서 사용되는 레이아웃을 변경하고, 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다.

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트의 인증 관련 페이지(로그인, 회원가입 등) 또한 "simple", "card", "split" 세 가지 레이아웃 변형을 지원합니다.

인증 레이아웃을 변경하려면 `resources/views/components/layouts/auth.blade.php`에서 사용되는 레이아웃을 수정하세요.

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="authentication"></a>
## 인증 (Authentication)

모든 스타터 키트는 인증 처리에 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다. Fortify는 로그인, 등록, 비밀번호 재설정, 이메일 인증 등 다양한 인증 경로와 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에 활성화된 기능에 따라 다음과 같은 인증 라우트를 자동으로 등록합니다.

| Route                              | Method | 설명                               |
| ----------------------------------- | ------ | ---------------------------------- |
| `/login`                           | `GET`    | 로그인 폼 표시                    |
| `/login`                           | `POST`   | 사용자 인증                       |
| `/logout`                          | `POST`   | 로그아웃                          |
| `/register`                        | `GET`    | 회원가입 폼 표시                  |
| `/register`                        | `POST`   | 신규 사용자 생성                  |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 폼 표시      |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 전송         |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 폼 표시           |
| `/reset-password`                  | `POST`   | 비밀번호 변경                     |
| `/email/verify`                    | `GET`    | 이메일 인증 알림 표시             |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 주소 인증                  |
| `/email/verification-notification` | `POST`   | 인증 이메일 재발송                |
| `/user/confirm-password`           | `GET`    | 비밀번호 확인 폼 표시             |
| `/user/confirm-password`           | `POST`   | 비밀번호 확인                     |
| `/two-factor-challenge`            | `GET`    | 2FA 챌린지 폼 표시                |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 인증                     |

애플리케이션의 모든 라우트를 확인하려면 `php artisan route:list` 아티즌 명령어를 사용할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화 (Enabling and Disabling Features)

Fortify의 기능 활성화/비활성화는 애플리케이션의 `config/fortify.php` 설정 파일에서 제어할 수 있습니다.

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

기능을 비활성화하려면 해당 항목을 `features` 배열에서 주석 처리하거나 삭제하세요. 예를 들어, 공개 회원가입을 막으려면 `Features::registration()`을 제거하면 됩니다.

[React](#react)나 [Vue](#vue) 스타터 키트 사용 시에는 프론트엔드 코드 내에서도 해당 기능의 라우트 참조를 모두 제거해야 합니다. 예를 들어 이메일 인증을 비활성화 할 경우, Vue 또는 React 컴포넌트 내 import 및 `verification` 관련 참조를 수동으로 삭제해야 합니다. 이 스타터 키트들은 타입 안전 라우팅을 위해 Wayfinder를 사용하며, 빌드 시점에 라우트 정의가 생성됩니다. 존재하지 않는 라우트를 참조하면 애플리케이션 빌드가 실패합니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이징 (Customizing User Creation and Password Reset)

사용자가 회원가입 또는 비밀번호 재설정을 진행할 때, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉토리에 위치한 액션 클래스를 호출합니다.

| 파일                           | 설명                                 |
| ------------------------------ | ------------------------------------ |
| `CreateNewUser.php`            | 신규 사용자 유효성 검사 및 생성      |
| `ResetUserPassword.php`        | 비밀번호 유효성 검사 및 변경         |
| `PasswordValidationRules.php`  | 비밀번호 유효성 검증 규칙 정의       |

예를 들어 회원가입 로직을 커스터마이징하려면 `CreateNewUser` 액션을 수정하세요.

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
### 이중 인증(2FA) (Two-Factor Authentication)

스타터 키트에는 TOTP 호환 인증 앱을 통한 이중 인증(2FA)이 내장되어 있어, 사용자가 더욱 안전하게 계정을 보호할 수 있습니다. 2FA는 `config/fortify.php` 파일의 `Features::twoFactorAuthentication()` 설정으로 기본 활성화되어 있습니다.

`confirm` 옵션은 사용자가 2FA를 완전히 켜기 전 코드 인증을 요구하며, `confirmPassword`는 2FA 활성화/비활성화 전 비밀번호 확인을 요구합니다. 자세한 사항은 [Fortify의 이중 인증 문서](/docs/12.x/fortify#two-factor-authentication)를 참고하세요.

<a name="rate-limiting"></a>
### 요청 제한 (Rate Limiting)

요청 제한은 무차별 대입 공격이나 반복적인 로그인 시도로 인증 엔드포인트가 과부하되는 것을 막아줍니다. Fortify의 요청 제한 정책은 `FortifyServiceProvider`에서 수정할 수 있습니다.

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 스타터 키트는 모두 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등의 기능을 제공합니다. 추가로, 각 스타터 키트의 [WorkOS AuthKit](https://authkit.com) 지원 변형이 준비되어 있으며, 이 버전은 다음 기능을 지원합니다.

<div class="content-list" markdown="1">

- 소셜 인증 (Google, Microsoft, GitHub, Apple)
- 패스키 인증
- 이메일 기반 "Magic Auth"
- SSO (싱글 사인온)

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정이 필요합니다](https://workos.com). WorkOS는 월간 활성 사용자 100만 명까지 무료 인증을 제공합니다.

WorkOS AuthKit을 인증 프로바이더로 사용하려면, `laravel new`로 새 애플리케이션을 생성하는 과정에서 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 설정

WorkOS 기반의 스타터 키트로 애플리케이션을 생성한 후, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 발급되는 정보를 사용해야 합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

추가로, WorkOS 대시보드에서 애플리케이션의 홈페이지 URL도 반드시 설정해야 합니다. 이 URL은 사용자가 애플리케이션 로그아웃 시 리디렉션되는 위치입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트를 사용할 때에는, WorkOS AuthKit 설정에서 "Email + Password" 인증 방식을 비활성화하는 것을 권장합니다. 이를 통해 사용자는 소셜 인증 제공자, 패스키, "Magic Auth", SSO만으로 인증할 수 있고, 애플리케이션은 사용자 비밀번호를 전혀 다루지 않아도 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

또한 WorkOS AuthKit 세션 비활성화 타임아웃을 Laravel 애플리케이션의 세션 타임아웃(일반적으로 2시간)에 맞춰 설정하는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React 및 Vue 스타터 키트는 Inertia의 [서버 사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능을 지원합니다. SSR 호환 번들을 빌드하려면 아래 명령어를 실행하세요.

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령어도 제공됩니다. 이 명령어는 SSR 호환 번들 빌드 후, Laravel 개발 서버와 Inertia SSR 서버를 동시에 실행시켜 로컬 환경에서 SSR 기능을 테스트할 수 있습니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 키트 (Community Maintained Starter Kits)

Laravel 인스톨러를 사용해 새로운 애플리케이션을 생성할 때, Packagist에 등록된 커뮤니티 유지 스타터 키트의 패키지명을 `--using` 플래그와 함께 지정할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 제작하기

제작한 스타터 키트를 다른 사용자와 공유하려면, [Packagist](https://packagist.org)에 배포해야 합니다. 스타터 키트는 필요한 환경 변수 예시를 `.env.example` 파일에 정의하고, 별도의 설치 후 작업이 필요한 경우 `composer.json` 파일의 `post-create-project-cmd` 배열에 명시해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 스타터 키트 버전 업그레이드는 어떻게 하나요?

모든 스타터 키트는 새로운 애플리케이션 개발을 위한 견고한 출발점을 제공합니다. 전체 코드에 대한 소유권이 있어, 원하는 대로 수정·확장할 수 있습니다. 별도의 스타터 키트 업그레이드는 필요하지 않습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

이메일 인증을 활성화하려면, `App/Models/User.php` 모델에 `MustVerifyEmail` 인터페이스를 구현하도록 import하고 적용하세요.

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

회원가입 후, 사용자는 인증 이메일을 받게 됩니다. 특정 라우트에 대해 이메일 인증이 완료된 사용자만 접근하도록 하려면 해당 라우트에 `verified` 미들웨어를 추가하세요.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 변형 스타터 키트 사용 시에는 이메일 인증이 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

애플리케이션 브랜딩에 맞춰 기본 이메일 템플릿을 커스터마이즈하고 싶을 수 있습니다. 이메일 템플릿을 수정하려면, 아래 명령어로 이메일 관련 뷰 파일을 애플리케이션에 복사해 사용하세요.

```
php artisan vendor:publish --tag=laravel-mail
```

해당 명령을 실행하면 `resources/views/vendor/mail` 경로에 여러 파일이 생성됩니다. 이 파일들과, `resources/views/vendor/mail/themes/default.css`를 자유롭게 수정해 기본 이메일 템플릿과 스타일을 변경할 수 있습니다.
