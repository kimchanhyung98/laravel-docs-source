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
    - [사용자 생성 및 비밀번호 재설정 커스터마이즈](#customizing-actions)
    - [2단계 인증(2FA)](#two-factor-authentication)
    - [요청 제한(Rate Limiting)](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트는 회원 가입과 인증에 필요한 라우트, 컨트롤러, 뷰(View)를 포함하여 Laravel 애플리케이션의 기본 구조를 신속하게 구축할 수 있게 해줍니다. 스타터 키트는 인증 기능 구현을 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다.

이 스타터 키트는 선택사항이므로 반드시 사용해야 하는 것은 아닙니다. 원한다면 Laravel의 새 복사본을 설치해 직접 처음부터 애플리케이션을 구축해도 됩니다. 어떤 방법을 선택하시든, 멋진 결과물을 만들 수 있을 것이라 확신합니다!

<a name="creating-an-application"></a>
## 스타터 키트를 이용한 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 키트를 사용해 새로운 Laravel 애플리케이션을 생성하려면 먼저 [PHP 및 Laravel CLI 도구 설치](/docs/12.x/installation#installing-php)가 필요합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 설치기 명령줄 도구를 아래와 같이 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

이후, Laravel 설치기 명령어를 사용해 새 Laravel 애플리케이션을 만듭니다. 설치기가 어떤 스타터 키트를 사용할지 물어볼 것입니다.

```shell
laravel new my-app
```

애플리케이션이 생성된 후, 프론트엔드 의존성을 NPM으로 설치하고 개발 서버를 실행하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버가 실행되면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 이용한 React 프론트엔드를 갖춘 모던한 Laravel 애플리케이션을 개발할 수 있는 강력한 시작점을 제공합니다.

Inertia를 활용하면 전통적인 서버 사이드 라우팅과 컨트롤러를 통해 싱글 페이지 React 애플리케이션을 손쉽게 만들 수 있습니다. React의 강력한 프론트엔드 기능과 Laravel 백엔드의 뛰어난 생산성, 그리고 Vite의 빠른 컴파일 속도를 동시에 누릴 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 이용한 Vue 프론트엔드를 갖춘 Laravel 애플리케이션 개발을 위한 훌륭한 출발점을 제공합니다.

Inertia를 통해 Vue 기반의 싱글 페이지 애플리케이션을 Laravel의 서버 사이드 라우팅과 컨트롤러로 쉽게 구축할 수 있습니다. Vue의 프론트엔드 기능과 Laravel, Vite가 결합된 생산성을 경험해보세요.

이 스타터 키트는 Vue의 Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 갖춘 Laravel 애플리케이션 개발에 최적화된 시작점을 제공합니다.

Livewire는 오직 PHP만으로도 동적이고 반응적인 프론트엔드 UI를 만들 수 있는 강력한 도구입니다. 주로 Blade 템플릿을 사용하는 팀이나, React나 Vue 같은 자바스크립트 기반 SPA 프레임워크보다 더 단순한 대안을 찾는 경우에 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 모든 스타터 키트와 마찬가지로 백엔드와 프론트엔드 코드는 애플리케이션 내에 포함되어 있어, 최대한 자유롭게 커스터마이징할 수 있습니다.

프론트엔드 코드는 대부분 `resources/js` 디렉토리에 위치합니다. 애플리케이션의 외관과 동작을 자유롭게 변경할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅(Hook)
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

추가적인 shadcn 컴포넌트를 발행하려면, 먼저 [원하는 컴포넌트 조회](https://ui.shadcn.com) 후, 아래와 같이 `npx` 명령어를 사용해 발행합니다.

```shell
npx shadcn@latest add switch
```

이렇게 하면 Switch 컴포넌트가 `resources/js/components/ui/switch.tsx`에 추가됩니다. 이제 어느 페이지에서든 컴포넌트를 사용할 수 있습니다.

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

React 스타터 키트는 "사이드바(sidebar)" 레이아웃과 "헤더(header)" 레이아웃, 두 가지 주요 레이아웃을 제공합니다. 기본값은 사이드바 레이아웃이지만, `resources/js/layouts/app-layout.tsx` 파일에서 불러오는 레이아웃을 바꾸면 헤더 레이아웃으로 전환할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃은 기본 사이드바, "인셋(inset)" 변형, "플로팅(floating)" 변형으로 세 가지가 있습니다. 원하는 변형을 `resources/js/components/app-sidebar.tsx` 컴포넌트에서 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

로그인 및 회원 가입 페이지 등 인증 관련 페이지 역시 "simple", "card", "split" 세 가지 레이아웃 변형을 지원합니다.

레이아웃을 변경하려면 `resources/js/layouts/auth-layout.tsx` 파일에서 임포트하는 레이아웃을 바꿔주세요.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 코드가 애플리케이션 내에 포함되어 있어 원하는 만큼 자유롭게 수정할 수 있습니다.

프론트엔드 코드는 `resources/js` 디렉토리에 대부분 저장됩니다. 외관이나 동작을 원하는 대로 커스터마이징할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 컴포저블 / 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

추가적인 shadcn-vue 컴포넌트를 발행하려면, 먼저 [컴포넌트 조회](https://www.shadcn-vue.com) 후, 아래와 같이 `npx` 명령어를 사용해 발행할 수 있습니다.

```shell
npx shadcn-vue@latest add switch
```

Switch 컴포넌트가 `resources/js/components/ui/Switch.vue` 파일로 추가됩니다. 이후 모든 페이지에서 사용할 수 있습니다.

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

Vue 스타터 키트 역시 "사이드바(sidebar)"와 "헤더(header)" 두 가지 주요 레이아웃을 제공합니다. 기본값은 사이드바 레이아웃이며, 상단의 `resources/js/layouts/AppLayout.vue` 파일의 임포트를 변경하면 헤더 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

사이드바에는 기본, "인셋(inset)", "플로팅(floating)" 세 가지 변형이 있습니다. `resources/js/components/AppSidebar.vue`에서 원하는 변형을 적용할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트의 로그인, 회원 가입 등 인증 페이지 역시 "simple", "card", "split" 세 가지 레이아웃을 지원합니다.

레이아웃을 변경하려면 `resources/js/layouts/AuthLayout.vue` 파일에서 임포트를 수정하면 됩니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 3, Tailwind, [Flux UI](https://fluxui.dev/) 기반으로 설계되었습니다. 모든 코드가 애플리케이션 내에 포함되어 있어 원하는 만큼 수정할 수 있습니다.

#### Livewire와 Volt

프론트엔드 코드는 `resources/views` 디렉토리에 위치합니다. 애플리케이션의 외관 및 기능을 자유롭게 편집할 수 있습니다.

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # 재사용 가능한 Blade 파셜
├── dashboard.blade.php   # 인증된 사용자의 대시보드
├── welcome.blade.php     # 게스트용 환영 페이지
```

#### 전통적인 Livewire 컴포넌트

프론트엔드 코드는 `resources/views`에, 연결된 백엔드 로직은 `app/Livewire` 디렉토리에 있습니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 키트도 "사이드바(sidebar)"와 "헤더(header)" 두 가지 주요 레이아웃을 지원합니다. 기본은 사이드바 레이아웃이며, `resources/views/components/layouts/app.blade.php`에서 헤더 레이아웃으로 변경할 수 있습니다. 이때 메인 Flux 컴포넌트에는 `container` 속성을 추가해야 합니다.

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트의 인증 관련 페이지(예: 로그인, 회원 가입) 역시 "simple", "card", "split" 세 가지 레이아웃을 지원합니다.

레이아웃을 바꾸려면 `resources/views/components/layouts/auth.blade.php` 파일에서 변경하세요.

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="authentication"></a>
## 인증 (Authentication)

모든 스타터 키트는 인증 처리를 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다. Fortify는 로그인, 회원 가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능의 라우트와 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에서 활성화된 기능에 따라 다음과 같은 인증 라우트를 자동으로 등록합니다.

| Route                              | Method | 설명                                    |
| ---------------------------------- | ------ | --------------------------------------- |
| `/login`                           | `GET`    | 로그인 폼 표시                          |
| `/login`                           | `POST`   | 사용자 인증 실행                        |
| `/logout`                          | `POST`   | 로그아웃 처리                           |
| `/register`                        | `GET`    | 회원 가입 폼 표시                       |
| `/register`                        | `POST`   | 신규 사용자 생성                        |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 폼 표시            |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 이메일 발송        |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 폼 표시                 |
| `/reset-password`                  | `POST`   | 비밀번호 업데이트                       |
| `/email/verify`                    | `GET`    | 이메일 인증 안내 표시                   |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 인증 처리                        |
| `/email/verification-notification` | `POST`   | 인증 이메일 재발송                      |
| `/user/confirm-password`           | `GET`    | 비밀번호 재확인 폼 표시                 |
| `/user/confirm-password`           | `POST`   | 비밀번호 재확인 처리                    |
| `/two-factor-challenge`            | `GET`    | 2FA 도전 폼 표시                        |
| `/two-factor-challenge`            | `POST`   | 2FA(2단계 인증) 코드 확인               |

애플리케이션 내의 모든 라우트는 `php artisan route:list` 아티즌 명령어로 조회할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화 (Enabling and Disabling Features)

애플리케이션의 `config/fortify.php` 설정 파일에서 Fortify의 각 기능별 활성화 여부를 제어할 수 있습니다.

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

특정 기능을 비활성화하려면 해당 항목을 주석 처리하거나 `features` 배열에서 제거하면 됩니다. 예를 들어, `Features::registration()`을 제거하면 공개 회원 가입 기능이 비활성화됩니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이즈 (Customizing User Creation and Password Reset)

사용자가 회원 가입을 하거나 비밀번호를 재설정할 때, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉토리에 위치한 액션 클래스를 실행합니다.

| 파일                              | 설명                                  |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | 신규 사용자 유효성 검사 및 생성        |
| `ResetUserPassword.php`       | 비밀번호 유효성 검사 및 변경          |
| `PasswordValidationRules.php` | 비밀번호 유효성 검사 규칙 정의        |

예를 들어, 회원 가입 시 로직을 커스터마이즈하려면 `CreateNewUser` 액션을 다음과 같이 수정하면 됩니다.

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
### 2단계 인증(2FA) (Two-Factor Authentication)

모든 스타터 키트에는 2단계 인증(2FA)이 기본 제공되어, 사용자는 TOTP 방식 호환 인증 앱을 사용해 계정을 더욱 안전하게 보호할 수 있습니다. 2FA는 `config/fortify.php`의 `Features::twoFactorAuthentication()`로 기본 활성화되어 있습니다.

`confirm` 옵션은 2FA 활성화 과정에서 코드를 한번 더 요구하며, `confirmPassword` 옵션은 2FA 설정 또는 해제 시 비밀번호 재확인을 요구합니다. 자세한 내용은 [Fortify의 2단계 인증 문서](/docs/12.x/fortify#two-factor-authentication)를 참고하세요.

<a name="rate-limiting"></a>
### 요청 제한(Rate Limiting) (Rate Limiting)

요청 제한(Rate Limiting)은 과도한 로그인 시도(브루트 포스 공격 등)로 인증 엔드포인트가 과부하되는 것을 막아줍니다. Fortify의 rate limiting 동작은 애플리케이션의 `FortifyServiceProvider`에서 커스터마이즈할 수 있습니다.

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 스타터 키트는 Laravel의 내장 인증 시스템을 사용해 로그인, 회원 가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 기능을 제공합니다. 이에 더해, 각각의 스타터 키트에는 [WorkOS AuthKit](https://authkit.com) 기반 변형도 제공됩니다.

<div class="content-list" markdown="1">

- 소셜 인증(구글, 마이크로소프트, GitHub, 애플)
- 패스키 인증
- 이메일 기반 "매직 인증"(Magic Auth)
- SSO(싱글 사인온)

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정이 필요](https://workos.com)합니다. WorkOS는 월 100만 명 미만 활성 사용자에 대해 무료 인증을 제공합니다.

WorkOS AuthKit을 인증 제공자로 사용하려면, `laravel new`로 새 스타터 키트 기반 애플리케이션을 생성할 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트로 새 애플리케이션을 만들었다면, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수 값을 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 애플리케이션을 생성할 때 제공받은 값과 동일해야 합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션 홈페이지(URL)를 설정해야 합니다. 이 URL은 사용자가 로그아웃한 뒤 리디렉션되는 주소입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트 사용 시에는, 애플리케이션의 WorkOS AuthKit 설정에서 "이메일+비밀번호" 인증 방식을 비활성화하는 것이 권장됩니다. 이렇게 하면 사용자는 소셜 인증, 패스키, "매직 인증", SSO만 사용해 인증할 수 있게 되어, 애플리케이션에서 직접 비밀번호를 관리할 필요가 없어집니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

WorkOS AuthKit 세션의 비활성화 타임아웃도 Laravel 애플리케이션의 세션 타임아웃 값(일반적으로 2시간)에 맞춰 설정하는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React와 Vue 스타터 키트는 Inertia의 [서버 사이드 렌더링(server-side rendering)](https://inertiajs.com/server-side-rendering) 기능을 지원합니다. SSR에 최적화된 번들을 빌드하려면 아래 명령어를 실행하세요.

```shell
npm run build:ssr
```

추가로, 편의를 위해 `composer dev:ssr` 명령어가 제공됩니다. 이 명령어는 SSR용 번들을 빌드한 후 Laravel 개발 서버와 Inertia SSR 서버를 함께 시작하여, Inertia SSR로 로컬 애플리케이션을 테스트할 수 있습니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 키트 (Community Maintained Starter Kits)

Laravel 설치기를 사용해 새 애플리케이션을 만들 때, `--using` 플래그에 Packagist에 등록된 커뮤니티 유지 스타터 키트를 지정할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 제작 및 공개

직접 만든 스타터 키트를 다른 사람들과 공유하려면, [Packagist](https://packagist.org)에 공개해야 합니다. 필수 환경 변수는 `.env.example` 파일에 정의하고, 설치 후 추가 명령어가 필요하면 `composer.json`의 `post-create-project-cmd` 배열에 명시해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 업그레이드는 어떻게 하나요?

각 스타터 키트는 새로운 애플리케이션 개발을 위한 단단한 시작점을 제공합니다. 모든 소스 코드에 대한 완전한 소유권이 있으므로, 원하는 대로 수정, 커스터마이즈하여 직접 구축하시면 됩니다. 스타터 키트 자체의 별도 업그레이드는 필요하지 않습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증(Email Verification)은 어떻게 활성화하나요?

이메일 인증 기능을 추가하려면 `App/Models/User.php` 모델에서 `MustVerifyEmail`을 임포트한 후, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하게 하면 됩니다.

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

이후 회원 등록이 성공하면 사용자는 인증 이메일을 받게 됩니다. 이메일 인증이 완료되기 전까지 일부 라우트 접근을 막으려면, 라우트 그룹에 `verified` 미들웨어를 추가하세요.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 변형 스타터 키트 사용 시에는 이메일 인증이 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿은 어떻게 수정하나요?

애플리케이션의 브랜드에 맞추어 기본 이메일 템플릿을 커스터마이즈하고 싶다면, 아래 명령어로 이메일 뷰 파일을 애플리케이션에 복사할 수 있습니다.

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령어 실행 후, `resources/views/vendor/mail`에 여러 파일이 생성됩니다. 원하는 템플릿 파일과 `resources/views/vendor/mail/themes/default.css` 파일을 수정해 이메일 디자인과 외관을 변경할 수 있습니다.
