# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [스타터 키트를 활용한 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [인증(Authentication)](#authentication)
    - [기능 활성화 및 비활성화](#enabling-and-disabling-features)
    - [사용자 생성 및 비밀번호 재설정 커스터마이즈](#customizing-actions)
    - [2단계 인증](#two-factor-authentication)
    - [속도 제한(Rate Limiting)](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 관리 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션의 개발을 더욱 빠르게 시작할 수 있도록, [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공합니다. 이 스타터 키트는 Laravel 애플리케이션 개발의 출발점을 만들어주며, 여러분의 애플리케이션 사용자의 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰를 포함하고 있습니다. 스타터 키트는 인증 처리를 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다.

이러한 스타터 키트 사용은 필수가 아니며, 단순히 Laravel의 새 복사본을 설치해서 직접 애플리케이션을 구축할 수도 있습니다. 어떤 방법을 선택하더라도 여러분이 멋진 애플리케이션을 만들 것이라 믿습니다!

<a name="creating-an-application"></a>
## 스타터 키트를 활용한 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 키트를 사용하여 새로운 Laravel 애플리케이션을 생성하려면, 먼저 [PHP 및 Laravel CLI 도구를 설치](/docs/12.x/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 설치기 CLI 도구를 아래와 같이 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

이후, Laravel 설치기 CLI를 사용하여 새로운 Laravel 애플리케이션을 생성하세요. 설치기 실행 중에 원하는 스타터 키트를 선택할 수 있습니다:

```shell
laravel new my-app
```

애플리케이션 생성 후, 프론트엔드 의존성을 NPM으로 설치하고 Laravel 개발 서버를 시작하면 됩니다:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버가 시작되면, 브라우저에서 [http://localhost:8000](http://localhost:8000)에서 애플리케이션에 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 이용해 React 기반의 Laravel 애플리케이션을 구축하는 데 견고하고 현대적인 출발점을 제공합니다.

Inertia는 고전적인 서버사이드 라우팅 및 컨트롤러를 활용해 모던한 싱글 페이지 React 애플리케이션을 만들 수 있게 합니다. 이를 통해 React의 프론트엔드 파워와 Laravel의 뛰어난 백엔드 생산성, 그리고 Vite의 매우 빠른 빌드 성능까지 모두 누릴 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 활용하여 Vue 프론트엔드로 Laravel 애플리케이션을 개발할 때 훌륭한 출발점을 제공합니다.

Inertia 덕분에, 고전적인 서버사이드 라우팅 및 컨트롤러를 통해 최신 싱글 페이지 Vue 애플리케이션을 구현할 수 있습니다. Vue 프론트엔드의 파워와 Laravel 백엔드의 뛰어난 생산성, 그리고 Vite의 초고속 컴파일을 모두 경험하실 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 채택합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com)를 프론트엔드로 사용하는 Laravel 애플리케이션을 개발할 때 완벽한 출발점을 제공합니다.

Livewire는 PHP만으로 동적이고 반응형인 프론트엔드 UI를 만드는 강력한 방법입니다. Blade 템플릿을 주로 사용하는 개발팀이나 JavaScript 기반 SPA 프레임워크(React, Vue)보다 더 간단한 대안을 찾는 경우에 특히 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 활용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 모든 스타터 키트와 마찬가지로, 백엔드 및 프론트엔드 코드가 애플리케이션 안에 모두 포함되어, 자유롭게 커스터마이즈할 수 있습니다.

프론트엔드 코드는 주로 `resources/js` 디렉터리에 위치합니다. 애플리케이션의 스타일 및 동작을 원하는 대로 아래와 같이 자유롭게 수정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn 컴포넌트를 가져오려면, 먼저 [추가하려는 컴포넌트를 찾고](https://ui.shadcn.com), 아래 명령어로 컴포넌트를 등록하세요:

```shell
npx shadcn@latest add switch
```

위 예시에서, 명령어 실행 시 `resources/js/components/ui/switch.tsx`에 Switch 컴포넌트가 추가됩니다. 컴포넌트가 등록되면, 다음과 같이 페이지 내에서 자유롭게 사용할 수 있습니다:

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

React 스타터 키트에는 "sidebar" 레이아웃과 "header" 레이아웃, 두 가지 주요 레이아웃이 포함되어 있습니다. 기본값은 sidebar 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일에서 import되는 레이아웃을 변경해 header 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 옵션(Variants)

sidebar 레이아웃에는 기본 sidebar, "inset", 그리고 "floating" 등 세 가지 변형이 있습니다. `resources/js/components/app-sidebar.tsx` 컴포넌트에서 원하는 옵션으로 변경할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 옵션

React 스타터 키트에 포함된 로그인, 회원가입 등의 인증 페이지는 "simple", "card", "split" 등 세 가지 레이아웃 옵션을 제공합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/auth-layout.tsx` 파일 최상단에서 import되는 레이아웃을 수정하세요:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구축됩니다. 다른 스타터 키트와 마찬가지로, 백엔드 및 프론트엔드 코드 전체가 여러분의 애플리케이션에 포함되어 완벽한 커스터마이즈가 가능합니다.

프론트엔드 코드는 주로 `resources/js` 디렉터리에 위치하고 있으며, 다음과 같은 디렉터리 구조를 가집니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 컴포저블/훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn-vue 컴포넌트를 등록하려면, 먼저 [등록할 컴포넌트를 찾은 뒤](https://www.shadcn-vue.com), 아래 명령어를 실행하세요:

```shell
npx shadcn-vue@latest add switch
```

예를 들어, 이 명령을 실행하면 Switch 컴포넌트가 `resources/js/components/ui/Switch.vue`에 추가됩니다. 컴포넌트 등록 후에는 아래와 같이 자유롭게 사용할 수 있습니다:

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

Vue 스타터 키트도 "sidebar"와 "header" 두 가지 주요 레이아웃을 제공합니다. 기본값은 sidebar 레이아웃이고, `resources/js/layouts/AppLayout.vue` 파일에서 import되는 레이아웃을 수정하여 header로 변경할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 옵션(Variants)

sidebar 레이아웃에는 기본 sidebar, "inset", "floating" 등 세 가지 변형이 있습니다. 원하는 옵션 적용은 `resources/js/components/AppSidebar.vue` 컴포넌트에서 설정할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 옵션

Vue 스타터 키트의 로그인, 회원가입 등 인증 페이지 역시 "simple", "card", "split" 세 가지 레이아웃 변형이 제공됩니다.

인증 레이아웃 변경 시에는 `resources/js/layouts/AuthLayout.vue` 파일에서 import되는 레이아웃을 수정하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 4, Tailwind, [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 다른 스타터 키트와 같이, 백엔드 및 프론트엔드 전체 코드를 여러분의 애플리케이션 안에서 자유롭게 수정할 수 있습니다.

프론트엔드 코드는 주로 `resources/views` 디렉터리에 배치되어 있습니다:

```text
resources/views
├── components            # 재사용 가능한 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── layouts               # 애플리케이션 레이아웃
├── pages                 # Livewire 페이지
├── partials              # 재사용 가능한 Blade partials
├── dashboard.blade.php   # 인증된 사용자 대시보드
├── welcome.blade.php     # 게스트 사용자 환영 페이지
```

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 키트에도 "sidebar"와 "header" 두 가지 주요 레이아웃이 제공됩니다. 기본값은 sidebar 레이아웃이며, `resources/views/layouts/app.blade.php` 파일에서 사용되는 레이아웃을 변경할 수 있습니다. 또한, main Flux 컴포넌트에 `container` 속성을 반드시 추가해야 합니다:

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 옵션

Livewire 스타터 키트의 로그인, 회원가입 등 인증 페이지 역시 "simple", "card", "split"의 세 가지 레이아웃 변형을 지원합니다.

인증 레이아웃을 변경하려면, `resources/views/layouts/auth.blade.php` 파일에서 사용되는 레이아웃을 수정하세요:

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 인증(Authentication)

모든 스타터 키트는 인증 처리를 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능에 필요한 라우트, 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에서 활성화된 기능에 따라 다음과 같은 인증 라우트를 자동으로 등록합니다:

| Route                              | Method | 설명                              |
| ----------------------------------- | ------ | --------------------------------- |
| `/login`                           | `GET`    | 로그인 폼 표시                    |
| `/login`                           | `POST`   | 사용자 인증 처리                   |
| `/logout`                          | `POST`   | 로그아웃 처리                      |
| `/register`                        | `GET`    | 회원가입 폼 표시                   |
| `/register`                        | `POST`   | 신규 사용자 생성                   |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 폼 표시        |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 발송           |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 폼 표시            |
| `/reset-password`                  | `POST`   | 비밀번호 업데이트                  |
| `/email/verify`                    | `GET`    | 이메일 인증 안내 표시               |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 주소 인증                    |
| `/email/verification-notification` | `POST`   | 인증 이메일 재전송                  |
| `/user/confirm-password`           | `GET`    | 비밀번호 확인 폼 표시               |
| `/user/confirm-password`           | `POST`   | 비밀번호 확인                       |
| `/two-factor-challenge`            | `GET`    | 2FA 인증 코드 입력 폼 표시           |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 확인                       |

애플리케이션의 모든 라우트 목록은 `php artisan route:list` 명령어로 확인할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화 (Enabling and Disabling Features)

애플리케이션의 `config/fortify.php` 파일에서 어떤 Fortify 기능을 활성화할지 제어할 수 있습니다:

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

기능을 비활성화하려면, 해당 기능을 `features` 배열에서 주석 처리하거나 삭제하면 됩니다. 예를 들어, 공개 회원가입을 막으려면 `Features::registration()`을 제거하세요.

[React](#react) 또는 [Vue](#vue) 스타터 키트를 사용할 경우, 비활성화한 기능과 관련된 모든 프론트엔드 코드(라우트 import 등)도 반드시 함께 제거해야 합니다. 이들 스타터 키트는 타입 안정성이 보장되는 라우팅을 위해 Wayfinder를 사용하며, 빌드 시점에 라우트 정의를 생성합니다. 존재하지 않는 라우트를 참조할 경우, 애플리케이션 빌드가 실패할 수 있습니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이즈 (Customizing User Creation and Password Reset)

사용자가 회원가입을 하거나 비밀번호를 재설정할 경우, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉터리 내 액션 클래스를 호출합니다:

| 파일                          | 설명                                   |
| ----------------------------- | -------------------------------------- |
| `CreateNewUser.php`           | 신규 사용자 유효성 검사 및 생성         |
| `ResetUserPassword.php`       | 사용자 비밀번호 유효성 검사 및 업데이트 |
| `PasswordValidationRules.php` | 비밀번호 유효성 검사 규칙 정의          |

예시로, 회원가입 로직을 커스터마이즈하려면 `CreateNewUser` 액션을 편집하세요:

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

모든 스타터 키트에는 기본적으로 내장된 2단계 인증(2FA)이 포함되어 있어, 사용자가 TOTP 호환 인증 앱을 활용해 계정을 더욱 안전하게 보호할 수 있습니다. 2FA는 `config/fortify.php` 설정에서 `Features::twoFactorAuthentication()`로 기본 활성화되어 있습니다.

`confirm` 옵션은 2FA 활성화 시 사용자가 코드를 직접 입력하여 검증하도록 하고, `confirmPassword` 옵션은 2FA 활성화/비활성화 전 비밀번호 확인을 요구합니다. 자세한 내용은 [Fortify 2단계 인증 문서](/docs/12.x/fortify#two-factor-authentication)를 참고하세요.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

속도 제한은 무차별 대입 공격이나 반복 로그인 시도를 막아 인증 엔드포인트의 과부하를 방지합니다. Fortify의 속도 제한 동작은 애플리케이션의 `FortifyServiceProvider`에서 조정할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 스타터 키트에서는 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 추가로, 각 스타터 키트별로 [WorkOS AuthKit](https://authkit.com)을 통해 제공되는 변형도 있으며, 여기에는 다음과 같은 기능이 포함됩니다:

<div class="content-list" markdown="1">

- 소셜 인증(구글, 마이크로소프트, GitHub, 애플)
- 패스키 인증(Passkey authentication)
- 이메일 기반 "Magic Auth"
- SSO

</div>

WorkOS 인증 공급자를 사용하려면 [WorkOS 계정이 필요](https://workos.com)합니다. WorkOS는 월간 최대 100만 명의 사용자까지 무료 인증 서비스를 제공합니다.

WorkOS AuthKit을 인증 공급자로 사용하려면, `laravel new`로 스타터 키트 기반 애플리케이션을 생성할 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트로 새 애플리케이션을 만든 뒤에는, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 제공하는 정보를 그대로 입력하십시오:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

추가로, WorkOS 대시보드에서 애플리케이션 홈페이지 URL을 올바르게 설정해야 합니다. 이 URL은 사용자가 로그아웃할 때 리디렉션되는 위치입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트를 사용할 때는, WorkOS AuthKit 설정 내 "Email + Password" 인증 기능을 비활성화하고, 사용자가 소셜 인증, 패스키, Magic Auth, SSO만을 이용해 인증하게 하는 것을 권장합니다. 이렇게 하면 애플리케이션이 사용자 비밀번호를 직접 처리할 필요가 사라집니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 만료 시간 설정

또한, WorkOS AuthKit 세션 비활성화 타임아웃이 Laravel 애플리케이션의 세션 만료 시간(일반적으로 2시간)과 일치하도록 설정하는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React 및 Vue 스타터 키트는 Inertia의 [서버사이드 렌더링](https://inertiajs.com/server-side-rendering) 기능을 지원합니다. 애플리케이션을 Inertia SSR에 호환되게 패키징하려면 `build:ssr` 명령어를 실행하세요:

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령어도 제공됩니다. 이 명령어를 실행하면, SSR 대응 번들 빌드 이후 Laravel 개발 서버 및 Inertia SSR 서버가 동시에 시작되어, 로컬 환경에서 SSR 엔진을 활용한 테스트가 가능합니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 관리 스타터 키트 (Community Maintained Starter Kits)

Laravel 설치기를 이용해 새로운 애플리케이션을 만들 때, Packagist에 등록된 커뮤니티 관리 스타터 키트 패키지를 `--using` 옵션에 명시할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 직접 제작

직접 제작한 스타터 키트를 다른 사람들과 공유하려면, 해당 패키지를 [Packagist](https://packagist.org)에 등록해야 합니다. 필수 환경 변수는 `.env.example` 파일에 정의하고, 필요한 post-install 명령들은 스타터 키트의 `composer.json`의 `post-create-project-cmd` 배열에 추가해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 업그레이드는 어떻게 하나요?

모든 스타터 키트는 새로운 애플리케이션 개발의 강력한 출발점을 제공합니다. 전체 소스코드에 대한 소유권이 부여되므로, 구성 및 확장, 커스터마이즈를 자유롭게 할 수 있습니다. 별도로 스타터 키트 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

이메일 인증을 활용하려면, `App/Models/User.php` 모델에서 `MustVerifyEmail` import 주석을 해제하고, 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 설정하세요:

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

회원가입 후, 사용자에게 이메일 인증 메일이 전송됩니다. 특정 라우트에 인증된 이메일 유저만 접근하도록 제한하려면, 라우트에 `verified` 미들웨어를 추가하세요:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 변형 스타터 키트에서는 이메일 인증이 필수 사항이 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿은 어떻게 바꾸나요?

애플리케이션의 브랜딩에 맞게 이메일 템플릿을 커스터마이즈하고 싶을 때는, 다음 명령어로 이메일 뷰를 게시(publish)하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령을 실행하면 여러 파일이 `resources/views/vendor/mail`에 생성됩니다. 이들 파일과 `resources/views/vendor/mail/themes/default.css` 파일을 수정하여 기본 이메일 템플릿의 디자인을 원하는 대로 변경할 수 있습니다.
