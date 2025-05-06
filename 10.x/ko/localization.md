# 로컬라이제이션

- [소개](#introduction)
    - [언어 파일 퍼블리싱](#publishing-the-language-files)
    - [로케일 설정](#configuring-the-locale)
    - [복수형 언어](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열의 파라미터 치환](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 재정의하기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> 기본적으로, Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 통해 퍼블리싱할 수 있습니다.

Laravel의 로컬라이제이션 기능은 다양한 언어의 문자열을 편리하게 가져오는 방법을 제공하여, 애플리케이션에서 손쉽게 다국어를 지원할 수 있게 해줍니다.

Laravel에서는 번역 문자열을 관리하는 두 가지 방식을 제공합니다. 첫 번째로, 언어 문자열은 애플리케이션의 `lang` 디렉터리 내의 파일에 저장할 수 있습니다. 이 디렉터리 내에는 애플리케이션에서 지원하는 언어별로 하위 디렉터리가 있을 수 있습니다. 이것은 Laravel이 내장된 기능(예: 유효성 검사 에러 메시지)의 번역 문자열을 관리하는 방식입니다.

    /lang
        /en
            messages.php
        /es
            messages.php

또는, 번역 문자열을 `lang` 디렉터리에 위치한 JSON 파일로 정의할 수도 있습니다. 이 방법을 사용할 경우, 지원하는 각 언어마다 해당하는 JSON 파일이 존재해야 합니다. 많은 수의 번역 문자열이 필요한 애플리케이션에서는 이 방식을 추천합니다.

    /lang
        en.json
        es.json

본 문서에서는 번역 문자열을 관리하는 각 방식을 자세히 다룰 것입니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 퍼블리싱

기본적으로, Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하거나 직접 만들고자 한다면, `lang:publish` Artisan 명령어를 사용하여 `lang` 디렉터리 구조를 생성해야 합니다. `lang:publish` 명령어는 애플리케이션에 `lang` 디렉터리를 생성하고, Laravel이 사용하는 기본 언어 파일 세트를 퍼블리싱합니다.

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장되어 있습니다. 이 값을 변경하여 애플리케이션의 요구에 맞게 설정할 수 있습니다.

런타임에서 단일 HTTP 요청에 대해 기본 언어를 변경하려면, `App` 파사드가 제공하는 `setLocale` 메서드를 사용할 수 있습니다.

    use Illuminate\Support\Facades\App;

    Route::get('/greeting/{locale}', function (string $locale) {
        if (! in_array($locale, ['en', 'es', 'fr'])) {
            abort(400);
        }

        App::setLocale($locale);

        // ...
    });

"대체 언어(fallback language)"를 설정할 수도 있습니다. 대체 언어는 현재 언어에 번역 문자열이 없을 때 사용됩니다. 기본 언어와 마찬가지로, 대체 언어도 `config/app.php` 설정 파일에서 설정합니다.

    'fallback_locale' => 'en',

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인하기

현재 로케일을 확인하거나, 로케일이 특정 값과 일치하는지 확인하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다.

    use Illuminate\Support\Facades\App;

    $locale = App::currentLocale();

    if (App::isLocale('en')) {
        // ...
    }

<a name="pluralization-language"></a>
### 복수형 언어

Eloquent 및 프레임워크의 기타 부분에서 단어의 단수형을 복수형으로 변환하는 데 사용하는 "복수화(pluralizer)" 도구가 있습니다. 이 도구가 영어가 아닌 다른 언어를 사용하도록 지정할 수 있습니다. 이를 위해, 애플리케이션 서비스 프로바이더의 `boot` 메서드 안에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 복수화 도구가 지원하는 언어는: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다.

    use Illuminate\Support\Pluralizer;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Pluralizer::useLanguage('spanish');     

        // ...     
    }

> [!WARNING]  
> 복수화 언어를 커스터마이즈하는 경우, Eloquent 모델의 [테이블 이름](/docs/{{version}}/eloquent#table-names)은 명시적으로 정의하는 것이 좋습니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로, 번역 문자열은 `lang` 디렉터리 내에 파일로 저장됩니다. 이 디렉터리 내에는 애플리케이션에서 지원하는 각 언어별로 하위 디렉터리가 있어야 합니다. 이는 Laravel이 내장 기능(예: 유효성 검증 에러 메시지)의 번역 문자열을 관리하는 방식입니다.

    /lang
        /en
            messages.php
        /es
            messages.php

모든 언어 파일은 키-값 쌍의 배열을 반환해야 합니다. 예를 들면 다음과 같습니다.

    <?php

    // lang/en/messages.php

    return [
        'welcome' => 'Welcome to our application!',
    ];

> [!WARNING]  
> 지역에 따라 언어가 다른 경우, 언어 디렉터리 이름은 ISO 15897 기준을 따르는 것이 좋습니다. 예를 들어, 영국 영어는 "en-gb"가 아니라 "en_GB"를 사용해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역해야 할 문자열이 매우 많은 애플리케이션의 경우, 모든 문자열에 "짧은 키"를 부여하고 뷰에서 참조하는 것은 혼돈을 야기할 수 있습니다. 또한, 매번 키를 새로 만들어야 하므로 번거로울 수 있습니다.

이런 이유로, Laravel은 "기본" 번역 문자열 자체를 키로 사용해 번역 문자열을 정의하는 방식을 지원합니다. 이러한 파일은 `lang` 디렉터리 내에 JSON 파일로 저장됩니다. 예를 들어, 스페인어 번역이 필요한 경우 `lang/es.json` 파일을 생성해야 합니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키/파일 충돌 주의

다른 번역 파일 이름과 충돌하는 키를 정의해서는 안 됩니다. 예를 들어, "NL" 로케일에서 `__('Action')`을 번역할 때 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없는 경우, 번역기는 `nl/action.php` 파일의 모든 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

`__` 헬퍼 함수를 사용하여 언어 파일에서 번역 문자열을 가져올 수 있습니다. 번역 문자열을 "짧은 키"로 정의했다면, `__` 함수에 "도트 표기법(dot syntax)"을 사용하여 파일명과 키를 함께 전달해야 합니다. 예를 들어, `lang/en/messages.php`에 정의된 `welcome` 번역 문자열을 가져오려면 다음과 같이 합니다.

    echo __('messages.welcome');

지정한 번역 문자열이 존재하지 않으면, `__` 함수는 해당 키를 그대로 반환합니다. 즉, 위 예시에서 번역문이 없으면 `messages.welcome`이 반환됩니다.

[기본 번역 문자열을 키로 사용](#using-translation-strings-as-keys)하는 경우, 번역하고 싶은 기본 문자열 자체를 `__` 함수에 전달하면 됩니다.

    echo __('I love programming.');

마찬가지로, 번역문이 없으면 주어진 문자열(key)을 그대로 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용할 경우, `{{ }}` 에코 구문으로 번역 문자열을 바로 표시할 수 있습니다.

    {{ __('messages.welcome') }}

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열의 파라미터 치환

원한다면, 번역 문자열에 플레이스홀더(placeholder)를 정의할 수 있습니다. 모든 플레이스홀더는 `:` 접두사를 가집니다. 예를 들어, 이름을 위한 플레이스홀더를 포함한 환영 메시지를 정의할 수 있습니다.

    'welcome' => 'Welcome, :name',

이후, 번역 문자열을 가져올 때 두 번째 인자로 치환할 배열을 전달하세요.

    echo __('messages.welcome', ['name' => 'dayle']);

만약 플레이스홀더가 대문자 전부이거나 첫 글자만 대문자인 경우, 변환된 값도 그에 맞게 대문자로 출력됩니다.

    'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
    'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle

<a name="object-replacement-formatting"></a>
#### 객체 치환 포맷팅

번역 플레이스홀더에 객체를 전달하면, 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 내장 "매직 메서드" 중 하나입니다. 하지만, 때로는 사용하는 클래스가 제3자 라이브러리에 속해 있을 때 등, `__toString` 메서드를 수정할 수 없는 경우가 있습니다.

이럴 때는 해당 객체 타입에 맞는 커스텀 포맷터를 등록할 수 있습니다. 이를 위해, 번역기의 `stringable` 메서드를 사용합니다. 이 메서드는 클로저를 받으며, 처리할 객체 타입을 타이프힌트로 명확히 지정해야 합니다. 일반적으로, `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

    use Illuminate\Support\Facades\Lang;
    use Money\Money;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Lang::stringable(function (Money $money) {
            return $money->formatTo('en_GB');
        });
    }

<a name="pluralization"></a>
### 복수형 처리

복수형 처리는 언어마다 복잡한 규칙이 있기 때문에 번역에서 중요한 문제입니다. 하지만, Laravel에서는 직접 정의한 규칙에 따라 다르게 문자열을 번역할 수 있습니다. `|` 기호를 사용해, 단수형과 복수형 문구를 나눌 수 있습니다.

    'apples' => 'There is one apple|There are many apples',

[번역 문자열을 키로 사용하는 방식](#using-translation-strings-as-keys)에서도 복수형 처리는 지원됩니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

여러 값 범위에 따른 복수형 처리도 가능합니다.

    'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',

이와 같이 복수형 옵션이 정의된 문자열을 사용할 때는 `trans_choice` 함수를 사용해 카운트에 맞는 번역값을 가져올 수 있습니다.

    echo trans_choice('messages.apples', 10);

복수형 문자열에도 플레이스홀더 속성을 사용할 수 있으며, 치환할 값을 배열로 세 번째 인자로 전달하면 됩니다.

    'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

    echo trans_choice('time.minutes_ago', 5, ['value' => 5]);

`trans_choice` 함수에 전달된 정수 값을 표시하려면, 내장된 `:count` 플레이스홀더를 사용할 수 있습니다.

    'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 재정의하기

일부 패키지는 자체 언어 파일을 포함할 수 있습니다. 이 경우, 패키지의 핵심 파일을 직접 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 동일한 이름의 파일을 위치시켜 원하는 번역 문자열만 오버라이드(재정의)할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 영어 번역 문자열(`messages.php`)을 수정하고 싶다면, `lang/vendor/hearthfire/en/messages.php` 파일을 만들면 됩니다. 이 파일에서 오버라이드하고자 하는 번역 문자열만 정의하면 되며, 나머지는 패키지의 원본 파일에서 가져오게 됩니다.