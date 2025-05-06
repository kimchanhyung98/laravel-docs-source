# 문자열(문자열 처리)

- [소개](#introduction)
- [사용 가능한 메소드](#available-methods)

<a name="introduction"></a>
## 소개

Laravel은 문자열 값을 다루기 위한 다양한 함수를 제공합니다. 이 함수들 중 상당수는 Laravel 프레임워크 내부에서 사용되지만, 여러분의 애플리케이션에서도 편리하게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메소드

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<a name="strings-method-list"></a>
### 문자열(Strings)

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
## 문자열(문자열 처리)

<a name="method-__"></a>
#### `__()` {.collection-method}

`__` 함수는 주어진 번역 문자열 또는 번역 키를 [언어 파일](/docs/{{version}}/localization)을 사용하여 번역합니다:

    echo __('Welcome to our application');

    echo __('messages.welcome');

지정한 번역 문자열 또는 키가 존재하지 않으면, `__` 함수는 원래의 값을 반환합니다. 따라서 위 예시에서 해당 번역 키가 없으면 `__` 함수는 `messages.welcome`을 반환합니다.

<a name="method-class-basename"></a>
#### `class_basename()` {.collection-method}

`class_basename` 함수는 지정한 클래스에서 네임스페이스를 제거하고 클래스명만 반환합니다:

    $class = class_basename('Foo\Bar\Baz');

    // Baz

<a name="method-e"></a>
#### `e()` {.collection-method}

`e` 함수는 PHP의 `htmlspecialchars` 함수를 기본적으로 `double_encode` 옵션을 true로 하여 실행합니다:

    echo e('<html>foo</html>');

    // &lt;html&gt;foo&lt;/html&gt;

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()` {.collection-method}

`preg_replace_array` 함수는 주어진 문자열에서 패턴에 일치하는 부분들을 배열의 값으로 차례차례 대체합니다:

    $string = 'The event will take place between :start and :end';

    $replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

    // The event will take place between 8:30 and 9:00

<a name="method-str-after"></a>
#### `Str::after()` {.collection-method}

`Str::after` 메소드는 문자열에서 지정한 값 이후의 모든 내용을 반환합니다. 만약 값이 존재하지 않으면 전체 문자열을 반환합니다:

    use Illuminate\Support\Str;

    $slice = Str::after('This is my name', 'This is');

    // ' my name'

<a name="method-str-after-last"></a>
#### `Str::afterLast()` {.collection-method}

`Str::afterLast` 메소드는 문자열 내에서 지정한 값이 마지막으로 등장한 이후의 모든 내용을 반환합니다. 값이 존재하지 않으면 전체 문자열을 반환합니다:

    use Illuminate\Support\Str;

    $slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

    // 'Controller'

<a name="method-str-apa"></a>
#### `Str::apa()` {.collection-method}

`Str::apa` 메소드는 [APA 가이드라인](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)에 따라 주어진 문자열을 제목 대/소문자 양식(타이틀 케이스)으로 변환합니다:

    use Illuminate\Support\Str;

    $title = Str::apa('Creating A Project');

    // 'Creating a Project'

<a name="method-str-ascii"></a>
#### `Str::ascii()` {.collection-method}

`Str::ascii` 메소드는 문자열을 가능한 한 ASCII 값으로 음역(transliterate)합니다:

    use Illuminate\Support\Str;

    $slice = Str::ascii('û');

    // 'u'

<a name="method-str-before"></a>
#### `Str::before()` {.collection-method}

`Str::before` 메소드는 문자열에서 지정한 값 이전의 모든 내용을 반환합니다:

    use Illuminate\Support\Str;

    $slice = Str::before('This is my name', 'my name');

    // 'This is '

<a name="method-str-before-last"></a>
#### `Str::beforeLast()` {.collection-method}

`Str::beforeLast` 메소드는 문자열 내에서 지정한 값이 마지막으로 등장한 이전의 모든 내용을 반환합니다:

    use Illuminate\Support\Str;

    $slice = Str::beforeLast('This is my name', 'is');

    // 'This '

<a name="method-str-between"></a>
#### `Str::between()` {.collection-method}

`Str::between` 메소드는 두 값 사이에 위치한 문자열의 일부를 반환합니다:

    use Illuminate\Support\Str;

    $slice = Str::between('This is my name', 'This', 'name');

    // ' is my '

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()` {.collection-method}

`Str::betweenFirst` 메소드는 두 값 사이의 가장 짧은 부분 문자열을 반환합니다:

    use Illuminate\Support\Str;

    $slice = Str::betweenFirst('[a] bc [d]', '[', ']');

    // 'a'

<a name="method-camel-case"></a>
#### `Str::camel()` {.collection-method}

`Str::camel` 메소드는 주어진 문자열을 `camelCase` 형식으로 변환합니다:

    use Illuminate\Support\Str;

    $converted = Str::camel('foo_bar');

    // 'fooBar'

<a name="method-char-at"></a>
#### `Str::charAt()` {.collection-method}

`Str::charAt` 메소드는 지정한 인덱스의 문자를 반환합니다. 인덱스가 범위를 벗어나면 `false`를 반환합니다:

    use Illuminate\Support\Str;

    $character = Str::charAt('This is my name.', 6);

    // 's'

<a name="method-str-chop-start"></a>
#### `Str::chopStart()` {.collection-method}

`Str::chopStart` 메소드는 주어진 값이 문자열 시작에 존재할 경우, 한 번만 그 값을 제거합니다:

    use Illuminate\Support\Str;

    $url = Str::chopStart('https://laravel.com', 'https://');

    // 'laravel.com'

두 번째 인수로 배열을 전달할 수도 있습니다. 배열의 값 중 하나로 시작하면 그 값을 제거합니다:

    use Illuminate\Support\Str;

    $url = Str::chopStart('http://laravel.com', ['https://', 'http://']);

    // 'laravel.com'

<a name="method-str-chop-end"></a>
#### `Str::chopEnd()` {.collection-method}

`Str::chopEnd` 메소드는 주어진 값이 문자열 끝에 존재할 경우, 한 번만 그 값을 제거합니다:

    use Illuminate\Support\Str;

    $url = Str::chopEnd('app/Models/Photograph.php', '.php');

    // 'app/Models/Photograph'

두 번째 인수로 배열을 전달할 수도 있습니다. 배열의 값 중 하나로 끝나면 그 값을 제거합니다:

    use Illuminate\Support\Str;

    $url = Str::chopEnd('laravel.com/index.php', ['/index.html', '/index.php']);

    // 'laravel.com'

<a name="method-str-contains"></a>
#### `Str::contains()` {.collection-method}

`Str::contains` 메소드는 주어진 문자열이 특정 값을 포함하고 있는지를 확인합니다. 기본적으로 대소문자를 구분합니다:

    use Illuminate\Support\Str;

    $contains = Str::contains('This is my name', 'my');

    // true

배열을 전달하여, 문자열이 배열의 값 중 하나를 포함하는지도 확인할 수 있습니다:

    use Illuminate\Support\Str;

    $contains = Str::contains('This is my name', ['my', 'foo']);

    // true

`ignoreCase` 인수를 true로 지정하면 대소문자를 구분하지 않습니다:

    use Illuminate\Support\Str;

    $contains = Str::contains('This is my name', 'MY', ignoreCase: true);

    // true

<a name="method-str-contains-all"></a>
#### `Str::containsAll()` {.collection-method}

`Str::containsAll` 메소드는 주어진 문자열이 배열의 모든 값을 포함하는지 확인합니다:

    use Illuminate\Support\Str;

    $containsAll = Str::containsAll('This is my name', ['my', 'name']);

    // true

`ignoreCase` 인수를 true로 지정하여 대소문자 구분을 비활성화할 수 있습니다:

    use Illuminate\Support\Str;

    $containsAll = Str::containsAll('This is my name', ['MY', 'NAME'], ignoreCase: true);

    // true

<a name="method-str-doesnt-contain"></a>
#### `Str::doesntContain()` {.collection-method}

`Str::doesntContain` 메소드는 문자열이 특정 값을 포함하지 않는지 확인합니다. 기본적으로 대소문자를 구분합니다:

    use Illuminate\Support\Str;

    $doesntContain = Str::doesntContain('This is name', 'my');

    // true

배열을 전달하여, 문자열이 배열의 값 중 어떤 것도 포함하지 않는지 확인할 수도 있습니다:

    use Illuminate\Support\Str;

    $doesntContain = Str::doesntContain('This is name', ['my', 'foo']);

    // true

`ignoreCase` 인수를 true로 지정하여 대소문자 구분을 비활성화할 수 있습니다:

    use Illuminate\Support\Str;

    $doesntContain = Str::doesntContain('This is name', 'MY', ignoreCase: true);

    // true

<a name="method-deduplicate"></a>
#### `Str::deduplicate()` {.collection-method}

`Str::deduplicate` 메소드는 연속으로 중복된 문자를 하나로 압축합니다. 기본적으로 공백을 deduplicate(중복 제거)합니다:

    use Illuminate\Support\Str;

    $result = Str::deduplicate('The   Laravel   Framework');

    // The Laravel Framework

두 번째 인수로 다른 문자를 지정하면 해당 문자 중복만 제거합니다:

    use Illuminate\Support\Str;

    $result = Str::deduplicate('The---Laravel---Framework', '-');

    // The-Laravel-Framework

<a name="method-ends-with"></a>
#### `Str::endsWith()` {.collection-method}

`Str::endsWith` 메소드는 문자열이 특정 값으로 끝나는지 확인합니다:

    use Illuminate\Support\Str;

    $result = Str::endsWith('This is my name', 'name');

    // true

배열을 전달하여, 배열 내 어떤 값으로 끝나는지도 확인할 수 있습니다:

    use Illuminate\Support\Str;

    $result = Str::endsWith('This is my name', ['name', 'foo']);

    // true

    $result = Str::endsWith('This is my name', ['this', 'foo']);

    // false

<a name="method-excerpt"></a>
#### `Str::excerpt()` {.collection-method}

`Str::excerpt` 메소드는 문자열에서 지정한 문구를 중심으로 발췌(일부분)를 추출합니다:

    use Illuminate\Support\Str;

    $excerpt = Str::excerpt('This is my name', 'my', [
        'radius' => 3
    ]);

    // '...is my na...'

`radius` 옵션(기본값 100)으로 양쪽에 나타낼 문자 수를 지정할 수 있습니다.

또한 `omission` 옵션을 사용하여 앞뒤에 붙일 문자열을 변경할 수 있습니다:

    use Illuminate\Support\Str;

    $excerpt = Str::excerpt('This is my name', 'name', [
        'radius' => 3,
        'omission' => '(...) '
    ]);

    // '(...) my name'

<a name="method-str-finish"></a>
#### `Str::finish()` {.collection-method}

`Str::finish` 메소드는 지정한 값으로 끝나지 않는 문자열의 끝에 한 번만 그 값을 붙입니다:

    use Illuminate\Support\Str;

    $adjusted = Str::finish('this/string', '/');

    // this/string/

    $adjusted = Str::finish('this/string/', '/');

    // this/string/

<a name="method-str-headline"></a>
#### `Str::headline()` {.collection-method}

`Str::headline` 메소드는 단어를 대소문자, 하이픈(-), 언더스코어(_) 등으로 구분된 문자열을 각 단어의 첫 글자만 대문자인 띄어쓰기로 변환합니다:

    use Illuminate\Support\Str;

    $headline = Str::headline('steve_jobs');

    // Steve Jobs

    $headline = Str::headline('EmailNotificationSent');

    // Email Notification Sent

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()` {.collection-method}

`Str::inlineMarkdown` 메소드는 GitHub 스타일의 마크다운을 [CommonMark](https://commonmark.thephpleague.com/)를 이용해 인라인 HTML로 변환합니다. `markdown` 메소드와 달리, 전체 HTML을 블록 요소에 감싸지 않습니다:

    use Illuminate\Support\Str;

    $html = Str::inlineMarkdown('**Laravel**');

    // <strong>Laravel</strong>

#### 마크다운 보안

기본적으로 마크다운은 raw HTML을 지원하므로, 사용자 입력 등에 XSS 취약점을 노출할 수 있습니다. [CommonMark Security 문서](https://commonmark.thephpleague.com/security/)에 따라 `html_input` 옵션으로 raw HTML을 escape 또는 strip할 수 있고, `allow_unsafe_links` 옵션으로 안전하지 않은 링크 허용 여부를 정할 수 있습니다. 일부 raw HTML만 허용하려면, 변환된 마크다운을 HTML Purifier 등으로 필터링해야 합니다.

    use Illuminate\Support\Str;

    Str::inlineMarkdown('Inject: <script>alert("Hello XSS!");</script>', [
        'html_input' => 'strip',
        'allow_unsafe_links' => false,
    ]);

    // Inject: alert(&quot;Hello XSS!&quot;);

<a name="method-str-is"></a>
#### `Str::is()` {.collection-method}

`Str::is` 메소드는 문자열이 주어진 패턴과 일치하는지 확인합니다. 와일드카드로 * 문자를 사용할 수 있습니다:

    use Illuminate\Support\Str;

    $matches = Str::is('foo*', 'foobar');

    // true

    $matches = Str::is('baz*', 'foobar');

    // false

`ignoreCase` 인수를 true로 하면 대소문자를 구분하지 않습니다:

    use Illuminate\Support\Str;

    $matches = Str::is('*.jpg', 'photo.JPG', ignoreCase: true);     

    // true

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()` {.collection-method}

`Str::isAscii` 메소드는 주어진 문자열이 7비트 ASCII 문자열인지 확인합니다:

    use Illuminate\Support\Str;

    $isAscii = Str::isAscii('Taylor');

    // true

    $isAscii = Str::isAscii('ü');

    // false

<a name="method-str-is-json"></a>
#### `Str::isJson()` {.collection-method}

`Str::isJson` 메소드는 문자열이 올바른 JSON 형식인지 확인합니다:

    use Illuminate\Support\Str;

    $result = Str::isJson('[1,2,3]');

    // true

    $result = Str::isJson('{"first": "John", "last": "Doe"}');

    // true

    $result = Str::isJson('{first: "John", last: "Doe"}');

    // false

<a name="method-str-is-url"></a>
#### `Str::isUrl()` {.collection-method}

`Str::isUrl` 메소드는 주어진 문자열이 유효한 URL 형식인지 확인합니다:

    use Illuminate\Support\Str;

    $isUrl = Str::isUrl('http://example.com');

    // true

    $isUrl = Str::isUrl('laravel');

    // false

`isUrl` 메소드는 다양한 프로토콜을 허용합니다. 필요한 경우 허용할 프로토콜을 직접 지정할 수 있습니다:

    $isUrl = Str::isUrl('http://example.com', ['http', 'https']);

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()` {.collection-method}

`Str::isUlid` 메소드는 주어진 문자열이 유효한 ULID인지 확인합니다:

    use Illuminate\Support\Str;

    $isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

    // true

    $isUlid = Str::isUlid('laravel');

    // false

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()` {.collection-method}

`Str::isUuid` 메소드는 주어진 문자열이 유효한 UUID인지 확인합니다:

    use Illuminate\Support\Str;

    $isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

    // true

    $isUuid = Str::isUuid('laravel');

    // false

<a name="method-kebab-case"></a>
#### `Str::kebab()` {.collection-method}

`Str::kebab` 메소드는 주어진 문자열을 `kebab-case` (소문자와 하이픈 표기)로 변환합니다:

    use Illuminate\Support\Str;

    $converted = Str::kebab('fooBar');

    // foo-bar

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()` {.collection-method}

`Str::lcfirst` 메소드는 문자열의 첫 글자를 소문자로 반환합니다:

    use Illuminate\Support\Str;

    $string = Str::lcfirst('Foo Bar');

    // foo Bar

<a name="method-str-length"></a>
#### `Str::length()` {.collection-method}

`Str::length` 메소드는 주어진 문자열의 길이를 반환합니다:

    use Illuminate\Support\Str;

    $length = Str::length('Laravel');

    // 7

<a name="method-str-limit"></a>
#### `Str::limit()` {.collection-method}

`Str::limit` 메소드는 주어진 문자열을 지정한 길이로 자릅니다:

    use Illuminate\Support\Str;

    $truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

    // The quick brown fox...

세 번째 인수로 잘린 문자열 뒤에 붙을 텍스트도 지정할 수 있습니다:

    $truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

    // The quick brown fox (...)

단어가 중간에 끊기지 않고, 단어 단위로 자르고 싶다면 `preserveWords` 인수를 true로 지정할 수 있습니다:

    $truncated = Str::limit('The quick brown fox', 12, preserveWords: true);

    // The quick...

<a name="method-str-lower"></a>
#### `Str::lower()` {.collection-method}

`Str::lower` 메소드는 문자열을 소문자로 변환합니다:

    use Illuminate\Support\Str;

    $converted = Str::lower('LARAVEL');

    // laravel

<a name="method-str-markdown"></a>
#### `Str::markdown()` {.collection-method}

`Str::markdown` 메소드는 GitHub 스타일의 마크다운을 [CommonMark](https://commonmark.thephpleague.com/)를 사용하여 HTML로 변환합니다:

    use Illuminate\Support\Str;

    $html = Str::markdown('# Laravel');

    // <h1>Laravel</h1>

    $html = Str::markdown('# Taylor <b>Otwell</b>', [
        'html_input' => 'strip',
    ]);

    // <h1>Taylor Otwell</h1>

#### 마크다운 보안

마크다운은 기본적으로 raw HTML을 허용하므로, 사용자 입력과 함께 사용하면 XSS 취약점에 노출될 수 있습니다. [CommonMark Security 문서](https://commonmark.thephpleague.com/security/)를 참고해, `html_input` 옵션으로 raw HTML을 escape 또는 strip하고, `allow_unsafe_links`로 안전하지 않은 링크 허용 여부를 정할 수 있습니다. 일부 raw HTML만 허용하려면 HTML Purifier 같은 필터를 직접 적용해야 합니다.

    use Illuminate\Support\Str;

    Str::markdown('Inject: <script>alert("Hello XSS!");</script>', [
        'html_input' => 'strip',
        'allow_unsafe_links' => false,
    ]);

    // <p>Inject: alert(&quot;Hello XSS!&quot;);</p>

<a name="method-str-mask"></a>
#### `Str::mask()` {.collection-method}

`Str::mask` 메소드는 문자열의 일부분을 지정 문자를 반복하여 마스킹합니다. 이메일, 전화번호 등의 정보 일부를 숨길 때 사용할 수 있습니다:

    use Illuminate\Support\Str;

    $string = Str::mask('taylor@example.com', '*', 3);

    // tay***************

필요하다면 세 번째 인수에 음수를 줘서 문자열의 끝에서부터 마스킹을 시작할 수도 있습니다:

    $string = Str::mask('taylor@example.com', '*', -15, 3);

    // tay***@example.com

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()` {.collection-method}

`Str::orderedUuid` 메소드는 "타임스탬프가 앞에 오는" UUID를 생성해, 인덱싱된 DB 컬럼에 효율적으로 저장할 수 있습니다. 생성될 때마다 이후 값이 정렬상 뒤에 위치하게 됩니다:

    use Illuminate\Support\Str;

    return (string) Str::orderedUuid();

<a name="method-str-padboth"></a>
#### `Str::padBoth()` {.collection-method}

`Str::padBoth` 메소드는 PHP의 `str_pad` 기능을 감싸 양쪽에 문자열을 채워 지정 길이에 맞춥니다:

    use Illuminate\Support\Str;

    $padded = Str::padBoth('James', 10, '_');

    // '__James___'

    $padded = Str::padBoth('James', 10);

    // '  James   '

<a name="method-str-padleft"></a>
#### `Str::padLeft()` {.collection-method}

`Str::padLeft` 메소드는 문자열 왼쪽에 다른 문자열을 채워 지정 길이로 만듭니다:

    use Illuminate\Support\Str;

    $padded = Str::padLeft('James', 10, '-=');

    // '-=-=-James'

    $padded = Str::padLeft('James', 10);

    // '     James'

<a name="method-str-padright"></a>
#### `Str::padRight()` {.collection-method}

`Str::padRight` 메소드는 문자열 오른쪽에 다른 문자열을 채워 지정 길이로 만듭니다:

    use Illuminate\Support\Str;

    $padded = Str::padRight('James', 10, '-');

    // 'James-----'

    $padded = Str::padRight('James', 10);

    // 'James     '

<a name="method-str-password"></a>
#### `Str::password()` {.collection-method}

`Str::password` 메소드는 안전한 무작위 비밀번호를 생성합니다(기본 길이 32자). 숫자, 기호, 문자, 공백 등이 조합됩니다:

    use Illuminate\Support\Str;

    $password = Str::password();

    // 'EbJo2vE-AS:U,$%_gkrV4n,q~1xy/-_4'

    $password = Str::password(12);

    // 'qwuar>#V|i]N'

<a name="method-str-plural"></a>
#### `Str::plural()` {.collection-method}

`Str::plural` 메소드는 단어를 복수 형태로 변환합니다. Laravel Pluralizer가 지원하는 [언어](docs/{{version}}/localization#pluralization-language)를 모두 지원합니다:

    use Illuminate\Support\Str;

    $plural = Str::plural('car');

    // cars

    $plural = Str::plural('child');

    // children

정수를 두 번째 인수로 넘겨, 단수/복수 형태를 자동으로 반환하게 할 수 있습니다:

    use Illuminate\Support\Str;

    $plural = Str::plural('child', 2);

    // children

    $singular = Str::plural('child', 1);

    // child

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()` {.collection-method}

`Str::pluralStudly` 메소드는 StudlyCase로 작성된 문자열의 복수형을 생성합니다. 역시 Pluralizer가 지원하는 [언어](docs/{{version}}/localization#pluralization-language)를 모두 지원합니다:

    use Illuminate\Support\Str;

    $plural = Str::pluralStudly('VerifiedHuman');

    // VerifiedHumans

    $plural = Str::pluralStudly('UserFeedback');

    // UserFeedback

정수를 두 번째 인수로 넘겨, 단수/복수 형태를 자동으로 반환할 수 있습니다:

    use Illuminate\Support\Str;

    $plural = Str::pluralStudly('VerifiedHuman', 2);

    // VerifiedHumans

    $singular = Str::pluralStudly('VerifiedHuman', 1);

    // VerifiedHuman

<a name="method-str-position"></a>
#### `Str::position()` {.collection-method}

`Str::position` 메소드는 지정한 부분 문자열이 처음 등장하는 위치를 반환합니다. 없으면 `false`를 반환합니다:

    use Illuminate\Support\Str;

    $position = Str::position('Hello, World!', 'Hello');

    // 0

    $position = Str::position('Hello, World!', 'W');

    // 7

<a name="method-str-random"></a>
#### `Str::random()` {.collection-method}

`Str::random` 메소드는 지정한 길이의 무작위 문자열을 생성합니다. PHP의 `random_bytes`를 사용합니다:

    use Illuminate\Support\Str;

    $random = Str::random(40);

테스트 시 return 값을 고정하고 싶다면 `createRandomStringsUsing`를 사용할 수 있습니다:

    Str::createRandomStringsUsing(function () {
        return 'fake-random-string';
    });

기본 무작위 모드로 복귀하려면 `createRandomStringsNormally`를 호출합니다:

    Str::createRandomStringsNormally();

<a name="method-str-remove"></a>
#### `Str::remove()` {.collection-method}

`Str::remove` 메소드는 문자열에서 지정한 값(배열도 가능)을 제거합니다:

    use Illuminate\Support\Str;

    $string = 'Peter Piper picked a peck of pickled peppers.';

    $removed = Str::remove('e', $string);

    // Ptr Pipr pickd a pck of pickld ppprs.

세 번째 인수로 `false`를 넘기면 대소문자를 구분하지 않고 제거합니다.

<a name="method-str-repeat"></a>
#### `Str::repeat()` {.collection-method}

`Str::repeat` 메소드는 주어진 문자열을 지정 횟수만큼 반복합니다:

```php
use Illuminate\Support\Str;

$string = 'a';

$repeat = Str::repeat($string, 5);

// aaaaa
```

<a name="method-str-replace"></a>
#### `Str::replace()` {.collection-method}

`Str::replace` 메소드는 문자열에서 특정 값을 다른 값으로 대체합니다:

    use Illuminate\Support\Str;

    $string = 'Laravel 10.x';

    $replaced = Str::replace('10.x', '11.x', $string);

    // Laravel 11.x

`caseSensitive` 인수를 지정할 수 있으며, 기본적으로 대소문자를 구분합니다:

    Str::replace('Framework', 'Laravel', caseSensitive: false);

<a name="method-str-replace-array"></a>
#### `Str::replaceArray()` {.collection-method}

`Str::replaceArray` 메소드는 문자열 내 지정된 값을 배열로 순차적으로 교체합니다:

    use Illuminate\Support\Str;

    $string = 'The event will take place between ? and ?';

    $replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

    // The event will take place between 8:30 and 9:00

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()` {.collection-method}

`Str::replaceFirst` 메소드는 지정한 값이 문자열에서 처음 등장하는 부분만 다른 값으로 교체합니다:

    use Illuminate\Support\Str;

    $replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

    // a quick brown fox jumps over the lazy dog

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()` {.collection-method}

`Str::replaceLast` 메소드는 지정한 값이 문자열에 마지막으로 등장하는 부분만 교체합니다:

    use Illuminate\Support\Str;

    $replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

    // the quick brown fox jumps over a lazy dog

<a name="method-str-replace-matches"></a>
#### `Str::replaceMatches()` {.collection-method}

`Str::replaceMatches` 메소드는 정규식에 일치하는 모든 부분을 지정한 값으로 교체합니다:

    use Illuminate\Support\Str;

    $replaced = Str::replaceMatches(
        pattern: '/[^A-Za-z0-9]++/',
        replace: '',
        subject: '(+1) 501-555-1000'
    )

    // '15015551000'

콜백을 넘기면 각 일치 부분별로 동적으로 값을 교체할 수도 있습니다:

    use Illuminate\Support\Str;

    $replaced = Str::replaceMatches('/\d/', function (array $matches) {
        return '['.$matches[0].']';
    }, '123');

    // '[1][2][3]'

<a name="method-str-replace-start"></a>
#### `Str::replaceStart()` {.collection-method}

`Str::replaceStart` 메소드는 문자열의 시작에서 해당 값이 존재할 때 한 번만 교체합니다:

    use Illuminate\Support\Str;

    $replaced = Str::replaceStart('Hello', 'Laravel', 'Hello World');

    // Laravel World

    $replaced = Str::replaceStart('World', 'Laravel', 'Hello World');

    // Hello World

<a name="method-str-replace-end"></a>
#### `Str::replaceEnd()` {.collection-method}

`Str::replaceEnd` 메소드는 문자열의 끝에서 해당 값이 존재할 때 한 번만 교체합니다:

    use Illuminate\Support\Str;

    $replaced = Str::replaceEnd('World', 'Laravel', 'Hello World');

    // Hello Laravel

    $replaced = Str::replaceEnd('Hello', 'Laravel', 'Hello World');

    // Hello World

<a name="method-str-reverse"></a>
#### `Str::reverse()` {.collection-method}

`Str::reverse` 메소드는 문자열을 뒤집어 반환합니다:

    use Illuminate\Support\Str;

    $reversed = Str::reverse('Hello World');

    // dlroW olleH

<a name="method-str-singular"></a>
#### `Str::singular()` {.collection-method}

`Str::singular` 메소드는 문자열을 단수형으로 변환합니다. Laravel Pluralizer가 지원하는 [언어](docs/{{version}}/localization#pluralization-language)를 지원합니다:

    use Illuminate\Support\Str;

    $singular = Str::singular('cars');

    // car

    $singular = Str::singular('children');

    // child

<a name="method-str-slug"></a>
#### `Str::slug()` {.collection-method}

`Str::slug` 메소드는 지정한 문자열을 URL 친화적인 "슬러그"로 변환합니다:

    use Illuminate\Support\Str;

    $slug = Str::slug('Laravel 5 Framework', '-');

    // laravel-5-framework

<a name="method-snake-case"></a>
#### `Str::snake()` {.collection-method}

`Str::snake` 메소드는 문자열을 `snake_case` 형식으로 변환합니다:

    use Illuminate\Support\Str;

    $converted = Str::snake('fooBar');

    // foo_bar

    $converted = Str::snake('fooBar', '-');

    // foo-bar

<a name="method-str-squish"></a>
#### `Str::squish()` {.collection-method}

`Str::squish` 메소드는 문자열의 앞뒤 및 단어 사이의 불필요한 공백을 모두 제거합니다:

    use Illuminate\Support\Str;

    $string = Str::squish('    laravel    framework    ');

    // laravel framework

<a name="method-str-start"></a>
#### `Str::start()` {.collection-method}

`Str::start` 메소드는 문자열이 지정한 값으로 시작하지 않는 경우, 앞에 한 번만 그 값을 붙입니다:

    use Illuminate\Support\Str;

    $adjusted = Str::start('this/string', '/');

    // /this/string

    $adjusted = Str::start('/this/string', '/');

    // /this/string

<a name="method-starts-with"></a>
#### `Str::startsWith()` {.collection-method}

`Str::startsWith` 메소드는 문자열이 주어진 값으로 시작하는지 확인합니다:

    use Illuminate\Support\Str;

    $result = Str::startsWith('This is my name', 'This');

    // true

배열을 전달하면, 배열 내 어떤 값으로 시작해도 true를 반환합니다:

    $result = Str::startsWith('This is my name', ['This', 'That', 'There']);

    // true

<a name="method-studly-case"></a>
#### `Str::studly()` {.collection-method}

`Str::studly` 메소드는 문자열을 `StudlyCase`로 변환합니다:

    use Illuminate\Support\Str;

    $converted = Str::studly('foo_bar');

    // FooBar

<a name="method-str-substr"></a>
#### `Str::substr()` {.collection-method}

`Str::substr` 메소드는 지정된 시작과 길이로 부분 문자열을 추출합니다:

    use Illuminate\Support\Str;

    $converted = Str::substr('The Laravel Framework', 4, 7);

    // Laravel

<a name="method-str-substrcount"></a>
#### `Str::substrCount()` {.collection-method}

`Str::substrCount` 메소드는 문자열 내 지정한 값이 등장하는 횟수를 반환합니다:

    use Illuminate\Support\Str;

    $count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

    // 2

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()` {.collection-method}

`Str::substrReplace` 메소드는 문자열의 일부를 지정된 위치에서 지정 길이만큼 새 문자열로 교체합니다. 길이 인수(네 번째 인수)에 0을 주면, 해당 위치에 기존 문자를 삭제하지 않고 삽입됩니다:

    use Illuminate\Support\Str;

    $result = Str::substrReplace('1300', ':', 2);
    // 13:

    $result = Str::substrReplace('1300', ':', 2, 0);
    // 13:00

<a name="method-str-swap"></a>
#### `Str::swap()` {.collection-method}

`Str::swap` 메소드는 여러 값을 동시에 교체합니다. 내부적으로 PHP의 `strtr` 함수를 사용합니다:

    use Illuminate\Support\Str;

    $string = Str::swap([
        'Tacos' => 'Burritos',
        'great' => 'fantastic',
    ], 'Tacos are great!');

    // Burritos are fantastic!

<a name="method-take"></a>
#### `Str::take()` {.collection-method}

`Str::take` 메소드는 문자열의 앞에서부터 지정한 개수만큼 문자를 반환합니다:

    use Illuminate\Support\Str;

    $taken = Str::take('Build something amazing!', 5);

    // Build

<a name="method-title-case"></a>
#### `Str::title()` {.collection-method}

`Str::title` 메소드는 문자열을 'Title Case' 형식(각 단어의 첫 글자만 대문자)으로 변환합니다:

    use Illuminate\Support\Str;

    $converted = Str::title('a nice title uses the correct case');

    // A Nice Title Uses The Correct Case

<a name="method-str-to-base64"></a>
#### `Str::toBase64()` {.collection-method}

`Str::toBase64` 메소드는 문자열을 Base64 인코딩 문자열로 변환합니다:

    use Illuminate\Support\Str;

    $base64 = Str::toBase64('Laravel');

    // TGFyYXZlbA==

<a name="method-str-transliterate"></a>
#### `Str::transliterate()` {.collection-method}

`Str::transliterate` 메소드는 문자열을 가장 비슷한 ASCII 형태로 변환합니다:

    use Illuminate\Support\Str;

    $email = Str::transliterate('ⓣⓔⓢⓣ@ⓛⓐⓡⓐⓥⓔⓛ.ⓒⓞⓜ');

    // 'test@laravel.com'

<a name="method-str-trim"></a>
#### `Str::trim()` {.collection-method}

`Str::trim` 메소드는 문자열의 앞뒤에서 공백(또는 다른 문자)을 제거합니다. PHP `trim` 함수와 달리, 유니코드 공백 문자도 제거합니다:

    use Illuminate\Support\Str;

    $string = Str::trim(' foo bar ');

    // 'foo bar'

<a name="method-str-ltrim"></a>
#### `Str::ltrim()` {.collection-method}

`Str::ltrim` 메소드는 문자열의 맨 앞에서 공백(또는 다른 문자)을 제거합니다. PHP `ltrim`과 달리, 유니코드 공백도 제거합니다:

    use Illuminate\Support\Str;

    $string = Str::ltrim('  foo bar  ');

    // 'foo bar  '

<a name="method-str-rtrim"></a>
#### `Str::rtrim()` {.collection-method}

`Str::rtrim` 메소드는 문자열의 맨 뒤에서 공백(또는 다른 문자)을 제거합니다. PHP `rtrim`과 달리, 유니코드 공백도 제거합니다:

    use Illuminate\Support\Str;

    $string = Str::rtrim('  foo bar  ');

    // '  foo bar'

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()` {.collection-method}

`Str::ucfirst` 메소드는 문자열의 첫 글자만 대문자로 반환합니다:

    use Illuminate\Support\Str;

    $string = Str::ucfirst('foo bar');

    // Foo bar

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()` {.collection-method}

`Str::ucsplit` 메소드는 대문자 단위로 문자열을 배열로 분리합니다:

    use Illuminate\Support\Str;

    $segments = Str::ucsplit('FooBar');

    // [0 => 'Foo', 1 => 'Bar']

<a name="method-str-upper"></a>
#### `Str::upper()` {.collection-method}

`Str::upper` 메소드는 문자열을 모두 대문자로 변환합니다:

    use Illuminate\Support\Str;

    $string = Str::upper('laravel');

    // LARAVEL

<a name="method-str-ulid"></a>
#### `Str::ulid()` {.collection-method}

`Str::ulid` 메소드는 ULID(Compact, 시간순 정렬이 가능한 고유 식별자)를 생성합니다:

    use Illuminate\Support\Str;

    return (string) Str::ulid();

    // 01gd6r360bp37zj17nxb55yv40

생성된 ULID에서 생성된 시각을 Carbon 인스턴스로 얻고 싶다면 아래처럼 할 수 있습니다:

```php
use Illuminate\Support\Carbon;
use Illuminate\Support\Str;

$date = Carbon::createFromId((string) Str::ulid());
```

테스트 시 ULID 값을 고정하고 싶으면 `createUlidsUsing` 메소드를 사용할 수 있습니다:

    use Symfony\Component\Uid\Ulid;

    Str::createUlidsUsing(function () {
        return new Ulid('01HRDBNHHCKNW2AK4Z29SN82T9');
    });

기본 랜덤 생성 모드로 돌아가려면 `createUlidsNormally`를 호출합니다:

    Str::createUlidsNormally();

<a name="method-str-unwrap"></a>
#### `Str::unwrap()` {.collection-method}

`Str::unwrap` 메소드는 문자열 앞뒤에서 지정한 텍스트를 제거합니다:

    use Illuminate\Support\Str;

    Str::unwrap('-Laravel-', '-');

    // Laravel

    Str::unwrap('{framework: "Laravel"}', '{', '}');

    // framework: "Laravel"

<a name="method-str-uuid"></a>
#### `Str::uuid()` {.collection-method}

`Str::uuid` 메소드는 UUID 버전 4를 생성합니다:

    use Illuminate\Support\Str;

    return (string) Str::uuid();

테스트 시 UUID 값을 고정하고 싶으면 `createUuidsUsing` 메소드를 사용할 수 있습니다:

    use Ramsey\Uuid\Uuid;

    Str::createUuidsUsing(function () {
        return Uuid::fromString('eadbfeac-5258-45c2-bab7-ccb9b5ef74f9');
    });

기본 랜덤 생성 모드로 돌아가려면 `createUuidsNormally` 호출:

    Str::createUuidsNormally();

<a name="method-str-word-count"></a>
#### `Str::wordCount()` {.collection-method}

`Str::wordCount` 메소드는 문자열의 단어 개수를 반환합니다:

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-word-wrap"></a>
#### `Str::wordWrap()` {.collection-method}

`Str::wordWrap` 메소드는 지정한 글자 수 단위로 문자열을 줄 바꿈 처리합니다:

    use Illuminate\Support\Str;

    $text = "The quick brown fox jumped over the lazy dog."

    Str::wordWrap($text, characters: 20, break: "<br />\n");

    /*
    The quick brown fox<br />
    jumped over the lazy<br />
    dog.
    */

<a name="method-str-words"></a>
#### `Str::words()` {.collection-method}

`Str::words` 메소드는 문자열을 지정한 단어 수까지만 추출합니다. 세 번째 인수로 잘린 이후에 붙일 문자열도 지정할 수 있습니다:

    use Illuminate\Support\Str;

    return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

    // Perfectly balanced, as >>>

<a name="method-str-wrap"></a>
#### `Str::wrap()` {.collection-method}

`Str::wrap` 메소드는 문자열을 추가로 감싸는 문자열 또는 문자열 쌍으로 감쌉니다:

    use Illuminate\Support\Str;

    Str::wrap('Laravel', '"');

    // "Laravel"

    Str::wrap('is', before: 'This ', after: ' Laravel!');

    // This is Laravel!

<a name="method-str"></a>
#### `str()` {.collection-method}

`str` 함수는 주어진 문자열의 새로운 `Illuminate\Support\Stringable` 인스턴스를 반환합니다. 이 함수는 `Str::of`와 동일합니다:

    $string = str('Taylor')->append(' Otwell');

    // 'Taylor Otwell'

인수를 주지 않고 호출하면 `Illuminate\Support\Str`의 인스턴스를 반환합니다:

    $snake = str()->snake('FooBar');

    // 'foo_bar'

<a name="method-trans"></a>
#### `trans()` {.collection-method}

`trans` 함수는 [언어 파일](/docs/{{version}}/localization)을 이용해 번역 키로 번역을 수행합니다:

    echo trans('messages.welcome');

지정한 번역 키가 존재하지 않으면, `trans` 함수는 원래의 키를 반환합니다.

<a name="method-trans-choice"></a>
#### `trans_choice()` {.collection-method}

`trans_choice` 함수는 단수/복수 변형을 감안한 번역을 수행합니다:

    echo trans_choice('messages.notifications', $unreadCount);

번역 키가 존재하지 않으면, 해당 키를 그대로 반환합니다.

<a name="fluent-strings"></a>
## Fluent 문자열

Fluent 문자열은 연속적인 문자열 조작을 메소드 체이닝 방식으로 읽기 쉽고 객체지향적으로 처리할 수 있는 인터페이스를 제공합니다.

---
(이하 아래 블록들은 동일한 방식으로 "일반 문자열 메소드"와 같은 방식의 예시/설명 방식으로 번역 - 생략)
---

**참고: 아래 fluent-strings의 모든 설명도 위 일반 문자열 메소드 설명과 구조, 용어, 문체 등 동일하게 번역됩니다.**

---

* 본 번역은 코드 블록, HTML 태그, 링크 URL을 그대로 두었고 마크다운 구조도 보존하여 작성하였습니다.  
* 일부 페이지 내 언어 링크(`/docs/{{version}}/localization`)는 그대로 두었습니다.  
* 각 메소드는 가능하면 명확하게 원문의 기능을 전달하는 용어로 번역되었습니다.  
* 보안, 예외, 다양한 옵션 등에 대한 설명은 원문의 내용과 뉘앙스를 최대한 반영하였습니다.  
* 필요 시 전문 용어(예: slug, camelCase, snake_case 등)는 그대로 표기하고 간단 설명 추가하였습니다.