# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과값을 청크로 나누기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [SELECT 문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Join)](#joins)
- [유니언(Union)](#unions)
- [기본 WHERE 절](#basic-where-clauses)
    - [WHERE 절](#where-clauses)
    - [OR WHERE 절](#or-where-clauses)
    - [WHERE NOT 절](#where-not-clauses)
    - [WHERE ANY / ALL / NONE 절](#where-any-all-none-clauses)
    - [JSON WHERE 절](#json-where-clauses)
    - [추가 WHERE 절](#additional-where-clauses)
    - [논리적 그룹핑](#logical-grouping)
- [고급 WHERE 절](#advanced-where-clauses)
    - [WHERE EXISTS 절](#where-exists-clauses)
    - [하위 쿼리 WHERE 절](#subquery-where-clauses)
    - [전체 텍스트 WHERE 절](#full-text-where-clauses)
- [정렬, 그룹핑, Limit, Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹핑](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [INSERT 문](#insert-statements)
    - [Upsert](#upserts)
- [UPDATE 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [DELETE 문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 쉽고 직관적으로 생성하고 실행할 수 있도록 편리한 fluent 인터페이스를 제공합니다. 이 쿼리 빌더를 사용하면 애플리케이션 내에서 거의 모든 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 호환됩니다.

라라벨 쿼리 빌더는 SQL 인젝션 공격으로부터 애플리케이션을 보호하기 위해 PDO 파라미터 바인딩을 사용합니다. 따라서 쿼리 빌더에 전달하는 문자열을 별도로 정리(clean)하거나 이스케이프(escape)할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력값이 쿼리에서 참조하는 컬럼명(특히 "order by" 컬럼 등)으로 직접 사용되도록 해서는 절대 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

쿼리를 시작할 때는 `DB` 파사드에서 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 fluent 쿼리 빌더 인스턴스를 반환하며, 여기에 추가로 다양한 제약 조건을 체이닝하여 쿼리를 구성할 수 있습니다. 마지막으로 `get` 메서드를 사용해 쿼리 결과를 조회할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 모든 사용자를 나열합니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담고 있는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체로 표현됩니다. 각 컬럼의 값은 객체의 속성(property)으로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> 라라벨의 컬렉션(Collection) 객체는 데이터를 매핑하거나 집계 처리할 때 매우 강력한 다양한 메서드를 제공합니다. 라라벨 컬렉션에 대해 더 자세히 알아보려면 [컬렉션 문서](/docs/12.x/collections)를 참고하시기 바랍니다.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회하기

데이터베이스 테이블에서 단일 행만 조회하고 싶다면, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 일치하는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키기를 원한다면, `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외가 잡히지 않은 경우, 라라벨은 자동으로 404 HTTP 응답을 클라이언트에 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 아니라 한 컬럼의 값만 필요하다면, `value` 메서드를 사용해 레코드에서 해당 컬럼의 값을 바로 추출할 수 있습니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면, `find` 메서드를 사용할 수 있습니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값의 목록 조회하기

특정 컬럼의 값들만 모아서 `Illuminate\Support\Collection` 인스턴스로 얻고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 예를 들어, 사용자의 직함(title)만을 컬렉션으로 뽑아올 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인자로 원하는 컬럼명을 지정하면, 결과 컬렉션의 키를 해당 컬럼의 값으로 사용할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과값을 청크로 나누기

수천 건 이상의 데이터베이스 레코드를 처리해야 하는 경우, `DB` 파사드가 제공하는 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 한 번에 작은 청크 단위(조각)로 데이터를 조회한 뒤, 각 청크를 클로저(콜백)로 전달하여 처리합니다. 예를 들어, 아래처럼 `users` 테이블 전체를 100건씩 청크로 나눠 처리할 수 있습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 추가적인 청크 처리가 중단됩니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크로 결과를 나누는 도중에 레코드를 업데이트한다면, 처리 도중 예상치 못한 방식으로 청크 결과가 달라질 수 있습니다. 청크로 나눠서 조회하는 도중에 레코드를 업데이트해야 한다면, 반드시 `chunkById` 메서드를 사용하는 것이 좋습니다. 이 메서드는 자동으로 해당 레코드의 기본 키(primary key)를 기반으로 결과를 페이지네이션합니다.

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

`chunkById` 및 `lazyById` 메서드는 실행되는 쿼리에 자체적으로 "where" 조건을 추가하기 때문에, 직접 지정하는 조건들은 주로 [논리적으로 그룹핑](#logical-grouping)하여 클로저 안에서 처리하는 것이 좋습니다.

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
> 청크 콜백 내에서 레코드를 업데이트하거나 삭제할 때, 기본 키 또는 외래 키가 변경되면 청크 쿼리에 영향을 미칠 수 있습니다. 이로 인해 일부 레코드가 청크 처리 결과에서 누락될 수 있으니 주의해야 합니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행합니다. 하지만 각 청크를 콜백으로 전달하는 대신, `lazy()` 메서드는 [LazyCollection](/docs/12.x/collections#lazy-collections) 객체를 반환하여 전체 결과를 하나의 스트림처럼 순차적으로 다룰 수 있도록 해줍니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 조회한 레코드를 순회하면서 업데이트할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드들은 레코드의 기본 키(primary key)를 기준으로 결과를 자동으로 페이지네이션합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 결과를 순회하며 레코드를 업데이트하거나 삭제하는 경우, 기본 키나 외래 키의 변경이 쿼리 청크에 영향을 줄 수 있습니다. 그 결과 일부 레코드가 결과 집합에서 누락될 수 있으므로 주의해야 합니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`과 같은 다양한 집계 관련 메서드도 제공합니다. 쿼리를 구성한 뒤 아래와 같이 집계 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

당연히, 집계 값을 더 정교하게 계산하고 싶다면 다른 절들과 함께 조합해서 사용할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 판별하기

쿼리 조건에 일치하는 레코드가 존재하는지 알아볼 때 굳이 `count` 메서드를 쓸 필요 없이, `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## SELECT 문

<a name="specifying-a-select-clause"></a>
#### SELECT 절 지정하기

항상 테이블의 모든 컬럼을 조회할 필요는 없습니다. `select` 메서드를 사용해 쿼리의 SELECT 절을 원하는 컬럼만 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 쿼리 결과에서 중복된 값을 제거하고 고유한 행만 반환할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 기존 SELECT 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

가끔 쿼리 내에 임의의 문자열을 삽입해야 할 때가 있습니다. 이럴 때는 `DB` 파사드의 `raw` 메서드를 사용하여 raw 문자열 표현식을 만들 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 문장은 쿼리 내에 문자열로 직접 삽입되기 때문에, 반드시 SQL 인젝션 취약점이 발생하지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 메서드 대신, 쿼리의 여러 부분에 raw 표현식을 삽입할 수 있는 아래 메서드들도 사용할 수 있습니다. **참고로, raw 표현식을 활용하는 어떤 쿼리라도 SQL 인젝션으로부터 100% 안전함을 라라벨이 보장하지 않으니 주의하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 이 메서드는 두 번째 인수로 바인딩 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 쿼리 내에 raw한 "where" 절을 삽입할 때 사용할 수 있습니다. 이 메서드들은 두 번째 인자로 바인딩 배열을 선택적으로 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 및 `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 사용할 때 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 옵션으로 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 raw 문자열을 사용할 때 쓸 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 사용할 수 있도록 해줍니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Join)

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더에서도 조인(Join) 절을 쿼리에 추가할 수 있습니다. 기본적인 "inner join"을 수행하려면, 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하면 됩니다. 첫 번째 인수는 조인할 테이블명을 지정하고, 나머지 인수로 조인 조건 컬럼을 전달합니다. 여러 테이블을 한 쿼리에서 조인하는 것도 가능합니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### Left Join / Right Join 절

"inner join" 대신 "left join"이나 "right join"을 사용하려면, `leftJoin` 또는 `rightJoin` 메서드를 사용할 수 있습니다. 이 메서드들의 시그니처는 `join` 메서드와 동일합니다.

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### Cross Join 절

"cross join"을 수행하려면 `crossJoin` 메서드를 사용할 수 있습니다. Cross join은 첫 번째 테이블과 조인 테이블 간의 카테시안 곱(Cartesian product)을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 조인 조건을 지정하고 싶을 때는, `join` 메서드의 두 번째 인수에 클로저를 전달하면 됩니다. 클로저에서는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아와 "join" 절의 세부 조건을 구성할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 절이 필요하다면, JoinClause 인스턴스에서 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 이 경우, 두 컬럼끼리 비교하는 것이 아니라 컬럼 값과 직접 값을 비교합니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 하위 쿼리 Join

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면, 쿼리에 하위 쿼리를 조인할 수 있습니다. 각 메서드는 세 개의 인수―서브쿼리, 별칭, 연관 컬럼을 정의하는 클로저―를 받습니다. 예를 들어, 아래 예시는 각 사용자(user) 레코드에, 해당 사용자가 가장 최근 발행한 블로그 글의 `created_at` 타임스탬프 정보를 포함하는 컬렉션을 조회합니다.

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
#### Lateral Join

> [!WARNING]
> Lateral join은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서만 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하면 하위 쿼리와 함께 "lateral join"을 수행할 수 있습니다. 이 메서드들은 하위 쿼리와 별칭을 인수로 받으며, 조인 조건은 하위 쿼리 내에서 `where` 절로 작성해야 합니다. Lateral join은 각 행에 대해 개별적으로 평가되며, 쿼리 외부의 컬럼을 하위 쿼리에서 참조할 수 있습니다.

아래 예시는 각 사용자와 그 사용자가 작성한 가장 최근 블로그 글 최대 3개씩을 포함해서 컬렉션을 조회합니다. 각 사용자는 최대 3건의 가장 최신 블로그 글과 함께 결과에 등장할 수 있습니다. 조인 조건은 하위 쿼리 내에서 `whereColumn`으로 현재 user 행을 참조합니다.

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
## 유니언(Union)

쿼리 빌더는 두 개 이상의 쿼리를 "union" 연산으로 손쉽게 합칠 수 있도록 별도의 메서드를 제공합니다. 예를 들어, 첫 번째 쿼리를 만든 뒤, `union` 메서드를 사용해 여러 쿼리와 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도 `unionAll` 메서드가 제공됩니다. `unionAll`로 합쳐진 쿼리는 중복 결과가 제거되지 않습니다. 두 메서드는 시그니처가 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 WHERE 절

<a name="where-clauses"></a>
### WHERE 절

쿼리 빌더의 `where` 메서드를 사용해 쿼리에 다양한 "where" 조건을 추가할 수 있습니다. 가장 기본적 형태의 `where` 메서드는 세 개의 인수를 받습니다. 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 모든 연산자 사용 가능), 세 번째는 값을 뜻합니다.

예를 들어, `votes` 컬럼값이 `100`이고, `age` 컬럼값이 `35`보다 큰 사용자를 조회하는 쿼리는 아래와 같습니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의상, 어느 컬럼이 특정 값과 `=`(같음) 인지만 확인한다면, `where` 메서드에서 값을 두 번째 인수로 바로 넘길 수 있습니다. 라라벨은 자동으로 `=` 연산자를 사용해줍니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

복수의 컬럼에 한 번에 조건을 걸고 싶다면, `where` 메서드에 연관 배열(associative array)을 전달할 수 있습니다.

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

앞서 언급했듯이, 데이터베이스에서 지원하는 모든 연산자를 사용할 수 있습니다.

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

조건을 배열로 전달할 수도 있습니다. 이 경우, 각 배열 원소는 일반적으로 `where` 메서드에 전달하는 세 개의 인자를 포함한 배열이어야 합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력값이 쿼리에서 참조하는 컬럼명(특히 "order by" 컬럼 등)으로 직접 사용되도록 해서는 안 됩니다.

> [!WARNING]
> MySQL 및 MariaDB에서는 문자열과 숫자를 비교하면 자동으로 문자열이 정수로 형변환됩니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되므로, 의도하지 않은 결과가 나올 수 있습니다. 예를 들어, 테이블의 `secret` 컬럼이 `aaa`인 경우 `User::where('secret', 0)`을 실행하면 해당 행이 반환됩니다. 이 문제를 방지하려면 값을 쿼리에 사용하기 전에 반드시 올바른 타입으로 형변환해야 합니다.

<a name="or-where-clauses"></a>

### Or Where 절

쿼리 빌더의 `where` 메서드를 연속으로 호출하면 각 "where" 절은 `and` 연산자로 결합됩니다. 하지만, `orWhere` 메서드를 사용하면 `or` 연산자로 쿼리에 절을 추가할 수 있습니다. `orWhere` 메서드는 `where` 메서드와 동일한 인수를 허용합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

"or" 조건을 괄호로 묶어서 그룹화해야 할 경우, `orWhere` 메서드의 첫 번째 인수로 클로저를 전달하면 됩니다.

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

위 예제는 아래와 같은 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 방지하기 위해 항상 `orWhere` 호출은 그룹화해서 사용하는 것이 좋습니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 특정 쿼리 제약 조건 그룹을 부정(negate)할 때 사용할 수 있습니다. 예를 들어, 아래 쿼리는 "세일 상품이거나 가격이 10보다 작은 상품"을 제외합니다.

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

여러 컬럼에 동일한 쿼리 제약 조건을 적용해야 할 때가 있습니다. 예를 들어, 특정 값이 주어진 컬럼 목록 중 하나라도 `LIKE` 조건을 만족하는 모든 레코드를 조회하고 싶을 수 있습니다. 이럴 때 `whereAny` 메서드를 사용할 수 있습니다.

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

위 쿼리는 아래와 같은 SQL을 생성합니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

비슷하게, `whereAll` 메서드는 주어진 컬럼 모두가 제약 조건에 일치하는 레코드를 조회합니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 아래와 같이 작성됩니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 주어진 컬럼 중 어디에도 해당 조건에 일치하지 않는 레코드를 조회합니다.

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

위 쿼리는 다음과 같은 SQL을 만듭니다.

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

라라벨은 JSON 타입 컬럼을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에서 JSON 컬럼 쿼리를 지원합니다. JSON 컬럼을 쿼리할 때는 `->` 연산자를 사용합니다.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열을 쿼리하려면 `whereJsonContains`, `whereJsonDoesntContain` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL를 사용하는 경우, `whereJsonContains` 및 `whereJsonDoesntContain`에 값의 배열을 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한, JSON 키의 존재 여부를 확인하려면 `whereJsonContainsKey`, `whereJsonDoesntContainKey` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, `whereJsonLength` 메서드를 사용해 JSON 배열의 길이로 쿼리할 수 있습니다.

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

`whereLike` 메서드를 사용하면 패턴 매칭을 위한 "LIKE" 절을 쿼리에 추가할 수 있습니다. 이 메서드는 데이터베이스 제품에 상관없이 문자열 패턴 매칭 쿼리를 수행할 수 있으며, 대소문자 구분도 설정할 수 있습니다. 기본적으로 이 매칭은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인자를 사용하여 대소문자를 구분하는 검색도 가능합니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 "or" 조건과 함께 LIKE 절을 추가할 때 사용합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드는 "NOT LIKE" 절을 쿼리에 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`를 사용하면 "or" 조건과 함께 NOT LIKE 조건을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색 옵션은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 특정 컬럼의 값이 지정한 배열에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 컬럼의 값이 지정한 배열에 포함되어 있지 않은지를 검사합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

또한, `whereIn` 메서드의 두 번째 인수로 쿼리 객체를 전달할 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예제는 다음과 같은 SQL을 생성합니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 많은 개수의 정수 데이터를 전달해야 할 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼의 값이 두 값의 범위 내에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼의 값이 두 값의 범위를 벗어난 경우를 체크합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 한 컬럼의 값이 같은 레코드 내의 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 한 컬럼의 값이 같은 레코드 내의 두 컬럼 값 사이에 있지 않은지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 특정 컬럼의 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull` 메서드는 컬럼이 `NULL`이 아닌지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 컬럼의 값을 특정 날짜와 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth` 메서드는 특정 월과 비교하고자 할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 한 달 중 특정 일과 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 특정 연도와 값을 비교합니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 시간을 기준으로 값을 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`, `whereFuture` 메서드는 컬럼의 값이 과거 또는 미래에 해당하는지 여부를 판별할 때 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture` 메서드는 오늘 또는 과거/미래까지 포함해서 비교할 때 사용합니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 각각 오늘, 오늘 이전, 오늘 이후에 해당하는 값을 판별할 때 사용합니다.

```php
$invoices = DB::table('invoices')
    ->whereToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereBeforeToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereAfterToday('due_at')
    ->get();
```

또한, `whereTodayOrBefore`, `whereTodayOrAfter` 메서드를 사용하면 오늘을 포함하여 그 이전 또는 이후 값까지 비교할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼의 값이 동일한지 확인할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

또한, 비교 연산자를 `whereColumn` 메서드에 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

컬럼 비교 배열을 전달하면, 각 조건은 `and` 연산자로 결합됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹핑

여러 "where" 절을 괄호로 그룹화해야 원하는 논리적 쿼리 구조를 만들 수 있습니다. 실제로, 예상치 못한 쿼리 동작을 방지하려면 `orWhere` 메서드 사용 시 항상 괄호로 그룹핑하는 것이 좋습니다. 이를 위해 `where` 메서드에 클로저를 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위와 같이, `where` 메서드에 클로저를 전달하면 쿼리 빌더는 제약 조건 그룹을 시작합니다. 클로저에는 쿼리 빌더 인스턴스가 전달되므로, 괄호로 묶어야 할 조건을 자유롭게 작성할 수 있습니다. 위 예제는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 방지하기 위해 항상 `orWhere` 호출은 그룹화해서 사용하는 것이 좋습니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" SQL 절을 작성할 수 있게 해줍니다. 이 메서드는 쿼리 빌더 인스턴스를 인수로 받는 클로저를 전달받으며, 이 안에서 "exists" 절에 포함될 서브쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는, 클로저 대신 쿼리 객체 자체를 `whereExists` 메서드에 제공할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위의 두 예제 모두 다음과 같은 SQL을 생성합니다.

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

서브쿼리의 실행 결과와 특정 값을 비교하는 "where" 절이 필요한 경우가 있습니다. 이럴 때는 `where` 메서드에 클로저와 값을 전달하면 됩니다. 예를 들어, 아래 쿼리는 주어진 타입의 최근 "membership"을 보유한 모든 사용자를 조회합니다.

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

또는 컬럼 값을 서브쿼리 결과와 비교해야 할 경우, 컬럼명, 연산자, 클로저를 순서대로 `where` 메서드에 전달할 수 있습니다. 아래 예시는 평균값보다 적은 금액을 가진 수입(income) 레코드를 조회합니다.

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문(Full Text) Where 절

> [!WARNING]
> 전문(Full Text) where 절은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText`, `orWhereFullText` 메서드를 사용하면 [전문 인덱스](/docs/12.x/migrations#available-index-types)가 정의된 컬럼에 대해 전문 검색 "where" 절을 추가할 수 있습니다. 이 메서드들은 라라벨이 데이터베이스 별로 적절한 SQL로 변환해줍니다. 예를 들어, MariaDB나 MySQL을 사용할 때는 `MATCH ... AGAINST` 구문이 사용됩니다.

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

`orderBy` 메서드는 쿼리 결과를 특정 컬럼을 기준으로 정렬할 수 있게 해줍니다. 첫 번째 인수로는 정렬할 컬럼명을, 두 번째 인수로는 정렬 방향을 지정합니다. 정렬 방향에는 `asc`(오름차순) 또는 `desc`(내림차순)를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

다수의 컬럼을 기준으로 정렬하려면 원하는 만큼 `orderBy`를 체이닝해서 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향(second argument)은 생략이 가능하며, 기본값은 오름차순입니다. 내림차순으로 정렬하려면 두 번째 매개변수에 `desc`를 명시하거나, `orderByDesc` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

마지막으로, `->` 연산자를 사용하면 JSON 컬럼 내의 값을 기준으로 정렬할 수 있습니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드를 사용하면 날짜 기준으로 손쉽게 결과를 정렬할 수 있습니다. 기본적으로 이 메서드는 테이블의 `created_at` 컬럼 기준으로 정렬합니다. 원하는 컬럼명을 직접 전달하여 정렬 컬럼을 변경할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 임의로 한 명의 사용자를 가져오고 싶을 때 아래와 같이 사용할 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 지우기

`reorder` 메서드는 앞서 쿼리에 적용된 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드에 컬럼명과 정렬 방향을 전달하면, 기존의 모든 정렬 조건을 제거하고 새로운 정렬 방식으로 쿼리를 수행합니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

더 편리하게, `reorderDesc` 메서드를 이용하면 내림차순 정렬로 쉽게 재정렬할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상했듯이, `groupBy`와 `having` 메서드를 사용하여 결과를 그룹화할 수 있습니다. `having` 메서드의 사용법은 `where` 메서드와 유사합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용하면 특정 범위 내의 결과만 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy` 메서드에 여러 컬럼을 인수로 전달해서, 여러 컬럼을 기준으로 그룹화할 수도 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 구문을 작성하려면 [havingRaw](#raw-methods) 메서드 문서를 참고하세요.

<a name="limit-and-offset"></a>
### LIMIT 및 OFFSET

`limit`과 `offset` 메서드를 사용해서 쿼리에서 반환할 결과의 개수를 제한하거나, 일부 결과를 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절(Conditional Clauses)

때에 따라 어떤 조건이 만족될 때만 쿼리에 특정 절을 적용하고 싶을 수 있습니다. 예를 들어, HTTP 요청에서 특정 입력값이 존재할 때만 `where` 구문을 추가하려면 `when` 메서드를 사용할 수 있습니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`로 평가될 때만 두 번째 인수(클로저)를 실행합니다. 만약 첫 번째 인수가 `false`라면 클로저는 실행되지 않습니다. 위 예시의 경우, 요청에 `role` 필드가 있을 때만 해당 클로저가 실행됩니다.

세 번째 인수로 또 다른 클로저를 전달하면, 첫 번째 인수가 `false`일 때만 이 클로저가 실행됩니다. 아래 예시는 기본 정렬 기준을 설정하는 방식입니다.

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
## INSERT 구문

쿼리 빌더는 데이터베이스 테이블에 레코드를 삽입할 수 있는 `insert` 메서드도 제공합니다. `insert` 메서드는 컬럼명과 값을 담은 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

배열의 배열을 전달하여 여러 개의 레코드를 한 번에 삽입할 수 있습니다. 각 배열은 하나의 레코드를 의미합니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드 삽입 중 에러가 발생해도 이를 무시하고 계속 진행합니다. 이 메서드를 사용할 때는 중복 레코드 에러 등이 무시되며, 데이터베이스 엔진에 따라 다른 에러도 무시될 수 있습니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict 모드를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리의 결과를 활용해서 테이블에 새 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id 컬럼이 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입한 후, 해당 id 값을 바로 얻을 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 때는 `insertGetId` 메서드가 자동 증가 컬럼의 이름이 반드시 `id`여야 합니다. 만약 다른 "시퀀스"에서 ID를 조회하려면, 두 번째 인자로 컬럼명을 전달해야 합니다.

<a name="upserts"></a>
### UPSERT

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 값으로 업데이트합니다. 첫 번째 인수는 삽입/업데이트할 값들의 배열이고, 두 번째 인수는 레코드를 고유하게 식별하는 컬럼(들)입니다. 세 번째 인수는 레코드가 이미 존재할 때(즉, 일치하는 레코드가 있을 때) 어떤 컬럼을 업데이트할 것인지 지정하는 배열입니다.

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

위 예시에서 라라벨은 두 개의 레코드를 삽입하려고 시도합니다. 만약 동일한 `departure`와 `destination` 값을 가진 레코드가 이미 존재한다면, 해당 레코드의 `price` 컬럼이 갱신됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인수에 명시된 컬럼에 "primary" 또는 "unique" 인덱스가 필요합니다. 추가로, MariaDB와 MySQL 데이터베이스 드라이버는 `upsert`의 두 번째 인수를 무시하고, 항상 테이블의 "primary" 및 "unique" 인덱스를 이용해 기존 레코드를 판단합니다.

<a name="update-statements"></a>
## UPDATE 구문

쿼리 빌더는 레코드 삽입뿐만 아니라, 기존의 레코드를 수정(update)하는 기능도 제공합니다. `update` 메서드는 변경하고자 하는 컬럼명과 값의 페어 배열을 인수로 받으며, 영향을 받은 레코드 개수를 반환합니다. 또한, `where` 절을 활용해 업데이트 대상을 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### UPDATE 또는 INSERT

때로는 데이터베이스에 이미 존재하는 레코드는 업데이트하고, 없으면 새로 생성(insert)하고 싶을 수 있습니다. 이런 상황에서는 `updateOrInsert` 메서드를 사용할 수 있습니다. 이 메서드는 두 개의 인수를 받습니다. 첫 번째는 레코드를 찾기 위한 조건의 배열, 두 번째는 업데이트할 컬럼명과 값의 배열입니다.

`updateOrInsert` 메서드는 먼저 첫 번째 인수로 주어진 컬럼과 값으로 레코드를 찾으려고 시도합니다. 일치하는 레코드가 있으면 두 번째 인수의 값으로 업데이트되고, 없다면 두 인수를 합친 값으로 새 레코드가 생성됩니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

또한, 상황에 따라 업데이트/삽입되는 값을 동적으로 지정하려면 클로저를 전달할 수도 있습니다.

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

JSON 컬럼의 값을 수정할 때는 `->` 문법을 사용하여 JSON 객체 내부에서 업데이트할 키를 지정할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+ 버전에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가(Increment) 및 감소(Decrement)

쿼리 빌더에서는 특정 컬럼의 값을 간단하게 증가시키거나 감소시키는 메서드도 제공합니다. 두 메서드 모두 최소 한 개의 인수(수정할 컬럼명)를 받으며, 두 번째 인수로 증감할 수치도 지정할 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 증가/감소와 동시에 추가 컬럼도 함께 업데이트할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, 여러 컬럼을 한 번에 증감하고 싶다면 `incrementEach`와 `decrementEach` 메서드를 사용할 수 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## DELETE 구문

쿼리 빌더의 `delete` 메서드를 사용하면 테이블에서 레코드를 삭제할 수 있습니다. `delete` 메서드는 영향을 받은 레코드의 개수를 반환합니다. `delete` 호출 전에 "where" 절을 추가하면 삭제 대상을 제한할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더는 `select` 쿼리 실행 시 "비관적 잠금"을 위한 몇 가지 메서드를 제공합니다. "공유 잠금"(shared lock)을 적용하려면 `sharedLock` 메서드를 사용하세요. 공유 잠금은 선택한 행이 트랜잭션이 완료될 때까지 수정되지 않도록 막아줍니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 `lockForUpdate` 메서드를 사용할 수도 있습니다. "For update" 잠금은 해당 레코드가 수정되거나, 다른 공유 잠금 쿼리에서 선택되는 것을 모두 막습니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

반드시 필요한 것은 아니지만, 비관적 잠금 쿼리는 [트랜잭션](/docs/12.x/database#database-transactions) 내부에서 사용하는 것이 좋습니다. 이렇게 하면 전체 작업이 끝날 때까지 데이터가 변경되지 않는 상태로 유지됩니다. 만약 트랜잭션 도중 실패한다면, 트랜잭션은 모든 변경 사항을 롤백하고, 잠금 또한 자동으로 해제됩니다.

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

애플리케이션 전체에서 반복적으로 사용되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 활용해 이 로직을 재사용 가능한 객체로 추출할 수 있습니다. 예를 들어, 아래와 같은 쿼리 두 개가 있다고 가정하겠습니다.

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

두 쿼리 모두에 공통적으로 들어가는 목적지 필터링 로직을 하나의 객체로 추출할 수 있습니다.

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

이제 쿼리 빌더의 `tap` 메서드를 이용해 해당 객체의 로직을 쿼리에 적용할 수 있습니다.

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
#### 쿼리 파이프(Query Pipes)

`tap` 메서드는 항상 쿼리 빌더 인스턴스를 반환합니다. 만약 쿼리를 실행하고 다른 값을 반환하는 객체를 추출하고 싶다면, `pipe` 메서드를 사용할 수 있습니다.

아래는 애플리케이션 전반에서 공통적으로 사용하는 [페이지네이션](/docs/12.x/pagination) 로직을 담은 쿼리 객체 예시입니다. `DestinationFilter`가 쿼리에 조건만 적용하는 것과 다르게, `Paginate` 객체는 쿼리를 실행해서 paginator 인스턴스를 반환합니다.

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
        private string $perPage = 25,
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

쿼리 빌더의 `pipe` 메서드를 사용해, 이 객체를 통해 공통 페이지네이션 로직을 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리 작성 중에 `dd`와 `dump` 메서드를 사용해 쿼리의 바인딩 값과 SQL을 출력할 수 있습니다. `dd` 메서드는 디버그 정보를 출력한 뒤 요청 처리를 중단하며, 반면 `dump` 메서드는 디버그 정보를 보여주고도 요청을 계속 이어갑니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드를 쿼리에 사용하면, 파라미터 바인딩까지 모두 치환된 SQL 쿼리를 출력할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```