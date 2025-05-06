# 지역화(Localization)

- [소개](#introduction)
    - [언어 파일 퍼블리싱하기](#publishing-the-language-files)
    - [로케일 설정하기](#configuring-the-locale)
    - [복수형 언어(Pluralization Language)](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열 내 파라미터 치환](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이드하기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하고 싶다면, `lang:publish` Artisan 명령어를 사용해 언어 파일을 퍼블리싱할 수 있습니다.

Laravel의 지역화 기능은 여러 언어로 문자열을 손쉽게 가져올 수 있도록 하여, 애플리케이션에서 다양한 언어 지원을 쉽게 구현하게 해줍니다.

Laravel은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째로, 언어 문자열은 애플리케이션의 `lang` 디렉터리 내 파일들에 저장할 수 있습니다. 이 디렉터리 안에는 애플리케이션에서 지원하는 각 언어별로 하위 디렉터리가 있을 수 있습니다. 이 방식은 Laravel에서 기본적으로 제공하는 기능(예: 유효성 검사 에러 메시지 등)의 번역 문자열을 관리하는 데 사용됩니다.

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

또한, 번역 문자열을 `lang` 디렉터리 내 JSON 파일로 정의할 수도 있습니다. 이 방식을 사용할 때는, 애플리케이션이 지원하는 각 언어별로 해당하는 JSON 파일이 디렉터리에 존재해야 합니다. 번역 대상 문자열이 매우 많은 애플리케이션의 경우 이 방식이 권장됩니다.

```text
/lang
    en.json
    es.json
```

이 문서에서는 두 가지 번역 문자열 관리 방식을 모두 다룹니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 퍼블리싱하기

기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하거나 직접 작성하고 싶다면, `lang:publish` Artisan 명령어로 `lang` 디렉터리를 생성해야 합니다. `lang:publish` 명령은 애플리케이션 내에 `lang` 디렉터리를 만들고 Laravel이 사용하는 기본 언어 파일 셋을 퍼블리싱합니다.

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정하기

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장되어 있으며, 보통 `APP_LOCALE` 환경 변수를 통해 설정합니다. 이 값을 애플리케이션 요구에 맞게 자유롭게 수정할 수 있습니다.

기본 언어에 번역 문자열이 없는 경우 사용될 "폴백 언어(fallback language)"도 설정할 수 있습니다. 폴백 언어 역시 `config/app.php` 파일에서 설정하며, 보통 `APP_FALLBACK_LOCALE` 환경 변수로 값을 세팅합니다.

실행 중 HTTP 요청 한 건에 한해서 기본 언어를 수정하고 싶다면 `App` 파사드의 `setLocale` 메서드를 사용할 수 있습니다.

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
#### 현재 로케일 확인하기

`App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용하면 현재 로케일을 확인하거나, 특정 값과 같은지 검사할 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 언어(Pluralization Language)

Laravel의 "복수형 변환기(pluralizer)"는 Eloquent 및 프레임워크의 여러 부분에서 단수를 복수로 변환할 때 사용됩니다. 영문이 아닌 다른 언어로 복수형 변환기를 사용하고 싶다면, 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 `useLanguage` 메서드를 호출하면 됩니다. 복수형 변환기가 현재 지원하는 언어는 다음과 같습니다: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`

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
> 복수형 변환기의 언어를 변경하는 경우, 반드시 Eloquent 모델의 [테이블명](https://laravel.com/docs/{{version}}/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로 번역 문자열은 `lang` 디렉터리 안의 파일에 저장합니다. 이 디렉터리에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. Laravel은 내장 기능의 번역 문자열(예: 유효성 검사 에러 메시지 등)을 이런 방식으로 관리합니다.

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키-값 쌍 배열을 반환합니다. 예시:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 지역에 따라 구분되는 언어는, ISO 15897 표준에 따라 언어 디렉터리명을 지정해야 합니다. 예를 들어, 영국 영어는 "en-gb"가 아니라 "en_GB"로 지정해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역 대상 문자열이 매우 많은 애플리케이션에서는 모든 문자열에 "짧은 키"를 일일이 붙이면 뷰에서 참조하기 혼란스럽고, 매번 키를 만들어내는 것도 번거로울 수 있습니다.

이런 이유로, Laravel은 번역 문자열을 "기본" 원문 문자열 자체로 키로 사용하는 방식도 지원합니다. 번역 문자열을 키로 사용하는 언어 파일은 `lang` 디렉터리에 JSON 파일로 저장합니다. 예를 들어, 애플리케이션이 스페인어를 지원하는 경우 `lang/es.json` 파일을 생성해야 합니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키/파일 충돌

다른 번역 파일명과 충돌되는 번역 문자열 키를 정의해서는 안 됩니다. 예를 들어, "NL" 로케일에 대해 `__('Action')`을 번역하는데 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없으면, 번역기는 `nl/action.php` 파일의 전체 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

`__` 헬퍼 함수를 이용해 언어 파일에서 번역 문자열을 가져올 수 있습니다. "짧은 키" 방식을 사용할 경우, 점(.) 구문법으로 파일명.키 형태로 `__` 함수에 전달해야 합니다. 예를 들어, `lang/en/messages.php` 파일에서 `welcome` 번역 문자열을 가져오려면:

```php
echo __('messages.welcome');
```

만약 지정한 번역 문자열이 존재하지 않으면, `__` 함수는 전달한 키 그대로를 반환합니다. 즉, 위 예시에서 번역 문자열이 없으면 `messages.welcome`을 반환합니다.

[기본 번역문 자체를 키로 쓰는 방식](#using-translation-strings-as-keys)을 사용할 경우, 번역하고자 하는 원문 문자열 자체를 `__` 함수에 전달하면 됩니다.

```php
echo __('I love programming.');
```

역시 문자열이 존재하지 않으면, `__` 함수는 전달된 원문 문자열을 그대로 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용하는 경우, `{{ }}` 이스케이프 구문으로 번역 문자열을 출력할 수 있습니다.

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 파라미터 치환

원한다면 번역 문자열 내에 플레이스홀더(placeholder)를 정의할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어 이름을 받을 환영 메시지는 다음과 같이 정의할 수 있습니다.

```php
'welcome' => 'Welcome, :name',
```

번역 문자열을 가져올 때, `__` 함수의 두 번째 인자로 치환 값을 배열로 전달하여 플레이스홀더를 교체할 수 있습니다.

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더가 모두 대문자 또는 첫 글자만 대문자인 경우, 치환 값 역시 그에 맞게 대/소문자가 일치합니다.

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 포맷팅

플레이스홀더에 객체를 전달하면 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring)은 PHP 내장 "매직 메서드" 중 하나입니다. 하지만, 간혹 해당 클래스가 서드파티 라이브러리 소유일 때처럼 `__toString`을 직접 제어할 수 없는 경우도 있습니다.

이런 경우, Laravel은 특정 타입의 객체에 대해 직접 커스텀 포맷팅 핸들러를 등록할 수 있습니다. `stringable` 메서드를 호출하면 되며, 이 메서드는 포맷팅할 객체 타입이 명시된 클로저를 인자로 받습니다. 보통 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 `stringable`을 호출합니다.

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

복수형(Pluralization)은 언어마다 규칙이 매우 복잡하지만, Laravel은 직접 정의한 복수 규칙에 따라 번역 문자열을 다르게 반환할 수 있습니다. `|` 기호를 사용해 단수와 복수를 구분합니다.

```php
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열 자체를 키로 사용하는 경우](#using-translation-strings-as-keys)에도 복수형을 지원합니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

값의 범위마다 여러 가지 복수형을 지정할 수도 있습니다.

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형 옵션이 있는 번역 문자열을 정의한 후엔, `trans_choice` 함수를 사용해 특정 "count"에 맞는 문자열을 가져올 수 있습니다. 아래 예시에서, count가 1보다 크므로 복수형이 반환됩니다.

```php
echo trans_choice('messages.apples', 10);
```

복수형 번역 문자열에서도 플레이스홀더를 사용할 수 있습니다. 이 경우, `trans_choice` 함수의 세 번째 인자로 치환할 배열을 전달합니다.

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice` 함수에 전달한 정수 값을 그대로 출력하려면 내장 `:count` 플레이스홀더를 사용할 수 있습니다.

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이드하기

일부 패키지는 자체 언어 파일을 포함할 수 있습니다. 이런 경우, 패키지의 핵심 파일을 변경하지 않고도 원하는 문자열을 오버라이드할 수 있는데, 이때는 `lang/vendor/{package}/{locale}` 디렉터리에 파일을 두면 됩니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php`에서 영어 번역 문자열을 오버라이드하고 싶으면, 다음 경로에 파일을 두어야 합니다: `lang/vendor/hearthfire/en/messages.php`. 이 파일에는 오버라이드하고 싶은 문자열만 정의하면 되며, 오버라이드하지 않은 나머지 번역 문자열은 여전히 패키지의 원본 파일에서 불러옵니다.