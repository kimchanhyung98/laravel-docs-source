# 로컬라이제이션

- [소개](#introduction)
    - [로케일 설정](#configuring-the-locale)
- [번역 문자열 정의](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열의 파라미터 치환](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이딩](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

Laravel의 로컬라이제이션 기능은 다양한 언어의 문자열을 손쉽게 가져올 수 있는 방법을 제공하여, 애플리케이션에서 여러 언어를 쉽게 지원할 수 있게 해줍니다.

Laravel은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째로, 언어 문자열은 `resources/lang` 디렉터리 내의 파일에 저장될 수 있습니다. 이 디렉터리 내에는 애플리케이션에서 지원하는 각 언어별로 하위 디렉터리가 존재할 수 있습니다. 이 방식은 Laravel이 내장 기능(예: 유효성 검사 오류 메시지)의 번역 문자열을 관리하는데 사용하는 방식입니다:

    /resources
        /lang
            /en
                messages.php
            /es
                messages.php

또는, 번역 문자열을 `resources/lang` 디렉터리에 위치한 JSON 파일 내에 정의할 수도 있습니다. 이 경우, 애플리케이션에서 지원하는 각 언어마다 해당하는 JSON 파일을 이 디렉터리 내에 생성해야 합니다. 이 방식은 번역해야 할 문자열이 많은 애플리케이션에 추천됩니다:

    /resources
        /lang
            en.json
            es.json

이 문서에서는 번역 문자열을 관리하는 각 방법에 대해 다룹니다.

<a name="configuring-the-locale"></a>
### 로케일 설정

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장되어 있습니다. 이 값은 애플리케이션 요구에 맞게 자유롭게 수정할 수 있습니다.

HTTP 요청 한 건에 대해 런타임에서 기본 언어를 변경하고 싶다면, `App` 파사드가 제공하는 `setLocale` 메서드를 사용할 수 있습니다:

    use Illuminate\Support\Facades\App;

    Route::get('/greeting/{locale}', function ($locale) {
        if (! in_array($locale, ['en', 'es', 'fr'])) {
            abort(400);
        }

        App::setLocale($locale);

        //
    });

또한, 활성화된 언어에 원하는 번역 문자열이 포함되어 있지 않을 때 사용할 "폴백 언어"(fallback language)를 설정할 수 있습니다. 폴백 언어 역시 `config/app.php` 설정 파일에서 지정합니다:

    'fallback_locale' => 'en',

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인

현재 로케일을 확인하거나, 특정 값과 일치하는지 확인하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

    use Illuminate\Support\Facades\App;

    $locale = App::currentLocale();

    if (App::isLocale('en')) {
        //
    }

<a name="defining-translation-strings"></a>
## 번역 문자열 정의

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로 번역 문자열은 `resources/lang` 디렉터리 내의 파일에 저장됩니다. 이 디렉터리 내에는 애플리케이션에서 지원하는 각 언어별로 하위 디렉터리가 있어야 합니다. 이 방식은 Laravel이 내장 기능(예: 유효성 검사 오류 메시지)의 번역 문자열을 관리하는 방식입니다:

    /resources
        /lang
            /en
                messages.php
            /es
                messages.php

모든 언어 파일은 키가 할당된 문자열의 배열을 반환합니다. 예를 들어:

    <?php

    // resources/lang/en/messages.php

    return [
        'welcome' => 'Welcome to our application!',
    ];

> {note} 지역에 따라 구분되는 언어의 경우, ISO 15897 규격에 따라 언어 디렉터리 이름을 지정해야 합니다. 예를 들어, 영국 영어의 경우 "en_GB"를 사용해야 하며, "en-gb"는 사용하지 않아야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역해야 할 문자열이 많은 애플리케이션의 경우, 모든 문자열을 "짧은 키"로 정의하는 것은 뷰에서 키를 참조할 때 혼란을 초래할 수 있고, 모든 번역 문자열마다 키를 만들어야 하는 번거로움이 있습니다.

이런 이유로 Laravel은 문자열의 "기본" 번역 자체를 키로 사용하여 번역 문자열을 정의하는 방식을 지원합니다. 이 방식은 `resources/lang` 디렉터리 내의 JSON 파일로 번역 문자열을 관리합니다. 예를 들어, 스페인어 번역이 필요한 경우 `resources/lang/es.json` 파일을 생성해야 합니다:

```js
{
    "I love programming.": "Me encanta programar."
}
```

#### 키와 파일명 충돌

다른 번역 파일명과 충돌하는 번역 문자열 키를 정의해서는 안 됩니다. 예를 들어, "NL" 로케일에서 `__('Action')`을 번역하려고 할 때 `nl/action.php` 파일은 존재하지만, `nl.json` 파일이 존재하지 않으면, 번역기는 `nl/action.php`의 내용을 반환합니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

언어 파일에서 번역 문자열을 가져오려면 `__` 헬퍼 함수를 사용할 수 있습니다. 번역 문자열을 "짧은 키"로 정의한 경우에는 파일명과 키를 "닷(dot)" 표기법을 사용하여 `__` 함수에 전달합니다. 예를 들어, `resources/lang/en/messages.php` 언어 파일에서 `welcome` 번역 문자열을 가져오려면:

    echo __('messages.welcome');

지정한 번역 문자열이 존재하지 않으면, `__` 함수는 원래 전달받은 번역 문자열 키를 반환합니다. 즉, 위 예제에서 번역이 없다면 `__` 함수는 `messages.welcome`을 반환합니다.

[기본 번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)에는 문자열의 기본 번역 자체를 `__` 함수에 전달하면 됩니다:

    echo __('I love programming.');

마찬가지로, 번역 문자열이 없으면 `__` 함수는 전달받은 문자열을 그대로 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용하는 경우, `{{ }}` 출력 구문으로 번역 문자열을 쉽게 표시할 수 있습니다:

    {{ __('messages.welcome') }}

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열의 파라미터 치환

원한다면 번역 문자열에 플레이스홀더를 정의할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어, 다음과 같이 이름을 위한 플레이스홀더가 포함된 환영 메시지를 정의할 수 있습니다:

    'welcome' => 'Welcome, :name',

번역 문자열을 가져올 때 플레이스홀더를 치환하려면, 두 번째 인수로 치환할 값의 배열을 `__` 함수에 전달하면 됩니다:

    echo __('messages.welcome', ['name' => 'dayle']);

플레이스홀더가 모두 대문자이거나, 첫 글자만 대문자인 경우 번역된 값도 동일하게 대소문자가 적용됩니다:

    'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
    'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle

<a name="pluralization"></a>
### 복수형 처리

복수형 처리는 다양한 언어에서 복잡한 규칙이 있기 때문에 어려운 문제이지만, Laravel에서는 직접 정의한 복수형 규칙에 따라 문자열을 다르게 번역할 수 있습니다. `|` 문자로 단수와 복수형을 구분할 수 있습니다:

    'apples' => 'There is one apple|There are many apples',

물론, [번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)에도 복수형 처리가 가능합니다:

```js
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

값의 범위에 따라 더 복잡한 복수형 규칙을 정의할 수도 있습니다:

    'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',

복수형 옵션이 정의된 번역 문자열의 경우, 특정 "개수"에 맞는 문장을 가져오려면 `trans_choice` 함수를 사용합니다. 다음 예시에서 개수가 1보다 크므로 복수형 번역이 반환됩니다:

    echo trans_choice('messages.apples', 10);

복수형 문자열에도 플레이스홀더 속성을 정의할 수 있습니다. 이 플레이스홀더는 `trans_choice` 함수의 세 번째 인수로 배열을 전달해 치환할 수 있습니다:

    'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

    echo trans_choice('time.minutes_ago', 5, ['value' => 5]);

`trans_choice` 함수에 전달된 정수 값을 표시하려면 내장된 `:count` 플레이스홀더를 사용할 수 있습니다:

    'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이딩

일부 패키지는 자체 언어 파일을 포함하고 있을 수 있습니다. 이런 파일을 수정하려면, 패키지의 원본 파일을 직접 수정하는 대신, `resources/lang/vendor/{package}/{locale}` 디렉터리에 파일을 배치해서 오버라이드할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php`에서 영어 번역 문자열을 오버라이드하려면, `resources/lang/vendor/hearthfire/en/messages.php` 파일을 추가하면 됩니다. 이 파일 내에는 오버라이드하고자 하는 번역 문자열만 정의하면 됩니다. 오버라이드하지 않은 나머지 번역 문자열은 여전히 패키지의 원본 언어 파일에서 로드됩니다.