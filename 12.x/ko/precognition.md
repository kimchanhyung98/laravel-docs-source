# Precognition

- [소개](#introduction)
- [라이브 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 미래 HTTP 요청의 결과를 미리 예측할 수 있게 해줍니다. Precognition의 주요 사용 사례 중 하나는 백엔드의 검증 규칙을 중복하지 않고도 프론트엔드 자바스크립트 애플리케이션에서 실시간("라이브") 검증을 제공하는 것입니다. Precognition은 Laravel의 Inertia 기반 [스타터 킷](/docs/12.x/starter-kits)과 특히 잘 어울립니다.

Laravel이 "precognitive request"를 수신하면 해당 라우트의 모든 미들웨어를 실행하며 라우트 컨트롤러 의존성을 해결하고, [폼 요청](/docs/12.x/validation#form-request-validation) 검증도 수행하지만, 실제로 라우트 컨트롤러 메서드는 실행하지 않습니다.

<a name="live-validation"></a>
## 라이브 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기 (Using Vue)

Laravel Precognition을 사용하면 프론트엔드 Vue 애플리케이션에서 검증 규칙을 중복하지 않고도 라이브 검증 경험을 제공할 수 있습니다. 작동 방식을 설명하기 위해, 애플리케이션 내에서 새 사용자를 생성하는 폼을 만들어보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 그리고 라우트의 검증 규칙을 담을 [폼 요청](/docs/12.x/validation#form-request-validation)을 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, NPM을 통해 Vue용 Laravel Precognition 프론트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-vue
```

Laravel Precognition 패키지를 설치한 후, `useForm` 함수를 사용해 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 제공하여 폼 객체를 생성할 수 있습니다.

그 다음, 라이브 검증을 활성화하려면 각 인풋의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하고, 검증하려는 입력 이름을 넘겨줘야 합니다:

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

사용자가 폼을 채우면, Precognition은 라우트의 폼 요청에 정의된 검증 규칙을 기반으로 라이브 검증 결과를 제공합니다. 각 입력이 변경되면 디바운스된 "precognitive" 검증 요청이 Laravel 애플리케이션에 전송됩니다. 디바운스 타임아웃은 폼의 `setValidationTimeout` 함수를 호출하여 설정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행 중일 때 폼의 `validating` 속성은 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

검증 요청 또는 폼 제출 중 반환된 모든 검증 오류는 폼의 `errors` 객체에 자동으로 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 오류가 있는지 여부는 `hasErrors` 속성을 통해 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

또한, 각 입력이 검증에 통과했는지 실패했는지는 입력 이름을 `valid` 또는 `invalid` 함수에 전달하여 알 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 폼 입력값은 한 번 변화하고 검증 응답이 반환된 이후에야 `valid` 또는 `invalid` 상태로 표시됩니다.

Precognition으로 폼 입력의 일부만 검증할 경우, 오류를 수동으로 제거하는 것이 유용할 수 있습니다. 이때는 폼의 `forgetError` 함수를 사용하세요:

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

사용자가 상호작용한 입력만 검증하는 대신, 사용자가 아직 조작하지 않은 입력도 검증해야 하는 경우가 있습니다. 예를 들어, "마법사형(wizard)" UI에서 다음 단계로 넘어가기 전에 표시된 모든 입력을 검증해야 할 때입니다.

Precognition으로 이를 처리하려면, `validate` 메서드를 호출할 때 `only` 설정 키에 검증할 필드 이름 배열을 전달하세요. 검증 결과는 `onSuccess` 혹은 `onValidationError` 콜백으로 처리할 수 있습니다:

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

물론, 폼 제출 응답에 따른 코드도 실행할 수 있습니다. 폼의 `submit` 함수는 Axios 요청 프로미스를 반환하므로, 응답 데이터를 편리하게 다루거나, 성공 시 폼을 초기화하거나, 실패 시 처리할 수 있습니다:

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

폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성을 통해 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기 (Using Vue and Inertia)

> [!NOTE]
> Vue와 Inertia로 Laravel 애플리케이션을 개발할 때, 백엔드와 프론트엔드 인증 스캐폴드를 제공하는 [스타터 킷](/docs/12.x/starter-kits)을 사용하는 것을 고려해보세요.

Vue와 Inertia에서 Precognition을 사용하려면, 우선 [Vue 사용하기](#using-vue) 문서도 확인하세요. 그리고 Inertia 호환 Precognition 라이브러리를 NPM으로 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치 후, Precognition의 `useForm` 함수는 앞서 설명한 검증 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 명시할 필요가 없도록 간소화되었으며, 대신 Inertia의 [visit 옵션들](https://inertiajs.com/manual-visits)을 단 하나의 인수로 넘길 수 있습니다. 또한, Vue 예제와는 달리 `submit` 메서드는 Promise를 반환하지 않고, 대신 Inertia가 지원하는 [이벤트 콜백들](https://inertiajs.com/manual-visits#event-callbacks)을 `submit` 메서드에 전달된 방문 옵션에서 지정할 수 있습니다:

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

Laravel Precognition을 사용하여 React 프론트엔드 애플리케이션에도 검증 규칙을 중복하지 않고 실시간 검증 기능을 제공할 수 있습니다. 작동 방식을 살펴보기 위해, 새 사용자 생성을 위한 폼을 만들어 보겠습니다.

먼저, Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트에 추가하고, 그 검증 규칙을 담을 [폼 요청](/docs/12.x/validation#form-request-validation)을 만듭니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, React용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-react
```

설치 후, `useForm` 함수를 사용해 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 데이터로 폼 객체를 생성하세요.

라이브 검증을 활성화하려면 각 입력의 `change`와 `blur` 이벤트를 청취해야 합니다. `change` 이벤트 핸들러에서는 `setData` 함수를 써서 입력의 이름과 새 값을 폼 데이터에 저장하고, `blur` 이벤트 핸들러에서는 폼의 `validate` 메서드에 입력 이름을 전달하여 검증을 수행합니다:

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

사용자가 폼을 채우면, Precognition은 라우트의 폼 요청 검증 규칙에 따라 라이브 검증 결과를 제공합니다. 입력이 변경될 때마다 디바운스된 "precognitive" 검증 요청이 Laravel에 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 조정할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행 중이면 폼의 `validating` 속성은 `true`입니다:

```jsx
{form.validating && <div>Validating...</div>}
```

검증 요청이나 폼 제출 시 반환된 오류는 자동으로 `errors` 객체에 저장됩니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

검증 오류가 있는지 여부는 `hasErrors` 속성으로 알 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

각 입력 필드가 검증 통과 혹은 실패했는지는 `valid`와 `invalid` 함수에 입력 이름을 전달해 확인할 수 있습니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력은 한 번 변하고 검증 응답이 도착한 이후에야 valid 또는 invalid 상태가 됩니다.

Precognition으로 폼의 일부 입력만 검증할 경우, 오류를 수동으로 지우는 것이 유용할 수 있습니다. 폼의 `forgetError` 함수를 사용하세요:

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

입력 `blur` 이벤트에 묶어 개별 항목을 검증할 수도 있지만, 사용자가 아직 상호작용하지 않은 입력도 검증할 필요가 생길 수 있습니다. 특히 "마법사형(wizard)" UI에서는 모든 표시된 입력을 유효성 검사하고 다음 단계로 진행해야 할 때가 그렇습니다.

이때는 `validate` 메서드 호출 시 검증할 필드명을 `only` 설정값으로 전달하고, `onSuccess`나 `onValidationError` 콜백으로 결과를 처리하세요:

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

물론, 폼 제출 응답에 따라 로직을 수행할 수 있습니다. `submit` 함수는 Axios 요청 프로미스를 반환해, 응답 payload 접근과 성공 시 폼 초기화, 실패 시 처리 등을 쉽게 할 수 있습니다:

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

폼 제출 요청 진행 중인가 여부는 `processing` 속성으로 알 수 있습니다:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기 (Using React and Inertia)

> [!NOTE]
> React와 Inertia로 Laravel을 개발할 때, 백엔드 및 프론트엔드 인증 스캐폴더를 제공하는 [스타터 킷](/docs/12.x/starter-kits)을 활용하면 시작하기 쉽습니다.

React와 Inertia에서 Precognition을 사용하려면, 우선 [React 사용하기](#using-react) 내용을 확인하세요. 그리고 Inertia 호환 Precognition 라이브러리를 NPM으로 설치합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치 후, `useForm` 함수는 앞서 설명한 검증 기능이 추가된 Inertia [폼 헬퍼](https://inertiajs.com/forms#form-helper)를 반환합니다.

폼 헬퍼의 `submit` 메서드는 HTTP 메서드와 URL 지정이 필요 없어졌으며, 대신 Inertia의 [방문 옵션들](https://inertiajs.com/manual-visits)을 단 하나의 인수로 받습니다. 예제와는 달리 `submit` 메서드는 Promise를 반환하지 않으며, 대신 Inertia가 지원하는 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 방문 옵션에 지정할 수 있습니다:

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

Laravel Precognition을 사용하면 Alpine 애플리케이션에서도 검증 규칙 중복 없이 라이브 검증 경험을 제공할 수 있습니다. 작동 방식을 설명하기 위해 새 사용자 생성을 위한 폼을 만들어 보겠습니다.

먼저, 라우트에 Precognition 활성화를 위해 `HandlePrecognitiveRequests` 미들웨어를 추가하세요. 이 라우트에서 사용할 검증 규칙을 담을 [폼 요청](/docs/12.x/validation#form-request-validation)도 만들어야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

이후, Alpine용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치하세요:

```shell
npm install laravel-precognition-alpine
```

필요하면 `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록합니다:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Laravel Precognition 패키지를 설치하고 등록한 후, `$form` "매직"을 사용해 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 전달하여 폼 객체를 생성할 수 있습니다.

라이브 검증을 활성화하려면 폼 데이터를 관련 입력에 바인딩하고, 각 입력의 `change` 이벤트를 청취하세요. `change` 이벤트 핸들러에서 폼의 `validate` 메서드에 입력 이름을 넘겨 호출합니다:

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

사용자가 폼을 작성하면, 폼 요청 검증 규칙에 따라 Precognition이 라이브 검증 결과를 제공합니다. 각 입력이 변경될 때마다 디바운스된 Precognitive 검증 요청이 Laravel 백엔드로 전송됩니다. 디바운스 타임아웃은 폼의 `setValidationTimeout` 함수로 조정하세요:

```js
form.setValidationTimeout(3000);
```

검증 요청이 진행되는 동안 폼의 `validating` 속성은 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

검증 요청이나 폼 제출 시 반환된 모든 오류가 폼의 `errors` 객체에 자동으로 채워집니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 오류가 있는지 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

입력이 통과했는지 실패했는지는 `valid` 와 `invalid` 함수에 입력 이름을 전달해 판단할 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력 상태는 한 번 변경되고 검증 응답이 도착한 이후에야 valid 혹은 invalid로 표시됩니다.

입력의 `change` 이벤트에 묶어 개별 입력을 검증할 수도 있지만, 아직 상호작용하지 않은 입력을 검증해야 할 수도 있습니다. 특히 "마법사형" UI 구현 시, 사용자가 조작하지 않은 입력이라도 모두 검증한 후 다음 단계로 진행하는 경우가 그렇습니다.

이럴 때는 `validate` 메서드를 호출하며 `only` 옵션에 검증할 필드명을 배열로 전달하고, `onSuccess` 또는 `onValidationError` 콜백으로 결과를 받으세요:

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

폼 제출 요청이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 다시 채우기

위 예제의 사용자 생성 폼에서는 Precognition으로 라이브 검증을 하지만, 전통적인 서버 측 폼 제출도 수행합니다. 따라서 서버에서 반환된 "old" 입력값과 검증 오류로 폼을 채워야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는 XHR을 통해 폼을 제출하려면 폼의 `submit` 함수(Axios 요청 프로미스 반환)를 사용할 수 있습니다:

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
### Axios 설정하기 (Configuring Axios)

Precognition 검증 라이브러리는 HTTP 요청을 보내기 위해 [Axios](https://github.com/axios/axios) 클라이언트를 사용합니다. 필요에 따라 애플리케이션에 맞춰 Axios 인스턴스를 커스터마이징할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때, `resources/js/app.js` 파일에서 각 요청에 추가 헤더를 넣을 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 애플리케이션용으로 설정된 Axios 인스턴스가 있다면, Precognition에게 이 인스턴스를 사용하도록 알려줄 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia 특화 Precognition 라이브러리는 검증 요청에만 구성된 Axios 인스턴스를 사용합니다. 폼 제출은 항상 Inertia가 처리합니다.

<a name="customizing-validation-rules"></a>
## 검증 규칙 커스터마이징 (Customizing Validation Rules)

Precognitive 요청 중 실행할 검증 규칙을 커스터마이징하려면 요청의 `isPrecognitive` 메서드를 활용하세요.

예를 들어, 사용자 생성 폼에서는 비밀번호가 "유출되지 않은(uncompromised)" 상태인지 검증하는 규칙을 최종 폼 제출 시에만 적용한다고 가정해봅시다. Precognitive 검증 요청에서는 비밀번호가 필수이며 최소 8자라는 규칙만 검증하도록 조정할 수 있습니다. `isPrecognitive` 메서드를 사용해 폼 요청 내 검증 규칙을 커스터마이징할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * 요청에 적용할 검증 규칙 반환
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

기본적으로 Laravel Precognition은 precognitive 검증 요청 시 파일을 업로드하거나 검증하지 않습니다. 이는 큰 파일이 불필요하게 여러 번 업로드되는 것을 방지하기 위한 조치입니다.

이 때문에, 설정한 폼 요청에서 [검증 규칙 커스터마이징](#customizing-validation-rules)을 통해 해당 필드(예: 파일)가 전체 폼 제출 시에만 필수임을 명시해줘야 합니다:

```php
/**
 * 요청에 적용할 검증 규칙 반환
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

모든 검증 요청마다 파일을 포함시키고 싶으면, 클라이언트 측 폼 인스턴스에서 `validateFiles` 함수를 호출할 수 있습니다:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리 (Managing Side-Effects)

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, 다른 미들웨어에서 발생하는 부수 효과 중 precognitive 요청 시 건너뛰어야 할 부분이 있는지 고려해야 합니다.

예를 들어, 사용자가 애플리케이션과 상호작용한 횟수를 증가시키는 미들웨어가 있지만, precognitive 요청은 상호작용으로 카운트하고 싶지 않을 수 있습니다. 이 경우, 미들웨어에서 `isPrecognitive` 메서드로 요청을 검사한 뒤 카운트를 증가시킬지 결정할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * 요청 처리
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

테스트에서 precognitive 요청을 만들고 싶다면, Laravel의 `TestCase`는 `withPrecognition` 헬퍼를 제공해 `Precognition` 요청 헤더를 자동으로 추가합니다.

또한, precognitive 요청이 성공했는지(즉, 검증 오류를 반환하지 않았는지) 확인하려면 응답 객체의 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:

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