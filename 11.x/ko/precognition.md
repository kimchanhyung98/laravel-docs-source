# Precognition

- [소개](#introduction)
- [라이브 유효성 검사](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [유효성 검사 규칙 사용자 정의하기](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리하기](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 미래의 HTTP 요청 결과를 미리 예측할 수 있게 해줍니다. Precognition의 주된 사용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드의 유효성 검사 규칙을 중복 작성하지 않고 "라이브" 유효성 검사를 제공하는 기능입니다. Precognition은 특히 Laravel의 Inertia 기반 [스타터 킷들](/docs/11.x/starter-kits)과 잘 어울립니다.

Laravel이 "Precognitive 요청"을 받으면, 해당 라우트의 미들웨어를 모두 실행하고 라우트의 컨트롤러 의존성을 해결합니다. 여기에는 [폼 요청 유효성 검사](/docs/11.x/validation#form-request-validation)도 포함되지만, 라우트 컨트롤러 메서드는 실제로 실행하지 않습니다.

<a name="live-validation"></a>
## 라이브 유효성 검사 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기 (Using Vue)

Laravel Precognition을 사용하면 프론트엔드 Vue 애플리케이션에 유효성 검사 규칙을 중복 구현할 필요 없이 라이브 유효성 검사 경험을 제공할 수 있습니다. 이를 설명하기 위해, 새로운 사용자를 생성하는 폼을 만들어 보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 그리고 라우트의 유효성 검사 규칙을 담는 [폼 요청](/docs/11.x/validation#form-request-validation)을 만들어야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, Vue용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치하세요:

```shell
npm install laravel-precognition-vue
```

Laravel Precognition 패키지가 설치되면 `useForm` 함수를 사용해 폼 객체를 생성하세요. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 인수로 전달합니다.

라이브 유효성 검사를 활성화하려면 각 입력 요소의 `change` 이벤트에서 폼의 `validate` 메서드를 호출해 입력 이름을 전달하세요:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```

사용자가 폼을 채우면, Precognition이 라우트의 폼 요청에 정의된 유효성 검사 규칙에 기반한 라이브 검증 결과를 제공합니다. 입력값이 변경될 때마다 디바운스된 Precognitive 유효성 검사 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 폼의 `setValidationTimeout` 함수로 조절할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검사 요청이나 폼 제출 중 반환된 오류들은 폼의 `errors` 객체에 자동으로 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 오류가 있는지 여부는 폼의 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

입력값이 통과했는지 실패했는지는 각각 폼의 `valid`와 `invalid` 함수에 입력 이름을 전달해 알 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]  
> 입력값이 변경되어 유효성 검사 응답이 도착해야만 해당 입력이 유효한지 또는 무효한지 표시됩니다.

Precognition으로 폼의 일부 입력만 검증할 때는 수동으로 오류를 지우는 것이 유용할 수 있습니다. 이때는 폼의 `forgetError` 함수를 사용하세요:

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```

위 예제처럼 각 입력의 `change` 이벤트에 연결해서 사용자가 상호작용할 때 개별 필드를 검증할 수 있지만, 사용자가 입력하지 않은 필드를 검증해야 하는 경우도 있습니다. 예를 들어 "마법사(wizard)" 형태의 UI에서 다음 단계로 넘어가기 전에 현재 보여지는 모든 필드를 검증할 때입니다.

이때는 `validate` 메서드를 호출하면서 `only` 옵션에 검증하려는 필드 이름 배열을 전달하세요. 성공과 실패에 대한 콜백은 `onSuccess`, `onValidationError`로 처리할 수 있습니다:

```html
<button
    type="button" 
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

물론 폼 제출 응답에 따라 별도의 동작을 실행할 수도 있습니다. 폼의 `submit` 메서드는 Axios 요청 프로미스를 반환하므로, 성공 시 폼 초기화 또는 실패 처리 등에 용이합니다:

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```

폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성을 확인하세요:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기 (Using Vue and Inertia)

> [!NOTE]  
> Vue와 Inertia로 Laravel 애플리케이션을 개발할 때 빠르게 시작하려면 [스타터 킷들](/docs/11.x/starter-kits)을 사용하는 것을 추천합니다. 이 스타터 킷은 백엔드와 프론트엔드 인증 스캐폴딩을 제공합니다.

Vue와 Inertia에서 Precognition을 사용하려면, 먼저 [Vue 사용법](#using-vue) 문서를 참고하세요. Vue와 함께 Inertia를 사용할 경우, NPM을 통해 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치가 완료되면 Precognition의 `useForm` 함수는 Inertia의 [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환하며, 앞서 설명한 유효성 검사 기능이 추가되어 있습니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL 지정이 필요 없도록 간소화되었으며, 대신 Inertia의 [방문 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인자로 전달할 수 있습니다. 예제 Vue와 달리 Promise를 반환하지 않고, 방문 옵션에 Inertia가 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 설정할 수 있습니다:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue-inertia';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit({
    preserveScroll: true,
    onSuccess: () => form.reset(),
});
</script>
```

<a name="using-react"></a>
### React 사용하기 (Using React)

Laravel Precognition을 사용하면 프론트엔드 React 애플리케이션에 유효성 검사 규칙 중복 없이 라이브 유효성 검사 기능을 제공할 수 있습니다. 사용법을 이해하기 위해 새로운 사용자 생성용 폼을 만들어 보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 추가하세요. 그리고 [폼 요청](/docs/11.x/validation#form-request-validation) 클래스로 유효성 검사를 정의해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그다음, React용 Precognition 프론트엔드 헬퍼를 NPM으로 설치하세요:

```shell
npm install laravel-precognition-react
```

설치가 완료되면 `useForm` 함수를 사용해 HTTP 메서드(`post`), URL(`/users`), 초기 데이터와 함께 폼 객체를 만듭니다.

라이브 유효성 검사를 위해 각 입력의 `change`와 `blur` 이벤트를 활용하세요. `change` 이벤트 핸들러에서는 폼의 `setData` 함수를 통해 변경된 값을 저장하고, `blur` 이벤트에서 `validate` 메서드로 유효성 검사를 수행합니다.

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```

사용자가 폼을 작성하면서 입력을 변경하면, Precognition이 라우트 폼 요청에 정의된 유효성 검사 규칙에 기반한 라이브 유효성 검사 결과를 제공합니다. 입력값이 변경될 때마다 지연된 Precognitive 요청이 라라벨 서버에 전송됩니다. 디바운스 지연 시간은 `setValidationTimeout` 함수로 설정 가능합니다:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청이 진행 중이면 `validating` 속성이 `true`입니다:

```jsx
{form.validating && <div>Validating...</div>}
```

유효성 검사 요청 또는 폼 제출 중 발생한 오류는 자동으로 `errors` 객체에 채워집니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

오류 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

유효하거나 무효인지의 판단은 각각 `valid`와 `invalid` 함수에 입력 이름을 넘겨 확인합니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]  
> 입력값이 변경되고 유효성 검사 응답을 받은 경우에만 해당 입력이 유효하거나 무효한 상태로 표시됩니다.

Precognition으로 폼 일부 입력에 대해서만 검증한다면, 오류를 수동으로 지우는 기능도 유용합니다. 이때는 `forgetError` 메서드를 사용합니다:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.value);

        form.forgetError('avatar');
    }}
>
```

각 입력의 `blur` 이벤트에 연결해 개별 필드 유효성 검사를 할 수 있지만, 아직 사용자가 상호작용하지 않은 필드도 검증해야 하는 경우가 있습니다. 예를 들어 "마법사(wizard)" UI에서 다음 단계로 넘어가기 전 모든 표시된 필드를 검증하는 경우입니다.

이때는 `validate` 메서드 호출 시 `only` 옵션에 검증할 필드 이름 배열을 넘기고, 성공과 실패 시 동작은 `onSuccess`, `onValidationError` 콜백을 통해 처리하세요:

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```

폼 제출 응답에 따른 후속 처리도 가능하며, `submit` 함수는 Axios 프로미스를 반환합니다:

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```

폼 제출 요청이 처리 중인지 확인하려면 `processing` 속성을 사용하세요:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기 (Using React and Inertia)

> [!NOTE]  
> React와 Inertia로 Laravel 애플리케이션을 개발할 때 빠르게 시작하려면 [스타터 킷들](/docs/11.x/starter-kits)을 사용하는 것을 추천합니다. 이 스타터 킷은 백엔드와 프론트엔드 인증 스캐폴딩을 제공합니다.

React와 Inertia에서 Precognition을 사용하기 전, 기본 [React 사용법](#using-react)을 확인하세요. React에서 Inertia를 함께 사용할 경우, 다음과 같이 Inertia 호환 Precognition 라이브러리를 NPM으로 설치하세요:

```shell
npm install laravel-precognition-react-inertia
```

설치 후, Precognition의 `useForm`은 Inertia의 [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환하며, 위에서 설명한 유효성 검사 기능을 포함합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL 지정이 없어도 되도록 축약되었으며, Inertia [방문 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인자로 전달합니다. React 예제와 달리 Promise를 반환하지 않고, 방문 옵션에 Inertia가 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 사용할 수 있습니다:

```js
import { useForm } from 'laravel-precognition-react-inertia';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = (e) => {
    e.preventDefault();

    form.submit({
        preserveScroll: true,
        onSuccess: () => form.reset(),
    });
};
```

<a name="using-alpine"></a>
### Alpine과 Blade 사용하기 (Using Alpine and Blade)

Laravel Precognition을 사용해 프론트엔드 Alpine 애플리케이션에서도 유효성 검사 규칙 중복 없이 라이브 유효성 검사 기능을 제공할 수 있습니다. 예제로 사용자 생성 폼을 만들어 보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 추가해야 하며, 라우트의 유효성 검사 규칙을 담을 [폼 요청](/docs/11.x/validation#form-request-validation) 클래스를 만들어야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, Alpine용 Precognition 프론트엔드 헬퍼를 NPM으로 설치하세요:

```shell
npm install laravel-precognition-alpine
```

그런 다음, `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록하세요:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Laravel Precognition 패키지가 설치 및 등록되면, Precognition의 `$form` 마법 함수를 사용해 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 전달하여 폼 객체를 생성할 수 있습니다.

라이브 유효성 검사를 위해 입력에 데이터 바인딩 후, 각 입력의 `change` 이벤트에 이벤트 리스너를 연결하고, 이벤트 핸들러에서 폼의 `validate` 메서드에 해당 입력 이름을 넘기세요:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```

사용자가 폼을 작성하면, Precognition이 라우트 폼 요청의 유효성 검사 규칙에 따라 라이브 유효성 검사 결과를 제공합니다. 입력 수정 시 디바운스된 Precognitive 요청이 라라벨에 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 메서드로 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검사 요청이 진행 중이면 `validating` 속성이 `true`입니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

유효성 검사 요청 혹은 폼 제출 시 반환된 오류는 자동으로 `errors` 객체에 채워집니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

오류 존재 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

각 입력이 유효한지 아닌지는 `valid` 및 `invalid` 함수에 입력 이름을 전달해 확인할 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]  
> 입력값이 변경되어 유효성 검사 응답이 도착한 후에만 해당 입력의 유효/무효 상태가 표시됩니다.

앞서 살펴본 것처럼, 각 입력의 `change` 이벤트를 감지해 개별 필드를 검증할 수 있지만, 사용자가 입력하지 않은 필드도 검증해야 하는 경우가 있습니다. 이는 "마법사(wizard)" UI에서 현재 보여지는 모든 필드를 검증한 뒤 다음 단계로 넘어갈 때 흔히 발생합니다.

이런 경우 `validate` 메서드를 호출하면서 `only` 옵션에 필드 이름 배열을 넘겨주고, 결과는 `onSuccess`, `onValidationError` 콜백으로 처리하세요:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

폼 제출 요청이 처리 중인지 확인하려면 `processing` 속성을 검사하세요:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 재설정하기

위 사용자 생성 예제에서는 Precognition으로 라이브 유효성 검사를 수행하지만, 전통적인 서버 사이드 폼 제출 방식으로 폼을 전송합니다. 따라서 서버 측 폼 제출에서 반환된 이전 입력값(`old`)과 유효성 검사 오류들을 폼에 채워야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

XHR 방식의 폼 제출을 원한다면, 폼의 `submit` 함수를 사용하세요. 이 함수는 Axios 요청 프로미스를 반환합니다:

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
### Axios 설정하기 (Configuring Axios)

Precognition 유효성 검사 라이브러리는 HTTP 클라이언트로 [Axios](https://github.com/axios/axios)를 사용해 백엔드 요청을 전송합니다. 필요에 따라 Axios 인스턴스를 커스터마이징할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때, `resources/js/app.js` 파일에서 요청 헤더를 추가할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 앱에서 정의한 Axios 인스턴스를 사용하고 싶다면, Precognition에 해당 인스턴스를 명시적으로 지정할 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]  
> Inertia 버전 Precognition 라이브러리는 유효성 검사 요청에 대해서만 지정된 Axios 인스턴스를 사용합니다. 폼 제출은 항상 Inertia를 통해 전송됩니다.

<a name="customizing-validation-rules"></a>
## 유효성 검사 규칙 사용자 정의하기 (Customizing Validation Rules)

Precognitive 요청 중에 실행될 유효성 검사 규칙을 `isPrecognitive` 메서드를 이용해 조건부로 조절할 수 있습니다.

예를 들어, 사용자 생성 폼에서 비밀번호가 보안 검증("uncompromised")을 통과하는지 여부는 최종 제출 시에만 검사하고, Precognitive 요청 때는 단순히 비밀번호가 요구되고 최소 8자임만 확인한다고 합시다. 아래처럼 `isPrecognitive` 메서드를 활용해 폼 요청의 규칙을 커스터마이징할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

<a name="handling-file-uploads"></a>
## 파일 업로드 처리 (Handling File Uploads)

기본적으로 Precognition은 유효성 검사 요청에서 파일을 업로드하거나 검증하지 않습니다. 이는 큰 파일을 불필요하게 여러 번 업로드하는 것을 방지하기 위함입니다.

이 동작으로 인해, 애플리케이션에서는 [유효성 검사 규칙을 사용자 정의하여](#customizing-validation-rules) 파일 필드는 전체 폼 제출 시에만 필수임을 명시하는 것이 좋습니다:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```

모든 유효성 검사 요청에서 파일을 포함시키고 싶다면, 클라이언트 측 폼 인스턴스에서 `validateFiles` 메서드를 호출하세요:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리하기 (Managing Side-Effects)

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가하면, Precognitive 요청 시 건너뛰어야 할 _다른_ 미들웨어의 부수 효과가 있는지 고려해야 합니다.

예를 들어, 사용자의 애플리케이션 내 "상호작용" 횟수를 기록하는 미들웨어가 있을 때, Precognitive 요청을 상호작용으로 집계하지 않으려면, 요청의 `isPrecognitive` 메서드를 체크하여 처리할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```

<a name="testing"></a>
## 테스트 (Testing)

테스트에서 Precognitive 요청을 하려면, Laravel의 `TestCase`에 포함된 `withPrecognition` 헬퍼를 사용해 요청 헤더에 `Precognition` 헤더를 추가할 수 있습니다.

또한, 유효성 검사 오류 없이 성공적인 Precognitive 요청인지 확인하려면, 응답에서 `assertSuccessfulPrecognition` 메서드를 사용하세요:

```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```