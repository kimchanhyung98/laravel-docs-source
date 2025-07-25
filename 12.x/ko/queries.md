# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계 (Aggregate)](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Join)](#joins)
- [유니온(Union)](#unions)
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
    - [전체 텍스트 Where 절](#full-text-where-clauses)
- [정렬, 그룹화, Limit, Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [Upsert](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

라라벨의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행할 수 있는 편리하고 유연한 인터페이스를 제공합니다. 이 쿼리 빌더를 활용하면 애플리케이션에서 대부분의 데이터베이스 작업을 손쉽게 수행할 수 있으며, 라라벨이 지원하는 모든 데이터베이스 시스템과 완벽하게 연동됩니다.

라라벨 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호합니다. 쿼리 빌더에 전달되는 문자열은 별도의 정제나 필터링 작업 없이도 안전하게 사용할 수 있습니다.

> [!WARNING]
> PDO는 컬럼명을 바인딩하는 기능을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에서 참조하는 컬럼명(특히 `order by` 컬럼 등)에 직접 반영되지 않도록 반드시 주의해야 합니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 가져오기

쿼리를 시작할 때는 `DB` 파사드의 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 유연한 쿼리 빌더 인스턴스를 반환하므로, 쿼리에 제약 조건을 체이닝하여 추가하고 마지막에 `get` 메서드로 결과를 가져올 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담고 있는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체로 표현됩니다. 각 컬럼의 값은 객체의 속성(property)처럼 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> 라라벨의 컬렉션(collecton)은 데이터 매핑, 필터링, 집계 등 다양한 강력한 기능을 제공합니다. 컬렉션에 대한 더 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하시기 바랍니다.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 또는 컬럼 가져오기

데이터베이스 테이블에서 단일 행만 조회하고 싶다면, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

매칭되는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키며, 이를 이용해 반드시 행을 가져와야 할 때는 `firstOrFail` 메서드를 사용할 수 있습니다. 만약 이 예외가 처리되지 않으면, 404 HTTP 응답이 클라이언트에 자동으로 반환됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 아니라 하나의 값만 필요하다면, `value` 메서드를 사용해 해당 컬럼의 값만 바로 추출할 수 있습니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 가져오고 싶을 때는 `find` 메서드를 사용하면 됩니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값의 목록 가져오기

단일 컬럼의 값만을 담은 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 예를 들어, 사용자들의 타이틀(titles)만 컬렉션으로 가져올 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인수로 키가 될 컬럼을 지정하면, 해당 컬럼을 키로 하는 컬렉션을 생성할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기

수천 개 이상의 대용량 레코드를 다루어야 할 경우, `DB` 파사드가 제공하는 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 한 번에 적은 양의 결과만 가져와 각 청크를 클로저로 전달하며, 각 청크에 대한 처리를 완료할 때마다 다음 청크를 가져옵니다. 예를 들어, `users` 테이블의 모든 레코드를 한 번에 100개씩 처리하려면 아래와 같이 작성합니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면, 그 이후의 청크 처리는 중단할 수 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중에 레코드의 업데이트 작업을 할 경우, 청크 결과가 예기치 않게 달라질 수 있습니다. 만약 청크 처리 중 레코드를 갱신할 계획이라면, 반드시 `chunkById` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 레코드의 기본키(primary key)를 기준으로 자동으로 페이지네이션을 처리합니다.

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

`chunkById` 및 `lazyById` 메서드는 쿼리에 자체적으로 "where" 조건을 추가하므로, 본인이 추가하는 조건은 [논리적 그룹화](#logical-grouping)를 하여 클로저 내부에서 처리하는 것이 좋습니다.

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
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제할 때, 기본키나 외래키 값이 변경될 경우 쿼리의 범위가 달라져 청크 결과에 일부 레코드가 제외될 수 있습니다. 이런 점을 반드시 주의해야 합니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백으로 전달하는 대신, 전체 결과를 하나의 [LazyCollection](/docs/12.x/collections#lazy-collections) 스트림처럼 다룰 수 있게 반환합니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 결과 레코드들을 순회하며 업데이트해야 할 경우에는 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 레코드의 기본키를 활용해 자동으로 페이지네이션을 처리합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 레코드를 순회하며 업데이트하거나 삭제할 때, 기본키나 외래키 값이 변경되면 쿼리 범위가 바뀌어 일부 레코드가 누락될 수 있으니 반드시 유의하시기 바랍니다.

<a name="aggregates"></a>
### 집계 (Aggregate)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 메서드를 제공합니다. 쿼리를 구성한 후에 이 메서드를 호출하여 집계 결과를 바로 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 다른 조건절들과 결합하여 원하는 방식으로 집계 값을 산출할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

특정 조건에 맞는 레코드가 존재하는지 단순히 확인할 경우, `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다.

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## Select 구문

<a name="specifying-a-select-clause"></a>
#### Select 절 지정

데이터베이스 테이블의 모든 컬럼을 조회하지 않고, 원하는 컬럼만 직접 지정하고 싶을 때는 `select` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복을 제거한 결과만 반환하도록 쿼리를 강제할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스를 생성하고, 기존 select 절에 컬럼을 추가하려면 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

때로는 쿼리 내에 임의의 문자열(즉, SQL 표현식 등)을 삽입해야 할 경우가 있습니다. 이럴 때는 `DB` 파사드가 제공하는 `raw` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 문자열 그대로 쿼리에 삽입됩니다. 이로 인해 SQL 인젝션 취약점이 발생할 수 있으니, 반드시 주의해서 사용해야 합니다.

<a name="raw-methods"></a>
### Raw 관련 메서드

`DB::raw` 메서드 외에도 쿼리 빌더의 여러 부분에 raw 표현식을 삽입할 수 있는 다양한 전용 메서드가 제공됩니다.  
**중요:** Raw 표현식을 사용하는 쿼리는 라라벨이 SQL 인젝션을 방지해준다고 보장할 수 없습니다.

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))`와 동일하게 동작합니다. 이 메서드는 두 번째 인수로 바인딩 배열을 선택적으로 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 쿼리에 raw "where" 절을 추가할 때 사용할 수 있습니다. 이 메서드들도 두 번째 인수로 바인딩 배열을 선택적으로 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 및 `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 지정할 수 있도록 합니다. 이 메서드들도 두 번째 인수로 바인딩 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 raw 문자열을 지정할 때 사용할 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 지정할 때 사용할 수 있습니다.

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

쿼리 빌더를 사용하면 쿼리에 조인(join) 구문을 추가할 수도 있습니다. 기본적인 "inner join"을 하려면, 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하면 됩니다. 이때 첫 번째 인수는 조인할 테이블명, 나머지 인수는 조인의 컬럼 제약조건을 지정합니다. 한 번에 여러 테이블을 조인할 수도 있습니다.

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

"inner join" 대신 "left join" 또는 "right join"을 하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하면 됩니다. 이 메서드들의 사용법은 `join` 메서드와 동일합니다.

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

"cross join"을 실행하려면 `crossJoin` 메서드를 사용할 수 있습니다. 크로스 조인은 첫 번째 테이블과 조인될 테이블 사이의 데카르트 곱(Cartesian product)을 만듭니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 join 절을 작성해야 할 때는, `join` 메서드의 두 번째 인수에 클로저를 전달할 수 있습니다. 이 클로저에는 `Illuminate\Database\Query\JoinClause` 인스턴스가 전달되며, 이를 사용해 "join" 절에 다양한 조건을 지정할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에 "where" 절을 사용하고자 한다면, `JoinClause` 인스턴스의 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 이 메서드들은 두 컬럼을 비교하는 것이 아니라, 컬럼과 값을 비교합니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 Join

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 서브쿼리와도 조인을 수행할 수 있습니다. 이 메서드들은 세 개의 인수를 받으며, 각각 서브쿼리, 별칭(테이블 이름), 컬럼 관계를 정의하는 클로저입니다. 다음 예제는 각 사용자 레코드에 대해, 해당 사용자가 가장 최근 발행한 블로그 포스트의 `created_at` 타임스탬프도 함께 가져오는 방법을 보여줍니다.

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
> Lateral 조인은 현재 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하면 서브쿼리와 함께 "lateral join"을 적용할 수 있습니다. 이 메서드는 각각 서브쿼리와 별칭(테이블 이름) 두 개의 인수를 받습니다. 조인 조건은 전달하는 서브쿼리의 `where` 절 안에서 지정하면 됩니다. lateral 조인은 각 행(row)마다 실행되며, 서브쿼리 밖(즉, 외부 쿼리)의 컬럼도 참조할 수 있습니다.

다음 예제는 사용자 컬렉션과 각 사용자의 가장 최근 블로그 게시글 3개를 함께 가져오는 방법을 보여줍니다. 각 사용자는 최대 3개의 최신 글 정보를 포함하는 여러 행(row)으로 반환될 수 있습니다. 조인 조건은 서브쿼리에서 `whereColumn`을 활용해 현재 사용자 행의 값을 참조합니다.

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
## 유니온(Union)

쿼리 빌더는 두 개 이상의 쿼리를 "union"으로 결합하는 편리한 방법도 제공합니다. 예를 들어, 먼저 하나의 쿼리를 정의한 후, `union` 메서드로 더 많은 쿼리와 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 외에도 `unionAll` 메서드가 제공되며, 이 메서드로 결합된 쿼리는 중복된 결과를 제거하지 않습니다. `unionAll`의 메서드 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용하면 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 형태는 세 개의 인수를 받는데, 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 비교할 값입니다.

아래 예제는 `votes` 컬럼이 `100`이고, `age` 컬럼이 `35`보다 큰 사용자를 조회하는 방법입니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

좀 더 편리하게 `=` 연산 조건만 지정할 경우, 두 번째 인수에 값만 전달하면 됩니다. 라라벨은 이 경우 자동으로 `=` 연산자를 적용합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

연관 배열을 `where` 메서드에 전달하면, 여러 컬럼 조건을 한 번에 지정할 수도 있습니다.

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

위에서 설명했듯이, 데이터베이스에서 지원하는 모든 연산자를 사용할 수 있습니다.

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

조건 배열의 각 요소가 세 개의 인수를 가지는 배열(`컬럼, 연산자, 값`)이면, 한 번에 여러 조건을 추가하는 것도 가능합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명을 바인딩할 수 없습니다. 따라서 사용자 입력이 쿼리에 참조되는 컬럼명(특히 `order by` 컬럼 등)에 직접 반영되지 않도록 반드시 주의하세요.

> [!WARNING]
> MySQL과 MariaDB에서는 문자열-숫자 비교 시, 문자열을 자동으로 정수로 형변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되기 때문에, 예기치 않은 결과가 발생할 수 있습니다. 예를 들어, `secret` 컬럼의 값이 `aaa`이고, `User::where('secret', 0)`을 수행하면 해당 행이 반환됩니다. 이를 방지하기 위해 쿼리에 사용되는 값의 타입을 반드시 올바르게 변환한 후 전달해야 합니다.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드를 연속으로 호출하면, 각 "where" 절이 `and` 연산자로 연결됩니다. 그러나 `orWhere` 메서드를 사용하면, 해당 조건을 `or` 연산자로 연결할 수 있습니다. `orWhere`의 사용법과 인수는 `where`와 동일합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 "or" 조건을 그룹핑해야 할 때는, `orWhere`의 첫 번째 인수로 클로저를 넘기면 됩니다.

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

위 코드는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 전역 스코프가 적용될 때 예기치 않은 동작을 방지하려면, 항상 `orWhere` 호출은 그룹핑해서 사용하는 것이 좋습니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 지정한 쿼리 조건 그룹을 부정(NOT)할 때 사용할 수 있습니다. 아래 예제는 `clearance` 컬럼이 true이거나, `price`가 10 미만인 상품을 제외한 레코드만 가져옵니다.

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

여러 컬럼에 동일한 쿼리 조건을 적용해야 할 경우가 있습니다. 예를 들어, 컬럼 목록 중 하나라도 특정 값과 `LIKE` 조건을 만족하는 모든 레코드를 조회하려면, `whereAny` 메서드를 사용할 수 있습니다.

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

위 쿼리는 다음과 같은 SQL로 변환됩니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

비슷하게, `whereAll` 메서드를 사용하면 주어진 모든 컬럼이 같은 조건을 만족하는 레코드를 조회할 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음과 같은 SQL이 생성됩니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

또한, `whereNone` 메서드를 사용하면, 주어진 모든 컬럼이 특정 조건을 하나도 만족하지 않는 레코드를 조회할 수 있습니다.

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

위 쿼리는 다음과 같이 변환됩니다.

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

라라벨은 JSON 컬럼 타입을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에 대해 JSON 컬럼 쿼리도 지원합니다. JSON 컬럼을 쿼리할 땐 `->` 연산자를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열을 쿼리할 때는 `whereJsonContains` 및 `whereJsonDoesntContain` 메서드를 이용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL을 사용하는 경우, 값 배열을 `whereJsonContains` 및 `whereJsonDoesntContain` 메서드에 전달하는 것도 가능합니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한, 특정 JSON 키가 포함된 결과만 가져오거나, 포함되지 않은 결과만 가져오고 싶을 때는 `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이를 기준으로 쿼리하고 싶다면 `whereJsonLength` 메서드를 사용할 수 있습니다.

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

`whereLike` 메서드는 패턴 매칭을 위해 쿼리에 "LIKE" 절을 추가할 수 있게 해줍니다. 이 메서드들을 사용하면 데이터베이스에 종속적이지 않게 문자열 매칭 쿼리를 작성할 수 있으며, 대소문자 구분 여부도 설정할 수 있습니다. 기본적으로 문자열 매칭은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 사용하여 대소문자 구분 검색을 활성화할 수 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 LIKE 조건과 함께 "or" 절을 추가할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드는 쿼리에 "NOT LIKE" 절을 추가할 수 있게 해줍니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike`를 사용하면 NOT LIKE 조건을 가진 "or" 절을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색 옵션은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 지정한 컬럼의 값이 주어진 배열에 포함되어 있는지를 검증합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 해당 컬럼의 값이 주어진 배열에 포함되어 있지 않은지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 메서드의 두 번째 인수로 쿼리 객체를 전달할 수도 있습니다.

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
> 대용량의 정수 배열을 바인딩하여 쿼리에 추가해야 한다면, 메모리 사용량을 크게 줄이기 위해 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하는 것이 좋습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼 값이 두 값의 범위 밖에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 컬럼 값이 동일한 테이블의 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns` 메서드는 컬럼 값이 동일한 테이블의 두 컬럼 값 범위 밖에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween` 메서드는 지정한 값이 동일한 테이블 행의 두 컬럼 값 사이에 있는지 검증합니다.

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween` 메서드는 값이 동일한 테이블 행의 두 컬럼 값 범위 밖에 있는지 확인합니다.

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 지정한 컬럼의 값이 `NULL`인지 검증합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull` 메서드는 해당 컬럼의 값이 `NULL`이 아닌지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 컬럼의 값을 특정 날짜와 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth` 메서드는 컬럼의 값을 특정 월과 비교할 때 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay` 메서드는 컬럼의 값을 한 달 중 특정 날짜와 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear` 메서드는 컬럼의 값을 특정 연도와 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime` 메서드는 컬럼 값을 특정 시간과 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`, `whereFuture` 메서드는 컬럼의 값이 과거 또는 미래인지 확인하는 데 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture` 메서드는 현재 날짜 및 시간을 포함하여 컬럼 값이 과거 또는 미래인지 확인하는 데 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 컬럼의 값이 오늘, 오늘 이전, 또는 오늘 이후인지 각각 확인할 수 있습니다.

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

마찬가지로, `whereTodayOrBefore`, `whereTodayOrAfter` 메서드는 오늘 포함 이전 혹은 이후인지를 확인할 때 사용할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼이 같은지 검증하는 데 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 `whereColumn` 메서드에 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

컬럼 비교 배열을 `whereColumn` 메서드에 전달할 수도 있습니다. 이 조건들은 `and` 연산자로 결합됩니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

경우에 따라 쿼리 내에서 여러 "where" 절을 괄호로 묶어 논리적으로 그룹화해야 할 때가 있습니다. 실제로, `orWhere` 메서드 호출은 일반적으로 괄호로 그룹화하는 것이 예기치 않은 쿼리 동작을 피하는 데 좋습니다. 이를 위해서는 `where` 메서드에 클로저를 전달하면 됩니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위에서 볼 수 있듯이, `where` 메서드에 클로저를 전달하면 쿼리 빌더는 새로운 제약 조건 그룹을 괄호로 생성합니다. 이 클로저는 쿼리 빌더 인스턴스를 매개변수로 받아 괄호 내에 묶여야 할 제약 조건을 정의할 수 있습니다. 위 예제는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프가 적용될 때 예기치 않은 동작을 방지하기 위해 항상 `orWhere` 호출을 그룹화하는 것이 좋습니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 작성할 수 있습니다. `whereExists` 메서드는 클로저를 받아, 이 클로저가 쿼리 빌더 인스턴스를 전달받아 "exists" 절 안에 포함될 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는 클로저 대신 쿼리 객체를 직접 `whereExists` 메서드에 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예제 모두 다음과 같은 SQL을 생성합니다.

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

경우에 따라 서브쿼리의 결과를 주어진 값과 비교하는 "where" 절을 작성해야 할 수 있습니다. 이를 위해서는 클로저와 값을 `where` 메서드에 전달하면 됩니다. 예를 들어, 아래 쿼리는 주어진 타입의 최근 "membership"을 가진 모든 사용자를 가져옵니다.

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

또는, 컬럼을 서브쿼리의 결과와 비교하는 "where" 절을 작성할 수 있습니다. 이 때는 컬럼, 비교 연산자, 클로저를 `where` 메서드에 전달하면 됩니다. 예를 들어, 아래 쿼리는 금액이 평균 미만인 모든 수입 레코드를 가져옵니다.

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전체 텍스트 Where 절

> [!WARNING]
> 전체 텍스트 where 절은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText`, `orWhereFullText` 메서드를 통해 전체 텍스트 인덱스가 있는 [컬럼](/docs/12.x/migrations#available-index-types)에 대해 전체 텍스트 "where" 절을 쿼리에 추가할 수 있습니다. 이 메서드들은 사용 중인 데이터베이스 시스템에 맞는 적합한 SQL로 변환됩니다. 예를 들어 MariaDB 또는 MySQL을 사용할 때는 `MATCH AGAINST` 절이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, Limit, Offset

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드를 사용하면 쿼리 결과를 지정한 컬럼으로 정렬할 수 있습니다. 첫 번째 인수는 정렬 대상 컬럼이며, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼을 기준으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향 인수는 생략할 수 있으며, 기본값은 오름차순(asc)입니다. 내림차순으로 정렬하고 싶다면 두 번째 인수를 지정하거나, `orderByDesc` 메서드를 사용하면 됩니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

마지막으로, `->` 연산자를 사용하여 JSON 컬럼 내의 특정 값으로 정렬할 수도 있습니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest` 및 `oldest` 메서드를 사용하면 날짜 기준으로 손쉽게 정렬할 수 있습니다. 기본적으로 테이블의 `created_at` 컬럼을 기준으로 정렬합니다. 또는 정렬에 사용할 컬럼명을 전달할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder` 메서드는 쿼리 결과를 무작위로 정렬합니다. 예를 들어, 임의의 사용자 한 명을 가져올 때 사용할 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 이전에 적용된 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드 호출 시 컬럼과 정렬 방향을 함께 전달하면, 기존 "order by" 절을 모두 제거하고 지정한 컬럼, 방향으로 정렬을 새로 적용할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

편의를 위해 `reorderDesc` 메서드를 사용해 내림차순 정렬로 바꿀 수도 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상하듯이, `groupBy`와 `having` 메서드를 사용해 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드의 시그니처는 `where` 메서드와 비슷합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용해서 결과가 특정 범위에 속하는지 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy` 메서드에 여러 인수를 전달하여 여러 컬럼을 기준으로 그룹화할 수도 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 구문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit 및 Offset

`limit`과 `offset` 메서드를 사용해 쿼리 결과로 반환되는 레코드 수를 제한하거나, 지정한 개수만큼 결과를 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

특정 조건에 따라 쿼리의 일부 절(예: where)을 적용해야 할 수 있습니다. 예를 들어, HTTP 요청에 주어진 값이 있을 때만 `where` 문을 적용하고 싶을 수 있습니다. 이런 경우 `when` 메서드를 사용할 수 있습니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`일 때만 주어진 클로저를 실행합니다. 만약 첫 번째 인수가 `false`이면 클로저는 실행되지 않습니다. 즉, 위 예시에서 `role` 필드가 요청에 포함되어 있고, 값이 `true`로 평가될 때만 클로저가 실행됩니다.

또한, `when` 메서드에 세 번째 인수로 클로저를 전달할 수도 있습니다. 이 클로저는 첫 번째 인수가 `false`로 평가될 때만 실행됩니다. 아래 예시는 쿼리의 기본 정렬 방식을 상황에 맞게 적용하는 방법을 보여줍니다.

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
## Insert 문

쿼리 빌더에서는 데이터베이스 테이블에 레코드를 삽입할 수 있는 `insert` 메서드도 제공합니다. `insert` 메서드는 컬럼명과 값 쌍의 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 배열의 배열을 전달하면 됩니다. 각각의 배열이 삽입할 레코드 한 개를 나타냅니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드 삽입 중 발생하는 오류를 무시합니다. 이 메서드를 사용할 때는 중복 레코드 오류가 무시되며, 데이터베이스 엔진에 따라 다른 유형의 오류도 무시될 수 있다는 점을 유의해야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict 모드](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 삽입할 데이터를 결정하기 위해 서브쿼리를 사용하여 새로운 레코드를 테이블에 삽입할 수 있습니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 auto-increment 컬럼이 있는 경우, `insertGetId` 메서드를 사용해 레코드를 삽입하고 바로 ID 값을 얻을 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 때 `insertGetId` 메서드는 자동 증가 컬럼 이름이 `id`라고 가정합니다. 만약 다른 "시퀀스"에서 ID를 가져오고 싶다면, `insertGetId` 메서드의 두 번째 인수로 컬럼명을 전달할 수 있습니다.

<a name="upserts"></a>
### Upserts

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 있는 레코드는 새로운 값으로 업데이트합니다. 첫 번째 인수에는 삽입 또는 업데이트할 값들을, 두 번째 인수에는 레코드를 고유하게 식별할 컬럼(또는 컬럼 배열), 세 번째 인수에는 이미 존재하는 레코드에서 업데이트할 컬럼 배열을 전달합니다.

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

위 예시에서 라라벨은 두 레코드 삽입을 시도합니다. 만약 동일한 `departure`, `destination` 컬럼 조합이 이미 존재하면 해당 레코드의 `price` 컬럼 값을 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인수(고유 컬럼들)가 반드시 "primary" 또는 "unique" 인덱스를 가져야 합니다. 또한 MariaDB, MySQL 드라이버는 `upsert`의 두 번째 인수를 무시하고 테이블의 "primary", "unique" 인덱스만을 이용해 기존 레코드를 판별합니다.

<a name="update-statements"></a>
## Update 문

데이터베이스에 데이터를 삽입하는 것 외에도, 쿼리 빌더를 사용해 기존 레코드들을 `update` 메서드로 수정할 수 있습니다. `update` 메서드는 업데이트할 컬럼과 값의 쌍이 담긴 배열을 인수로 받으며, 영향을 받은 행의 개수를 반환합니다. `where` 절 등으로 `update` 쿼리를 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

가끔은 데이터베이스에 기존 레코드가 있으면 업데이트하고, 없으면 생성하고 싶을 수 있습니다. 이럴 때는 `updateOrInsert` 메서드를 사용하세요. 이 메서드는 찾으려는 레코드 조건 배열과, 업데이트할 컬럼 및 값 배열 두 가지 인수를 받습니다.

`updateOrInsert` 메서드는 첫 번째 인수의 컬럼과 값 쌍을 기준으로 데이터베이스에서 레코드를 찾아보고, 존재한다면 두 번째 인수에 주어진 값으로 컬럼을 업데이트합니다. 찾지 못했다면 두 인수의 값을 병합해 새로운 레코드를 삽입합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

`updateOrInsert` 메서드에 클로저를 전달하면, 레코드의 존재 여부에 따라 업데이트/삽입할 컬럼을 동적으로 지정할 수도 있습니다.

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

JSON 컬럼을 업데이트할 때는 `->` 문법을 사용하여 JSON 오브젝트 내의 특정 키를 업데이트할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소 (Increment & Decrement)

쿼리 빌더는 특정 컬럼 값을 증가시키거나 감소시키는 편리한 메서드도 제공합니다. 이들은 최소한 수정할 컬럼명을 인수로 받으며, 두 번째 인수로 증감할 수치를 설정할 수도 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 증가 또는 감소 연산과 동시에 추가 컬럼도 업데이트할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, `incrementEach` 및 `decrementEach` 메서드로 여러 컬럼을 한 번에 증가 또는 감소시킬 수 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>

## 삭제(DELETE) 구문

쿼리 빌더의 `delete` 메서드를 사용하여 테이블에서 레코드를 삭제할 수 있습니다. `delete` 메서드는 영향을 받은 행(row)의 개수를 반환합니다. `delete` 메서드를 호출하기 전에 "where" 절을 추가하여 삭제 대상을 제한할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더는 `select` 구문을 실행할 때 "비관적 잠금"을 구현할 수 있는 몇 가지 메서드를 제공합니다. "공유 잠금(shared lock)"을 적용하려면 `sharedLock` 메서드를 사용하면 됩니다. 공유 잠금은 트랜잭션이 커밋될 때까지 선택된 행이 수정되는 것을 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 `lockForUpdate` 메서드를 사용할 수도 있습니다. "for update" 잠금은 선택된 레코드가 수정되거나, 다른 공유 잠금과 함께 선택되는 것을 모두 방지합니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금을 사용할 때는 [트랜잭션](/docs/12.x/database#database-transactions)으로 감싸는 것이 필수는 아니지만, 권장됩니다. 이렇게 하면 데이터 조회 후 전체 작업이 끝날 때까지 데이터베이스의 데이터가 변경되지 않도록 보장할 수 있습니다. 만약 실패가 발생한다면, 트랜잭션이 변경 내용을 자동으로 롤백하고 잠금을 해제합니다.

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

애플리케이션 곳곳에서 반복적으로 동일한 쿼리 로직을 사용해야 한다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 사용하여 쿼리 로직을 재사용 가능한 객체로 추출할 수 있습니다. 다음은 애플리케이션 내에서 두 가지 서로 다른 쿼리를 사용하는 예시입니다.

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

이처럼 쿼리들 사이에 공통적으로 들어가는 목적지(destination) 필터링 로직을 하나의 재사용 객체로 추출할 수 있습니다.

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

그런 다음, 쿼리 빌더의 `tap` 메서드를 사용하여 이 객체의 로직을 쿼리에 적용할 수 있습니다.

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

`tap` 메서드는 항상 쿼리 빌더 인스턴스를 반환합니다. 쿼리를 실행해서 다른 값을 반환하도록 객체를 추출하고 싶다면, 대신 `pipe` 메서드를 사용할 수 있습니다.

다음은 애플리케이션 전반에 반복적으로 사용되는 [페이지네이션](/docs/12.x/pagination) 로직을 담은 쿼리 객체 예시입니다. `DestinationFilter`와 달리 `Paginate` 객체는 쿼리에 조건만 적용하는 것이 아니라, 쿼리를 실행해서 페이저네이터(paginator) 인스턴스를 반환합니다.

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

쿼리 빌더의 `pipe` 메서드를 사용하면, 이 객체를 사용해 반복되는 페이지네이션 로직을 쉽게 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리를 작성하는 도중 `dd` 및 `dump` 메서드를 사용하여 현재 쿼리 바인딩과 SQL을 출력할 수 있습니다. `dd` 메서드는 디버그 정보를 출력한 뒤 요청 실행을 즉시 중단합니다. `dump` 메서드는 디버그 정보를 보여주지만, 요청은 계속 진행됩니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드를 사용하면, 파라미터 바인딩이 모두 반영된 SQL 쿼리를 바로 출력할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```