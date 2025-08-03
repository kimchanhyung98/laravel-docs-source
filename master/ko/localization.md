# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [언어 파일 퍼블리싱](#publishing-the-language-files)
    - [로케일 구성하기](#configuring-the-locale)
    - [복수형 언어 설정](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열 내 매개변수 교체](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 덮어쓰기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 골격에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하고자 할 경우, `lang:publish` Artisan 명령어를 통해 퍼블리싱할 수 있습니다.

Laravel의 로컬라이제이션 기능은 여러 언어로 된 문자열을 쉽게 불러올 수 있는 편리한 방법을 제공하여, 애플리케이션에서 다국어를 지원하기 쉽게 만듭니다.

Laravel은 번역 문자열 관리를 위한 두 가지 방법을 제공합니다. 첫째, 번역 문자열은 애플리케이션의 `lang` 디렉토리 내 파일에 저장할 수 있습니다. 이 디렉토리 내에는 애플리케이션에서 지원하는 각 언어별 하위 디렉토리가 있을 수 있습니다. Laravel 내장 기능(예: validation 에러 메시지) 번역 관리에 이 방식을 사용합니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

또는, `lang` 디렉토리 내에 JSON 파일로 번역 문자열을 정의할 수도 있습니다. 이 방식에서는 애플리케이션이 지원하는 각 언어에 해당하는 JSON 파일을 이 디렉토리에 두게 됩니다. 다수의 번역 문자열이 필요한 애플리케이션에 권장하는 방법입니다:

```text
/lang
    en.json
    es.json
```

이 문서에서는 번역 문자열 관리를 위한 두 가지 방식을 차례로 설명합니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 퍼블리싱

기본 Laravel 애플리케이션 골격에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 수정하거나 새로 만들고자 할 때는, `lang:publish` Artisan 명령어를 실행하여 `lang` 디렉토리를 스캐폴딩하는 것이 좋습니다. 이 명령어는 애플리케이션에 `lang` 디렉토리를 생성하고, Laravel에서 사용하는 기본 언어 파일 세트를 퍼블리시합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 구성하기

애플리케이션의 기본 언어는 `config/app.php` 구성 파일의 `locale` 설정 옵션에 저장되어 있고, 보통은 `APP_LOCALE` 환경 변수로 설정됩니다. 이 값을 필요에 맞게 자유롭게 변경할 수 있습니다.

또한 기본 언어에 해당 번역 문자열이 없을 때 사용할 "폴백(fallback) 언어"를 설정할 수도 있습니다. 폴백 언어 역시 `config/app.php`에서 설정하고, 일반적으로 `APP_FALLBACK_LOCALE` 환경 변수 값으로 정합니다.

특정 HTTP 요청에 대해서 프로그래밍 실행 중에 기본 언어를 변경하고자 하면, `App` 파사드가 제공하는 `setLocale` 메서드를 사용할 수 있습니다:

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

현재 설정된 로케일을 확인하거나 특정 로케일인지 검사하고자 하면, `App` 파사드의 `currentLocale`과 `isLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 언어 설정

Laravel의 복수형 변환기(pluralizer)는 Eloquent 및 프레임워크 내 여러 부분에서 단수 문자열을 복수형으로 변환할 때 사용됩니다. 기본적으로 영어를 사용하지만, 다른 언어를 지정할 수도 있습니다. 이 작업은 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하여 수행합니다. 현재 복수형 변환기가 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다:

```php
use Illuminate\Support\Pluralizer;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');

    // ...
}
```

> [!WARNING]
> 복수형 변환기의 언어를 변경할 경우, Eloquent 모델에서 [테이블 이름(table names)](/docs/master/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로 번역 문자열은 `lang` 디렉토리 내 각 언어별 하위 디렉토리에 파일로 저장합니다. 이 방법은 Laravel 내장 기능(예: validation 에러 메시지)에서 주로 사용하는 방식입니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키-값 배열을 반환합니다. 예를 들어:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 지역에 따라 언어가 다를 경우, 언어 디렉토리 이름은 ISO 15897 규격에 따라 명명해야 합니다. 예를 들어, 영국 영어는 "en_GB"로 지정해야 하며, "en-gb"는 사용하지 않습니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

많은 수의 번역 문자열을 가진 애플리케이션에서는 모든 문자열에 대해 짧은 키를 정의하는 것이 관리하기 어렵고, 뷰에서 키를 참조할 때 헷갈릴 수 있습니다.

이 때문에 Laravel은 "기본(default)" 번역 문자열 자체를 키로 사용하는 방식을 추가로 지원합니다. 이 경우 언어 파일은 JSON 형식으로 `lang` 디렉토리에 저장됩니다. 예를 들어, 애플리케이션에 스페인어 번역이 있다면 `lang/es.json` 파일을 생성합니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키와 파일 이름 충돌

번역 문자열 키가 다른 번역 파일 이름과 충돌해서는 안 됩니다. 예를 들어, "NL" 로케일에서 `__('Action')`를 번역할 때 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없으면, 번역기는 `nl/action.php` 전체 내용을 반환합니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

`__` 헬퍼 함수를 사용해서 언어 파일에서 번역 문자열을 가져올 수 있습니다. 짧은 키 방식을 사용했다면, 키가 포함된 파일명과 키를 도트(`.`) 구분 방식으로 전달합니다. 예를 들어, `lang/en/messages.php` 파일 내의 `welcome` 번역을 불러오려면 다음과 같이 작성합니다:

```php
echo __('messages.welcome');
```

번역 문자열이 존재하지 않으면, `__` 함수는 입력받은 키를 그대로 반환합니다. 위 예제라면 문자열이 없을 경우 `messages.welcome`이 리턴됩니다.

[기본 번역 문자열을 키로 사용하는 방식](#using-translation-strings-as-keys)을 사용할 경우, `__` 함수에 문자열의 기본 번역을 그대로 전달하세요:

```php
echo __('I love programming.');
```

마찬가지로 번역이 없으면 입력받은 기본 문자열을 그대로 반환합니다.

[Blade 템플릿 엔진](/docs/master/blade)을 사용하는 경우, `{{ }}` 구문을 통해 번역 문자열을 출력할 수 있습니다:

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 매개변수 교체

원한다면 번역 문자열 안에 플레이스홀더(자리 표시자)를 정의할 수 있습니다. 플레이스홀더는 모두 `:`로 시작합니다. 예를 들어, 이름을 포함한 환영 메시지를 정의할 수 있습니다:

```php
'welcome' => 'Welcome, :name',
```

번역 문자열을 가져올 때, 플레이스홀더 값들을 두 번째 인수로 배열 형태로 전달하면 치환됩니다:

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더 이름이 모두 대문자거나 첫 글자만 대문자일 경우, 치환되는 값도 대소문자가 그대로 반영됩니다:

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 활용 플레이스홀더 포맷팅

만약 플레이스홀더에 객체를 지정하면, 해당 객체의 `__toString` 메서드가 호출되어 문자열화됩니다. PHP가 기본 제공하는 "매직 메서드"입니다. 그러나 서드파티 라이브러리 등 외부 클래스의 `__toString` 메서드를 직접 제어하지 못할 수도 있습니다.

이럴 때 Laravel은 특정 클래스용 커스텀 포맷팅 핸들러를 등록할 수 있도록 `stringable` 메서드를 제공합니다. 이 메서드는 포맷팅 책임이 있는 클래스 타입을 명시하는 클로저를 인자로 받습니다. 일반적으로 이 코드는 애플리케이션의 `AppServiceProvider` 클래스를 `boot` 메서드에서 사용합니다:

```php
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Lang::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<a name="pluralization"></a>
### 복수형 처리 (Pluralization)

복수형 처리는 다양한 언어마다 복잡한 규칙이 있어 까다롭지만, Laravel은 정의한 복수형 규칙에 따라 문자열을 다르게 번역할 수 있도록 지원합니다. `|` 문자로 단수형과 복수형을 구분해 정의합니다:

```php
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열을 키로 사용하는 방식](#using-translation-strings-as-keys)에서도 복수형이 지원됩니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

복수형 범위를 세부적으로 나누어 더 복잡한 규칙도 만들 수 있습니다:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형을 포함한 번역 문자열을 정의한 다음 `trans_choice` 함수를 사용하여 특정 개수에 맞는 문자열을 가져올 수 있습니다. 이 예제에서는 개수가 하나보다 크므로 복수형 문자열이 반환됩니다:

```php
echo trans_choice('messages.apples', 10);
```

복수형 문자열에서도 플레이스홀더를 사용할 수 있으며, `trans_choice` 함수 세 번째 인수로 배열을 전달해 치환할 수 있습니다:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice`에 전달된 숫자 값을 표시하고 싶으면 내장된 `:count` 플레이스홀더를 사용할 수 있습니다:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 덮어쓰기

일부 패키지는 자체 언어 파일을 포함해 배포됩니다. 패키지의 핵심 파일을 직접 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉토리에 원하는 내용을 덮어쓰는 파일을 두어 변경할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 영어(`en`) 번역 문자열 `messages.php`를 덮어쓰고 싶다면 다음 경로에 파일을 생성하세요: `lang/vendor/hearthfire/en/messages.php` 이 파일에는 덮어쓰고 싶은 번역 문자열만 정의하면 됩니다. 덮어쓰지 않은 문자열은 여전히 패키지 원본 언어 파일에서 로드됩니다.