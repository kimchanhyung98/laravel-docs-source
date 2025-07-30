# 지역화 (Localization)

- [소개](#introduction)
    - [언어 파일 게시하기](#publishing-the-language-files)
    - [로케일 구성하기](#configuring-the-locale)
    - [복수형 언어(Pluralization Language)](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열 내 매개변수 치환하기](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 재정의하기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 맞춤 설정하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

Laravel의 지역화 기능은 다양한 언어로 된 문자열을 편리하게 가져올 수 있게 하여, 애플리케이션에서 여러 언어를 쉽게 지원할 수 있도록 도와줍니다.

Laravel은 두 가지 방법으로 번역 문자열을 관리할 수 있습니다. 첫 번째는 애플리케이션의 `lang` 디렉토리 내에 언어별 하위 디렉토리를 두고 문자열을 저장하는 방식입니다. 이 방식은 Laravel이 내장된 기능들(예: 유효성 검사 오류 메시지)의 번역 문자열을 관리할 때 사용하는 방법입니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

또 다른 방식은 `lang` 디렉토리 내에 JSON 파일로 번역 문자열을 정의하는 것입니다. 이 방식은 애플리케이션에서 지원하는 각 언어별로 JSON 파일을 두고 관리합니다. 많은 번역 문자열을 가진 애플리케이션에서 이 방식을 권장합니다:

```text
/lang
    en.json
    es.json
```

이 문서에서는 두 가지 방법을 모두 다룹니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 게시하기

기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 없습니다. Laravel의 언어 파일을 맞춤 설정하거나 직접 생성하려면 `lang:publish` Artisan 명령어로 `lang` 디렉토리를 생성해야 합니다. 이 명령은 애플리케이션에 `lang` 디렉토리를 만들고, Laravel에서 사용하는 기본 언어 파일 세트를 게시합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 구성하기

애플리케이션의 기본 언어 설정은 `config/app.php` 설정 파일 내 `locale` 옵션에 저장되어 있으며, 일반적으로 `APP_LOCALE` 환경 변수로 설정됩니다. 필요에 따라 이 값을 자유롭게 변경할 수 있습니다.

또한 기본 언어에 해당하는 번역 문자열이 없을 때 사용할 "대체 언어(fallback language)"도 설정할 수 있습니다. 이 대체 언어도 `config/app.php`에서 `fallback_locale` 옵션을 통해 설정하며, 보통 `APP_FALLBACK_LOCALE` 환경 변수로 값이 지정됩니다.

실행 중에 한 번의 HTTP 요청 단위로 기본 언어를 변경하려면, `App` 파사드의 `setLocale` 메서드를 사용할 수 있습니다:

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

현재 로케일을 확인하거나 특정 로케일인지 검사하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 언어(Pluralization Language)

Eloquent와 프레임워크 일부에서 단수형 문자열을 복수형으로 변환하기 위해 사용하는 Laravel의 "복수형 변환기(pluralizer)"가 영어 외의 다른 언어를 사용할 수 있도록 지정할 수 있습니다. 이를 위해 애플리케이션 서비스 프로바이더의 `boot` 메서드에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다:

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
> 복수형 변환기의 언어를 변경했다면, Eloquent 모델의 [테이블 이름(table names)](/docs/12.x/eloquent#table-names)을 명시적으로 정의하는 것이 좋습니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

보통 번역 문자열은 `lang` 디렉토리에 언어별 하위 디렉토리를 만들고, 그 안에 파일로 저장합니다. 이 방식은 Laravel 내장 기능(예: 유효성 검사 메시지) 번역 문자열 관리에 사용됩니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키-값 쌍을 반환하는 배열입니다. 예를 들면:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 동일한 언어라도 지역에 따라 구분할 때는 ISO 15897 표준에 따라 디렉토리 이름을 지정해야 합니다. 예를 들어, 영국 영어는 "en_GB"로 표기해야 하며, "en-gb"는 사용하지 않습니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

많은 수의 번역 문자열을 가진 애플리케이션에서, 모든 문자열에 대해 "짧은 키"를 정의하는 것은 뷰에서 키를 참조할 때 혼란스럽고 관리가 번거로울 수 있습니다.

이런 이유로 Laravel은 "기본" 번역 문자열을 키로 사용하는 방식을 지원합니다. 이 경우 언어 파일은 `lang` 디렉토리 내의 JSON 파일로 저장합니다. 예를 들어 스페인어 번역이 있다면 `lang/es.json` 파일을 만듭니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키와 파일 이름 충돌

번역 문자열 키를 정의할 때 다른 번역 파일 이름과 충돌하지 않도록 주의해야 합니다. 예를 들어 "NL" 로케일에서 `__('Action')`을 번역할 때 `nl/action.php` 파일이 있고 `nl.json` 파일이 존재하지 않으면, 번역기는 `nl/action.php` 전체 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

`__` 헬퍼 함수로 언어 파일에서 번역 문자열을 가져올 수 있습니다. "짧은 키" 방식을 사용하는 경우, 파일명과 키를 점(.) 구분법으로 전달합니다. 예를 들어, `lang/en/messages.php`에서 `welcome` 키 문자열을 가져오려면:

```php
echo __('messages.welcome');
```

지정한 번역 문자열이 없으면 `__` 함수는 전달된 키를 그대로 반환합니다. 위 예시에서 해당 번역이 없으면 `messages.welcome`이 반환됩니다.

[기본 번역 문자열을 키로 사용하는 방식](#using-translation-strings-as-keys)일 경우에는 문자열 자체를 `__` 함수에 전달합니다:

```php
echo __('I love programming.');
```

이 역시 번역이 없으면 해당 기본 문자열이 그대로 반환됩니다.

[Blade 템플릿 엔진](/docs/12.x/blade)을 사용하는 경우, `{{ }}` 구문을 통해 쉽게 출력할 수 있습니다:

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 매개변수 치환하기

번역 문자열 내에 플레이스홀더(자리 표시자)를 정의할 수 있으며 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어 이름을 치환하는 환영 메시지를 정의할 수 있습니다:

```php
'welcome' => 'Welcome, :name',
```

치환하려면 `__` 함수의 두 번째 인자로 치환 대상 배열을 전달하면 됩니다:

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더가 모두 대문자거나 처음 글자만 대문자인 경우, 치환되는 값도 대문자 또는 첫 글자 대문자 형식으로 변환됩니다:

```php
'welcome' => 'Welcome, :NAME', // 출력 예: Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // 출력 예: Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 형식 처리

번역 문자열 플레이스홀더에 객체를 전달하면, 해당 객체의 `__toString` 메서드가 호출됩니다. `__toString`은 PHP의 내장 매직 메서드 중 하나입니다. 다만, 경우에 따라 서드파티 라이브러리 같은 클래스의 `__toString` 메서드를 수정할 수 없는 상황도 있습니다.

이럴 때 Laravel은 특정 객체 타입에 대해 커스텀 포매팅 핸들러를 등록할 수 있도록 합니다. `Lang` 파사드의 `stringable` 메서드에 콜백을 등록하세요. 콜백 매개변수에 포맷 대상 객체 타입을 지정해야 하며, 보통 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드에서 등록합니다:

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

복수형 처리는 다양한 언어별 복잡한 규칙들이 있어 까다로운 문제입니다. Laravel은 플러럴(plural) 구분을 위해 문자열에 `|` 구분자를 사용하여 단수형과 복수형을 구분할 수 있게 지원합니다:

```php
'apples' => 'There is one apple|There are many apples',
```

물론 [번역 문자열 키로 사용하기](#using-translation-strings-as-keys) 방식도 복수형을 지원합니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

더 나아가, 여러 범위값별로 번역 문자열을 지정하는 복잡한 복수형 규칙도 만들 수 있습니다:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형 문자열을 정의했다면, `trans_choice` 함수를 사용해 주어진 수에 따라 적절한 번역 문자열을 가져옵니다. 예제에서 1보다 큰 수이므로 복수형 문자열이 반환됩니다:

```php
echo trans_choice('messages.apples', 10);
```

복수형 문자열에 플레이스홀더도 정의할 수 있습니다. `trans_choice` 함수의 세 번째 인자에 배열로 치환값을 전달하세요:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice`에 전달된 정수 값을 문자열 내에 표시하고 싶다면, 미리 정의된 `:count` 플레이스홀더를 사용할 수 있습니다:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 재정의하기

몇몇 패키지는 자체 언어 파일을 포함하고 있습니다. 패키지 파일을 직접 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉토리에 파일을 추가해 특정 번역 문자열을 재정의할 수 있습니다.

예를 들어 `skyrim/hearthfire`라는 패키지의 영어 번역 문자열 중 `messages.php`를 재정의하고자 한다면, 다음 경로에 언어 파일을 두어야 합니다: `lang/vendor/hearthfire/en/messages.php`. 이 파일에는 재정의할 번역 문자열만 정의하면 됩니다. 나머지 문자열은 원래 패키지 언어 파일에서 계속 불러옵니다.