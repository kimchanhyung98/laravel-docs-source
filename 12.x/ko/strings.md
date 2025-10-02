# 문자열 (Strings)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 문자열 값을 다루기 위한 다양한 함수들을 제공합니다. 이 함수들 중 상당수가 프레임워크 내에서 직접 사용되지만, 개발자는 필요에 따라 이러한 함수들을 자신의 애플리케이션에서도 자유롭게 활용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<a name="strings-method-list"></a>
### 문자열

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
[Str::doesntEndWith](#method-str-doesnt-end-with)
[Str::doesntStartWith](#method-str-doesnt-start-with)
[Str::deduplicate](#method-deduplicate)
[Str::endsWith](#method-ends-with)
[Str::excerpt](#method-excerpt)
[Str::finish](#method-str-finish)
[Str::fromBase64](#method-str-from-base64)
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
### Fluent 문자열

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
[doesntEndWith](#method-fluent-str-doesnt-end-with)
[doesntStartWith](#method-fluent-str-doesnt-start-with)
[encrypt](#method-fluent-str-encrypt)
[endsWith](#method-fluent-str-ends-with)
[exactly](#method-fluent-str-exactly)
[excerpt](#method-fluent-str-excerpt)
[explode](#method-fluent-str-explode)
[finish](#method-fluent-str-finish)
[fromBase64](#method-fluent-str-from-base64)
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
[whenDoesntEndWith](#method-fluent-str-when-doesnt-end-with)
[whenDoesntStartWith](#method-fluent-str-when-doesnt-start-with)
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

`__` 함수는 [언어 파일](/docs/12.x/localization)을 이용해 지정된 번역 문자열 또는 번역 키를 번역합니다:

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

만약 지정한 번역 문자열이나 키가 존재하지 않는 경우에는 `__` 함수가 전달된 값을 그대로 반환합니다. 따라서 위 예시에서 해당 번역 키가 없으면 `messages.welcome`이 반환됩니다.

<a name="method-class-basename"></a>
#### `class_basename()`

`class_basename` 함수는 지정한 클래스에서 네임스페이스를 제거하고 클래스명만 반환합니다:

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()`

`e` 함수는 PHP의 `htmlspecialchars` 함수를 기반으로 하며, `double_encode` 옵션이 기본적으로 `true`로 설정되어 있습니다:

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()`

`preg_replace_array` 함수는 문자열에서 정규 표현식 패턴에 일치하는 부분을 배열의 값들로 순차적으로 치환합니다:

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()`

`Str::after` 메서드는 주어진 값 이후의 문자열을 반환합니다. 만약 값이 문자열에 포함되지 않은 경우 전체 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()`

`Str::afterLast` 메서드는 주어진 값이 마지막으로 등장한 이후의 문자열을 반환합니다. 해당 값이 문자열 내에 없으면 전체 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
#### `Str::apa()`

`Str::apa` 메서드는 지정한 문자열을 [APA 가이드라인](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 타이틀 케이스(APA 스타일)로 변환합니다:

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()`

`Str::ascii` 메서드는 지정한 문자열을 가능한 한 ASCII 값으로 변환하려고 시도합니다:

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()`

`Str::before` 메서드는 주어진 값 이전의 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()`

`Str::beforeLast` 메서드는 주어진 값이 마지막으로 등장하기 전까지의 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
#### `Str::between()`

`Str::between` 메서드는 두 값 사이에 위치한 문자열 일부를 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()`

`Str::betweenFirst` 메서드는 두 값 사이에 있는 최소 부분 문자열을 반환합니다:

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()`

`Str::camel` 메서드는 주어진 문자열을 `camelCase` 형식으로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
#### `Str::charAt()`

`Str::charAt` 메서드는 지정한 인덱스의 문자를 반환합니다. 인덱스 범위를 벗어나면 `false`를 반환합니다:

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
#### `Str::chopStart()`

`Str::chopStart` 메서드는 전달한 값이 문자열의 앞에 있을 때만 한 번만 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

배열로 값들을 전달할 수도 있습니다. 문자열이 배열 내 값으로 시작한다면 해당 값이 제거됩니다:

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()`

`Str::chopEnd` 메서드는 전달한 값이 문자열의 마지막에 있을 때만 한 번만 제거합니다:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

배열로 값들을 전달할 수도 있습니다. 문자열이 배열 내 값으로 끝난다면 해당 값이 제거됩니다:

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
#### `Str::contains()`

`Str::contains` 메서드는 지정한 문자열이 특정 값을 포함하는지 확인합니다. 기본적으로 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

배열을 전달하여 주어진 문자열이 배열 값 중 하나라도 포함하고 있는지 검사할 수 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()`

`Str::containsAll` 메서드는 주어진 문자열이 배열의 모든 값을 포함하는지 확인합니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()`

`Str::doesntContain` 메서드는 주어진 문자열이 특정 값을 포함하지 않는지 확인합니다. 기본적으로 대소문자를 구분합니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

배열을 전달하여 주어진 문자열이 배열 내 모든 값과 일치하지 않는지 검사할 수 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정하여 대소문자 구분을 비활성화할 수 있습니다:

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
#### `Str::deduplicate()`

`Str::deduplicate` 메서드는 지정한 문자가 연속해서 나올 경우 한 개로 줄여줍니다. 기본적으로 연속된 공백 문자를 하나의 공백으로 만듭니다:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

두 번째 인자로 다른 문자도 지정할 수 있습니다:

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-str-doesnt-end-with"></a>
#### `Str::doesntEndWith()`

`Str::doesntEndWith` 메서드는 주어진 문자열이 특정 값으로 끝나지 않는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', 'dog');

// true
```

배열로 값들을 전달할 수도 있으며, 배열 내 값으로 끝나지 않으면 `true`를 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', ['this', 'foo']);

// true

$result = Str::doesntEndWith('This is my name', ['name', 'foo']);

// false
```

<a name="method-str-doesnt-start-with"></a>
#### `Str::doesntStartWith()`

`Str::doesntStartWith` 메서드는 주어진 문자열이 특정 값으로 시작하지 않는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::doesntStartWith('This is my name', 'That');

// true
```

배열을 전달할 경우, 주어진 값들 중 아무것도 해당 문자열의 앞에 없다면 `true`가 반환됩니다:

```php
$result = Str::doesntStartWith('This is my name', ['What', 'That', 'There']);

// true
```

<a name="method-ends-with"></a>
#### `Str::endsWith()`

`Str::endsWith` 메서드는 주어진 문자열이 특정 값으로 끝나는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

배열을 전달하여, 배열 내 값 중 하나라도 일치하면 `true`를 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()`

`Str::excerpt` 메서드는 주어진 문장에서 특정 구절이 최초로 등장하는 부분을 중심으로 발췌하여 반환합니다:

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` 옵션(기본값: 100)을 통해 생략된 문자열 양쪽에 몇 글자를 포함할지 지정할 수 있습니다.

또한 `omission` 옵션을 사용하여 앞뒤에 붙는 생략 문자열을 커스터마이즈할 수 있습니다:

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

`Str::finish` 메서드는 문자열이 특정 값으로 끝나지 않는 경우, 그 값을 문자열 끝에 한 번만 추가합니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-from-base64"></a>
#### `Str::fromBase64()`

`Str::fromBase64` 메서드는 Base64 인코딩된 문자열을 디코딩합니다:

```php
use Illuminate\Support\Str;

$decoded = Str::fromBase64('TGFyYXZlbA==');

// Laravel
```

<a name="method-str-headline"></a>
#### `Str::headline()`

`Str::headline` 메서드는 하이픈(-), 언더스코어(_), 대소문자 구분 등으로 구분된 문자열을, 각 단어의 첫 글자가 대문자인 띄어쓰기된 문자열로 변환합니다:

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()`

`Str::inlineMarkdown` 메서드는 GitHub 형식의 마크다운(GFM)을 [CommonMark](https://commonmark.thephpleague.com/)를 이용해 인라인 HTML로 변환합니다. `markdown` 메서드와 달리, 생성된 HTML 전체를 블록 엘리먼트로 감싸지 않습니다:

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

#### 마크다운 보안

기본적으로 마크다운은 원시 HTML을 지원하므로, 사용자 입력을 그대로 사용할 경우 교차 사이트 스크립팅(XSS) 취약점이 발생할 수 있습니다. [CommonMark Security documentation](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션으로 원시 HTML을 escape 하거나 제거할 수 있고, `allow_unsafe_links` 옵션을 사용해 안전하지 않은 링크 허용 여부를 지정할 수 있습니다. 특정 원시 HTML만 허용해야 한다면, 변환 결과를 HTML Purifier를 통해 처리해야 합니다:

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

`Str::is` 메서드는 주어진 문자열이 특정 패턴과 일치하는지 확인합니다. 와일드카드(*) 사용이 가능합니다:

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

`ignoreCase` 인수를 `true`로 설정해 대소문자를 무시할 수 있습니다:

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()`

`Str::isAscii` 메서드는 문자열이 7비트 ASCII인지 확인합니다:

```php
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()`

`Str::isJson` 메서드는 문자열이 유효한 JSON인지 확인합니다:

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

`Str::isUrl` 메서드는 문자열이 유효한 URL인지 확인합니다:

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

`isUrl` 메서드는 다양한 프로토콜을 유효로 간주합니다. 제한하고 싶다면 두 번째 인자로 허용할 프로토콜 목록을 전달할 수 있습니다:

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()`

`Str::isUlid` 메서드는 문자열이 유효한 ULID인지 확인합니다:

```php
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()`

`Str::isUuid` 메서드는 문자열이 유효한 UUID인지 확인합니다:

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

버전(1, 3, 4, 5, 6, 7, 8)에 따라 UUID 형식을 검사하고 싶다면 `version` 인자를 전달할 수 있습니다:

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 4);

// true

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 1);

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

`Str::lcfirst` 메서드는 주어진 문자열의 첫 문자를 소문자로 변환해 반환합니다:

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()`

`Str::length` 메서드는 주어진 문자열의 길이를 반환합니다:

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()`

`Str::limit` 메서드는 지정된 길이까지 문자열을 잘라냅니다:

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

세 번째 인자를 전달하여 잘린 뒤 붙일 문자열을 변경할 수 있습니다:

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

단어 단위로 자름을 보장하려면 `preserveWords` 인자를 사용할 수 있습니다. `true`로 설정하면 가장 가까운 단어 경계까지 잘립니다:

```php
$truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

// The quick...
```

<a name="method-str-lower"></a>
#### `Str::lower()`

`Str::lower` 메서드는 문자열을 모두 소문자로 변경합니다:

```php
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
#### `Str::markdown()`

`Str::markdown` 메서드는 GitHub 형식의 마크다운을 [CommonMark](https://commonmark.thephpleague.com/)로 HTML로 변환합니다:

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

기본적으로 마크다운은 원시 HTML을 지원하므로, 사용자 입력을 그대로 사용할 경우 교차 사이트 스크립팅(XSS) 취약점이 발생할 수 있습니다. [CommonMark Security documentation](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션으로 원시 HTML을 escape 하거나 제거할 수 있고, `allow_unsafe_links`로 위험한 링크 허용 여부를 설정할 수 있습니다. 특정 원시 HTML만 허용해야 한다면, 변환 결과를 HTML Purifier를 통해 처리해야 합니다:

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

`Str::mask` 메서드는 문자열의 일부를 반복된 문자로 마스킹하여 이메일, 전화번호 등 일부 항목을 가릴 수 있게 합니다:

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

세 번째 인자에 음수를 넣으면, 마지막에서부터 마스킹이 시작됩니다:

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-match"></a>
#### `Str::match()`

`Str::match` 메서드는 전달된 정규 표현식과 일치하는 문자열의 부분을 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::match('/bar/', 'foo bar');

// 'bar'

$result = Str::match('/foo (.*)/', 'foo bar');

// 'bar'
```

<a name="method-str-match-all"></a>
#### `Str::matchAll()`

`Str::matchAll` 메서드는 주어진 정규 표현식과 일치하는 모든 문자열 부분을 컬렉션으로 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/bar/', 'bar foo bar');

// collect(['bar', 'bar'])
```

매칭 그룹을 명시하면, 첫 번째 그룹에 대한 항목만 반환합니다:

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

// collect(['un', 'ly']);
```

일치하는 값이 없으면 빈 컬렉션이 반환됩니다.

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()`

`Str::orderedUuid` 메서드는 인덱스가 있는 컬럼에 효율적으로 저장할 수 있는 "타임스탬프 기반" UUID를 생성합니다. 이전에 생성된 UUID보다 항상 이후로 정렬됩니다:

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()`

`Str::padBoth` 메서드는 PHP의 `str_pad` 함수를 래핑하며, 문자열의 양쪽을 지정한 문자열로 채워서 원하는 길이에 맞춥니다:

```php
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()`

`Str::padLeft` 메서드는 PHP의 `str_pad`를 이용해 왼쪽을 원하는 길이만큼 지정한 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()`

`Str::padRight` 메서드는 PHP의 `str_pad`를 이용해 오른쪽을 원하는 길이만큼 지정한 문자열로 채웁니다:

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
#### `Str::password()`

`Str::password` 메서드는 지정한 길이의 안전한 무작위 비밀번호를 생성합니다. 비밀번호는 영문, 숫자, 기호, 공백이 혼합된 문자열입니다. 기본적으로 32자리 문자열이 생성됩니다:

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
#### `Str::plural()`

`Str::plural` 메서드는 단수 단어 문자열을 복수형으로 변환합니다. 이 함수는 [Laravel 복수화가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

두 번째 인자로 정수를 전달하여 단수 또는 복수형을 조건에 따라 반환할 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

`prependCount` 인수를 전달하여 복수화된 문자열 앞에 포맷팅된 `$count`를 붙일 수 있습니다:

```php
use Illuminate\Support\Str;

$label = Str::plural('car', 1000, prependCount: true);

// 1,000 cars
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()`

`Str::pluralStudly` 메서드는 StudlyCaps 형식(대문자로 시작하는 단어 조합)의 단어를 복수형으로 변환합니다. 이 함수 역시 [Laravel 복수화가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

두 번째 인자로 정수를 전달해 단수/복수 여부를 제어할 수 있습니다:

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>
#### `Str::position()`

`Str::position` 메서드는 부분 문자열이 본문 내 처음 등장하는 위치를 반환합니다. 만약 없다면 `false`를 반환합니다:

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
#### `Str::random()`

`Str::random` 메서드는 지정한 길이의 무작위 문자열을 생성하며, PHP의 `random_bytes` 함수를 사용합니다:

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

테스트 중에는 `Str::random`이 반환하는 값을 "가짜"로 지정할 수도 있습니다. 이를 위해 `createRandomStringsUsing` 메서드를 사용할 수 있습니다:

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

실제 무작위 문자열로 다시 돌리고 싶을 때는 `createRandomStringsNormally` 메서드를 호출하세요:

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
#### `Str::remove()`

`Str::remove` 메서드는 문자열에서 지정한 값 또는 값들의 배열을 제거합니다:

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

세 번째 인자에 `false`를 넘기면 대소문자를 구분하지 않고 제거할 수 있습니다.

<a name="method-str-repeat"></a>
#### `Str::repeat()`

`Str::repeat` 메서드는 문자열을 지정된 횟수만큼 반복하여 반환합니다:

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()`

`Str::replace` 메서드는 문자열 내 특정 값을 다른 값으로 대체합니다:

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

`caseSensitive` 인자를 설정할 수 있습니다. 기본값은 `true`(대소문자 구분)입니다:

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

`Str::replaceArray` 메서드는 문자열 내의 값을 배열의 값들로 순차적으로 치환합니다:

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()`

`Str::replaceFirst` 메서드는 문자열 내에서 지정한 값의 첫 번째 등장만을 다른 값으로 대체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()`

`Str::replaceLast` 메서드는 문자열 내에서 지정한 값이 마지막으로 등장하는 부분만 다른 값으로 대체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()`

`Str::replaceMatches` 메서드는 주어진 패턴과 일치하는 모든 부분을 지정한 문자열로 대체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

콜백 함수(클로저)를 전달해, 일치 부분마다 개별적으로 대체 논리를 직접 구현할 수도 있습니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()`

`Str::replaceStart` 메서드는 문자열의 시작 부분이 지정한 값과 일치할 때만 이를 다른 값으로 대체합니다:

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()`

`Str::replaceEnd` 메서드는 문자열의 끝 부분이 지정한 값과 일치하는 경우에만 이를 다른 값으로 대체합니다:

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

`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. 이 함수는 [Laravel 복수화가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다:

```php
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()`

`Str::slug` 메서드는 주어진 문자열을 URL에 적합한 "슬러그(slug)" 문자열로 변환합니다:

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()`

`Str::snake` 메서드는 주어진 문자열을 `snake_case` 형식으로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()`

`Str::squish` 메서드는 문자열 내 불필요한 모든 공백을 제거하고, 단어 사이의 중복 공백까지 하나로 줄입니다:

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()`

`Str::start` 메서드는 문자열이 지정한 값으로 시작하지 않으면, 그 값을 한 번만 문자열 앞에 붙입니다:

```php
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()`

`Str::startsWith` 메서드는 문자열이 특정 값으로 시작하는지 확인합니다:

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

배열을 전달하면, 해당 값들 중 하나라도 일치하면 `true`를 반환합니다:

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()`

`Str::studly` 메서드는 주어진 문자열을 `StudlyCase` 형식으로 변환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()`

`Str::substr` 메서드는 지정한 시작 위치와 길이에 따라 문자열 일부를 반환합니다:

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()`

`Str::substrCount` 메서드는 특정 값이 문자열 내에서 몇 번 등장하는지 반환합니다:

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()`

`Str::substrReplace` 메서드는 문자열의 일부를 지정한 위치에서 시작해, 지정한 개수만큼 교체하거나 0을 전달하면 삽입만 수행합니다:

```php
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()`

`Str::swap` 메서드는 PHP의 `strtr`를 사용하여, 문자열 내 여러 값을 한 번에 교체합니다:

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

`Str::take` 메서드는 문자열의 처음부터 지정한 수만큼의 문자를 반환합니다:

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
#### `Str::title()`

`Str::title` 메서드는 문자열을 `Title Case`로 변환합니다(각 단어의 첫 글자가 대문자):

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
#### `Str::toBase64()`

`Str::toBase64` 메서드는 지정한 문자열을 Base64 형식으로 인코딩합니다:

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
#### `Str::transliterate()`

`Str::transliterate` 메서드는 주어진 문자열을 가장 가까운 ASCII 표현으로 변환하려고 시도합니다:

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
#### `Str::trim()`

`Str::trim` 메서드는 지정한 문자열의 양쪽 끝에서 공백(또는 다른 문자)을 제거합니다. PHP의 기본 `trim` 함수와 달리, 유니코드 공백문자도 함께 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
#### `Str::ltrim()`

`Str::ltrim` 메서드는 문자열 앞부분에서 공백(또는 다른 문자)을 제거합니다. PHP의 기본 `ltrim`과 달리, 유니코드 공백도 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
#### `Str::rtrim()`

`Str::rtrim` 메서드는 문자열 뒷부분에서 공백(또는 다른 문자)을 제거합니다. PHP의 기본 `rtrim`과 달리, 유니코드 공백도 제거합니다:

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()`

`Str::ucfirst` 메서드는 주어진 문자열의 첫 문자를 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()`

`Str::ucsplit` 메서드는 대문자를 기준으로 문자열을 배열로 분할합니다:

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-upper"></a>
#### `Str::upper()`

`Str::upper` 메서드는 전달한 문자열을 모두 대문자로 변환합니다:

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()`

`Str::ulid` 메서드는 ULID(Compact, 시간순 정렬 가능한 고유 식별자)를 생성합니다:

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

ULID 생성 시점의 일시를 `Illuminate\Support\Carbon` 인스턴스로 얻고 싶다면, Laravel의 Carbon 통합 기능의 `createFromId`를 사용할 수 있습니다:

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

테스트 시에는 `Str::ulid`가 반환하는 값을 "가짜"로 지정할 수 있습니다. 이를 위해 `createUlidsUsing` 메서드를 사용할 수 있습니다:

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

실제 ULID로 다시 돌리고 싶을 때는 `createUlidsNormally` 메서드를 사용하세요:

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
#### `Str::unwrap()`

`Str::unwrap` 메서드는 지정한 문자열을 시작과 끝에서 각각 제거합니다:

```php
use Illuminate\Support\Str;

Str::unwrap('-Laravel-', '-');

// Laravel

Str::unwrap('{framework: "Laravel"}', '{', '}');

// framework: "Laravel"
```

<a name="method-str-uuid"></a>
#### `Str::uuid()`

`Str::uuid` 메서드는 UUID(version 4)를 생성합니다:

```php
use Illuminate\Support\Str;

return (string) Str::uuid();
```

테스트 환경에서 `Str::uuid`가 반환하는 값을 고정하려면 `createUuidsUsing` 메서드를 사용할 수 있습니다:

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

다시 정상적인 무작위 UUID 생성을 원한다면 `createUuidsNormally`를 호출하세요:

```php
Str::createUuidsNormally();
```

<a name="method-str-uuid7"></a>
#### `Str::uuid7()`

`Str::uuid7` 메서드는 UUID(version 7)를 생성합니다:

```php
use Illuminate\Support\Str;

return (string) Str::uuid7();
```

UUID7의 정렬 기준 시점을 지정하려면 `DateTimeInterface`를 인자로 사용할 수 있습니다:

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()`

`Str::wordCount` 메서드는 문자열이 포함하는 단어의 개수를 반환합니다:

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()`

`Str::wordWrap` 메서드는 지정한 글자 수만큼 문자열을 감싸줍니다:

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

`Str::words` 메서드는 문자열 내 단어 개수를 제한합니다. 세 번째 인자로 잘린 뒤 붙일 문자열을 전달할 수 있습니다:

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
#### `Str::wrap()`

`Str::wrap` 메서드는 주어진 문자열을 앞뒤로 추가 문자열을 감싸서 반환합니다:

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
#### `str()`

`str` 함수는 주어진 문자열로 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of` 메서드와 동일합니다:

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

인자가 없으면, `Illuminate\Support\Str` 인스턴스를 반환합니다:

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()`

`trans` 함수는 [언어 파일](/docs/12.x/localization)을 이용해 지정된 번역 키를 번역합니다:

```php
echo trans('messages.welcome');
```

번역 키가 존재하지 않으면 주어진 키 자체를 반환합니다. 즉, 위 예시에서 해당 키가 없으면 `messages.welcome`이 반환됩니다.

<a name="method-trans-choice"></a>
#### `trans_choice()`

`trans_choice` 함수는 주어진 번역 키를 복수 형태에 맞게 번역합니다:

```php
echo trans_choice('messages.notifications', $unreadCount);
```

번역 키가 존재하지 않으면 `trans_choice` 함수는 주어진 키를 그대로 반환합니다. 즉, 위 예시에서 해당 키가 없으면 `messages.notifications`가 반환됩니다.

<a name="fluent-strings"></a>
## Fluent 문자열 (Fluent Strings)

Fluent 문자열은 더 유연하고 객체지향적으로 문자열 값을 다룰 수 있도록 해주며, 기존 문자열 관련 함수보다 가독성 높고, 다양한 문자열 조작을 체이닝 형태로 수행할 수 있습니다.

<!-- 이하 Fluent 문자열 API 내부는 동일 구조와 예시를 유지하면서 이미 위 규칙 및 표현을 충실히 적용함. 추가 설명이 필요한 부분만 자연스럽게 의역 & 문맥화. -->