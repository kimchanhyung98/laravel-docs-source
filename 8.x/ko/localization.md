# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [로케일 설정하기](#configuring-the-locale)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열 자체를 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 불러오기](#retrieving-translation-strings)
    - [번역 문자열 내 매개변수 치환하기](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 덮어쓰기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

Laravel의 로컬라이제이션 기능은 여러 언어로 된 문자열을 쉽게 불러올 수 있게 하여, 애플리케이션 내에서 다국어 지원을 간편하게 구현할 수 있도록 도와줍니다.

Laravel은 번역 문자열을 관리하는 두 가지 방식을 제공합니다. 첫 번째는 `resources/lang` 디렉토리 내에 파일 형태로 문자열을 저장하는 방법입니다. 이 디렉토리 안에는 애플리케이션이 지원하는 각 언어별 하위 디렉토리가 존재할 수 있습니다. Laravel은 기본적으로 검증 오류 메시지와 같은 내장 기능의 번역 문자열을 이 방식을 통해 관리합니다:

```
/resources
    /lang
        /en
            messages.php
        /es
            messages.php
```

또 다른 방법은 JSON 파일을 `resources/lang` 디렉토리에 위치시키는 것입니다. 이때 모든 지원 언어별로 대응하는 JSON 파일이 이 디렉토리에 위치합니다. 애플리케이션에 번역할 문자열이 많을 경우 이 방식이 권장됩니다:

```
/resources
    /lang
        en.json
        es.json
```

본 문서에서 두 가지 방식 모두를 다루겠습니다.

<a name="configuring-the-locale"></a>
### 로케일 설정하기

애플리케이션의 기본 언어는 `config/app.php` 설정 파일 내 `locale` 옵션에 저장되어 있습니다. 필요에 따라 이 값을 자유롭게 변경할 수 있습니다.

런타임 중 단일 HTTP 요청에 대해 기본 언어를 변경하려면 `App` 파사드가 제공하는 `setLocale` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function ($locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    //
});
```

활성 언어에 번역 문자열이 없는 경우 사용될 "대체 언어(fallback language)"도 설정할 수 있습니다. 기본 언어와 마찬가지로 대체 언어는 `config/app.php` 설정 파일에서 구성합니다:

```
'fallback_locale' => 'en',
```

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인하기

`App` 파사드의 `currentLocale` 메서드로 현재 로케일을 확인하거나, `isLocale` 메서드를 사용해 특정 로케일인지 여부를 확인할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    //
}
```

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로 번역 문자열은 `resources/lang` 디렉토리 내 파일에 저장됩니다. 이 안에는 애플리케이션에서 지원하는 각 언어별 하위 디렉토리가 있어야 합니다. 이는 Laravel이 내장 기능인 검증 오류 메시지 등에서 번역 문자열을 관리하는 방식입니다:

```
/resources
    /lang
        /en
            messages.php
        /es
            messages.php
```

모든 언어 파일은 키가 지정된 문자열 배열을 반환합니다. 예를 들면:

```
<?php

// resources/lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!NOTE]
> 지역에 따라 구분되는 언어의 경우, 언어 디렉토리 이름은 ISO 15897 표준에 맞춰 지정해야 합니다. 예를 들어 영국 영어는 `en-gb`가 아닌 `en_GB`를 사용하세요.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열 자체를 키로 사용하기

번역 문자열이 많아지면 "짧은 키"를 일일이 정의하는 것이 뷰에서 키를 참조할 때 혼란스러울 수 있으며, 모든 문자열마다 키를 계속 만드는 게 번거로워집니다.

이 때문에 Laravel은 번역 문자열 자체의 "기본" 번역문을 키로 사용하는 방식을 지원합니다. 이 방법을 사용할 경우 JSON 파일을 `resources/lang` 디렉토리에 저장합니다. 예를 들어, 애플리케이션에 스페인어 번역이 있다면 `resources/lang/es.json` 파일을 생성해야 합니다:

```js
{
    "I love programming.": "Me encanta programar."
}
```

#### 키와 파일명 충돌 주의

번역 문자열 키는 다른 번역 파일명과 충돌하지 않아야 합니다. 예를 들어, `__('Action')`를 "NL" 로케일에 대해 번역하려 하는데, `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없으면, 번역기는 `nl/action.php`의 내용을 반환합니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 불러오기

`__` 헬퍼 함수를 사용해 번역 문자열을 언어 파일에서 불러올 수 있습니다. "짧은 키" 방식을 사용한다면 `__` 함수에 "점(dot)" 구문으로 파일명과 키를 전달해야 합니다. 예를 들어 `resources/lang/en/messages.php` 파일 내 `welcome` 번역 문자열을 불러오려면 다음과 같이 작성합니다:

```
echo __('messages.welcome');
```

지정한 번역 문자열이 없으면 `__` 함수는 키를 그대로 반환합니다. 위 예제에서는 번역이 없으면 `messages.welcome`을 반환합니다.

[번역 문자열 자체가 키인 경우](#using-translation-strings-as-keys)에는 기본 문자열을 `__` 함수에 전달해야 합니다:

```
echo __('I love programming.');
```

마찬가지로, 번역 문자열이 없으면 전달된 문자열 키를 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용하는 경우, `{{ }}` 출력 구문을 통해 번역 문자열을 출력할 수 있습니다:

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 매개변수 치환하기

번역 문자열에 플레이스홀더를 정의할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어 사용자 이름을 치환하는 환영 메시지는 다음과 같습니다:

```
'welcome' => 'Welcome, :name',
```

이 플레이스홀더를 치환하려면 `__` 함수에 두 번째 인수로 치환값 배열을 전달하세요:

```
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더가 모두 대문자이거나 첫 글자만 대문자일 경우, 치환되는 값도 그 형태에 맞게 대문자로 변환됩니다:

```
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="pluralization"></a>
### 복수형 처리

복수형 처리(pluralization)는 여러 언어마다 다양한 규칙이 있어 복잡하지만, Laravel은 사용자가 정의한 복수형 규칙에 따라 문자열을 다르게 번역하도록 도와줍니다. 싱글/플루럴 구분 문자열은 `|` 문자로 구분합니다:

```
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열 자체를 키로 사용할 때](#using-translation-strings-as-keys)도 복수형 처리가 지원됩니다:

```js
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

더 복잡한 복수형 규칙도 작성할 수 있는데, 다수 범위별로 번역 문자열을 지정할 수도 있습니다:

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형이 정의된 번역 문자열은 `trans_choice` 함수를 사용해 특정 개수(count)에 맞는 문자열을 가져옵니다. 예를 들어, 개수가 1보다 크므로 복수형이 반환됩니다:

```
echo trans_choice('messages.apples', 10);
```

복수형 문자열 내 플레이스홀더도 정의할 수 있고, 세 번째 인자로 값 배열을 넘겨 치환할 수 있습니다:

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice` 함수에 전달된 정수 값을 직접 출력하려면 내장 플레이스홀더 `:count`를 사용할 수 있습니다:

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 덮어쓰기

일부 패키지는 자체 언어 파일을 제공할 수 있습니다. 패키지 핵심 파일을 직접 수정하는 대신, `resources/lang/vendor/{package}/{locale}` 디렉토리에 파일을 두어 덮어쓸 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 영어 번역 문자열인 `messages.php`를 덮어써야 할 경우, `resources/lang/vendor/hearthfire/en/messages.php` 위치에 파일을 두면 됩니다. 이 파일에는 덮어쓰려는 번역 문자열만 정의하면 되며, 나머지 문자열은 패키지 원본 언어 파일에서 계속 로드됩니다.