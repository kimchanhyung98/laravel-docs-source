# 프론트엔드

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 블레이드](#php-and-blade)
    - [라이브와이어](#livewire)
    - [스타터 킷](#php-starter-kits)
- [React 또는 Vue 사용하기](#using-react-or-vue)
    - [이너샤](#inertia)
    - [스타터 킷](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개

라라벨은 [라우팅](/docs/{{version}}/routing), [유효성 검사](/docs/{{version}}/validation), [캐싱](/docs/{{version}}/cache), [큐](/docs/{{version}}/queues), [파일 스토리지](/docs/{{version}}/filesystem)와 같은 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 하지만, 저희는 개발자에게 강력하고 아름다운 풀스택 경험, 즉 프론트엔드 빌드를 위한 모던하고 멋진 솔루션을 제공하는 것이 중요하다고 믿습니다.

라라벨로 애플리케이션을 만들 때 프론트엔드를 개발하는 주요 방식은 두 가지가 있으며, 어떤 방식을 선택할지는 PHP를 활용할지, 아니면 Vue와 React 같은 자바스크립트 프레임워크를 사용할지에 따라 달라집니다. 아래에서 이 두 옵션 모두를 살펴보고, 여러분의 애플리케이션에 가장 적합한 프론트엔드 선택을 하는 데 도움을 드리겠습니다.

<a name="using-php"></a>
## PHP 사용하기

<a name="php-and-blade"></a>
### PHP와 블레이드

과거에는 대부분의 PHP 애플리케이션이 데이터베이스에서 요청한 데이터를 PHP의 `echo` 명령문과 섞인 단순한 HTML 템플릿을 통해 브라우저에 HTML을 렌더링했습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

라라벨에서는 여전히 [뷰](/docs/{{version}}/views)와 [블레이드](/docs/{{version}}/blade)를 사용해 이러한 방식으로 HTML을 렌더링할 수 있습니다. 블레이드는 데이터를 출력하거나 반복하는 등의 기능을 간편하고 간결한 문법으로 제공하는 매우 경량 템플릿 언어입니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이런 방식으로 애플리케이션을 구축할 때, 폼 제출 및 기타 페이지 상호작용은 보통 서버로부터 완전히 새로운 HTML 문서를 받아 브라우저에서 전체 페이지를 다시 렌더링합니다. 오늘날에도 많은 애플리케이션이 단순한 블레이드 템플릿을 사용해 프론트엔드를 구축하는 데 적합할 수 있습니다.

<a name="growing-expectations"></a>
#### 높아지는 기대치

하지만 웹 애플리케이션에 대한 사용자 기대치가 높아지면서, 더 다이나믹하고 정교한 상호작용을 지닌 프론트엔드를 구축할 필요성을 느끼는 개발자가 많아졌습니다. 이에 따라 일부 개발자들은 Vue, React와 같은 자바스크립트 프레임워크를 이용해 프론트엔드를 만들기 시작했습니다.

반면, 익숙한 백엔드 언어를 선호하는 개발자들은 주로 백엔드 언어를 사용하면서도 현대적인 웹 UI를 구축할 수 있는 솔루션을 개발해왔습니다. 예를 들어, [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리가 이런 필요로 인해 탄생했습니다.

라라벨 생태계에서는 PHP만을 주로 활용하여 모던하고 다이나믹한 프론트엔드를 만들 수 있도록 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 등장하게 되었습니다.

<a name="livewire"></a>
### 라이브와이어

[Laravel Livewire](https://livewire.laravel.com)는 Vue와 React 같은 최신 자바스크립트 프레임워크로 구축한 프론트엔드 못지않게, 동적이고 현대적인 라라벨 기반 프론트엔드를 구축할 수 있게 해주는 프레임워크입니다.

라이브와이어를 사용할 때는 UI의 독립적인 일부분을 렌더링하는 "컴포넌트"를 만들고, 메서드와 데이터를 프론트엔드에서 호출하고 상호작용할 수 있도록 노출합니다. 예를 들어, 간단한 "카운터" 컴포넌트는 아래와 같이 작성할 수 있습니다.

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

카운터의 블레이드 템플릿은 다음과 같습니다.

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보다시피, 라이브와이어를 사용하면 `wire:click` 같은 새로운 HTML 속성을 작성해 라라벨 애플리케이션의 프론트엔드와 백엔드를 연결할 수 있습니다. 또한, 단순한 블레이드 표현식으로 컴포넌트의 현재 상태를 렌더링할 수 있습니다.

많은 개발자들에게 라이브와이어는 라라벨을 사용한 프론트엔드 개발의 패러다임을 바꿔주었으며, 라라벨의 익숙함을 유지하면서도 현대적이고 다이나믹한 웹 애플리케이션을 쉽게 구축할 수 있게 해줍니다. 보통 라이브와이어 개발자들은 [Alpine.js](https://alpinejs.dev/)를 활용해, 필요한 곳에만 자바스크립트를 '뿌려' 다이얼로그 창과 같은 UI를 구현하기도 합니다.

라라벨이 처음이라면, 먼저 [뷰](/docs/{{version}}/views)와 [블레이드](/docs/{{version}}/blade)의 기본 사용법에 익숙해지는 것이 좋습니다. 그 후에 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고하여, 인터랙티브한 라이브와이어 컴포넌트로 애플리케이션을 한 단계 업그레이드해 보세요.

<a name="php-starter-kits"></a>
### 스타터 킷

PHP와 라이브와이어를 사용해 프론트엔드를 구축하고 싶다면, [Livewire 스타터 킷](/docs/{{version}}/starter-kits)을 이용해 빠르게 개발을 시작할 수 있습니다.

<a name="using-react-or-vue"></a>
## React 또는 Vue 사용하기

라라벨과 라이브와이어로 현대적인 프론트엔드를 구축할 수 있지만, 여전히 많은 개발자들이 React나 Vue와 같은 자바스크립트 프레임워크의 힘을 활용하길 원합니다. 이를 통해 NPM을 통한 풍부한 자바스크립트 패키지 및 툴에 접근할 수 있습니다.

그러나 별도의 도구 없이 라라벨을 React 또는 Vue와 연동하려면, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증 등 여러 복잡한 과제를 직접 해결해야 합니다. 클라이언트 사이드 라우팅은 종종 [Next](https://nextjs.org/)나 [Nuxt](https://nuxt.com/)와 같은, 방향성이 강한 React/Vue 프레임워크로 쉽게 처리할 수 있지만, 데이터 하이드레이션과 인증은 백엔드 프레임워크인 라라벨과 프론트엔드 프레임워크를 결합할 때 여전히 복잡한 과제입니다.

또한, 개발자들은 별도의 코드 저장소 두 개를 관리해야 하므로, 유지보수, 릴리즈, 배포를 모두 각 저장소에서 조율해야 합니다. 이런 문제들은 극복할 수 있지만, 저희는 그것이 생산적이거나 즐거운 개발 방식이라고 생각하지 않습니다.

<a name="inertia"></a>
### 이너샤

다행히도 라라벨은 양쪽 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 라라벨 애플리케이션과 최신 React 또는 Vue 프론트엔드를 연결해주는 다리 역할을 하여, 라라벨의 라우팅, 데이터 하이드레이션, 인증을 활용하면서도 React 또는 Vue로 완전한 프론트엔드를 구축할 수 있도록 도와줍니다. 이렇게 하면 모든 것이 하나의 코드 저장소에서 관리되어, 라라벨과 React/Vue 모두의 장점을 최대한 살릴 수 있습니다.

라라벨 애플리케이션에 Inertia를 설치하면 기존과 동일하게 라우터 및 컨트롤러를 작성합니다. 차이점은 컨트롤러에서 블레이드 템플릿을 반환하는 대신 Inertia 페이지를 반환한다는 것입니다.

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

Inertia 페이지는 보통 `resources/js/pages` 디렉터리에 저장된 React 또는 Vue 컴포넌트와 일치합니다. `Inertia::render` 메서드를 통해 전달된 데이터는 해당 페이지 컴포넌트의 "props"로 하이드레이션됩니다.

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

이렇게 Inertia를 사용하면 라라벨의 백엔드와 자바스크립트 기반 프론트엔드를 가볍게 연결하면서, React나 Vue의 강력함을 그대로 활용할 수 있습니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링이 필요해 Inertia 도입이 망설여진다면 걱정하지 마세요. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한, [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)를 통해 배포할 때, Inertia의 서버 사이드 렌더링 프로세스를 항상 원활하게 유지할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 킷

Inertia와 Vue / React를 사용해 프론트엔드를 구축하려면, [React 혹은 Vue용 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 활용해 손쉽게 개발을 시작할 수 있습니다. 이 두 스타터 킷 모두 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 사용한 프론트엔드 및 백엔드 인증 플로우를 기본 제공하므로, 여러분의 다음 멋진 프로젝트를 바로 시작할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링

Blade와 라이브와이어를 사용하든, Vue/React와 Inertia를 사용하든, 대부분 애플리케이션의 CSS를 프로덕션에 적합한 에셋으로 번들링해야 할 것입니다. 물론, Vue나 React로 프론트엔드를 작성하는 경우라면 컴포넌트도 브라우저에 적합한 자바스크립트 파일로 번들링해야 합니다.

기본적으로 라라벨은 [Vite](https://vitejs.dev)를 사용하여 에셋 번들링을 처리합니다. Vite는 번개처럼 빠른 빌드 속도와 거의 즉각적인 Hot Module Replacement(HMR)를 로컬 개발 중에 제공합니다. 모든 신규 라라벨 프로젝트 및 [스타터 킷](/docs/{{version}}/starter-kits)에는 `vite.config.js` 파일이 포함되어, 라라벨에 최적화된 가벼운 Vite 플러그인이 자동 로드됩니다.

라라벨과 Vite를 가장 빠르게 시작하는 방법은 [애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)으로 개발을 시작하는 것입니다. 이 스타터 킷은 프론트엔드 및 백엔드 인증 작업을 기본적으로 제공하여 개발을 빠르게 시작할 수 있도록 도와줍니다.

> [!NOTE]
> 라라벨에서 Vite를 사용하는 방법의 상세한 문서는 [에셋 번들링 및 컴파일 전용 문서](/docs/{{version}}/vite)를 참고하세요.