# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [언어 파일 게시하기](#publishing-the-language-files)
    - [로케일 설정하기](#configuring-the-locale)
    - [복수화 언어](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [단축 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열 내 매개변수 치환하기](#replacing-parameters-in-translation-strings)
    - [복수화(Pluralization)](#pluralization)
- [패키지 언어 파일 재정의하기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하고 싶다면 `lang:publish` Artisan 명령어로 게시할 수 있습니다.

Laravel의 로컬라이제이션 기능은 다양한 언어의 문자열을 편리하게 가져올 수 있게 해주어, 애플리케이션에서 여러 언어를 손쉽게 지원할 수 있게 합니다.

Laravel은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째는 애플리케이션의 `lang` 디렉터리에 각 언어별 하위 디렉터리를 만들어 언어 문자열을 파일로 저장하는 방식입니다. 이 방식은 Laravel이 유효성 검사 오류 메시지와 같은 내장 기능의 번역 문자열 관리를 위해 사용하는 방법입니다:

```
/lang
    /en
        messages.php
    /es
        messages.php
```

또한 번역 문자열은 `lang` 디렉터리 내에 배치된 JSON 파일로 정의할 수도 있습니다. 이 방법을 사용할 경우, 애플리케이션에서 지원하는 각 언어마다 해당하는 JSON 파일이 위치합니다. 많은 수의 번역 문자열을 가진 애플리케이션에서 이 방식이 권장됩니다:

```
/lang
    en.json
    es.json
```

이 문서에서는 이러한 각각의 번역 문자열 관리 방식을 다룰 것입니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 게시하기

기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel 언어 파일을 커스터마이징하거나 직접 만들고 싶다면 `lang:publish` Artisan 명령어를 사용해 `lang` 디렉터리를 생성해야 합니다. 이 명령어는 애플리케이션에 `lang` 디렉터리를 생성하고 Laravel에서 기본으로 사용하는 언어 파일 세트를 게시합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정하기

애플리케이션의 기본 언어는 보통 `APP_LOCALE` 환경 변수로 설정되는 `config/app.php` 구성 파일의 `locale` 옵션에 저장됩니다. 이 값은 애플리케이션 필요에 따라 자유롭게 변경할 수 있습니다.

기본 언어에 해당하는 번역 문자열이 없을 경우 사용할 "대체 언어(fallback language)"도 설정할 수 있습니다. 대체 언어 역시 `config/app.php` 구성 파일에 설정하며, 보통 `APP_FALLBACK_LOCALE` 환경 변수 값을 통해 지정합니다.

런타임 시 단일 HTTP 요청에 대해서 기본 언어를 변경하고 싶다면, `App` 파사드에서 제공하는 `setLocale` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function (string $locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    // ...
});
```

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인하기

현재 로케일 값을 확인하거나 특정 로케일인지 체크하려면 `App` 파사드의 `currentLocale`과 `isLocale` 메서드를 사용할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수화 언어

Eloquent와 프레임워크의 다른 부분에서 단수형 문자열을 복수형으로 변환하기 위해 사용되는 Laravel의 "복수화(pluralizer)" 기능이 영어가 아닌 다른 언어를 사용할 수 있도록 지정할 수 있습니다. 이는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출함으로써 설정할 수 있습니다. 현재 복수화 기능이 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다:

```
use Illuminate\Support\Pluralizer;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');

    // ...
}
```

> [!WARNING]  
> 복수화 언어를 변경할 경우, 반드시 Eloquent 모델의 [테이블 이름](/docs/11.x/eloquent#table-names)를 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 단축 키 사용하기

대부분의 경우 번역 문자열은 `lang` 디렉터리 내의 파일에 저장됩니다. 이 디렉터리에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. 이 방법은 Laravel이 유효성 검증 오류 메시지와 같은 내장 기능의 문자열 관리를 위해 사용하는 방식입니다:

```
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키가 지정된 문자열 배열을 반환합니다. 예를 들어:

```
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]  
> 국가별 변형이 있는 언어(territory-specific)라면 ISO 15897 규격에 따라 언어 디렉터리 이름을 지어야 합니다. 예를 들어 영국 영어는 "en_GB"로 명명해야 하며 "en-gb"는 사용하지 마십시오.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역할 문자열이 많아질 경우, 모든 문자열에 대해 "단축 키"를 정의하는 것은 뷰(view)에서 키를 참조할 때 혼란스럽고 관리가 번거로워집니다.

이 때문에 Laravel은 "기본" 번역 문자열 자체를 키로 사용해 번역 문자열을 정의하는 기능도 지원합니다. 이 방식은 `lang` 디렉터리에 JSON 파일로 저장합니다. 만약 애플리케이션에 스페인어 번역이 있다면 `lang/es.json` 파일을 생성해야 합니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키와 파일 이름 충돌 처리

다른 번역 파일 이름과 충돌하는 번역 키는 정의하지 않아야 합니다. 예를 들어 "NL" 로케일에서 `__('Action')`을 번역할 때 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없으면, 번역 결과로 `nl/action.php` 파일 전체 내용이 반환됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

`__` 도우미 함수를 사용하여 언어 파일에서 번역 문자열을 가져올 수 있습니다. 만약 "단축 키"를 사용해 번역 문자열을 정의했다면, `__` 함수에는 키를 포함하는 파일명과 키를 "점(dot)" 표기법으로 전달해야 합니다. 예를 들어 `lang/en/messages.php` 파일에서 `welcome` 번역 문자열을 가져오는 예시입니다:

```
echo __('messages.welcome');
```

만약 지정한 번역 문자열이 존재하지 않으면 `__` 함수는 키 자체를 반환합니다. 위 예시라면 번역 문자열이 없을 경우 `messages.welcome`이 반환됩니다.

[기본 번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)는 기본 문자열을 그대로 `__` 함수에 넘기면 됩니다:

```
echo __('I love programming.');
```

이 경우에도 번역된 문자열이 없다면 함수에 전달한 키 자체가 반환됩니다.

[Blade 템플릿 엔진](/docs/11.x/blade)을 사용하는 경우, `{{ }}` 구문을 이용해 번역 문자열을 출력할 수 있습니다:

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 매개변수 치환하기

원한다면 번역 문자열에 플레이스홀더(변수 자리 표시자)를 정의할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어 환영 메시지에 `:name`이라는 자리 표시자를 만들 수 있습니다:

```
'welcome' => 'Welcome, :name',
```

번역 문자열을 가져올 때 플레이스홀더를 치환하려면, `__` 함수의 두 번째 인수로 치환할 값의 연관 배열을 전달하면 됩니다:

```
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더가 모두 대문자이거나 첫 글자만 대문자인 경우, 치환되는 값도 대응하는 대소문자로 표시됩니다:

```
'welcome' => 'Welcome, :NAME', // 결과: Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // 결과: Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 포맷팅

번역 플레이스홀더에 객체를 전달하면 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 내장 매직 메서드 중 하나입니다. 다만, 제3자 라이브러리 등 제어할 수 없는 클래스 객체의 경우 `__toString` 메서드를 직접 다루지 못할 수도 있습니다.

이 경우 Laravel은 해당 객체 타입에 대해 사용자 정의 포맷터를 등록할 수 있게 합니다. 이를 위해 번역기의 `stringable` 메서드를 호출해야 합니다. `stringable`은 클로저를 인자로 받아 포맷팅할 객체의 타입을 타입 힌트로 명시해야 하며, 보통 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

```
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
```

<a name="pluralization"></a>
### 복수화(Pluralization)

복수화는 복잡한 문제입니다. 언어마다 복수형 규칙이 다양하기 때문입니다. 그러나 Laravel은 정의한 복수화 규칙에 따라 문자열을 다르게 번역하는 데 도움을 줍니다. `|` 문자로 단수형과 복수형을 구분해 정의할 수 있습니다:

```
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)에도 복수화는 지원됩니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

더욱 복잡한 복수화 규칙도 만들 수 있으며, 여러 값 범위에 따른 번역 문자열을 지정할 수 있습니다:

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수화가 포함된 번역 문자열을 정의한 후 `trans_choice` 함수를 사용하여 주어진 "개수"에 맞는 번역 문자열을 가져올 수 있습니다. 이 예에서는 개수가 1보다 크기 때문에 복수형 문자열이 반환됩니다:

```
echo trans_choice('messages.apples', 10);
```

복수화 문자열 내에 플레이스홀더도 정의할 수 있습니다. 플레이스홀더를 치환하려면 `trans_choice` 함수의 세 번째 인자로 배열을 전달하세요:

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice` 함수에 전달된 정수 값을 표시하고 싶다면 내장 플레이스홀더인 `:count`를 사용할 수 있습니다:

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 재정의하기

일부 패키지는 자체 언어 파일을 포함해서 출고됩니다. 이들 패키지의 핵심 파일을 직접 수정하지 않고, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 배치해 재정의할 수 있습니다.

예를 들어 `skyrim/hearthfire`라는 패키지에서 영어 번역 문자열인 `messages.php`를 재정의할 필요가 있다면, `lang/vendor/hearthfire/en/messages.php` 경로에 파일을 넣으면 됩니다. 이 파일에는 재정의할 번역 문자열만 정의하면 됩니다. 재정의하지 않은 문자열은 여전히 패키지의 원본 언어 파일에서 불러옵니다.