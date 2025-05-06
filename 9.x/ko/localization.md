# 지역화(Localization)

- [소개](#introduction)
    - [로케일 설정](#configuring-the-locale)
    - [복수형 언어 선택](#pluralization-language)
- [번역 문자열 정의](#defining-translation-strings)
    - [짧은 키 사용](#using-short-keys)
    - [번역 문자열을 키로 사용](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열의 파라미터 대체](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이드](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

Laravel의 지역화 기능은 다양한 언어로 문자열을 쉽게 가져올 수 있는 편리한 방법을 제공하여, 애플리케이션에서 다국어 지원을 손쉽게 구현할 수 있습니다.

Laravel은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째로, 언어 문자열을 `lang` 디렉터리 내의 파일에 저장할 수 있습니다. 이 디렉터리 안에는 애플리케이션에서 지원하는 각 언어별로 하위 디렉터리가 존재할 수 있습니다. Laravel은 이 방식을 사용하여 내장 기능(예: 유효성 검사 오류 메시지 등)의 번역 문자열을 관리합니다.

    /lang
        /en
            messages.php
        /es
            messages.php

또는, 번역 문자열을 `lang` 디렉터리 내에 위치한 JSON 파일에 정의할 수도 있습니다. 이 방식을 사용할 경우, 애플리케이션에서 지원하는 각 언어별로 해당 언어의 JSON 파일이 존재해야 합니다. 다수의 번역 문자열을 관리해야 하는 애플리케이션에 권장되는 방식입니다.

    /lang
        en.json
        es.json

이 문서에서는 번역 문자열을 관리하는 각각의 방법에 대해 설명합니다.

<a name="configuring-the-locale"></a>
### 로케일 설정

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장됩니다. 필요에 따라 이 값을 변경할 수 있습니다.

런타임 중에 `App` 파사드의 `setLocale` 메서드를 사용하여 특정 HTTP 요청에 대한 기본 언어를 변경할 수도 있습니다.

    use Illuminate\Support\Facades\App;

    Route::get('/greeting/{locale}', function ($locale) {
        if (! in_array($locale, ['en', 'es', 'fr'])) {
            abort(400);
        }

        App::setLocale($locale);

        //
    });

또한, 활성 언어에 번역 문자열이 없을 경우 사용할 "대체(fallback) 언어"를 설정할 수 있습니다. 기본 언어와 마찬가지로 대체 언어도 `config/app.php` 설정 파일에서 지정합니다.

    'fallback_locale' => 'en',

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인하기

현재 로케일을 확인하거나, 로케일이 특정 값인지 확인하고 싶다면 `App` 파사드의 `currentLocale`, `isLocale` 메서드를 사용할 수 있습니다.

    use Illuminate\Support\Facades\App;

    $locale = App::currentLocale();

    if (App::isLocale('en')) {
        //
    }

<a name="pluralization-language"></a>
### 복수형 언어 선택

Laravel의 "Pluralizer"(복수형 변환기)는 Eloquent 및 프레임워크의 다른 부분에서 단수 문자열을 복수형으로 변환하는 데 사용됩니다. 만약 영어 이외의 언어를 사용하고 싶다면, 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 지원되는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다.

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

> **경고**
> 복수형 변환기의 언어를 커스터마이즈할 경우, 반드시 Eloquent 모델의 [테이블 이름](/docs/{{version}}/eloquent#table-names)을 명시적으로 지정해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의

<a name="using-short-keys"></a>
### 짧은 키 사용

대부분의 경우, 번역 문자열은 `lang` 디렉터리 내의 파일에 저장됩니다. 이 디렉터리 안에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. 이는 Laravel이 내장 기능(예: 유효성 검사 오류 메시지 등)에서 번역 문자열을 관리하는 방식과 동일합니다.

    /lang
        /en
            messages.php
        /es
            messages.php

모든 언어 파일은 키로 구성된 배열을 반환해야 합니다. 예시는 다음과 같습니다.

    <?php

    // lang/en/messages.php

    return [
        'welcome' => 'Welcome to our application!',
    ];

> **경고**
> 지역이 다른 언어(예: 영국 영어 등)의 경우, 언어 디렉터리는 ISO 15897 규정에 따라 명명해야 합니다. 예를 들어, 영국 영어는 "en-gb"가 아닌 "en_GB"로 작성해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용

번역해야 할 문자열의 수가 많을 경우, 모든 문자열에 대해 "짧은 키"를 생성하고 참조하는 과정이 혼란스러울 수 있으며, 매번 새로운 키를 만드는 것도 번거로울 수 있습니다.

이러한 이유로, Laravel은 번역 문자열 자체(기본 번역)를 키로 사용하는 방식도 지원합니다. 이 방식에 사용하는 번역 파일은 `lang` 디렉터리에 JSON 파일로 저장합니다. 예를 들어, 스페인어 번역의 경우 `lang/es.json` 파일을 생성해야 합니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키 / 파일 충돌

다른 번역 파일명과 충돌하는 번역 문자열 키를 지정해서는 안 됩니다. 예를 들어, "NL" 로케일에서 `__('Action')`을 번역하려 할 때 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없다면, 번역기는 `nl/action.php` 파일의 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

언어 파일에서 번역 문자열을 가져오려면 `__` 헬퍼 함수를 사용할 수 있습니다. "짧은 키" 방식의 경우, 키가 포함된 파일 이름과 키를 "dot" 문법을 사용해 `__` 함수에 전달해야 합니다. 예를 들어, `lang/en/messages.php` 파일에서 `welcome` 번역 문자열을 가져오는 방법은 아래와 같습니다.

    echo __('messages.welcome');

지정된 번역 문자열이 없으면, `__` 함수는 번역 문자열의 키를 반환합니다. 즉, 위의 예시에서 번역 문자열이 없다면 `__` 함수는 `messages.welcome`을 반환합니다.

[기본 번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)는, 번역 문자열의 기본값을 그대로 `__` 함수에 전달하면 됩니다.

    echo __('I love programming.');

마찬가지로, 번역 문자열이 존재하지 않는다면 `__` 함수는 전달받은 번역 문자열 키를 그대로 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용할 경우, `{{ }}` 구문을 사용해서 번역 문자열을 출력할 수도 있습니다.

    {{ __('messages.welcome') }}

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열의 파라미터 대체

원한다면 번역 문자열에 플레이스홀더를 정의할 수 있습니다. 플레이스홀더는 모두 `:`로 시작합니다. 예를 들어, 사용자명에 따라 환영 메시지를 만들 수 있습니다.

    'welcome' => 'Welcome, :name',

이 플레이스홀더를 대체하려면, 대체할 값을 배열로 두 번째 인자에 전달하면 됩니다.

    echo __('messages.welcome', ['name' => 'dayle']);

플레이스홀더가 모두 대문자이거나 첫 글자만 대문자라면, 변환된 값 역시 동일하게 대문자로 표시됩니다.

    'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
    'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle

<a name="object-replacement-formatting"></a>
#### 객체 대체 포맷 지정

만약 객체를 번역 문자열의 플레이스홀더로 제공할 경우, 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 "매직 메서드" 중 하나입니다. 그러나, 해당 클래스가 서드파티 라이브러리에서 온 것이라 제어할 수 없는 경우도 있습니다.

이럴 때는 해당 타입의 객체에 대해 커스텀 포맷 핸들러를 등록할 수 있습니다. 이를 위해 번역기의 `stringable` 메서드를 사용합니다. `stringable` 메서드는 클로저를 인자로 받으며, 해당 타입을 타입힌트 해야 합니다. 일반적으로는, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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

<a name="pluralization"></a>
### 복수형 처리

복수형 처리는 언어별로 매우 다양한 규칙이 있어 복잡하지만, Laravel은 직접 정의한 규칙에 따라 번역 문자열을 다르게 처리하도록 도와줍니다. `|` 문자를 사용해 단수와 복수 형태를 구분할 수 있습니다.

    'apples' => 'There is one apple|There are many apples',

물론, [번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)에도 복수형 처리가 지원됩니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

여러 값의 범위별로 번역 문자열을 지정하는 좀 더 복잡한 규칙도 작성할 수 있습니다.

    'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',

복수형 옵션을 포함하는 번역 문자열을 정의한 후에는, `trans_choice` 함수를 사용해 "개수"에 맞는 문장을 가져올 수 있습니다. 예를 들어, 아래와 같이 개수가 1보다 많을 때는 복수형이 반환됩니다.

    echo trans_choice('messages.apples', 10);

또한, 복수형 문자열 안에 플레이스홀더 속성을 정의해 대체할 수도 있습니다. 이 경우 `trans_choice` 함수의 세 번째 인자로 배열을 전달하면 됩니다.

    'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

    echo trans_choice('time.minutes_ago', 5, ['value' => 5]);

`trans_choice` 함수에 전달된 정수 값을 출력하려면 내장 플레이스홀더 `:count`를 사용할 수 있습니다.

    'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이드

일부 패키지는 자체 언어 파일을 포함하고 있을 수 있습니다. 이러한 내용을 변경하기 위해 패키지의 핵심 파일을 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 배치하여 오버라이드할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php`에서 영어 번역 문자열을 오버라이드하고 싶다면, 파일을 `lang/vendor/hearthfire/en/messages.php`에 두면 됩니다. 이 파일에는 오버라이드하고자 하는 번역 문자열만 정의하면 됩니다. 오버라이드하지 않은 번역 문자열은 여전히 패키지의 원본 언어 파일에서 불러옵니다.