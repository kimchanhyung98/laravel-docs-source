# 업그레이드 가이드 (Upgrade Guide)

- [11.x에서 12.0으로 업그레이드하기](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 영향이 큰 변경 사항

<div class="content-list" markdown="1">

- [의존성 업데이트](#updating-dependencies)
- [라라벨 인스톨러 업데이트](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 영향이 중간 정도인 변경 사항

<div class="content-list" markdown="1">

- [모델과 UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 영향이 적은 변경 사항

<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [동시성 결과 인덱스 매핑](#concurrency-result-index-mapping)
- [컨테이너 클래스 의존성 해결 방식](#container-class-dependency-resolution)
- [이미지 유효성 검증 시 SVG 제외](#image-validation)
- [다중 스키마 데이터베이스 조회](#multi-schema-database-inspecting)
- [중첩 배열 요청 병합](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x에서 12.0으로 업그레이드하기

#### 예상 업그레이드 시간: 5분

> [!NOTE]
> 가능한 모든 주요 변경 사항을 문서화하고자 노력합니다. 하지만 이 중 일부 변경 사항은 프레임워크의 잘 사용되지 않는 부분에 해당하므로, 실제로 귀하의 애플리케이션에 영향을 주는 부분은 일부일 수 있습니다. 시간을 절약하고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하여 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
### 의존성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 의존성 버전을 업데이트해야 합니다.

<div class="content-list" markdown="1">

- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`을 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

</div>

<a name="carbon-3"></a>
#### Carbon 3

**영향 가능성: 낮음**

[Carbon 2.x](https://carbon.nesbot.com/docs/)에 대한 지원이 제거되었습니다. 이제 모든 Laravel 12 애플리케이션은 [Carbon 3.x](https://carbon.nesbot.com/docs/#api-carbon-3)를 필수로 사용해야 합니다.

<a name="updating-the-laravel-installer"></a>
### 라라벨 인스톨러 업데이트

새로운 라라벨 애플리케이션을 만들 때 라라벨 인스톨러 CLI 도구를 사용한다면, 인스톨러를 12.x 및 [새로운 라라벨 스타터 킷](https://laravel.com/starter-kits)과 호환되도록 반드시 업데이트해야 합니다. 만약 `composer global require`로 설치했다면, 아래 명령어로 인스톨러를 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

만약 `php.new`로 PHP와 라라벨을 처음 설치했다면, 사용 중인 OS 환경에 맞게 `php.new` 설치 명령어를 다시 실행해서 최신 버전의 PHP와 라라벨 인스톨러를 설치하면 됩니다.

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# 관리자 권한으로 실행...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

또는, [Laravel Herd](https://herd.laravel.com)에서 제공하는 라라벨 인스톨러 번들 버전을 사용 중이라면, Herd를 최신 버전으로 업데이트해야 합니다.

<a name="authentication"></a>
### 인증

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자에서 `$expires` 파라미터는 이제 '분'이 아닌 '초' 단위로 전달해야 합니다.

<a name="concurrency"></a>
### 동시성(Concurrency)

<a name="concurrency-result-index-mapping"></a>
#### 동시성 결과 인덱스 매핑

**영향 가능성: 낮음**

`Concurrency::run` 메서드에 연관 배열을 전달하면, 동시 실행 작업의 결과가 각각의 키에 매핑되어 반환됩니다.

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
#### 컨테이너 클래스 의존성 해결 방식

**영향 가능성: 낮음**

의존성 주입 컨테이너가 클래스 인스턴스를 해결할 때, 이제 클래스 속성(property)의 기본값도 존중합니다. 이전에는 기본값 없이 인스턴스를 생성했다면, 이번 변경으로 코드에 해당 동작을 반영해야 할 수 있습니다.

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
#### 다중 스키마 데이터베이스 조회

**영향 가능성: 낮음**

`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마의 결과를 포함합니다. 특정 스키마에 대해서만 결과를 조회하려면 `schema` 인수를 사용할 수 있습니다.

```php
// 모든 스키마의 테이블...
$tables = Schema::getTables();

// 'main' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: 'main');

// 'main', 'blog' 스키마의 모든 테이블...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 포함된 테이블 이름을 반환합니다. 원하는 동작으로 변경하려면 `schemaQualified` 인수를 사용할 수 있습니다.

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` 및 `db:show` 명령어는 이제 MySQL, MariaDB, SQLite에서 PostgreSQL 및 SQL Server와 같이 모든 스키마의 결과를 출력합니다.

<a name="updated-blueprint-constructor-signature"></a>
#### `Blueprint` 생성자 시그니처 변경

**영향 가능성: 매우 낮음**

`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫 번째 인수로 `Illuminate\Database\Connection` 인스턴스를 기대합니다.

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### 모델과 UUIDv7

**영향 가능성: 중간**

이제 `HasUuids` 트레잇은 UUID 스펙 버전 7(정렬 가능한 UUID)에 맞는 값을 반환합니다. 모델의 ID로 기존처럼 정렬 가능한 UUIDv4 문자열을 계속 사용하고 싶다면, 이제 `HasVersion4Uuids` 트레잇을 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 트레잇은 제거되었습니다. 이전에 이 트레잇을 사용했다면, 그 대신 이제 동일한 동작을 제공하는 `HasUuids` 트레잇을 사용해야 합니다.

<a name="requests"></a>
### 요청(Request)

<a name="nested-array-request-merging"></a>
#### 중첩 배열 요청 병합

**영향 가능성: 낮음**

`$request->mergeIfMissing()` 메서드는 이제 "dot" 표기법을 사용하여 중첩 배열 데이터를 병합할 수 있습니다. 기존에는 이 메서드를 이용해 최상위 배열 키에 "dot" 표기법을 가진 키를 생성했다면, 이 변경 사항을 반영하여 코드를 수정해야 할 수 있습니다.

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="validation"></a>
### 유효성 검증(Validation)

<a name="image-validation"></a>
#### 이미지 유효성 검증 시 SVG 제외

`image` 유효성 검증 규칙은 이제 기본적으로 SVG 이미지를 허용하지 않습니다. `image` 규칙에서 SVG를 허용하려면 명시적으로 옵션을 추가해야 합니다.

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// 또는...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### 기타

또한 `laravel/laravel` [GitHub 저장소](https://github.com/laravel/laravel)의 변경 사항도 확인하시는 것을 권장합니다. 여기의 많은 변경 사항은 필수는 아니지만, 애플리케이션과 동기화할 수 있습니다. 일부 변경 내용은 이 업그레이드 가이드에서 다루지만, 설정 파일이나 주석(comment) 변경과 같이 다루지 않는 부분도 있습니다. [GitHub 비교 도구](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용해 변경점을 쉽게 확인하고, 필요한 부분만 선택적으로 업데이트할 수 있습니다.
