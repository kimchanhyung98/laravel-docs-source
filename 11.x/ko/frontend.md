# 프론트엔드

- [소개](#introduction)
- [PHP 활용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 키트](#php-starter-kits)
- [Vue / React 활용하기](#using-vue-react)
    - [Inertia](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개

Laravel은 [라우팅](/docs/{{version}}/routing), [유효성 검사](/docs/{{version}}/validation), [캐싱](/docs/{{version}}/cache), [큐](/docs/{{version}}/queues), [파일 저장소](/docs/{{version}}/filesystem) 등 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 그러나 저희는 개발자에게 프론트엔드 구축을 위한 강력하고 아름다운 풀스택 경험 또한 제공하는 것이 중요하다고 믿습니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드를 구축하는 두 가지 주요 방식이 있으며, 어떤 방법을 선택할지는 PHP를 활용할지, 아니면 Vue 및 React와 같은 자바스크립트 프레임워크를 사용할지에 따라 달라집니다. 아래에서 각각의 옵션을 다루므로, 자신의 애플리케이션 프론트엔드 개발에 적합한 방법을 선택할 수 있습니다.

<a name="using-php"></a>
## PHP 활용하기

<a name="php-and-blade"></a>
### PHP와 Blade

과거에는 대부분의 PHP 애플리케이션이 데이터베이스에서 요청 시 가져온 데이터를 PHP `echo` 문으로 간단히 HTML 템플릿에 삽입하여 HTML을 브라우저에 렌더링했습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 [뷰](/docs/{{version}}/views)와 [Blade](/docs/{{version}}/blade)를 사용하여 여전히 이 방식으로 HTML을 렌더링할 수 있습니다. Blade는 데이터를 출력하고, 데이터를 반복하는 등의 작업을 간편하게 처리할 수 있는 매우 경량의 템플릿 언어입니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이러한 방식으로 애플리케이션을 만들면 폼 제출이나 기타 페이지 상호작용 시 서버에서 아예 새로운 HTML 문서를 받아와 브라우저에서 전체 페이지를 다시 렌더링합니다. 오늘날에도 많은 애플리케이션이 이처럼 단순한 Blade 템플릿을 활용하여 프론트엔드를 구성해도 충분히 적합할 수 있습니다.

<a name="growing-expectations"></a>
#### 높아진 기대치

그러나 웹 애플리케이션에 대한 사용자 기대치가 높아짐에 따라, 더욱 역동적이고 세련된 상호작용이 가능한 프론트엔드를 개발해야 할 필요성을 느끼는 개발자들이 많아졌습니다. 이러한 점을 감안하여, 일부 개발자들은 Vue나 React와 같은 자바스크립트 프레임워크를 이용해 프론트엔드를 구축하기 시작했습니다.

반면, 익숙한 백엔드 언어의 사용을 선호하는 개발자들은 주로 백엔드 언어를 활용하면서도 현대적인 웹 애플리케이션 UI를 개발할 수 있는 솔루션을 개발해 왔습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리가 등장했습니다.

Laravel 생태계에서도 PHP 중심으로 현대적이고 역동적인 프론트엔드를 만들고자 하는 요구에서 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 개발되었습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Vue나 React와 같은 현대적인 자바스크립트 프레임워크로 개발한 프론트엔드처럼 동적이고 살아있는 경험을 제공하는 Laravel 기반 프론트엔드 개발 프레임워크입니다.

Livewire를 사용할 때는 UI의 개별 영역을 렌더링하고, 프론트엔드와 상호작용할 수 있도록 메서드와 데이터를 노출하는 Livewire "컴포넌트"를 만듭니다. 예를 들어, 간단한 "카운터" 컴포넌트는 다음과 같습니다.

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

카운터에 대응하는 템플릿은 다음과 같이 작성할 수 있습니다.

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피 Livewire는 `wire:click`과 같은 새로운 HTML 속성을 작성할 수 있게 해주어, Laravel 애플리케이션의 프론트엔드와 백엔드를 연결합니다. 또한 Blade 표현식을 통해 컴포넌트의 현재 상태를 렌더링할 수 있습니다.

Livewire는 많은 개발자들에게 Laravel 프론트엔드 개발에 혁신을 가져다주었고, 그들은 Laravel의 익숙한 환경을 벗어나지 않고도 현대적이고 동적인 웹 애플리케이션을 구축할 수 있게 되었습니다. Livewire를 사용하는 개발자들은 [Alpine.js](https://alpinejs.dev/)도 함께 활용하여, 대화창 렌더링처럼 프론트엔드에서 정말 필요한 부분에만 자바스크립트를 간결하게 사용할 수 있습니다.

Laravel을 처음 접한다면 [뷰](/docs/{{version}}/views)와 [Blade](/docs/{{version}}/blade)의 기본 사용법을 익히시길 권장합니다. 그런 다음, 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고하여 상호작용이 풍부한 Livewire 컴포넌트로 애플리케이션을 한 단계 발전시켜 보세요.

<a name="php-starter-kits"></a>
### 스타터 키트

PHP와 Livewire를 활용하여 프론트엔드를 구축하고 싶다면 Breeze 또는 Jetstream [스타터 키트](/docs/{{version}}/starter-kits)를 활용하여 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 스타터 키트들은 [Blade](/docs/{{version}}/blade)와 [Tailwind](https://tailwindcss.com)를 이용해 백엔드 및 프론트엔드 인증 흐름을 자동으로 구성해 주어, 여러분이 곧바로 새로운 아이디어에 집중할 수 있도록 도와줍니다.

<a name="using-vue-react"></a>
## Vue / React 활용하기

Laravel과 Livewire로도 현대적인 프론트엔드를 만들 수 있지만, 많은 개발자들은 여전히 Vue나 React와 같은 자바스크립트 프레임워크의 강력함을 활용하길 원합니다. 이를 통해 NPM에서 제공되는 다양한 자바스크립트 패키지와 도구의 풍부한 생태계를 이용할 수 있습니다.

그러나 추가 도구 없이 Laravel과 Vue 또는 React를 결합하면 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 등 복잡한 문제를 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 [Nuxt](https://nuxt.com/)나 [Next](https://nextjs.org/)와 같은 Vue / React 전용 프레임워크로 간소화될 수 있지만, 데이터 하이드레이션과 인증은 백엔드 프레임워크인 Laravel과 프론트엔드 프레임워크를 결합할 때 여전히 까다롭고 번거로운 과제입니다.

또한, 개발자들은 두 개의 별도 코드 저장소를 관리해야 하므로, 관리, 릴리즈, 배포를 양쪽 저장소에서 조율해야 할 수 있습니다. 이러한 문제들이 극복 불가능한 것은 아니지만, 저희는 이것이 생산적이거나 즐거운 개발 방식이라고 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행히도 Laravel은 양쪽의 장점을 동시에 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 현대적인 Vue 또는 React 프론트엔드 사이를 연결해 주며, 라우팅, 데이터 하이드레이션, 인증을 위한 Laravel의 라우트와 컨트롤러를 그대로 활용하면서 Vue / React를 통해 완성도 높은 프론트엔드를 구축할 수 있게 합니다. 이 모든 작업이 하나의 코드 저장소에서 이루어집니다. 이 방식으로 Laravel과 Vue / React 양쪽의 장점을 온전히 누릴 수 있습니다.

Laravel 애플리케이션에 Inertia를 설치한 후에는 기존과 동일하게 라우트와 컨트롤러를 작성합니다. 다만 컨트롤러에서 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환합니다.

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
     * 지정한 사용자의 프로필을 표시합니다.
     */
    public function show(string $id): Response
    {
        return Inertia::render('Users/Profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 일반적으로 애플리케이션의 `resources/js/Pages` 디렉터리에 저장되는 Vue 또는 React 컴포넌트와 대응합니다. `Inertia::render` 메서드를 통해 페이지로 전달한 데이터는 해당 컴포넌트의 "props"로 사용됩니다.

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

보시다시피 Inertia 덕분에 Vue 또는 React의 모든 기능을 활용해 프론트엔드를 개발하면서, Laravel 기반 백엔드와 자바스크립트 기반 프론트엔드를 가볍게 연결할 수 있습니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링이 필요해서 Inertia 도입을 망설이고 있다면 걱정하지 마세요. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또, [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션을 배포할 때 Inertia의 서버 사이드 렌더링 프로세스가 항상 실행되도록 쉽게 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 키트

Inertia와 Vue / React를 활용해 프론트엔드를 구성하고 싶다면 Breeze 또는 Jetstream [스타터 키트](/docs/{{version}}/starter-kits#breeze-and-inertia)를 통해 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 스타터 키트들은 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 이용해 백엔드와 프론트엔드 인증 흐름을 자동으로 구성하므로, 새로운 아이디어 개발에 즉시 착수할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링

Blade와 Livewire, 또는 Vue / React와 Inertia 중 어떤 것으로 프론트엔드를 개발하든, 애플리케이션의 CSS를 배포용 에셋으로 번들링해야 할 필요가 있습니다. 물론, Vue나 React로 프론트엔드를 개발한다면 컴포넌트 또한 브라우저에서 실행 가능한 자바스크립트 에셋으로 번들링해야 합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 이용해 에셋을 번들링합니다. Vite는 매우 빠른 빌드 속도와 거의 즉각적인 Hot Module Replacement(HMR)를 제공합니다. 새롭게 생성된 모든 Laravel 애플리케이션(스타터 키트 포함)에는 Vite 사용을 간편하게 만들어 주는 `vite.config.js` 파일과 Laravel 전용 Vite 플러그인이 포함되어 있습니다.

Laravel과 Vite를 가장 빠르게 시작하는 방법은 [Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) 스타터 키트를 사용해 프로젝트를 시작하는 것입니다. Breeze는 프론트엔드와 백엔드 인증 구성을 제공하여 애플리케이션 개발을 빠르게 시작할 수 있게 도와줍니다.

> [!NOTE]  
> Laravel에서 Vite를 활용하는 방법에 대한 자세한 문서는 [에셋 번들링 및 컴파일 전용 문서](/docs/{{version}}/vite)를 참고하세요.