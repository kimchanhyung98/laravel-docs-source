# 스타터 킷 (Starter Kits)

- [소개](#introduction)
- [스타터 킷을 사용하여 애플리케이션 생성하기](#creating-an-application)
- [사용 가능한 스타터 킷](#available-starter-kits)
    - [React](#react)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [스타터 킷 커스터마이징](#starter-kit-customization)
    - [React](#react-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [WorkOS AuthKit 인증](#workos)
- [Inertia SSR](#inertia-ssr)
- [커뮤니티 유지 스타터 킷](#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개

새로운 라라벨 애플리케이션 개발을 빠르게 시작할 수 있도록, [애플리케이션 스타터 킷](https://laravel.com/starter-kits)을 제공합니다. 이 스타터 킷은 라라벨 애플리케이션을 만드는 데 필요한 라우트, 컨트롤러, 뷰를 미리 제공하여, 회원가입 및 사용자 인증 등 필수 기능을 바로 사용할 수 있도록 도와줍니다.

이 스타터 킷을 사용하는 것은 선택 사항입니다. 원한다면 라라벨을 처음부터 설치하여 직접 애플리케이션을 구축할 수도 있습니다. 어떤 방식을 택하든, 멋진 결과물을 만들어낼 수 있을 것입니다!

<a name="creating-an-application"></a>
## 스타터 킷을 사용하여 애플리케이션 생성하기

스타터 킷을 사용하여 새로운 라라벨 애플리케이션을 생성하려면, 먼저 [PHP와 라라벨 CLI 도구](/docs/12.x/installation#installing-php)를 설치해야 합니다. 이미 PHP와 Composer가 설치되어 있다면, Composer 명령어로 라라벨 설치 도구(Laravel installer)를 추가할 수 있습니다.

```shell
composer global require laravel/installer
```

이제 라라벨 설치 CLI를 이용해 새로운 애플리케이션을 만들 수 있습니다. 설치 도구를 실행하면 원하는 스타터 킷을 선택할 수 있습니다.

```shell
laravel new my-app
```

라라벨 애플리케이션이 만들어지면, NPM을 이용해 프론트엔드 의존성 패키지를 설치하고 라라벨 개발 서버를 시작하면 됩니다.

```shell
cd my-app
npm install && npm run build
composer run dev
```

라라벨 개발 서버를 실행하면, 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 주소로 애플리케이션에 접속할 수 있습니다.

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 킷

<a name="react"></a>
### React

React 스타터 킷은 [Inertia](https://inertiajs.com)를 기반으로, React 프론트엔드와 함께라라벨 애플리케이션을 만들 수 있는 견고하고 현대적인 출발점을 제공합니다.

Inertia를 사용하면 서버사이드 라우팅과 컨트롤러를 그대로 유지하면서, 최신 싱글페이지 React 애플리케이션을 만들 수 있습니다. 이를 통해 React의 강력한 프론트엔드 능력과 라라벨의 생산성, 그리고 Vite의 빠른 컴파일 속도를 동시에 누릴 수 있습니다.

React 스타터 킷은 React 19, TypeScript, Tailwind, 그리고 [shadcn/ui](https://ui.shadcn.com) 컴포넌트 라이브러리를 활용합니다.

<a name="vue"></a>
### Vue

Vue 스타터 킷은 [Inertia](https://inertiajs.com)를 기반으로, Vue 프론트엔드와 함께 라라벨 애플리케이션을 개발하기 위한 훌륭한 출발점을 제공합니다.

Inertia를 통해 서버사이드 라우팅과 컨트롤러를 그대로 이용하면서, 최신 싱글페이지 Vue 애플리케이션을 구축할 수 있습니다. 그러면 Vue의 프론트엔드 기능과 라라벨의 뛰어난 백엔드 생산성, 그리고 Vite의 빠른 컴파일 속도를 모두 활용할 수 있습니다.

Vue 스타터 킷은 Vue Composition API, TypeScript, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/) 컴포넌트 라이브러리를 사용합니다.

<a name="livewire"></a>
### Livewire

Livewire 스타터 킷은 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 기반으로, 라라벨 애플리케이션 개발을 위한 최적의 출발점입니다.

Livewire는 PHP만으로 동적이고 반응성 높은 프론트엔드 UI를 만들 수 있게 해주는 강력한 도구입니다. 주로 Blade 템플릿을 사용하는 팀이나, React, Vue와 같은 JavaScript 기반 SPA 프레임워크보다 더 단순한 방법을 찾는 팀에게 잘 어울립니다.

Livewire 스타터 킷은 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 활용합니다.

<a name="starter-kit-customization"></a>
## 스타터 킷 커스터마이징

<a name="react-customization"></a>
### React

React 스타터 킷은 Inertia 2, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)를 사용하여 구현되었습니다. 모든 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드 전체가 여러분 애플리케이션 내부에 있으며, 원하는 대로 자유롭게 커스터마이즈할 수 있습니다.

프론트엔드 코드는 대부분 `resources/js` 디렉터리에 있습니다. 애플리케이션의 외관과 동작을 원하는 대로 수정할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 React 컴포넌트
├── hooks/         # React 훅(hook)
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

추가적인 shadcn 컴포넌트를 사용하고 싶다면, [원하는 컴포넌트를 찾아](https://ui.shadcn.com) 아래와 같이 `npx` 명령어로 추가하면 됩니다.

```shell
npx shadcn@latest add switch
```

예를 들어 위 명령어는 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx` 경로에 생성합니다. 컴포넌트가 생성되면, 아래와 같이 원하는 모든 페이지에서 사용할 수 있습니다.

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

React 스타터 킷은 "sidebar(사이드바)" 레이아웃과 "header(헤더)" 레이아웃, 두 가지 기본 레이아웃을 제공합니다. 기본값은 사이드바 레이아웃이며, 헤더 레이아웃으로 변경하고 싶다면, `resources/js/layouts/app-layout.tsx` 파일 상단의 import 부분을 수정하면 됩니다.

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### 사이드바 변형(Variant)

사이드바 레이아웃은 기본 사이드바, "inset(인셋)", "floating(플로팅)" 세 가지 변형이 있습니다. 원하는 스타일로 적용하려면 `resources/js/components/app-sidebar.tsx` 컴포넌트의 코드를 아래와 같이 수정하세요.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 킷에 포함된 로그인 및 회원가입 페이지 등의 인증 관련 뷰에는 "simple(심플)", "card(카드)", "split(분할)" 세 가지 레이아웃 변형이 지원됩니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/auth-layout.tsx` 파일 상단의 import 부분을 아래와 같이 수정하세요.

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Vue 스타터 킷은 Inertia 2, Vue 3 Composition API, Tailwind, [shadcn-vue](https://www.shadcn-vue.com/)와 함께 제공됩니다. 모든 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드 전체가 여러분 애플리케이션 내부에 있으므로, 완전히 자유롭게 커스터마이즈할 수 있습니다.

프론트엔드 코드는 대부분 `resources/js` 디렉터리에 있습니다. 애플리케이션의 외관과 동작을 원하는 대로 수정할 수 있습니다.

```text
resources/js/
├── components/    # 재사용 가능한 Vue 컴포넌트
├── composables/   # Vue composable/hook
├── layouts/       # 애플리케이션 레이아웃
├── lib/           # 유틸리티 함수 및 설정
├── pages/         # 페이지 컴포넌트
└── types/         # TypeScript 타입 정의
```

추가적인 shadcn-vue 컴포넌트를 사용하려면, [원하는 컴포넌트를 찾아](https://www.shadcn-vue.com) 아래와 같이 `npx` 명령어로 추가하면 됩니다.

```shell
npx shadcn-vue@latest add switch
```

예를 들어 위 명령어는 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue` 경로에 생성합니다. 이렇게 생성된 컴포넌트는 원하는 Vue 페이지에서 자유롭게 사용할 수 있습니다.

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

Vue 스타터 킷 역시 "sidebar(사이드바)"와 "header(헤더)" 두 가지 기본 레이아웃 중 선택할 수 있습니다. 기본값은 사이드바 레이아웃이며, 헤더 레이아웃으로 변경하려면 `resources/js/layouts/AppLayout.vue` 파일 상단의 import 부분을 수정하면 됩니다.

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### 사이드바 변형(Variant)

사이드바 레이아웃은 기본 스타일, "inset(인셋)", "floating(플로팅)" 세 가지 변형이 있습니다. 원하는 스타일로 적용하려면 `resources/js/components/AppSidebar.vue` 컴포넌트의 코드를 아래와 같이 수정하세요.

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 킷에 포함된 로그인 및 회원가입 페이지와 같은 인증 관련 뷰에도 "simple(심플)", "card(카드)", "split(분할)" 세 가지 레이아웃 변형이 있습니다.

인증 레이아웃을 변경하려면, `resources/js/layouts/AuthLayout.vue` 파일 상단의 import 부분을 아래와 같이 수정하세요.

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Livewire 스타터 킷은 Livewire 3, Tailwind, [Flux UI](https://fluxui.dev/)를 활용해 만들어집니다. 다른 스타터 킷과 마찬가지로, 백엔드와 프론트엔드 코드 전체가 프로젝트 내에 있어 여러분만의 맞춤 애플리케이션 제작이 가능합니다.

#### Livewire와 Volt

프론트엔드 코드는 대부분 `resources/views` 디렉터리에 위치합니다. 이 영역의 코드를 자유롭게 수정하여 애플리케이션의 외관과 동작을 맞춤화할 수 있습니다.

```text
resources/views
├── components            # 재사용 가능한 Livewire 컴포넌트
├── flux                  # 커스터마이즈된 Flux 컴포넌트
├── livewire              # Livewire 페이지
├── partials              # 재사용 가능한 Blade partial
├── dashboard.blade.php   # 인증 사용자 대시보드
├── welcome.blade.php     # 비인증(게스트) 사용자의 환영 페이지
```

#### 기존 방식의 Livewire 컴포넌트

프론트엔드 코드는 `resources/views` 디렉터리에 있고, 각 Livewire 컴포넌트의 백엔드 로직은 `app/Livewire` 디렉터리에 위치합니다.

<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 스타터 킷 역시 "sidebar(사이드바)"와 "header(헤더)" 두 가지 기본 레이아웃 중에 선택할 수 있습니다. 기본값은 사이드바 레이아웃이며, 헤더 레이아웃을 사용하고 싶다면, `resources/views/components/layouts/app.blade.php` 파일에서 레이아웃을 아래와 같이 변경하고, 메인 Flux 컴포넌트에 `container` 속성을 추가해야 합니다.

```blade
<x-layouts.app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts.app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Livewire 스타터 킷의 로그인, 회원가입 등 인증 페이지들 역시 "simple(심플)", "card(카드)", "split(분할)" 세 가지 레이아웃 변형이 있습니다.

인증 레이아웃을 변경하려면, `resources/views/components/layouts/auth.blade.php` 파일에서 아래와 같이 레이아웃을 수정하면 됩니다.

```blade
<x-layouts.auth.split>
    {{ $slot }}
</x-layouts.auth.split>
```

<a name="workos"></a>
## WorkOS AuthKit 인증

기본적으로 React, Vue, Livewire 스타터 킷은 모두 라라벨 내장 인증 시스템을 사용해서 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 또한 별도로, 각 스타터 킷별로 [WorkOS AuthKit](https://authkit.com)을 활용한 버전도 지원합니다. 이 버전은 아래와 같은 기능을 제공합니다.

<div class="content-list" markdown="1">

- 소셜 인증(Google, Microsoft, GitHub, Apple)
- 패스키 인증(Passkey)
- 이메일 기반 "매직 인증(Magic Auth)"
- SSO(싱글사인온)

</div>

WorkOS를 인증 제공자로 사용하려면 [WorkOS 계정이 필요합니다](https://workos.com). WorkOS는 월간 활성 사용자 100만 명까지 무료로 인증 서비스를 제공합니다.

WorkOS AuthKit을 인증 방식으로 사용하려면, `laravel new`로 새 스타터 킷 기반 애플리케이션 생성 시 WorkOS 옵션을 선택하면 됩니다.

### WorkOS 스타터 킷 설정하기

WorkOS 기반 스타터 킷으로 새 애플리케이션을 생성한 뒤, `.env` 파일에서 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 값들은 WorkOS 대시보드에서 애플리케이션별로 제공받아 입력합니다.

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

또한 WorkOS 대시보드에서 애플리케이션의 홈페이지 URL도 설정하세요. 이 주소로 사용자는 로그아웃 후 리다이렉트됩니다.

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 인증 방법 설정

WorkOS 기반 스타터 킷을 사용할 때는, WorkOS AuthKit 설정에서 "이메일+비밀번호" 인증을 비활성화하고, 소셜 인증 및 패스키, "매직 인증", SSO 만 활성화하는 것을 권장합니다. 이렇게 하면 사용자의 비밀번호를 직접 관리하지 않아도 됩니다.

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit 세션 만료 시간 설정

또한 라라벨 애플리케이션에 설정된 세션 만료 시간(일반적으로 2시간)에 맞춰, WorkOS AuthKit 측의 세션 비활성화(timeout) 설정도 동일하게 맞추는 것을 추천합니다.

<a name="inertia-ssr"></a>
### Inertia SSR

React와 Vue 스타터 킷은 Inertia의 [서버사이드 렌더링(SSR)](https://inertiajs.com/server-side-rendering) 기능을 지원합니다. SSR에 필요한 번들을 빌드하려면 아래 명령어를 실행하세요.

```shell
npm run build:ssr
```

편의를 위해 `composer dev:ssr` 명령어도 제공됩니다. 이 명령은 SSR 호환 번들을 빌드한 뒤, 라라벨 개발 서버와 Inertia SSR 서버를 실행하여, 로컬 환경에서 Inertia의 서버사이드 렌더링 기능을 직접 테스트할 수 있게 해줍니다.

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 스타터 킷

라라벨 설치 도구로 새 애플리케이션을 생성할 때, Packagist에 등록된 커뮤니티 유지 스타터 킷을 `--using` 옵션으로 지정하여 사용할 수 있습니다.

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### 스타터 킷 제작 및 등록

여러분이 만든 스타터 킷을 다른 개발자들도 사용할 수 있도록 하려면, [Packagist](https://packagist.org)에 배포해야 합니다. 스타터 킷은 요구하는 환경 변수 목록을 `.env.example` 파일에 정의하고, 별도의 post-install 명령어가 필요하다면 `composer.json` 파일의 `post-create-project-cmd` 배열에 나열해야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드하나요?

각 스타터 킷은 새로운 애플리케이션 개발에 있어 견고한 출발점을 제공합니다. 소스 코드를 모두 직접 소유하게 되므로, 원하는 대로 수정, 확장, 커스터마이즈하여 완전히 자신만의 애플리케이션을 만들 수 있습니다. 별도로 스타터 킷 자체를 이후에 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증 기능은 어떻게 활성화하나요?

이메일 인증은 `App/Models/User.php` 모델에서 `MustVerifyEmail` import 부분의 주석을 해제하고, 해당 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 하면 됩니다.

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

회원가입이 완료되면, 사용자에게 인증 이메일이 자동으로 발송됩니다. 사용자의 이메일 인증 전까지 접근을 제한하고 싶은 라우트에는 `verified` 미들웨어를 추가하세요.

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> [WorkOS](#workos) 버전 스타터 킷을 사용하는 경우에는 이메일 인증이 필수가 아닙니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

기본 제공 이메일 템플릿의 디자인을 애플리케이션의 브랜드 스타일에 맞게 수정하고 싶다면, 다음 명령어로 이메일 뷰 파일을 애플리케이션에 퍼블리시할 수 있습니다.

```
php artisan vendor:publish --tag=laravel-mail
```

이렇게 하면 `resources/views/vendor/mail` 경로에 여러 파일이 생성됩니다. 각 파일과, 기본 이메일 템플릿의 스타일을 변경하려면 `resources/views/vendor/mail/themes/default.css` 파일을 수정하면 됩니다.
