# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [언어 파일 발행하기](#publishing-the-language-files)
    - [로케일 설정하기](#configuring-the-locale)
    - [복수형 언어 처리](#pluralization-language)
- [번역 문자열 정의하기](#defining-translation-strings)
    - [짧은 키 사용하기](#using-short-keys)
    - [번역 문자열을 키로 사용하기](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열 내 파라미터 대체하기](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이드하기](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하고 싶다면, `lang:publish` Artisan 명령어를 통해 해당 파일들을 발행할 수 있습니다.

Laravel의 로컬라이제이션 기능은 여러 언어의 문자열을 손쉽게 가져올 수 있는 편리한 방법을 제공하여, 애플리케이션에서 다국어 지원을 간단하게 구현할 수 있게 합니다.

Laravel은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫번째는 애플리케이션의 `lang` 디렉터리 내 파일들에 저장하는 방식입니다. 이 디렉터리에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 존재할 수 있습니다. Laravel 내부 기능(예: 유효성 검증 오류 메시지)의 번역 문자열 관리가 이 방식을 사용합니다:

```
/lang
    /en
        messages.php
    /es
        messages.php
```

또는, 번역 문자열을 `lang` 디렉터리에 위치한 JSON 파일 내에 정의할 수도 있습니다. 이 방식을 쓸 경우, 애플리케이션에서 지원하는 각 언어는 해당 디렉터리 내에 대응하는 JSON 파일을 갖게 됩니다. 많은 번역 문자열을 가진 애플리케이션에 이 방법을 권장합니다:

```
/lang
    en.json
    es.json
```

이 문서에서는 번역 문자열을 관리하는 두 가지 방식 모두를 다룰 것입니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 발행하기

기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하거나 직접 생성하려면 `lang:publish` Artisan 명령어를 통해 `lang` 디렉터리를 생성하고 기본 Laravel 언어 파일 세트를 발행해야 합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정하기

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장됩니다. 이 값을 애플리케이션 필요에 맞게 자유롭게 변경할 수 있습니다.

런타임 시 단일 HTTP 요청에 대해 기본 언어를 변경하려면 `App` 파사드에서 제공하는 `setLocale` 메서드를 사용할 수 있습니다:

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

활성 언어에 해당 번역 문자열이 없을 때 사용할 "대체 언어(fallback language)"를 설정할 수도 있습니다. 대체 언어 역시 `config/app.php` 설정 파일에서 아래와 같이 구성합니다:

```
'fallback_locale' => 'en',
```

<a name="determining-the-current-locale"></a>
#### 현재 로케일 확인하기

`App` 파사드의 `currentLocale` 메서드로 현재 로케일을 확인하거나, `isLocale` 메서드로 현재 로케일이 특정 값인지 확인할 수 있습니다:

```
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 언어 처리

Laravel에서 Eloquent 및 기타 프레임워크 일부가 단수형 문자열을 복수형 문자열로 변환할 때 사용하는 "pluralizer"에 영어가 아닌 다른 언어를 사용하도록 지정할 수 있습니다. 이 기능은 애플리케이션의 Service Provider 내 `boot` 메서드에서 `useLanguage` 메서드를 호출하여 설정합니다. 현재 pluralizer가 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다:

```
use Illuminate\Support\Pluralizer;

/**
 * 애플리케이션 서비스 초기화
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');     

    // ...     
}
```

> [!WARNING]  
> pluralizer의 언어를 사용자 정의할 경우, Eloquent 모델의 [테이블 이름](/docs/10.x/eloquent#table-names)을 명시적으로 정의하는 것이 좋습니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로 번역 문자열은 `lang` 디렉터리 내 파일에 저장됩니다. 이 디렉터리에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. Laravel 내부 기능(유효성 검증 오류 메시지 등)의 번역 문자열 관리가 이 방식을 따릅니다:

```
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키가 있는 문자열 배열을 반환합니다. 예를 들어:

```
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]  
> 지역별로 구분되는 언어를 사용할 경우, ISO 15897 표준에 따라 언어 디렉터리명을 지정해야 합니다. 예를 들어, 영국 영어는 "en-gb"가 아닌 "en_GB"로 명명해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역 문자열이 많을 경우, 모든 문자열에 대해 "짧은 키"를 정의하는 것은 뷰 내에서 키를 참조할 때 혼란을 줄 수 있고, 매번 키를 새로 짓는 것도 번거로워집니다.

이런 점을 해결하기 위해 Laravel은 번역 문자열 자체의 "기본 번역문"을 키로 사용하는 방식을 지원합니다. 이 방식을 사용할 때의 언어 파일은 `lang` 디렉터리에 JSON 형식으로 저장됩니다. 예를 들어, 애플리케이션에서 스페인어 번역을 지원한다면 `lang/es.json` 파일을 생성해야 합니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키 / 파일 이름 충돌

번역 문자열 키를 정의할 때, 다른 번역 파일 이름과 충돌하지 않도록 주의해야 합니다. 예를 들어, "NL" 로케일에 대해 `__('Action')`을 번역하려고 할 때 `nl/action.php` 파일은 존재하지만 `nl.json` 파일이 없으면, 번역기는 `nl/action.php`의 전체 내용을 반환합니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

언어 파일의 번역 문자열은 `__` 헬퍼 함수를 사용하여 가져올 수 있습니다. "짧은 키"를 사용하여 정의했다면, 키를 포함하는 파일명과 키를 "도트(dot)" 문법으로 전달합니다. 예를 들어, `lang/en/messages.php` 파일에서 `welcome` 번역 문자열을 가져오려면 다음과 같이 합니다:

```
echo __('messages.welcome');
```

지정한 번역 문자열이 존재하지 않으면, `__` 함수는 해당 번역 키를 그대로 반환합니다. 위 예시에서는 번역문이 없으면 `messages.welcome`을 반환합니다.

[기본 번역 문자열을 키로 사용하는 경우](#using-translation-strings-as-keys)에는, 기본 문자열을 직접 `__` 함수에 전달해야 합니다:

```
echo __('I love programming.');
```

마찬가지로, 번역문이 없으면 기본 문자열(키) 자체를 반환합니다.

[Blade 템플릿 엔진](/docs/10.x/blade)을 쓸 때는 `{{ }}` 이코 문법으로 번역 문자열을 표시할 수 있습니다:

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열 내 파라미터 대체하기

번역 문자열에 플레이스홀더를 정의할 수 있습니다. 모든 플레이스홀더는 `:` 문자로 시작합니다. 예를 들어, 다음과 같이 이름을 받는 환영 메시지를 정의할 수 있습니다:

```
'welcome' => 'Welcome, :name',
```

플레이스홀더를 치환하면서 번역문을 가져오기 위해서는 `__` 함수의 두 번째 인자로 치환할 값을 배열로 전달합니다:

```
echo __('messages.welcome', ['name' => 'dayle']);
```

만약 플레이스홀더가 모두 대문자이거나 첫 글자만 대문자라면 치환된 값도 대문자 형태에 맞춰 변환됩니다:

```
'welcome' => 'Welcome, :NAME', // 출력: Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // 출력: Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 형식 지정

플레이스홀더에 객체를 전달하면 해당 객체의 `__toString` 메서드가 호출됩니다. `__toString` 메서드는 PHP 내장 "매직 메서드" 중 하나입니다. 하지만, 외부 라이브러리 클래스 등 제어할 수 없는 객체의 경우 `__toString` 메서드를 변경할 수 없습니다.

이럴 때는 Laravel에서 특정 객체 타입만을 위한 커스텀 형식화 핸들러를 등록할 수 있습니다. 이를 위해 번역기의 `stringable` 메서드를 호출합니다. `stringable`은 형식화를 담당할 객체 타입을 type-hint한 클로저를 받으며, 일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * 애플리케이션 서비스 초기화
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

복수형 처리는 언어마다 복잡한 규칙이 있기에 어려운 문제입니다. 하지만 Laravel에서는 정의한 복수형 규칙에 따라 문자열을 다르게 변환할 수 있도록 돕습니다. `|` 기호로 단수형과 복수형을 구분합니다:

```
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열을 키로 사용할 경우](#using-translation-strings-as-keys)에도 복수형을 지원합니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

복수형 옵션을 여러 개 구간으로 나누어 더 복잡하게 설정할 수도 있습니다:

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

복수형이 포함된 번역 문자열을 정의한 후에는 `trans_choice` 함수를 사용하여 특정 "개수"에 맞는 문자열을 가져올 수 있습니다. 아래 예시에서 개수가 1보다 크므로 복수형 번역 문자열이 반환됩니다:

```
echo trans_choice('messages.apples', 10);
```

또한 복수형 문자열에도 플레이스홀더를 정의할 수 있으며, `trans_choice` 함수의 세 번째 인자로 치환할 값을 배열로 전달합니다:

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

`trans_choice` 함수에 전달한 정수 값을 출력하려면 내장된 `:count` 플레이스홀더를 이용하세요:

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이드하기

일부 패키지는 자체 언어 파일을 포함합니다. 패키지의 핵심 파일을 직접 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 두어 번역 문자열을 오버라이드할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지에서 `messages.php`의 영어 번역 문자열을 오버라이드하려면 다음 경로에 언어 파일을 생성합니다: `lang/vendor/hearthfire/en/messages.php`. 이 파일에는 변경하려는 번역 문자열만 정의하면 되고, 변경하지 않은 문자열은 패키지의 원본 언어 파일에서 계속 로드됩니다.