# 지역화(Localization)

- [소개](#introduction)
    - [언어 파일 퍼블리싱](#publishing-the-language-files)
    - [로케일 설정](#configuring-the-locale)
    - [복수형 언어 설정](#pluralization-language)
- [번역 문자열 정의](#defining-translation-strings)
    - [짧은 키 사용](#using-short-keys)
    - [번역 문자열을 키로 사용](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열의 파라미터 치환](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이드](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스캐폴드는 `lang` 디렉터리를 포함하지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 통해 파일을 퍼블리싱할 수 있습니다.

Laravel의 지역화 기능은 다양한 언어의 문자열을 쉽게 가져올 수 있는 편리한 방법을 제공하며, 이를 통해 애플리케이션에서 여러 언어를 쉽게 지원할 수 있습니다.

Laravel에서는 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 먼저, 언어 문자열은 애플리케이션의 `lang` 디렉터리 내에 파일로 저장할 수 있습니다. 이 디렉터리에서는 애플리케이션이 지원하는 각 언어별 하위 디렉터리를 둘 수 있습니다. Laravel은 기본적인 검증 에러 메시지와 같은 내장 기능의 번역 문자열도 이러한 방식으로 관리합니다.

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

또는, 번역 문자열을 `lang` 디렉터리에 위치한 JSON 파일 내에 정의할 수도 있습니다. 이 방식을 사용할 경우, 애플리케이션에서 지원하는 각 언어마다 해당 언어의 JSON 파일이 있어야 합니다. 많은 번역 문자열을 가진 애플리케이션에는 이 방식이 권장됩니다.

```text
/lang
    en.json
    es.json
```

각 방식에 대해 아래에서 자세히 다루겠습니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 퍼블리싱

기본적으로 Laravel 애플리케이션 스캐폴드는 `lang` 디렉터리를 포함하지 않습니다. 언어 파일을 커스터마이즈하거나 직접 생성하려면, `lang:publish` Artisan 명령어를 통해 `lang` 디렉터리를 스캐폴딩해야 합니다. `lang:publish` 명령은 애플리케이션에 `lang` 디렉터리를 생성하고, Laravel에서 사용하는 기본 언어 파일 세트를 퍼블리싱합니다.

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정

애플리케이션의 기본 언어는 `config/app.php`의 `locale` 설정 항목에 저장되어 있으며, 보통 `APP_LOCALE` 환경 변수를 통해 지정됩니다. 필요에 따라 이 값을 자유롭게 수정할 수 있습니다.

또한, "폴백 언어(fallback language)"도 설정할 수 있는데, 기본 언어에 해당 번역 문자열이 없을 때 사용됩니다. 폴백 언어 역시 `config/app.php` 파일에서 `APP_FALLBACK_LOCALE` 환경 변수로 설정할 수 있습니다.

실행 중에 단일 HTTP 요청에서 기본 언어를 변경하려면 `App` 파사드의 `setLocale` 메서드를 사용할 수 있습니다.

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

`App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용하여 현재 로케일을 확인하거나 특정 값과 일치하는지 체크할 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 언어 설정

Eloquent 및 프레임워크의 다른 일부에서 단수 문자열을 복수형으로 변환할 때 사용하는 Laravel의 "pluralizer"에 영어가 아닌 언어를 사용할 수 있습니다. 이는 애플리케이션 서비스 프로바이더의 `boot` 메서드 내부에서 `useLanguage` 메서드를 호출하여 설정할 수 있습니다. 현재 플러럴라이저가 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다.

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
> 플러럴라이저 언어를 커스터마이즈하는 경우, Eloquent 모델의 [테이블명](/docs/{{version}}/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의

<a name="using-short-keys"></a>
### 짧은 키 사용

일반적으로 번역 문자열은 `lang` 디렉터리 내부의 파일에 저장합니다. 이 디렉터리 내에는 앱이 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. 이것은 Laravel이 내장 기능의 번역 문자열을 관리하는 표준 방식입니다.

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키와 문자열로 구성된 배열을 반환해야 합니다. 예시:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 영국 영어 등 지역별로 변형되는 언어의 경우, 디렉터리명은 ISO 15897에 따라 작성해야 합니다. 예를 들어, 영국 영어는 "en-gb" 대신 "en_GB"를 사용해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용

번역 문자열이 매우 많을 경우, 모든 문자열을 "짧은 키"로 정의하면 키를 참조할 때 혼란스러울 수 있고, 새로운 키를 계속 만들어야 하므로 번거롭습니다.

이런 이유로, Laravel은 번역 문자열의 "기본값" 자체를 키로 사용할 수 있도록 지원합니다. 이 방식의 언어 파일은 `lang` 디렉터리에 JSON 파일로 저장합니다. 예를 들어, 앱에 스페인어 번역이 있다면 `lang/es.json` 파일을 생성해야 합니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키 / 파일 충돌

다른 번역 파일명과 충돌하는 번역 문자열 키는 정의하지 않는 것이 좋습니다. 예를 들어, "NL" 로케일에 대해 `__('Action')`을 번역하려고 할 때 `nl/action.php` 파일은 있지만 `nl.json` 파일이 없다면, 번역기는 `nl/action.php` 파일 전체 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

언어 파일로부터 번역 문자열을 가져올 때는 `__` 헬퍼 함수를 사용할 수 있습니다. "짧은 키"를 사용하는 경우, `__` 함수에 파일명과 키를 "닷(.)" 문법으로 전달해야 합니다. 예를 들어, `lang/en/messages.php`파일의 `welcome`번역 문자열을 가져오려면 아래와 같습니다.

```php
echo __('messages.welcome');
```

지정한 번역 문자열이 존재하지 않으면, `__` 함수는 전달받은 키를 그대로 반환합니다. 위 예시에서 만약 해당 번역 문자열이 없으면 `messages.welcome`을 반환합니다.

[기본 번역 문자열을 키로 사용](#using-translation-strings-as-keys)하는 경우, 해당 문자열을 그대로 `__` 함수에 전달하면 됩니다.

```php
echo __('I love programming.');
```

이 경우에도 번역 문자열이 없으면 함수는 전달받은 실제 문자열을 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용한다면, `{{ }}` 이코 시택스를 써서 번역 문자열을 출력할 수 있습니다.

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열의 파라미터 치환

원한다면, 번역 문자열에 플레이스홀더를 정의할 수 있습니다. 모든 플레이스홀더는 `:` 접두사를 사용합니다. 예를 들어, 이름 플레이스홀더가 있는 환영 메시지는 다음과 같이 정의할 수 있습니다.

```php
'welcome' => 'Welcome, :name',
```

번역 문자열을 가져올 때 플레이스홀더를 치환하려면, `__` 함수 두 번째 인자로 치환할 값을 배열로 전달하세요.

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

만약 플레이스홀더가 모두 대문자거나, 첫 글자만 대문자라면, 치환 값도 자동으로 대/소문자가 맞추어집니다.

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 형식화

플레이스홀더에 객체를 전달하는 경우 객체의 `__toString` 메서드가 호출됩니다. PHP의 [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 내장 "매직 메서드" 중 하나입니다. 하지만, 종종 타사의 라이브러리 객체 등 내 마음대로 `__toString`을 커스터마이즈할 수 없는 경우도 있습니다.

이런 경우, 해당 객체 타입에 맞는 커스텀 형식 핸들러를 등록할 수 있습니다. 이를 위해서는, 번역기의 `stringable` 메서드를 호출하면 됩니다. 이 메서드는 형식화를 담당할 객체 타입을 타입힌트하는 클로저를 받습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 설정합니다.

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
### 복수형 처리(Pluralization)

복수형 처리는 언어마다 규칙이 다르기 때문에 복잡할 수 있지만, Laravel에서는 정의한 복수형 규칙에 따라 번역 문자열을 다르게 번역할 수 있습니다. `|` 문자를 사용해 단수형과 복수형을 구분합니다.

```php
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)에도 복수형을 지원합니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

더 복잡한 규칙, 예를 들어 여러 값 구간에 따라 번역 문자열을 달리할 수도 있습니다.

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형 번역 문자열을 정의한 후에는 `trans_choice` 함수를 사용해 해당 갯수("count")에 맞는 번역을 가져올 수 있습니다. 아래 예시는, 카운트가 1보다 크므로 복수형 메시지가 반환됩니다.

```php
echo trans_choice('messages.apples', 10);
```

복수형 문자열에도 플레이스홀더를 지정할 수 있으며, `trans_choice` 함수 세 번째 인자로 값을 전달하면 치환됩니다.

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice` 함수에 전달한 정수 값을 그대로 출력하고 싶다면 내장 플레이스홀더 `:count`를 사용할 수 있습니다.

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이드

일부 패키지는 자체적으로 언어 파일을 제공할 수 있습니다. 이러한 번역을 수정하고 싶을 때 직접 패키지의 코어 파일을 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 생성해 오버라이드할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php`에서 영어 번역 문자열을 오버라이드하려면, `lang/vendor/hearthfire/en/messages.php`에 언어 파일을 두면 됩니다. 이 파일에는 오버라이드하려는 번역 문자열만 정의하면 되며, 나머지는 여전히 패키지의 기본 언어 파일에서 불러옵니다.