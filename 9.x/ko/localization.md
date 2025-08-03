# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [로케일 구성하기](#configuring-the-locale)
    - [복수형 처리 언어](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 불러오기](#retrieving-translation-strings)
    - [번역 문자열 내 매개변수 치환하기](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이딩](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

Laravel의 로컬라이제이션 기능은 다양한 언어의 문자열을 편리하게 불러올 수 있게 하여, 애플리케이션에서 여러 언어를 쉽게 지원할 수 있도록 합니다.

Laravel은 번역 문자열을 관리하는 두 가지 방식을 제공합니다. 첫 번째는 `lang` 디렉토리 내에 번역 문자열을 파일로 저장하는 방식입니다. 이 디렉토리 안에는 애플리케이션에서 지원하는 각 언어마다 하위 디렉토리가 있을 수 있습니다. 이 방식은 Laravel이 기본 제공하는 검증 오류 메시지와 같은 기능들의 번역 문자열을 관리하는 기본 방식입니다:

```
/lang
    /en
        messages.php
    /es
        messages.php
```

또 다른 방법은 `lang` 디렉토리에 JSON 파일로 번역 문자열을 정의하는 것입니다. 이 방식은 애플리케이션에서 지원하는 각 언어마다 해당 언어 이름으로 된 JSON 파일이 존재합니다. 이렇게 하는 방법은 번역할 문자열이 많은 애플리케이션에 권장됩니다:

```
/lang
    en.json
    es.json
```

이 문서에서는 이러한 두 가지 번역 문자열 관리 방식을 각각 다루겠습니다.

<a name="configuring-the-locale"></a>
### 로케일 구성하기

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장됩니다. 애플리케이션의 요구에 맞게 이 값을 자유롭게 변경할 수 있습니다.

HTTP 요청 단위로 기본 언어를 변경하려면, `App` 파사드가 제공하는 `setLocale` 메서드를 런타임에 사용할 수 있습니다:

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

또한, 활성 언어에 특정 번역 문자열이 없을 경우 사용할 "대체(fallback) 언어"를 설정할 수 있습니다. 대체 언어는 기본 언어 설정과 마찬가지로 `config/app.php` 설정 파일에서 구성합니다:

```
'fallback_locale' => 'en',
```

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인하기

현재 로케일을 확인하거나 특정 로케일인지 검사하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    //
}
```

<a name="pluralization-language"></a>
### 복수형 처리 언어

Eloquent 등 프레임워크의 일부는 단수형 문자열을 복수형으로 변환하기 위해 Laravel의 "pluralizer"를 사용합니다. 기본값은 영어이지만, 이 복수형 변환기를 다른 언어에 맞게 사용할 수도 있습니다. 이를 위해 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 복수형 처리를 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다:

```
use Illuminate\Support\Pluralizer;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Pluralizer::useLanguage('spanish');     

    // ...     
}
```

> [!WARNING]
> 복수형 변환기 언어를 변경할 경우, Eloquent 모델의 [테이블 이름](/docs/9.x/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

번역 문자열은 보통 `lang` 디렉토리 내의 파일에 저장합니다. 이 디렉토리에는 애플리케이션에서 지원하는 각 언어마다 하위 디렉토리가 있어야 합니다. Laravel은 기본 제공 기능(예: 검증 오류 메시지)의 번역 문자열을 이렇게 관리합니다:

```
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키로 된 문자열 배열을 반환합니다. 예를 들어:

```
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 지역에 따라 언어가 다른 경우, 언어 디렉토리는 ISO 15897 표준에 따라 명명해야 합니다. 예를 들어, 영국 영어는 "en-gb" 대신 "en_GB"로 명명해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역할 문자열이 많은 애플리케이션에서는 모든 문자열에 "짧은 키"를 정의하는 것이 뷰에서 키를 참조할 때 혼란을 줄 수 있고, 계속해서 키를 만들어야 하는 것이 번거로울 수 있습니다.

이러한 이유로 Laravel은 번역 문자열의 기본 번역 자체를 키로 사용하는 방식을 지원합니다. 이 방식에 따라 번역 파일은 `lang` 디렉토리 내에 JSON 파일로 저장됩니다. 예를 들어, 애플리케이션에 스페인어 번역이 있다면 다음과 같이 `lang/es.json` 파일을 만듭니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키 / 파일 충돌 주의

번역 문자열 키가 다른 번역 파일 이름과 충돌하지 않도록 해야 합니다. 예를 들어, "NL" 로케일에 대해 `__('Action')`을 번역하는데, 만약 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없다면, 번역된 결과는 `nl/action.php` 파일 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 불러오기

`__` 헬퍼 함수를 사용하여 언어 파일에서 번역 문자열을 불러올 수 있습니다. "짧은 키"를 사용하는 경우, `__` 함수에 키가 포함된 파일 이름과 키를 점(dot) 표기법으로 전달해야 합니다. 예를 들어, `lang/en/messages.php` 언어 파일의 `welcome` 번역 문자열을 불러오려면 다음과 같이 합니다:

```
echo __('messages.welcome');
```

지정한 번역 문자열이 존재하지 않는 경우, `__` 함수는 전달된 키를 그대로 반환합니다. 위 예시에서는 `messages.welcome`를 반환할 것입니다.

[기본 번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys), `__` 함수에 기본 번역 문자열을 그대로 전달해야 합니다:

```
echo __('I love programming.');
```

여기서도 만약 번역 문자열이 존재하지 않으면, `__` 함수는 전달한 기본 문자열을 그대로 반환합니다.

[Blade 템플릿 엔진](/docs/9.x/blade)을 사용하는 경우, `{{ }}` 구문을 활용해 번역 문자열을 쉽게 출력할 수 있습니다:

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 매개변수 치환하기

필요에 따라 번역 문자열 내에 `:` 접두어가 붙은 플레이스홀더를 정의할 수 있습니다. 예를 들어, 환영 메시지에 이름을 위한 플레이스홀더가 있을 수 있습니다:

```
'welcome' => 'Welcome, :name',
```

번역 문자열을 불러올 때 `__` 함수의 두 번째 인자로 치환할 값을 배열로 전달하면 플레이스홀더를 대체할 수 있습니다:

```
echo __('messages.welcome', ['name' => 'dayle']);
```

만약 플레이스홀더가 모두 대문자이거나 첫 글자만 대문자인 경우, 치환되는 값 또한 그에 맞춰 대문자 처리가 됩니다:

```
'welcome' => 'Welcome, :NAME', // 출력 예: Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // 출력 예: Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 포맷팅

번역 문자열 플레이스홀더에 객체를 전달하면, 해당 객체의 `__toString` 메서드가 호출되어 문자열로 변환됩니다. `__toString`은 PHP의 "매직 메서드" 중 하나입니다. 그러나 때로는 서드파티 라이브러리 등의 클래스의 `__toString` 메서드를 직접 제어할 수 없는 경우도 있습니다.

이런 경우 Laravel은 특정 객체 타입에 대해 커스텀 포맷팅 핸들러를 등록하는 기능을 제공합니다. 이를 위해 `Lang` 파사드의 `stringable` 메서드를 호출합니다. `stringable`은 처리할 객체 타입을 타입힌트하는 클로저를 인자로 받습니다. 보통 이 코드는 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 호출합니다:

```
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Lang::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<a name="pluralization"></a>
### 복수형 처리

복수형 처리는 언어별로 매우 다양한 규칙이 있어 복잡한 문제입니다. 하지만 Laravel은 사용자가 정의한 복수형 규칙에 따라 문자열을 다르게 번역할 수 있도록 도와줍니다. `|` 문자를 사용해 단수형과 복수형을 구분할 수 있습니다:

```
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)에도 복수형 처리가 지원됩니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

보다 복잡한 규칙을 사용해 여러 값 범위에 따라 번역 문자열을 다르게 지정할 수도 있습니다:

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형 옵션이 포함된 번역 문자열을 정의한 후, `trans_choice` 함수를 사용해 특정 "개수"에 따른 해당 문자열을 가져올 수 있습니다. 이 예에서는 개수가 1보다 크므로 복수형 문자열을 반환합니다:

```
echo trans_choice('messages.apples', 10);
```

복수형 문자열 내에도 플레이스홀더를 정의할 수 있으며, `trans_choice` 함수의 세 번째 인자로 치환할 값을 배열로 전달해 대체할 수 있습니다:

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

만약 `trans_choice` 함수에 전달한 정수 값을 그대로 표시하고 싶다면, 내장된 `:count` 플레이스홀더를 사용할 수 있습니다:

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이딩

일부 패키지들은 자체 언어 파일을 포함하고 있습니다. 이 파일의 내용을 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉토리에 오버라이딩할 파일을 배치할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 영어 번역 문자열이 담긴 `messages.php`를 오버라이딩하려면, `lang/vendor/hearthfire/en/messages.php` 경로에 파일을 위치시키면 됩니다. 이 파일에는 오버라이딩하려는 번역 문자열만 정의하면 되고, 나머지 문자열은 원래 패키지의 언어 파일에서 계속 불러옵니다.