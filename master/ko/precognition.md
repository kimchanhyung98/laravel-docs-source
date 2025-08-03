# Precognition

- [소개](#introduction)
- [라이브 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 구성하기](#configuring-axios)
- [유효성 검증 규칙 사용자 정의하기](#customizing-validation-rules)
- [파일 업로드 처리하기](#handling-file-uploads)
- [부수 효과 관리하기](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 미래에 실행될 HTTP 요청의 결과를 미리 예측할 수 있게 해줍니다. Precognition의 주요 사용 사례 중 하나는, 애플리케이션의 백엔드 유효성 검증 규칙을 중복하지 않고도 프런트엔드 JavaScript 애플리케이션에서 "라이브" 유효성 검증을 제공할 수 있다는 점입니다. 특히 Laravel의 Inertia 기반 [스타터 키트](/docs/master/starter-kits)와 잘 어울립니다.

Laravel이 “precognitive request”를 받으면, 해당 라우트의 모든 미들웨어를 실행하고 라우트 컨트롤러의 의존성도 해석하며, [폼 요청](/docs/master/validation#form-request-validation)에 정의된 유효성 검증까지 수행하지만, 라우트 컨트롤러의 메서드는 실제로 실행하지 않습니다.

<a name="live-validation"></a>
## 라이브 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기 (Using Vue)

Laravel Precognition을 사용하면 프런트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복하지 않고도 라이브 유효성 검증 기능을 제공할 수 있습니다. 동작 방식을 설명할 예제로, 애플리케이션 내에서 새 사용자 생성 폼을 만들어보겠습니다.

먼저, 라우트에서 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 그리고 라우트에서 사용할 유효성 검증 규칙을 보관할 [폼 요청](/docs/master/validation#form-request-validation)을 생성하세요:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, NPM을 사용해 Vue용 Laravel Precognition 프런트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-vue
```

패키지 설치 후에는, Precognition의 `useForm` 함수를 사용해 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 전달하여 폼 객체를 생성할 수 있습니다.

라이브 유효성 검증을 활성화하려면, 각 입력 요소의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하고, 해당 입력 이름을 인수로 전달하세요:

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

이제 사용자가 폼을 작성할 때, Precognition이 해당 라우트의 폼 요청에 정의된 유효성 검증 규칙을 바탕으로 라이브 유효성 검증 결과를 제공합니다. 사용자가 입력값을 변경할 때 디바운스된 "precognitive" 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 시간을 폼의 `setValidationTimeout` 함수로 조절할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검증 요청이나 폼 제출 중 반환된 모든 유효성 오류는 자동으로 폼의 `errors` 객체에 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 오류가 있는지 여부는 `hasErrors` 속성으로 알 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

특정 입력이 유효한지 또는 유효하지 않은지는 해당 입력의 이름을 `valid`와 `invalid` 함수에 전달하여 확인할 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 입력값이 변경되고 유효성 검증 응답이 도착해야만 입력은 유효하거나 유효하지 않은 상태로 표시됩니다.

Precognition으로 폼 일부 입력에 대해서만 유효성 검증할 경우, 오류를 수동으로 지우는 게 유용할 수 있습니다. `forgetError` 메서드를 사용하면 특정 입력의 오류를 삭제할 수 있습니다:

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

앞서 본 것처럼, 입력의 `change` 이벤트에 연결해 사용자가 상호작용할 때 개별 입력을 유효성 검증할 수 있습니다. 다만, 사용자가 아직 조작하지 않은 입력도 유효성 검증할 필요가 있습니다. 이는 "위저드" 등에서, 다음 단계로 넘어가기 전에 사용자와 상호작용했든 안 했든 화면에 보이는 모든 입력을 유효성 검증하려 할 때 일반적입니다.

이 경우, `validate` 메서드를 호출하면서 `only` 설정 값으로 검증할 필드 이름 배열을 전달하세요. 그리고 `onSuccess` 또는 `onValidationError` 콜백을 통해 유효성 검증 결과에 대응할 수 있습니다:

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

물론 폼 제출 응답을 받은 후 실행할 코드도 작성할 수 있습니다. 폼의 `submit` 함수는 Axios 요청 프로미스를 반환하므로, 성공 시 응답 데이터를 참조하거나 폼을 초기화하거나 요청 실패 시 처리하기에 편리합니다:

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

폼 제출 요청이 진행 중인지 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기 (Using Vue and Inertia)

> [!NOTE]
> Vue와 Inertia로 Laravel 애플리케이션을 빠르게 개발하고 싶다면, [스타터 키트](/docs/master/starter-kits)를 사용해보세요. 스타터 키트는 백엔드 및 프런트엔드 인증 스캐폴딩도 함께 제공합니다.

Precognition을 Vue와 Inertia와 함께 사용하려면, 먼저 [Vue 사용하기](#using-vue) 문서를 참고하세요. Vue와 Inertia를 같이 쓸 때는, NPM으로 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치 후, Precognition의 `useForm` 함수는 위에서 설명한 유효성 검증 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드와 URL을 지정할 필요 없이 호출할 수 있으며, 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째이자 유일한 인수로 전달합니다. 또한 React 예제와 달리 `submit` 메서드는 Promise를 반환하지 않으며, `submit` 호출 시 전달된 visit 옵션에 Inertia에서 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 지정할 수 있습니다:

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

Laravel Precognition을 사용하면 프런트엔드 React 애플리케이션에서 유효성 검증 규칙을 중복하지 않고도 라이브 유효성 검증을 제공할 수 있습니다. 동작 방식을 설명하기 위해, 앞서 Vue에서 했던 것처럼 새 사용자 생성 폼을 만들어보겠습니다.

우선, Precognition 활성화를 위해 `HandlePrecognitiveRequests` 미들웨어를 라우트에 추가하고, [폼 요청](/docs/master/validation#form-request-validation)을 만들어 유효성 규칙을 정의하세요:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그런 다음 React용 Laravel Precognition 프런트엔드 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-react
```

설치가 완료되면 `useForm` 함수로 HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 전달하여 폼 객체를 생성할 수 있습니다.

라이브 유효성 검증을 위해 각 입력 요소의 `change` 및 `blur` 이벤트에 리스너를 달아주세요. `change` 이벤트 핸들러에서는 `setData` 메서드로 입력 이름과 값을 전달해 폼 데이터를 갱신하고, `blur` 이벤트 핸들러에서는 `validate` 메서드에 입력 이름을 전달해 해당 입력을 유효성 검증합니다:

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

앞서 Vue 예제에서 설명한 것과 같이, 사용자가 입력을 변경하면 Precognition이 디바운스된 유효성 검증 요청을 Laravel 애플리케이션으로 전송하고, 유효성 검증 규칙에 따라 결과를 제공합니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 조정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이면 `validating` 속성이 `true`입니다:

```jsx
{form.validating && <div>Validating...</div>}
```

유효성 오류는 자동으로 `errors` 객체에 채워집니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 오류가 있는지 `hasErrors` 속성으로 알 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

특정 입력이 유효한지 여부는 `valid`와 `invalid` 메서드로 확인할 수 있습니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력값이 변경되고 유효성 검증 응답을 받아야만 해당 입력이 유효하거나 유효하지 않은 상태로 표시됩니다.

Precognition으로 폼 일부 입력의 유효성 검증을 할 때, 오류를 수동으로 삭제해야 할 경우 `forgetError` 메서드를 사용할 수 있습니다:

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

사용자가 아직 조작하지 않은 입력도 유효성 검증이 필요한 경우, 즉 "위저드" 스타일 폼에서 다음 단계로 넘어가기 전에 표시된 모든 입력을 검증하려면, `validate` 메서드에 `only` 설정으로 필드 이름 목록을 전달하고, `onSuccess`, `onValidationError` 콜백으로 결과를 처리하세요:

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

폼 제출 시 반응하는 코드를 작성하려면 `submit` 함수가 반환하는 Axios 요청 프로미스를 활용하세요:

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

폼 제출 요청이 진행 중인지 확인하려면 `processing` 속성을 검사하세요:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기 (Using React and Inertia)

> [!NOTE]
> React와 Inertia로 Laravel 애플리케이션을 빠르게 시작하려면, [스타터 키트](/docs/master/starter-kits)를 활용해보세요. 스타터 키트는 백엔드 및 프런트엔드 인증 스캐폴딩을 제공합니다.

Precognition을 React와 Inertia로 사용하려면, 먼저 [React 사용하기](#using-react) 섹션을 참고하세요. React와 Inertia를 함께 쓸 때는 NPM으로 Inertia 호환 Precognition 라이브러리를 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치가 완료되면 `useForm` 함수는 위의 유효성 검증 기능이 포함된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼 `submit` 메서드는 HTTP 메서드와 URL 지정이 필요 없으며, 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째 인수로 전달하도록 간소화되었습니다. React 예제와 달리 `submit`은 Promise를 반환하지 않고, 전달된 visit 옵션에 Inertia가 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 포함시킬 수 있습니다:

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

Laravel Precognition 덕분에 프런트엔드 Alpine 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 라이브 유효성 검증 기능을 제공할 수 있습니다. 동작 방식을 설명하기 위해, 새 사용자를 생성하는 폼을 만들어보겠습니다.

우선, Precognition을 켜려면 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가하고, [폼 요청](/docs/master/validation#form-request-validation)을 만들어 유효성 검증 규칙을 정의하세요:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로 Alpine용 Laravel Precognition 프런트엔드 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록합니다:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

설치 및 등록을 마친 후, Precognition의 `$form` "매직"을 사용해 HTTP 메서드(`post`), URL(`/users`), 초기 폼 데이터를 전달해 폼 객체를 생성할 수 있습니다.

라이브 유효성 검증을 활성화하려면 폼 데이터를 관련 입력에 바인딩하고, 각 입력의 `change` 이벤트에서 폼의 `validate` 메서드에 입력 이름을 전달하세요:

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

사용자가 입력할 때마다, 라우트의 폼 요청에 정의된 유효성 검증 규칙에 따라 Precognition이 라이브 유효성 검증 결과를 제공합니다. 입력 변경 시 디바운스된 "precognitive" 유효성 검증 요청이 서버로 전송됩니다. 디바운스 시간은 `setValidationTimeout` 함수로 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중이면 `validating` 속성이 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

유효성 검증 오류는 자동으로 `errors` 객체에 할당됩니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 오류가 있는지 여부도 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

특정 입력이 유효한지 또는 유효하지 않은지는 `valid`와 `invalid` 메서드에 입력 이름을 전달해 알 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력이 변경되고 유효성 검증 응답이 도착해야만 유효/유효하지 않은 상태로 표시됩니다.

앞서 예시처럼, 입력의 `change` 이벤트에 연결해 개별 입력을 유효성 검증할 수 있지만, 사용자가 아직 조작하지 않은 입력도 검증해야 할 수 있습니다. 이는 "위저드" 등에서 다음 단계로 넘어가기 전에 화면에 표시된 모든 입력을 유효성 검증할 때 흔한 요구사항입니다.

이럴 때는 `validate` 메서드에 `only` 설정으로 검증할 필드를 명시하고, `onSuccess`, `onValidationError` 콜백으로 결과를 처리하세요:

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

폼 제출 요청이 진행 중인지 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 입력 데이터 재채우기

앞서 사용자 생성 예제에서는 라이브 유효성 검증에 Precognition을 사용하지만, 전통적인 서버 측 폼 제출 방식도 함께 사용합니다. 따라서 서버에서 반환된 이전 입력값과 유효성 오류를 폼에 채워줘야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는 XHR을 통해 폼을 제출하려면, 폼의 `submit` 함수(Axios 요청 프로미스 반환)를 사용할 수 있습니다:

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
### Axios 구성하기 (Configuring Axios)

Precognition 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용해 백엔드에 요청을 전송합니다. 편의를 위해 애플리케이션 요구에 따라 Axios 인스턴스를 커스터마이징할 수 있습니다. 예를 들어, `laravel-precognition-vue`를 사용하는 경우, `resources/js/app.js`에서 모든 요청에 추가 헤더를 붙일 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 애플리케이션용으로 구성된 Axios 인스턴스가 있다면, Precognition에 해당 인스턴스를 사용하도록 알려줄 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia용 Precognition 라이브러리는 유효성 검증 요청에만 설정된 Axios 인스턴스를 사용합니다. 폼 제출 요청은 항상 Inertia가 전송합니다.

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 사용자 정의하기 (Customizing Validation Rules)

precognitive 요청 중에 실행할 유효성 검증 규칙을 요청의 `isPrecognitive` 메서드를 사용해 커스터마이징할 수 있습니다.

예를 들어, 사용자 생성 폼에서 비밀번호가 실제 폼 제출 시에만 "uncompromised"(브루트포스 공격에 노출되지 않은 상태) 조건을 만족하도록 검증하고, precognitive 요청 시에는 단순히 필수 및 최소 8자만 검사하도록 할 수 있습니다. `isPrecognitive` 메서드를 활용해 폼 요청의 규칙을 분기하세요:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * 요청에 적용할 유효성 검증 규칙을 반환합니다.
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
## 파일 업로드 처리하기 (Handling File Uploads)

기본적으로 Laravel Precognition은 precognitive 유효성 검증 요청에서 파일을 업로드하거나 검증하지 않습니다. 이는 큰 파일을 불필요하게 여러 번 업로드하는 일을 방지합니다.

따라서, 서버 측 폼 요청에서 [유효성 검증 규칙을 적절히 변경](#customizing-validation-rules)해, 파일 필드는 전체 폼 제출 시에만 파일이 필수임을 지정해야 합니다:

```php
/**
 * 요청에 적용할 유효성 검증 규칙을 반환합니다.
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

모든 유효성 검증 요청에서 파일도 포함하고자 한다면, 클라이언트 측 폼 인스턴스에서 `validateFiles` 메서드를 호출하세요:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리하기 (Managing Side-Effects)

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, precognitive 요청 동안 건너뛰어야 할 _다른_ 미들웨어의 부수 효과가 있는지 고려해야 합니다.

예를 들어, 사용자가 애플리케이션과 상호작용할 때마다 총 상호작용 횟수를 증가시키는 미들웨어가 있다면, precognitive 요청은 실제 상호작용으로 간주하지 않도록 `isPrecognitive` 메서드를 검사한 뒤에 증가시켜야 합니다:

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * 들어오는 요청을 처리합니다.
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

테스트에서 precognitive 요청을 실행하려면, Laravel의 `TestCase` 클래스에 포함된 `withPrecognition` 헬퍼를 사용해 `Precognition` 요청 헤더를 추가할 수 있습니다.

또한, precognitive 요청이 성공했는지(예: 유효성 오류를 반환하지 않았는지) 검증하고 싶다면, 응답 객체의 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:

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