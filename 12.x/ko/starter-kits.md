# 스타터 키트

- [소개](#introduction)
- [스타터 키트를 활용한 애플리케이션 생성](#creating-an-application)
- [이용 가능한 스타터 키트](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 키트 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 키트](#community-maintained-starter-kits)
- [자주 묻는 질문(FAQ)](#faqs)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션 개발을 빠르게 시작할 수 있도록 [애플리케이션 스타터 키트](https://laravel.com/starter-kits)를 제공하고 있습니다. 이 스타터 키트는 다음 Laravel 애플리케이션을 만드는데 필요한 라우트, 컨트롤러, 뷰 등 사용자 등록과 인증을 위한 기반 구성을 포함하고 있습니다.

스타터 키트를 사용하지 않아도 되며, 원하는 경우 Laravel의 새 복사본을 직접 설치해 처음부터 애플리케이션을 구축할 수 있습니다. 어떤 방법을 선택하더라도, 여러분이 멋진 것을 만들어낼 것이라 믿습니다!

<a name="creating-an-application"></a>
## 스타터 키트를 활용한 애플리케이션 생성

우리의 스타터 키트 중 하나를 사용하여 새로운 Laravel 애플리케이션을 생성하려면, 먼저 [PHP와 Laravel CLI 도구를 설치](/docs/{{version}}/installation#installing-php)해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer를 통해 Laravel 설치 CLI 도구를 다음과 같이 설치할 수 있습니다:

```shell
composer global require laravel/installer
```

그 다음, Laravel 설치 CLI를 사용해 새로운 Laravel 애플리케이션을 만드세요. 설치 도구가 원하는 스타터 키트 선택을 안내합니다:

```shell
laravel new my-app
```

애플리케이션 생성 후, 프론트엔드 의존성을 NPM을 통해 설치하고 Laravel 개발 서버를 시작하세요:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버를 시작하면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접근할 수 있습니다.

<a name="available-starter-kits"></a>
## 이용 가능한 스타터 키트

<a name="react"></a>
### React

React 스타터 키트는 [Inertia](https://inertiajs.com)를 활용한 React 프론트엔드 기반의 Laravel 애플리케이션 구축을 위한 견고하고 최신의 출발점을 제공합니다.

Inertia를 사용하면, 전통적인 서버사이드 라우팅과 컨트롤러를 활용하여 현대적인 싱글 페이지 React 애플리케이션을 만들 수 있습니다. 즉, React의 강력한 프론트엔드 능력과 Laravel의 생산성, 빠른 Vite 번들링을 동시에 누릴 수 있습니다.

React 스타터 키트는 React 19, TypeScript, Tailwind, [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 사용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 키트는 [Inertia](https://inertiajs.com)를 기반으로 Vue 프론트엔드와 함께 Laravel 애플리케이션을 구축할 수 있는 좋은 출발점을 제공합니다.

Inertia를 통해 서버사이드 라우팅과 컨트롤러를 사용하는 현대적인 싱글 페이지 Vue 애플리케이션을 만들 수 있습니다. Vue의 프론트엔드 파워에 Laravel의 뛰어난 백엔드 생산성과 초고속 Vite 빌드를 결합할 수 있습니다.

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 활용한 Laravel 애플리케이션 구축을 위한 완벽한 시작점을 제공합니다.

Livewire는 순수 PHP만으로 동적이고 반응형인 프론트엔드 UI를 구축할 수 있는 강력한 방법입니다. Blade 템플릿을 주로 사용하는 팀에게 적합하며, React나 Vue 같은 자바스크립트 기반 SPA 프레임워크에 비해 더 간단한 대안을 찾는 팀에게 이상적입니다.

Livewire 스타터 키트는 Livewire, Tailwind, [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 사용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이징

<a name="react-customization"></a>
### React

React 스타터 키트는 Inertia 2, React 19, Tailwind 4, [shadcn/ui](https://ui.shadcn.com)로 구축되어 있습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 애플리케이션 내부에 포함되어 전체 커스터마이징이 가능합니다.

프론트엔드 코드는 주로 `resources/js` 디렉터리에 위치합니다. 원하는 대로 코드를 수정하여 애플리케이션의 모습과 동작을 변경할 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React hooks
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn 컴포넌트를 게시하려면, 먼저 [게시하려는 컴포넌트를 찾고](https://ui.shadcn.com) `npx` 명령어로 게시하세요:

```shell
npx shadcn@latest add switch
```

이 예시에서, Switch 컴포넌트는 `resources/js/components/ui/switch.tsx`에 게시됩니다. 게시된 후, 어떤 페이지에서도 해당 컴포넌트를 사용할 수 있습니다:

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
#### 이용 가능한 레이아웃

React 스타터 키트는 기본적으로 "사이드바"와 "헤더" 두 가지 주요 레이아웃을 제공합니다. 사이드바 레이아웃이 기본이며, `resources/js/layouts/app-layout.tsx` 파일 상단에서 불러오는 레이아웃을 변경해 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 기본, "inset", "floating" 등 세 가지 변형이 있습니다. `resources/js/components/app-sidebar.tsx` 파일에서 원하는 변형을 선택해 설정할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트의 로그인 및 회원가입과 같은 인증 페이지에도 "simple", "card", "split"의 세 가지 레이아웃 변형이 제공됩니다.

`resources/js/layouts/auth-layout.tsx` 파일 상단에서 불러오는 레이아웃을 변경해 인증 레이아웃을 전환하세요:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 키트는 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)로 구성되어 있습니다. 모든 스타터 키트처럼 백엔드와 프론트엔드 코드가 애플리케이션 내에 위치해 있어 자유로운 커스터마이징이 가능합니다.

프론트엔드 코드는 주로 `resources/js` 디렉터리에 위치합니다. 원하는 대로 코드를 수정해 애플리케이션의 모습과 동작을 개성 있게 바꿀 수 있습니다:

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue 컴포저블 / 훅
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 정의
```

추가 shadcn-vue 컴포넌트를 게시하려면, 먼저 [게시할 컴포넌트를 찾고](https://www.shadcn-vue.com) `npx`로 다음과 같이 게시합니다:

```shell
npx shadcn-vue@latest add switch
```

이 명령어는 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue`에 게시합니다. 게시된 후, 페이지 어디에서든 컴포넌트를 사용할 수 있습니다:

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
#### 이용 가능한 레이아웃

Vue 스타터 키트도 "사이드바"와 "헤더" 두 가지 주요 레이아웃을 포함합니다. 기본값은 사이드바 레이아웃이며, `resources/js/layouts/AppLayout.vue` 상단의 import 구성을 바꾸면 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃 역시 기본, "inset", "floating" 세 가지 변형이 있습니다. `resources/js/components/AppSidebar.vue`에서 옵션을 수정할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트의 인증(로그인, 회원가입) 페이지 역시 "simple", "card", "split" 세 가지 레이아웃 변형을 제공합니다.

`resources/js/layouts/AuthLayout.vue` 파일 상단의 import 구성을 변경하여 인증 레이아웃을 바꿀 수 있습니다:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 키트는 Livewire 3, Tailwind, [Flux UI](https://fluxui.dev/)로 구성되어 있습니다. 모든 스타터 키트처럼 전체 백엔드와 프론트엔드 코드가 애플리케이션에 포함되어 자유로운 커스터마이징이 가능합니다.

#### Livewire와 Volt

프론트엔드 코드는 `resources/views` 디렉터리에 위치합니다. 원하는 대로 코드를 수정하여 애플리케이션의 모양과 동작을 변경하세요:

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스터마이징 된 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # Blade 파샬
├── dashboard.blade.php   # 인증된 사용자 대시보드
├── welcome.blade.php     # 게스트 환영 페이지
```

#### 전통적인 Livewire 컴포넌트

프론트엔드 코드는 `resouces/views`에 위치하며, 해당 Livewire 컴포넌트의 백엔드 로직은 `app/Livewire` 디렉터리에 있습니다.

<a name="livewire-available-layouts"></a>
#### 이용 가능한 레이아웃

Livewire 스타터 키트도 "사이드바"와 "헤더" 두 가지 주요 레이아웃을 제공합니다. 사이드바가 기본이며, `resources/views/components/layouts/app.blade.php` 파일에서 사용하는 레이아웃을 변경해 헤더 레이아웃으로 전환할 수 있습니다. 또한, 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다:

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 키트의 로그인, 회원가입 등 인증 페이지 역시 "simple", "card", "split" 세 가지 레이아웃 변형을 지원합니다.

`resources/views/components/layouts/auth.blade.php` 파일에서 사용하는 레이아웃을 다음처럼 변경하세요:

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="workos"></a>
## WorkOS AuthKit 인증

기본적으로 React, Vue, Livewire 스타터 키트 모두 Laravel 기본 인증 시스템을 사용해 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등의 기능을 제공합니다. 더불어, 각 스타터 키트의 [WorkOS AuthKit](https://authkit.com) 기반 버전도 제공하여 다음과 같은 기능을 지원합니다:

<div class="content-list" markdown="1">

- 소셜 인증(구글, 마이크로소프트, GitHub, 애플)
- 패스키 인증
- 이메일 기반 "매직 인증"
- SSO

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정이 필요합니다](https://workos.com). WorkOS는 월간 1백만 명까지 무료 인증을 제공합니다.

WorkOS AuthKit을 인증 제공자로 사용하려면, `laravel new`로 새 스타터 키트 기반 애플리케이션을 만들 때 WorkOS 옵션을 선택하세요.

### WorkOS 스타터 키트 설정

WorkOS 기반 스타터 키트로 새 애플리케이션을 생성한 후, `.env` 파일에 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값은 WorkOS 대시보드에서 애플리케이션에 부여된 값과 일치해야 합니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한, WorkOS 대시보드에서 애플리케이션의 홈페이지 URL도 설정해야 합니다. 이 주소는 사용자가 로그아웃한 후 리디렉션되는 위치입니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방법 설정

WorkOS 기반 스타터 키트 사용 시, 애플리케이션의 WorkOS AuthKit 설정에서 "이메일 + 비밀번호" 인증을 비활성화하는 것이 좋습니다. 이렇게 하면 소셜 로그인, 패스키, "매직 인증", SSO만 활성화되어 비밀번호를 직접 관리하지 않아도 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 타임아웃 설정

또한, WorkOS AuthKit 세션 비활성화 타임아웃도 Laravel 애플리케이션의 세션 타임아웃 기준(통상 2시간)에 맞추는 것이 좋습니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React와 Vue 스타터 키트는 Inertia의 [서버 사이드 렌더링](https://inertiajs.com/server-side-rendering) 기능을 지원합니다. SSR 호환 번들을 빌드하려면 `build:ssr` 명령어를 실행하세요:

```shell
npm run build:ssr
```

편의상, `composer dev:ssr` 명령어도 사용할 수 있습니다. 이 명령어는 SSR 호환 번들을 빌드한 뒤 Laravel 개발 서버 및 Inertia SSR 서버를 함께 구동하여, SSR 엔진으로 로컬에서 앱을 테스트할 수 있도록 해줍니다:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 키트

Laravel 설치기를 사용해 새 애플리케이션을 만들 때, `--using` 플래그에 Packagist의 커뮤니티 유지 스타터 키트를 지정할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 키트 제작

다른 이용자가 사용할 수 있게 하려면 스타터 키트를 [Packagist](https://packagist.org)에 등록해야 합니다. .env.example 파일에 필요한 환경변수를 정의하고, 설치 후 실행해야 할 명령어는 `composer.json`의 `post-create-project-cmd` 배열에 작성해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문(FAQ)

<a name="faq-upgrade"></a>
#### 스타터 키트는 어떻게 업그레이드하나요?

모든 스타터 키트는 새 프로젝트의 견고한 출발점을 제공합니다. 코드 소유권이 100% 여러분에게 있으므로 마음대로 코드 수정, 커스터마이징, 확장하여 원하는 대로 애플리케이션을 구축하실 수 있습니다. 스타터 키트 자체를 별도로 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증은 어떻게 활성화하나요?

이메일 인증을 사용하려면, `App/Models/User.php` 모델에서 `MustVerifyEmail` 임포트를 주석 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 해야 합니다:

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

등록 완료 후, 사용자는 인증 이메일을 받게 됩니다. 이메일 미인증 시 특정 라우트 접근을 제한하려면, 해당 라우트에 `verified` 미들웨어를 추가하세요:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 버전 스타터 키트 사용 시에는 이메일 인증이 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 수정하려면?

애플리케이션 브랜드에 맞춰 기본 이메일 템플릿을 커스터마이징하고 싶을 수 있습니다. 이를 위해 아래 명령어로 이메일 뷰를 프로젝트로 퍼블리시하세요:

```
php artisan vendor:publish --tag=laravel-mail
```

그러면 `resources/views/vendor/mail` 폴더에 여러 파일이 생성됩니다. 각 파일 및 `resources/views/vendor/mail/themes/default.css`를 수정해 기본 이메일 템플릿의 스타일과 모양을 변경할 수 있습니다.