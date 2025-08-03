# 문자열 (Strings)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)

<a name="introduction"></a>
## 소개

Laravel은 문자열 값을 다루기 위한 다양한 함수를 포함하고 있습니다. 이러한 함수 중 다수는 프레임워크 자체에서 사용하지만, 필요에 따라 여러분의 애플리케이션에서도 편리하게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드



<a name="strings-method-list"></a>
### Strings

<div class="collection-method-list" markdown="1">

[\__](#method-__)
[class_basename](#method-class-basename)
[e](#method-e)
[preg_replace_array](#method-preg-replace-array)
[Str::after](#method-str-after)
[Str::afterLast](#method-str-after-last)
[Str::apa](#method-str-apa)
[Str::ascii](#method-str-ascii)
[Str::before](#method-str-before)
[Str::beforeLast](#method-str-before-last)
[Str::between](#method-str-between)
[Str::betweenFirst](#method-str-between-first)
[Str::camel](#method-camel-case)
[Str::charAt](#method-char-at)
[Str::chopStart](#method-str-chop-start)
[Str::chopEnd](#method-str-chop-end)
[Str::contains](#method-str-contains)
[Str::containsAll](#method-str-contains-all)
[Str::doesntContain](#method-str-doesnt-contain)
[Str::deduplicate](#method-deduplicate)
[Str::endsWith](#method-ends-with)
[Str::excerpt](#method-excerpt)
[Str::finish](#method-str-finish)
[Str::headline](#method-str-headline)
[Str::inlineMarkdown](#method-str-inline-markdown)
[Str::is](#method-str-is)
[Str::isAscii](#method-str-is-ascii)
[Str::isJson](#method-str-is-json)
[Str::isUlid](#method-str-is-ulid)
[Str::isUrl](#method-str-is-url)
[Str::isUuid](#method-str-is-uuid)
[Str::kebab](#method-kebab-case)
[Str::lcfirst](#method-str-lcfirst)
[Str::length](#method-str-length)
[Str::limit](#method-str-limit)
[Str::lower](#method-str-lower)
[Str::markdown](#method-str-markdown)
[Str::mask](#method-str-mask)
[Str::orderedUuid](#method-str-ordered-uuid)
[Str::padBoth](#method-str-padboth)
[Str::padLeft](#method-str-padleft)
[Str::padRight](#method-str-padright)
[Str::password](#method-str-password)
[Str::plural](#method-str-plural)
[Str::pluralStudly](#method-str-plural-studly)
[Str::position](#method-str-position)
[Str::random](#method-str-random)
[Str::remove](#method-str-remove)
[Str::repeat](#method-str-repeat)
[Str::replace](#method-str-replace)
[Str::replaceArray](#method-str-replace-array)
[Str::replaceFirst](#method-str-replace-first)
[Str::replaceLast](#method-str-replace-last)
[Str::replaceMatches](#method-str-replace-matches)
[Str::replaceStart](#method-str-replace-start)
[Str::replaceEnd](#method-str-replace-end)
[Str::reverse](#method-str-reverse)
[Str::singular](#method-str-singular)
[Str::slug](#method-str-slug)
[Str::snake](#method-str-snake-case)
[Str::squish](#method-str-squish)
[Str::start](#method-str-start)
[Str::startsWith](#method-starts-with)
[Str::studly](#method-studly-case)
[Str::substr](#method-str-substr)
[Str::substrCount](#method-str-substrcount)
[Str::substrReplace](#method-str-substrreplace)
[Str::swap](#method-str-swap)
[Str::take](#method-take)
[Str::title](#method-title-case)
[Str::toBase64](#method-str-to-base64)
[Str::transliterate](#method-str-transliterate)
[Str::trim](#method-str-trim)
[Str::ltrim](#method-str-ltrim)
[Str::rtrim](#method-str-rtrim)
[Str::ucfirst](#method-str-ucfirst)
[Str::ucsplit](#method-str-ucsplit)
[Str::upper](#method-str-upper)
[Str::ulid](#method-str-ulid)
[Str::unwrap](#method-str-unwrap)
[Str::uuid](#method-str-uuid)
[Str::uuid7](#method-str-uuid7)
[Str::wordCount](#method-str-word-count)
[Str::wordWrap](#method-str-word-wrap)
[Str::words](#method-str-words)
[Str::wrap](#method-str-wrap)
[str](#method-str)
[trans](#method-trans)
[trans_choice](#method-trans-choice)

</div>

<a name="fluent-strings-method-list"></a>
### Fluent Strings

<div class="collection-method-list" markdown="1">

[after](#method-fluent-str-after)
[afterLast](#method-fluent-str-after-last)
[apa](#method-fluent-str-apa)
[append](#method-fluent-str-append)
[ascii](#method-fluent-str-ascii)
[basename](#method-fluent-str-basename)
[before](#method-fluent-str-before)
[beforeLast](#method-fluent-str-before-last)
[between](#method-fluent-str-between)
[betweenFirst](#method-fluent-str-between-first)
[camel](#method-fluent-str-camel)
[charAt](#method-fluent-str-char-at)
[classBasename](#method-fluent-str-class-basename)
[chopStart](#method-fluent-str-chop-start)
[chopEnd](#method-fluent-str-chop-end)
[contains](#method-fluent-str-contains)
[containsAll](#method-fluent-str-contains-all)
[deduplicate](#method-fluent-str-deduplicate)
[dirname](#method-fluent-str-dirname)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[excerpt](#method-fluent-str-excerpt)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[headline](#method-fluent-str-headline)
[inlineMarkdown](#method-fluent-str-inline-markdown)
[is](#method-fluent-str-is)
[isAscii](#method-fluent-str-is-ascii)
[isEmpty](#method-fluent-str-is-empty)
[isNotEmpty](#method-fluent-str-is-not-empty)
[isJson](#method-fluent-str-is-json)
[isUlid](#method-fluent-str-is-ulid)
[isUrl](#method-fluent-str-is-url)
[isUuid](#method-fluent-str-is-uuid)
[kebab](#method-fluent-str-kebab)
[lcfirst](#method-fluent-str-lcfirst)
[length](#method-fluent-str-length)
[limit](#method-fluent-str-limit)
[lower](#method-fluent-str-lower)
[markdown](#method-fluent-str-markdown)
[mask](#method-fluent-str-mask)
[match](#method-fluent-str-match)
[matchAll](#method-fluent-str-match-all)
[isMatch](#method-fluent-str-is-match)
[newLine](#method-fluent-str-new-line)
[padBoth](#method-fluent-str-padboth)
[padLeft](#method-fluent-str-padleft)
[padRight](#method-fluent-str-padright)
[pipe](#method-fluent-str-pipe)
[plural](#method-fluent-str-plural)
[position](#method-fluent-str-position)
[prepend](#method-fluent-str-prepend)
[remove](#method-fluent-str-remove)
[repeat](#method-fluent-str-repeat)
[replace](#method-fluent-str-replace)
[replaceArray](#method-fluent-str-replace-array)
[replaceFirst](#method-fluent-str-replace-first)
[replaceLast](#method-fluent-str-replace-last)
[replaceMatches](#method-fluent-str-replace-matches)
[replaceStart](#method-fluent-str-replace-start)
[replaceEnd](#method-fluent-str-replace-end)
[scan](#method-fluent-str-scan)
[singular](#method-fluent-str-singular)
[slug](#method-fluent-str-slug)
[snake](#method-fluent-str-snake)
[split](#method-fluent-str-split)
[squish](#method-fluent-str-squish)
[start](#method-fluent-str-start)
[startsWith](#method-fluent-str-starts-with)
[stripTags](#method-fluent-str-strip-tags)
[studly](#method-fluent-str-studly)
[substr](#method-fluent-str-substr)
[substrReplace](#method-fluent-str-substrreplace)
[swap](#method-fluent-str-swap)
[take](#method-fluent-str-take)
[tap](#method-fluent-str-tap)
[test](#method-fluent-str-test)
[title](#method-fluent-str-title)
[toBase64](#method-fluent-str-to-base64)
[toHtmlString](#method-fluent-str-to-html-string)
[transliterate](#method-fluent-str-transliterate)
[trim](#method-fluent-str-trim)
[ltrim](#method-fluent-str-ltrim)
[rtrim](#method-fluent-str-rtrim)
[ucfirst](#method-fluent-str-ucfirst)
[ucsplit](#method-fluent-str-ucsplit)
[unwrap](#method-fluent-str-unwrap)
[upper](#method-fluent-str-upper)
[when](#method-fluent-str-when)
[whenContains](#method-fluent-str-when-contains)
[whenContainsAll](#method-fluent-str-when-contains-all)
[whenEmpty](#method-fluent-str-when-empty)
[whenNotEmpty](#method-fluent-str-when-not-empty)
[whenStartsWith](#method-fluent-str-when-starts-with)
[whenEndsWith](#method-fluent-str-when-ends-with)
[whenExactly](#method-fluent-str-when-exactly)
[whenNotExactly](#method-fluent-str-when-not-exactly)
[whenIs](#method-fluent-str-when-is)
[whenIsAscii](#method-fluent-str-when-is-ascii)
[whenIsUlid](#method-fluent-str-when-is-ulid)
[whenIsUuid](#method-fluent-str-when-is-uuid)
[whenTest](#method-fluent-str-when-test)
[wordCount](#method-fluent-str-word-count)
[words](#method-fluent-str-words)
[wrap](#method-fluent-str-wrap)

</div>

<a name="strings"></a>
## 문자열 (Strings)

<a name="method-__"></a>
#### `__()`

`__` 함수는 주어진 번역 문자열이나 번역 키를 [언어 파일]을 참고해 번역합니다:

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

만약 지정한 번역 문자열이나 키가 존재하지 않는다면, `__` 함수는 주어진 값을 그대로 반환합니다. 따라서 위 예제에서 `messages.welcome` 키가 없을 경우, `messages.welcome`가 반환됩니다.

<a name="method-class-basename"></a>
#### `class_basename()`

`class_basename` 함수는 네임스페이스를 제외한 클래스 이름을 반환합니다:

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()`

`e` 함수는 PHP의 `htmlspecialchars` 함수를 래핑하며, 기본적으로 `double_encode` 옵션이 `true`로 설정되어 있습니다:

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()`

`preg_replace_array` 함수는 문자열에서 주어진 패턴을 배열의 값들로 순차적으로 치환합니다:

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()`

`Str::after` 메서드는 문자열에서 주어진 값 뒤의 모든 내용을 반환합니다. 만약 값이 문자열에 없다면 전체 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()`

`Str::afterLast` 메서드는 문자열에서 주어진 값의 마지막 발생 이후 모든 내용을 반환합니다. 값이 없다면 전체 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
#### `Str::apa()`

`Str::apa` 메서드는 [APA 스타일](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 주어진 문자열을 타이틀 케이스로 변환합니다:

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()`

`Str::ascii` 메서드는 문자열을 가능한 한 ASCII 값으로 변환하려 시도합니다:

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()`

`Str::before` 메서드는 문자열에서 주어진 값 이전의 모든 내용을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()`

`Str::beforeLast` 메서드는 문자열에서 주어진 값의 마지막 발생 이전의 모든 내용을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
#### `Str::between()`

`Str::between` 메서드는 두 값 사이에 있는 문자열 부분을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()`

`Str::betweenFirst` 메서드는 두 값사이에서 가능한 가장 작은 문자열 조각을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()`

`Str::camel` 메서드는 주어진 문자열을 `camelCase` 형태로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
#### `Str::charAt()`

`Str::charAt` 메서드는 지정한 인덱스에 위치한 문자를 반환합니다. 인덱스가 경계를 벗어나면 `false`를 반환합니다:

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
#### `Str::chopStart()`

`Str::chopStart` 메서드는 문자열의 시작 부분에 주어진 값이 있을 경우, 그 첫 번째 발생만 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

배열을 두 번째 인수로 전달해도 됩니다. 문자열이 배열 중 어떤 값으로 시작하면 해당 값을 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()`

`Str::chopEnd` 메서드는 문자열의 끝 부분에 주어진 값이 있을 경우, 그 마지막 발생만 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

배열을 두 번째 인수로 전달해도 됩니다. 문자열이 배열 중 어떤 값으로 끝나면 해당 값을 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
#### `Str::contains()`

`Str::contains` 메서드는 문자열 내에 주어진 값이 포함되어 있는지 확인합니다. 기본적으로 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

값들을 배열로 전달해 해당 값들 중 하나라도 포함되어있는지 확인할 수도 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 끌 수도 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()`

`Str::containsAll` 메서드는 문자열이 배열 내 모든 값을 포함하는지 확인합니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수도 있습니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()`

`Str::doesntContain` 메서드는 문자열에 주어진 값이 포함되어 있지 않은지 확인합니다. 기본적으로 대소문자 구분합니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

값들을 배열로 전달해 배열의 어떤 값도 포함되어 있지 않은지 확인할 수도 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정해 대소문자 구분을 끌 수도 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
#### `Str::deduplicate()`

`Str::deduplicate` 메서드는 연속된 특정 문자를 단일 문자로 줄여줍니다. 기본 값은 공백 문자입니다:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

두 번째 인수로 다른 문자를 지정하여 중복을 제거할 수도 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-ends-with"></a>
#### `Str::endsWith()`

`Str::endsWith` 메서드는 문자열이 주어진 값으로 끝나는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

배열을 사용해 여러 값 중 하나로 끝나는지 검사할 수도 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()`

`Str::excerpt` 메서드는 주어진 문구의 첫 번째 인스턴스를 포함하는 문자열 요약을 추출합니다:

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` 옵션(기본값: 100)은 잘린 문자열 좌우에 표시할 문자 수를 지정합니다. `omission` 옵션으로 요약에 앞뒤로 붙일 문자열을 지정할 수도 있습니다:

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-str-finish"></a>
#### `Str::finish()`

`Str::finish` 메서드는 주어진 값으로 끝나지 않으면 문자열 끝에 단일 인스턴스를 추가합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-headline"></a>
#### `Str::headline()`

`Str::headline` 메서드는 카멜 케이스, 하이픈, 밑줄 등으로 구분된 문자열을 띄어쓰기로 구분하고 각 단어의 첫 글자를 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()`

`Str::inlineMarkdown` 메서드는 GitHub flavored Markdown을 [CommonMark](https://commonmark.thephpleague.com/)를 사용해 인라인 HTML로 변환합니다. `markdown` 메서드와 달리 최상위에 블록 레벨 요소를 포함하지 않습니다:

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

#### Markdown 보안

Markdown은 기본적으로 원시 HTML을 허용하지만, 이는 사용자 입력에 대한 크로스 사이트 스크립팅(XSS) 취약점을 발생시킬 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션으로 원시 HTML을 이스케이프하거나 제거할 수 있고, `allow_unsafe_links` 옵션으로 안전하지 않은 링크 허용 여부를 지정할 수 있습니다. 일부 원시 HTML을 허용해야 할 경우, 결과 Markdown을 HTML Purifier에 거치는 것이 안전합니다:

```php
use Illuminate\Support\Str;

Str::inlineMarkdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-str-is"></a>
#### `Str::is()`

`Str::is` 메서드는 주어진 문자열이 특정 패턴과 일치하는지 검사합니다. 와일드카드(*)를 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

`ignoreCase` 인수를 `true`로 설정하면 대소문자를 구분하지 않습니다:

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()`

`Str::isAscii` 메서드는 주어진 문자열이 7비트 ASCII 문자열인지 판별합니다:

```php
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()`

`Str::isJson` 메서드는 문자열이 유효한 JSON인지 판별합니다:

```php
use Illuminate\Support\Str;

$result = Str::isJson('[1,2,3]');

// true

$result = Str::isJson('{"first": "John", "last": "Doe"}');

// true

$result = Str::isJson('{first: "John", last: "Doe"}');

// false
```

<a name="method-str-is-url"></a>
#### `Str::isUrl()`

`Str::isUrl` 메서드는 문자열이 유효한 URL인지 판별합니다:

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

이 메서드는 다양한 프로토콜을 허용하지만, 특정 프로토콜만 허용하려면 두 번째 인수로 지정할 수 있습니다:

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()`

`Str::isUlid` 메서드는 문자열이 유효한 ULID인지 검사합니다:

```php
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()`

`Str::isUuid` 메서드는 문자열이 유효한 UUID인지 검사합니다:

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

<a name="method-kebab-case"></a>
#### `Str::kebab()`

`Str::kebab` 메서드는 주어진 문자열을 `kebab-case` 형식으로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()`

`Str::lcfirst` 메서드는 문자열의 첫 문자를 소문자로 변환해 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()`

`Str::length` 메서드는 문자열의 길이를 반환합니다:

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()`

`Str::limit` 메서드는 문자열을 지정한 길이로 자릅니다:

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

세 번째 인수로 자른 뒤에 덧붙일 문자열을 지정할 수 있습니다:

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

`preserveWords` 인수를 `true`로 설정하면 완전한 단어 경계에서 자릅니다:

```php
$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

// The quick...
```

<a name="method-str-lower"></a>
#### `Str::lower()`

`Str::lower` 메서드는 문자열을 모두 소문자로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
#### `Str::markdown()`

`Str::markdown` 메서드는 GitHub flavored Markdown을 [CommonMark](https://commonmark.thephpleague.com/)를 사용해 HTML로 변환합니다:

```php
use Illuminate\Support\Str;

$html = Str::markdown('# Laravel');

// <h1>Laravel</h1>

$html = Str::markdown('# Taylor <b>Otwell</b>', [
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### Markdown 보안

기본적으로 Markdown은 원시 HTML을 지원하여 사용자 입력에 XSS 취약점이 발생할 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라서, `html_input` 옵션으로 원시 HTML을 제거하거나 이스케이프하고, `allow_unsafe_links` 옵션으로 안전하지 않은 링크 허용 여부를 지정할 수 있습니다. 원시 HTML을 일부 허용해야 하면 HTML Purifier를 통해 결과를 정제하세요:

```php
use Illuminate\Support\Str;

Str::markdown('Inject: <script>alert("Hello XSS!");</script>', [
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-str-mask"></a>
#### `Str::mask()`

`Str::mask` 메서드는 문자열의 일부를 반복 문자로 가려서 이메일, 전화번호 같은 민감 정보를 숨길 때 사용합니다:

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

음수 인덱스를 세 번째 인수로 제공하면 문자열 끝에서부터 거리만큼 떨어진 위치부터 마스킹을 시작합니다:

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()`

`Str::orderedUuid` 메서드는 타임스탬프를 앞에 붙인 UUID를 생성합니다. 이 UUID는 인덱싱된 데이터베이스 열에 효율적으로 저장할 수 있으며, 생성된 UUID들은 시간순으로 정렬됩니다:

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()`

`Str::padBoth` 메서드는 PHP의 `str_pad`를 감싸서, 문자열의 양쪽을 지정된 문자열로 채워 최종 문자열이 원하는 길이에 도달하게 만듭니다:

```php
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()`

`Str::padLeft` 메서드는 문자열의 왼쪽을 지정된 문자열로 채워 최종 문자열이 원하는 길이에 도달하게 만듭니다:

```php
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()`

`Str::padRight` 메서드는 문자열의 오른쪽을 지정된 문자열로 채워 최종 문자열이 원하는 길이에 도달하게 만듭니다:

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
#### `Str::password()`

`Str::password` 메서드는 지정한 길이만큼 안전하고 무작위인 비밀번호를 생성합니다. 비밀번호는 문자, 숫자, 기호, 공백을 포함합니다. 기본 길이는 32자입니다:

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
#### `Str::plural()`

`Str::plural` 메서드는 단수형 단어 문자열을 복수형으로 변환합니다. Laravel의 복수형 처리기가 지원하는 [모든 언어](/docs/master/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

두 번째 인수로 정수를 전달하여 단수 또는 복수형을 반환할 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()`

`Str::pluralStudly` 메서드는 StudlyCase 형식의 단수형 단어를 복수형으로 변환합니다. Laravel 복수형 처리기의 [지원 언어](/docs/master/localization#pluralization-language)를 따릅니다:

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

두 번째 인수로 정수를 전달하여 단수 또는 복수형을 반환할 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>
#### `Str::position()`

`Str::position` 메서드는 문자열에서 특정 부분 문자열이 처음 발생하는 위치를 반환합니다. 부분 문자열이 없으면 `false`를 반환합니다:

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
#### `Str::random()`

`Str::random` 메서드는 지정한 길이만큼 무작위 문자열을 생성합니다. 이 함수는 PHP의 `random_bytes`를 사용합니다:

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

테스트 중에는 반환값을 "가짜"로 만들고 싶을 수 있는데, `createRandomStringsUsing` 메서드를 사용합니다:

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

다시 원래대로 무작위 문자열을 생성하려면 `createRandomStringsNormally` 메서드를 호출하세요:

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
#### `Str::remove()`

`Str::remove` 메서드는 문자열에서 주어진 값(또는 값 배열)을 제거합니다:

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

세 번째 인수에 `false`를 전달하면 대소문자를 무시하고 제거할 수 있습니다.

<a name="method-str-repeat"></a>
#### `Str::repeat()`

`Str::repeat` 메서드는 문자열을 지정한 횟수만큼 반복합니다:

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()`

`Str::replace` 메서드는 문자열에서 특정 부분을 다른 문자열로 치환합니다:

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

기본적으로 대소문자 구분이 적용되며, `caseSensitive` 인수로 설정을 바꿀 수 있습니다:

```php
Str::replace('Framework', 'Laravel', caseSensitive: false);
```

<a name="method-str-replace-array"></a>
#### `Str::replaceArray()`

`Str::replaceArray` 메서드는 배열의 값들로 문자열 내 특정 값을 순차적으로 치환합니다:

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()`

`Str::replaceFirst` 메서드는 문자열 내 첫 번째로 등장하는 값을 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()`

`Str::replaceLast` 메서드는 문자열 내 마지막으로 등장하는 값을 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()`

`Str::replaceMatches` 메서드는 주어진 패턴과 일치하는 문자열 부분을 주어진 문자열이나 클로저 결과로 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

클로저를 사용하면 일치하는 부분을 받아 치환할 값을 반환할 수 있습니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()`

`Str::replaceStart` 메서드는 문자열이 주어진 값으로 시작하면, 그 첫 번째 값을 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()`

`Str::replaceEnd` 메서드는 문자열이 주어진 값으로 끝나면, 그 마지막 값을 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

// Hello Laravel

$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-reverse"></a>
#### `Str::reverse()`

`Str::reverse` 메서드는 문자열을 뒤집어 반환합니다:

```php
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
#### `Str::singular()`

`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. `plural` 메서드와 마찬가지로 Laravel 복수형 처리기의 [모든 언어](/docs/master/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()`

`Str::slug` 메서드는 URL에 적합한 "슬러그" 문자열을 생성합니다:

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()`

`Str::snake` 메서드는 문자열을 `snake_case` 형태로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()`

`Str::squish` 메서드는 문자열 내 모든 불필요한 공백을 제거하며, 단어 사이 공백도 하나로 줄입니다:

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()`

`Str::start` 메서드는 문자열이 주어진 값으로 시작하지 않으면, 그 값을 추가합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()`

`Str::startsWith` 메서드는 문자열이 주어진 값으로 시작하는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

값 배열을 전달하면, 어떤 값으로든 시작하면 `true`를 반환합니다:

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()`

`Str::studly` 메서드는 문자열을 `StudlyCase` 형태로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()`

`Str::substr` 메서드는 주어진 시작 위치와 길이로 문자열의 일부를 반환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()`

`Str::substrCount` 메서드는 문자열 내 특정 값이 등장하는 횟수를 반환합니다:

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()`

`Str::substrReplace` 메서드는 문자열의 주어진 위치부터 주어진 길이만큼 텍스트를 치환하거나 삽입합니다. 네 번째 인수에 0을 넣으면 기존 문자를 대체하지 않고 삽입합니다:

```php
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()`

`Str::swap` 메서드는 PHP의 `strtr` 함수를 사용해 문자열 내 여러 값을 한 번에 치환합니다:

```php
use Illuminate\Support\Str;

$string = Str::swap([
    'Tacos' => 'Burritos',
    'great' => 'fantastic',
], 'Tacos are great!');

// Burritos are fantastic!
```

<a name="method-take"></a>
#### `Str::take()`

`Str::take` 메서드는 문자열의 처음부터 지정한 문자 수 만큼 반환합니다:

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
#### `Str::title()`

`Str::title` 메서드는 문자열을 `Title Case`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
#### `Str::toBase64()`

`Str::toBase64` 메서드는 문자열을 Base64 인코딩 형식으로 변환합니다:

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
#### `Str::transliterate()`

`Str::transliterate` 메서드는 문자열을 가능한 한 가까운 ASCII 표현으로 변환하려 시도합니다:

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
#### `Str::trim()`

`Str::trim` 메서드는 PHP 기본 `trim`과 달리 유니코드 공백까지 포함해 문자열 양 끝의 공백(또는 지정한 문자열)을 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
#### `Str::ltrim()`

`Str::ltrim` 메서드는 문자열 왼쪽 끝에서 공백(또는 지정 문자열)을 제거합니다. PHP 기본 `ltrim`과 달리 유니코드 공백도 처리합니다:

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
#### `Str::rtrim()`

`Str::rtrim` 메서드는 문자열 오른쪽 끝에서 공백(또는 지정 문자열)을 제거합니다. PHP 기본 `rtrim`과 달리 유니코드 공백도 처리합니다:

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()`

`Str::ucfirst` 메서드는 문자열 첫 문자를 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()`

`Str::ucsplit` 메서드는 대문자 문자를 기준으로 문자열을 배열로 분할합니다:

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-upper"></a>
#### `Str::upper()`

`Str::upper` 메서드는 문자열을 모두 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()`

`Str::ulid` 메서드는 간결하고 시간 순서대로 정렬되는 유니크 식별자인 ULID를 생성합니다:

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

해당 ULID가 생성된 시간 정보를 담은 `Illuminate\Support\Carbon` 인스턴스를 원하면 Laravel Carbon 통합의 `createFromId` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

테스트 시 반환값을 가짜로 만들려면 `createUlidsUsing` 메서드를 쓰세요:

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

기본 ULID 생성을 복원하려면 `createUlidsNormally` 메서드를 호출하세요:

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
#### `Str::unwrap()`

`Str::unwrap` 메서드는 문자열의 시작과 끝에서 지정한 문자열들을 제거합니다:

```php
use Illuminate\Support\Str;

Str::unwrap('-Laravel-', '-');

// Laravel

Str::unwrap('{framework: "Laravel"}', '{', '}');

// framework: "Laravel"
```

<a name="method-str-uuid"></a>
#### `Str::uuid()`

`Str::uuid` 메서드는 UUID (버전 4)를 생성합니다:

```php
use Illuminate\Support\Str;

return (string) Str::uuid();
```

테스트 중에는 `createUuidsUsing` 메서드를 이용해 반환값을 가짜로 처리할 수 있습니다:

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

다시 기본 UUID 생성을 복원하려면 `createUuidsNormally` 메서드를 호출하세요:

```php
Str::createUuidsNormally();
```

<a name="method-str-uuid7"></a>
#### `Str::uuid7()`

`Str::uuid7` 메서드는 버전 7 UUID를 생성합니다:

```php
use Illuminate\Support\Str;

return (string) Str::uuid7();
```

`DateTimeInterface` 구현 객체를 전달해 생성하는 UUID의 타임스탬프를 특정할 수도 있습니다:

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()`

`Str::wordCount` 메서드는 문자열에 포함된 단어 수를 반환합니다:

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()`

`Str::wordWrap` 메서드는 문자열을 지정된 문자 수마다 줄바꿈합니다:

```php
use Illuminate\Support\Str;

$text = "The quick brown fox jumped over the lazy dog."

Str::wordWrap($text, characters: 20, break: "<br />\n");

/*
The quick brown fox<br />
jumped over the lazy<br />
dog.
*/
```

<a name="method-str-words"></a>
#### `Str::words()`

`Str::words` 메서드는 문자열의 단어 수를 제한합니다. 세 번째 인수로 잘린 문자열 뒤에 덧붙일 문자열을 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
#### `Str::wrap()`

`Str::wrap` 메서드는 문자열을 지정한 문자열 또는 문자열 쌍으로 감쌉니다:

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
#### `str()`

`str` 함수는 주어진 문자열로부터 새로운 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of` 메서드와 동일합니다:

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

인수를 넘기지 않으면 `Illuminate\Support\Str` 인스턴스를 반환합니다:

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()`

`trans` 함수는 주어진 번역 키를 [언어 파일]을 참고해 번역합니다:

```php
echo trans('messages.welcome');
```

해당 키가 존재하지 않으면, 키 자체를 반환합니다.

<a name="method-trans-choice"></a>
#### `trans_choice()`

`trans_choice` 함수는 주어진 번역 키를 활용하여 복수형 번역을 수행합니다:

```php
echo trans_choice('messages.notifications', $unreadCount);
```

키가 존재하지 않으면, 키 자체를 반환합니다.

<a name="fluent-strings"></a>
## Fluent Strings

Fluent Strings는 좀 더 유창하고 객체지향적인 방식으로 문자열을 다룰 수 있는 인터페이스입니다. 여러 문자열 조작 메서드를 메서드 체이닝으로 연결할 수 있어, 전통적인 함수 호출보다 읽기 쉽고 편리합니다.

<a name="method-fluent-str-after"></a>
#### `after`

`after` 메서드는 문자열 내 주어진 값 뒤의 모든 내용을 반환합니다. 값이 없으면 전체 문자열이 반환됩니다:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
#### `afterLast`

`afterLast` 메서드는 문자열 내 주어진 값 마지막 발생 뒤의 모든 내용을 반환합니다. 값이 없으면 전체 문자열이 반환됩니다:

```php
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-apa"></a>
#### `apa`

`apa` 메서드는 [APA 스타일](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 문자열을 타이틀 케이스로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->apa();

// A Nice Title Uses the Correct Case
```

<a name="method-fluent-str-append"></a>
#### `append`

`append` 메서드는 문자열 뒤에 값을 덧붙입니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
#### `ascii`

`ascii` 메서드는 문자열을 가능하면 ASCII 문자열로 변환하려 시도합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
#### `basename`

`basename` 메서드는 문자열의 마지막 파일명 또는 경로 요소를 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

필요에 따라 확장자명을 제거할 문자열로 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
#### `before`

`before` 메서드는 문자열 내 주어진 값 이전 모든 내용을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
#### `beforeLast`

`beforeLast` 메서드는 문자열 내 주어진 값 마지막 발생 이전 모든 내용을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
#### `between`

`between` 메서드는 두 값 사이 부분 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
#### `betweenFirst`

`betweenFirst` 메서드는 두 값 사이 가능한 가장 작은 부분 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
#### `camel`

`camel` 메서드는 문자열을 `camelCase` 형태로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// 'fooBar'
```

<a name="method-fluent-str-char-at"></a>
#### `charAt`

`charAt` 메서드는 지정한 위치의 문자를 반환합니다. 인덱스가 범위를 벗어나면 `false`를 반환합니다:

```php
use Illuminate\Support\Str;

$character = Str::of('This is my name.')->charAt(6);

// 's'
```

<a name="method-fluent-str-class-basename"></a>
#### `classBasename`

`classBasename` 메서드는 네임스페이스를 제외한 클래스 이름을 반환합니다:

```php
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// 'Baz'
```

<a name="method-fluent-str-chop-start"></a>
#### `chopStart`

`chopStart` 메서드는 문자열의 시작 부분에 특정 값이 있으면 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopStart('https://');

// 'laravel.com'
```

배열을 전달하면, 배열 내 어떤 값으로 시작하면 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopStart(['https://', 'http://']);

// 'laravel.com'
```

<a name="method-fluent-str-chop-end"></a>
#### `chopEnd`

`chopEnd` 메서드는 문자열 끝 부분에 특정 값이 있으면 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopEnd('.com');

// 'https://laravel'
```

배열을 전달하면 배열의 값으로 끝나면 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopEnd(['.com', '.io']);

// 'http://laravel'
```

<a name="method-fluent-str-contains"></a>
#### `contains`

`contains` 메서드는 문자열이 주어진 값을 포함하는지 판단합니다. 기본적으로 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

배열을 인수로 주어 어느 하나라도 포함하는지 확인할 수도 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

`ignoreCase`를 `true`로 설정해 대소문자 구분을 끌 수도 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('MY', ignoreCase: true);

// true
```

<a name="method-fluent-str-contains-all"></a>
#### `containsAll`

`containsAll` 메서드는 문자열이 주어진 배열 내 모든 값을 포함하는지 판단합니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

`ignoreCase`를 `true`로 설정해 대소문자 구분을 끌 수도 있습니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-fluent-str-deduplicate"></a>
#### `deduplicate`

`deduplicate` 메서드는 연속된 특정 문자를 단일 문자로 줄입니다. 기본값은 공백입니다:

```php
use Illuminate\Support\Str;

$result = Str::of('The   Laravel   Framework')->deduplicate();

// The Laravel Framework
```

두 번째 인수로 다른 문자를 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::of('The---Laravel---Framework')->deduplicate('-');

// The-Laravel-Framework
```

<a name="method-fluent-str-dirname"></a>
#### `dirname`

`dirname` 메서드는 문자열에서 상위 디렉토리 경로를 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

두 번째 인수로 상위 디렉토리 몇 단계까지 반환할지 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-ends-with"></a>
#### `endsWith`

`endsWith` 메서드는 문자열이 주어진 값으로 끝나는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

배열을 인수로 받아 한 값이라도 해당하면 `true`를 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith(['name', 'foo']);

// true

$result = Str::of('This is my name')->endsWith(['this', 'foo']);

// false
```

<a name="method-fluent-str-exactly"></a>
#### `exactly`

`exactly` 메서드는 문자열이 완전히 일치하는지 검사합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-excerpt"></a>
#### `excerpt`

`excerpt` 메서드는 문자열에서 주어진 구문의 첫 번째 발생 부분을 포함하는 요약문을 추출합니다:

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius`(기본값 100)와 `omission` 옵션은 원하는 대로 조정할 수 있습니다:

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-fluent-str-explode"></a>
#### `explode`

`explode` 메서드는 구분자로 문자열을 분할하고, 결과를 컬렉션으로 반환합니다:

```php
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
#### `finish`

`finish` 메서드는 문자열이 주어진 값으로 끝나지 않으면 추가합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-headline"></a>
#### `headline`

`headline` 메서드는 카멜 케이스, 하이픈, 밑줄 등으로 구분된 문자열을 띄어쓰기로 구분하고 각 단어 첫 글자를 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-inline-markdown"></a>
#### `inlineMarkdown`

`inlineMarkdown` 메서드는 GitHub flavored Markdown을 인라인 HTML로 변환합니다:

```php
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

#### Markdown 보안

기본적으로 Markdown은 원시 HTML을 허용하여 XSS 취약점이 발생할 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)를 참고해 `html_input` 및 `allow_unsafe_links` 옵션을 설정하세요. 필요 시 HTML Purifier를 통해 결과를 정제해야 합니다:

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->inlineMarkdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// Inject: alert(&quot;Hello XSS!&quot;);
```

<a name="method-fluent-str-is"></a>
#### `is`

`is` 메서드는 문자열이 특정 패턴과 일치하는지 확인합니다. 와일드카드(*) 지원:

```php
use Illuminate\Support\Str;

$matches = Str::of('foobar')->is('foo*');

// true

$matches = Str::of('foobar')->is('baz*');

// false
```

<a name="method-fluent-str-is-ascii"></a>
#### `isAscii`

`isAscii` 메서드는 문자열이 7비트 ASCII인지 판단합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('Taylor')->isAscii();

// true

$result = Str::of('ü')->isAscii();

// false
```

<a name="method-fluent-str-is-empty"></a>
#### `isEmpty`

`isEmpty` 메서드는 문자열이 비어있는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isEmpty();

// true

$result = Str::of('Laravel')->trim()->isEmpty();

// false
```

<a name="method-fluent-str-is-not-empty"></a>
#### `isNotEmpty`

`isNotEmpty` 메서드는 문자열이 비어있지 않은지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-json"></a>
#### `isJson`

`isJson` 메서드는 문자열이 유효한 JSON인지 검사합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('[1,2,3]')->isJson();

// true

$result = Str::of('{"first": "John", "last": "Doe"}')->isJson();

// true

$result = Str::of('{first: "John", last: "Doe"}')->isJson();

// false
```

<a name="method-fluent-str-is-ulid"></a>
#### `isUlid`

`isUlid` 메서드는 문자열이 ULID인지 검사합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-url"></a>
#### `isUrl`

`isUrl` 메서드는 문자열이 URL인지 검사합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('http://example.com')->isUrl();

// true

$result = Str::of('Taylor')->isUrl();

// false
```

특정 프로토콜만 허용하려면 배열로 지정하세요:

```php
$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

<a name="method-fluent-str-is-uuid"></a>
#### `isUuid`

`isUuid` 메서드는 문자열이 UUID인지 검사합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

<a name="method-fluent-str-kebab"></a>
#### `kebab`

`kebab` 메서드는 문자열을 `kebab-case`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
#### `lcfirst`

`lcfirst` 메서드는 첫 글자만 소문자로 변환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```

<a name="method-fluent-str-length"></a>
#### `length`

`length` 메서드는 문자열 길이를 반환합니다:

```php
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
#### `limit`

`limit` 메서드는 문자열을 지정 길이까지 자르고 필요한 경우 문자열을 덧붙입니다:

```php
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

문자열 덧붙임은 두 번째 인수로 변경 가능하며, `preserveWords` 인수를 통해 단어 단위 자르기도 지원합니다:

```php
$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

$truncated = Str::of('The quick brown fox')->limit(12, preserveWords: true);
```

<a name="method-fluent-str-lower"></a>
#### `lower`

`lower` 메서드는 문자열을 소문자로 변환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-markdown"></a>
#### `markdown`

`markdown` 메서드는 GitHub flavored Markdown을 HTML로 변환합니다:

```php
use Illuminate\Support\Str;

$html = Str::of('# Laravel')->markdown();

// <h1>Laravel</h1>

$html = Str::of('# Taylor <b>Otwell</b>')->markdown([
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### Markdown 보안

Markdown 원시 HTML 지원으로 인한 XSS 취약점은 [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라 `html_input` 및 `allow_unsafe_links` 옵션 조절로 보완해야 하며, 필요 시 HTML Purifier 사용을 권장합니다:

```php
use Illuminate\Support\Str;

Str::of('Inject: <script>alert("Hello XSS!");</script>')->markdown([
    'html_input' => 'strip',
    'allow_unsafe_links' => false,
]);

// <p>Inject: alert(&quot;Hello XSS!&quot;);</p>
```

<a name="method-fluent-str-mask"></a>
#### `mask`

`mask` 메서드는 문자열 일부를 지정 문자로 가립니다:

```php
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

음수 인수로 문자열 끝에서부터 거리를 지정할 수도 있습니다:

```php
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
#### `match`

`match` 메서드는 패턴에 매치되는 문자열 부분을 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->match('/bar/');

// 'bar'

$result = Str::of('foo bar')->match('/foo (.*)/');

// 'bar'
```

<a name="method-fluent-str-match-all"></a>
#### `matchAll`

`matchAll` 메서드는 패턴에 매치되는 모든 부분 문자열을 컬렉션으로 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

매칭 그룹이 있으면 첫 그룹 매치 결과만 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

매치가 없으면 빈 컬렉션을 반환합니다.

<a name="method-fluent-str-is-match"></a>
#### `isMatch`

`isMatch` 메서드는 문자열이 정규식과 일치하는지 `true`/`false`로 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->isMatch('/foo (.*)/');

// true

$result = Str::of('laravel')->isMatch('/foo (.*)/');

// false
```

<a name="method-fluent-str-new-line"></a>
#### `newLine`

`newLine` 메서드는 문자열 끝에 줄바꿈 문자를 추가합니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
#### `padBoth`

`padBoth` 메서드는 문자열 양쪽을 지정 문자열로 채워 최종 길이를 만듭니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padBoth(10, '_');

// '__James___'

$padded = Str::of('James')->padBoth(10);

// '  James   '
```

<a name="method-fluent-str-padleft"></a>
#### `padLeft`

`padLeft` 메서드는 문자열 왼쪽을 지정 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padLeft(10, '-=');

// '-=-=-James'

$padded = Str::of('James')->padLeft(10);

// '     James'
```

<a name="method-fluent-str-padright"></a>
#### `padRight`

`padRight` 메서드는 문자열 오른쪽을 지정 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padRight(10, '-');

// 'James-----'

$padded = Str::of('James')->padRight(10);

// 'James     '
```

<a name="method-fluent-str-pipe"></a>
#### `pipe`

`pipe` 메서드는 현재 문자열 값을 주어진 호출 가능한(callable) 함수에 전달해 변환합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$hash = Str::of('Laravel')->pipe('md5')->prepend('Checksum: ');

// 'Checksum: a5c95b86291ea299fcbe64458ed12702'

$closure = Str::of('foo')->pipe(function (Stringable $str) {
    return 'bar';
});

// 'bar'
```

<a name="method-fluent-str-plural"></a>
#### `plural`

`plural` 메서드는 단수형 단어를 복수형으로 변환합니다:

```php
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

두 번째 인수로 정수를 주면 단수 또는 복수형을 반환할 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

<a name="method-fluent-str-position"></a>
#### `position`

`position` 메서드는 부분 문자열이 처음 나타나는 위치를 반환합니다. 없으면 `false` 반환:

```php
use Illuminate\Support\Str;

$position = Str::of('Hello, World!')->position('Hello');

// 0

$position = Str::of('Hello, World!')->position('W');

// 7
```

<a name="method-fluent-str-prepend"></a>
#### `prepend`

`prepend` 메서드는 문자열 앞에 값을 추가합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
#### `remove`

`remove` 메서드는 문자열에서 특정 값(또는 값 배열)을 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite');

// Arkansas is beautiful!
```

두 번째 인수에 `false`를 주면 대소문자를 무시합니다.

<a name="method-fluent-str-repeat"></a>
#### `repeat`

`repeat` 메서드는 문자열을 지정 횟수만큼 반복합니다:

```php
use Illuminate\Support\Str;

$repeated = Str::of('a')->repeat(5);

// aaaaa
```

<a name="method-fluent-str-replace"></a>
#### `replace`

`replace` 메서드는 특정 문자열을 다른 문자열로 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

기본적으로 대소문자를 구분하며, 옵션으로 구분 여부 설정 가능:

```php
$replaced = Str::of('macOS 13.x')->replace(
    'macOS', 'iOS', caseSensitive: false
);
```

<a name="method-fluent-str-replace-array"></a>
#### `replaceArray`

`replaceArray` 메서드는 배열 값으로 특정 문자열을 순차적으로 치환합니다:

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
#### `replaceFirst`

`replaceFirst` 메서드는 문자열 내 첫 번째 발생하는 값만 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
#### `replaceLast`

`replaceLast` 메서드는 문자열 내 마지막 발생하는 값만 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
#### `replaceMatches`

`replaceMatches` 메서드는 패턴에 일치하는 모든 부분을 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

클로저를 사용하면 매치된 부분마다 변환 로직을 적용할 수 있습니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-replace-start"></a>
#### `replaceStart`

`replaceStart` 메서드는 문자열 시작 부분의 특정 값만 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceStart('Hello', 'Laravel');

// Laravel World

$replaced = Str::of('Hello World')->replaceStart('World', 'Laravel');

// Hello World
```

<a name="method-fluent-str-replace-end"></a>
#### `replaceEnd`

`replaceEnd` 메서드는 문자열 끝 부분의 특정 값만 치환합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

// Hello Laravel

$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

// Hello World
```

<a name="method-fluent-str-scan"></a>
#### `scan`

`scan` 메서드는 [`sscanf` PHP 함수](https://www.php.net/manual/en/function.sscanf.php) 형식에 맞춰 입력을 파싱하고, 결과를 컬렉션으로 반환합니다:

```php
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
#### `singular`

`singular` 메서드는 문자열을 단수형으로 변환합니다:

```php
use Illuminate\Support\Str;

$singular = Str::of('cars')->singular();

// car

$singular = Str::of('children')->singular();

// child
```

<a name="method-fluent-str-slug"></a>
#### `slug`

`slug` 메서드는 URL 친화적인 슬러그 문자열을 생성합니다:

```php
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
#### `snake`

`snake` 메서드는 문자열을 `snake_case` 형태로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
#### `split`

`split` 메서드는 정규식에 따라 문자열을 분할하고 컬렉션으로 반환합니다:

```php
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
#### `squish`

`squish` 메서드는 불필요한 모든 공백을 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
#### `start`

`start` 메서드는 문자열이 특정 값으로 시작하지 않으면 추가합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->start('/');

// /this/string

$adjusted = Str::of('/this/string')->start('/');

// /this/string
```

<a name="method-fluent-str-starts-with"></a>
#### `startsWith`

`startsWith` 메서드는 문자열이 특정 값으로 시작하는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

배열을 전달하면 어느 하나라도 해당하면 `true` 반환:

```php
$result = Str::of('This is my name')->startsWith(['This', 'That', 'There']);

// true
```

<a name="method-fluent-str-strip-tags"></a>
#### `stripTags`

`stripTags` 메서드는 문자열에서 HTML과 PHP 태그를 제거합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags();

// Taylor Otwell

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags('<b>');

// Taylor <b>Otwell</b>
```

<a name="method-fluent-str-studly"></a>
#### `studly`

`studly` 메서드는 문자열을 `StudlyCase` 형태로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
#### `substr`

`substr` 메서드는 지정된 시작 위치와 길이만큼 문자열 일부를 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Laravel Framework')->substr(8);

// Framework

$string = Str::of('Laravel Framework')->substr(8, 5);

// Frame
```

<a name="method-fluent-str-substrreplace"></a>
#### `substrReplace`

`substrReplace` 메서드는 지정 위치와 길이만큼 문자열 일부를 치환합니다. 길이로 0을 주면 기존 문자를 덮어쓰지 않고 삽입합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-swap"></a>
#### `swap`

`swap` 메서드는 PHP `strtr` 함수를 활용해 여러 문자열을 동시에 치환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Tacos are great!')
    ->swap([
        'Tacos' => 'Burritos',
        'great' => 'fantastic',
    ]);

// Burritos are fantastic!
```

<a name="method-fluent-str-take"></a>
#### `take`

`take` 메서드는 문자열 처음부터 지정된 수만큼 부분 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$taken = Str::of('Build something amazing!')->take(5);

// Build
```

<a name="method-fluent-str-tap"></a>
#### `tap`

`tap` 메서드는 문자열을 클로저에 전달하지만 원본 문자열에는 영향을 주지 않고, 클로저 실행 후 원본 문자열을 반환합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Laravel')
    ->append(' Framework')
    ->tap(function (Stringable $string) {
        dump('String after append: '.$string);
    })
    ->upper();

// LARAVEL FRAMEWORK
```

<a name="method-fluent-str-test"></a>
#### `test`

`test` 메서드는 문자열이 주어진 정규식에 부합하는지 `true`/`false`로 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
#### `title`

`title` 메서드는 문자열을 `Title Case`로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-to-base64"></a>
#### `toBase64`

`toBase64` 메서드는 문자열을 Base64 인코딩 형식으로 변환합니다:

```php
use Illuminate\Support\Str;

$base64 = Str::of('Laravel')->toBase64();

// TGFyYXZlbA==
```

<a name="method-fluent-str-to-html-string"></a>
#### `toHtmlString`

`toHtmlString` 메서드는 문자열을 `Illuminate\Support\HtmlString` 인스턴스로 변환해, Blade 템플릿에서 이스케이프 없이 출력하도록 합니다:

```php
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-fluent-str-transliterate"></a>
#### `transliterate`

`transliterate` 메서드는 문자열을 가능한 가까운 ASCII 표현으로 변환하려 시도합니다:

```php
use Illuminate\Support\Str;

$email = Str::of('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ')->transliterate()

// 'test@laravel.com'
```

<a name="method-fluent-str-trim"></a>
#### `trim`

`trim` 메서드는 문자열 양 끝의 공백(또는 지정한 문자열)을 제거합니다. PHP의 `trim`과 달리 유니코드 공백도 삭제합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ltrim"></a>
#### `ltrim`

`ltrim` 메서드는 문자열 왼쪽의 공백(또는 지정한 문자열)을 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```

<a name="method-fluent-str-rtrim"></a>
#### `rtrim`

`rtrim` 메서드는 문자열 오른쪽의 공백(또는 지정한 문자열)을 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
#### `ucfirst`

`ucfirst` 메서드는 문자열 첫 글자를 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
#### `ucsplit`

`ucsplit` 메서드는 문자열을 대문자 기준으로 분할해 컬렉션으로 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo', 'Bar'])
```

<a name="method-fluent-str-unwrap"></a>
#### `unwrap`

`unwrap` 메서드는 문자열 앞뒤의 지정 문자열을 제거합니다:

```php
use Illuminate\Support\Str;

Str::of('-Laravel-')->unwrap('-');

// Laravel

Str::of('{framework: "Laravel"}')->unwrap('{', '}');

// framework: "Laravel"
```

<a name="method-fluent-str-upper"></a>
#### `upper`

`upper` 메서드는 문자열을 모두 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
#### `when`

`when` 메서드는 조건이 참일 때만 클로저를 실행하며, 해당 클로저에 fluent 문자열 인스턴스를 전달합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Taylor')
    ->when(true, function (Stringable $string) {
        return $string->append(' Otwell');
    });

// 'Taylor Otwell'
```

필요 시 세 번째 인수로 조건이 거짓일 때 실행할 클로저도 전달할 수 있습니다.

<a name="method-fluent-str-when-contains"></a>
#### `whenContains`

`whenContains` 메서드는 문자열이 특정 값을 포함하면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains('tony', function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

세 번째 인수로 클로저를 넣으면 포함하지 않을 때 실행합니다. 배열로 복수 값도 검사할 수 있습니다.

<a name="method-fluent-str-when-contains-all"></a>
#### `whenContainsAll`

`whenContainsAll` 메서드는 문자열이 배열 내 모든 값을 포함하면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContainsAll(['tony', 'stark'], function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

<a name="method-fluent-str-when-empty"></a>
#### `whenEmpty`

`whenEmpty` 메서드는 문자열이 비어있으면 클로저를 실행합니다. 클로저 반환값은 메서드 반환값이 됩니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('  ')->trim()->whenEmpty(function (Stringable $string) {
    return $string->prepend('Laravel');
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-empty"></a>
#### `whenNotEmpty`

`whenNotEmpty` 메서드는 문자열이 비어있지 않으면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Framework')->whenNotEmpty(function (Stringable $string) {
    return $string->prepend('Laravel ');
});

// 'Laravel Framework'
```

<a name="method-fluent-str-when-starts-with"></a>
#### `whenStartsWith`

`whenStartsWith` 메서드는 문자열이 특정 값으로 시작하면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenStartsWith('disney', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-ends-with"></a>
#### `whenEndsWith`

`whenEndsWith` 메서드는 문자열이 특정 값으로 끝나면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('disney world')->whenEndsWith('world', function (Stringable $string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-exactly"></a>
#### `whenExactly`

`whenExactly` 메서드는 문자열이 정확히 특정 문자열과 일치하면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-exactly"></a>
#### `whenNotExactly`

`whenNotExactly` 메서드는 문자열이 특정 문자열과 정확히 일치하지 않으면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('framework')->whenNotExactly('laravel', function (Stringable $string) {
    return $string->title();
});

// 'Framework'
```

<a name="method-fluent-str-when-is"></a>
#### `whenIs`

`whenIs` 메서드는 문자열이 패턴과 일치하면 클로저를 실행합니다. 와일드카드(*) 지원:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('foo/bar')->whenIs('foo/*', function (Stringable $string) {
    return $string->append('/baz');
});

// 'foo/bar/baz'
```

<a name="method-fluent-str-when-is-ascii"></a>
#### `whenIsAscii`

`whenIsAscii` 메서드는 문자열이 7비트 ASCII면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel')->whenIsAscii(function (Stringable $string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is-ulid"></a>
#### `whenIsUlid`

`whenIsUlid` 메서드는 문자열이 ULID이면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
#### `whenIsUuid`

`whenIsUuid` 메서드는 문자열이 UUID이면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// 'a0a2a2d2'
```

<a name="method-fluent-str-when-test"></a>
#### `whenTest`

`whenTest` 메서드는 문자열이 주어진 정규식과 일치하면 클로저를 실행합니다:

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('laravel framework')->whenTest('/laravel/', function (Stringable $string) {
    return $string->title();
});

// 'Laravel Framework'
```

<a name="method-fluent-str-word-count"></a>
#### `wordCount`

`wordCount` 메서드는 문자열 내 단어 수를 반환합니다:

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
#### `words`

`words` 메서드는 문자열의 단어 수를 제한합니다. 필요하면 자른 뒤 덧붙일 문자열도 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-fluent-str-wrap"></a>
#### `wrap`

`wrap` 메서드는 문자열 앞뒤에 지정 문자열이나 문자열 쌍을 덧붙입니다:

```php
use Illuminate\Support\Str;

Str::of('Laravel')->wrap('"');

// "Laravel"

Str::is('is')->wrap(before: 'This ', after: ' Laravel!');

// This is Laravel!
```