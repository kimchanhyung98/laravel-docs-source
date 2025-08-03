# 스타터 킷 (Starter Kits)

- [소개](#introduction)
- [스타터 킷을 사용하여 애플리케이션 생성하기](#creating-an-application)
- [사용 가능한 스타터 킷](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 킷 맞춤 설정](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 킷](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션을 빠르게 시작할 수 있도록, [애플리케이션 스타터 킷](https://laravel.com/starter-kits)을 제공합니다. 이 스타터 킷들은 Laravel 애플리케이션 구축을 위한 출발점으로 사용자 등록 및 인증에 필요한 라우트, 컨트롤러, 뷰를 포함하고 있습니다.

이 스타터 킷들은 반드시 사용해야 하는 것은 아니며, Laravel을 새로 설치하여 밑바닥부터 직접 애플리케이션을 만들어도 됩니다. 어떤 방식을 선택하든 훌륭한 결과물을 만들 수 있을 것입니다!

<a name="creating-an-application"></a>
## 스타터 킷을 사용하여 애플리케이션 생성하기

Laravel 스타터 킷 중 하나로 새 애플리케이션을 만들려면, 우선 [PHP와 Laravel CLI 도구를 설치해야 합니다](/docs/12.x/installation#installing-php). 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 설치 프로그램 CLI를 글로벌로 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

그다음, Laravel 설치 프로그램 CLI로 새 Laravel 애플리케이션을 생성하세요. 설치 프로그램이 선호하는 스타터 킷을 선택하도록 안내합니다:

```shell
laravel new my-app
```

Laravel 애플리케이션을 생성했다면, NPM을 통해 프론트엔드 의존성을 설치하고 Laravel 개발 서버를 시작하세요:

```shell
cd my-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면 웹 브라우저에서 애플리케이션에 [http://localhost:8000](http://localhost:8000) 경로로 접근할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 킷

<a name="react"></a>
### React

React 스타터 킷은 Inertia를 사용한 React 프론트엔드와 함께 Laravel 애플리케이션을 구축할 수 있는 현대적이고 견고한 출발점입니다.

Inertia는 전통적인 서버측 라우팅과 컨트롤러를 활용하면서도 모던한 단일 페이지 React 애플리케이션을 빌드할 수 있게 해줍니다. 이를 통해 React의 프론트엔드 강력함과 Laravel의 뛰어난 백엔드 생산성을 결합할 수 있으며, Vite를 통한 매우 빠른 컴파일도 제공합니다.

React 스타터 킷은 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 킷은 Inertia를 사용한 Vue 프론트엔드와 함께 Laravel 애플리케이션을 빌드하기 좋은 출발점입니다.

Inertia를 통해 전통적인 서버측 라우팅과 컨트롤러를 사용하면서 현대적인 단일 페이지 Vue 애플리케이션을 만들 수 있습니다. 덕분에 Vue의 강력한 프론트엔드 기능과 Laravel의 뛰어난 백엔드 생산성, 그리고 Vite의 빠른 컴파일을 활용할 수 있습니다.

Vue 스타터 킷은 Vue 3 Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 킷은 [Laravel Livewire](https://livewire.laravel.com)를 사용한 Laravel 애플리케이션 구축에 최적화된 출발점입니다.

Livewire는 PHP만으로 동적이고 반응형 프론트엔드를 만들 수 있는 강력한 방법으로, Blade 템플릿을 주로 사용하는 팀에게 적합하며 React나 Vue 같은 자바스크립트 중심 SPA 프레임워크의 복잡함을 덜어줍니다.

Livewire 스타터 킷은 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 킷 맞춤 설정

<a name="react-customization"></a>
### React

React 스타터 킷은 Inertia 2, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)로 구성되어 있습니다. 모든 백엔드와 프론트엔드 코드는 애플리케이션 내에 위치해 있어 완전한 맞춤화가 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉터리에 있습니다. 이 코드를 자유롭게 수정하여 애플리케이션의 외관과 동작을 맞춤 설정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가적인 shadcn 컴포넌트를 사용하려면, 먼저 [원하는 컴포넌트를 찾아보고](https://ui.shadcn.com) `npx`로 컴포넌트를 퍼블리시하세요:

```shell
npx shadcn@latest add switch
```

예를 들어 위 명령은 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx` 위치에 퍼블리시합니다. 퍼블리시된 컴포넌트는 페이지 어디서든 사용할 수 있습니다:

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

React 스타터 킷은 "sidebar" 레이아웃과 "header" 레이아웃 두 가지 기본 레이아웃을 제공합니다. 기본값은 sidebar 레이아웃이며, `resources/js/layouts/app-layout.tsx` 파일 상단에서 불러오는 레이아웃을 바꾸어 header 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // 기본값(제거 대상)
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // 추가 대상
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형 종류

sidebar 레이아웃은 기본 사이드바 변형, "inset" 변형, "floating" 변형 총 세 가지 변형을 제공합니다. `resources/js/components/app-sidebar.tsx` 컴포넌트에서 원하는 변형을 선택할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [기본 - 제거]
<Sidebar collapsible="icon" variant="inset"> [추가]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 킷의 인증 페이지들(로그인, 회원가입)은 "simple", "card", "split" 세 가지 레이아웃 옵션을 제공합니다.

인증 레이아웃을 변경하려면 `resources/js/layouts/auth-layout.tsx` 파일 상단의 레이아웃 불러오기 부분을 수정하세요:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // 제거
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // 추가
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 킷은 Inertia 2, Vue 3 Composition API, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 코드가 애플리케이션 내에 존재해 완전한 맞춤화가 가능합니다.

프론트엔드 코드 대부분은 `resources/js` 디렉터리에 있습니다. 자유롭게 수정하여 애플리케이션의 모양과 기능을 원하는 대로 조정할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue composables / 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn-vue 컴포넌트를 퍼블리시하려면, 먼저 [원하는 컴포넌트를 찾아](https://www.shadcn-vue.com) `npx`를 사용하세요:

```shell
npx shadcn-vue@latest add switch
```

위 예시 명령은 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue` 경로에 퍼블리시합니다. 이제 페이지 어디서든 이 컴포넌트를 사용할 수 있습니다:

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

Vue 스타터 킷도 "sidebar"와 "header" 두 가지 기본 레이아웃을 제공합니다. 기본값은 sidebar이며, `resources/js/layouts/AppLayout.vue` 상단에서 불러오는 레이아웃을 수정하여 header 레이아웃으로 변경할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // 기본값(제거)
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // 추가
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형 종류

sidebar 레이아웃은 기본 사이드바, "inset", 그리고 "floating" 총 세 가지 변형이 있습니다. `resources/js/components/AppSidebar.vue` 컴포넌트에서 원하는 변형으로 설정하세요:

```text
<Sidebar collapsible="icon" variant="sidebar"> [기본-제거]
<Sidebar collapsible="icon" variant="inset"> [추가]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 킷 내 인증 페이지들도 "simple", "card", "split" 세 가지 레이아웃 변형을 지원합니다.

변경하려면 `resources/js/layouts/AuthLayout.vue` 파일 상단의 레이아웃 불러오는 부분을 수정하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // 제거
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // 추가
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 킷은 Livewire 3, Tailwind, 그리고 [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 모든 백엔드, 프론트엔드 코드는 애플리케이션 내부에 있어 자유롭게 맞춤 설정할 수 있습니다.

#### Livewire와 Volt

프론트엔드 코드는 `resources/views` 디렉터리에 위치합니다. 자유롭게 수정하여 앱 외관과 동작을 조절하세요:

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # Flux 컴포넌트 커스텀
├── livewire              # Livewire 페이지
├── partials              # 재사용 가능한 Blade 부분 템플릿
├── dashboard.blade.php   # 인증된 사용자 대시보드
├── welcome.blade.php     # 게스트 용 환영 페이지
```

#### 전통적인 Livewire 컴포넌트

프론트엔드 코드는 `resources/views`에 위치하며, `app/Livewire`는 Livewire 컴포넌트를 위한 백엔드 로직이 담겨 있습니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 킷도 "sidebar"와 "header" 두 가지 주요 레이아웃을 제공합니다. 기본값은 sidebar이며, 이 레이아웃을 변경하려면 `resources/views/components/layouts/app.blade.php` 파일에서 사용 중인 레이아웃을 바꾸고, 메인 Flux 컴포넌트에 `container` 속성을 추가하세요:

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 킷의 인증 페이지도 "simple", "card", "split" 세 가지 레이아웃을 제공합니다.

변경하려면 `resources/views/components/layouts/auth.blade.php`에서 사용하는 레이아웃을 수정하세요:

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="workos"></a>
## WorkOS AuthKit 인증

기본적으로 React, Vue, Livewire 스타터 킷은 Laravel 내장 인증 시스템을 사용해 로그인, 회원가입, 비밀번호 초기화, 이메일 인증 등을 제공합니다. 더불어, 각 스타터 킷의 WorkOS AuthKit 기반 변형도 존재하며, 다음 기능을 지원합니다:

<div class="content-list" markdown="1">

- 소셜 인증 (Google, Microsoft, GitHub, Apple)
- Passkey 인증
- 이메일 기반 "Magic Auth"
- SSO (Single Sign-On)

</div>

WorkOS를 인증 공급자로 사용하려면 [WorkOS 계정](https://workos.com)이 필요합니다. WorkOS는 월 활성 사용자 100만 명까지 무료 인증 서비스를 제공합니다.

WorkOS AuthKit을 애플리케이션 인증 공급자로 사용하려면, `laravel new`로 새 애플리케이션 생성 시 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 킷 설정하기

WorkOS 기반 스타터 킷으로 새 애플리케이션을 만든 뒤, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 해당 값들은 WorkOS 대시보드에서 확인할 수 있습니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

추가로, WorkOS 대시보드에서 애플리케이션 홈페이지 URL을 설정하세요. 이 주소는 사용자가 로그아웃 시 리다이렉트되는 위치입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방법 설정하기

WorkOS 기반 스타터 킷을 사용할 때는 애플리케이션의 WorkOS AuthKit 설정에서 "이메일 + 비밀번호" 인증을 비활성화하는 것을 권장합니다. 이렇게 하면 사용자는 소셜 인증, passkey, Magic Auth, SSO로만 인증할 수 있어 애플리케이션에서 사용자 비밀번호를 다룰 필요가 없어집니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정하기

또한, WorkOS AuthKit 세션 비활성화 타임아웃을 Laravel 애플리케이션에서 설정한 세션 타임아웃(보통 2시간)과 동일하게 맞추는 것이 권장됩니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React와 Vue 스타터 킷은 Inertia의 [서버사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능을 지원합니다. Inertia SSR 호환 번들 빌드를 생성하려면 다음 명령을 실행하세요:

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령도 제공됩니다. 이 명령은 SSR 번들을 빌드한 뒤 Laravel 개발 서버와 Inertia SSR 서버를 함께 시작해, 로컬에서 서버사이드 렌더링 테스트가 가능합니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 킷

Laravel 설치 프로그램을 사용할 때 `--using` 플래그에 커뮤니티에서 관리하는 Packagist 스타터 킷을 지정할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 킷 직접 만들기

본인의 스타터 킷을 다른 사용자도 사용할 수 있게 하려면 [Packagist](https://packagist.org)에 배포해야 합니다. 스타터 킷은 `.env.example` 파일에 필요한 환경 변수들을 정의하고, 설치 후 실행할 명령어들은 `composer.json`의 `post-create-project-cmd` 배열에 명시해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드하나요?

각 스타터 킷은 다음 애플리케이션의 견고한 출발점을 제공합니다. 코드를 완벽히 소유할 수 있어 원하는 대로 수정하고 맞춤화해서 사용할 수 있습니다. 하지만 스타터 킷 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

`App/Models/User.php` 모델에서 `MustVerifyEmail` import 부분의 주석을 해제하고, 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 수정하세요:

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

회원 가입 후 사용자는 인증 이메일을 받게 됩니다. 이메일 인증이 완료될 때까지 접근을 제한하려면 라우트에 `verified` 미들웨어를 추가하세요:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> 이메일 인증은 [WorkOS](#workos) 스타터 킷 변형을 사용할 때는 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

기본 이메일 템플릿을 애플리케이션 브랜드에 맞게 커스텀하려면 아래 명령으로 메일 뷰를 퍼블리시하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

이 명령으로 `resources/views/vendor/mail` 내부에 여러 파일이 복사됩니다. 여기에 포함된 파일과 `resources/views/vendor/mail/themes/default.css` 파일을 수정하여 기본 이메일 템플릿의 모양과 스타일을 변경할 수 있습니다.