# 로컬라이제이션

- [소개](#introduction)
    - [언어 파일 퍼블리싱](#publishing-the-language-files)
    - [로케일 설정](#configuring-the-locale)
    - [복수형 처리 언어 지정](#pluralization-language)
- [번역 문자열 정의](#defining-translation-strings)
    - [짧은 키 사용](#using-short-keys)
    - [번역 문자열을 키로 사용](#using-translation-strings-as-keys)
- [번역 문자열 조회](#retrieving-translation-strings)
    - [번역 문자열 파라미터 치환](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이딩](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이징하고 싶다면 `lang:publish` Artisan 커맨드를 통해 직접 퍼블리시해야 합니다.

Laravel의 로컬라이제이션 기능은 다양한 언어로 문자열을 쉽게 조회할 수 있도록 해주어, 애플리케이션에서 여러 언어를 손쉽게 지원할 수 있게 해줍니다.

Laravel에서는 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째로, 번역 문자열을 애플리케이션의 `lang` 디렉터리 내의 파일로 저장할 수 있습니다. 이 디렉터리 안에는 애플리케이션이 지원하는 각 언어별로 하위 디렉터리가 존재할 수 있습니다. 이는 Laravel이 유효성 검사 오류 메시지 등 내장 기능의 번역 문자열을 관리하는 방식입니다:

    /lang
        /en
            messages.php
        /es
            messages.php

또는, 번역 문자열을 `lang` 디렉터리 내에 위치한 JSON 파일로 정의할 수도 있습니다. 이 방식을 사용할 때는, 애플리케이션이 지원하는 각 언어마다 해당 언어의 JSON 파일이 디렉터리에 존재해야 합니다. 번역 문자열이 많은 대형 애플리케이션에서는 이 방법을 추천합니다:

    /lang
        en.json
        es.json

이 문서에서는 각 번역 문자열 관리 방식에 대해 자세히 다룹니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 퍼블리싱

기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이징하거나 직접 작성하려면 `lang:publish` Artisan 커맨드를 통해 `lang` 디렉터리를 생성해야 합니다. `lang:publish` 명령은 애플리케이션에 `lang` 디렉터리를 만들어주고, Laravel이 사용하는 기본 언어 파일들을 퍼블리시합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장되어 있으며, 보통은 `APP_LOCALE` 환경 변수를 통해 지정됩니다. 이 값은 애플리케이션의 필요에 따라 자유롭게 변경할 수 있습니다.

또한 "폴백 언어(fallback language)"도 설정할 수 있는데, 이는 기본 언어에 해당 번역 문자열이 없을 때 사용됩니다. 폴백 언어도 마찬가지로 `config/app.php` 설정 파일에서 `APP_FALLBACK_LOCALE` 환경 변수로 지정합니다.

HTTP 요청 시점에 한해서 기본 언어를 동적으로 변경하고 싶다면, `App` 파사드의 `setLocale` 메서드를 사용할 수 있습니다:

```php
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
#### 현재 로케일 확인

현재 로케일을 알아내거나, 특정 로케일인지 확인하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 처리 언어 지정

Eloquent 등 프레임워크의 여러 부분에서 단수 문자열을 복수형으로 변환하기 위해 사용하는 "복수형 변환기(pluralizer)"가 영어 이외의 언어를 사용하도록 지시할 수 있습니다. 이를 위해서는 애플리케이션 서비스 프로바이더의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 지원되는 복수형 언어는: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish` 입니다:

```php
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
> 복수형 언어를 커스터마이즈할 경우, 반드시 Eloquent 모델의 [테이블 명](/docs/{{version}}/eloquent#table-names)을 명확하게 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의

<a name="using-short-keys"></a>
### 짧은 키(short key) 사용

일반적으로 번역 문자열은 `lang` 디렉터리 내의 파일에 저장됩니다. 애플리케이션이 지원하는 각 언어마다 하위 폴더를 두는 것이 권장 방식입니다. 이 방식은 Laravel이 기본 기능(예: 유효성 검사 오류 메시지 등)의 번역 문자열을 관리하는 방법이기도 합니다.

    /lang
        /en
            messages.php
        /es
            messages.php

모든 언어 파일은 키-값 형식의 배열을 반환합니다. 예시:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]  
> 영국 영어처럼 지역이 다른 언어의 경우 디렉터리 명명을 ISO 15897 표준에 따르세요. 예: British English라면 "en-gb"가 아니라 "en_GB"로 사용해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용

번역 문자열이 많은 애플리케이션에서는 모든 문자열에 "짧은 키"를 할당하고 이 키를 뷰에서 참조하는 것이 관리상 혼란스러울 수 있습니다. 또한 매번 새로운 키를 만드는 것도 번거로운 작업입니다.

이런 이유로, Laravel은 번역 문자열의 "기본값" 자체를 키로 사용하는 것도 지원합니다. 번역 문자열을 키로 사용하는 경우 언어 파일은 `lang` 디렉터리 내의 JSON 파일로 저장됩니다. 예를 들어, 스페인어 번역이 필요하다면 `lang/es.json` 파일을 생성합니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키/파일 충돌

다른 번역 파일 이름과 충돌하는 번역 키는 사용하지 마세요. 예를 들어, "NL" 로케일에서 `__('Action')`을 번역하려고 할 때 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없으면, 번역기는 `nl/action.php`의 전체 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 조회

언어 파일에서 번역 문자열을 조회할 때는 `__` 헬퍼 함수를 사용합니다. "짧은 키"로 번역 문자열을 정의한 경우, 해당 파일명(폴더명 제외)과 키를 "도트" 문법(`.`)으로 지정합니다. 예를 들어, `lang/en/messages.php`에서 `welcome` 키를 조회할 경우:

```php
echo __('messages.welcome');
```

지정한 번역 문자열이 없다면, `__` 함수는 해당 키를 그대로 반환합니다. 다시 말해, 위 예시에서 번역 문자열이 없으면 `messages.welcome`을 반환합니다.

[기본 번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)는 문자열 자체를 `__` 함수에 전달하면 됩니다:

```php
echo __('I love programming.');
```

마찬가지로, 이 번역 문자열이 없을 경우에도 `__` 함수는 입력받은 문자열 그대로 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용한다면 `{{ }}` 이코 구문으로 직접 출력할 수 있습니다:

```php
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 파라미터 치환

필요한 경우, 번역 문자열 내에 플레이스홀더(자리표시자)를 사용할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어 사용자명을 표시하는 환영 메시지:

```php
'welcome' => 'Welcome, :name',
```

조회 시 플레이스홀더를 치환하려면, `__` 함수의 두 번째 인자로 배열을 넘기면 됩니다.

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더가 모두 대문자거나 첫 글자만 대문자라면, 치환된 값에도 동일하게 적용됩니다:

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 파라미터 포매팅

플레이스홀더에 객체를 넘기면, 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 내장 "매직 메서드" 중 하나입니다. 하지만 외부 라이브러리 등에서 온 객체처럼 직접적으로 `__toString`을 제어할 수 없는 경우도 있습니다.

이런 경우, Laravel에서는 특정 객체 유형에 대해 커스텀 포매팅 헨들러를 등록할 수 있습니다. 이를 위해서는 변환기의 `stringable` 메서드를 사용합니다. type-hint로 포매팅할 객체 타입을 지정하고 보통 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

```php
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
### 복수형 처리

복수형(Pluralization)은 언어별로 매우 다양한 규칙이 존재해 까다로운 문제입니다. 그러나 Laravel은 사용자가 정의한 복수형 규칙에 따라 문자열을 다르게 번역할 수 있도록 도와줍니다. `|` 문자로 단수와 복수를 구분할 수 있습니다:

```php
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열 자체를 키로 쓸 때](#using-translation-strings-as-keys)도 복수형 처리가 가능합니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

특정 숫자 범위별로 더 복잡한 복수형 규칙도 만들 수 있습니다:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형 옵션이 포함된 번역 문자열을 정의했다면, `trans_choice` 함수를 사용해 "개수"에 맞는 번역을 불러올 수 있습니다. 아래 예시에서는 개수가 1 이상이므로 복수형이 반환됩니다:

```php
echo trans_choice('messages.apples', 10);
```

복수형 문자열에서도 플레이스홀더를 사용할 수 있으며, `trans_choice` 함수의 세 번째 인자로 배열을 넘기면 치환할 수 있습니다:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice` 함수에 넘긴 정수값을 그대로 출력하려면 내장 `:count` 플레이스홀더를 사용하면 됩니다:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이딩

일부 패키지는 자체 언어 파일을 함께 제공합니다. 이러한 번역 문자열을 변경할 때는 패키지의 코어 파일을 수정하지 말고, `lang/vendor/{package}/{locale}` 디렉터리에 해당 파일을 추가해 오버라이드할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 영어 번역 `messages.php`를 오버라이드하려면 `lang/vendor/hearthfire/en/messages.php` 파일을 추가하면 됩니다. 오버라이드 파일에는 변경이 필요한 번역 문자열만 정의하면 되며, 정의하지 않은 문자열은 여전히 패키지의 원본 언어 파일에서 로딩됩니다.