# 프론트엔드

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 키트](#php-starter-kits)
- [Vue / React 사용하기](#using-vue-react)
    - [Inertia](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개

Laravel은 [라우팅](/docs/{{version}}/routing), [유효성 검사](/docs/{{version}}/validation), [캐싱](/docs/{{version}}/cache), [큐](/docs/{{version}}/queues), [파일 저장](/docs/{{version}}/filesystem) 등과 같은 현대적인 웹 애플리케이션 개발에 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 하지만 저희는 강력한 프론트엔드 구축 방식을 포함해 개발자에게 아름다운 풀스택 경험을 제공하는 것이 중요하다고 믿습니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드 개발을 해결하는 주요 방법은 두 가지가 있으며, 어떤 방식을 선택할지는 PHP를 활용할지 아니면 Vue, React와 같은 자바스크립트 프레임워크를 사용할지에 따라 결정됩니다. 아래에서 두 가지 옵션을 모두 설명하여 여러분의 애플리케이션에 가장 적합한 프론트엔드 개발 방식을 선택하는 데 도움이 되고자 합니다.

<a name="using-php"></a>
## PHP 사용하기

<a name="php-and-blade"></a>
### PHP와 Blade

과거 대부분의 PHP 애플리케이션은 단순한 HTML 템플릿 안에 PHP `echo` 문을 섞어 데이터베이스에서 요청 시 가져온 데이터를 출력하며 HTML을 렌더링했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 이러한 방식의 HTML 렌더링을 [뷰](/docs/{{version}}/views)와 [Blade](/docs/{{version}}/blade)를 통해 여전히 구현할 수 있습니다. Blade는 데이터를 표시하거나 반복하는 데 편리하고 간결한 문법을 제공하는 초경량 템플릿 언어입니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이와 같이 애플리케이션을 개발할 경우, 폼 제출이나 페이지 상호작용 시마다 서버에서 완전히 새로운 HTML 문서를 받아 브라우저에서 전체 페이지를 다시 렌더링하게 됩니다. 현재도 많은 애플리케이션이 간단한 Blade 템플릿을 활용해 프론트엔드를 구성하는 형태로 충분히 잘 동작할 수 있습니다.

<a name="growing-expectations"></a>
#### 높아지는 기대치

하지만 웹 애플리케이션에 대한 사용자 기대치가 높아지면서, 더 정교하고 역동적인 프론트엔드와 상호작용에 대한 요구가 커졌습니다. 이에 따라 일부 개발자는 Vue, React 같은 자바스크립트 프레임워크를 활용해 프론트엔드를 개발하기 시작했습니다.

반면 익숙한 백엔드 언어를 계속 사용하고자 하는 개발자들은 주로 백엔드 언어를 이용하면서도 현대적인 웹 UI를 구축할 수 있는 솔루션을 개발했습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 이런 요구가 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리의 탄생을 이끌었습니다.

Laravel 생태계에서는 PHP를 활용해 현대적으로 역동적인 프론트엔드를 구축하려는 요구에서 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 등장했습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Vue나 React와 같은 현대적인 자바스크립트 프레임워크로 구축한 프론트엔드처럼 동적이고 모던한 Laravel 기반 프론트엔드를 손쉽게 만들 수 있는 프레임워크입니다.

Livewire를 사용할 때는 UI의 특정 부분을 렌더링하고 메서드 및 데이터를 프론트엔드에서 호출·상호작용할 수 있도록 하는 Livewire "컴포넌트"를 생성합니다. 예를 들어, 간단한 "카운터" 컴포넌트는 다음과 같습니다:

```php
<?php

namespace App\Http\Livewire;

use Livewire\Component;

class Counter extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }

    public function render()
    {
        return view('livewire.counter');
    }
}
```

그리고 카운터의 대응 템플릿은 다음과 같이 작성할 수 있습니다:

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피, Livewire를 사용하면 `wire:click`과 같이 Laravel 애플리케이션의 프론트엔드와 백엔드를 연결해주는 새로운 HTML 속성을 작성할 수 있습니다. 또한, 컴포넌트의 현재 상태는 간단한 Blade 표현식으로 렌더링할 수 있습니다.

많은 개발자에게 Livewire는 Laravel로의 프론트엔드 개발 경험에 혁신을 가져다주었습니다. 이제 Laravel의 익숙한 환경 안에서 현대적이고 동적인 웹 애플리케이션을 쉽게 구축할 수 있습니다. 보통 Livewire를 사용하는 개발자는 [Alpine.js](https://alpinejs.dev/)를 활용해, 예를 들어 다이얼로그 창을 렌더링하는 등 꼭 필요한 곳에만 "자바스크립트 향신료"를 적용합니다.

Laravel를 처음 접한다면 [뷰](/docs/{{version}}/views) 및 [Blade](/docs/{{version}}/blade) 기본 사용법부터 익히길 권장합니다. 그 후 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고해 인터랙티브한 Livewire 컴포넌트로 애플리케이션을 한 단계 업그레이드할 수 있습니다.

<a name="php-starter-kits"></a>
### 스타터 키트

PHP와 Livewire를 사용해 프론트엔드를 개발하고 싶다면 Breeze 또는 Jetstream [스타터 키트](/docs/{{version}}/starter-kits)를 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 두 스타터 키트 모두 [Blade](/docs/{{version}}/blade)와 [Tailwind](https://tailwindcss.com)를 사용해 애플리케이션의 백엔드·프론트엔드 인증 플로우를 손쉽게 제작해 주기 때문에, 바로 다음 멋진 아이디어 개발에 집중할 수 있습니다.

<a name="using-vue-react"></a>
## Vue / React 사용하기

Laravel과 Livewire만으로 현대적인 프론트엔드를 만드는 것이 가능하지만, 많은 개발자는 여전히 Vue, React 같은 자바스크립트 프레임워크의 강력한 생태계(NPM을 통한 패키지 및 툴 제공)를 활용하길 원합니다.

그러나 추가 도구 없이 Laravel과 Vue 또는 React를 결합하면 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 등 복잡한 문제를 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 [Nuxt](https://nuxt.com/), [Next](https://nextjs.org/)와 같은 주관이 뚜렷한 Vue/React 프레임워크로 쉽게 처리할 수 있지만, 데이터 하이드레이션과 인증은 여전히 벡엔드 프레임워크인 Laravel과 프론트엔드 프레임워크를 결합할 때 해결하기 까다롭습니다.

또한 개발자는 코드 리포지터리를 백엔드와 프론트엔드로 분리해 관리해야 하며, 유지보수나 배포, 릴리즈 작업도 양쪽에서 조율해야 하는 부담이 있습니다. 물론 이 문제들은 극복 가능하지만, 저희는 이것이 생산적이고 즐거운 애플리케이션 개발 방식이라고 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행히, Laravel은 두 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 Vue/React 기반 현대 프론트엔드 사이에 연결고리가 되어, Vue/React로 완전한 현대적 프론트엔드를 구축하면서도, 라우팅·데이터 하이드레이션·인증 등은 Laravel의 라우트 및 컨트롤러를 활용하도록 해 줍니다. 이 모든 것이 하나의 코드 리포지터리에서 이루어집니다. 이 방식은 Laravel과 Vue / React 각각의 강점을 온전히 누리면서도 어느 한 쪽의 역량을 제한하지 않습니다.

애플리케이션에 Inertia를 설치하면 기존과 같이 라우트와 컨트롤러를 작성합니다. 다만 컨트롤러에서 Blade 템플릿을 반환하는 대신, Inertia 페이지를 반환하게 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 표시합니다.
     */
    public function show(string $id): Response
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 Vue 또는 React 컴포넌트로, 보통 애플리케이션의 `resources/js/Pages` 디렉터리에 저장됩니다. `Inertia::render` 메서드를 통해 페이지에 전달된 데이터는 페이지 컴포넌트의 "props"를 하이드레이션하는 데 사용됩니다:

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/vue3';

const props = defineProps(['user']);
</script>

<template>
    <Head title="User Profile" />

    <Layout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Profile
            </h2>
        </template>

        <div class="py-12">
            Hello, {{ user.name }}
        </div>
    </Layout>
</template>
```

보시다시피, Inertia를 활용하면 Laravel 기반 백엔드와 자바스크립트 기반 프론트엔드를 가볍게 연결하면서, Vue나 React의 모든 기능을 활용할 수 있습니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링이 필요하다고 해서 Inertia 사용을 망설일 필요는 없습니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한 [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포할 경우, Inertia의 서버 사이드 렌더링 프로세스가 항상 실행되도록 매우 손쉽게 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 키트

Inertia 및 Vue / React로 프론트엔드를 구축하고자 한다면 Breeze 또는 Jetstream [스타터 키트](/docs/{{version}}/starter-kits#breeze-and-inertia)를 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 두 스타터 키트는 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 활용해 백엔드와 프론트엔드 인증 플로우를 제작해 주므로 바로 다음 멋진 아이디어 개발에 집중할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링

Blade와 Livewire 또는 Vue / React와 Inertia를 사용하든, 대개 애플리케이션의 CSS를 프로덕션용 에셋으로 번들링해야 할 필요가 있습니다. 물론 Vue나 React로 프론트엔드를 개발할 경우 컴포넌트도 브라우저에서 구동 가능한 자바스크립트 에셋으로 번들링해야 합니다.

Laravel은 기본적으로 에셋 번들러로 [Vite](https://vitejs.dev)를 사용합니다. Vite는 놀라운 빌드 속도를 제공하며, 로컬 개발 시 거의 즉각적인 핫 모듈 리플레이스먼트(HMR)를 지원합니다. 모든 신규 Laravel 애플리케이션(스타터 키트 포함)에는 `vite.config.js` 파일이 존재하며, 여기에 경량 Laravel Vite 플러그인이 로드되어 Laravel과 Vite의 조합을 더욱 즐겁게 만들어 줍니다.

Laravel과 Vite로 프로젝트를 시작하는 가장 빠른 방법은 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze)를 이용하는 것입니다. Breeze는 프론트엔드와 백엔드 인증 스캐폴딩을 제공해 개발을 빠르게 시작할 수 있도록 돕는 가장 간단한 스타터 키트입니다.

> [!NOTE]  
> Laravel에서 Vite를 활용하는 방법에 대한 더 자세한 문서는 [에셋 번들링 및 컴파일에 관한 전용 문서](/docs/{{version}}/vite)를 참고해 주세요.