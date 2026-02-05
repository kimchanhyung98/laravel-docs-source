# 프론트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [시작용 키트](#php-starter-kits)
- [React 또는 Vue 사용하기](#using-react-or-vue)
    - [Inertia](#inertia)
    - [시작용 키트](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [라우팅](/docs/master/routing), [유효성 검증](/docs/master/validation), [캐싱](/docs/master/cache), [큐](/docs/master/queues), [파일 저장소](/docs/master/filesystem) 등, 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 그러나 저희는 개발자에게 강력한 프론트엔드 개발 환경까지 아우르는 아름다운 풀스택 경험을 제공하는 것이 중요하다고 생각합니다.

Laravel로 애플리케이션을 개발할 때 프론트엔드 개발을 수행하는 주요 방식은 두 가지가 있으며, 어떤 접근 방식을 선택할지는 프론트엔드를 PHP로 구축할지, 아니면 Vue, React 같은 JavaScript 프레임워크를 사용할지에 따라 결정됩니다. 아래에서는 이 두 옵션에 대해 자세히 다루어, 여러분의 애플리케이션에 가장 적합한 프론트엔드 개발 방식을 선택하실 수 있도록 안내합니다.

<a name="using-php"></a>
## PHP 사용하기 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade

과거의 대부분 PHP 애플리케이션은, 데이터베이스에서 가져온 데이터를 PHP의 `echo` 구문과 함께 HTML 템플릿에 삽입하여 브라우저로 HTML을 렌더링하였습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서도 [뷰](/docs/master/views)와 [Blade](/docs/master/blade)를 사용해 이런 방식의 HTML 렌더링이 가능합니다. Blade는 데이터를 출력하고, 반복문을 돌리는 등 다양한 작업을 간단한 문법으로 처리할 수 있는 매우 경량화된 템플릿 언어입니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이렇게 애플리케이션을 구축할 경우, 폼 제출이나 기타 페이지 상호작용이 발생하면 서버에서 완전히 새로운 HTML 문서를 받아와서 브라우저가 전체 페이지를 새로 렌더링하게 됩니다. 오늘날에도 많은 애플리케이션에서는 단순한 Blade 템플릿 기반 프론트엔드 구성만으로 충분할 수 있습니다.

<a name="growing-expectations"></a>
#### 높아진 기대치

그러나 사용자들의 웹 애플리케이션에 대한 기대치가 점차 높아지면서, 좀 더 다이내믹하고 세련된 프론트엔드를 원하게 된 개발자들이 많아졌습니다. 그 결과, Vue나 React 같은 JavaScript 프레임워크를 활용하여 프론트엔드를 개발하기 시작한 개발자들도 있습니다.

반면 백엔드 언어에 익숙한 개발자들은, 익숙한 백엔드 언어만을 활용해 현대적인 웹 애플리케이션 UI를 구현할 수 있게 해주는 다양한 솔루션을 개발하기 시작했습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 탄생했습니다.

마찬가지로 Laravel 생태계에서는 PHP를 중심으로 현대적이고 다이내믹한 프론트엔드를 구축하고자 하는 요구로 인해 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 탄생하였습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는, 최신 JavaScript 프레임워크(Vue, React 등)로 만든 것처럼 동적이고 현대적인 프론트엔드를 Laravel로 구축할 수 있도록 해주는 프레임워크입니다.

Livewire를 사용할 때는, UI의 한 부분을 담당하는 Livewire "컴포넌트"를 만들어, 이 컴포넌트에서 데이터를 노출하거나 메서드를 정의하여 프론트엔드에서 상호작용할 수 있습니다. 예를 들어, 간단한 "Counter" 컴포넌트는 다음과 같이 작성할 수 있습니다.

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

이 카운터의 템플릿은 다음과 같이 작성합니다.

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

위 예시에서 볼 수 있듯이, Livewire에서는 `wire:click` 같은 새로운 HTML 속성을 작성하여 Laravel 애플리케이션의 프론트엔드와 백엔드를 연결할 수 있습니다. 또한, 컴포넌트의 현재 상태는 Blade 표현식만으로 간단히 렌더링할 수 있습니다.

많은 개발자들에게 Livewire는 Laravel에서 프론트엔드 개발의 패러다임을 바꿔 주었습니다. Livewire를 이용하면 Laravel의 익숙한 개발 환경 안에서 현대적이고 다이내믹한 웹 애플리케이션을 만들 수 있습니다. Livewire를 사용하는 개발자들은 보통 [Alpine.js](https://alpinejs.dev/)도 함께 사용하여, 모달 다이얼로그 등 특정한 부분에만 필요한 만큼만 JavaScript를 추가로 활용합니다.

Laravel를 처음 접하신다면, [뷰](/docs/master/views) 및 [Blade](/docs/master/blade)의 기본 사용법부터 익히는 것을 추천합니다. 그 후에는 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고하여, 인터랙티브한 Livewire 컴포넌트로 애플리케이션을 한 단계 더 발전시키실 수 있습니다.

<a name="php-starter-kits"></a>
### 시작용 키트 (Starter Kits)

PHP와 Livewire를 이용해 프론트엔드를 구축하고자 한다면, [Livewire 스타터 키트](/docs/master/starter-kits)를 활용하여 애플리케이션 개발을 빠르게 시작할 수 있습니다.

<a name="using-react-or-vue"></a>
## React 또는 Vue 사용하기 (Using React or Vue)

Laravel와 Livewire만으로도 현대적인 프론트엔드를 구축할 수 있지만, 여전히 많은 개발자들은 React나 Vue 같은 JavaScript 프레임워크의 강력함을 활용하고 싶어합니다. 이렇게 하면 NPM을 통해 이용 가능한 방대한 JavaScript 패키지 및 도구 생태계의 이점을 누릴 수 있습니다.

하지만 추가적인 도구 없이 Laravel을 React나 Vue와 결합할 경우, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 등 복잡한 문제들을 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 [Next](https://nextjs.org/)나 [Nuxt](https://nuxt.com/)와 같은 권장 구조가 있는 React/Vue 프레임워크로 간단히 처리할 수 있지만, 데이터 하이드레이션과 인증 문제는 Laravel 같은 백엔드 프레임워크와 프론트엔드 프레임워크를 조합할 때 여전히 복잡하고 번거로운 문제로 남습니다.

또한, 백엔드와 프론트엔드 코드를 각각 다른 저장소(레포지토리)로 관리해야 하므로 유지 보수, 릴리스, 배포까지 여러 저장소 간의 작업을 조정해야 하는 부담이 있습니다. 이런 문제들이 완전히 극복할 수 없는 건 아니지만, 저희는 이런 방식이 생산적이거나 즐거운 개발 경험을 준다고 생각하지 않습니다.

<a name="inertia"></a>
### Inertia

다행히 Laravel은 두 가지 방식의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 여러분의 Laravel 애플리케이션과 최신 React 또는 Vue 프론트엔드 사이를 연결해 주는 다리 역할을 합니다. 이를 통해 단일 코드 저장소(레포지토리)에서 라우팅, 데이터 하이드레이션, 인증은 Laravel의 라우트 및 컨트롤러가 담당하고, 프론트엔드는 React 또는 Vue로 완성도 높게 구현할 수 있습니다. 이 방식을 사용하면 Laravel과 React/Vue의 강점을 모두 온전히 살릴 수 있습니다.

애플리케이션에 Inertia를 설치하면 기존과 똑같이 라우트와 컨트롤러를 작성합니다. 다만, 컨트롤러에서는 Blade 템플릿 대신 Inertia 페이지를 반환합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): Response
    {
        return Inertia::render('users/show', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

Inertia 페이지는 보통 애플리케이션의 `resources/js/pages` 디렉토리에 저장된 React 또는 Vue 컴포넌트와 연결됩니다. `Inertia::render` 메서드로 전달한 데이터는 페이지 컴포넌트의 "props"를 통해 전달되어 화면에서 바로 사용할 수 있습니다.

```jsx
import Layout from '@/layouts/authenticated';
import { Head } from '@inertiajs/react';

export default function Show({ user }) {
    return (
        <Layout>
            <Head title="Welcome" />
            <h1>Welcome</h1>
            <p>Hello {user.name}, welcome to Inertia.</p>
        </Layout>
    )
}
```

이처럼 Inertia를 사용하면, 프론트엔드 개발 시 React나 Vue의 모든 기능을 활용하면서도, 백엔드는 Laravel로 견고하게 구축할 수 있습니다. Inertia는 두 생태계를 매우 가볍고 효율적으로 연결해 주는 역할을 합니다.

#### 서버 사이드 렌더링

만약 Inertia를 도입하고 싶지만, 애플리케이션에 서버 사이드 렌더링(SSR)이 꼭 필요하다면 걱정하지 않으셔도 됩니다. Inertia는 [서버 사이드 렌더링을 지원](https://inertiajs.com/server-side-rendering)합니다. 또한 [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)로 애플리케이션을 배포하는 경우에도, Inertia의 SSR 프로세스를 항상 원활하게 실행할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 시작용 키트 (Starter Kits)

Inertia와 Vue/React로 프론트엔드를 구축하고자 할 경우, [React 또는 Vue 애플리케이션 스타터 키트](/docs/master/starter-kits)를 활용하여 애플리케이션 개발을 빠르게 시작할 수 있습니다. 이 스타터 키트들은 Inertia, Vue/React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 조합하여, 여러분의 애플리케이션에 필요한 백엔드 및 프론트엔드 인증 구조까지 미리 구성해 줍니다. 이제 바로 여러분의 멋진 아이디어를 구현해 보세요.

<a name="bundling-assets"></a>
## 에셋 번들링 (Bundling Assets)

Blade와 Livewire로 프론트엔드를 개발하든, Vue/React와 Inertia로 개발하든, 애플리케이션의 CSS 에셋을 프로덕션용으로 번들링 할 필요가 있습니다. 만약 Vue나 React로 프론트엔드를 만들 경우, 컴포넌트들도 브라우저에서 실행 가능한 JavaScript 에셋으로 번들링해야 합니다.

기본적으로 Laravel은 [Vite](https://vitejs.dev)를 이용해 에셋을 번들링합니다. Vite는 매우 빠른 빌드 속도와, 로컬 개발 환경에서 거의 즉각적인 Hot Module Replacement(HMR) 기능을 제공합니다. 모든 새로운 Laravel 애플리케이션(및 스타터 키트 포함)에는, 가벼운 Laravel Vite 플러그인을 불러오는 `vite.config.js` 파일이 포함되어 있으므로, 손쉽게 Vite를 활용할 수 있습니다.

Laravel과 Vite로 가장 빠르게 개발을 시작하는 방법은, [애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용하여 프로젝트 기반을 만드는 것입니니다. 이 키트는 프론트엔드와 백엔드 인증 구조까지 미리 제공하여 여러분의 개발을 빠르게 시작할 수 있습니다.

> [!NOTE]
> Laravel에서 Vite를 활용하는 보다 자세한 안내는 [에셋 번들링 및 컴파일 전용 문서](/docs/master/vite)를 참고해 주시기 바랍니다.
