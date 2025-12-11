# 프리코그니션 (Precognition)

- [소개](#introduction)
- [실시간 유효성 검증](#live-validation)
    - [Vue 사용하기](#using-vue)
    - [React 사용하기](#using-react)
    - [Alpine과 Blade 사용하기](#using-alpine)
    - [Axios 설정하기](#configuring-axios)
- [유효성 검증 규칙 커스터마이징](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [부수 효과 관리](#managing-side-effects)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Precognition은 미래의 HTTP 요청 결과를 미리 예측할 수 있도록 해줍니다. Precognition의 주요 활용 사례 중 하나는 프론트엔드 JavaScript 애플리케이션에서 백엔드 유효성 검증 규칙을 중복 정의하지 않고도 "실시간" 유효성 검증을 제공할 수 있다는 점입니다.

Laravel이 "precognitive request(프리코그니션 요청)"를 받으면, 해당 라우트의 모든 미들웨어를 실행하고, 컨트롤러의 의존성도 해석하며, [폼 요청](/docs/12.x/validation#form-request-validation) 유효성 검증도 진행합니다. 그러나 실제로 컨트롤러 메서드는 실행하지 않습니다.

> [!NOTE]
> Inertia 2.3부터 Precognition 지원이 기본 내장되어 있습니다. 자세한 내용은 [Inertia Forms 문서](https://inertiajs.com/docs/v2/the-basics/forms)를 참고하세요. 이전 Inertia 버전은 Precognition 0.x가 필요합니다.

<a name="live-validation"></a>
## 실시간 유효성 검증 (Live Validation)

<a name="using-vue"></a>
### Vue 사용하기

Laravel Precognition을 사용하면, 프론트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 예시로, 새로운 사용자를 생성하는 폼을 만들어보겠습니다.

먼저, Precognition을 라우트에서 활성화하려면, 라우트 정의에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 또한, 해당 라우트의 유효성 검증 규칙을 담을 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, NPM을 사용하여 Vue용 Laravel Precognition 프런트엔드 헬퍼를 설치합니다.

```shell
npm install laravel-precognition-vue
```

이제 Precognition 패키지를 설치했으므로, Precognition의 `useForm` 함수를 사용해 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 그리고 초기 폼 데이터를 제공합니다.

실시간 유효성 검증을 활성화하려면, 각 입력 요소의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하고, 입력의 이름을 전달하면 됩니다.

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

이제 사용자가 폼을 채워나가면, Precognition이 해당 라우트의 폼 요청에 정의된 유효성 검증 규칙을 기반으로 실시간 유효성 검증 결과를 제공합니다. 입력값이 변경될 때마다 프리코그니션 유효성 검증 요청이 디바운스되어 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 폼의 `setValidationTimeout` 함수를 호출하여 조절할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다.

```html
<div v-if="form.validating">
    Validating...
</div>
```

유효성 검증 요청 또는 폼 제출 시 반환되는 모든 유효성 검증 오류는 자동으로 폼의 `errors` 객체에 할당됩니다.

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

폼에 어떤 오류라도 존재하는지 확인하려면, 폼의 `hasErrors` 속성을 사용할 수 있습니다.

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

또한, 각각의 입력값이 유효성 검증에 통과했는지(`valid`) 혹은 실패했는지(`invalid`)도 입력 이름을 전달하여 판별할 수 있습니다.

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 폼 입력값이 변경되고 유효성 검증 응답이 도착해야만 해당 입력값이 유효 혹은 무효 상태로 표시됩니다.

Precognition으로 폼의 일부 입력값만 검증할 때는, 오류를 수동으로 지워주는 것이 필요할 수 있습니다. 이때는 폼의 `forgetError` 함수를 사용할 수 있습니다.

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

위와 같이, 입력의 `change` 이벤트에 연결하여 사용자가 입력에 반응할 때마다 개별 입력값을 검증할 수 있습니다. 그러나, 아직 사용자가 직접 입력하지 않은 값도 검증해야 할 때가 있습니다. 예를 들어, "위자드(wizard)"처럼 다음 단계로 넘어가기 전에 모든 보이는 입력값을 검증하고자 할 때 흔히 발생합니다.

이럴 때 Precognition에서는, `validate` 메서드에 검증하고자 하는 필드 이름들을 `only` 옵션으로 전달하면 됩니다. 결과 처리 시 `onSuccess`, `onValidationError` 콜백을 활용할 수 있습니다.

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

물론, 폼 제출에 대한 응답을 받고 추가 로직을 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프라미스를 반환하므로, 응답 데이터를 참조하거나, 성공 시 입력값을 초기화하거나, 실패한 요청을 처리할 수 있습니다.

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

폼 제출 요청이 진행 중인지 확인하려면 폼의 `processing` 속성을 확인하면 됩니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-react"></a>
### React 사용하기

Laravel Precognition을 활용하면 프론트엔드 React 애플리케이션에서 유효성 검증 규칙을 중복하지 않고도 사용자에게 실시간 유효성 검증 경험을 제공할 수 있습니다. 새로운 사용자를 생성하는 폼을 예시로 알아보겠습니다.

먼저 Precognition을 라우트에 적용하려면, 해당 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 하며, 라우트의 유효성 검증 규칙을 담을 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 만듭니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

다음으로, React용 Laravel Precognition 프론트엔드 헬퍼를 NPM으로 설치합니다.

```shell
npm install laravel-precognition-react
```

Precognition 패키지를 설치한 후에는, Precognition의 `useForm` 함수를 사용하여 폼 객체를 생성할 수 있습니다. HTTP 메서드(`post`), 대상 URL(`/users`), 그리고 초기 폼 데이터를 전달합니다.

실시간 유효성 검증을 위해 각 입력값의 `change`, `blur` 이벤트를 리스닝해야 합니다. `change` 이벤트 핸들러에서는 `setData` 함수를 사용하여 입력값을 갱신하고, `blur` 이벤트에서는 `validate` 메서드를 호출해 입력값의 이름을 전달합니다.

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

이제, 사용자가 폼을 작성하면 라우트의 폼 요청에 정의된 유효성 검증 규칙을 기반으로 Precognition이 실시간 유효성 검증을 제공합니다. 입력값이 바뀔 때마다, 디바운스된 프리코그니션 유효성 검증 요청이 Laravel 애플리케이션으로 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 조정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행되는 동안에는, 폼의 `validating` 속성이 `true`로 설정됩니다.

```jsx
{form.validating && <div>Validating...</div>}
```

검증 요청 또는 폼 전송 중 반환된 유효성 검증 오류는 자동으로 폼의 `errors` 객체에 할당됩니다.

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

폼에 어떤 오류라도 존재하는지 확인하려면, 폼의 `hasErrors` 속성을 사용할 수 있습니다.

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

개별 입력값이 통과했는지(`valid`) 혹은 실패했는지(`invalid`)도 해당 입력 이름을 인자로 넘겨 판별할 수 있습니다.

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 폼 입력값이 변경되고 유효성 검증 응답이 도착해야만 해당 입력값이 유효 혹은 무효 상태로 표시됩니다.

Precognition으로 폼의 일부 입력값만 검증할 때는, 오류를 수동으로 지워주는 것이 필요할 수 있습니다. 이때는 폼의 `forgetError` 함수를 사용할 수 있습니다.

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.files[0]);

        form.forgetError('avatar');
    }}
>
```

입력의 `blur` 이벤트에 연결하여 사용자가 직접 입력에 반응할 때마다 개별 입력값을 검증할 수 있지만, 아직 직접 입력하지 않은 값도 검증이 필요할 때가 있습니다. 예를 들어, "위자드(wizard)" 구조로 다음 단계로 이동하기 전에 모든 보이는 입력값을 검증하고 싶을 때가 있습니다.

이럴 때 Precognition에서는, `validate` 메서드에 검증하고자 하는 필드 이름들을 `only` 옵션으로 전달하면 됩니다. 결과 처리 시 `onSuccess`, `onValidationError` 콜백으로 처리할 수 있습니다.

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

또한 폼 제출 응답에 따라 추가 코드를 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프라미스를 반환하므로, 응답 데이터 접근, 성공 시 입력값 초기화, 실패 처리 등에 활용할 수 있습니다.

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

폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성을 통해 확인할 수 있습니다.

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-alpine"></a>
### Alpine과 Blade 사용하기

Laravel Precognition을 사용하면 Alpine 기반 프론트엔드 애플리케이션에서도 유효성 검증 규칙을 중복하지 않고 실시간 유효성 검증을 제공할 수 있습니다. 예시로, 새로운 사용자를 생성하는 폼을 만들어보겠습니다.

먼저 Precognition을 라우트에서 활성화하려면, 해당 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가하고, 검증 규칙을 담은 [폼 요청](/docs/12.x/validation#form-request-validation) 클래스를 만듭니다.

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

그 다음, NPM을 사용하여 Alpine용 Laravel Precognition 프론트엔드 헬퍼를 설치합니다.

```shell
npm install laravel-precognition-alpine
```

그리고 `resources/js/app.js` 파일에서 아래와 같이 Precognition 플러그인을 Alpine에 등록합니다.

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

이제 Precognition 패키지가 설치되고 등록되었으니, Precognition의 `$form` "매직"을 활용해 폼 객체를 생성할 수 있습니다. HTTP 메서드(`post`), 대상 URL(`/users`), 그리고 초기 폼 데이터를 전달합니다.

실시간 유효성 검증을 활성화하려면, 입력값과 폼 데이터를 바인딩한 후, 각 입력의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하고 입력 이름을 전달하면 됩니다.

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

이렇게 하면, 사용자가 폼을 작성해나갈 때 Precognition이 해당 라우트 폼 요청에 정의된 유효성 검증 규칙을 기반으로 실시간 결과를 제공합니다. 입력값이 변경될 때마다 프리코그니션 유효성 검증 요청이 디바운스되어 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 조정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다.

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

검증 요청이나 폼 제출에서 반환된 유효성 검증 오류는 자동으로 폼의 `errors` 객체에 할당됩니다.

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

폼에 어떤 오류라도 존재하는지 확인하려면, 폼의 `hasErrors` 속성을 사용할 수 있습니다.

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

특정 입력값이 통과했는지(`valid`) 혹은 실패했는지(`invalid`)는 입력 이름을 인자로 넘겨 확인할 수 있습니다.

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력값이 변경된 후 유효성 검증 응답이 도착해야 유효 및 무효로 표시됩니다.

이처럼 입력의 `change` 이벤트에 연결해 사용자가 직접 입력할 때마다 검증할 수 있지만, 사용자가 아직 입력하지 않은 값도 검증해야 할 때가 있습니다. 예를 들어, "위자드(wizard)" 구조로 다음 단계로 이동하기 전에 모든 보이는 입력값을 검증하고 싶을 때가 그렇습니다.

이런 경우 Precognition의 `validate` 메서드에 검증하고자 하는 필드 이름을 `only` 옵션으로 전달하여 활용할 수 있습니다. 결과 처리는 `onSuccess`와 `onValidationError` 콜백으로 할 수 있습니다.

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

폼 제출 요청이 진행 중인지 확인하려면 폼의 `processing` 속성을 참고하세요.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 자동 채우기 (Repopulating Old Form Data)

위에서 설명한 예시에서는 Precognition을 사용해 실시간 유효성 검증을 수행하지만, 실제 폼 제출은 기존의 서버 사이드 폼 제출 방식을 따릅니다. 이 경우 서버에서 반환된 "old" 입력값과 유효성 검증 오류로 폼이 다시 채워져야 합니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

또는, XHR로 폼을 전송하고 싶으면 폼의 `submit` 함수를 사용하세요. 이 함수는 Axios 요청 프라미스를 반환합니다.

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

Precognition 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용해 백엔드로 요청을 보냅니다. 필요시, 애플리케이션에 맞게 Axios 인스턴스를 커스터마이징할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때 `resources/js/app.js`에서 추가 헤더를 설정할 수 있습니다.

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

이미 커스텀 Axios 인스턴스를 사용하는 경우라면, Precognition에서 해당 인스턴스를 사용할 수도 있습니다.

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

<a name="customizing-validation-rules"></a>
## 유효성 검증 규칙 커스터마이징 (Customizing Validation Rules)

프리코그니션 요청에 대해 실행되는 유효성 검증 규칙을 커스터마이징하려면, 요청의 `isPrecognitive` 메서드를 활용할 수 있습니다.

예를 들어, 사용자 생성 폼에서는 최종 폼 제출 시에만 비밀번호가 "uncompromised(유출되지 않음)" 여부를 검사하고 싶을 수 있습니다. 프리코그니션 유효성 검증 요청에서는 비밀번호 필수 및 최소 8자만 체크하도록 규칙을 다르게 정의할 수 있습니다. 이를 `isPrecognitive` 메서드를 활용해 쉽게 구현할 수 있습니다.

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

기본적으로 Laravel Precognition은 프리코그니션 유효성 검증 요청 중에는 파일을 업로드하거나 검증하지 않습니다. 이는 대용량 파일이 불필요하게 여러 번 업로드되는 일을 막기 위함입니다.

이러한 동작 때문에, 애플리케이션에서는 [해당 폼 요청의 유효성 검증 규칙을 커스터마이징](#customizing-validation-rules)하여, 전체 폼 제출 시에만 파일 필드가 필수임을 명시해야 합니다.

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

프리코그니션 요청에서도 파일을 포함시키고 싶다면, 클라이언트 측 폼 인스턴스에서 `validateFiles` 함수를 호출하면 됩니다.

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 부수 효과 관리 (Managing Side-Effects)

라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때, 프리코그니션 요청에서 _다른_ 미들웨어의 부수 효과를 건너뛰는 것이 적절한지 반드시 고려해야 합니다.

예를 들어, 사용자가 애플리케이션을 사용할 때마다 "interactions(상호작용)" 횟수를 기록하는 미들웨어가 있다고 가정합시다. 프리코그니션 요청은 실제 사용과 무관하므로 이 횟수에 집계되지 않도록 하는 것이 좋습니다. 이를 위해 요청의 `isPrecognitive` 메서드를 체크하여 집계 로직을 분기할 수 있습니다.

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

테스트 코드에서 프리코그니션 요청을 만들고 싶다면, Laravel의 `TestCase`에 포함된 `withPrecognition` 헬퍼를 사용할 수 있습니다. 이 헬퍼는 요청에 `Precognition` 요청 헤더를 추가해줍니다.

또한, 프리코그니션 요청이 성공적으로 처리(즉, 유효성 검증 오류가 없었음)되었는지 확인하려면, 응답에 있는 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다.

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
