# 시작 템플릿 (Starter Kits)

- [소개](#introduction)
- [시작 템플릿으로 애플리케이션 생성하기](#creating-an-application)
- [사용 가능한 시작 템플릿](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [시작 템플릿 커스터마이즈](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [인증(Authentication)](#authentication)
    - [기능 활성화 및 비활성화](#enabling-and-disabling-features)
    - [사용자 생성 및 비밀번호 재설정 커스터마이징](#customizing-actions)
    - [이중 인증(2FA)](#two-factor-authentication)
    - [요청 제한(Rate Limiting)](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 시작 템플릿](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록, [애플리케이션 시작 템플릿](https://laravel.com/starter-kits)을 제공합니다. 시작 템플릿을 사용하면 사용자 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰가 모두 포함되어 있어 바로 Laravel 애플리케이션을 구축할 수 있습니다. 이 시작 템플릿은 인증 기능을 제공하기 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다.

이 템플릿들은 선택사항이며, 무조건 사용할 필요는 없습니다. Laravel을 새로 설치해서 직접 애플리케이션을 처음부터 만드는 것도 자유입니다. 어떤 방법을 선택하든, 여러분만의 멋진 서비스를 만들 수 있을 것입니다!

<a name="creating-an-application"></a>
## 시작 템플릿으로 애플리케이션 생성하기 (Creating an Application Using a Starter Kit)

시작 템플릿을 사용해 새로운 Laravel 애플리케이션을 만들려면, 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/12.x/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 인스톨러 CLI 도구를 설치하세요:

```shell
composer global require laravel/installer
```

이제 Laravel 인스톨러 CLI를 사용하여 새로운 Laravel 애플리케이션을 만듭니다. 인스톨러는 원하는 시작 템플릿을 선택하도록 안내합니다:

```shell
laravel new my-app
```

애플리케이션이 생성된 후, NPM을 통해 프론트엔드 의존성을 설치하고, Laravel 개발 서버를 실행하면 됩니다:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버를 시작하면, 웹 브라우저를 통해 [http://localhost:8000](http://localhost:8000)에서 애플리케이션에 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 시작 템플릿 (Available Starter Kits)

<a name="react"></a>
### React

React 시작 템플릿은 [Inertia](https://inertiajs.com)를 활용하여 React 프론트엔드와 함께 Laravel 애플리케이션을 구축하기 위한 강력하고 현대적인 기반을 제공합니다.

Inertia를 사용하면 전통적인 서버사이드 라우팅과 컨트롤러 방식을 그대로 유지한 채로, 현대적인 React 단일 페이지(싱글 페이지) 애플리케이션을 만들 수 있습니다. React의 강력한 프론트엔드와 Laravel의 뛰어난 생산성, 그리고 Vite의 빠른 빌드 환경을 함께 누릴 수 있습니다.

React 시작 템플릿은 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 시작 템플릿은 [Inertia](https://inertiajs.com)를 활용하여 Vue 프론트엔드와 함께 Laravel 애플리케이션을 구축하기에 최적화된 출발점을 제공합니다.

Inertia를 사용하면 전통적인 서버사이드 라우팅과 컨트롤러를 그대로 활용하면서, 현대적인 Vue 단일 페이지 애플리케이션을 만들 수 있습니다. Vue의 효율적인 프론트엔드와 Laravel의 강력한 백엔드, 그리고 신속한 Vite 빌드 시스템을 모두 경험할 수 있습니다.

Vue 시작 템플릿은 Vue Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 시작 템플릿은 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드와 함께하는 애플리케이션 개발을 위한 완벽한 시작점을 제공합니다.

Livewire는 오직 PHP만으로 동적이고 반응형인 프론트엔드 UI를 구축할 수 있는 강력한 도구입니다. 주로 Blade 템플릿을 사용하는 팀이나, React와 Vue 같은 JavaScript 기반 SPA 프레임워크보다 간단한 대안을 찾는 경우에 Livewire가 적합합니다.

Livewire 시작 템플릿은 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 시작 템플릿 커스터마이즈 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 시작 템플릿은 Inertia 2, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 모든 시작 템플릿과 마찬가지로, 서버 및 프론트엔드 코드는 애플리케이션 내부에 모두 존재하여 전면적으로 커스터마이징할 수 있습니다.

프론트엔드 코드는 주로 `resources/js` 디렉터리에 위치하며, 애플리케이션의 디자인과 동작을 자유롭게 수정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

추가적인 shadcn 컴포넌트를 가져와 사용하려면, 먼저 [원하는 컴포넌트를 찾고](https://ui.shadcn.com), `npx` 명령어로 컴포넌트를 퍼블리시하세요:

```shell
npx shadcn@latest add switch
```

이 예시에서는 Switch 컴포넌트가 `resources/js/components/ui/switch.tsx`에 추가됩니다. 퍼블리시 후에는 원하는 페이지 어디서든 사용할 수 있습니다:

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

#### 사용 가능한 레이아웃

React 시작 템플릿은 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 기본 레이아웃을 제공합니다. 사이드바 레이아웃이 기본이지만, `resources/js/layouts/app-layout.tsx` 파일에서 import하는 레이아웃을 변경하여 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

#### 사이드바 변형

사이드바 레이아웃은 기본 사이드바, "inset" 변형, "floating" 변형 등 세 가지 변형이 제공됩니다. 원하는 변형을 `resources/js/components/app-sidebar.tsx`에서 변경할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

#### 인증 페이지 레이아웃 변형

React 시작 템플릿에 포함된 로그인, 회원가입 등 인증 페이지도 "simple", "card", "split" 총 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/auth-layout.tsx` 파일 상단에서 import하는 레이아웃을 수정하세요:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 시작 템플릿은 Inertia 2, Vue 3 Composition API, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/)를 기반으로 구현되어 있습니다. 모든 시작 템플릿과 마찬가지로, 서버 및 프론트엔드 코드가 애플리케이션 내에 존재하여 전체 커스터마이즈가 가능합니다.

주요 프론트엔드 코드는 `resources/js` 디렉터리에 위치하며, 자유롭게 수정하여 기능과 스타일을 원하는 대로 구현할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 합성(composables)/훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

추가적인 shadcn-vue 컴포넌트를 사용하려면, 먼저 [원하는 컴포넌트를 찾은 뒤](https://www.shadcn-vue.com), `npx` 명령어로 컴포넌트를 퍼블리시하세요:

```shell
npx shadcn-vue@latest add switch
```

이렇게 하면 Switch 컴포넌트가 `resources/js/components/ui/Switch.vue`에 추가됩니다. 퍼블리시가 완료되면, 원하는 페이지에서 아래와 같이 사용할 수 있습니다:

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

#### 사용 가능한 레이아웃

Vue 시작 템플릿에는 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 기본 레이아웃이 있습니다. 사이드바 레이아웃이 기본이나, `resources/js/layouts/AppLayout.vue` 파일에서 import 레이아웃을 변경하면 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

#### 사이드바 변형

사이드바 레이아웃은 기본, "inset", "floating" 세 가지 변형이 있습니다. 원하는 변형을 `resources/js/components/AppSidebar.vue`에서 변경할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

#### 인증 페이지 레이아웃 변형

Vue 시작 템플릿의 로그인, 회원가입 등 인증 페이지도 "simple", "card", "split" 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/AuthLayout.vue` 파일 상단의 import를 수정하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 시작 템플릿은 Livewire 4, Tailwind, 그리고 [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 모든 시작 템플릿과 마찬가지로, 서버와 프론트엔드 코드는 애플리케이션 내에 존재하여 전면적으로 커스터마이즈할 수 있습니다.

프론트엔드 코드는 주로 `resources/views` 디렉터리에 위치하며, 다음과 같이 자유롭게 수정하여 원하는 스타일과 기능을 구현할 수 있습니다:

```text
resources/views
├── components            # 재사용 가능한 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── layouts               # 애플리케이션 레이아웃
├── pages                 # Livewire 페이지
├── partials              # 재사용 Blade 파셜
├── dashboard.blade.php   # 인증된 사용자용 대시보드
├── welcome.blade.php     # 비회원(게스트)용 환영 페이지
```

#### 사용 가능한 레이아웃

Livewire 시작 템플릿은 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 기본 레이아웃을 제공합니다. 사이드바가 기본이나, `resources/views/layouts/app.blade.php`에서 사용하는 레이아웃을 바꾸면 헤더 레이아웃으로 변경할 수 있습니다. 또한 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다:

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

#### 인증 페이지 레이아웃 변형

Livewire 시작 템플릿에 포함된 로그인, 회원가입 등 인증 페이지도 "simple", "card", "split" 세 가지 레이아웃을 제공합니다.

인증 레이아웃을 변경하려면, `resources/views/layouts/auth.blade.php`에서 사용하는 레이아웃을 수정하세요:

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 인증(Authentication)

모든 시작 템플릿은 인증 처리를 위해 [Laravel Fortify](/docs/12.x/fortify)를 사용합니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 인증과 관련된 라우트, 컨트롤러, 로직을 모두 제공합니다.

Fortify는 `config/fortify.php` 설정 파일 내에서 활성화된 기능에 따라 다음과 같은 인증 관련 라우트를 자동 등록합니다:

| Route                              | Method | 설명                                     |
| ---------------------------------- | ------ | ------------------------------------------ |
| `/login`                           | `GET`    | 로그인 폼 표시                            |
| `/login`                           | `POST`   | 사용자 인증 처리                          |
| `/logout`                          | `POST`   | 사용자 로그아웃 처리                      |
| `/register`                        | `GET`    | 회원가입 폼 표시                          |
| `/register`                        | `POST`   | 신규 사용자 생성                          |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 폼 표시              |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 발송                 |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 폼 표시                   |
| `/reset-password`                  | `POST`   | 비밀번호 변경 처리                        |
| `/email/verify`                    | `GET`    | 이메일 인증 알림 표시                     |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 주소 인증 확인                     |
| `/email/verification-notification` | `POST`   | 인증 이메일 다시 발송                     |
| `/user/confirm-password`           | `GET`    | 비밀번호 확인 폼 표시                     |
| `/user/confirm-password`           | `POST`   | 비밀번호 확인 처리                        |
| `/two-factor-challenge`            | `GET`    | 이중 인증(2FA) 도전 폼 표시               |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 검증                             |

`php artisan route:list` 명령어를 실행하면 애플리케이션 내 모든 라우트 목록을 확인할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화

애플리케이션의 `config/fortify.php` 파일 내 `features` 배열에서 Fortify 기능 활성화 여부를 제어할 수 있습니다:

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

기능을 비활성화하려면, 해당 항목을 `features` 배열에서 주석처리하거나 삭제하세요. 예를 들어, `Features::registration()`을 제거하면 공개 회원가입이 비활성화됩니다.

[React](#react) 또는 [Vue](#vue) 시작 템플릿을 사용하는 경우, 프론트엔드 코드 내에서도 비활성화된 기능 라우트에 대한 참조를 모두 제거해야 합니다. 예를 들어 이메일 인증을 비활성화하면, 관련된 라우트 import 및 참조도 코드에서 삭제해야 합니다. 이는 해당 템플릿들이 Wayfinder를 사용하여 타입 안전 라우팅을 빌드 시 생성하는데, 더이상 존재하지 않는 라우트를 참조할 경우 빌드가 실패하기 때문입니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이징

사용자가 회원가입하거나 비밀번호를 재설정할 때 Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉터리 내 액션 클래스를 호출합니다:

| 파일                             | 설명                                            |
| -------------------------------- | ------------------------------------------------|
| `CreateNewUser.php`              | 새 사용자 유효성 검사 및 생성                   |
| `ResetUserPassword.php`          | 사용자 비밀번호 유효성 검사 및 변경              |
| `PasswordValidationRules.php`    | 비밀번호 유효성 규칙 정의                       |

예를 들어, 회원가입 로직을 커스터마이즈하려면 `CreateNewUser` 액션을 수정하면 됩니다:

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
### 이중 인증(2FA)

시작 템플릿에는 이중 인증(2FA)이 내장되어 있어, 사용자가 모든 TOTP 호환 인증 앱으로 계정을 보호할 수 있습니다. 2FA는 `config/fortify.php` 설정 파일의 `Features::twoFactorAuthentication()`을 통해 기본적으로 활성화됩니다.

`confirm` 옵션은 2FA를 완전히 활성화하기 위해 사용자가 한 번 더 코드를 확인하도록 강제하며, `confirmPassword` 옵션은 2FA 활성화/비활성화 시 비밀번호 확인을 요구합니다. 자세한 내용은 [Fortify 이중 인증 문서](/docs/12.x/fortify#two-factor-authentication)를 참고하세요.

<a name="rate-limiting"></a>
### 요청 제한(Rate Limiting)

요청 제한은 무차별 대입 공격 및 반복되는 로그인 시도로부터 인증 엔드포인트를 보호합니다. Fortify의 요청 제한 동작은 `FortifyServiceProvider` 내에서 커스터마이즈할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 시작 템플릿은 Laravel의 인증 시스템을 활용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 기능을 제공합니다. 추가로, 각 시작 템플릿에는 [WorkOS AuthKit](https://authkit.com) 기반 버전도 제공되어 다음과 같은 기능을 사용할 수 있습니다:

<div class="content-list" markdown="1">

- 소셜 인증(Google, Microsoft, GitHub, Apple 등)
- 패스키(passkey) 인증
- 이메일 기반 "Magic Auth"
- SSO(싱글사인온)

</div>

WorkOS를 인증 공급자로 사용하려면 [WorkOS 계정이 필요](https://workos.com)합니다. WorkOS는 월간 100만 명까지의 활성 사용자에 대해 무료 인증을 지원합니다.

WorkOS AuthKit을 인증 공급자로 사용하려면, `laravel new`를 이용해 새 시작 템플릿 기반 애플리케이션을 생성할 때 WorkOS 옵션을 선택하면 됩니다.

### WorkOS 시작 템플릿 설정

WorkOS 기반 시작 템플릿을 사용해 애플리케이션을 만들었다면, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경변수를 반드시 설정해야 합니다. 이 값들은 WorkOS 대시보드의 애플리케이션 정보와 일치해야 합니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션 홈페이지 URL도 설정해야 하며, 이는 사용자가 로그아웃된 후 리다이렉트될 위치입니다.

#### AuthKit 인증 방식 설정

WorkOS 기반 시작 템플릿을 사용할 때는, WorkOS AuthKit 설정에서 "이메일 + 비밀번호" 인증을 비활성화하고, 소셜 인증, 패스키, "Magic Auth", SSO만 활성화하는 것을 권장합니다. 이를 통해 애플리케이션이 직접 사용자 비밀번호 정보를 다루지 않아도 됩니다.

#### AuthKit 세션 만료 시간 설정

또한 WorkOS AuthKit의 세션 비활성화(만료) 시간을 Laravel 애플리케이션의 세션 만료 임계값(일반적으로 2시간)에 맞춰 설정하는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React 및 Vue 시작 템플릿은 Inertia의 [서버사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. 애플리케이션에 SSR 지원 번들을 빌드하려면, 다음과 같이 명령어를 실행하세요:

```shell
npm run build:ssr
```

또한, `composer dev:ssr` 명령어도 제공되어, SSR 번들 빌드 완료 후 Laravel 개발 서버와 Inertia SSR 서버를 동시에 실행할 수 있습니다. 이 명령어를 통해 Inertia의 서버사이드 렌더링 환경에서 로컬 테스트가 가능합니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 시작 템플릿 (Community Maintained Starter Kits)

Laravel 인스톨러로 새 애플리케이션을 생성할 때, `--using` 플래그를 활용해 Packagist에 등록된 원하는 커뮤니티 유지 시작 템플릿을 지정할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

#### 시작 템플릿 제작하기

여러 개발자와 시작 템플릿을 공유하려면, 먼저 [Packagist](https://packagist.org)에 등록해야 합니다. 템플릿의 `.env.example` 파일에 필요한 환경 변수들을 정의하고, post-install 명령어는 `composer.json`의 `post-create-project-cmd` 배열에 추가하세요.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 업그레이드는 어떻게 하나요?

시작 템플릿은 다음 애플리케이션을 위한 확실한 출발점을 제공합니다. 여러분이 전체 코드를 소유하고 있으므로 원하는 대로 수정, 커스터마이즈, 확장이 가능합니다. 별도로 템플릿 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증을 어떻게 활성화하나요?

이메일 인증을 추가하려면, 우선 `App/Models/User.php` 모델에서 `MustVerifyEmail` import의 주석을 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 하세요:

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

회원가입 후 사용자는 인증 이메일을 받게 됩니다. 특정 라우트는 이메일 인증되지 않은 사용자가 접근하지 못하도록 `verified` 미들웨어를 추가할 수 있습니다:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 변형 템플릿을 사용할 경우 이메일 인증은 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

기본 이메일 템플릿을 변경하여 애플리케이션의 브랜드에 맞추고 싶을 때가 있을 수 있습니다. 이 템플릿을 수정하려면 아래 커맨드로 이메일 뷰 파일을 애플리케이션에 퍼블리시하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령어로 `resources/views/vendor/mail` 아래에 여러 파일이 생성됩니다. 이 중 원하는 파일과 `resources/views/vendor/mail/themes/default.css`를 수정하여 이메일 템플릿의 디자인과 룩앤필을 바꿀 수 있습니다.
