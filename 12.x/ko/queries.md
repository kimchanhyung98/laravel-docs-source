# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과 조각 처리](#chunking-results)
    - [지연 스트리밍 처리](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니언](#unions)
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
    - [벡터 유사성 절](#vector-similarity-clauses)
- [정렬, 그룹화, 제한, 오프셋](#ordering-grouping-limit-and-offset)
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
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 손쉽고 유연하게 작성하고 실행할 수 있는 인터페이스를 제공합니다. 이는 애플리케이션에서 대부분의 데이터베이스 작업을 처리하는 데 사용할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽히 호환됩니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호합니다. 쿼리 빌더에 전달되는 문자열은 바인딩되어 전달되므로, 별도로 문자열을 정제하거나 이스케이프할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력을 기반으로 쿼리에서 참조하는 컬럼명, 특히 "order by" 컬럼 등을 절대로 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회

`DB` 파사드에서 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 유연한 쿼리 빌더 인스턴스를 반환하며, 추가적인 조건을 체이닝하고 마지막에 `get` 메서드로 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 표시합니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체입니다. 각 컬럼 값은 객체의 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터를 변환하고 집계하기 위한 매우 강력한 메서드를 다양하게 제공합니다. Laravel 컬렉션에 대한 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회

데이터베이스 테이블에서 한 행만 조회하려면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

조건에 맞는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException`을 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. 예외가 잡히지 않으면 404 HTTP 응답이 자동으로 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없다면, `value` 메서드로 특정 컬럼의 값만 바로 추출할 수 있습니다. 이 메서드는 해당 컬럼 값을 직접 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

또한, `id` 컬럼 값으로 특정 행을 조회하려면 `find` 메서드를 사용할 수 있습니다:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회

특정 컬럼값만 모은 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면 `pluck` 메서드를 사용할 수 있습니다. 아래 예시는 사용자들의 직함 컬렉션을 조회하는 예시입니다:

```php
use Illuminate\Support\Facades.DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인자로 결과 컬렉션의 키가 될 컬럼을 지정할 수도 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 조각 처리 (Chunking Results)

수천 건의 데이터베이스 레코드를 다루어야 할 때는 `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 한번에 소량의 결과만 조회해서 콜백으로 전달합니다. 예를 들어, `users` 테이블 전체를 한 번에 100개씩 처리하려면 다음과 같이 할 수 있습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades.DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

콜백에서 `false`를 반환하면 추가로 쿼리가 처리되지 않습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

조각별로 레코드를 업데이트한다면 예상치 못한 방식으로 결과가 달라질 수 있습니다. 조각 처리 중에 레코드를 업데이트해야 한다면 `chunkById` 메서드를 사용하는 것이 가장 좋습니다. 이 메서드는 자동으로 주 키(primary key)를 기준으로 결과를 페이지네이션합니다:

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

`chunkById` 및 `lazyById` 메서드는 내부적으로 직접 "where" 조건을 추가하므로, 추가적인 조건이 있다면 [논리적 그룹화](#logical-grouping)를 위해 클로저로 감싸는 것이 좋습니다:

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
> 조각 처리 콜백 안에서 레코드의 주키(primary key) 또는 외래키(foreign key)를 변경하면 쿼리 결과에 영향이 있을 수 있습니다. 일부 레코드가 결과에서 누락될 수 있으니 주의하세요.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍 처리 (Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)처럼 쿼리를 조각별로 실행합니다. 그러나 각 조각을 콜백으로 전달하는 대신, `lazy()` 메서드는 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환하여 전체 결과를 스트림처럼 다룰 수 있도록 합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 반복 처리 중에 레코드를 업데이트해야 한다면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이들은 주키를 기준으로 자동 페이징됩니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 중에 레코드의 주키(primary key)나 외래키(foreign key) 값을 변경하면 쿼리의 결과가 달라질 수 있으며, 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등의 다양한 집계 메서드를 제공합니다. 쿼리를 작성한 후 이러한 메서드를 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 집계 메서드는 다른 조건과도 함께 사용할 수 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

쿼리 조건에 맞는 레코드가 존재하는지 `count` 대신 `exists`와 `doesntExist` 메서드를 사용할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## Select 구문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### Select 절 지정

데이터베이스 테이블의 모든 컬럼을 조회하지 않고, 원하는 컬럼만 지정하고 싶을 때는 `select` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드는 쿼리 결과가 중복되지 않도록 강제할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있을 때, 기존 select 절에 컬럼을 추가하려면 `addSelect` 메서드를 사용할 수 있습니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 (Raw Expressions)

쿼리에 임의의 SQL 문자열을 삽입해야 할 때가 있습니다. 이럴 때 `DB` 파사드의 `raw` 메서드로 Raw 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 문자열로 그대로 삽입되므로, SQL 인젝션 취약점에 노출되지 않도록 각별한 주의가 필요합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 대신 아래 메서드를 사용하여 쿼리의 다양한 부분에 raw 표현식을 삽입할 수도 있습니다. **Raw 표현식을 사용하는 쿼리는 Laravel이 SQL 인젝션으로부터 완전히 보호해줄 수 없습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 두 번째 인자로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`, `orWhereRaw` 메서드는 쿼리에 raw "where" 절을 삽입합니다. 두 번째 인자로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`, `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 사용할 수 있게 합니다. 두 번째 인자로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 raw 문자열을 사용할 수 있습니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 사용할 수 있도록 합니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더로 쿼리에 조인(join) 절을 추가할 수 있습니다. 기본 "inner join"을 하려면 `join` 메서드를 사용하세요. 첫 번째 인자는 조인할 테이블 이름이며, 나머지 인자로는 컬럼 제약조건을 지정합니다. 한번의 쿼리에서 여러 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join" 또는 "right join"을 하고 싶다면, `leftJoin`이나 `rightJoin` 메서드를 사용하면 됩니다. 시그니처는 `join`과 동일합니다:

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

"cross join"을 하려면 `crossJoin` 메서드를 사용할 수 있습니다. cross join은 두 테이블 간의 데카르트 곱(cartesian product)을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인 조건이 필요하다면, 두 번째 인수로 클로저를 전달하세요. 이 클로저에는 `Illuminate\Database\Query\JoinClause` 인스턴스가 전달되며, 이를 통해 다양한 조인 조건을 추가할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 절을 사용하려면, `JoinClause` 인스턴스의 `where`와 `orWhere` 메서드를 사용하면 됩니다. 이들은 두 컬럼이 아닌, 컬럼과 값을 비교합니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하여 서브쿼리와 조인할 수 있습니다. 각 메서드는 세 개의 인자를 받으며, 서브쿼리, 별칭, 연결할 컬럼을 정의하는 클로저입니다. 아래 예시는 각 사용자마다 최근에 게시한 블로그 포스트의 `created_at` 타임스탬프를 포함하여 사용자 컬렉션을 조회하는 예시입니다:

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
#### Lateral 조인

> [!WARNING]
> Lateral 조인은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하여 서브쿼리와 "lateral join"을 수행할 수 있습니다. 각 메서드는 서브쿼리와 별칭 두 개의 인자를 받으며, 조인 조건은 해당 서브쿼리의 `where` 절에서 지정해야 합니다. Lateral 조인은 각 행별로 평가되며, 서브쿼리 외부의 컬럼을 참조할 수 있습니다.

아래 예시는 각 사용자와 해당 사용자의 최근 블로그 포스트 3개를 조회하는 예시입니다. 각 사용자는 최대 3개의 결과 행을 생성할 수 있습니다. 조인 조건은 서브쿼리 안에서 `whereColumn`을 사용하여 현재 사용자 행을 참조합니다:

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
## 유니언 (Unions)

쿼리 빌더는 여러 쿼리를 "union"으로 합치는 편리한 방법도 제공합니다. 예를 들어, 기본 쿼리를 만든 후 `union` 메서드를 호출해 더 많은 쿼리와 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$usersWithoutFirstName = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($usersWithoutFirstName)
    ->get();
```

`union` 이외에도, `unionAll` 메서드는 중복 결과를 제거하지 않고 그대로 합칩니다. 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용해 "where" 절을 추가할 수 있습니다. 가장 기본적인 호출 방식은 세 개의 인자를 필요로 합니다. 첫 번째는 컬럼명, 두 번째는 데이터베이스에서 지원하는 연산자, 세 번째는 비교 값입니다.

예를 들어 아래 쿼리는 `votes` 컬럼이 100이고, `age` 컬럼이 35보다 큰 사용자를 조회합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

`=` 연산자를 사용할 때는 두 번째 인자로 바로 값을 넘겨도 되며, 이 경우 Laravel이 `=` 연산을 자동으로 적용합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

여러 컬럼을 한 번에 조건으로 조회하고 싶을 때는 연관 배열을 전달할 수 있습니다:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

뿐만 아니라, 데이터베이스에서 지원하는 모든 연산자를 사용할 수 있습니다:

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

세 개의 인자 배열을 요소로 하는 배열을 전달하면, 여러 조건을 한 번에 지정할 수도 있습니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에서 참조되는 컬럼명에 영향을 주어서는 안 됩니다. "order by" 컬럼명에도 동일하게 적용됩니다.

> [!WARNING]
> MySQL과 MariaDB는 문자열-숫자 비교 시 문자열을 자동으로 정수로 변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되어 예상과 다른 결과가 발생할 수 있습니다. 예를 들어, 테이블에 `secret` 컬럼 값이 `aaa`인 레코드가 있고 `User::where('secret', 0)`을 실행하면 해당 행이 반환될 수 있습니다. 따라서 쿼리 사용 전 값의 타입을 반드시 명확히 지정하십시오.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드 체이닝 시 기본적으로 `and`로 연결됩니다. 하지만, `or`로 조건을 연결하려면 `orWhere` 메서드를 사용하면 됩니다. `orWhere` 역시 `where`와 같은 인자를 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

"or" 조건을 괄호로 그룹화하고 싶다면, 첫 번째 인자로 클로저를 전달하면 됩니다:

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

위 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 전역 스코프 적용 시 의도치 않은 쿼리 동작을 피하기 위해 항상 `orWhere` 호출 그룹화를 권장합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`과 `orWhereNot` 메서드는 쿼리 조건 그룹을 부정(negate, NOT)합니다. 다음 쿼리는 할인 중이거나 가격이 10 미만인 상품을 제외합니다:

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

여러 컬럼에 동일한 조건을 적용해야 할 때가 있습니다. 예를 들어, 목록 중 하나라도 `LIKE` 패턴과 일치하는 모든 레코드를 조회하려면 `whereAny`를 사용할 수 있습니다:

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

위 쿼리는 아래와 같은 SQL을 생성합니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

마찬가지로, 모든 컬럼이 조건을 만족해야 할 때는 `whereAll`을 사용할 수 있습니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

이 쿼리는 다음과 같습니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

어떤 컬럼도 조건을 만족하지 않아야 할 때 `whereNone`을 사용할 수 있습니다:

```php
$albums = DB::table('albums')
    ->where('published', true)
    ->whereNone([
        'title',
        'lyrics',
        'tags',
    ], 'like', '%explicit%')
    ->get();
```

이 쿼리는 다음과 같습니다:

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

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에서 직접 JSON 컬럼을 대상으로 조회할 수 있습니다. JSON 컬럼 조회는 `->` 연산자를 사용합니다:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

JSON 배열을 조건으로 처리하고 싶다면 `whereJsonContains`, `whereJsonDoesntContain` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL을 사용하는 경우에는 값 배열을 전달할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

JSON 키의 포함 여부로 검색할 때는 `whereJsonContainsKey`, `whereJsonDoesntContainKey` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이로 검색하려면 `whereJsonLength`를 사용할 수 있습니다:

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

`whereLike` 메서드는 패턴 매칭을 위한 "LIKE" 절을 쿼리에 추가합니다. 이 메서드는 데이터베이스에 독립적인(agnostic) 방식으로 문자열 매칭 쿼리를 수행하며, 기본적으로 대소문자를 구분하지 않습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인자를 true로 지정하면 대소문자를 구분하는 검색도 가능합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`는 "or" 절과 LIKE 조건을 함께 추가할 때 사용합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 절을 쿼리에 추가합니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로 `orWhereNotLike`를 사용하면 "or" + "NOT LIKE"가 결합된 조건을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색 옵션은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 컬럼 값이 주어진 배열에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 주어진 배열에 포함되지 않는 값을 조회합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

두 번째 인자로 쿼리 객체를 전달할 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예제는 다음과 같은 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 매우 많은 정수 배열을 바인딩해야 할 때는 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 사용하면 메모리 사용을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값 밖에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 하나의 컬럼 값이 같은 행의 두 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 컬럼 값이 두 컬럼 값의 범위 밖에 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween`는 특정 값이 같은 행의 두 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`는 값이 두 컬럼 값의 범위 밖에 있는지 확인합니다:

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 해당 컬럼 값이 `NULL`인지 확인합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼 값이 NULL이 아닌지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`로 컬럼 값을 특정 날짜와 비교할 수 있습니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`로는 컬럼 값을 특정 월과 비교합니다:

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay`는 컬럼 값을 특정 일(day of month)과 비교합니다:

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`는 컬럼 값을 특정 연도와 비교합니다:

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`는 컬럼 값을 특정 시간과 비교합니다:

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast` 및 `whereFuture`는 컬럼 값이 과거/미래인지 확인합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture`는 현재 시점 포함 여부까지 포함하여 과거/미래를 판별합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 각각 오늘/오늘 이전/오늘 이후에 해당하는지 확인합니다:

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

`whereTodayOrBefore`, `whereTodayOrAfter`로 오늘 포함해 이전/이후 범위를 지정할 수 있습니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼이 같은지, 혹은 비교 연산 결과를 판별합니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 지정할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

컬럼 비교 배열을 전달하면 AND 조건으로 연결됩니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화 (Logical Grouping)

조건을 괄호로 그룹화해야 원하는 쿼리 결과를 만들 수 있습니다. 특히, `orWhere`는 항상 괄호로 묶는 것이 좋습니다. 클로저를 `where` 메서드에 전달하면 그룹화가 됩니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위의 예시는 다음 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프가 적용될 때 의도치 않은 쿼리 동작을 방지하려면 항상 `orWhere` 그룹화를 하세요.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" SQL 절을 작성할 수 있도록 해줍니다. 이 메서드는 클로저를 받아, 해당 클로저 안에서 쿼리 빌더를 사용해 exists 서브쿼리를 작성할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

혹은 클로저 대신 쿼리 객체를 `whereExists`에 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 예시는 아래와 같은 SQL을 만듭니다:

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

서브쿼리 결과와 값을 비교하는 "where" 절이 필요하다면, `where`에 클로저와 값을 전달하면 됩니다. 다음 쿼리는 특정 타입의 최근 "membership"이 있는 사용자를 모두 조회합니다:

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

또한, 서브쿼리 결과와 컬럼 값을 비교할 수도 있습니다. 예를 들어, 평균보다 금액이 작은 수입(income)을 조회하려면 다음과 같이 할 수 있습니다:

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
> 전체 텍스트 where 절은 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText`와 `orWhereFullText`로 [전체 텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 생성된 컬럼에 전체 텍스트 "where" 절을 추가할 수 있습니다. 이 메서드는 사용 중인 데이터베이스에 따라 적합한 SQL(MariaDB/MySQL은 `MATCH AGAINST` 절 등)로 변환됩니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
### 벡터 유사성 절

> [!NOTE]
> 벡터 유사성 절은 현재 PostgreSQL 커넥션의 `pgvector` 확장에서만 지원됩니다. 벡터 컬럼 및 인덱스 정의 관련 정보는 [마이그레이션 문서](/docs/12.x/migrations#available-column-types)를 참고하세요.

`whereVectorSimilarTo` 메서드는 대상 벡터와 주어진 벡터 간의 코사인 유사도를 기준으로 결과를 필터하고, 관련도 순으로 정렬합니다. `minSimilarity`는 0.0~1.0(1.0은 완전히 동일) 사이 값을 지정합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

벡터 자리에 일반 문자열을 지정하면, Laravel이 [Laravel AI SDK](/docs/12.x/ai-sdk#embeddings)를 사용해 임베딩을 자동 생성합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

기본적으로 이 메서드는 거리(유사도 기준) 순으로 정렬합니다. 정렬을 비활성화하려면 `order` 인자로 false를 전달하면 됩니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

더 세밀하게 제어하려면 `selectVectorDistance`, `whereVectorDistanceLessThan`, `orderByVectorDistance` 메서드를 조합할 수 있습니다:

```php
$documents = DB::table('documents')
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한, 오프셋 (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드를 사용하면 쿼리 결과를 특정 컬럼 기준으로 정렬할 수 있습니다. 첫 번째 인자는 정렬할 컬럼명, 두 번째 인자는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 기본적으로 오름차순이며, 내림차순은 두 번째 인자를 지정하거나, `orderByDesc`를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

JSON 컬럼 내부 값을 정렬하려면 `->` 연산자를 사용할 수 있습니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`, `oldest` 메서드는 쉽게 날짜 기준 정렬을 제공합니다. 기본적으로 테이블의 `created_at` 컬럼 기준으로 정렬됩니다. 원하는 컬럼명을 전달할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 무작위 사용자를 조회할 때 사용할 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거하기

`reorder` 메서드는 이미 추가된 모든 "order by" 절을 제거하고 정렬이 되지 않은 결과로 반환합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

특정 컬럼과 방향으로 재정렬하려면 `reorder`에 인자를 전달할 수 있습니다. 즉, 기존 정렬 절을 모두 제거하고 새로운 정렬을 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

내림차순 재정렬을 위해서는 `reorderDesc` 메서드도 사용할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화 (Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`, `having` 메서드로 결과 그룹화를 할 수 있습니다. `having` 메서드는 `where` 메서드와 유사한 시그니처를 가집니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween`을 사용하면 지정한 범위 내에서 결과를 필터링할 수 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

다수 컬럼을 그룹화하려면 `groupBy`에 여러 인자를 전달하면 됩니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 having 구문 작성은 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit 및 Offset

`limit`, `offset` 메서드로 결과 범위를 제한 및 스킵할 수 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

애플리케이션의 다른 조건에 따라 특정 쿼리 절을 적용하고 싶을 때가 있습니다. 예를 들어, HTTP 요청에 특정 입력값이 있는 경우에만 `where` 구문을 적용하고 싶다면 `when` 메서드를 사용하면 됩니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인자가 true일 때만 주어진 클로저를 실행합니다. 위 예시에서도 `role` 값이 존재하고 true로 평가되는 경우만 클로저가 실행됩니다.

세 번째 인자로 또 다른 클로저를 전달할 수도 있는데, 이 클로저는 첫 번째 인자가 false일 때만 실행됩니다. 예를 들어, 쿼리의 기본 정렬을 조건에 따라 다르게 적용할 수 있습니다:

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
## Insert 구문 (Insert Statements)

쿼리 빌더의 `insert` 메서드로 레코드를 데이터베이스에 삽입할 수 있습니다. `insert`는 컬럼명과 값 쌍의 배열을 인자로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

한 번에 여러 레코드를 삽입하려면 배열의 배열을 전달하면 됩니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore`는 삽입 오류가 발생해도 무시하고 계속 실행합니다. 이 메서드를 사용할 때는 중복 레코드 관련 에러가 무시된다는 점, 그리고 데이터베이스 엔진에 따라 다른 신종 에러도 무시될 수 있다는 점을 유의하세요. 예를 들면, `insertOrIgnore`는 [MySQL의 strict 모드](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing`은 서브쿼리 결과를 기반으로 테이블에 새로운 레코드를 삽입합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 ID가 있을 경우, `insertGetId` 메서드로 레코드 삽입 후 ID 값을 바로 반환받을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL 사용 시, `insertGetId`는 자동 증가 컬럼명이 반드시 `id`여야 합니다. 만약 다른 "시퀀스"에서 ID를 받고 싶다면, 두 번째 파라미터로 컬럼명을 전달하면 됩니다.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 내용으로 업데이트합니다. 첫 번째 인자에는 삽입/업데이트할 값, 두 번째 인자에는 레코드 고유성을 확인할 기준 컬럼배열, 세 번째 인자는 이미 존재하는 경우 업데이트할 컬럼 배열입니다:

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

위 예시에서, Laravel은 두 개 레코드를 삽입 시도하며, 같은 `departure`, `destination` 값이 이미 있다면 해당 행의 `price`만 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스 엔진은 `upsert`의 두 번째 인자에 명시한 컬럼이 "primary"나 "unique" 인덱스가 있어야 합니다. MariaDB, MySQL 드라이버는 항상 테이블의 "primary"/"unique" 인덱스를 기준으로 중복을 판단합니다.

<a name="update-statements"></a>
## Update 구문 (Update Statements)

삽입 뿐만 아니라, `update` 메서드를 통해서도 기존 레코드를 갱신할 수 있습니다. `update`는 컬럼-값 쌍의 배열을 받으며, 영향을 받은 행의 개수를 반환합니다. `where` 등을 함께 사용해 쿼리 범위를 지정할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update or Insert

기존 레코드를 업데이트하고, 없으면 새로 생성하고 싶을 때는 `updateOrInsert`를 사용하세요. 첫 번째 인자는 조건, 두 번째 인자는 업데이트할 컬럼-값 쌍입니다.

`updateOrInsert`는 첫 번째 인자로 레코드를 찾고, 존재하면 두 번째 인자로 업데이트하고, 없으면 두 인자를 합친 속성 값으로 새 레코드를 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

레코드 존재 여부에 따라 다르게 값을 삽입/업데이트해야 한다면, 클로저를 두 번째 인자로 전달할 수도 있습니다:

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
### JSON 컬럼 업데이트 (Updating JSON Columns)

JSON 컬럼을 업데이트할 때는 `->` 구문을 사용해 JSON 객체의 키를 직접 지정하여 업데이트할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소 (Increment and Decrement)

쿼리 빌더는 특정 컬럼 값을 쉽게 증가시키거나 감소시키는 `increment`, `decrement` 메서드도 제공합니다. 첫 번째 인자는 컬럼명, 두 번째 인자는 수치(기본값 1)입니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

증가/감소와 함께 다른 컬럼을 업데이트하고 싶다면 추가 컬럼 배열을 세 번째 인자로 전달할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

`incrementEach`, `decrementEach`로 여러 컬럼을 한 번에 갱신할 수도 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문 (Delete Statements)

쿼리 빌더의 `delete` 메서드로 레코드를 삭제할 수 있습니다. `delete`는 영향을 받은 행의 개수를 반환하며, "where" 조건으로 삭제 유효 범위를 제한할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 select 쿼리 실행 시 "비관적 잠금(pessimistic locking)"을 위한 메서드도 제공합니다. "공유 잠금(shared lock)"을 하려면 `sharedLock`을 호출하면 됩니다. 공유 잠금은 트랜잭션이 커밋될 때까지 해당 행이 수정되지 못하도록 막습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는, `lockForUpdate`로 "for update" 잠금을 걸 수 있습니다. 이 잠금은 해당 레코드가 다른 공유 잠금에서도 읽히지 못하고, 오직 현재 트랜잭션에서만 수정/읽기가 가능합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

꼭 필수는 아니지만, 비관적 잠금을 사용할 때는 [트랜잭션](/docs/12.x/database#database-transactions)으로 래핑하는 것이 권장됩니다. 이렇게 하면 작업 도중 데이터가 변경되지 않으며, 실패 시 자동으로 롤백되어 잠금이 해제됩니다:

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
## 재사용 가능한 쿼리 컴포넌트 (Reusable Query Components)

애플리케이션 전반에 여러 번 같은 쿼리 로직이 반복된다면, 쿼리 빌더의 `tap`, `pipe` 메서드를 사용해 재사용 가능한 객체로 분리할 수 있습니다. 예를 들어, 다음과 같이 두 쿼리에 공통 로직이 있다면:

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

공통적인 목적지(destination) 필터링을 다음처럼 객체로 분리할 수 있습니다:

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

이제 쿼리 빌더의 `tap` 메서드로 객체 로직을 쉽게 적용할 수 있습니다:

```php
use App\Scopes\DestinationFilter;
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->orderByDesc('price')
    ->get();

// ...

DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```

<a name="query-pipes"></a>
#### 쿼리 파이프 (Query Pipes)

`tap` 메서드는 반드시 쿼리 빌더 인스턴스를 반환합니다. 쿼리를 실행하고 다른 값을 반환하고 싶다면, `pipe` 메서드를 사용할 수 있습니다.

예를 들어, 애플리케이션 전역에서 [페이지네이션](/docs/12.x/pagination) 로직을 공유하려면 아래처럼 객체화할 수 있습니다. 이 unlike `DestinationFilter`, `Paginate`는 쿼리를 실행해 paginator 인스턴스를 반환합니다:

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

쿼리 빌더의 `pipe` 메서드를 이용해 아래와 같이 파이프라인을 만들 수 있습니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리를 작성하는 중간에 `dd`, `dump` 메서드를 사용해 쿼리 바인딩과 SQL 구문을 바로 출력해 볼 수 있습니다. `dd`는 디버그 정보를 표시한 후 요청을 즉시 종료하며, `dump`는 정보를 표시한 뒤 요청을 계속 처리합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`, `ddRawSql` 메서드는 매개변수가 올바르게 대입된 쿼리 SQL을 바로 볼 수 있습니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```