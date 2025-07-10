# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [언어 파일 퍼블리싱](#publishing-the-language-files)
    - [로케일 설정](#configuring-the-locale)
    - [복수형 처리 언어](#pluralization-language)
- [번역 문자열 정의](#defining-translation-strings)
    - [짧은 키 사용](#using-short-keys)
    - [번역 문자열 자체를 키로 사용](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열의 파라미터 치환](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이드](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]
> 기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 직접 커스터마이즈하고 싶다면 `lang:publish` 아티즌 명령어를 통해 퍼블리싱할 수 있습니다.

라라벨의 로컬라이제이션 기능을 사용하면 다양한 언어로 된 문자열을 쉽게 가져올 수 있으므로, 여러분의 애플리케이션에서 여러 언어를 간단하게 지원할 수 있습니다.

라라벨은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 먼저, 애플리케이션의 `lang` 디렉터리 내 파일에 번역 문자열을 저장할 수 있습니다. 이 디렉터리 안에는 애플리케이션이 지원하는 각 언어별로 별도의 하위 디렉터리를 둘 수 있습니다. 이 방식은 라라벨이 내장 기능(예: 유효성 검증 오류 메시지 등)을 번역 문자열로 관리할 때 사용하는 방식입니다.

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

또는, 번역 문자열을 `lang` 디렉터리 내에 위치한 JSON 파일에 정의할 수도 있습니다. 이 방식을 사용할 경우, 애플리케이션에서 지원하는 각 언어에 해당하는 JSON 파일을 이 디렉터리 안에 두게 됩니다. 번역해야 할 문자열이 많을 때에는 이 방식을 권장합니다.

```text
/lang
    en.json
    es.json
```

이 문서에서는 위 두 가지 번역 문자열 관리 방법을 각각 다루겠습니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 퍼블리싱

기본적으로, 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 수정하거나 직접 만들고 싶다면 `lang:publish` 아티즌 명령어를 실행해서 `lang` 디렉터리를 생성해야 합니다. `lang:publish` 명령어는 여러분의 애플리케이션 내에 `lang` 디렉터리를 만들고, 라라벨에서 사용하는 기본 언어 파일 세트를 퍼블리싱합니다.

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정

애플리케이션의 기본 언어는 `config/app.php` 설정 파일 내 `locale` 옵션에 저장됩니다. 이 값은 일반적으로 `APP_LOCALE` 환경 변수를 통해 설정합니다. 여러분의 애플리케이션에 맞게 이 값을 자유롭게 변경할 수 있습니다.

또한 "폴백 언어(fallback language)"도 설정할 수 있습니다. 폴백 언어는 기본 언어에서 특정 번역 문자열을 찾지 못할 때 사용됩니다. 폴백 언어 역시 `config/app.php` 파일에서 설정하며, 보통 `APP_FALLBACK_LOCALE` 환경 변수로 지정합니다.

HTTP 요청 처리 중 런타임에서 일시적으로 기본 언어를 바꾸고 싶다면, `App` 파사드가 제공하는 `setLocale` 메서드를 사용할 수 있습니다.

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

현재 설정되어 있는 로케일을 확인하거나, 특정 값과 일치하는지 검사하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 처리 언어

Eloquent 및 프레임워크의 일부 기능에서 단수형 문자열을 복수형 형태로 변환할 때 사용하는 "복수형 변환기"의 언어를 영어 이외의 언어로 지정할 수 있습니다. 이를 위해 여러분의 애플리케이션 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 지원하는 복수형 변환 언어는 다음과 같습니다: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`

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
> 복수형 변환기의 언어를 커스터마이즈했다면, Eloquent 모델의 [테이블명](/docs/12.x/eloquent#table-names)을 반드시 명시적으로 지정해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의

<a name="using-short-keys"></a>
### 짧은 키 사용

일반적으로 번역 문자열은 `lang` 디렉터리 내 파일에 저장합니다. 이 디렉터리 안에는 애플리케이션이 지원하는 각 언어별로 별도의 하위 디렉터리가 있어야 합니다. 라라벨은 내장 기능(예: 유효성 검증 오류 메시지 등)에서 이 방식을 사용합니다.

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키-값 형태의 배열을 반환합니다. 예시:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 영국 영어, 미국 영어와 같이 지역에 따라 다르게 번역하는 언어의 경우, ISO 15897 규약에 따라 언어 디렉터리를 이름 지어야 합니다. 예를 들어, 영국 영어는 "en-gb"가 아니라 "en_GB"를 사용해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열 자체를 키로 사용

번역해야 할 문자열이 많은 애플리케이션에서는 "짧은 키(short key)"를 매번 만들고 관리하는 과정이 뷰 파일에서 번역 키를 참조할 때 혼란스럽거나 비효율적일 수 있습니다.

이때 라라벨은 번역 문자열의 "기본" 텍스트 자체를 키처럼 사용하는 방식도 지원합니다. 이러한 방식의 언어 파일은 `lang` 디렉터리 내 JSON 파일로 저장합니다. 예를 들어 스페인어 번역의 경우에는 `lang/es.json` 파일을 만들면 됩니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키/파일명 충돌 주의

다른 번역 파일명과 충돌하는 번역 문자열 키를 정의해서는 안 됩니다. 예를 들어 "NL" 로케일에서 `__('Action')`을 번역하려고 할 때 `nl/action.php` 파일은 있고 `nl.json` 파일이 없으면, 변환된 결과로 `nl/action.php` 파일 전체 내용이 반환될 수 있습니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

번역 문자열을 가져올 때는 `__` 헬퍼 함수를 사용할 수 있습니다. "짧은 키" 방식을 사용하는 경우, 키가 들어 있는 파일명과, 해당 키를 점(`.`) 표기법으로 `__` 함수에 전달해야 합니다. 아래 예시는 `lang/en/messages.php` 파일에 있는 `welcome` 번역 문자열을 가져오는 방법입니다.

```php
echo __('messages.welcome');
```

지정한 번역 문자열이 존재하지 않을 경우, `__` 함수는 전달받은 문자열 키를 그대로 반환합니다. 즉, 위 예시에서 만약 해당 번역 문자열이 없다면 `__` 함수는 `messages.welcome`을 반환합니다.

만약 [번역 문자열을 그대로 키로 사용하는 방식](#using-translation-strings-as-keys)을 쓴다면, 해당 문자열의 기본 텍스트를 `__` 함수에 넘기면 됩니다.

```php
echo __('I love programming.');
```

마찬가지로 번역 문자열이 존재하지 않으면 전달받은 문자열 키 자체를 반환합니다.

[Blade 템플릿 엔진](/docs/12.x/blade)을 사용할 때는 `{{ }}` 문법으로 번역 문자열을 출력할 수 있습니다.

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열의 파라미터 치환

필요에 따라 번역 문자열 내에 플레이스홀더를 정의할 수 있습니다. 플레이스홀더는 모두 `:`로 시작합니다. 예를 들어 이름을 지정하는 환영 메시지를 다음과 같이 정의할 수 있습니다.

```php
'welcome' => 'Welcome, :name',
```

번역 문자열을 가져올 때, 두 번째 인자로 치환 대상 값을 담은 배열을 넘겨주면 플레이스홀더가 해당 값으로 치환됩니다.

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

만약 플레이스홀더가 모두 대문자형, 혹은 첫 글자만 대문자인 경우라면, 번역 시에도 값의 대소문자가 맞게 변환됩니다.

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 포맷팅

만약 번역 문자열의 플레이스홀더로 객체를 전달하면, 해당 객체의 `__toString` 메서드가 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 내장 "매직 메서드" 중 하나입니다. 하지만 사용하는 객체의 클래스가 외부 라이브러리 등에 속해 있어서, 여러분이 직접 `__toString` 메서드 구현을 바꿀 수 없는 경우도 있습니다.

이럴 때는 라라벨에서 해당 타입의 객체를 어떻게 문자열로 변환할지 "커스텀 포맷 핸들러"를 등록할 수 있습니다. 이를 위해서는 번역기의 `stringable` 메서드를 호출하면 됩니다. 이 메서드는 포맷할 객체의 타입을 타입힌트로 받는 클로저를 인자로 받습니다. 일반적으로는 여러분의 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드에서 호출합니다.

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

복수형 처리는 언어마다 규칙이 매우 다양해서 쉽게 다루기 어렵지만, 라라벨은 지정한 복수형 규칙에 따라 다른 번역 문자열을 반환할 수 있도록 도와줍니다. 문자열에 `|` 문자를 사용해서 단수형과 복수형을 구분할 수 있습니다.

```php
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열을 키로 사용하는 방식](#using-translation-strings-as-keys)에서도 복수형 처리가 지원됩니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

더 복잡한 복수형 규칙을 지정해 여러 값의 범위별로 다른 번역 문자열을 반환할 수도 있습니다.

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형 번역 문자열을 정의했다면, 특정 "수(count)" 값에 맞는 번역을 가져오기 위해 `trans_choice` 함수를 사용하면 됩니다. 아래 예시에서는 count 값이 1보다 크기 때문에 복수형 번역 문자열이 반환됩니다.

```php
echo trans_choice('messages.apples', 10);
```

복수형 처리 문자열 안에도 플레이스홀더를 정의할 수 있습니다. 이 경우, `trans_choice` 함수에 세 번째 인자로 값을 배열로 넘기면 해당 값으로 치환됩니다.

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

또, `trans_choice` 함수에 전달한 정수값을 문자열 안에 직접 표시하고 싶다면 내장 플레이스홀더 `:count`를 사용할 수 있습니다.

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이드

일부 패키지는 자체 언어 파일을 제공합니다. 패키지의 핵심 파일을 직접 수정하여 번역을 변경하는 대신, `lang/vendor/{package}/{locale}` 디렉터리 내에 파일을 만들어 오버라이드할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php`에 담긴 영어 번역 문자열을 커스터마이즈하려면, `lang/vendor/hearthfire/en/messages.php`와 같은 경로에 언어 파일을 두면 됩니다. 이 파일에는 오버라이드하고자 하는 번역 문자열만 정의하면 되고, 나머지 번역 문자열은 여전히 패키지의 오리지널 언어 파일에서 불러옵니다.