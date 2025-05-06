# 프론트엔드

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP & Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 킷](#php-starter-kits)
- [Vue / React 사용하기](#using-vue-react)
    - [Inertia](#inertia)
    - [스타터 킷](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개

Laravel은 [라우팅](/docs/{{version}}/routing), [유효성 검사](/docs/{{version}}/validation), [캐싱](/docs/{{version}}/cache), [큐](/docs/{{version}}/queues), [파일 저장소](/docs/{{version}}/filesystem) 등과 같은 현대 웹 애플리케이션 개발에 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 우리는 개발자들에게 강력한 프론트엔드 구축 방식을 포함한 아름다운 풀스택 경험을 제공하는 것이 중요하다고 생각합니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드 구축 방법에는 두 가지 주요 방식이 있습니다. 어떤 방식을 선택할지는 PHP를 활용할지, 또는 Vue, React와 같은 JavaScript 프레임워크를 활용할지에 따라 달라집니다. 아래에서 각각의 옵션을 자세히 설명하니, 내 애플리케이션에 가장 적합한 프론트엔드 개발 방법을 결정하는 데 참고하시기 바랍니다.

<a name="using-php"></a>
## PHP 사용하기

<a name="php-and-blade"></a>
### PHP & Blade

과거에는 대부분의 PHP 애플리케이션이 단순한 HTML 템플릿에 PHP의 `echo` 문을 삽입하여, 요청 중 데이터베이스로부터 가져온 데이터를 브라우저에 HTML로 랜더링했습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 [뷰](/docs/{{version}}/views)와 [Blade](/docs/{{version}}/blade)를 사용하여 이러한 방식으로 HTML을 랜더링할 수 있습니다. Blade는 데이터를 표시하거나 데이터를 반복하는 데 편리한, 간단하고 가벼운 템플릿 언어입니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이렇게 애플리케이션을 개발하면, 폼 제출이나 기타 페이지 상호작용 시 서버로부터 전체 HTML 문서를 새로 받아오고 브라우저에서 전체 페이지를 다시 랜더링합니다. 오늘날에도 많은 애플리케이션은 이처럼 간단한 Blade 템플릿만으로 충분히 프론트엔드를 구축할 수 있습니다.

<a name="growing-expectations"></a>
#### 높아진 기대치

하지만 웹 애플리케이션에 대한 사용자들의 기대가 높아지면서, 많은 개발자들은 더욱 다이나믹하고 매끄러운 상호작용이 가능한 프론트엔드를 구축할 필요성을 느끼게 되었습니다. 그래서 일부 개발자들은 Vue나 React 같은 JavaScript 프레임워크를 사용하여 프론트엔드를 개발하기 시작했습니다.

한편, 자신이 익숙한 백엔드 언어를 그대로 사용하고자 하는 개발자들은 주로 백엔드 언어를 활용하면서도 현대적인 웹 UI를 개발할 수 있는 솔루션을 만들기도 했습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 등장했습니다.

Laravel에서는 PHP를 주로 사용하여 현대적이고 동적인 프론트엔드를 구현할 수 있는 [Laravel Livewire](https://laravel-livewire.com)와 [Alpine.js](https://alpinejs.dev/)가 등장했습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://laravel-livewire.com)는 Vue나 React 같은 최신 JavaScript 프레임워크로 만든 프론트엔드 못지않게 다이나믹하고 현대적이며 생동감 넘치는 프론트엔드를 Laravel에서 손쉽게 구축할 수 있게 해주는 프레임워크입니다.

Livewire를 사용할 때는 UI에서 하나의 독립적인 영역을 랜더링하고, 프론트엔드에서 호출 또는 상호작용할 수 있는 메서드와 데이터를 제공하는 Livewire “컴포넌트”를 만듭니다. 예를 들어, 간단한 카운터 컴포넌트는 다음과 같이 구현할 수 있습니다.

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

그리고 카운터의 템플릿은 아래와 같이 작성합니다.

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보다시피 Livewire는 `wire:click`과 같은 새로운 HTML 속성을 통해 Laravel 애플리케이션의 프론트엔드와 백엔드를 연결할 수 있습니다. 또한, 컴포넌트의 현재 상태를 간단한 Blade 표현식으로 랜더링할 수 있습니다.

많은 개발자들에게 Livewire는 Laravel 프론트엔드 개발 방식에 혁신을 가져왔으며, Laravel의 익숙한 환경 안에서 현대적이고 동적인 웹 애플리케이션을 구축할 수 있도록 해줍니다. 대개 Livewire를 사용하는 개발자들은 [Alpine.js](https://alpinejs.dev/)도 함께 활용하여, 예를 들어 대화 상자 같은 요소를 랜더링해야 할 때만 자바스크립트를 필요에 따라 추가합니다.

Laravel를 처음 접한다면, 먼저 [뷰](/docs/{{version}}/views), [Blade](/docs/{{version}}/blade)의 기본 사용법을 익히고 공식 [Laravel Livewire 문서](https://laravel-livewire.com/docs)를 참고하여 Livewire 컴포넌트로 인터랙티브한 애플리케이션을 만드는 방법을 배워 보시기 바랍니다.

<a name="php-starter-kits"></a>
### 스타터 킷

PHP와 Livewire를 사용해 프론트엔드를 구축하고 싶다면, Breeze나 Jetstream [스타터 킷](/docs/{{version}}/starter-kits)을 이용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 두 스타터 킷은 [Blade](/docs/{{version}}/blade)와 [Tailwind](https://tailwindcss.com)를 활용하여 백엔드 및 프론트엔드 인증 흐름을 자동으로 생성해 주므로 곧바로 멋진 프로젝트 아이디어를 실현할 수 있습니다.

<a name="using-vue-react"></a>
## Vue / React 사용하기

Laravel와 Livewire로도 현대적인 프론트엔드를 만들 수 있지만, 여전히 많은 개발자들은 Vue나 React 같은 JavaScript 프레임워크의 강력함을 활용하는 것을 선호합니다. 이를 통해 NPM을 통한 다양한 자바스크립트 패키지와 도구 생태계를 이용할 수 있습니다.

그러나 추가적인 도구 없이 Laravel을 Vue 또는 React와 함께 사용하는 경우, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증과 같은 여러 복잡한 문제를 별도로 해결해야 합니다. 클라이언트 사이드 라우팅은 [Nuxt](https://nuxt.com/)나 [Next](https://nextjs.org/)와 같은 Vue/React 프레임워크를 사용하면 쉽게 해결할 수 있지만, 데이터 하이드레이션과 인증은 여전히 Laravel과 이러한 프론트엔드 프레임워크를 연동할 때 복잡하고 번거로운 과제입니다.

또한 관리해야 할 코드 저장소가 백엔드와 프론트엔드로 분리되기 때문에, 유지보수와 배포, 릴리즈 일정을 맞추는 데 추가적인 부담이 생깁니다. 이러한 문제는 극복 불가능하지 않지만, 생산적이거나 즐거운 애플리케이션 개발 방식이라고는 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행스럽게도, Laravel은 두 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 Vue 또는 React 기반 최신 프론트엔드 사이의 간극을 메워줍니다. 이를 통해 단일 코드 저장소 내에서 라우팅, 데이터 하이드레이션, 인증은 Laravel의 라우트와 컨트롤러를 이용하면서 프런트엔드는 Vue나 React로 완성도 높게 개발할 수 있습니다. 따라서 Laravel과 Vue/React의 모든 강점을 제한 없이 활용할 수 있습니다.

Inertia를 Laravel 애플리케이션에 설치한 후에는 기존과 동일하게 라우트와 컨트롤러를 작성하면 됩니다. 단, 컨트롤러에서 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Inertia\Inertia;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     *
     * @param  int  $id
     * @return \Inertia\Response
     */
    public function show($id)
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 Vue나 React 컴포넌트에 해당하며, 보통 애플리케이션의 `resources/js/Pages` 디렉토리에 저장됩니다. `Inertia::render` 메서드로 전달한 데이터는 해당 페이지 컴포넌트의 "props"로 하이드레이션됩니다.

```vue
<script setup>
import Layout from '@/Layouts/Authenticated.vue';
import { Head } from '@inertiajs/inertia-vue3';

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

이처럼 Inertia를 사용하면 Laravel 기반 백엔드와 JavaScript 기반 프론트엔드 사이를 가볍게 연결하면서 Vue나 React의 모든 기능을 자유롭게 활용할 수 있습니다.

#### 서버 사이드 렌더링

애플리케이션에서 서버 사이드 렌더링이 필요해서 Inertia 도입을 망설이고 있다면, 걱정하지 않으셔도 됩니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한 [Laravel Forge](https://forge.laravel.com)로 배포할 때도 Inertia의 서버 사이드 렌더링 프로세스를 항상 실행 상태로 손쉽게 관리할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 킷

Inertia와 Vue/React를 이용해 프론트엔드를 구축하고 싶다면 Breeze 또는 Jetstream [스타터 킷](/docs/{{version}}/starter-kits#breeze-and-inertia)을 사용해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 스타터 킷들은 Inertia, Vue/React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 활용해 백엔드와 프론트엔드 인증 흐름을 자동으로 구성해 주므로 곧장 멋진 아이디어를 실현할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링

Blade와 Livewire, 혹은 Vue/React와 Inertia 중 어떤 방식으로 프론트엔드를 개발하더라도, 애플리케이션의 CSS 파일을 프로덕션용 에셋으로 번들링해야 할 필요가 있습니다. 특히 Vue나 React로 프론트엔드를 개발한다면 컴포넌트 역시 브라우저에서 사용할 수 있도록 JavaScript 에셋으로 번들링해야 합니다.

기본적으로, Laravel은 [Vite](https://vitejs.dev)를 이용해 에셋을 번들링합니다. Vite는 매우 빠른 빌드 속도와 거의 즉각적인 핫 모듈 교체(HMR)를 제공합니다. 모든 신규 Laravel 애플리케이션(스타터 킷 활용 포함)에는 Vite를 Laravel과 쉽게 연동할 수 있도록 경량의 Laravel Vite 플러그인을 로드하는 `vite.config.js` 파일이 포함되어 있습니다.

Laravel과 Vite를 가장 빠르게 시작하는 방법은 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze)를 사용하는 것입니다. Breeze는 프론트엔드와 백엔드 인증 스캐폴딩을 제공해 애플리케이션 개발을 신속하게 시작할 수 있도록 도와줍니다.

> **참고**  
> Laravel에서 Vite를 활용한 에셋 번들링 및 컴파일에 대한 더 자세한 내용은 [자세한 Vite 문서](/docs/{{version}}/vite)를 참고하세요.