# 프런트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 키트](#php-starter-kits)
- [React 또는 Vue 사용하기](#using-react-or-vue)
    - [Inertia](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [자산 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [라우팅](/docs/12.x/routing), [유효성 검증](/docs/12.x/validation), [캐싱](/docs/12.x/cache), [큐](/docs/12.x/queues), [파일 저장소](/docs/12.x/filesystem) 등 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 하지만 개발자에게 강력한 프런트엔드 구축 방법까지 포함한 아름다운 풀스택 경험을 제공하는 것도 중요하다고 믿습니다.

Laravel로 애플리케이션을 만들 때 프런트엔드를 다루는 주요 방법은 두 가지가 있습니다. 하나는 PHP를 활용해 프런트엔드를 구축하는 방법이고, 다른 하나는 Vue나 React 같은 자바스크립트 프레임워크를 사용하는 방법입니다. 아래에서 두 가지 옵션에 대해 모두 설명하므로, 여러분의 애플리케이션에 가장 적합한 프런트엔드 개발 방식을 선택하는 데 도움이 될 것입니다.

<a name="using-php"></a>
## PHP 사용하기 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade (PHP and Blade)

과거 대부분의 PHP 애플리케이션은 단순한 HTML 템플릿 안에 PHP `echo` 구문을 섞어 데이터베이스에서 가져온 데이터를 렌더링하는 방식으로 HTML을 브라우저에 출력했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 이 HTML 렌더링 방식을 [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)를 이용해 여전히 구현할 수 있습니다. Blade는 매우 가벼운 템플릿 언어로, 데이터를 출력하거나, 반복문을 작성하는 등 간결하고 편리한 문법을 제공합니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이 방식으로 애플리케이션을 만들 때는 폼 제출이나 다른 페이지 상호작용이 서버에서 완전히 새로운 HTML 문서를 받아오고, 브라우저가 페이지 전체를 다시 렌더링하는 방식입니다. 오늘날에도 많은 애플리케이션들은 단순한 Blade 템플릿을 사용해 프런트엔드를 이처럼 구성하는 데 매우 적합할 수 있습니다.

<a name="growing-expectations"></a>
#### 커져가는 기대 (Growing Expectations)

하지만 웹 애플리케이션에 대한 사용자 기대가 발전함에 따라, 더 세련된 상호작용과 역동적인 프런트엔드를 필요로 하는 개발자들이 늘고 있습니다. 이에 따라 일부 개발자들은 Vue나 React 같은 자바스크립트 프레임워크로 프런트엔드를 구축하는 방식을 선택합니다.

반면에 익숙한 백엔드 언어를 계속 사용하고 싶어 하는 개발자들은 주로 자신이 선호하는 백엔드 언어를 이용하면서도 현대적인 웹 UI를 구축할 수 있는 해결책들을 만들어냈습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 등장했습니다.

Laravel 생태계 내에서는 PHP를 중심으로 현대적이고 동적인 프런트엔드를 만들 필요성에서 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 등장하게 되었습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Vue나 React 등 최신 자바스크립트 프레임워크로 만든 프런트엔드처럼 동적이고 현대적인 UI를 Laravel로 쉽게 구축할 수 있게 해 주는 프레임워크입니다.

Livewire를 사용할 때는 UI의 일부를 담당하는 Livewire "컴포넌트"를 만들고, 이 컴포넌트에 메서드와 데이터를 노출시켜서 애플리케이션 프런트엔드에서 호출하고 상호작용할 수 있습니다. 간단한 "Counter" 컴포넌트 예시는 다음과 같습니다:

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

그리고 이에 대응하는 템플릿은 다음과 같이 작성합니다:

```blade
<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>
```

보시다시피 Livewire는 `wire:click` 같은 새로운 HTML 속성들을 통해 Laravel 애플리케이션의 프런트엔드와 백엔드를 연결합니다. 또한, 컴포넌트의 현재 상태를 Blade 표현식을 사용해 쉽게 렌더링할 수 있습니다.

많은 사용자에게 Livewire는 Laravel 내에서 편안하게 최신 동적 웹 애플리케이션을 구축할 수 있게 해주며 프런트엔드 개발 방식에 혁신을 가져왔습니다. 보통 Livewire를 사용할 때는 [Alpine.js](https://alpinejs.dev/)를 함께 사용하여, 다이얼로그 창 같이 일부 인터랙션에만 자바스크립트를 아주 가볍게 추가하는 방식을 추천합니다.

Laravel 초보자라면 우선 [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)의 기본 사용법에 익숙해진 후, 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고하여 인터랙티브한 Livewire 컴포넌트로 애플리케이션을 한 단계 더 발전시키세요.

<a name="php-starter-kits"></a>
### 스타터 키트 (Starter Kits)

PHP와 Livewire를 사용해 프런트엔드를 구축하고 싶다면, [Livewire 스타터 키트](/docs/12.x/starter-kits)를 활용해 애플리케이션 개발을 빠르게 시작할 수 있습니다.

<a name="using-react-or-vue"></a>
## React 또는 Vue 사용하기 (Using React or Vue)

Laravel과 Livewire로 현대적인 프런트엔드를 구축할 수 있지만, 여전히 많은 개발자가 React 또는 Vue 같은 자바스크립트 프레임워크의 강력한 생태계를 활용하기를 선호합니다. 이를 통해 NPM에서 제공하는 풍부한 자바스크립트 패키지와 도구를 활용할 수 있습니다.

그러나 별도의 도구 없이 Laravel과 React 혹은 Vue를 함께 사용할 경우, 클라이언트 측 라우팅, 데이터 하이드레이션, 인증과 같은 복잡한 문제들을 직접 해결해야 합니다. 클라이언트 측 라우팅은 [Next](https://nextjs.org/)나 [Nuxt](https://nuxt.com/) 같은 미리 설계된 React / Vue 프레임워크를 사용하면 어느 정도 간소화되지만, 데이터 하이드레이션과 인증 문제는 Laravel과 해당 프런트엔드 프레임워크를 함께 사용할 때 여전히 어렵고 번거로운 과제입니다.

또한, 개발자는 백엔드와 프런트엔드를 각각 별도의 코드 저장소로 관리해야 하며, 이 두 저장소를 함께 유지, 배포하는 데에도 많은 조율이 필요합니다. 이런 문제들이 넘을 수 없는 장벽은 아니지만, 생산적이거나 즐겁게 애플리케이션을 개발하는 방법이라고 생각하지는 않습니다.

<a name="inertia"></a>
### Inertia

다행히도 Laravel은 두 세계의 장점을 모두 제공합니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 React 또는 Vue 프런트엔드 간 다리를 놓아, React 또는 Vue를 사용해 완전하고 현대적인 프런트엔드를 구축하면서도 Laravel의 라우트와 컨트롤러를 활용해 라우팅, 데이터 하이드레이션, 인증을 한 코드 저장소 안에서 통합적으로 처리하게 해줍니다. 이 접근법으로 Laravel과 React / Vue 두 도구의 강점을 모두 손상 없이 누릴 수 있습니다.

Laravel 애플리케이션에 Inertia를 설치하면, 라우트와 컨트롤러는 평소처럼 작성합니다. 다만 컨트롤러에서 Blade 뷰를 반환하는 대신, Inertia 페이지를 반환합니다:

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

Inertia 페이지는 React 또는 Vue 컴포넌트에 해당하며, 보통 애플리케이션의 `resources/js/pages` 디렉토리에 저장합니다. `Inertia::render` 메서드를 통해 페이지에 전달된 데이터는 페이지 컴포넌트의 "props"를 하이드레이션하는 데 사용됩니다:

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

보시는 것처럼 Inertia는 React 또는 Vue의 강력함을 최대한 활용하면서 Laravel 기반 백엔드와 자바스크립트 기반 프런트엔드 사이의 가벼운 다리 역할을 해줍니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링이 필요해서 Inertia 사용이 걱정된다면 안심하세요. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한 [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)를 통해 애플리케이션 배포 시 Inertia의 서버 사이드 렌더링 프로세스가 항상 실행되도록 손쉽게 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 키트 (Starter Kits)

Inertia와 Vue / React를 사용해 프런트엔드를 만들고 싶다면, [React 또는 Vue 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 활용해 개발을 빠르게 시작할 수 있습니다. 이 스타터 키트는 Inertia, Vue / React, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 사용해 애플리케이션의 백엔드와 프런트엔드 인증 흐름을 뼈대부터 구성해 줍니다. 덕분에 새로운 아이디어 구현에 바로 몰입할 수 있습니다.

<a name="bundling-assets"></a>
## 자산 번들링 (Bundling Assets)

Blade 및 Livewire를 사용하든, Vue / React와 Inertia를 사용하든, 애플리케이션의 CSS를 프로덕션용 자산으로 번들링해야 할 필요가 있을 것입니다. 물론 Vue 또는 React로 프런트엔드를 만들면, 컴포넌트를 브라우저에서 실행 가능한 자바스크립트 파일로 묶는 작업도 필요합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 자산 번들러로 사용합니다. Vite는 번개처럼 빠른 빌드 속도와 로컬 개발 시 거의 즉각적인 핫 모듈 교체(HMR)를 제공합니다. 새 Laravel 애플리케이션 모두, 그리고 [스타터 키트](/docs/12.x/starter-kits)를 사용하는 애플리케이션에도 `vite.config.js` 파일이 포함되어 있으며, 여기에는 Laravel Vite 플러그인을 로드해 Laravel과 Vite를 쾌적하게 사용할 수 있도록 합니다.

Laravel과 Vite로 빠르게 시작하는 가장 좋은 방법은 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 이용하는 것입니다. 이 스타터 키트는 프런트엔드와 백엔드 인증 스캐폴딩을 제공해 개발 초기 진입 장벽을 크게 낮춰줍니다.

> [!NOTE]
> Laravel에서 Vite를 활용하는 상세한 문서는 [자산 번들링 및 컴파일 관련 문서](/docs/12.x/vite)를 참고하세요.