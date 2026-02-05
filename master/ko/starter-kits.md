# 스타터 킷 (Starter Kits)

- [소개](#introduction)
- [스타터 킷을 사용한 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 킷](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 킷 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [인증](#authentication)
    - [기능 활성화 및 비활성화](#enabling-and-disabling-features)
    - [사용자 생성 및 비밀번호 재설정 커스터마이즈](#customizing-actions)
    - [이중 인증(2FA)](#two-factor-authentication)
    - [속도 제한(Rate Limiting)](#rate-limiting)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 킷](#community-maintained-starter-kits)
- [자주 묻는 질문(FAQ)](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션 개발을 더 빠르게 시작할 수 있도록 [애플리케이션 스타터 킷](https://laravel.com/starter-kits)을 제공합니다. 이 스타터 킷은 회원가입 및 인증에 필요한 라우트, 컨트롤러, 뷰를 포함하고 있어, Laravel 애플리케이션 구축에 빠르게 돌입할 수 있게 해줍니다. 스타터 킷은 인증 기능 구현을 위해 [Laravel Fortify](/docs/master/fortify)를 사용합니다.

이 스타터 킷을 반드시 사용해야 하는 것은 아닙니다. 원한다면 Laravel을 새로 설치하여 처음부터 직접 애플리케이션을 개발할 수도 있습니다. 어떤 방법을 택하든 여러분의 멋진 개발을 기대합니다!

<a name="creating-an-application"></a>
## 스타터 킷을 사용한 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 킷을 활용해 새로운 Laravel 애플리케이션을 생성하려면, 우선 [PHP와 Laravel CLI 툴을 설치](/docs/master/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, 다음 명령어로 Laravel 설치기 CLI 툴을 Composer로 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

그 다음, Laravel 설치기 CLI를 이용해 애플리케이션을 만드세요. 설치기는 선호하는 스타터 킷을 선택하도록 안내합니다:

```shell
laravel new my-app
```

애플리케이션을 생성한 후, NPM을 이용해 프런트엔드 의존성을 설치하고 Laravel 개발 서버를 시작하세요:

```shell
cd my-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하고 나면, 여러분의 애플리케이션은 [http://localhost:8000](http://localhost:8000)에서 접근할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 킷 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 킷은 [Inertia](https://inertiajs.com)를 활용한, React 프런트엔드와 함께 현대적인 Laravel 애플리케이션을 만들 수 있는 강력한 출발점을 제공합니다.

Inertia를 통해 서버 사이드 라우팅과 컨트롤러 구조를 그대로 이용하면서도, React 기반의 최신 싱글 페이지 애플리케이션을 만들 수 있습니다. React의 프론트엔드 유연성과 Laravel의 강력한 백엔드 생산성, 그리고 매우 빠른 Vite 빌드를 모두 경험할 수 있습니다.

React 스타터 킷은 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 킷은 [Inertia](https://inertiajs.com)를 활용한, Vue 프론트엔드와 함께 Laravel 애플리케이션을 쉽게 시작할 수 있는 좋은 출발점을 제공합니다.

Inertia를 통해 서버 사이드 라우팅과 컨트롤러 구조를 그대로 유지하면서, 최신 싱글 페이지 Vue 애플리케이션을 만들 수 있습니다. Vue의 강력한 프론트엔드와 Laravel의 생산성, Vite의 번개같은 컴파일 속도를 모두 누릴 수 있습니다.

Vue 스타터 킷은 Vue Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 킷은 [Laravel Livewire](https://livewire.laravel.com)를 활용한 프런트엔드와 함께, Laravel 애플리케이션을 시작하는 데 최적의 선택지입니다.

Livewire는 오직 PHP만으로도 동적이고 반응적인 프런트엔드 UI를 만들 수 있게 해주는 강력한 도구입니다. 주로 Blade 템플릿을 사용하고, React나 Vue 기반의 SPA를 대체할 보다 단순한 대안을 원하는 팀에 적합합니다.

Livewire 스타터 킷은 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 함께 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 킷 커스터마이징 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 킷은 Inertia 2, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 모든 스타터 킷과 마찬가지로 백엔드와 프런트엔드의 모든 소스코드는 여러분이 완전히 수정할 수 있도록 애플리케이션 내에 존재합니다.

프런트엔드 코드는 주로 `resources/js` 디렉토리에 위치합니다. 이 코드들은 모두 자유롭게 수정하여 애플리케이션의 외관과 동작을 원하는 대로 조정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적으로 shadcn 컴포넌트를 활용하려면, 먼저 [원하는 컴포넌트를 찾은 뒤](https://ui.shadcn.com), 다음과 같이 `npx` 명령어로 컴포넌트를 퍼블리시하세요:

```shell
npx shadcn@latest add switch
```

이 예시에서는 Switch 컴포넌트가 `resources/js/components/ui/switch.tsx` 파일에 퍼블리시됩니다. 퍼블리시가 완료된 컴포넌트는 페이지 어디에서든 자유롭게 사용할 수 있습니다:

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

React 스타터 킷은 기본 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 주요 레이아웃을 제공합니다. 기본값은 사이드바 레이아웃이지만, `resources/js/layouts/app-layout.tsx` 파일 상단에서 import되는 레이아웃을 수정하여 헤더 레이아웃으로 변경할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

#### 사이드바 종류

사이드바 레이아웃에는 기본 사이드바, "inset" 타입, "floating" 타입 세 가지 종류가 있습니다. 원하는 스타일로 `resources/js/components/app-sidebar.tsx` 컴포넌트를 수정하여 선택할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

#### 인증 페이지 레이아웃 종류

React 스타터 킷에 포함된 로그인, 회원가입 등 인증 페이지는 "simple", "card", "split" 세 가지 레이아웃 유형을 제공합니다.

사용하는 인증 레이아웃을 변경하려면, `resources/js/layouts/auth-layout.tsx` 파일 상단의 import를 원하는 레이아웃으로 수정하세요:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 킷은 Inertia 2, Vue 3 Composition API, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 스타터 킷과 마찬가지로 백엔드와 프런트엔드의 모든 소스코드는 여러분이 원하는 대로 완전히 수정할 수 있습니다.

프런트엔드 코드는 주로 `resources/js` 디렉토리에 위치합니다. 자유롭게 이 코드들을 수정하여 애플리케이션의 디자인 및 동작을 커스터마이즈할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue composables / hooks
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

shadcn-vue 컴포넌트를 추가로 활용하려면, [원하는 컴포넌트를 찾은 뒤](https://www.shadcn-vue.com), `npx`로 컴포넌트를 퍼블리시하세요:

```shell
npx shadcn-vue@latest add switch
```

이 예에서는 Switch 컴포넌트가 `resources/js/components/ui/Switch.vue` 파일로 퍼블리시됩니다. 퍼블리시가 완료된 컴포넌트는 모든 페이지에서 자유롭게 사용할 수 있습니다:

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

Vue 스타터 킷은 기본 "사이드바" 레이아웃과 "헤더" 레이아웃, 두 가지 주요 레이아웃을 제공합니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/AppLayout.vue` 파일 상단의 import를 수정해 헤더 레이아웃으로 변경할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

#### 사이드바 종류

사이드바 레이아웃에는 기본 사이드바, "inset" 타입, "floating" 타입 세 가지 종류가 있습니다. `resources/js/components/AppSidebar.vue` 컴포넌트의 variant를 변경해 원하는 스타일로 설정하세요:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

#### 인증 페이지 레이아웃 종류

Vue 스타터 킷의 인증 관련 페이지(로그인, 회원가입 등)는 "simple", "card", "split" 세 가지 레이아웃을 지원합니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/AuthLayout.vue` 파일 상단 import 라인을 원하는 레이아웃으로 수정하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 킷은 Livewire 4, Tailwind, 그리고 [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 다른 스타터 킷들과 마찬가지로, 백엔드와 프런트엔드 코드 모두 여러분의 애플리케이션 내에 존재해 완전한 커스터마이징이 가능합니다.

프런트엔드 코드는 주로 `resources/views` 디렉토리에 있습니다. 원하는 외관과 동작으로 자유롭게 수정할 수 있습니다:

```text
resources/views
├── components            # 재사용 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── layouts               # 애플리케이션 레이아웃
├── pages                 # Livewire 페이지
├── partials              # 재사용 Blade 파셜
├── dashboard.blade.php   # 인증된 사용자 대시보드
├── welcome.blade.php     # 비회원사용자 환영 페이지
```

#### 사용 가능한 레이아웃

Livewire 스타터 킷은 "사이드바"와 "헤더" 두 가지 주요 레이아웃을 제공합니다. 기본값은 사이드바 레이아웃이며, `resources/views/layouts/app.blade.php` 파일에서 사용되는 레이아웃을 헤더로 변경할 수 있습니다. 아울러, 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다:

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

#### 인증 페이지 레이아웃 종류

Livewire 스타터 킷의 인증 관련 페이지(로그인, 회원가입 등) 역시 "simple", "card", "split" 세 가지 레이아웃이 있습니다.

레이아웃을 변경하려면, `resources/views/layouts/auth.blade.php` 파일에서 사용되는 레이아웃을 원하는 것으로 수정하세요:

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 인증 (Authentication)

모든 스타터 킷은 인증 처리를 위해 [Laravel Fortify](/docs/master/fortify)를 사용합니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 관련 라우트, 컨트롤러, 로직을 제공합니다.

Fortify는 애플리케이션의 `config/fortify.php` 설정 파일에서 활성화된 기능에 따라 다음 인증 라우트들을 자동으로 등록합니다:

| Route                              | Method | 설명                                   |
| ---------------------------------- | ------ | -------------------------------------- |
| `/login`                           | `GET`    | 로그인 폼 표시                         |
| `/login`                           | `POST`   | 사용자 인증 처리                       |
| `/logout`                          | `POST`   | 로그아웃                               |
| `/register`                        | `GET`    | 회원가입 폼 표시                       |
| `/register`                        | `POST`   | 신규 사용자 생성                       |
| `/forgot-password`                 | `GET`    | 비밀번호 재설정 요청 폼 표시           |
| `/forgot-password`                 | `POST`   | 비밀번호 재설정 링크 전송              |
| `/reset-password/{token}`          | `GET`    | 비밀번호 재설정 폼 표시                |
| `/reset-password`                  | `POST`   | 비밀번호 갱신                          |
| `/email/verify`                    | `GET`    | 이메일 인증 안내 표시                  |
| `/email/verify/{id}/{hash}`        | `GET`    | 이메일 주소 인증                       |
| `/email/verification-notification` | `POST`   | 인증 메일 재전송                       |
| `/user/confirm-password`           | `GET`    | 비밀번호 확인 폼 표시                  |
| `/user/confirm-password`           | `POST`   | 비밀번호 확인 처리                     |
| `/two-factor-challenge`            | `GET`    | 2차 인증(2FA) 입력 폼 표시             |
| `/two-factor-challenge`            | `POST`   | 2FA 코드 검증                          |

`php artisan route:list` Artisan 명령어를 통해 모든 라우트 목록을 확인할 수 있습니다.

<a name="enabling-and-disabling-features"></a>
### 기능 활성화 및 비활성화 (Enabling and Disabling Features)

애플리케이션의 `config/fortify.php` 설정 파일에서 Fortify의 각 기능을 활성화/비활성화할 수 있습니다:

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

어떤 기능을 비활성화하려면, `features` 배열에서 해당 항목을 주석 처리하거나 삭제하세요. 예를 들어, 공개 회원가입을 막으려면 `Features::registration()`을 제거하면 됩니다.

[React](#react) 또는 [Vue](#vue) 스타터 킷을 사용하는 경우, 프런트엔드 코드에서도 비활성화된 기능과 관련된 라우트 참조를 제거해야 합니다. 예를 들어, 이메일 인증을 비활성화한 경우 Vue/React 컴포넌트 내에서 `verification` 라우트에 대한 import 및 참조를 지우세요. 이는 해당 스타터 킷이 타입 안전 라우팅을 위해 Wayfinder를 사용하여 빌드 시점에 라우트 정의를 생성하기 때문입니다. 더 이상 존재하지 않는 라우트가 참조되면 애플리케이션 빌드가 실패합니다.

<a name="customizing-actions"></a>
### 사용자 생성 및 비밀번호 재설정 커스터마이즈 (Customizing User Creation and Password Reset)

사용자가 회원가입하거나 비밀번호를 재설정할 때, Fortify는 애플리케이션의 `app/Actions/Fortify` 디렉토리에 위치한 액션 클래스들을 호출합니다:

| 파일                            | 설명                            |
| ------------------------------- | ------------------------------ |
| `CreateNewUser.php`             | 신규 사용자 검증 및 생성        |
| `ResetUserPassword.php`         | 비밀번호 검증 및 업데이트       |
| `PasswordValidationRules.php`   | 비밀번호 유효성 규칙 정의      |

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
### 이중 인증(2FA) (Two-Factor Authentication)

스타터 킷에는 이중 인증(2FA) 기능이 기본 탑재되어 있어, TOTP 호환 인증 앱을 이용해 계정의 보안을 강화할 수 있습니다. `config/fortify.php` 내의 `Features::twoFactorAuthentication()`로 기본 활성화되어 있습니다.

`confirm` 옵션은 사용자가 2FA를 완전히 활성화하기 전에 코드를 통해 검증하도록 하고, `confirmPassword` 옵션은 2FA 활성화/비활성화 시 비밀번호 확인을 요구합니다. 자세한 사항은 [Fortify의 2차 인증 문서](/docs/master/fortify#two-factor-authentication)를 참고하세요.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting) (Rate Limiting)

속도 제한은 브루트포스 공격 등 반복된 로그인 시도로 인증 엔드포인트가 과부하 되는 일을 막아줍니다. Fortify의 속도 제한 정책은 애플리케이션의 `FortifyServiceProvider`에서 커스터마이즈할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 스타터 킷 모두 Laravel 내장 인증 시스템을 활용해 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 또한, 각각의 스타터 킷에는 [WorkOS AuthKit](https://authkit.com) 기반 버전도 제공되며, 다음과 같은 기능을 추가합니다:

<div class="content-list" markdown="1">

- 소셜 인증(구글, 마이크로소프트, Github, 애플)
- 패스키 인증
- 이메일 기반 "매직 인증(Magic Auth)"
- SSO(싱글 사인온)

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정](https://workos.com)이 필요합니다. WorkOS는 월 100만 명까지 무료 인증 서비스를 제공합니다.

WorkOS AuthKit을 인증 제공자로 사용하려면, `laravel new`로 새로운 스타터 킷 기반 애플리케이션을 만들 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 킷 설정

WorkOS 기반 스타터 킷으로 애플리케이션을 만든 뒤, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 애플리케이션별로 제공된 값을 입력해야 합니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드 내 애플리케이션의 홈페이지 URL도 설정해야 합니다. 이 URL은 사용자가 로그아웃 한 뒤 리디렉션될 주소입니다.

#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 킷을 사용할 때는, WorkOS AuthKit 설정에서 "Email + Password" 인증을 비활성화하고, 소셜 인증/패스키/매직 인증/SSO 방식만 허용하는 것이 권장됩니다. 이렇게 하면 애플리케이션이 사용자 비밀번호를 직접 관리하지 않아도 됩니다.

#### AuthKit 세션 시간 초과 설정

추가적으로, 애플리케이션의 세션 시간 제한(예: 2시간)과 WorkOS AuthKit 세션 비활성화(타임아웃) 설정을 동일하게 맞추는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React 및 Vue 스타터 킷은 Inertia의 [서버 사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능과 호환됩니다. SSR용 번들을 빌드하려면 다음 명령어를 실행하세요:

```shell
npm run build:ssr
```

편리하게 사용할 수 있는 `composer dev:ssr` 명령어도 제공됩니다. 이 명령어는 SSR 빌드 완료 후, Laravel 개발서버와 Inertia SSR 서버를 한 번에 실행하여, Inertia의 서버 사이드 렌더링 엔진을 통해 로컬에서 바로 테스트할 수 있도록 해줍니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 킷 (Community Maintained Starter Kits)

Laravel 설치기를 이용해 애플리케이션을 새로 만들 때, Packagist에 공개된 커뮤니티 유지 스타터 킷을 `--using` 플래그로 지정할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

#### 스타터 킷 제작 및 공개

여러분이 만든 스타터 킷을 다른 사람들이 쓸 수 있도록 하려면, [Packagist](https://packagist.org)에 배포해야 합니다. 스타터 킷은 필요한 환경 변수들을 `.env.example` 파일에 정의해야 하며, 추가 설치 명령어가 있다면 `composer.json`의 `post-create-project-cmd` 배열에 명시해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문(FAQ) (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드 하나요?

각 스타터 킷은 새 애플리케이션 개발을 위한 견고한 출발점을 제공합니다. 소스코드의 전체 소유권을 갖게 되므로, 원하는 대로 자유롭게 수정 및 확장할 수 있습니다. 이미 코드 전체를 직접 관리함으로써, 별도의 스타터 킷 업그레이드는 필요하지 않습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증 기능은 어떻게 활성화하나요?

`App/Models/User.php` 모델에서 `MustVerifyEmail` import 구문을 주석 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 해주세요:

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

이렇게 하면 회원가입 후, 사용자는 인증 메일을 받게 됩니다. 특정 라우트는 사용자의 이메일이 인증됐을 때만 접근 가능하도록 하려면 `verified` 미들웨어를 아래와 같이 라우트에 추가하세요:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 버전의 스타터 킷을 사용할 경우 이메일 인증은 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

애플리케이션 브랜드에 맞춰 이메일 템플릿을 커스터마이즈할 수 있습니다. 템플릿 수정을 원하면, 다음 명령어로 이메일 뷰를 퍼블리시하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령어를 실행하면 `resources/views/vendor/mail` 내에 여러 파일이 생성됩니다. 또한, `resources/views/vendor/mail/themes/default.css`도 함께 수정해 기본 이메일 템플릿의 디자인을 바꿀 수 있습니다.
