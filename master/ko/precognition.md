# Precognition

- [소개](#introduction)
- [실시간 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리하기](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개

Laravel Precognition은 미래의 HTTP 요청 결과를 미리 예측할 수 있도록 도와줍니다. Precognition의 주요 사용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드 검증 규칙을 중복하지 않고도 "실시간" 폼 검증을 제공하는 것입니다. Precognition은 Laravel의 Inertia 기반 [스타터 킷](/docs/{{version}}/starter-kits)과 특히 잘 어울립니다.

Laravel이 "precognitive request"(예측 요청)를 받으면, 해당 라우트의 모든 미들웨어를 실행하고 라우트 컨트롤러의 의존성을 해석하며, [폼 요청](/docs/{{version}}/validation#form-request-validation)도 검증합니다. 하지만 실제로 라우트의 컨트롤러 메서드는 실행하지 않습니다.

<a name="live-validation"></a>
## 실시간 검증

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면 프론트엔드 Vue 애플리케이션에서 검증 규칙을 중복하지 않고도 사용자에게 실시간 검증 경험을 제공할 수 있습니다. 작동 방식을 설명하기 위해, 신규 사용자를 만드는 폼을 예시로 만들어보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 그리고 해당 라우트의 검증 규칙을 보관할 [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, NPM을 통해 Vue용 Laravel Precognition 프론트엔드 헬퍼를 설치합니다.

```shell
npm install laravel-precognition-vue
```

설치가 끝나면 Precognition의 `useForm` 함수를 사용하여 폼 객체를 만들 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 전달합니다.

실시간 검증을 활성화하려면, 각 입력 필드의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하며 입력 필드명을 전달합니다.

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

이제 사용자가 폼을 작성하는 과정에서 Precognition이 라우트의 폼 요청 검증 규칙에 따라 실시간 검증 결과를 제공합니다. 입력 값이 변경될 때마다 디바운스된 "precognitive" 검증 요청이 Laravel 애플리케이션에 전송됩니다. 폼의 `setValidationTimeout` 함수를 호출하여 디바운스 대기 시간을 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행 중일 때에는 폼의 `validating` 속성이 `true`가 됩니다.

```html
<div v-if="form.validating">
    Validating...
</div>
```

검증 요청 또는 폼 제출 시 반환된 검증 오류는 자동으로 폼의 `errors` 객체에 반영됩니다.

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 어떠한 오류가 존재하는지 폼의 `hasErrors` 속성을 사용하여 확인할 수 있습니다.

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

또한 입력 필드의 이름을 각각 폼의 `valid`와 `invalid` 함수에 전달해 해당 필드의 검증 성공/실패 여부를 확인할 수 있습니다.

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 폼 입력값은 변경과 검증 응답이 완료된 후에만 유효/무효로 표시됩니다.

Precognition으로 폼의 일부 입력만 검증 중인 경우에는 오류를 수동으로 제거하는 것이 유용할 수 있습니다. 폼의 `forgetError` 함수를 사용하여 오류를 제거할 수 있습니다.

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
/>
```

이처럼 입력값이 변경될 때마다 각 입력의 `change` 이벤트와 연결해 검증할 수 있습니다. 하지만 사용자가 아직 건드리지 않은 입력값들까지 검증해야 할 경우가 있습니다. 예를 들어 "마법사(wizard) UI"에서는 사용 여부와 상관없이 모든 표시된 입력값을 다음 단계로 넘어가기 전에 검증하고 싶을 수 있습니다.

이럴 때는 `validate` 메서드 호출 시 `only` 설정 키에 검증할 필드명 배열을 전달하면 됩니다. 또한 `onSuccess` 또는 `onValidationError` 콜백으로 검증 결과 처리도 가능합니다.

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

물론, 폼 제출 응답에 따라 별도의 코드를 실행하는 것도 가능합니다. 폼의 `submit` 함수는 Axios 요청 프로미스를 반환하므로, 응답에 접근하거나, 성공 시 폼을 리셋하거나, 실패 시 처리를 쉽게 할 수 있습니다.

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

폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성을 검사하면 알 수 있습니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기

> [!NOTE]
> Vue와 Inertia로 Laravel 애플리케이션을 개발할 때 빠르게 시작하고 싶다면 [스타터 킷](/docs/{{version}}/starter-kits) 사용을 고려해보세요. Laravel의 스타터 킷은 백엔드와 프론트엔드 인증 기본 구조를 제공합니다.

Vue와 Inertia에서 Precognition을 사용하기 전에 먼저 [Vue에서 Precognition 사용](#using-vue) 문서를 참고하세요. Inertia와 함께 사용할 때는 Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다.

```shell
npm install laravel-precognition-vue-inertia
```

설치 후 Precognition의 `useForm` 함수는 Inertia [form helper](https://inertiajs.com/forms#form-helper)에 검증 기능이 추가되어 반환됩니다.

폼 헬퍼의 `submit` 메서드는 더 간단해져, HTTP 메서드나 URL을 지정할 필요가 없습니다. 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인자로 전달하면 됩니다. 또한 `submit` 메서드는 위 Vue 예시처럼 Promise를 반환하지 않습니다. 대신 Inertia에서 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 visit 옵션에 제공해 처리할 수 있습니다.

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
### React 사용하기

Laravel Precognition을 사용하면 프론트엔드 React 애플리케이션에서 검증 규칙을 중복하지 않고도 사용자에게 실시간 검증 경험을 제공할 수 있습니다. 신규 사용자를 만드는 폼을 예시로 설명해보겠습니다.

먼저 라우트에서 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가하고, 해당 라우트의 검증 규칙을 담을 [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, React용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치해야 합니다.

```shell
npm install laravel-precognition-react
```

설치가 끝나면 Precognition의 `useForm` 함수를 사용해 폼 객체를 만들 수 있습니다. HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 전달합니다.

실시간 검증을 위해 각 입력 필드의 `change`와 `blur` 이벤트를 감지해야 합니다. `change` 이벤트에서 `setData`로 값 업데이트, `blur`에서 `validate`로 검증을 호출합니다.

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

이제 사용자가 폼을 작성하면 Precognition이 라우트의 폼 요청 검증 규칙에 따라 실시간 검증 결과를 제공합니다. 입력값이 변경될 때마다 디바운스된 예측 검증 요청이 Laravel로 전송되며, `setValidationTimeout` 으로 디바운스 대기 시간을 조절할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

검증 요청 진행 중 여부는 `validating` 속성을 체크할 수 있습니다.

```jsx
{form.validating && <div>Validating...</div>}
```

검증 오류는 자동으로 폼의 `errors` 객체에 반영됩니다.

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 오류가 있는지 여부는 `hasErrors` 속성으로 확인합니다.

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

입력 값의 유효/무효 여부는 다음처럼 확인할 수 있습니다.

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력값은 변경 및 검증 응답이 도착한 후에만 유효/무효로 표시됩니다.

Precognition으로 폼의 일부 입력만 검증하는 경우 수동으로 오류를 삭제하는 것도 가능합니다.

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.value);

        form.forgetError('avatar');
    }}
/>
```

앞서 본 것처럼 각 입력의 `blur` 이벤트에 검증을 연결할 수 있습니다. 그러나 사용자가 아직 입력하지 않은 값들도 전체 검증이 필요하다면 다음 단계로 넘어가기 전에 표시된 모든 입력을 한 번에 검증하면 됩니다.

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

그리고 제출 응답에 반응하여 별도 코드를 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프로미스를 반환합니다.

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

폼 제출이 진행 중인지 여부는 `processing` 속성을 통해 알 수 있습니다.

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기

> [!NOTE]
> React와 Inertia로 Laravel 애플리케이션 개발을 빠르게 시작하고 싶다면 [스타터 킷](/docs/{{version}}/starter-kits) 사용을 고려하세요. Laravel 스타터 킷은 백엔드/프론트엔드 인증 템플릿을 제공합니다.

React와 Inertia에서 Precognition을 사용하기 전에 [React에서 Precognition 사용](#using-react) 관련 내용을 반드시 살펴보세요. React에서 Inertia와 함께 Precognition을 사용하려면 Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다.

```shell
npm install laravel-precognition-react-inertia
```

설치 후 Precognition의 `useForm` 함수가 Inertia [form helper](https://inertiajs.com/forms#form-helper)에 검증 기능을 추가해 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL 지정을 생략할 수 있도록 단순화되어 있습니다. 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 인자로 전달하면 됩니다. `submit` 메서드는 Promise를 반환하지 않고, 대신 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 visit 옵션에 지정해 사용할 수 있습니다.

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
### Alpine과 Blade 사용하기

Laravel Precognition을 사용하여 프론트엔드 Alpine 애플리케이션의 검증 규칙을 중복하지 않고도 실시간 검증 경험을 제공할 수 있습니다. 신규 사용자 생성 폼 예시로 설명합니다.

먼저 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가하고, [폼 요청](/docs/{{version}}/validation#form-request-validation) 클래스를 만들어야 합니다.

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, Alpine용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치하세요.

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록합니다.

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Precognition 패키지를 설치하고 등록한 다음, Precognition의 `$form` "매직"을 활용해 폼 객체를 만들 수 있습니다. HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 입력합니다.

실시간 검증을 위해 폼 데이터를 입력값에 바인딩하고, 각 입력의 `change` 이벤트를 감지해 `validate` 메서드를 실행합니다.

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

이제 사용자가 폼을 입력하면 Precognition이 서버의 폼 요청 검증 규칙 기반으로 실시간 검증을 제공합니다. 입력이 바뀌면 디바운스된 검증 요청이 전송되며, `setValidationTimeout`으로 디바운스 시간을 조정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행 중일 때는 `validating` 속성값이 `true`가 됩니다.

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

검증 오류는 자동으로 `errors` 객체에 포함됩니다.

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 전체 오류가 있는지 `hasErrors` 속성으로 확인할 수 있습니다.

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

입력값이 유효/무효인지 `valid`, `invalid` 함수로 판단할 수 있습니다.

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력값은 값이 변경되고 검증 응답이 도착한 이후에만 유효/무효로 표시됩니다.

마찬가지로 입력의 `change` 이벤트에 검증을 연결할 수 있지만, "마법사" UI처럼 아직 손대지 않은 값도 일괄 검증하고 싶을 땐 다음처럼 하면 됩니다.

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

폼 제출이 진행 중인지 `processing`으로 알 수 있습니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 재채우기

위 예시처럼 Precognition으로 실시간 검증을 하더라도 폼 제출은 전통적인 서버 사이드 방식일 수 있습니다. 이 경우, 폼에 서버에서 전달된 "old" 입력값과 검증 오류가 반영되어야 합니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는 폼을 XHR로 제출하고 싶다면 폼의 `submit` 함수를 통해 Axios 프로미스를 사용할 수 있습니다.

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
                    this.form.reset();

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
### Axios 설정하기

Precognition 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 통해 백엔드로 요청을 전송합니다. 필요하다면 이 Axios 인스턴스를 직접 커스터마이즈할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리 사용 시 `resources/js/app.js`에서 모든 요청에 추가 헤더를 붙일 수 있습니다.

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 커스텀 Axios 인스턴스가 있다면 Precognition이 해당 인스턴스를 사용하게 할 수도 있습니다.

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia 타입의 Precognition 라이브러리는 검증 요청에 대해서만 커스텀 Axios 인스턴스를 사용합니다. 폼 제출은 항상 Inertia를 통해 전송됩니다.

<a name="customizing-validation-rules"></a>
## 검증 규칙 커스터마이징

`isPrecognitive` 메서드를 활용하면 precognitive(예측) 요청 시 실행되는 검증 규칙을 커스터마이징할 수 있습니다.

예를 들어, 사용자 생성 폼에서 비밀번호가 "유출되지 않은(uncompromised)" 것인지 최종 제출에만 검증하고, 예측 검증 시에는 '필수' 및 최소 8자만 확인하고 싶다고 가정합니다. `isPrecognitive` 메서드로 폼 요청의 규칙을 변경할 수 있습니다.

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
## 파일 업로드 처리

기본적으로 Precognition은 예측 검증 요청 중에 파일을 업로드하거나 검증하지 않습니다. 즉, 대용량 파일을 여러 번 업로드하는 것을 방지합니다.

이런 동작 때문에 [폼 요청의 검증 규칙](#customizing-validation-rules)을 커스터마이징해서 실제 폼 제출에 대해서만 해당 필드를 `required`로 처리하도록 해야 합니다.

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

모든 검증 요청에 파일 업로드를 포함하고 싶다면 클라이언트 코드에서 `validateFiles` 함수를 호출하면 됩니다.

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리하기

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, "다른 미들웨어"에서 부수 효과(예: 데이터 저장, 카운트 증가 등)가 예측 요청 시 무시되어야 하는지 고려해야 합니다.

예를 들어, 사용자의 "상호작용" 카운트를 늘리는 미들웨어가 있다고 할 때, 예측 요청에 대해서는 카운트를 증가시키지 않아야 할 수 있습니다. 이럴 때는 `isPrecognitive` 메서드로 살펴본 후 부수 효과를 건너뛸 수 있습니다.

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
## 테스트

테스트에서 Precognition 요청을 하고 싶다면, Laravel의 `TestCase`는 `withPrecognition` 헬퍼를 제공하며, 이를 이용해 요청 헤더에 `Precognition`을 추가할 수 있습니다.

또한, 예측 요청이 성공(예: 검증 오류 없음)했는지 확인하려면, 응답에서 `assertSuccessfulPrecognition` 메서드를 사용하면 됩니다.

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
