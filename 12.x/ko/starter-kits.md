# 스타터 키트 (Starter Kits)

- [소개](#introduction)
- [스타터 키트를 사용한 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 커스터마이즈](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [이중 인증(2FA)](#two-factor-authentication)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 애플리케이션을 빠르게 구축할 수 있도록, [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공하고 있습니다. 이 스타터 키트는 Laravel 애플리케이션 구축 시 필요한 라우트, 컨트롤러, 뷰 등을 미리 포함하여 손쉽게 사용자 등록 및 인증 기능을 구현할 수 있도록 도와줍니다. 스타터 키트는 [Laravel Fortify](/docs/12.x/fortify)를 활용하여 인증 기능을 제공합니다.

하지만 이러한 스타터 키트의 사용은 필수가 아니며, 원한다면 Laravel를 새로 설치해서 직접 애플리케이션을 구축해도 무방합니다. 어떤 방식을 선택하든, 여러분만의 멋진 프로젝트를 만들 수 있을 것입니다!

<a name="creating-an-application"></a>
## 스타터 키트를 사용한 애플리케이션 생성 (Creating an Application Using a Starter Kit)

스타터 키트를 사용해 새로운 Laravel 애플리케이션을 생성하려면, 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/12.x/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, 아래 명령어로 Laravel 인스톨러 CLI 도구를 Composer를 통해 설치할 수 있습니다.

```shell
composer global require laravel/installer
```

그 다음, Laravel 인스톨러 CLI를 사용해 새로운 Laravel 애플리케이션을 생성하세요. 이 과정에서 사용할 스타터 키트를 선택하라는 안내가 표시됩니다.

```shell
laravel new my-app
```

애플리케이션이 생성되면, NPM으로 프론트엔드 의존성을 설치한 후 Laravel 개발 서버를 실행하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

개발 서버가 실행되면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000)로 접속하여 애플리케이션에 접근할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트 (Available Starter Kits)

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 기반으로, React 프론트엔드를 사용하는 현대적이며 견고한 Laravel 애플리케이션 구축에 적합한 출발점을 제공합니다.

Inertia를 이용하면, 서버 사이드 라우팅과 컨트롤러를 그대로 활용하면서도 React 기반의 싱글 페이지 애플리케이션(SPA)을 쉽게 만들 수 있습니다. 이를 통해 React의 프론트엔드 개발 능력과 Laravel의 뛰어난 백엔드 생산성, 그리고 Vite의 빠른 컴파일 성능을 모두 누릴 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 함께 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 기반으로, Vue 프론트엔드를 사용하는 Laravel 애플리케이션을 쉽게 시작할 수 있는 환경을 제공합니다.

Inertia를 사용하면 서버 사이드 라우팅과 컨트롤러를 그대로 유지하면서 Vue 기반의 현대적 싱글 페이지 애플리케이션을 개발할 수 있습니다. Vue의 프론트엔드 파워와 Laravel의 백엔드 생산성, Vite의 빠른 빌드 경험이 결합되어 효율적인 개발이 가능합니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 기반으로 한 Laravel 애플리케이션 구축에 최적화된 시작점을 제공합니다.

Livewire는 PHP만으로도 동적이고 반응성 있는 프론트엔드 UI를 쉽게 만들 수 있게 해주는 강력한 툴입니다. 주로 Blade 템플릿을 사용하는 팀이나, React 또는 Vue 같은 JavaScript 기반 SPA 프레임워크보다 더 단순한 대안을 원하는 개발자에게 적합합니다.

Livewire 스타터 키트는 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이즈 (Starter Kit Customization)

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 다른 스타터 키트와 마찬가지로, 모든 백엔드 및 프론트엔드 코드는 여러분의 애플리케이션 내에 저장되어 전체적인 커스터마이징이 가능합니다.

프론트엔드 코드 대부분은 `resources/js` 디렉터리에 위치하고 있습니다. 아래 구조를 참고하여 원하는 대로 화면이나 동작을 쉽게 커스터마이즈할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅(hooks)
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적으로 shadcn 컴포넌트를 프로젝트에 적용하려면, 먼저 [출시할 컴포넌트](https://ui.shadcn.com)를 찾은 뒤, `npx`로 컴포넌트를 추가합니다.

```shell
npx shadcn@latest add switch
```

이 예시에서는 Switch 컴포넌트가 `resources/js/components/ui/switch.tsx`에 생성됩니다. 컴포넌트가 추가되면 여러분의 각 페이지 내에서 사용할 수 있습니다.

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

React 스타터 키트에는 "사이드바 레이아웃"과 "헤더 레이아웃", 두 가지 주요 레이아웃이 포함되어 있습니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일의 상단 import를 수정해 헤더 레이아웃으로 변경할 수 있습니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본, "인셋(inset)", "플로팅(floating)" 등 세 가지 변형이 있습니다. 원하는 변형은 `resources/js/components/app-sidebar.tsx` 컴포넌트의 코드를 아래와 같이 수정하여 선택할 수 있습니다.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트에 포함된 인증(로그인, 회원가입 등) 페이지는 "simple", "card", "split" 등 세 가지의 레이아웃 변형을 지원합니다.

인증 페이지 레이아웃을 변경하려면 `resources/js/layouts/auth-layout.tsx` 파일의 상단 import를 수정합니다.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 다른 스타터 키트와 마찬가지로, 전체 백엔드와 프론트엔드 코드는 여러분의 애플리케이션 내에서 자유롭게 커스터마이즈할 수 있습니다.

프론트엔드 코드는 대부분 `resources/js` 폴더에 있습니다. 원하는 부분을 자유롭게 수정하여 화면이나 동작을 바꿀 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 컴포저블(컴포넌트 외부에서 사용하는 훅 개념)
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn-vue 컴포넌트를 적용하려면, 먼저 [추가할 컴포넌트](https://www.shadcn-vue.com)를 찾고 아래 명령으로 프로젝트에 적용하세요.

```shell
npx shadcn-vue@latest add switch
```

이 명령어를 사용하면 Switch 컴포넌트가 `resources/js/components/ui/Switch.vue`에 생성됩니다. 추가된 컴포넌트는 각 페이지에서 아래와 같이 쉽게 사용할 수 있습니다.

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

Vue 스타터 키트 역시 "사이드바 레이아웃"과 "헤더 레이아웃" 두 가지 주요 레이아웃을 제공합니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/AppLayout.vue` 파일의 import 부분을 수정하여 헤더 레이아웃으로 전환할 수 있습니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

Vue의 사이드바 레이아웃도 기본, "인셋", "플로팅" 등 3가지 변형을 제공합니다. `resources/js/components/AppSidebar.vue` 파일의 variant 속성을 수정해 원하는 스타일을 선택하세요.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

로그인 및 회원가입 등 Vue 스타터 키트의 인증 페이지 역시 "simple", "card", "split" 세 가지 레이아웃 변형을 제공합니다.

인증 레이아웃을 변경하려면 `resources/js/layouts/AuthLayout.vue`의 import를 원하는 레이아웃으로 수정하면 됩니다.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 3, Tailwind, [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 모든 백엔드 및 프론트엔드 코드는 여러분의 애플리케이션 안에 포함되어 있어, 필요에 따라 자유롭게 커스터마이즈할 수 있습니다.

#### Livewire와 Volt

프론트엔드 코드는 주로 `resources/views` 디렉터리에 위치합니다. 각 파일을 원하는 방식으로 수정해 애플리케이션 외형과 동작을 변경할 수 있습니다.

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # 재사용 Blade 부분 뷰
├── dashboard.blade.php   # 인증된 사용자 대시보드
├── welcome.blade.php     # 게스트 사용자 환영 페이지
```

#### 전통적 Livewire 컴포넌트

프론트엔드 코드가 `resources/views` 폴더에 위치하고, 해당 Livewire 컴포넌트의 백엔드 로직은 `app/Livewire` 디렉터리에 저장됩니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 키트도 "사이드바 레이아웃"과 "헤더 레이아웃" 두 가지를 제공합니다. 기본값은 사이드바 레이아웃이며, `resources/views/components/layouts/app.blade.php`의 레이아웃을 아래와 같이 헤더 레이아웃으로 바꿀 수 있습니다. 아울러, 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다.

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트에 포함된 로그인, 회원가입 등 인증 페이지도 "simple", "card", "split" 등 세 가지 레이아웃 변형을 지원합니다.

이 변형을 적용하려면 `resources/views/components/layouts/auth.blade.php` 파일에서 원하는 레이아웃을 사용하도록 수정하세요.

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="two-factor-authentication"></a>
## 이중 인증(2FA) (Two-Factor Authentication)

모든 스타터 키트에는 [Laravel Fortify](/docs/12.x/fortify#two-factor-authentication) 기반의 이중 인증(2FA) 기능이 내장되어 있어 사용자 계정에 추가적인 보안 계층을 제공합니다. 사용자는 TOTP(시간 기반 일회용 비밀번호) 방식의 인증 앱을 이용하여 계정을 안전하게 보호할 수 있습니다.

이중 인증 기능은 기본적으로 활성화되어 있으며, [Fortify](/docs/12.x/fortify#two-factor-authentication)에서 제공하는 다양한 설정을 모두 지원합니다.

```php
Features::twoFactorAuthentication([
    'confirm' => true,
    'confirmPassword' => true,
]);
```

<a name="workos"></a>
## WorkOS AuthKit 인증 (WorkOS AuthKit Authentication)

기본적으로 React, Vue, Livewire 스타터 키트는 모두 Laravel에서 제공하는 인증 시스템을 통해 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 인증 기능을 제공합니다. 추가로, 각 스타터 키트별로 [WorkOS AuthKit](https://authkit.com) 기반의 변형 버전도 제공되며 이 버전에서는 다음 기능을 지원합니다.

<div class="content-list" markdown="1">

- 소셜 인증(Google, Microsoft, GitHub, Apple)
- 패스키(생체 인증 등)
- 이메일 기반 "매직 인증(Magic Auth)"
- SSO(싱글사인온)

</div>

WorkOS 인증 프로바이더를 사용하려면 [WorkOS 계정이 필요](https://workos.com)합니다. WorkOS는 월별 활성 사용자 100만 명까지 무료 인증 서비스를 제공합니다.

WorkOS AuthKit을 인증 프로바이더로 사용하고 싶다면, `laravel new` 명령어로 애플리케이션을 만들 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트로 애플리케이션을 생성한 후, 애플리케이션의 `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 발급받은 값과 일치해야 합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션의 홈페이지 URL을 설정해야 하며, 이 URL은 사용자가 로그아웃한 후 리디렉션되는 경로입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방식 설정

WorkOS 기반 스타터 키트 사용 시, "이메일+비밀번호" 인증을 WorkOS AuthKit 설정에서 비활성화하도록 권장합니다. 그 대신 소셜 인증, 패스키, "매직 인증", SSO만을 허용하면 애플리케이션 측에서 비밀번호를 직접 다룰 필요가 없습니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

또한, WorkOS AuthKit 세션 비활성(미사용) 타임아웃을 Laravel 애플리케이션 내에서 설정한 세션 만료 기준(일반적으로 2시간)과 일치시킬 것을 권장합니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React 및 Vue 스타터 키트는 Inertia의 [서버 사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering)을 완벽하게 지원합니다. 애플리케이션에 SSR 호환 번들을 빌드하려면 아래 명령어를 실행하세요.

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령도 제공됩니다. 이 명령은 SSR 호환 번들을 빌드한 후, Laravel 개발 서버와 Inertia SSR 서버를 동시에 시작해서 SSR 환경에서 애플리케이션을 로컬로 테스트할 수 있도록 도와줍니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 키트 (Community Maintained Starter Kits)

Laravel 인스톨러로 새로운 애플리케이션을 만들 때, Packagist에 등록된 커뮤니티 유지 스타터 키트도 손쉽게 사용할 수 있습니다. `--using` 플래그에 원하는 키트 이름을 지정하세요.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 만들기

직접 만든 스타터 키트를 다른 개발자와 공유하려면, [Packagist](https://packagist.org)에 배포해야 합니다. 키트에서 필요한 환경 변수는 `.env.example` 파일에 반드시 정의하고, 필요 시 추가 설치 명령어는 `composer.json`의 `post-create-project-cmd` 배열에 명시해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문 (Frequently Asked Questions)

<a name="faq-upgrade"></a>
#### 업그레이드는 어떻게 하나요?

모든 스타터 키트는 새로운 애플리케이션을 구축할 때 강력한 출발점을 제공합니다. 코드 소유권이 전적으로 여러분에게 있으므로, 원하는 만큼 수정 및 커스터마이즈가 가능합니다. 별도로 스타터 키트 자체를 주기적으로 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증 기능은 어떻게 활성화하나요?

이메일 인증을 사용하려면, 먼저 `App/Models/User.php` 모델에서 `MustVerifyEmail` import의 주석을 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 해야 합니다.

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

이렇게 하면 회원가입 완료 후 사용자에게 인증 메일이 전송됩니다. 사용자가 이메일 인증 전까지 특정 라우트 접근을 막고 싶다면, 해당 라우트에 `verified` 미들웨어를 추가하세요.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 변형 스타터 키트에서는 이메일 인증이 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿은 어떻게 수정하나요?

애플리케이션 브랜딩에 맞게 기본 이메일 템플릿을 커스터마이즈하려면, 다음 Artisan 명령어로 이메일 뷰 파일을 프로젝트에 publish해야 합니다.

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령을 실행하면 `resources/views/vendor/mail` 폴더에 여러 파일이 생성됩니다. 이 파일들과 `resources/views/vendor/mail/themes/default.css` 파일을 수정하여, 이메일 템플릿의 디자인과 스타일을 자유롭게 변경할 수 있습니다.