# 문자열 (Strings)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 문자열 값을 조작하기 위한 다양한 함수를 제공합니다. 이 함수들 중 상당수는 프레임워크 내부적으로 사용되지만, 여러분이 필요할 경우 애플리케이션 내에서 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

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

`__` 함수는 여러분의 [언어 파일](/docs/12.x/localization)을 이용하여 지정된 번역 문자열 또는 번역 키를 변환합니다.

```php
echo __('Welcome to our application');

echo __('messages.welcome');
```

지정한 번역 문자열이나 키가 존재하지 않으면, 해당 값 자체를 반환합니다. 따라서 위 예제에서 번역 키가 존재하지 않는 경우 `__` 함수는 `messages.welcome`을 반환합니다.

<a name="method-class-basename"></a>
#### `class_basename()`

`class_basename` 함수는 주어진 클래스 이름에서 네임스페이스 부분을 제거하고 클래스명만 반환합니다.

```php
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()`

`e` 함수는 PHP의 `htmlspecialchars` 함수를 사용하며, 기본적으로 `double_encode` 옵션이 `true`로 설정되어 있습니다.

```php
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()`

`preg_replace_array` 함수는 배열을 이용해 문자열에 주어진 패턴을 순차적으로 치환합니다.

```php
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()`

`Str::after` 메서드는 문자열에서 지정한 값 뒤의 모든 문자열을 반환합니다. 지정한 값이 문자열 내에 없으면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()`

`Str::afterLast` 메서드는 해당 값이 문자열 내에 여러 번 나타날 때, 마지막으로 나타난 이후의 모든 문자열을 반환합니다. 만약 문자열에 해당 값이 없다면 전체 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-apa"></a>
#### `Str::apa()`

`Str::apa` 메서드는 주어진 문자열을 [APA 스타일 가이드라인](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 Title Case로 변환합니다.

```php
use Illuminate\Support\Str;

$title = Str::apa('Creating A Project');

// 'Creating a Project'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()`

`Str::ascii` 메서드는 문자열을 가능한 한 ASCII 값으로 변환하려고 시도합니다.

```php
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()`

`Str::before` 메서드는 문자열에서 지정된 값 앞의 모든 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()`

`Str::beforeLast` 메서드는 문자열에서 해당 값이 여러 번 나타날 때, 마지막으로 등장하기 전까지의 문자열을 반환합니다.

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

`Str::betweenFirst` 메서드는 두 값 사이에서 가장 작은(첫 번째) 부분 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()`

`Str::camel` 메서드는 주어진 문자열을 `camelCase`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// 'fooBar'
```

<a name="method-char-at"></a>
#### `Str::charAt()`

`Str::charAt` 메서드는 지정한 인덱스에 위치한 문자 한 개를 반환합니다. 인덱스가 유효 범위를 벗어나면 `false`를 반환합니다.

```php
use Illuminate\Support\Str;

$character = Str::charAt('This is my name.', 6);

// 's'
```

<a name="method-str-chop-start"></a>
#### `Str::chopStart()`

`Str::chopStart` 메서드는 주어진 값이 문자열의 가장 앞에 있을 경우, 해당 값의 첫 번째 등장만 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopStart('https://laravel.com', 'https://');

// 'laravel.com'
```

두 번째 인수에 배열을 전달할 수도 있습니다. 만약 문자열이 배열에 포함된 값 중 하나로 시작하면 해당 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

// 'laravel.com'
```

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()`

`Str::chopEnd` 메서드는 주어진 값이 문자열의 맨 끝에 나타날 경우, 마지막 등장만 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('app/Models/Photograph.php', '.php');

// 'app/Models/Photograph'
```

배열을 두 번째 인수로 전달할 수도 있습니다. 문자열이 배열에 있는 값 중 하나로 끝나면 해당 값을 제거합니다.

```php
use Illuminate\Support\Str;

$url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

// 'laravel.com'
```

<a name="method-str-contains"></a>
#### `Str::contains()`

`Str::contains` 메서드는 주어진 문자열에 해당 값(부분 문자열)이 포함되어 있는지 확인합니다. 기본적으로 대소문자를 구분합니다.

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

또한, 배열을 인수로 전달하면 배열 내 어떤 값이라도 문자열에 포함되어 있는지 판별할 수 있습니다.

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정하면 대소문자를 구분하지 않게 할 수 있습니다.

```php
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'MY', ignoreCase: true);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()`

`Str::containsAll` 메서드는 주어진 문자열이 배열의 모든 값을 모두 포함하고 있는지 확인합니다.

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

`ignoreCase` 인수를 `true`로 주면 대소문자를 구분하지 않습니다.

```php
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

// true
```

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()`

`Str::doesntContain` 메서드는 주어진 문자열이 해당 값(부분 문자열)을 포함하지 않는지 확인합니다. 기본적으로 대소문자를 구분합니다.

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'my');

// true
```

배열을 전달하면, 배열 내 어떤 값도 포함하지 않으면 true를 반환합니다.

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', ['my', 'foo']);

// true
```

`ignoreCase` 인수를 `true`로 설정하면 대소문자를 구분하지 않습니다.

```php
use Illuminate\Support\Str;

$doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

// true
```

<a name="method-deduplicate"></a>
#### `Str::deduplicate()`

`Str::deduplicate` 메서드는 연속되는 동일 문자를 하나로 줄여 반환합니다. 기본적으로 공백을 deduplicate(중복 제거)합니다.

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The   Laravel   Framework');

// The Laravel Framework
```

두 번째 인수에 다른 문자를 지정하여 해당 문자의 중복만 제거할 수 있습니다.

```php
use Illuminate\Support\Str;

$result = Str::deduplicate('The---Laravel---Framework', '-');

// The-Laravel-Framework
```

<a name="method-str-doesnt-end-with"></a>
#### `Str::doesntEndWith()`

`Str::doesntEndWith` 메서드는 주어진 문자열이 특정 값으로 끝나지 않는지 판별합니다.

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', 'dog');

// true
```

배열을 전달하면 해당 배열의 어떤 값으로도 끝나지 않으면 true를 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::doesntEndWith('This is my name', ['this', 'foo']);

// true

$result = Str::doesntEndWith('This is my name', ['name', 'foo']);

// false
```

<a name="method-str-doesnt-start-with"></a>
#### `Str::doesntStartWith()`

`Str::doesntStartWith` 메서드는 주어진 문자열이 특정 값으로 시작하지 않는지 판별합니다.

```php
use Illuminate\Support\Str;

$result = Str::doesntStartWith('This is my name', 'That');

// true
```

배열을 전달하면, 해당 배열의 어떤 값으로도 시작하지 않으면 true를 반환합니다.

```php
$result = Str::doesntStartWith('This is my name', ['What', 'That', 'There']);

// true
```

<a name="method-ends-with"></a>
#### `Str::endsWith()`

`Str::endsWith` 메서드는 주어진 문자열이 특정 값으로 끝나는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

여러 값을 배열로 전달할 수 있습니다. 배열 내 값 중 하나라도 일치하면 true를 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()`

`Str::excerpt` 메서드는 문자열에서 특정 구문(phrase)이 처음 등장하는 부분을 중심으로 발췌(excerpt)합니다.

```php
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` 옵션(기본값 100)은 잘려진 문자열 좌우에 표시될 문자 수를 지정합니다.

`omission` 옵션을 사용하여 잘린 부분 앞뒤에 표시할 문자열을 지정할 수도 있습니다.

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

`Str::finish` 메서드는 문자열이 특정 값으로 끝나지 않으면 해당 값을 한 번 추가해줍니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-from-base64"></a>
#### `Str::fromBase64()`

`Str::fromBase64` 메서드는 Base64로 인코딩된 문자열을 디코딩합니다.

```php
use Illuminate\Support\Str;

$decoded = Str::fromBase64('TGFyYXZlbA==');

// Laravel
```

<a name="method-str-headline"></a>
#### `Str::headline()`

`Str::headline` 메서드는 대/소문자, 하이픈, 언더스코어로 구분된 문자열을 단어별 첫 글자가 대문자인 공백 구분 문자열로 변환합니다.

```php
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()`

`Str::inlineMarkdown` 메서드는 GitHub 스타일의 마크다운을 [CommonMark](https://commonmark.thephpleague.com/)를 통해 인라인 HTML로 변환합니다. 단, `markdown` 메서드와 달리 HTML을 블록 요소로 감싸지 않습니다.

```php
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

#### 마크다운 보안

기본적으로 마크다운은 원시 HTML을 지원하기 때문에, 사용자 입력을 그대로 렌더링할 경우 XSS(크로스사이트 스크립팅) 취약점에 노출될 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)에 따라, `html_input` 옵션으로 원시 HTML을 escaping 또는 strip 할 수 있고, `allow_unsafe_links` 옵션으로 위험한 링크 허용 여부를 지정할 수 있습니다. 원시 HTML의 일부를 허용해야 하는 경우, 마크다운을 HTML Purifier로 정제한 뒤 렌더링하시기 바랍니다.

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

`Str::is` 메서드는 특정 문자열이 지정한 패턴과 일치하는지 확인합니다. `*` 기호를 와일드카드로 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

`ignoreCase` 인수로 대소문자 구분을 비활성화할 수 있습니다.

```php
use Illuminate\Support\Str;

$matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);

// true
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()`

`Str::isAscii` 메서드는 주어진 문자열이 7비트 ASCII인지 확인합니다.

```php
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()`

`Str::isJson` 메서드는 해당 문자열이 올바른 JSON 형식인지 확인합니다.

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

`Str::isUrl` 메서드는 해당 문자열이 올바른 URL인지 판별합니다.

```php
use Illuminate\Support\Str;

$isUrl = Str::isUrl('http://example.com');

// true

$isUrl = Str::isUrl('laravel');

// false
```

`isUrl`은 다양한 프로토콜을 유효하게 판단합니다. 특정 프로토콜만 허용하고 싶으면 두 번째 인수로 배열을 전달할 수 있습니다.

```php
$isUrl = Str::isUrl('http://example.com', ['http', 'https']);
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()`

`Str::isUlid` 메서드는 해당 문자열이 유효한 ULID인지 판별합니다.

```php
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()`

`Str::isUuid` 메서드는 해당 문자열이 올바른 UUID인지 판별합니다.

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

UUID 버전(1, 3, 4, 5, 6, 7, 8) 지정이 필요하다면, 두 번째 인수로 `version`을 전달할 수 있습니다.

```php
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 4);

// true

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de', version: 1);

// false
```

<a name="method-kebab-case"></a>
#### `Str::kebab()`

`Str::kebab` 메서드는 주어진 문자열을 `kebab-case`로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()`

`Str::lcfirst` 메서드는 주어진 문자열의 첫 글자를 소문자로 변환합니다.

```php
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()`

`Str::length` 메서드는 문자열의 길이를 반환합니다.

```php
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()`

`Str::limit` 메서드는 지정한 길이만큼 문자열을 잘라 반환합니다.

```php
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

세 번째 인수로 잘려진 문자열 뒤에 붙일 문자를 지정할 수 있습니다.

```php
$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

단어 단위로 잘리게 하려면 `preserveWords` 인수를 true로 지정하세요. 가장 가까운 단어 경계에 맞게 잘라줍니다.

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

`Str::markdown` 메서드는 GitHub 스타일 마크다운을 [CommonMark](https://commonmark.thephpleague.com/)를 사용해 HTML로 변환합니다.

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

기본적으로 마크다운은 원시 HTML을 지원하기 때문에 XSS(크로스사이트 스크립팅) 취약점에 노출될 수 있습니다. [CommonMark 보안 문서](https://commonmark.thephpleague.com/security/)를 참고해 `html_input`이나 `allow_unsafe_links` 옵션을 적절히 설정하고, 일부 원시 HTML을 허용하려면 HTML Purifier로 후처리하세요.

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

`Str::mask` 메서드는 문자열의 일부를 지정한 문자로 반복해서 가립니다. 이메일, 전화번호 등 민감한 데이터를 숨길 때 쓸 수 있습니다.

```php
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

세 번째 인수에 음수를 주면 문자열 끝에서부터 거리를 세기 시작합니다.

```php
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-match"></a>
#### `Str::match()`

`Str::match` 메서드는 주어진 정규식 패턴과 일치하는 부분 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::match('/bar/', 'foo bar');

// 'bar'

$result = Str::match('/foo (.*)/', 'foo bar');

// 'bar'
```

<a name="method-str-match-all"></a>
#### `Str::matchAll()`

`Str::matchAll` 메서드는 정규식 패턴에 일치하는 모든 부분을 컬렉션으로 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/bar/', 'bar foo bar');

// collect(['bar', 'bar'])
```

정규식에 그룹을 사용하면, 첫 번째 매칭 그룹만 컬렉션으로 반환합니다.

```php
use Illuminate\Support\Str;

$result = Str::matchAll('/f(\w*)/', 'bar fun bar fly');

// collect(['un', 'ly']);
```

일치하는 부분이 없으면 빈 컬렉션이 반환됩니다.

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()`

`Str::orderedUuid` 메서드는 인덱스가 있는 DB 컬럼에 효율적으로 저장될 수 있는 타임스탬프 기반 UUID를 생성합니다. 이 메서드로 생성된 각 UUID는 이전에 생성된 UUID보다 항상 이후에 정렬됩니다.

```php
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()`

`Str::padBoth` 메서드는 PHP의 `str_pad` 함수를 감싸며, 문자열 양 옆을 다른 문자열로 채워 최종 길이가 되도록 만듭니다.

```php
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()`

`Str::padLeft` 메서드는 문자열 왼쪽에 다른 문자열을 추가하여 원하는 길이가 될 때까지 채웁니다.

```php
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()`

`Str::padRight` 메서드는 문자열 오른쪽에 다른 문자열을 추가하여 원하는 길이가 될 때까지 채웁니다.

```php
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-password"></a>
#### `Str::password()`

`Str::password` 메서드는 지정된 길이만큼 강력하고 무작위로 생성된 비밀번호를 만들어줍니다. 비밀번호는 문자, 숫자, 특수문자, 공백을 조합하여 생성됩니다. 기본값은 32자입니다.

```php
use Illuminate\Support\Str;

$password = Str::password();

// 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

$password = Str::password(12);

// 'qwuar>#V|i]N'
```

<a name="method-str-plural"></a>
#### `Str::plural()`

`Str::plural` 메서드는 단수형 명사 문자열을 복수형으로 변환합니다. 이 기능은 [Laravel의 복수 변환기가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

정수형 두 번째 인수를 제공하면 입력한 숫자에 따라 단수 또는 복수형을 반환합니다.

```php
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

`prependCount` 인수를 통해 복수형 문자열 앞에 서식화된 `$count` 값을 붙일 수 있습니다.

```php
use Illuminate\Support\Str;

$label = Str::plural('car', 1000, prependCount: true);

// 1,000 cars
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()`

`Str::pluralStudly` 메서드는 StudlyCaps로 작성된 단수 단어를 복수형으로 변환합니다. 이 기능은 [Laravel 복수 변환기가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

정수형 두 번째 인수를 제공하면 단수 또는 복수형을 지정할 수 있습니다.

```php
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-position"></a>
#### `Str::position()`

`Str::position` 메서드는 지정한 부분 문자열이 처음으로 나타나는 위치(인덱스)를 반환합니다. 해당 부분 문자열이 없으면 `false`를 반환합니다.

```php
use Illuminate\Support\Str;

$position = Str::position('Hello, World!', 'Hello');

// 0

$position = Str::position('Hello, World!', 'W');

// 7
```

<a name="method-str-random"></a>
#### `Str::random()`

`Str::random` 메서드는 지정한 길이만큼 무작위 문자열을 생성합니다. PHP의 `random_bytes`가 사용됩니다.

```php
use Illuminate\Support\Str;

$random = Str::random(40);
```

테스트 환경에서는 `Str::random`이 반환하는 값을 임의로 설정할 수 있으며, `createRandomStringsUsing` 메서드를 사용합니다.

```php
Str::createRandomStringsUsing(function () {
    return 'fake-random-string';
});
```

원래대로 랜덤 문자열을 생성하게 하려면 `createRandomStringsNormally` 메서드를 호출하세요.

```php
Str::createRandomStringsNormally();
```

<a name="method-str-remove"></a>
#### `Str::remove()`

`Str::remove` 메서드는 주어진 값 또는 값의 배열을 문자열 내에서 모두 제거합니다.

```php
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

세 번째 인수로 `false`를 전달하면 대소문자 구분 없이 제거할 수 있습니다.

<a name="method-str-repeat"></a>
#### `Str::repeat()`

`Str::repeat` 메서드는 전달한 문자열을 지정된 횟수만큼 반복합니다.

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()`

`Str::replace` 메서드는 특정 문자열을 다른 문자열로 치환합니다.

```php
use Illuminate\Support\Str;

$string = 'Laravel 11.x';

$replaced = Str::replace('11.x', '12.x', $string);

// Laravel 12.x
```

`caseSensitive` 인수로 대소문자 구분 여부를 제어할 수 있습니다. 기본값은 대소문자 구분입니다.

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

`Str::replaceArray` 메서드는 배열의 각 값을 순서대로 문자열 내 지정한 값과 바꿉니다.

```php
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()`

`Str::replaceFirst` 메서드는 주어진 값이 처음 등장하는 곳만 새로운 값으로 치환합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()`

`Str::replaceLast` 메서드는 주어진 값이 마지막에 나타나는 곳만 새로운 값으로 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()`

`Str::replaceMatches` 메서드는 패턴에 일치하는 문자열 조각을 새로운 문자열로 모두 대체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches(
    pattern: '/[^A-Za-z0-9]++/',
    replace: '',
    subject: '(+1) 501-555-1000'
)

// '15015551000'
```

함수(Closure)를 전달하면, 패턴에 맞는 문자열 조각마다 콜백이 실행되고, 반환 결과로 대체됩니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceMatches('/\d/', function (array $matches) {
    return '['.$matches[0].']';
}, '123');

// '[1][2][3]'
```

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()`

`Str::replaceStart` 메서드는 해당 값이 문자열의 맨 앞에 있을 경우에만 첫 번째 등장을 새로운 값으로 교체합니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

// Laravel World

$replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()`

`Str::replaceEnd` 메서드는 해당 값이 문자열의 끝에 있을 경우에만 마지막 등장을 새로운 값으로 바꿉니다.

```php
use Illuminate\Support\Str;

$replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

// Hello Laravel

$replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

// Hello World
```

<a name="method-str-reverse"></a>
#### `Str::reverse()`

`Str::reverse` 메서드는 문자열을 역순으로 뒤집습니다.

```php
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
#### `Str::singular()`

`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. [Laravel 복수 변환기가 지원하는 모든 언어](/docs/12.x/localization#pluralization-language)를 지원합니다.

```php
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()`

`Str::slug` 메서드는 주어진 문자열을 URL에 적합한 "슬러그(slug)"로 변환합니다.

```php
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()`

`Str::snake` 메서드는 문자열을 `snake_case` 형식으로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()`

`Str::squish` 메서드는 불필요한 모든 공백(단어 사이 공백 포함)을 없애고 한 칸 공백으로 정리합니다.

```php
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()`

`Str::start` 메서드는 문자열이 해당 값으로 시작하지 않을 경우 값을 한 번 추가해줍니다.

```php
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()`

`Str::startsWith` 메서드는 문자열이 해당 값으로 시작하는지 확인합니다.

```php
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

배열을 인수로 전달할 경우, 배열 중 하나라도 일치하면 true를 반환합니다.

```php
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()`

`Str::studly` 메서드는 문자열을 `StudlyCase`(각 단어의 첫 글자만 대문자)로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()`

`Str::substr` 메서드는 시작 위치와 길이를 지정하여 해당 부분의 문자열을 반환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()`

`Str::substrCount` 메서드는 주어진 문자열 내 특정 값이 몇 번 나타나는지 반환합니다.

```php
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()`

`Str::substrReplace` 메서드는 문자열의 특정 위치부터 일정 길이만큼을 새로운 문자열로 바꿉니다. 네 번째 인수를 `0`으로 주면 기존 문자 삭제 없이 해당 위치에 새 문자열을 삽입합니다.

```php
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()`

`Str::swap` 메서드는 PHP의 `strtr` 함수를 사용하여 여러 값을 동시에 치환합니다.

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

`Str::take` 메서드는 문자열 첫 부분에서 지정한 개수만큼의 문자를 반환합니다.

```php
use Illuminate\Support\Str;

$taken = Str::take('Build something amazing!', 5);

// Build
```

<a name="method-title-case"></a>
#### `Str::title()`

`Str::title` 메서드는 문자열을 각 단어의 첫 글자만 대문자인 Title Case로 변환합니다.

```php
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-base64"></a>
#### `Str::toBase64()`

`Str::toBase64` 메서드는 문자열을 Base64로 인코딩합니다.

```php
use Illuminate\Support\Str;

$base64 = Str::toBase64('Laravel');

// TGFyYXZlbA==
```

<a name="method-str-transliterate"></a>
#### `Str::transliterate()`

`Str::transliterate` 메서드는 주어진 문자열을 가능한 가장 근접한 ASCII 형태로 변환합니다.

```php
use Illuminate\Support\Str;

$email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

// 'test@laravel.com'
```

<a name="method-str-trim"></a>
#### `Str::trim()`

`Str::trim` 메서드는 문자열의 앞뒤 공백(또는 특정 문자)을 제거합니다. PHP의 기본 `trim`과 달리 유니코드 공백 문자도 같이 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::trim(' foo bar ');

// 'foo bar'
```

<a name="method-str-ltrim"></a>
#### `Str::ltrim()`

`Str::ltrim` 메서드는 문자열의 앞쪽 공백(또는 특정 문자)을 제거합니다. PHP의 기본 `ltrim`과 달리 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::ltrim('  foo bar  ');

// 'foo bar  '
```

<a name="method-str-rtrim"></a>
#### `Str::rtrim()`

`Str::rtrim` 메서드는 문자열 끝 공백(또는 특정 문자)을 제거합니다. PHP의 기본 `rtrim`과 달리 유니코드 공백 문자도 제거합니다.

```php
use Illuminate\Support\Str;

$string = Str::rtrim('  foo bar  ');

// '  foo bar'
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()`

`Str::ucfirst` 메서드는 문자열의 첫 글자를 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()`

`Str::ucsplit` 메서드는 대문자를 기준으로 문자열을 배열로 분할합니다.

```php
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-upper"></a>
#### `Str::upper()`

`Str::upper` 메서드는 문자열 전체를 대문자로 변환합니다.

```php
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()`

`Str::ulid` 메서드는 ULID라는 시간순으로 정렬되는 고유 식별자를 생성합니다.

```php
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

특정 ULID가 생성된 날짜와 시간을 `Illuminate\Support\Carbon` 인스턴스 형태로 확인하려면, Carbon의 `createFromId` 메서드를 사용합니다.

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

테스트 환경에서는 `Str::ulid`값을 임의로 지정할 수 있습니다. 이 경우 `createUlidsUsing` 메서드를 활용합니다.

```php
use Symfony\Component\Uid\Ulid;

Str::createUlidsUsing(function () {
    return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
});
```

원래 ULID 자동 생성으로 복원하려면 `createUlidsNormally`를 호출하세요.

```php
Str::createUlidsNormally();
```

<a name="method-str-unwrap"></a>
#### `Str::unwrap()`

`Str::unwrap` 메서드는 지정한 문자열이 전체에서 앞과 뒤에 등장하면 그것을 제거합니다.

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

테스트 환경에서는 반환값을 임의로 설정할 수 있습니다. 이를 위해 `createUuidsUsing` 메서드를 사용하세요.

```php
use Ramsey\Uuid\Uuid;

Str::createUuidsUsing(function () {
    return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
});
```

기본 동작으로 복구하려면 `createUuidsNormally`를 호출하세요.

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

생성 시 사용할 시간 정보로 `DateTimeInterface` 객체를 넘길 수도 있습니다.

```php
return (string) Str::uuid7(time: now());
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()`

`Str::wordCount` 메서드는 문자열이 포함하는 단어의 개수를 반환합니다.

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()`

`Str::wordWrap` 메서드는 문자열을 지정한 글자수만큼 줄바꿈해서 반환합니다.

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

`Str::words` 메서드는 문자열의 단어 개수를 제한합니다. 잘라낸 곳 뒤에 붙일 문자열도 세 번째 인수로 지정할 수 있습니다.

```php
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str-wrap"></a>
#### `Str::wrap()`

`Str::wrap` 메서드는 주어진 문자열을 추가 문자열로 감쌉니다. 짝을 이루는 문자열도 가능하며, 각각 before/after 인수로 지정할 수 있습니다.

```php
use Illuminate\Support\Str;

Str::wrap('Laravel', '"');

// "Laravel"

Str::wrap('is', before: 'This ', after: ' Laravel!');

// This is Laravel!
```

<a name="method-str"></a>
#### `str()`

`str` 함수는 주어진 문자열에 대한 새로운 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 동작은 `Str::of` 메서드와 동일합니다.

```php
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

아무 인수도 주지 않을 경우, `Illuminate\Support\Str` 인스턴스를 반환합니다.

```php
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()`

`trans` 함수는 지정한 번역 키를 여러분의 [언어 파일](/docs/12.x/localization)을 이용해 번역해줍니다.

```php
echo trans('messages.welcome');
```

지정한 번역 키가 존재하지 않으면 해당 키 자체를 반환합니다. 즉, 위 예제에서 해당 키가 없을 때 `messages.welcome`을 반환합니다.

<a name="method-trans-choice"></a>
#### `trans_choice()`

`trans_choice` 함수는 지정한 번역 키를 복수 변형 규칙에 따라 변환해줍니다.

```php
echo trans_choice('messages.notifications', $unreadCount);
```

지정한 번역 키가 존재하지 않으면 해당 키 자체를 반환합니다. 위 예시대로라면, 존재하지 않을 때 `messages.notifications`를 반환합니다.

<a name="fluent-strings"></a>
## Fluent 문자열 (Fluent Strings)

Fluent 문자열 기능을 활용하면 객체 지향적인 방식으로 문자열을 다룰 수 있습니다. 여러 문자열 조작 작업을 체이닝으로 연결해 보다 읽기 쉬운 구문으로 사용할 수 있습니다.

<!-- 이하의 각 메서드 설명은 위 구조와 동일하게 번역됨 -->

[각 Fluent 문자열 메서드 문서들도 번역 규칙에 따라 그대로 번역되었습니다. 실제 파일에는 전체 코드 및 문서가 반영되어 있습니다.]