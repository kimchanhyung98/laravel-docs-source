# 문자열 (Strings)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)

<a name="introduction"></a>
## 소개

라라벨에는 문자열 값을 다루기 위한 다양한 함수들이 포함되어 있습니다. 이 함수들 중 상당수는 프레임워크 내부적으로 사용되지만, 필요하다면 여러분의 애플리케이션에서도 언제든지 편리하게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드



<a name="strings-method-list"></a>
### 문자열 관련 함수

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
[Str::match](#method-str-match)
[Str::matchAll](#method-str-match-all)
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
[Str::snake](#method-snake-case)
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
### 플루언트 문자열(Fluent Strings)

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
[decrypt](#method-fluent-str-decrypt)
[deduplicate](#method-fluent-str-deduplicate)
[dirname](#method-fluent-str-dirname)
[encrypt](#method-fluent-str-encrypt)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[excerpt](#method-fluent-str-excerpt)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[hash](#method-fluent-str-hash)
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
[toUri](#method-fluent-str-to-uri)
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
## 문자열

<a name="method-__"></a>
#### `__()`

`__` 함수는 지정한 번역 문자열 또는 번역 키를 [언어 파일](/docs/12.x/localization)을 사용하여 번역합니다.

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

만약 지정한 번역 문자열이나 키가 존재하지 않는 경우, `__` 함수는 전달된 값을 그대로 반환합니다. 따라서 위 예시에서 해당 번역 키가 존재하지 않으면, `__` 함수는 `messages.welcome`을 반환하게 됩니다.

<a name="method-class-basename"></a>
#### `class_basename()`

`class_basename` 함수는 전달한 클래스의 네임스페이스를 제외한 클래스 이름만 반환합니다.

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()`

`e` 함수는 PHP의 `htmlspecialchars` 함수를 실행하며, `double_encode` 옵션이 기본적으로 `true`로 설정되어 있습니다.

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()`

`preg_replace_array` 함수는 문자열에 있는 지정한 패턴을 배열에 담긴 값으로 순차적으로 치환합니다.

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()`

`Str::after` 메서드는 문자열에서 지정한 값 이후의 모든 내용을 반환합니다. 만약 지정된 값이 문자열 내에 존재하지 않으면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()`

`Str::afterLast` 메서드는 문자열에서 지정한 값이 마지막으로 나타나는 이후의 모든 내용을 반환합니다. 만약 해당 값이 문자열에 없으면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
#### `Str::apa()`

`Str::apa` 메서드는 [APA 가이드라인](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 주어진 문자열을 제목 표기법(Title Case)으로 변환합니다.

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()`

`Str::ascii` 메서드는 주어진 문자열을 ASCII 문자로 변환(음역)하려고 시도합니다.

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()`

`Str::before` 메서드는 문자열에서 지정한 값 이전의 모든 내용을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()`

`Str::beforeLast` 메서드는 문자열 내에서 지정한 값이 마지막으로 나타나기 이전의 모든 내용을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
#### `Str::between()`

`Str::between` 메서드는 두 값 사이에 위치한 문자열 부분을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()`

`Str::betweenFirst` 메서드는 두 값 사이에 위치한 가장 짧은 문자열 부분을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()`

`Str::camel` 메서드는 전달된 문자열을 `camelCase` 형태로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
#### `Str::charAt()`

`Str::charAt` 메서드는 지정한 인덱스(위치)에 해당하는 문자를 반환합니다. 만약 인덱스가 범위를 벗어나면 `false`를 반환합니다.

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
#### `Str::chopStart()`

`Str::chopStart` 메서드는 문자열의 시작 부분에 지정한 값이 있을 경우, 처음 한 번만 해당 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

두 번째 인자로 배열을 전달할 수도 있습니다. 이 경우, 문자열이 배열 안의 값 중 하나로 시작하면 해당 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()`

`Str::chopEnd` 메서드는 문자열의 끝부분에 지정한 값이 있을 경우, 마지막에 한 번만 해당 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

두 번째 인자로 배열을 전달할 수도 있습니다. 이 경우, 문자열이 배열 안의 값 중 하나로 끝나면 해당 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
#### `Str::contains()`

`Str::contains` 메서드는 주어진 문자열에 지정한 값이 포함되어 있는지 여부를 확인합니다. 기본적으로 이 메서드는 대소문자를 구분합니다.

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

여러 값을 배열로 전달할 수도 있으며, 해당 배열 중 하나라도 포함되어 있다면 `true`를 반환합니다.

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 지정하면, 대소문자를 구분하지 않도록 설정할 수 있습니다.

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()`

`Str::containsAll` 메서드는 주어진 문자열에 배열에 담긴 모든 값이 모두 포함되어 있는지를 확인합니다.

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

`ignoreCase` 인수를 `true`로 지정하면, 대소문자를 구분하지 않습니다.

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()`

`Str::doesntContain` 메서드는 주어진 문자열에 해당 값이 포함되어 있지 않은지를 확인합니다. 기본적으로 이 메서드는 대소문자를 구분합니다.

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

여러 값을 배열로 전달할 수도 있으며, 주어진 값들 중 어느 것도 포함되어 있지 않으면 `true`를 반환합니다.

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 지정하면, 대소문자를 구분하지 않게 설정할 수 있습니다.

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
#### `Str::deduplicate()`

`Str::deduplicate` 메서드는 문자열에서 특정 문자가 연속해서 나타나는 경우 한 번만 남기고 중복된 부분을 모두 하나로 합쳐줍니다. 기본적으로 이 메서드는 공백(스페이스)을 중복 제거합니다.

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

두 번째 인자로 중복 제거를 원하는 문자를 지정할 수도 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-ends-with"></a>

#### `Str::endsWith()`

`Str::endsWith` 메서드는 주어진 문자열이 특정 값으로 끝나는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

또한 값의 배열을 전달하여, 해당 문자열이 배열 내의 값들 중 하나로 끝나는지 확인할 수도 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()`

`Str::excerpt` 메서드는 주어진 문자열 중에서 지정한 구문(phrase)를 처음으로 발견한 위치를 중심으로 발췌한 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` 옵션(기본값은 `100`)을 사용하면, 잘라낼 문자열의 양쪽에 표시할 문자 개수를 지정할 수 있습니다.

또한, `omission` 옵션으로 잘린 문자열 앞뒤에 어떤 문자열을 붙일 것인지 지정할 수도 있습니다.

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

`Str::finish` 메서드는 주어진 문자열이 특정 값으로 끝나지 않는 경우 해당 값을 한 번만 덧붙여 반환합니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-headline"></a>
#### `Str::headline()`

`Str::headline` 메서드는 대소문자, 하이픈, 밑줄 등으로 구분된 문자열을 띄어쓰기로 분리하고, 각 단어의 첫 글자를 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()`

`Str::inlineMarkdown` 메서드는 [CommonMark](https://commonmark.thephpleague.com/)를 사용해 GitHub 스타일의 마크다운을 인라인 HTML로 변환합니다. 단, `markdown` 메서드와 달리 생성된 HTML 전체를 블록 레벨 요소로 감싸지는 않습니다.

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

#### 마크다운 보안

기본적으로 마크다운은 원시 HTML을 지원하며, 이를 사용자 입력에 사용할 경우 교차 사이트 스크립팅(XSS) 취약점이 생길 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션을 사용하여 원시 HTML을 escape 처리하거나 제거할 수 있으며, `allow_unsafe_links` 옵션으로 안전하지 않은 링크 허용 여부를 지정할 수 있습니다. 만약 일부 원시 HTML을 허용하려면, 변환된 마크다운을 반드시 HTML Purifier를 통해 필터링해야 합니다.

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

`Str::is` 메서드는 주어진 문자열이 특정 패턴과 일치하는지 확인합니다. 이때 별표(`*`)를 와일드카드로 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

대소문자 구분을 비활성화하려면 `ignoreCase` 인수를 `true`로 지정하면 됩니다.

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()`

`Str::isAscii` 메서드는 해당 문자열이 7비트 ASCII로만 이루어져 있는지 판별합니다.

```php
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()`

`Str::isJson` 메서드는 해당 문자열이 유효한 JSON인지 판별합니다.

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

`Str::isUrl` 메서드는 해당 문자열이 유효한 URL인지 확인합니다.

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

`isUrl` 메서드는 다양한 프로토콜을 URL로 허용합니다. 하지만, 허용할 프로토콜 목록을 직접 지정하고 싶다면 배열로 전달할 수 있습니다.

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()`

`Str::isUlid` 메서드는 주어진 문자열이 유효한 ULID인지 판별합니다.

```php
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()`

`Str::isUuid` 메서드는 주어진 문자열이 유효한 UUID인지 판별합니다.

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

<a name="method-kebab-case"></a>
#### `Str::kebab()`

`Str::kebab` 메서드는 주어진 문자열을 `kebab-case` 형식으로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()`

`Str::lcfirst` 메서드는 전달된 문자열의 첫 문자를 소문자로 변환하여 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()`

`Str::length` 메서드는 주어진 문자열의 길이를 반환합니다.

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()`

`Str::limit` 메서드는 주어진 문자열을 지정한 길이만큼 잘라 반환합니다.

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

세 번째 인수로 잘린 문자열 끝에 덧붙일 문자를 지정할 수도 있습니다.

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

문자열을 자를 때 단어가 끊기지 않도록 하려면 `preserveWords` 인수를 사용할 수 있습니다. 이 인수가 `true`이면, 단어 경계에 맞춰 잘립니다.

```php
$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

// The quick...
```

<a name="method-str-lower"></a>
#### `Str::lower()`

`Str::lower` 메서드는 주어진 문자열을 모두 소문자로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
#### `Str::markdown()`

`Str::markdown` 메서드는 [CommonMark](https://commonmark.thephpleague.com/)를 사용해 GitHub 스타일의 마크다운을 HTML로 변환합니다.

```php
use Illuminate\Support\Str;

$html = Str::markdown('# Laravel');

// <h1>Laravel</h1>

$html = Str::markdown('# Taylor <b>Otwell</b>', [
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### 마크다운 보안

기본적으로 마크다운은 원시 HTML을 지원하며, 이를 사용자 입력에 사용할 경우 교차 사이트 스크립팅(XSS) 취약점이 발생할 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션을 사용해 원시 HTML을 escape 또는 제거할 수 있으며, `allow_unsafe_links` 옵션으로 안전하지 않은 링크의 허용 여부를 지정할 수 있습니다. 일부 원시 HTML만 허용해야 한다면, 변환된 마크다운을 반드시 HTML Purifier를 통과시켜야 합니다.

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

`Str::mask` 메서드는 문자열의 일부 구간을 지정한 문자로 마스킹합니다. 이메일, 전화번호 등과 같이 문자열의 특정 부분을 가릴 때 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

필요하다면 세 번째 인수에 음수를 지정하여, 문자열의 끝에서부터 기준으로 마스킹을 시작할 수도 있습니다.

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-match"></a>
#### `Str::match()`

`Str::match` 메서드는 주어진 정규표현식에 가장 먼저 일치하는 문자열 일부를 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::match('/bar/', 'foo bar');

// 'bar'

$result = Str::match('/foo (.*)/', 'foo bar');

// 'bar'
```

<a name="method-str-match-all"></a>
#### `Str::matchAll()`

`Str::matchAll` 메서드는 주어진 정규표현식에 일치하는 모든 부분 문자열을 컬렉션 형태로 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/bar/', 'bar foo bar');

// collect(['bar', 'bar'])
```

정규표현식 내에 그룹을 지정하면, 일치하는 각 그룹의 결과를 컬렉션으로 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

// collect(['un', 'ly']);
```

일치하는 결과가 없다면, 빈 컬렉션이 반환됩니다.

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()`

`Str::orderedUuid` 메서드는 "타임스탬프 우선" UUID를 생성합니다. 이 UUID는 인덱스가 걸린 데이터베이스 컬럼에 효율적으로 저장할 수 있습니다. 해당 메서드를 여러 번 호출하면, 이전에 생성한 UUID 이후 값이 정렬된 상태로 생성됩니다.

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()`

`Str::padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸는 역할을 하며, 문자열의 양쪽을 특정 문자로 채워 지정한 길이에 맞춥니다.

```php
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()`

`Str::padLeft` 메서드도 `str_pad`를 감싸는 형태로 동작하며, 문자열의 왼쪽을 특정 문자열로 지정한 길이만큼 채웁니다.

```php
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()`

`Str::padRight` 메서드는 문자열의 오른쪽을 특정 문자로 채워 지정한 길이에 맞춥니다.

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
#### `Str::password()`

`Str::password` 메서드는 원하는 길이의 안전하고 무작위인 비밀번호를 생성합니다. 비밀번호는 문자, 숫자, 기호, 공백 등이 조합되어 생성됩니다. 기본 비밀번호 길이는 32자입니다.

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
#### `Str::plural()`

`Str::plural` 메서드는 단수 단어를 복수형으로 변환합니다. 이 함수는 [라라벨의 복수화 도구가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

두 번째 인수로 정수를 전달하면, 해당 숫자에 맞는 단수 또는 복수형을 반환합니다.

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()`

`Str::pluralStudly` 메서드는 Studly Caps 형태의 단어도 복수형으로 변환합니다. 이 함수 역시 [라라벨의 복수화 도구가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

두 번째 인수로 정수를 넘기면, 전달된 숫자에 맞는 단수 또는 복수형을 반환합니다.

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>

#### `Str::position()`

`Str::position` 메서드는 주어진 문자열 안에서 특정 부분 문자열이 처음으로 등장하는 위치(인덱스)를 반환합니다. 만약 해당 부분 문자열이 존재하지 않는 경우에는 `false`를 반환합니다.

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
#### `Str::random()`

`Str::random` 메서드는 지정한 길이만큼의 랜덤 문자열을 생성합니다. 이 함수는 PHP의 `random_bytes` 함수를 사용합니다.

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

테스트를 진행할 때, `Str::random` 메서드가 반환하는 값을 임의로 지정("페이크")할 수 있습니다. 이를 위해 `createRandomStringsUsing` 메서드를 사용할 수 있습니다.

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

다시 원래처럼 랜덤 문자열이 반환되도록 하려면, `createRandomStringsNormally` 메서드를 호출하면 됩니다.

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
#### `Str::remove()`

`Str::remove` 메서드는 문자열에서 지정한 값 또는 값들의 배열을 제거합니다.

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

세 번째 인수로 `false`를 전달하면, 대소문자를 구분하지 않고 문자열을 제거할 수 있습니다.

<a name="method-str-repeat"></a>
#### `Str::repeat()`

`Str::repeat` 메서드는 지정한 문자열을 반복하여 이어붙입니다.

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()`

`Str::replace` 메서드는 문자열 내에서 지정한 값을 다른 문자열로 교체합니다.

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

`replace` 메서드는 `caseSensitive` 인수도 받을 수 있습니다. 기본적으로 `replace`는 대소문자를 구분하여 동작합니다.

```php
$replaced = Str::replace(
    'php',
    'Laravel',
    'PHP Framework for Web Artisans',
    caseSensitive: false
);

// Laravel Framework for Web Artisans
```

<a name="method-str-replace-array"></a>
#### `Str::replaceArray()`

`Str::replaceArray` 메서드는 문자열 내에서 지정한 값을 배열의 각 원소로 순서대로 교체합니다.

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()`

`Str::replaceFirst` 메서드는 문자열에서 지정한 값이 처음 등장하는 한 번만 다른 문자열로 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()`

`Str::replaceLast` 메서드는 문자열에서 지정한 값이 마지막으로 등장하는 부분만 다른 문자열로 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()`

`Str::replaceMatches` 메서드는 문자열에서 지정한 패턴(정규 표현식)에 일치하는 모든 부분을 주어진 교체 문자열로 대체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

또한 `replaceMatches` 메서드는 클로저(익명 함수)를 인수로 전달할 수 있으며, 패턴과 일치한 각 부분에 대해 해당 클로저가 호출되어 교체값을 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()`

`Str::replaceStart` 메서드는 주어진 값이 문자열의 시작 부분에 있을 경우, 이 부분만 지정한 값으로 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()`

`Str::replaceEnd` 메서드는 주어진 값이 문자열의 마지막에 있는 경우, 이 부분만 지정한 값으로 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

// Hello Laravel

$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-reverse"></a>
#### `Str::reverse()`

`Str::reverse` 메서드는 문자열을 뒤집어서 반환합니다.

```php
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
#### `Str::singular()`

`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. 이 함수는 [라라벨 복수화 도구가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()`

`Str::slug` 메서드는 주어진 문자열을 URL에 적합한 "슬러그(slug)" 형태로 변환합니다.

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()`

`Str::snake` 메서드는 주어진 문자열을 `snake_case` 형태로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()`

`Str::squish` 메서드는 문자열 내의 불필요한 모든 공백(단어 사이의 여분 공백까지 포함)을 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()`

`Str::start` 메서드는 문자열이 지정한 값으로 시작하지 않는 경우, 그 값을 앞에 추가합니다. 이미 값으로 시작하면 변경하지 않습니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()`

`Str::startsWith` 메서드는 주어진 문자열이 특정 값으로 시작하는지를 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

여러 값들 중 하나라도 해당 문자열로 시작하면 `true`를 반환합니다. 값들을 배열로 전달할 수 있습니다.

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()`

`Str::studly` 메서드는 주어진 문자열을 `StudlyCase` 형태로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()`

`Str::substr` 메서드는 시작 인덱스와 길이를 지정하여, 해당 부분 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()`

`Str::substrCount` 메서드는 주어진 문자열에서 특정 값이 등장하는 횟수를 반환합니다.

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()`

`Str::substrReplace` 메서드는 문자열의 일부 구간을 지정한 시작 위치부터 네 번째 인수로 지정한 글자 수만큼 대체합니다. 네 번째 인수에 `0`을 지정하면, 해당 위치에 문자열을 삽입하며 원래 문자열의 기존 문자는 삭제하지 않습니다.

```php
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()`

`Str::swap` 메서드는 PHP의 `strtr` 함수를 사용해 주어진 문자열 내에서 여러 값을 한 번에 교체합니다.

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

`Str::take` 메서드는 문자열의 맨 앞에서부터 지정한 개수만큼의 문자를 반환합니다.

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
#### `Str::title()`

`Str::title` 메서드는 주어진 문자열을 모든 단어의 첫 글자가 대문자인 `Title Case` 형태로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
#### `Str::toBase64()`

`Str::toBase64` 메서드는 주어진 문자열을 Base64 인코딩으로 변환합니다.

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
#### `Str::transliterate()`

`Str::transliterate` 메서드는 주어진 문자열을 가장 가까운 ASCII 문자로 변환하려고 시도합니다.

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
#### `Str::trim()`

`Str::trim` 메서드는 문자열의 앞뒤에 있는 공백(또는 기타 문자)을 제거합니다. PHP 내장 함수인 `trim`과는 달리, `Str::trim`은 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
#### `Str::ltrim()`

`Str::ltrim` 메서드는 문자열 앞부분의 공백(또는 기타 문자)을 제거합니다. 이 메서드는 PHP의 내장 `ltrim`과 달리, 유니코드 공백도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
#### `Str::rtrim()`

`Str::rtrim` 메서드는 문자열 끝부분의 공백(또는 기타 문자)을 제거합니다. 이 메서드는 PHP의 내장 `rtrim`과 달리, 유니코드 공백도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()`

`Str::ucfirst` 메서드는 문자열의 첫 글자만 대문자로 변환하여 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()`

`Str::ucsplit` 메서드는 대문자로 된 문자를 기준으로 문자열을 배열로 분리합니다.

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-upper"></a>
#### `Str::upper()`

`Str::upper` 메서드는 주어진 문자열을 모두 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()`

`Str::ulid` 메서드는 ULID라 불리는, 시간 순으로 정렬이 가능한 컴팩트한 고유 식별자를 생성합니다.

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

생성된 ULID가 언제 생성되었는지 알고 싶다면, 라라벨의 Carbon 통합에서 제공하는 `createFromId` 메서드를 사용해 `Illuminate\Support\Carbon` 날짜 인스턴스로 변환할 수 있습니다.

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

테스트 환경에서는 `Str::ulid` 메서드가 반환하는 값을 임의("페이크")로 지정할 수 있습니다. 이를 위해 `createUlidsUsing` 메서드를 사용합니다.

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

ULID 반환이 원래 방식대로 동작하도록 하려면, `createUlidsNormally` 메서드를 사용할 수 있습니다.

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
#### `Str::unwrap()`

`Str::unwrap` 메서드는 주어진 문자열의 시작과 끝에서 각각 지정한 문자열을 제거합니다.

```php
use Illuminate\Support\Str;

Str::unwrap('-Laravel-', '-');

// Laravel

Str::unwrap('{framework: "Laravel"}', '{', '}');

// framework: "Laravel"
```

<a name="method-str-uuid"></a>

#### `Str::uuid()`

`Str::uuid` 메서드는 UUID(버전 4)를 생성합니다.

```php
use Illuminate\Support\Str;

return (string) Str::uuid();
```

테스트를 진행할 때, `Str::uuid` 메서드가 반환하는 값을 임의로 지정해야 할 때가 있습니다. 이런 경우에는 `createUuidsUsing` 메서드를 사용할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

`uuid` 메서드가 다시 정상적으로 UUID를 생성하도록 하려면, `createUuidsNormally` 메서드를 호출하면 됩니다.

```php
Str::createUuidsNormally();
```

<a name="method-str-uuid7"></a>
#### `Str::uuid7()`

`Str::uuid7` 메서드는 UUID(버전 7)를 생성합니다.

```php
use Illuminate\Support\Str;

return (string) Str::uuid7();
```

정렬이 가능한 UUID를 생성하기 위해, 선택적으로 `DateTimeInterface`를 인자로 전달할 수 있습니다.

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()`

`Str::wordCount` 메서드는 문자열이 포함하고 있는 단어의 개수를 반환합니다.

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()`

`Str::wordWrap` 메서드는 지정한 글자 수를 기준으로 문자열을 줄바꿈 처리합니다.

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

`Str::words` 메서드는 문자열의 단어 개수를 제한합니다. 세 번째 인수로 다른 문자열을 지정하여, 자른 문자열 끝에 덧붙일 수 있습니다.

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
#### `Str::wrap()`

`Str::wrap` 메서드는 주어진 문자열을 원하는 문자열(또는 문자열 쌍)로 감쌉니다.

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
#### `str()`

`str` 함수는 전달된 문자열을 기반으로 새로운 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of` 메서드와 동일합니다.

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

만약 `str` 함수에 인자를 제공하지 않으면, `Illuminate\Support\Str`의 인스턴스를 반환합니다.

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()`

`trans` 함수는 제공된 번역 키를 사용해 [언어 파일](/docs/12.x/localization)에서 해당 번역을 반환합니다.

```php
echo trans('messages.welcome');
```

지정한 번역 키가 존재하지 않을 경우, `trans` 함수는 키 자체를 반환합니다. 위 예시에서 번역 키가 없으면 `trans` 함수는 `messages.welcome`을 반환합니다.

<a name="method-trans-choice"></a>
#### `trans_choice()`

`trans_choice` 함수는 주어진 번역 키와 수량에 따라 적절하게 굴절된 형태의 문자열을 반환합니다.

```php
echo trans_choice('messages.notifications', $unreadCount);
```

지정한 번역 키가 없으면, `trans_choice` 함수 역시 키 자체를 반환합니다. 위 예시에서 번역 키가 없으면 `messages.notifications`가 반환됩니다.

<a name="fluent-strings"></a>
## Fluent Strings

Fluent strings는 문자열 값을 더욱 유연하고 객체지향적으로 다룰 수 있게 하는 기능으로, 전통적인 문자열 조작 방식보다 더 읽기 쉽고 여러 문자열 작업을 체이닝하여 사용할 수 있습니다.

<a name="method-fluent-str-after"></a>
#### `after`

`after` 메서드는 문자열에서 지정한 값 이후의 내용을 반환합니다. 만약 문자열에 해당 값이 없다면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
#### `afterLast`

`afterLast` 메서드는 문자열에서 지정한 값이 마지막으로 등장한 이후의 모든 내용을 반환합니다. 해당 값이 없다면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-apa"></a>
#### `apa`

`apa` 메서드는 [APA 가이드라인](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 문자열을 타이틀 케이스로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->apa();

// A Nice Title Uses the Correct Case
```

<a name="method-fluent-str-append"></a>
#### `append`

`append` 메서드는 지정한 값을 문자열 끝에 추가합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
#### `ascii`

`ascii` 메서드는 가능한 한 문자열을 ASCII 값으로 변환(음역)합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
#### `basename`

`basename` 메서드는 문자열의 마지막(경로의 끝) 부분만을 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

필요하다면, 마지막 부분에서 특정 "확장자"를 제거하도록 지정할 수 있습니다.

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
#### `before`

`before` 메서드는 문자열에서 지정한 값 이전의 모든 내용을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
#### `beforeLast`

`beforeLast` 메서드는 문자열에서 지정한 값이 마지막으로 등장하기 전까지의 모든 내용을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
#### `between`

`between` 메서드는 두 값 사이에 있는 부분 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
#### `betweenFirst`

`betweenFirst` 메서드는 두 값 사이의 가장 짧은 부분 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
#### `camel`

`camel` 메서드는 주어진 문자열을 `camelCase`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// 'fooBar'
```

<a name="method-fluent-str-char-at"></a>
#### `charAt`

`charAt` 메서드는 지정한 인덱스에 있는 문자를 반환합니다. 만약 인덱스가 범위를 벗어나면 `false`를 반환합니다.

```php
use Illuminate\Support\Str;

$character = Str::of('This is my name.')->charAt(6);

// 's'
```

<a name="method-fluent-str-class-basename"></a>
#### `classBasename`

`classBasename` 메서드는 클래스 네임스페이스를 제거한 클래스명만 반환합니다.

```php
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// 'Baz'
```

<a name="method-fluent-str-chop-start"></a>
#### `chopStart`

`chopStart` 메서드는 주어진 값이 문자열의 시작에 있을 경우, 첫 번째 한 번만 해당 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopStart('https://');

// 'laravel.com'
```

배열을 넘겨줄 수도 있습니다. 만약 문자열이 배열 내 어떤 값으로 시작하면, 해당 값이 제거됩니다.

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopStart(['https://', 'http://']);

// 'laravel.com'
```

<a name="method-fluent-str-chop-end"></a>
#### `chopEnd`

`chopEnd` 메서드는 주어진 값이 문자열의 끝에 있을 경우, 마지막 한 번만 그 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::of('https://laravel.com')->chopEnd('.com');

// 'https://laravel'
```

배열을 넘겨줄 수도 있습니다. 문자열이 배열 내 어떤 값으로 끝나면, 그 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::of('http://laravel.com')->chopEnd(['.com', '.io']);

// 'http://laravel'
```

<a name="method-fluent-str-contains"></a>
#### `contains`

`contains` 메서드는 주어진 문자열에 특정 값이 포함되어 있는지 확인합니다. 기본적으로 대소문자를 구분합니다.

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

또한 배열을 전달하여, 해당 값들 중 하나라도 포함되어 있는지 검사할 수 있습니다.

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

`ignoreCase` 인자를 `true`로 설정하면 대소문자를 무시할 수 있습니다.

```php
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('MY', ignoreCase: true);

// true
```

<a name="method-fluent-str-contains-all"></a>
#### `containsAll`

`containsAll` 메서드는 주어진 배열의 모든 값이 문자열에 모두 포함되어 있는지 확인합니다.

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

`ignoreCase` 인자를 `true`로 설정하면 대소문자를 구분하지 않습니다.

```php
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-fluent-str-decrypt"></a>
#### `decrypt`

`decrypt` 메서드는 암호화된 문자열을 [복호화](/docs/12.x/encryption)합니다.

```php
use Illuminate\Support\Str;

$decrypted = $encrypted->decrypt();

// 'secret'
```

복호화의 반대 작업인 암호화가 필요하면 [encrypt](#method-fluent-str-encrypt) 메서드를 참고하세요.

<a name="method-fluent-str-deduplicate"></a>
#### `deduplicate`

`deduplicate` 메서드는 문자열 안에서 연속적으로 반복되는 문자를 한 번만 남기고 모두 대체합니다. 기본적으로 이 메서드는 중복된 공백을 하나로 줄여줍니다.

```php
use Illuminate\Support\Str;

$result = Str::of('The   Laravel   Framework')->deduplicate();

// The Laravel Framework
```

두 번째 인자로 다른 문자를 지정하면 해당 문자로 중복을 제거할 수 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::of('The---Laravel---Framework')->deduplicate('-');

// The-Laravel-Framework
```

<a name="method-fluent-str-dirname"></a>
#### `dirname`

`dirname` 메서드는 문자열의 상위 디렉터리 부분만 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

필요하다면, 상위 몇 단계까지 디렉터리를 제거할지 지정할 수도 있습니다.

```php
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-encrypt"></a>
#### `encrypt`

`encrypt` 메서드는 문자열을 [암호화](/docs/12.x/encryption)합니다.

```php
use Illuminate\Support\Str;

$encrypted = Str::of('secret')->encrypt();
```

암호화의 반대 작업은 [decrypt](#method-fluent-str-decrypt) 메서드를 참고하세요.

<a name="method-fluent-str-ends-with"></a>
#### `endsWith`

`endsWith` 메서드는 문자열이 주어진 값으로 끝나는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

또한 배열을 전달하여, 해당 값들 중 하나로 끝나는지 확인할 수도 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith(['name', 'foo']);

// true

$result = Str::of('This is my name')->endsWith(['this', 'foo']);

// false
```

<a name="method-fluent-str-exactly"></a>
#### `exactly`

`exactly` 메서드는 두 문자열이 정확하게 일치하는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-excerpt"></a>
#### `excerpt`

`excerpt` 메서드는 해당 문자열에서 지정한 구절이 최초로 등장하는 부분을 중심으로 발췌한 내용을 추출합니다.

```php
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` 옵션(기본값 100)은 잘라낸 문자열 양 쪽에 몇 글자를 포함시킬지 결정합니다.

또한 `omission` 옵션을 사용하여, 잘린 문자열 앞뒤에 붙는 문자열을 변경할 수 있습니다.

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

`explode` 메서드는 지정한 구분자로 문자열을 분리하여, 분리된 각 부분을 포함하는 컬렉션을 반환합니다.

```php
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
#### `finish`

`finish` 메서드는 문자열이 이미 해당 값으로 끝나지 않는 경우, 지정한 값을 한 번만 문자열 끝에 추가합니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-hash"></a>
#### `hash`

`hash` 메서드는 주어진 [알고리즘](https://www.php.net/manual/en/function.hash-algos.php)을 사용하여 문자열을 해싱합니다.

```php
use Illuminate\Support\Str;

$hashed = Str::of('secret')->hash(algorithm: 'sha256');

// '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'
```

<a name="method-fluent-str-headline"></a>
#### `headline`

`headline` 메서드는 대소문자, 하이픈, 언더스코어 등으로 구분된 문자열을 각 단어의 첫 글자가 대문자인, 공백으로 구분된 문자열로 변환합니다.

```php
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-inline-markdown"></a>
#### `inlineMarkdown`

`inlineMarkdown` 메서드는 GitHub 스타일의 마크다운을 [CommonMark](https://commonmark.thephpleague.com/)를 이용하여 인라인 HTML로 변환합니다. `markdown` 메서드와 달리, 전체 생성된 HTML을 블록 레벨 요소로 감싸지 않습니다.

```php
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

#### 마크다운 보안

기본적으로 마크다운은 Raw HTML을 지원하기 때문에, Raw 사용자 입력을 사용할 경우 XSS(교차 사이트 스크립팅) 취약점이 발생할 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션을 설정하여 Raw HTML을 이스케이프하거나 제거할 수 있고, `allow_unsafe_links` 옵션으로 안전하지 않은 링크 허용 여부를 지정할 수 있습니다. Raw HTML 일부만 허용하려면, 변환된 마크다운을 HTML Purifier에 통과시켜야 합니다.

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

`is` 메서드는 주어진 문자열이 지정한 패턴과 일치하는지를 판단합니다. 별표(*)를 와일드카드로 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

$matches = Str::of('foobar')->is('foo*');

// true

$matches = Str::of('foobar')->is('baz*');

// false
```

<a name="method-fluent-str-is-ascii"></a>
#### `isAscii`

`isAscii` 메서드는 주어진 문자열이 아스키(ASCII) 문자열인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('Taylor')->isAscii();

// true

$result = Str::of('ü')->isAscii();

// false
```

<a name="method-fluent-str-is-empty"></a>
#### `isEmpty`

`isEmpty` 메서드는 주어진 문자열이 비어있는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isEmpty();

// true

$result = Str::of('Laravel')->trim()->isEmpty();

// false
```

<a name="method-fluent-str-is-not-empty"></a>
#### `isNotEmpty`

`isNotEmpty` 메서드는 주어진 문자열이 비어있지 않은지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-json"></a>
#### `isJson`

`isJson` 메서드는 주어진 문자열이 올바른 JSON 형식인지 확인합니다.

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

`isUlid` 메서드는 주어진 문자열이 ULID인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-url"></a>
#### `isUrl`

`isUrl` 메서드는 주어진 문자열이 URL인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('http://example.com')->isUrl();

// true

$result = Str::of('Taylor')->isUrl();

// false
```

`isUrl` 메서드는 다양한 프로토콜을 유효한 것으로 간주합니다. 하지만, 특정 프로토콜만 유효하도록 지정할 수도 있습니다.

```php
$result = Str::of('http://example.com')->isUrl(['http', 'https']);
```

<a name="method-fluent-str-is-uuid"></a>
#### `isUuid`

`isUuid` 메서드는 주어진 문자열이 UUID인지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

<a name="method-fluent-str-kebab"></a>
#### `kebab`

`kebab` 메서드는 주어진 문자열을 `kebab-case`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
#### `lcfirst`

`lcfirst` 메서드는 주어진 문자열의 첫 글자를 소문자로 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```

<a name="method-fluent-str-length"></a>
#### `length`

`length` 메서드는 주어진 문자열의 길이를 반환합니다.

```php
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
#### `limit`

`limit` 메서드는 주어진 문자열을 지정한 길이로 자릅니다.

```php
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

잘린 문자열 끝에 붙일 문자열을 두 번째 인수로 전달할 수도 있습니다.

```php
$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

문자열을 자를 때 단어가 잘리지 않도록 하려면, `preserveWords` 인수를 사용할 수 있습니다. 이 인수를 `true`로 설정하면, 가까운 단어 경계로 잘립니다.

```php
$truncated = Str::of('The quick brown fox')->limit(12, preserveWords: true);

// The quick...
```

<a name="method-fluent-str-lower"></a>
#### `lower`

`lower` 메서드는 주어진 문자열을 소문자로 변환합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-markdown"></a>
#### `markdown`

`markdown` 메서드는 GitHub 스타일의 마크다운을 HTML로 변환합니다.

```php
use Illuminate\Support\Str;

$html = Str::of('# Laravel')->markdown();

// <h1>Laravel</h1>

$html = Str::of('# Taylor <b>Otwell</b>')->markdown([
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

#### 마크다운 보안

기본적으로 마크다운은 Raw HTML을 지원하기 때문에, Raw 사용자 입력을 사용할 경우 XSS(교차 사이트 스크립팅) 취약점이 발생할 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션을 설정하여 Raw HTML을 이스케이프하거나 제거할 수 있고, `allow_unsafe_links` 옵션으로 안전하지 않은 링크 허용 여부를 지정할 수 있습니다. Raw HTML 일부만 허용하려면, 변환된 마크다운을 HTML Purifier에 통과시켜야 합니다.

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

`mask` 메서드는 문자열의 일부 구간을 지정한 문자를 반복해서 가리고(masking) 보여줄 때 사용할 수 있습니다. 주로 이메일 주소나 전화번호 등 일부 구간을 숨길 때 유용합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

필요한 경우, 세 번째 또는 네 번째 인수에 음수를 지정하여 문자열 끝에서부터 거리를 기준으로 마스킹을 시작할 수도 있습니다.

```php
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
#### `match`

`match` 메서드는 주어진 정규 표현식에 일치하는 문자열의 부분을 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->match('/bar/');

// 'bar'

$result = Str::of('foo bar')->match('/foo (.*)/');

// 'bar'
```

<a name="method-fluent-str-match-all"></a>
#### `matchAll`

`matchAll` 메서드는 주어진 정규 표현식에 일치하는 모든 부분을 컬렉션으로 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

정규식에 그룹을 지정하면, 해당 그룹의 첫 번째 일치값들로 이루어진 컬렉션을 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

일치 결과가 하나도 없으면, 빈 컬렉션이 반환됩니다.

<a name="method-fluent-str-is-match"></a>
#### `isMatch`

`isMatch` 메서드는 문자열이 주어진 정규 표현식과 일치하면 `true`를 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('foo bar')->isMatch('/foo (.*)/');

// true

$result = Str::of('laravel')->isMatch('/foo (.*)/');

// false
```

<a name="method-fluent-str-new-line"></a>
#### `newLine`

`newLine` 메서드는 문자열 끝에 줄바꿈 문자를 추가합니다.

```php
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
#### `padBoth`

`padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸며, 문자열 양쪽을 지정한 문자열로 채워서 최종적으로 원하는 길이가 되도록 만듭니다.

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padBoth(10, '_');

// '__James___'

$padded = Str::of('James')->padBoth(10);

// '  James   '
```

<a name="method-fluent-str-padleft"></a>
#### `padLeft`

`padLeft` 메서드는 PHP의 `str_pad` 함수를 감싸며, 문자열 왼쪽을 지정한 문자열로 채우고 원하는 길이가 될 때까지 반복합니다.

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padLeft(10, '-=');

// '-=-=-James'

$padded = Str::of('James')->padLeft(10);

// '     James'
```

<a name="method-fluent-str-padright"></a>
#### `padRight`

`padRight` 메서드는 PHP의 `str_pad` 함수를 감싸며, 문자열 오른쪽을 지정한 문자열로 채우고 원하는 길이가 될 때까지 반복합니다.

```php
use Illuminate\Support\Str;

$padded = Str::of('James')->padRight(10, '-');

// 'James-----'

$padded = Str::of('James')->padRight(10);

// 'James     '
```

<a name="method-fluent-str-pipe"></a>
#### `pipe`

`pipe` 메서드를 사용하면, 현재 문자열 값을 지정한 callable에 전달하여 변환할 수 있습니다.

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

`plural` 메서드는 단수 형태의 문자열을 복수 형태로 변환합니다. 이 함수는 [라라벨 플루럴라이저가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

문자열의 복수 또는 단수 형태를 사용하고자 할 때, 두 번째 인수로 정수를 전달할 수 있습니다.

```php
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

<a name="method-fluent-str-position"></a>
#### `position`

`position` 메서드는 특정 부분 문자열이 처음 등장하는 위치를 반환합니다. 부분 문자열이 존재하지 않으면 `false`를 반환합니다.

```php
use Illuminate\Support\Str;

$position = Str::of('Hello, World!')->position('Hello');

// 0

$position = Str::of('Hello, World!')->position('W');

// 7
```

<a name="method-fluent-str-prepend"></a>

#### `prepend`

`prepend` 메서드는 전달된 값을 문자열 앞에 추가(prepend)합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
#### `remove`

`remove` 메서드는 전달된 값이나 값들의 배열을 문자열에서 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite');

// Arkansas is beautiful!
```

문자열을 제거할 때 대소문자를 구분하지 않으려면 두 번째 파라미터로 `false`를 전달할 수 있습니다.

<a name="method-fluent-str-repeat"></a>
#### `repeat`

`repeat` 메서드는 문자열을 지정한 횟수만큼 반복합니다.

```php
use Illuminate\Support\Str;

$repeated = Str::of('a')->repeat(5);

// aaaaa
```

<a name="method-fluent-str-replace"></a>
#### `replace`

`replace` 메서드는 문자열 내에서 지정한 값을 다른 값으로 교체(replace)합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

`replace` 메서드는 `caseSensitive` 인수도 받을 수 있습니다. 기본적으로 이 메서드는 대소문자를 구분합니다.

```php
$replaced = Str::of('macOS 13.x')->replace(
    'macOS', 'iOS', caseSensitive: false
);
```

<a name="method-fluent-str-replace-array"></a>
#### `replaceArray`

`replaceArray` 메서드는 문자열에서 지정한 값을 배열의 각 요소로 순차적으로 교체합니다.

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
#### `replaceFirst`

`replaceFirst` 메서드는 문자열 내에서 지정한 값이 처음 나타나는 부분만 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
#### `replaceLast`

`replaceLast` 메서드는 문자열 내에서 지정한 값이 마지막으로 나타나는 부분만 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
#### `replaceMatches`

`replaceMatches` 메서드는 지정된 패턴과 일치하는 문자열의 모든 부분을 주어진 문자열로 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

`replaceMatches` 메서드는 클로저(Closure)도 인수로 받을 수 있습니다. 이 경우 패턴과 일치하는 각각의 문자열에 대해 해당 클로저가 호출되며, 클로저에서 원하는 교체 로직을 구현해 반환할 수 있습니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-replace-start"></a>
#### `replaceStart`

`replaceStart` 메서드는 지정한 값이 문자열 맨 앞에 있을 때만 해당 부분을 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceStart('Hello', 'Laravel');

// Laravel World

$replaced = Str::of('Hello World')->replaceStart('World', 'Laravel');

// Hello World
```

<a name="method-fluent-str-replace-end"></a>
#### `replaceEnd`

`replaceEnd` 메서드는 지정한 값이 문자열 맨 끝에 있을 때만 해당 부분을 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::of('Hello World')->replaceEnd('World', 'Laravel');

// Hello Laravel

$replaced = Str::of('Hello World')->replaceEnd('Hello', 'Laravel');

// Hello World
```

<a name="method-fluent-str-scan"></a>
#### `scan`

`scan` 메서드는 [`sscanf` PHP 함수](https://www.php.net/manual/en/function.sscanf.php)가 지원하는 포맷에 따라 문자열을 컬렉션으로 변환합니다.

```php
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
#### `singular`

`singular` 메서드는 문자열을 단수형(singular)으로 변환합니다. 이 함수는 [라라벨의 복수화 도구가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$singular = Str::of('cars')->singular();

// car

$singular = Str::of('children')->singular();

// child
```

<a name="method-fluent-str-slug"></a>
#### `slug`

`slug` 메서드는 주어진 문자열로 URL에 적합한 "슬러그(slug)"를 생성합니다.

```php
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
#### `snake`

`snake` 메서드는 주어진 문자열을 `snake_case`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
#### `split`

`split` 메서드는 정규 표현식을 사용해 문자열을 여러 부분으로 나눠 컬렉션으로 반환합니다.

```php
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
#### `squish`

`squish` 메서드는 문자열 내의 불필요한 공백(단어 사이 포함)을 모두 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
#### `start`

`start` 메서드는 문자열이 해당 값으로 시작하지 않을 경우, 앞에 한 번만 해당 값을 추가합니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->start('/');

// /this/string

$adjusted = Str::of('/this/string')->start('/');

// /this/string
```

<a name="method-fluent-str-starts-with"></a>
#### `startsWith`

`startsWith` 메서드는 주어진 문자열이 해당 값으로 시작하는지 여부를 판별합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

<a name="method-fluent-str-strip-tags"></a>
#### `stripTags`

`stripTags` 메서드는 문자열 내의 모든 HTML 및 PHP 태그를 제거합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags();

// Taylor Otwell

$result = Str::of('<a href="https://laravel.com">Taylor <b>Otwell</b></a>')->stripTags('<b>');

// Taylor <b>Otwell</b>
```

<a name="method-fluent-str-studly"></a>
#### `studly`

`studly` 메서드는 주어진 문자열을 `StudlyCase`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
#### `substr`

`substr` 메서드는 지정한 시작 위치와 길이만큼 문자열의 일부만 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Laravel Framework')->substr(8);

// Framework

$string = Str::of('Laravel Framework')->substr(8, 5);

// Frame
```

<a name="method-fluent-str-substrreplace"></a>
#### `substrReplace`

`substrReplace` 메서드는 문자열의 일부 구간만 지정한 문자로 교체합니다. 두 번째 인자는 시작 위치, 세 번째 인자는 교체할 문자 길이입니다. 세 번째 인자에 `0`을 전달하면 기존 문자를 삭제하지 않고 해당 위치에 새 문자열을 추가만 합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-swap"></a>
#### `swap`

`swap` 메서드는 PHP의 `strtr` 함수를 사용해 여러 개의 값을 한 번에 교체합니다.

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

`take` 메서드는 문자열의 처음부터 지정한 개수만큼의 문자를 반환합니다.

```php
use Illuminate\Support\Str;

$taken = Str::of('Build something amazing!')->take(5);

// Build
```

<a name="method-fluent-str-tap"></a>
#### `tap`

`tap` 메서드는 문자열을 전달된 클로저에 넘겨주어 원하는 조작을 가능하게 해줍니다. 클로저 내에서 어떤 값을 반환하더라도, `tap` 메서드는 항상 원본 문자열을 반환합니다.

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

`test` 메서드는 문자열이 주어진 정규 표현식 패턴과 일치하는지 판별합니다.

```php
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
#### `title`

`title` 메서드는 주어진 문자열을 `Title Case`(각 단어의 첫 글자가 대문자인 형태)로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-to-base64"></a>
#### `toBase64`

`toBase64` 메서드는 주어진 문자열을 Base64 형태로 인코딩합니다.

```php
use Illuminate\Support\Str;

$base64 = Str::of('Laravel')->toBase64();

// TGFyYXZlbA==
```

<a name="method-fluent-str-to-html-string"></a>
#### `toHtmlString`

`toHtmlString` 메서드는 주어진 문자열을 `Illuminate\Support\HtmlString` 인스턴스로 변환합니다. 이 객체는 Blade 템플릿에서 렌더링될 때 이스케이프되지 않습니다.

```php
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-fluent-str-to-uri"></a>
#### `toUri`

`toUri` 메서드는 주어진 문자열을 [Illuminate\Support\Uri](/docs/12.x/helpers#uri) 인스턴스로 변환합니다.

```php
use Illuminate\Support\Str;

$uri = Str::of('https://example.com')->toUri();
```

<a name="method-fluent-str-transliterate"></a>
#### `transliterate`

`transliterate` 메서드는 주어진 문자열을 가장 근접한 ASCII 형태로 변환하려고 시도합니다.

```php
use Illuminate\Support\Str;

$email = Str::of('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ')->transliterate()

// 'test@laravel.com'
```

<a name="method-fluent-str-trim"></a>
#### `trim`

`trim` 메서드는 문자열 양쪽의 공백을 제거합니다. PHP의 기본 `trim` 함수와 달리, 라라벨의 `trim`은 유니코드 공백 문자까지 함께 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ltrim"></a>
#### `ltrim`

`ltrim` 메서드는 문자열의 왼쪽(앞쪽) 공백을 제거합니다. PHP의 기본 `ltrim` 함수와 달리, 라라벨의 `ltrim`은 유니코드 공백 문자까지 함께 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```

<a name="method-fluent-str-rtrim"></a>
#### `rtrim`

`rtrim` 메서드는 문자열의 오른쪽(뒷쪽) 공백을 제거합니다. PHP의 기본 `rtrim` 함수와 달리, 라라벨의 `rtrim`은 유니코드 공백 문자까지 함께 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
#### `ucfirst`

`ucfirst` 메서드는 주어진 문자열의 첫 글자를 대문자로 변환해 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
#### `ucsplit`

`ucsplit` 메서드는 대문자를 기준으로 문자열을 분할하여 컬렉션으로 반환합니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo', 'Bar'])
```

<a name="method-fluent-str-unwrap"></a>
#### `unwrap`

`unwrap` 메서드는 지정한 문자열을 기준으로 앞뒤에서 제거합니다.

```php
use Illuminate\Support\Str;

Str::of('-Laravel-')->unwrap('-');

// Laravel

Str::of('{framework: "Laravel"}')->unwrap('{', '}');

// framework: "Laravel"
```

<a name="method-fluent-str-upper"></a>
#### `upper`

`upper` 메서드는 주어진 문자열을 모두 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>

#### `when`

`when` 메서드는 주어진 조건이 `true`일 때, 전달된 클로저를 실행합니다. 이때 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('Taylor')
    ->when(true, function (Stringable $string) {
        return $string->append(' Otwell');
    });

// 'Taylor Otwell'
```

필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 조건 파라미터가 `false`로 평가될 때 실행됩니다.

<a name="method-fluent-str-when-contains"></a>
#### `whenContains`

`whenContains` 메서드는 문자열에 주어진 값이 포함되어 있을 때 전달된 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains('tony', function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 문자열에 주어진 값이 포함되어 있지 않을 때 실행됩니다.

배열 형태로 여러 값을 전달하면, 해당 문자열이 배열에 있는 값 중 하나라도 포함하고 있는지 판별할 수 있습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContains(['tony', 'hulk'], function (Stringable $string) {
        return $string->title();
    });

// Tony Stark
```

<a name="method-fluent-str-when-contains-all"></a>
#### `whenContainsAll`

`whenContainsAll` 메서드는 문자열이 주어진 모든 하위 문자열을 포함하고 있을 때, 전달된 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Str;
use Illuminate\Support\Stringable;

$string = Str::of('tony stark')
    ->whenContainsAll(['tony', 'stark'], function (Stringable $string) {
        return $string->title();
    });

// 'Tony Stark'
```

필요하다면, `when` 메서드의 세 번째 인자로 또 다른 클로저를 전달할 수 있습니다. 이 클로저는 조건 파라미터가 `false`로 평가될 때 실행됩니다.

<a name="method-fluent-str-when-empty"></a>
#### `whenEmpty`

`whenEmpty` 메서드는 문자열이 비어 있을 때, 전달한 클로저를 실행합니다. 클로저가 값을 반환하면 해당 값이 `whenEmpty` 메서드의 반환값이 됩니다. 클로저에서 값을 반환하지 않으면 플루언트 문자열 인스턴스를 반환합니다.

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

`whenNotEmpty` 메서드는 문자열이 비어 있지 않을 때, 전달한 클로저를 실행합니다. 클로저가 값을 반환하면 해당 값이 `whenNotEmpty` 메서드의 반환값이 되고, 그렇지 않으면 플루언트 문자열 인스턴스를 반환합니다.

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

`whenStartsWith` 메서드는 문자열이 지정한 하위 문자열로 시작하면, 전달된 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`whenEndsWith` 메서드는 문자열이 지정한 하위 문자열로 끝나면, 전달한 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`whenExactly` 메서드는 문자열이 지정한 문자열과 정확히 일치할 때, 전달된 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`whenNotExactly` 메서드는 문자열이 지정한 문자열과 정확히 일치하지 않을 때, 전달된 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`whenIs` 메서드는 문자열이 지정한 패턴과 일치할 때, 클로저를 실행합니다. 패턴에는 와일드카드(*)를 사용할 수 있습니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`whenIsAscii` 메서드는 문자열이 7비트 ASCII인지 확인하여, 맞으면 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`whenIsUlid` 메서드는 문자열이 유효한 ULID인지 확인하여, 맞으면 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function (Stringable $string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
#### `whenIsUuid`

`whenIsUuid` 메서드는 문자열이 유효한 UUID인지 확인하여, 맞으면 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`whenTest` 메서드는 문자열이 지정한 정규 표현식에 일치할 때, 전달된 클로저를 실행합니다. 클로저는 플루언트 문자열 인스턴스를 인자로 받습니다.

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

`wordCount` 메서드는 문자열이 포함하고 있는 단어의 개수를 반환합니다.

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
#### `words`

`words` 메서드는 문자열에 포함된 단어 수를 제한합니다. 필요하다면, 잘린 문자열 뒤에 추가로 붙일 문자열을 지정할 수 있습니다.

```php
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-fluent-str-wrap"></a>
#### `wrap`

`wrap` 메서드는 대상 문자열을 추가로 감싸는 문자열(또는 쌍의 문자열)로 감쌉니다.

```php
use Illuminate\Support\Str;

Str::of('Laravel')->wrap('"');

// "Laravel"

Str::is('is')->wrap(before: 'This ', after: ' Laravel!');

// This is Laravel!
```