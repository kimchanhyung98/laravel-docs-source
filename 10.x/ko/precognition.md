# Precognition

- [소개](#introduction)
- [실시간 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [Vue와 Inertia 사용하기](#using-vue-and-inertia)
    - [React 사용하기](#using-react)
    - [React와 Inertia 사용하기](#using-react-and-inertia)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [유효성 검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 향후의 HTTP 요청 결과를 미리 예측할 수 있게 해줍니다. Precognition의 주요 사용 사례 중 하나는 애플리케이션의 백엔드 유효성 검증 규칙을 중복 작성하지 않고도 프론트엔드 JavaScript 애플리케이션에서 “실시간” 유효성 검증 기능을 제공하는 것입니다. Precognition은 특히 Laravel의 Inertia 기반 [스타터 키트](/docs/10.x/starter-kits)와 잘 어울립니다.

Laravel이 "precognitive request"를 받으면 해당 라우트의 모든 미들웨어를 실행하고 라우트의 컨트롤러 의존성을 해결하며, 이 과정에서 [폼 요청](/docs/10.x/validation#form-request-validation) 유효성 검증도 수행하지만, 실제로는 라우트의 컨트롤러 메서드는 실행하지 않습니다.

<a name="live-validation"></a>
## 실시간 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기 (Using Vue)

Laravel Precognition을 사용하면 프론트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복 작성하지 않고도 실시간 유효성 검증 기능을 제공할 수 있습니다. 예시로, 애플리케이션 내 신규 사용자 생성 폼을 만들어 보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트에 추가해야 합니다. 그리고 라우트의 유효성 검증 규칙을 담을 [폼 요청](/docs/10.x/validation#form-request-validation)을 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, NPM을 통해 Laravel Precognition의 Vue용 프론트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-vue
```

Laravel Precognition 패키지가 설치되면, 이제 `useForm` 함수를 사용해 폼 객체를 생성하세요. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 그리고 초기 폼 데이터를 전달합니다.

그다음, 각 입력 필드의 `change` 이벤트에서 폼의 `validate` 메서드를 호출해 실시간 유효성 검증을 활성화합니다. 이때 `validate` 함수에 검증할 입력 필드의 이름을 넘기면 됩니다:

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

이제 사용자가 폼에 입력하면서 `change` 이벤트가 발생할 때마다 Precognition이 폼 요청에 정의된 유효성 검증 규칙에 따라 실시간 결과를 알려줍니다. 이러한 검증 요청은 디바운스(debounce, 지연 처리) 되어 서버에 과도한 요청이 가지 않도록 합니다. 디바운스 타임아웃은 `setValidationTimeout` 함수를 호출하여 조절할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```

검증 요청이나 폼 제출 도중 반환된 유효성 검증 오류는 자동으로 폼의 `errors` 객체에 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼이 오류를 가지고 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

입력값이 유효한지 또는 유효하지 않은지 여부는 각각 `valid`와 `invalid` 함수에 입력 필드의 이름을 전달하여 판단할 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]  
> 입력 필드는 변경되어 검증 응답이 도착한 이후에야 유효하거나 유효하지 않음이 표시됩니다.

만약 폼 입력값 중 일부만 검증하고자 할 때는 오류를 수동으로 지우는 것이 유용할 수 있습니다. `forgetError` 메서드를 사용하면 특정 필드의 오류 정보를 초기화할 수 있습니다:

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

폼 제출 응답에 따라 코드 실행도 가능합니다. `submit` 함수는 Axios 요청 프로미스를 반환하므로, 성공 시 폼 초기화, 실패 시 오류 알림 등을 편리하게 수행할 수 있습니다:

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

폼 제출 요청이 진행 중인지 여부는 `processing` 속성으로 확인하세요:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
### Vue와 Inertia 사용하기 (Using Vue and Inertia)

> [!NOTE]  
> Vue와 Inertia로 Laravel 애플리케이션을 개발할 때 빠르게 시작하고 싶다면, Laravel의 [스타터 키트](/docs/10.x/starter-kits)를 이용해 보세요. 스타터 키트는 백엔드와 프론트엔드 인증 스캐폴딩을 제공합니다.

Vue와 Inertia 함께 사용할 경우, 먼저 [Vue 사용법](#using-vue)을 참고하세요. Inertia에 맞춘 Precognition 라이브러리는 NPM을 통해 별도로 설치해야 합니다:

```shell
npm install laravel-precognition-vue-inertia
```

설치 후 `useForm` 함수는 위에서 설명한 유효성 검증 기능이 추가된 Inertia [form helper](https://inertiajs.com/forms#form-helper)를 반환합니다.

`submit` 메서드는 HTTP 메서드나 URL을 지정할 필요가 없고, 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫 번째이자 유일한 인자로 받습니다. 또한, `submit`은 Vue 예제처럼 Promise를 반환하지 않고, 대신 Inertia가 지원하는 여러 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 visit 옵션에 지정할 수 있습니다:

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

Laravel Precognition을 사용하면 프론트엔드 React 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 실시간 검증 기능을 제공할 수 있습니다. 사례로 사용자 생성 폼을 만들어보겠습니다.

우선, 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가해 Precognition을 활성화해야 합니다. 그리고 라우트의 유효성 검증 규칙을 담을 [폼 요청](/docs/10.x/validation#form-request-validation)을 생성하세요:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

NPM을 통해 React용 Laravel Precognition 프론트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-react
```

설치가 완료되면 `useForm` 함수를 사용해 폼 객체를 생성하세요. HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 인자로 전달합니다.

실시간 유효성 검증을 활성화하려면 각 입력 필드의 `change`와 `blur` 이벤트를 감지해야 합니다. `change` 이벤트 핸들러에서는 `setData` 메서드를 호출하여 폼 데이터를 업데이트하고, `blur` 이벤트 핸들러에서는 해당 입력 이름을 인수로 `validate` 메서드를 호출합니다:

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
            <label for="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label for="email">Email</label>
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

사용자가 입력할 때마다, Precognition은 폼 요청에 정의된 유효성 규칙에 따라 실시간 검증 결과를 제공합니다. 변경 이벤트 발생 시 디바운스된 “precognitive” 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 다음과 같이 조절할 수 있습니다:

```js
form.setValidationTimeout(3000);
```

검증 요청이 실행 중이면 `validating` 속성은 `true`가 됩니다:

```jsx
{form.validating && <div>Validating...</div>}
```

검증 요청이나 폼 제출 중 반환된 오류는 자동으로 `errors` 객체에 채워집니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 오류가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

유효 여부 판단은 `valid`와 `invalid` 함수에 입력 이름을 전달해 할 수 있습니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]  
> 입력값은 한 번이라도 바뀌어 검증 응답이 와야만 유효 또는 유효하지 않음 상태로 보여집니다.

일부 입력값에 대해서만 유효성 검증을 하고 싶을 때는 `forgetError` 함수를 사용해 오류를 수동으로 지울 수 있습니다:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => 
        form.setData('avatar', e.target.value);

        form.forgetError('avatar');
    }
>
```

폼 제출 시 액션도 지정할 수 있습니다. `submit`은 Axios 요청 프로미스를 반환하므로, 성공 시 폼을 초기화하거나 실패 시 알림을 띄우는 용도로 편리합니다:

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

진행 중인 폼 제출 요청 여부는 `processing` 속성으로 확인하세요:

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
### React와 Inertia 사용하기 (Using React and Inertia)

> [!NOTE]  
> React와 Inertia를 사용해 Laravel 애플리케이션을 빠르게 개발하고 싶으면, [스타터 키트](/docs/10.x/starter-kits)를 활용해 보세요. 백엔드, 프론트엔드 인증 스캐폴딩을 제공합니다.

Precognition을 React와 Inertia에서 함께 사용하기 전에 [React 사용법](#using-react)을 먼저 참고하세요. React용 Inertia 호환 Precognition 라이브러리는 NPM을 통해 별도 설치해야 합니다:

```shell
npm install laravel-precognition-react-inertia
```

설치 후, `useForm` 함수는 앞서 설명한 검증 기능이 추가된 Inertia [form helper](https://inertiajs.com/forms#form-helper)를 반환합니다.

`submit` 메서드는 HTTP 메서드나 URL 지정 없이, 대신 Inertia의 [visit 옵션](https://inertiajs.com/manual-visits)을 첫번째이자 유일한 인자로 받습니다. 또한, React 예제와 달리 Promise를 반환하지 않습니다. 대신 `submit` 메서드에 제공된 visit 옵션에 Inertia가 지원하는 여러 [이벤트 콜백](https://inertiajs.com/manual-visits#event-callbacks)을 등록할 수 있습니다:

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

Laravel Precognition을 사용하면 Alpine 프론트엔드 애플리케이션에서 유효성 검증 규칙을 중복하지 않고 실시간 유효성 검증 기능을 제공할 수 있습니다. 예시로 사용자 생성 폼을 만들어 보겠습니다.

라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 추가하세요. 폼 요청을 만들어 검증 규칙을 정의해야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

NPM으로 Alpine용 Laravel Precognition 프론트엔드 헬퍼를 설치합니다:

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록하세요:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

이제 Laravel Precognition이 설치되고 등록되었으니, `$form` 매직 헬퍼를 사용해 폼 객체를 만듭니다. HTTP 메서드(`post`), 타깃 URL(`/users`), 초기 폼 데이터를 전달하세요.

실시간 유효성 검증은 각 입력값에 `x-model`로 바인딩하고, `change` 이벤트에 `validate` 메서드를 호출하면 활성화됩니다:

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

사용자가 입력하면, Precognition이 폼 요청에 설정된 유효성 규칙에 따라 실시간 검증 결과를 만들어 줍니다. 입력이 바뀔 때마다 디바운스된 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃 변경은 `setValidationTimeout`으로 가능합니다:

```js
form.setValidationTimeout(3000);
```

검증 요청 진행 중이면 `validating` 속성이 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

검증 요청이나 폼 제출 중 반환된 오류들은 자동으로 `errors` 객체에 채워집니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

오류 존재 여부는 `hasErrors` 속성으로 확인하세요:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

각 입력값이 통과했는지 실패했는지는 `valid` / `invalid` 함수에 입력 이름을 전달해 판단할 수 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]  
> 입력값 상태는 최소한 한 차례 변경되어 검증 결과가 도착한 이후에만 유효/유효하지 않음으로 표시됩니다.

폼 제출 요청이 진행 중인지를 확인하려면 `processing` 속성을 보세요:

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 재설정하기

위 예시처럼 Precognition으로 실시간 유효성 검증만 하고, 폼 제출은 전통적인 서버 제출 방식이라면, 서버에서 반환된 "old" 입력값과 유효성 오류를 다시 폼에 채워야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

만약 XHR 방식을 통한 폼 제출을 원한다면, `submit` 함수가 Axios 요청 프로미스를 반환하므로 이를 활용하세요:

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

Precognition 검증 라이브러리는 HTTP 요청을 보내기 위해 [Axios](https://github.com/axios/axios) 클라이언트를 사용합니다. 필요하다면 애플리케이션 요구에 맞게 Axios 인스턴스를 설정할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때는 `resources/js/app.js`에서 모든 요청에 추가 헤더를 설정할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 애플리케이션에 Axios 인스턴스가 설정되어 있다면, Precognition에 해당 인스턴스를 사용하도록 지시할 수도 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]  
> Inertia 버전의 Precognition 라이브러리는 검증 요청에는 구성된 Axios 인스턴스를 사용하지만, 폼 제출 요청은 항상 Inertia가 처리합니다.

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이징 (Customizing Validation Rules)

precognitive 요청 시 실행되는 유효성 검증 규칙을 `isPrecognitive` 메서드를 사용해 조건에 따라 바꿀 수 있습니다.

예를 들어, 회원가입 폼에서는 최종 제출 시에만 비밀번호가 “uncompromised” (안전한지 검사) 되어야 할 수 있습니다. Precognition 검증 요청 시에는 비밀번호가 필수이고 최소 8자임만 확인하도록 할 수 있습니다. 폼 요청에서 `isPrecognitive`를 활용해 다음과 같이 규칙을 정의할 수 있습니다:

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

기본적으로, Precognition은 파일을 업로드하거나 precognitive 검증 요청 시 파일 유효성 검증을 수행하지 않습니다. 이는 큰 파일을 여러 번 불필요하게 전송하는 문제를 피하려는 목적입니다.

따라서 관련 폼 요청의 유효성 검증 규칙을 [커스터마이징](#customizing-validation-rules)하여, 해당 필드는 전체 폼 제출 시에만 `required`하도록 설정하는 것이 좋습니다:

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

만약 모든 검증 요청에 파일도 포함시키고 싶다면, 클라이언트 쪽 폼 인스턴스에서 `validateFiles` 메서드를 호출하세요:

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리 (Managing Side-Effects)

`HandlePrecognitiveRequests` 미들웨어를 라우트에 추가할 때, 다른 미들웨어에서 발생하는 부수 효과 중에 precognitive 요청에선 생략해야 할 부분이 있는지 고려하세요.

예를 들어, 사용자 상호작용 횟수를 누적하는 미들웨어가 있다고 할 때, precognitive 요청만 제외하고 싶을 수 있습니다. 이럴 경우 `isPrecognitive` 메서드를 사용해 조건문으로 처리하세요:

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

테스트에서 precognitive 요청을 만들려면 Laravel의 `TestCase`는 `withPrecognition` 헬퍼를 제공합니다. 이 헬퍼는 `Precognition` 요청 헤더를 자동 추가합니다.

또한, precognitive 요청이 성공했는지 (즉, 유효성 오류가 없는지) 검증하려면 응답에 대해 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:

```php
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