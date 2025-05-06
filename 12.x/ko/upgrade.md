# 업그레이드 가이드

- [11.x에서 12.0으로 업그레이드하기](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 영향이 큰 변경 사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [Laravel Installer 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 중간 정도 영향의 변경 사항

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 영향이 적은 변경 사항

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해결](#container-class-dependency-resolution)
- [이미지 유효성 검사에서 SVG 제외](#image-validation)
- [다중 스키마 데이터베이스 검사](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드하기

#### 예상 소요 시간: 5분

> [!NOTE]
> 가능한 모든 파손 변경 사항을 문서화하려고 노력했습니다. 이 중 일부는 프레임워크의 잘 알려지지 않은 부분에 해당하므로 실제로는 일부 변경사항만이 여러분의 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용해 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다:

<div class="content-list" markdown="1">

- `laravel/framework`을 `^12.0`으로
- `phpunit/phpunit`을 `^11.0`으로
- `pestphp/pest`을 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

[Carbon 2.x](https://carbon.nesbot.com/docs/)에 대한 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션은 이제 [Carbon 3.x](https://carbon.nesbot.com/docs/#api-carbon-3)를 필요로 합니다.

<a name="updating-the-laravel-installer"></a>
### Laravel Installer 업데이트

Laravel 새 프로젝트 생성을 위해 Laravel Installer CLI 도구를 사용 중이라면, Installer를 12.x 및 [새 Laravel 스타터 킷](https://laravel.com/starter-kits)과 호환되도록 업데이트해야 합니다. 만약 `composer global require`로 설치했다면, 아래 명령어로 업데이트할 수 있습니다:

```shell
composer global update laravel/installer
```

만약 PHP와 Laravel을 `php.new`를 통해 설치했다면, 운영 체제에 맞는 `php.new` 설치 명령을 재실행하면 최신 PHP와 Laravel Installer를 다시 설치할 수 있습니다:

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자 권한으로 실행하세요...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

또는, [Laravel Herd](https://herd.laravel.com)에 번들된 Laravel Installer를 사용 중이라면 Herd를 최신 버전으로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 업데이트

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자가 이제 `$expires` 매개변수를 분 단위가 아닌 초 단위로 받도록 변경되었습니다.

<a name="concurrency"></a>
### 동시성

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑

**영향 가능성: 낮음**

`Concurrency::run` 메서드를 연관 배열과 함께 호출할 때, 동시 작업의 결과가 해당 키와 함께 반환됩니다:

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
### 컨테이너

<a name="container-class-dependency-resolution"></a>
#### 컨테이너 클래스 의존성 해결

**영향 가능성: 낮음**

의존성 주입 컨테이너가 이제 클래스 프로퍼티의 기본값을 존중하여 클래스 인스턴스를 해석합니다. 만약 이전에 기본값 없이 컨테이너가 클래스를 해석하는 것에 의존하고 있었다면, 이 동작 변경을 고려하여 애플리케이션을 조정해야 할 수 있습니다:

```php
class Example
{
    public function __construct(public ?Carbon $date = null) {}
}

$example = resolve(Example::class);

// <= 11.x
$example->date instanceof Carbon;

// >= 12.x
$example->date === null;
```

<a name="database"></a>
### 데이터베이스

<a name="multi-schema-database-inspecting"></a>
#### 다중 스키마 데이터베이스 검사

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마의 결과를 포함합니다. 특정 스키마만 조회하려면 `schema` 인자를 전달할 수 있습니다:

```php
// 모든 스키마의 모든 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$table = Schema::getTables(schema: 'main');

// 'main' 및 'blog' 스키마의 모든 테이블...
$table = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 포함된 테이블명을 반환합니다. 원한다면 `schemaQualified` 인자를 이용해 동작을 변경할 수 있습니다:

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$table = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$table = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` 및 `db:show` 명령은 이제 MySQL, MariaDB, SQLite에서도 PostgreSQL, SQL Server와 마찬가지로 모든 스키마의 결과를 출력합니다.

<a name="updated-blueprint-constructor-signature"></a>
#### `Blueprint` 생성자 시그니처 업데이트

**영향 가능성: 매우 낮음**

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자가 이제 첫 번째 인자로 `Illuminate\Database\Connection` 인스턴스를 받도록 변경되었습니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7

**영향 가능성: 중간**

`HasUuids` 트레잇이 이제 UUID 스펙 버전 7(순차적 UUID)과 호환되는 UUID를 반환합니다. 여전히 모델의 ID에 순차적 UUIDv4 문자열을 사용하고 싶다면 이제 `HasVersion4Uuids` 트레잇을 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레잇은 제거되었습니다. 이전에 이 트레잇을 사용했다면 이제 동일한 동작을 제공하는 `HasUuids` 트레잇을 사용하면 됩니다.

<a name="requests"></a>
### Request

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "dot" 표기법을 사용해 중첩 배열 데이터를 병합할 수 있습니다. 이전까지 이 메서드가 "dot" 표기법 키를 포함하는 최상위 배열 키를 생성하는 것에 의존했다면, 이번 변화에 맞게 애플리케이션을 조정해야 할 수 있습니다:

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="validation"></a>
### 유효성 검사

<a name="image-validation"></a>
#### 이미지 유효성 검사 규칙에서 SVG 제외

`image` 유효성 검사 규칙이 이제 기본적으로 SVG 이미지를 허용하지 않습니다. `image` 규칙을 사용할 때 SVG를 허용하고 싶다면 명시적으로 허용해야 합니다:

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타

`laravel/laravel` [깃허브 저장소](https://github.com/laravel/laravel)의 변경점도 참고하시길 권장합니다. 많은 변경사항은 필수 사항이 아니지만 코드 동기화를 고려해볼 수 있습니다. 이 가이드에서 다루는 변경사항 외에 설정 파일, 주석 등 일부 변경사항은 다루지 않습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)로 변경점을 쉽게 확인하고, 필요한 업데이트만 선택적으로 적용할 수 있습니다.