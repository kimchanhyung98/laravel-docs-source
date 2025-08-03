# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [지연 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [선택문](#select-statements)
- [원시 표현식](#raw-expressions)
- [조인](#joins)
- [합집합 (Unions)](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All / None 절](#where-any-all-none-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가 Where 절](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전문 텍스트 Where 절](#full-text-where-clauses)
- [정렬, 그룹화, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [제한 및 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [삽입문](#insert-statements)
    - [업서트](#upserts)
- [업데이트문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [삭제문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 쉽게 만들고 실행할 수 있는 편리하고 직관적인 인터페이스를 제공합니다. 애플리케이션 내에서 대부분의 데이터베이스 작업에 사용할 수 있으며, Laravel에서 지원하는 모든 데이터베이스 시스템과 완벽하게 작동합니다.

Laravel 쿼리 빌더는 PDO 매개변수 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 따라서 쿼리 바인딩에 전달되는 문자열을 별도로 정리하거나 클린징할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조하는 컬럼명을, 특히 "order by" 컬럼을 사용자 입력에 의해 결정되도록 절대 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회

`DB` 파사드가 제공하는 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대해 플루언트 쿼리 빌더 인스턴스를 반환하여, 더 많은 제약 조건을 체인 방식으로 추가하고 `get` 메서드를 호출해 최종적으로 쿼리 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 컬렉션 내 각 결과는 PHP `stdClass` 객체의 인스턴스입니다. 각 컬럼의 값은 해당 객체 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터를 매핑하고 축소할 때 매우 강력한 메서드를 제공합니다. Laravel 컬렉션에 대해 더 알고 싶다면 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 단일 행 또는 컬럼 조회

테이블에서 단일 행만 조회할 경우, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 조건에 맞는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 던질 `firstOrFail` 메서드를 사용할 수도 있습니다. 이 예외가 잡히지 않으면 클라이언트에 자동으로 404 HTTP 응답이 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않고 단일 값만 추출하려면 `value` 메서드를 사용하세요. 이 메서드는 컬럼 값을 직접 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 값으로 단일 행을 조회할 때에는 `find` 메서드를 사용합니다:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 리스트 조회

단일 컬럼의 값만 담은 `Illuminate\Support\Collection` 인스턴스를 얻으려면 `pluck` 메서드를 사용합니다. 다음 예시는 사용자 타이틀을 수집합니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인자로 키로 사용할 컬럼명을 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기

수천 개 이상의 데이터 레코드를 다뤄야 한다면, `DB` 파사드의 `chunk` 메서드를 사용하는 것을 고려하세요. 이 메서드는 결과를 작은 청크 단위로 나누어 각각을 클로저에 전달해 처리할 수 있도록 합니다. 예를 들면, `users` 테이블 전체를 100개씩 청크 단위로 불러오는 방법은 다음과 같습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리를 중단할 수도 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중에 데이터 업데이트가 필요하다면, 결과가 예상하지 못하게 변할 수 있으므로 `chunkById` 메서드를 사용하는 것이 좋습니다. 이 메서드는 자동으로 기본 키를 기준으로 페이징 처리합니다:

```php
DB::table('users')->where('active', false)
    ->chunkById(100, function (Collection $users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```

`chunkById`와 `lazyById` 메서드는 실행 중인 쿼리에 자체 "where" 조건을 추가하므로, 보통 사용자 조건들을 [논리적 그룹화](#logical-grouping)하여 아래와 같이 클로저 안에 묶는 것이 좋습니다:

```php
DB::table('users')->where(function ($query) {
    $query->where('credits', 1)->orWhere('credits', 2);
})->chunkById(100, function (Collection $users) {
    foreach ($users as $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['credits' => 3]);
    }
});
```

> [!WARNING]
> 청크 콜백 내에서 레코드를 업데이트하거나 삭제하는 경우, 기본 키(primary key) 또는 외래 키(foreign key) 변경이 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 특정 레코드가 청크 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍하기 (Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백으로 전달하는 대신 결과를 하나의 스트림처럼 다룰 수 있는 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

역시 조회 도중 업데이트가 필요하다면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 편이 좋습니다. 이 메서드들은 기본 키를 기준으로 자동 페이징을 수행합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 중 레코드를 업데이트하거나 삭제하는 경우, 기본 키나 외래 키 변경으로 인해 결과에서 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 함수를 지원합니다. 쿼리 생성 직후에 이들 메서드를 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론 다른 조건들과 결합해 집계값을 좀 더 세밀하게 산출할 수도 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 판단

조건에 맞는 레코드 존재를 확인할 때 `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## 선택문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### 선택절 지정하기

테이블의 모든 컬럼을 선택하지 않고 특정 컬럼만 조회하고 싶을 때 `select` 메서드를 사용해 쿼리의 select 절을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복 없는 결과만 반환하도록 쿼리를 강제할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있을 때 select 절에 컬럼을 추가하고자 하면 `addSelect` 메서드를 사용합니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## 원시 표현식 (Raw Expressions)

쿼리 내 임의의 문자열을 삽입해야 할 경우, `DB` 파사드가 제공하는 `raw` 메서드를 사용하여 원시 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> 원시 구문은 쿼리에 문자열 그대로 삽입되므로, SQL 인젝션 취약점을 만들지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### 원시 메서드

`DB::raw` 대신 아래 메서드들을 사용해 쿼리의 여러 부분에 원시 표현식을 삽입할 수 있습니다. **단, 원시 표현식을 사용하는 쿼리는 SQL 인젝션 보호를 Laravel이 완전히 보장하지 않음을 기억하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 두 번째 인자로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw` / `orWhereRaw`

이 메서드들은 쿼리에 원시 "where" 절을 삽입할 수 있으며, 두 번째 인자로 바인딩 배열을 받습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw` / `orHavingRaw`

`havingRaw`와 `orHavingRaw`는 원시 문자열을 "having" 절 값으로 사용할 때 씁니다. 두 번째 인자로 바인딩 배열을 받습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

"order by" 절에 원시 문자열을 전달할 때 사용합니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`group by` 절에 원시 문자열을 전달할 때 사용합니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### 내부 조인 절 (Inner Join)

쿼리 빌더는 조인 절을 추가하는 데도 사용할 수 있습니다. 기본적인 "내부 조인"은 `join` 메서드를 활용합니다. 첫 번째 인자는 조인할 테이블명이며, 나머지 인자는 조인의 컬럼 조건을 지정합니다. 여러 테이블을 한 쿼리에 조인하는 것도 가능합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### 좌측 / 우측 조인 절 (Left Join / Right Join)

"내부 조인" 대신 "좌측 조인" 또는 "우측 조인"을 수행하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 인자는 `join` 메서드와 동일합니다:

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### 크로스 조인 (Cross Join)

`crossJoin` 메서드를 사용하면 두 테이블 간의 카티션 곱(Cartesian product)을 생성하는 크로스 조인을 수행할 수 있습니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인을 만들고 싶다면 `join` 메서드에 클로저를 두 번째 인자로 넘길 수 있습니다. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아 조인 조건을 정의할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인 조건에 "where"를 적용할 수도 있습니다. `JoinClause` 인스턴스의 `where` 및 `orWhere` 메서드를 사용해 컬럼과 값 비교를 할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 서브쿼리에 대해 조인을 수행할 수 있습니다. 각 메서드는 세 인자를 받는데, 서브쿼리, 테이블 별칭, 컬럼 관계를 지정하는 클로저가 순서입니다. 예를 들면, 사용자 각각에 대해 가장 최근에 게시한 블로그 포스트의 생성 시간을 함께 조회할 수 있습니다:

```php
$latestPosts = DB::table('posts')
    ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
    ->where('is_published', true)
    ->groupBy('user_id');

$users = DB::table('users')
    ->joinSub($latestPosts, 'latest_posts', function (JoinClause $join) {
        $join->on('users.id', '=', 'latest_posts.user_id');
    })->get();
```

<a name="lateral-joins"></a>
#### 레터럴 조인 (Lateral Joins)

> [!WARNING]
> 레터럴 조인은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용해 서브쿼리와 "레터럴 조인"을 수행할 수 있습니다. 두 인자로 서브쿼리와 테이블 별칭을 받으며, 조인 조건은 서브쿼리 내 `where` 절에서 컬럼 값을 참조하며 지정합니다. 레터럴 조인은 각 행마다 평가되며 서브쿼리 외부 컬럼을 참조할 수 있습니다.

다음 예는 사용자 컬렉션과 각 사용자가 최근 작성한 블로그 포스트 3개를 함께 조회합니다. 사용자는 최대 3개의 행이 결과에 포함될 수 있으며, 현재 사용자의 행을 참조하는 `whereColumn` 조건이 서브쿼리에 있습니다:

```php
$latestPosts = DB::table('posts')
    ->select('id as post_id', 'title as post_title', 'created_at as post_created_at')
    ->whereColumn('user_id', 'users.id')
    ->orderBy('created_at', 'desc')
    ->limit(3);

$users = DB::table('users')
    ->joinLateral($latestPosts, 'latest_posts')
    ->get();
```

<a name="unions"></a>
## 합집합 (Unions)

쿼리 빌더는 두 개 이상의 쿼리를 "union"하는 메서드도 제공합니다. 초기 쿼리를 만들고 `union` 메서드로 다른 쿼리를 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도, 중복 결과를 제거하지 않는 `unionAll` 메서드가 있습니다. `unionAll` 메서드 또한 `union`과 같은 방식으로 사용할 수 있습니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더에서 `where` 메서드를 호출해 "where" 절을 쿼리에 추가할 수 있습니다. 가장 기본적인 `where` 메서드는 세 개의 인자가 필요합니다. 첫 번째 인자는 컬럼명, 두 번째 인자는 비교 연산자(데이터베이스가 지원하는 연산자 중 하나), 세 번째 인자는 컬럼 값과 비교할 값입니다.

예를 들어, 다음 쿼리는 `votes` 컬럼 값이 `100`이고 `age` 컬럼 값이 `35` 초과인 사용자들을 가져옵니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

간편하게 `=` 연산자를 명시하지 않고, 값만 두 번째 인자로 전달할 수 있습니다. 이런 경우 Laravel은 `=` 연산자를 가정합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

연관 배열을 `where` 메서드 인자로 전달하면 복수 컬럼 조건을 한 번에 지정할 수 있습니다:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

위에 적힌 것처럼 데이터베이스가 지원하는 어떤 연산자도 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>=', 100)
    ->get();

$users = DB::table('users')
    ->where('votes', '<>', 100)
    ->get();

$users = DB::table('users')
    ->where('name', 'like', 'T%')
    ->get();
```

또한 `where` 메서드에 조건 배열을 전달할 수도 있습니다. 배열 각 요소는 `where` 메서드에 보통 전달하는 세 인자 배열이어야 합니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않기 때문에, 쿼리에서 참조하는 컬럼명을 사용자 입력에 의해 결정하도록 허용해서는 안 됩니다. 특히 "order by" 컬럼에 주의하세요.

> [!WARNING]
> MySQL과 MariaDB는 문자열과 숫자를 비교할 때 자동으로 타입 캐스팅을 합니다. 예를 들어, 문자열이 숫자가 아닌 경우 `0`으로 캐스팅되기도 합니다. 예를 들어 `secret` 컬럼의 값이 `aaa`이고 `User::where('secret', 0)`를 실행하면 해당 행이 반환됩니다. 따라서 항상 값을 적절한 타입으로 캐스팅한 뒤 쿼리에 사용하세요.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드는 체인 시 기본적으로 조건들을 `AND` 연산자로 연결합니다. 하지만 `orWhere` 메서드를 사용해 `OR` 연산자로 조건을 연결할 수도 있습니다. `orWhere` 메서드도 `where` 메서드와 동일한 인자를 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 묶인 "or" 조건이 필요하면 `orWhere` 메서드에 클로저를 첫 번째 인자로 전달하세요:

```php
use Illuminate\Database\Query\Builder; 

$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
    })
    ->get();
```

위 예시가 생성하는 SQL은 아래와 같습니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> `orWhere` 메서드를 사용할 때는 항상 괄호로 묶어 그룹화해 예상치 못한 글로벌 스코프 적용 문제를 방지하세요.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 주어진 쿼리 제약 조건 그룹을 부정하는 데 사용합니다. 예를 들어, 클리어런스가 아닐 때와 가격이 10보다 작은 경우를 제외하고 상품을 조회한다고 할 때:

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
    })
    ->get();
```

<a name="where-any-all-none-clauses"></a>
### Where Any / All / None 절

동일한 쿼리 조건을 여러 컬럼에 적용해야 할 때가 있습니다. 예를 들어 지정한 컬럼 리스트 중 어떤 컬럼이라도 특정 패턴과 일치하는 레코드를 찾고 싶다면 `whereAny` 메서드를 사용하세요:

```php
$users = DB::table('users')
    ->where('active', true)
    ->whereAny([
        'name',
        'email',
        'phone',
    ], 'like', 'Example%')
    ->get();
```

위 쿼리가 만드는 SQL:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

반대로 `whereAll` 메서드는 모든 컬럼이 지정 조건을 만족할 때 레코드를 조회합니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리의 SQL:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 주어진 컬럼 목록 중 어떤 컬럼도 조건에 맞지 않는 레코드를 조회하는 데 사용합니다:

```php
$posts = DB::table('albums')
    ->where('published', true)
    ->whereNone([
        'title',
        'lyrics',
        'tags',
    ], 'like', '%explicit%')
    ->get();
```

위 쿼리의 SQL:

```sql
SELECT *
FROM albums
WHERE published = true AND NOT (
    title LIKE '%explicit%' OR
    lyrics LIKE '%explicit%' OR
    tags LIKE '%explicit%'
)
```

<a name="json-where-clauses"></a>
### JSON Where 절

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 컬럼 쿼리를 지원합니다. MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12+, SQL Server 2017+, SQLite 3.39.0+에서 사용 가능하며, `->` 연산자를 통해 JSON 키를 지정합니다:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

JSON 배열 항목을 조회하려면 `whereJsonContains` 및 `whereJsonDoesntContain` 메서드를 사용합니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL 사용 시에는 값으로 배열을 넘겨 다중 조건도 가능합니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한 JSON 키 포함 여부는 `whereJsonContainsKey`와 `whereJsonDoesntContainKey` 메서드로 확인합니다:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

JSON 배열 길이로도 조회할 수 있습니다. `whereJsonLength`를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### 추가 Where 절

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

`whereLike` 메서드는 쿼리에 LIKE 조건을 추가해 패턴 매칭을 수행합니다. 기본적으로 대소문자를 구분하지 않고, 데이터베이스에 독립적인 방식으로 작동합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인자를 통해 대소문자 구분 검색도 활성화할 수 있습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 OR 절과 LIKE 조건을 추가합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 NOT LIKE 조건을 추가합니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

유사하게 `orWhereNotLike`는 OR NOT LIKE 조건용입니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 옵션은 현재 SQL Server에서는 지원하지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 컬럼 값이 지정한 배열에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 지정한 배열에 값이 포함되지 않은 경우를 찾습니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 두 번째 인자에 쿼리 객체를 전달할 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예시는 다음 SQL과 같습니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 많은 수의 정수 바인딩을 추가할 때는 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 쓰면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값 범위 밖인지 검증합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 같은 행 내 두 컬럼 값 사이에 대상 컬럼 값이 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 이 범위 밖인 경우를 찾습니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween`은 주어진 값이 같은 행 내 두 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`은 범위 밖인 경우입니다:

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 지정 컬럼 값이 `NULL`인지 검사합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 `NULL`이 아닌 경우입니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

날짜 및 시간 기반 비교 메서드들입니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();

$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();

$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();

$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();

$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

지난 시점, 미래 시점 및 오늘에 대한 비교입니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereBeforeToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereAfterToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

두 컬럼이 같은지 비교하거나 연산자를 사용해 비교할 수 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();

$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

또한 여러 컬럼 쌍을 배열로 지정해 AND 조건으로 사용할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

여러 개의 Where 절을 괄호 내에 논리적으로 그룹화해야 할 때가 있습니다. 특히 `orWhere` 메서드 호출들에는 항상 그룹화를 적용해야 예상치 못한 쿼리 동작을 방지할 수 있습니다. 클로저를 `where` 메서드에 전달해 그룹화를 수행합니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위 구문은 다음과 같은 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> `orWhere` 호출은 언제나 괄호로 그룹화하여 글로벌 스코프 적용 시 예기치 않은 동작을 방지하세요.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 SQL의 "where exists" 절을 작성할 수 있습니다. 클로저를 전달받아 그 내부에서 서브쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

클로저 대신 쿼리 객체를 전달할 수도 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예시는 동일한 다음 SQL을 생성합니다:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```

<a name="subquery-where-clauses"></a>
### 서브쿼리 Where 절

서브쿼리 결과와 비교하는 Where 절도 작성할 수 있습니다. 예를 들어 특정 유형의 최신 "membership"이 있는 사용자를 조회할 때:

```php
use App\Models\User;
use Illuminate\Database\Query\Builder;

$users = User::where(function (Builder $query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```

또는 컬럼과 서브쿼리 결과를 비교할 수도 있습니다. 예를 들어 금액이 평균보다 적은 소득 기록을 조회할 때:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 텍스트 Where 절 (Full Text Where Clauses)

> [!WARNING]
> 전문 텍스트 검색은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 전문 텍스트 인덱스가 설정된 컬럼에 대해 전문 텍스트 검색용 where 절을 추가합니다. Laravel은 데이터베이스 시스템에 맞는 적절한 SQL로 변환하여 실행합니다. 예: MariaDB/MySQL에서는 `MATCH AGAINST`로 변환됩니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한 및 오프셋

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 결과를 지정한 컬럼 기준으로 정렬합니다. 첫 번째 인자는 컬럼명, 두 번째 인자는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

복수 컬럼 기준 정렬을 하려면 `orderBy`를 여러 번 호출하면 됩니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 옵션이며 기본값은 오름차순(asc)입니다. 내림차순 정렬이 필요하면 두 번째 인자에 `desc`를 쓰거나 `orderByDesc` 메서드를 사용하세요:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

JSON 컬럼 내 특정 키를 기준으로 정렬할 수도 있습니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드는 날짜 기준 정렬을 손쉽게 설정합니다. 기본값은 `created_at` 컬럼이며, 원하는 컬럼명을 전달할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위 순서로 정렬할 수 있습니다. 예를 들어, 임의의 사용자를 조회하려면:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거하기

`reorder` 메서드는 쿼리의 기존 "order by" 절을 모두 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder`에 컬럼명과 방향을 전달하면 기존 정렬을 제거하고 새로운 정렬을 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

내림차순 정렬을 적용하려면 `reorderDesc` 메서드를 사용하세요:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`와 `having` 메서드를 이용해 집계 결과를 그룹화하고 필터링할 수 있습니다. `having` 메서드의 시그니처는 `where` 메서드와 유사합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드는 특정 범위 내에 있는 그룹만 필터링할 때 사용합니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy` 메서드에 여러 인자를 전달해 복수 컬럼으로 그룹핑할 수도 있습니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

보다 고급 `having` 구문 작성은 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### 제한 및 오프셋

`limit`과 `offset` 메서드를 사용해 쿼리 결과 개수를 제한하거나 결과 일부를 건너뛸 수 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

특정 조건에 따라 쿼리 절이 적용되도록 하려면 `when` 메서드를 활용하세요. 예를 들어 HTTP 요청 내 특정 입력 값이 있을 때만 `where` 절을 추가하고 싶다면 다음과 같이 합니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인자가 `true`일 때만 클로저를 실행합니다. `false`인 경우 클로저가 실행되지 않습니다.

세 번째 인자로 다른 클로저를 넘겨 첫 번째 인자가 `false`일 때 실행하도록 할 수도 있습니다. 예제는 기본 정렬 설정 시나리오입니다:

```php
$sortByVotes = $request->boolean('sort_by_votes');

$users = DB::table('users')
    ->when($sortByVotes, function (Builder $query, bool $sortByVotes) {
        $query->orderBy('votes');
    }, function (Builder $query) {
        $query->orderBy('name');
    })
    ->get();
```

<a name="insert-statements"></a>
## 삽입문 (Insert Statements)

쿼리 빌더는 `insert` 메서드를 사용해 테이블에 레코드를 삽입할 수 있습니다. `insert`는 컬럼명과 값을 담은 배열을 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

복수 레코드를 한번에 삽입하려면 배열 배열을 전달합니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 삽입 중 오류가 발생해도 무시하며, 보통 중복 레코드 오류를 무시합니다. DB 엔진에 따라 다른 오류도 무시될 수 있음을 유념하세요. 예를 들어 MySQL 엄격 모드를 무시합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing`은 서브쿼리 결과를 삽입할 때 사용합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가하는 ID가 있으면 `insertGetId` 메서드로 삽입과 동시에 ID를 얻을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서 `insertGetId`는 기본 키 컬럼명이 `id`여야 합니다. 다른 시퀀스에서 ID를 얻으려면 두 번째 인자로 컬럼명을 지정하세요.

<a name="upserts"></a>
### 업서트 (Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 존재하는 레코드는 지정한 컬럼만 업데이트합니다. 첫 번째 인자는 삽입/수정할 값들 배열, 두 번째 인자는 레코드를 고유하게 식별할 컬럼 목록, 세 번째 인자는 업데이트할 컬럼 배열입니다:

```php
DB::table('flights')->upsert(
    [
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ],
    ['departure', 'destination'],
    ['price']
);
```

위 예시에서 같은 `departure`와 `destination` 값이 있으면 `price` 컬럼을 업데이트하고, 없으면 새로 삽입합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 두 번째 인자 컬럼에 대한 기본키나 유니크 인덱스가 있어야 합니다. MariaDB 및 MySQL 드라이버는 두 번째 인자를 무시하고 항상 테이블의 기본키 및 유니크 인덱스를 사용해 기존 레코드를 식별합니다.

<a name="update-statements"></a>
## 업데이트문 (Update Statements)

삽입 외에 기존 레코드 업데이트도 가능합니다. `update` 메서드는 컬럼과 값 쌍 배열을 받아 해당 컬럼을 업데이트합니다. 업데이트된 행 수를 반환하며, `where` 절로 조건 지정이 가능합니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 업데이트 또는 삽입

기존 레코드를 업데이트하거나 없으면 새로 삽입하려면 `updateOrInsert` 메서드를 사용합니다. 첫 번째 인자는 찾을 조건 배열, 두 번째 인자는 업데이트할 값 배열입니다.

조건에 맞는 레코드를 찾아 존재하면 업데이트하고, 없으면 두 배열을 합친 속성으로 새 레코드를 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

`updateOrInsert`에 클로저를 넘겨 조건 존재 여부에 따라 삽입/업데이트할 데이터를 동적으로 결정할 수도 있습니다:

```php
DB::table('users')->updateOrInsert(
    ['user_id' => $user_id],
    fn ($exists) => $exists ? [
        'name' => $data['name'],
        'email' => $data['email'],
    ] : [
        'name' => $data['name'],
        'email' => $data['email'],
        'marketable' => true,
    ],
);
```

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 컬럼을 업데이트할 땐 `->` 구문을 써서 JSON 내 키를 지정해야 합니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

특정 컬럼 값을 증가시키거나 감소시키는 메서드도 있습니다. 첫 번째 인자는 대상 컬럼이고, 두 번째 인자는 증감할 양입니다 (기본값 1):

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

증가 또는 감소 시 추가로 다른 컬럼들도 업데이트할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

복수 컬럼을 한 번에 증감시킬 수도 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## 삭제문 (Delete Statements)

쿼리 빌더의 `delete` 메서드를 사용해 레코드를 삭제할 수 있습니다. 삭제된 행 수를 반환합니다. 삭제 조건은 `where`로 제한할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 선택문에서 "비관적 잠금"을 걸 때 유용한 메서드를 제공합니다. 

`sharedLock` 메서드는 공유 잠금을 실행하여, 트랜잭션이 완료될 때까지 선택한 행이 수정되지 못하도록 합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

`lockForUpdate` 메서드는 "for update" 잠금을 걸며, 선택된 레코드가 수정되거나 다른 공유 잠금으로 선택되지 못하도록 막습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금을 사용할 때는 [트랜잭션](/docs/12.x/database#database-transactions) 내에서 감싸는 것이 권장됩니다. 이렇게 하면 트랜잭션이 끝날 때까지 데이터 변경을 막고, 실패 시 자동 롤백과 잠금 해제를 보장합니다:

```php
DB::transaction(function () {
    $sender = DB::table('users')
        ->lockForUpdate()
        ->find(1);

    $receiver = DB::table('users')
        ->lockForUpdate()
        ->find(2);

    if ($sender->balance < 100) {
        throw new RuntimeException('Balance too low.');
    }

    DB::table('users')
        ->where('id', $sender->id)
        ->update([
            'balance' => $sender->balance - 100
        ]);

    DB::table('users')
        ->where('id', $receiver->id)
        ->update([
            'balance' => $receiver->balance + 100
        ]);
});
```

<a name="reusable-query-components"></a>
## 재사용 가능한 쿼리 컴포넌트

애플리케이션에서 반복되는 쿼리 로직은 쿼리 빌더의 `tap`과 `pipe` 메서드로 재사용 가능한 객체로 추출할 수 있습니다.

예를 들어, 다음과 같이 목적지 필터링 조건을 가진 두 쿼리가 있다고 가정합시다:

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->orderByDesc('price')
    ->get();

// ...

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

위 목적지 필터링을 별도의 재사용 가능한 객체로 분리할 수 있습니다:

```php
<?php

namespace App\Scopes;

use Illuminate\Database\Query\Builder;

class DestinationFilter
{
    public function __construct(
        private ?string $destination,
    ) {
        //
    }

    public function __invoke(Builder $query): void
    {
        $query->when($this->destination, function (Builder $query) {
            $query->where('destination', $this->destination);
        });
    }
}
```

이제 쿼리 빌더의 `tap` 메서드를 사용해 해당 객체를 쿼리에 적용할 수 있습니다:

```php
use App\Scopes\DestinationFilter;
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->orderByDesc('price')
    ->get();

// ...

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

<a name="query-pipes"></a>
#### 쿼리 파이프 (Query Pipes)

`tap` 메서드는 항상 쿼리 빌더를 반환합니다. 그러나 쿼리를 실행해 다른 값을 반환하는 재사용 객체가 필요하면 `pipe` 메서드를 사용합니다.

예를 들어, 다음 `Paginate` 객체는 페이지네이션 로직을 공유합니다. `DestinationFilter`처럼 쿼리 조건을 적용하는 대신, 쿼리를 실행해 페이지네이터를 반환합니다:

```php
<?php

namespace App\Scopes;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Query\Builder;

class Paginate
{
    public function __construct(
        private string $sortBy = 'timestamp',
        private string $sortDirection = 'desc',
        private int $perPage = 25,
    ) {
        //
    }

    public function __invoke(Builder $query): LengthAwarePaginator
    {
        return $query->orderBy($this->sortBy, $this->sortDirection)
            ->paginate($this->perPage, pageName: 'p');
    }
}
```

쿼리 빌더의 `pipe` 메서드를 사용해 이 객체를 적용할 수 있습니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

빌드 중인 쿼리의 SQL 문과 바인딩을 출력하려면 `dd`와 `dump` 메서드를 사용하세요. `dd`는 출력 후 요청 실행을 멈추고, `dump`는 요청을 계속 실행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드는 쿼리의 SQL을 매개변수 바인딩이 대체된 채로 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
