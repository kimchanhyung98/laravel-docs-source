# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크 단위로 처리](#chunking-results)
    - [결과를 게으르게 스트리밍](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니온](#unions)
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
    - [풀텍스트 Where 절](#full-text-where-clauses)
    - [벡터 유사도 절](#vector-similarity-clauses)
- [정렬, 그룹화, 리밋과 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [리밋과 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소 연산](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 구성요소](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 손쉽고 유연하게 생성하고 실행할 수 있는 인터페이스를 제공합니다. 이 쿼리 빌더는 애플리케이션에서 대부분의 데이터베이스 작업을 처리할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 호환됩니다.

Laravel 쿼리 빌더는 PDO의 파라미터 바인딩(Parameter Binding)을 활용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 따라서 쿼리 바인딩 값으로 전달되는 문자열을 별도로 정제(Clean)하거나 필터링(Sanitize)할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조하는 컬럼명(예: "order by"에 사용할 컬럼명)을 사용자 입력값으로 받는 것은 절대로 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 조회

`DB` 파사드가 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 유연한(Fluent) 쿼리 빌더 인스턴스를 반환하며, 여기에 추가적인 제약을 체이닝하고 마지막에 `get` 메서드로 쿼리 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 목록으로 표시합니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 각각의 결과는 PHP의 `stdClass` 객체로 제공되며, 컬럼 값에 접근할 때는 객체의 속성처럼 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑과 축소를 위해 매우 강력한 다양한 메서드를 제공합니다. Laravel 컬렉션에 대해 더 알고 싶다면 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회

테이블에서 한 행만 조회하고 싶다면, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 일치하는 행이 없을 때 `Illuminate\Database\RecordNotFoundException`를 던지게 하려면 `firstOrFail` 메서드를 사용하세요. 이 예외가 잡히지 않으면, Laravel은 자동으로 404 HTTP 응답을 클라이언트로 전송합니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없다면, `value` 메서드로 기록에서 특정 컬럼의 값을 바로 추출할 수 있습니다. 이 메서드는 해당 컬럼의 값을 직접 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면, `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회

특정 컬럼의 값들만 모은 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 다음 예시에서는 사용자들의 직함(`title`)만을 모읍니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인수로 컬렉션의 키로 사용할 컬럼명을 지정할 수도 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리 (Chunking Results)

수천 건 이상의 데이터베이스 레코드를 처리해야 한다면, `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 작은 청크(조각) 단위로 한 번에 가져와서, 각 청크를 클로저에 전달해 처리하게 해줍니다. 예를 들어, `users` 테이블 전체를 100개씩 청크로 불러오는 예시입니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 더 이상의 청크 처리를 중단할 수 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리를 하면서 데이터베이스 레코드를 수정하는 경우, 예기치 않은 결과가 발생할 수 있습니다. 청크 중 레코드를 수정하는 경우에는 `chunkById` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 기본키 기준으로 자동 페이징을 처리합니다:

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

`chunkById` 및 `lazyById` 메서드는 쿼리 실행 시 자체적으로 "where" 조건을 추가하므로, 직접 지정한 조건들은 클로저 내부에 [논리적으로 그룹화](#logical-grouping)해서 사용하는 것이 좋습니다:

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
> 청크 콜백 내부에서 레코드를 갱신(Update)하거나 삭제(Delete)할 때, 기본키나 외래키가 변경되면 쿼리의 청크 결과에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 누락될 수 있으니 주의하세요.

<a name="streaming-results-lazily"></a>
### 결과를 게으르게 스트리밍 (Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)처럼 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백에 전달하는 대신 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환하여 결과를 스트림 방식으로 순차적으로 다룰 수 있게 합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 반복(iterate)하면서 레코드를 수정할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이들은 기본키 기준으로 자동 페이징 처리됩니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 중에 기본키나 외래키를 변경하면 쿼리의 청크 결과가 달라지거나 일부 레코드가 누락될 수 있으니 주의하세요.

<a name="aggregates"></a>
### 집계 함수 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`과 같은 집계값을 쉽게 가져올 수 있는 다양한 메서드를 제공합니다. 아래 예시처럼 쿼리를 만든 후 바로 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

다른 절(Clause)와 결합하여 집계값을 세밀하게 제어할 수 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

쿼리 조건에 해당하는 레코드가 존재하는지 확인하려면 `count` 대신, `exists`와 `doesntExist` 메서드를 사용할 수 있습니다:

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

테이블의 모든 컬럼이 아니라 일부 컬럼만 조회하고 싶다면 `select` 메서드로 쿼리의 "select" 절을 직접 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드는 결과에서 중복을 제거할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있다면 `addSelect` 메서드로 select 절에 컬럼을 추가할 수 있습니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 (Raw Expressions)

때때로 쿼리에 임의의 문자열을 삽입하고 싶을 수 있습니다. 이럴 때는 `DB` 파사드의 `raw` 메서드를 사용해 raw 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 문자열로 바로 삽입되므로, SQL 인젝션 취약점이 생기지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 사용 대신, 쿼리의 다양한 부분에 raw 표현식을 삽입할 수 있는 아래 메서드들을 사용할 수 있습니다. **주의: Raw 표현식을 사용하는 쿼리에 대해서는 SQL 인젝션 방지 여부를 Laravel이 보장하지 않습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있으며, 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`, `orWhereRaw` 메서드는 쿼리에 raw "where" 절을 추가합니다. 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`, `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 사용할 수 있습니다. 마찬가지로 바인딩 배열을 두 번째 인수로 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절의 값으로 raw 문자열을 사용할 수 있습니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절의 값으로 raw 문자열을 지정할 수 있습니다:

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

쿼리 빌더는 쿼리에 조인 절을 추가할 때도 사용할 수 있습니다. 가장 기본적인 "inner join"을 하려면, 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. 첫 번째 인수는 조인할 테이블명이고, 나머지 인수는 조인의 컬럼 제약 조건을 지정합니다. 한 번의 쿼리에서 여러 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join" 또는 "right join"을 하고 싶다면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 사용 방법은 `join`과 동일합니다:

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

"cross join"을 사용하려면 `crossJoin` 메서드를 이용할 수 있습니다. Cross join은 첫 번째 테이블과 조인 테이블 간의 데카르트 곱(cartesian product)을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 조인 절도 지정할 수 있습니다. `join` 메서드의 두 번째 인수로 클로저를 전달하면, 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아 "join" 절의 제한 조건을 지정하게 해줍니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 절이 필요하다면, `JoinClause`에서 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 이 경우 두 컬럼이 아닌, 컬럼과 값 비교가 이루어집니다:

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

서브쿼리를 조인하고 싶다면, `joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용할 수 있습니다. 이 메서드들은 각각 서브쿼리, 테이블 별칭, 관련 컬럼을 정의하는 클로저를 인수로 받습니다. 아래 예시는 각 사용자 레코드에 해당 사용자의 가장 최근에 발행된 블로그 포스트의 `created_at` 타임스탬프도 함께 포함하는 결과를 조회합니다:

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
> Lateral 조인은 현재 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서만 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하여 서브쿼리와 함께 "lateral join"을 수행할 수 있습니다. 이 메서드들은 각각 서브쿼리와 테이블 별칭을 인수로 받습니다. 조인 조건은 반환된 서브쿼리의 `where` 절에서 지정해야 하며, lateral 조인은 각 행마다 평가되면서 서브쿼리 외부의 컬럼도 참조할 수 있습니다.

아래 예시는 사용자 목록을 조회하면서 각 사용자의 최근 3개 블로그 포스트도 함께 조회합니다. 각 사용자는 최대 3개의 결과(블로그 포스트)로 출력될 수 있습니다:

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
## 유니온 (Unions)

쿼리 빌더는 두 개 이상의 쿼리를 하나로 합치는 "union" 기능도 제공합니다. 예를 들어, 초기 쿼리를 만들고 `union` 메서드를 사용해 다른 쿼리와 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 외에도 `unionAll` 메서드를 제공하며, `unionAll`은 결과에서 중복을 제거하지 않습니다. `unionAll`의 사용법도 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용해 "where" 절을 쿼리에 추가할 수 있습니다. 가장 기본적인 호출은 세 개의 인수를 받습니다. 첫 번째 인수는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 모든 연산자 가능), 세 번째는 컬럼 값과 비교할 값입니다.

예를 들어, 아래 쿼리는 `votes` 컬럼 값이 `100`이고, `age` 컬럼이 `35`보다 큰 사용자들을 조회합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

동등(=) 비교만 할 경우에는 두 번째 인수로 값을 전달해도 되며, 이 경우 Laravel은 연산자를 `=`로 인식합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

여러 컬럼을 한 번에 조건으로 지정하려면, 연관 배열을 `where` 메서드에 전달할 수 있습니다:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

이미 언급했듯, 데이터베이스가 지원하는 모든 연산자를 사용할 수 있습니다:

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

조건의 배열을 `where` 함수에 전달할 수도 있습니다. 배열의 각 요소는 일반적으로 `where` 메서드에 전달하는 세 개의 인수를 포함한 배열입니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조하는 컬럼명을 사용자 입력값으로 받는 것은 절대 허용해서는 안 됩니다. (특히 "order by" 절의 컬럼명 등)

> [!WARNING]
> MySQL과 MariaDB는 문자열과 숫자 비교시 문자열을 자동으로 정수형식으로 변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 간주되어 예기치 않은 결과가 발생할 수 있습니다. 예를 들어, 테이블에 `secret` 컬럼 값이 `aaa`인 행이 있고, `User::where('secret', 0)`을 실행하면 그 행이 반환될 수 있습니다. 이런 현상을 막으려면 항상 쿼리 사용 전에 값의 타입을 명확히 변환하여 사용하세요.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드를 연속으로 체이닝하면 조건들이 `and` 연산자로 결합됩니다. 그러나 `or` 연산자로 조건을 결합하려면 `orWhere` 메서드를 사용하세요. 사용법은 `where`와 동일합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 묶어서 "or" 조건을 그룹화하려면, 첫 번째 인수로 클로저를 전달하면 됩니다:

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

위 코드는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 전역 스코프가 적용되는 상황에서 예기치 않은 동작을 방지하기 위해, 항상 `orWhere`는 그룹화해서 사용하는 것이 좋습니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`와 `orWhereNot` 메서드는 조건 그룹의 부정(NOT)을 적용할 수 있습니다. 아래 예시는 "clearance" 제품이나 가격이 10 미만인 상품을 제외한 결과를 조회합니다:

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

여러 컬럼에 동일한 쿼리 조건을 적용하고 싶을 때가 있습니다. 예를 들어, 지정한 컬럼 목록 중 "하나라도" 값이 특정 패턴과 일치하는 레코드를 조회하려면 `whereAny` 메서드를 사용합니다:

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

위 쿼리는 다음과 같은 SQL을 생성합니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

`whereAll` 메서드를 사용하면 지정한 컬럼 "모두"가 조건을 만족하는 레코드를 조회할 수 있습니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음 SQL을 만듭니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 지정한 컬럼 중 "어느 것도" 조건에 일치하지 않는 레코드를 조회합니다:

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

이 쿼리는 다음과 같이 변환됩니다:

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

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에서 JSON 컬럼 조회도 지원합니다. JSON 컬럼을 조회하려면 `->` 연산자를 사용하세요:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

`whereJsonContains`, `whereJsonDoesntContain` 메서드를 사용해 JSON 배열을 조회할 수도 있습니다:

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

또한, JSON 키가 포함되어 있거나 포함되어 있지 않은 결과만 조회하려면 `whereJsonContainsKey`, `whereJsonDoesntContainKey` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이로 조회하려면 `whereJsonLength` 메서드를 사용하세요:

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

`whereLike` 메서드는 문자열 패턴 매칭을 위해 "LIKE" 절을 쿼리에 추가합니다. 이 메서드는 데이터베이스 종류에 구애받지 않는 방식으로 문자열 검색 쿼리를 실행하며, 대소문자 구분 옵션도 설정할 수 있습니다. 기본적으로는 대소문자를 구분하지 않습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 통한 대소문자 구분 검색도 가능합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드를 사용하면 "or"절과 함께 LIKE 조건을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike` 메서드는 "NOT LIKE" 절을 추가합니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로, `orWhereNotLike` 메서드는 "or" 조건과 함께 NOT LIKE을 추가합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> SQL Server에서는 `whereLike`의 대소문자 구분 옵션이 현재 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 지정 컬럼의 값이 특정 배열에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 값이 배열에 포함되지 않는지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

배열 대신 쿼리 객체도 두 번째 인수로 넘길 수 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 코드의 SQL 변환 예:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 많은 integer 값을 쿼리에 바인딩하려면, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용해 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼의 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 값이 범위 밖에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 한 행 내에서 두 컬럼 값의 사이에 특정 컬럼 값이 위치하는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 위와 반대로, 두 값의 외부 범위에 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween`은 지정한 값이 한 행 내 두 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`은 값이 두 컬럼 값의 범위 밖에 있는지 확인합니다:

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼 값이 `NULL`인지 확인합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼 값이 `NULL`이 아닌지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값을 날짜와 비교합니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`는 특정 월과 비교합니다:

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay`는 월 중 특정 날과 비교합니다:

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`은 특정 연도와 비교합니다:

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`은 특정 시간과 비교합니다:

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`, `whereFuture` 메서드는 컬럼의 값이 과거인지 미래인지 판단합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture` 메서드는 현재 시점 포함 여부를 판단합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 지정 컬럼이 오늘/오늘 이전/오늘 이후인지 판별합니다:

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

`whereTodayOrBefore`, `whereTodayOrAfter`는 오늘도 포함하여 이전/이후를 판별합니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼이 같은지 비교합니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 넘길 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 개의 컬럼 비교를 배열로 넘길 수도 있습니다. 조건들은 `and`로 결합됩니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화 (Logical Grouping)

여러 "where" 절을 괄호로 묶어 논리적으로 그룹화해야 할 때가 있습니다. 특히 `orWhere`를 사용할 때는 항상 괄호로 묶는 것이 예측 가능한 쿼리 작동에 유리합니다. 이럴 때 `where`에 클로저를 전달하면 됩니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

클로저를 `where`에 넘기면, 쿼리 빌더는 제약 조건 그룹을 시작합니다. 클로저 내에서 추가 조건을 지정할 수 있습니다. 위 코드는 다음 SQL과 동일합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프가 붙은 경우 예기치 않은 동작을 방지하기 위해, 항상 `orWhere`는 그룹화해서 사용하는 것이 좋습니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" SQL 절을 작성할 수 있게 해줍니다. 이 메서드는 클로저를 받아, 클로저에서 쿼리 빌더 인스턴스를 받아 "exists" 절 내에 실행할 쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

클로저 대신 쿼리 객체를 직접 넘길 수도 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 예시 모두 다음 SQL을 생성합니다:

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

때로는 서브쿼리 결과와 값을 비교하는 "where" 절이 필요할 수 있습니다. 이럴 땐, 클로저와 값을 `where`에 넘기면 됩니다. 예시로, 다음 쿼리는 지정한 종류(type)의 최근 "membership"이 있는 모든 사용자를 조회합니다:

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

또는 컬럼과 서브쿼리를 비교하는 절이 필요하다면, 컬럼명, 연산자, 클로저를 전달하면 됩니다. 예를 들어, 전체 소득(Income) 기록에서 금액(amount)이 평균보다 적은 것을 찾을 수 있습니다:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 풀텍스트 Where 절

> [!WARNING]
> 풀텍스트 Where 절은 현재 MariaDB, MySQL, PostgreSQL만 지원됩니다.

`whereFullText`, `orWhereFullText` 메서드는 [풀텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 생성된 컬럼에 대한 풀텍스트 "where" 절을 추가합니다. 이 메서드들은 MariaDB, MySQL의 경우 `MATCH AGAINST` 구문 등 데이터베이스 특성에 맞는 SQL로 변환됩니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
### 벡터 유사도 절

> [!NOTE]
> 벡터 유사도 절은 현재 `pgvector` 확장 모듈이 설치된 PostgreSQL 연결에서만 지원됩니다. 벡터 컬럼 및 인덱스 정의는 [마이그레이션 문서](/docs/12.x/migrations#available-column-types)를 참고하세요.

`whereVectorSimilarTo` 메서드는 주어진 벡터에 대해 코사인 유사도를 기준으로 결과를 필터링하고, 관련도 순으로 정렬합니다. `minSimilarity` 임계값은 `0.0`(전혀 다름)부터 `1.0`(완벽히 동일) 사이의 값이어야 합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

벡터로 일반 문자열을 전달하면, Laravel이 [Laravel AI SDK](/docs/12.x/ai-sdk#embeddings)를 이용하여 자동으로 임베딩을 생성합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

기본적으로 `whereVectorSimilarTo`는 거리 순(유사도가 높은 것부터)으로 주문한 결과를 반환합니다. 주문(order) 동작을 끄고 싶을 때는 `order` 인수에 `false`를 전달하세요:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

더 세부적으로 제어가 필요하다면, `selectVectorDistance`, `whereVectorDistanceLessThan`, `orderByVectorDistance` 메서드를 각각 활용할 수 있습니다:

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
## 정렬, 그룹화, 리밋과 오프셋 (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드를 사용하면 결과를 지정 컬럼 값으로 정렬할 수 있습니다. 첫 번째 인수는 정렬할 컬럼명, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼 기준으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 생략하면 기본적으로 오름차순(asc)입니다. 내림차순으로 정렬하려면 두 번째 인자로 명시하거나, `orderByDesc`를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

또한 `->` 연산자를 사용하여 JSON 컬럼 내부의 값을 기준으로 정렬할 수도 있습니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드는 날짜 기준으로 손쉽게 결과를 정렬해줍니다. 기본적으로 `created_at` 컬럼값을 기준으로 하며, 다른 컬럼명을 넘겨줄 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드로 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 임의의 사용자를 하나 불러올 때 사용할 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거

`reorder` 메서드는 이전의 "order by" 절을 모두 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 호출 시 컬럼명과 방향을 넘기면 기존 "order by" 절을 전부 지우고 새로운 정렬 조건을 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

간단하게 내림차순 정렬만 하고 싶다면 `reorderDesc`를 사용할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화 (Grouping)

<a name="groupby-having"></a>
#### `groupBy`, `having` 메서드

`groupBy`, `having` 메서드를 사용해 결과를 그룹화할 수 있습니다. `having` 메서드는 `where`와 비슷한 형태로 사용합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드는 특정 값 범위에 해당하는 결과로 필터링할 때 사용합니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 컬럼을 그룹 기준으로 지정하고 싶다면 인수를 나열해 전달하면 됩니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 having 구문은 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### 리밋과 오프셋 (Limit and Offset)

`limit`, `offset` 메서드를 사용해 쿼리의 리턴 결과 개수 제한 또는 특정 개수 건너뛰기(Skip)가 가능합니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

때때로 특정 조건에서만 쿼리 절을 적용하고 싶을 수 있습니다. 예를 들어, 입력값이 주어진 경우에만 `where` 문을 추가하고 싶은 경우에는 `when` 메서드를 이용하면 됩니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`로 평가될 때만 클로저를 실행합니다. 만약 첫 번째 인수가 `false`라면, 클로저는 실행되지 않습니다. 위 예시에서 `role` 필드가 입력 데이터에 존재하고 참 값일 때만, 클로저 내부의 쿼리를 실행하게 됩니다.

세 번째 인수로 또 다른 클로저를 넘기면, 첫 번째 인수가 `false`일 때만 해당 클로저가 실행됩니다. 이를 활용하여 쿼리의 기본 정렬 방식을 동적으로 설정할 수도 있습니다:

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

쿼리 빌더는 `insert` 메서드를 제공하여 레코드를 데이터베이스 테이블에 삽입할 수 있습니다. `insert` 메서드는 컬럼명 및 값 배열을 인수로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면, 배열의 배열(각각이 하나의 레코드)을 전달하세요:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore`는 중복 등으로 에러가 발생해도 무시하고 삽입을 시도합니다. 이 메서드 사용 시, 중복 레코드 에러뿐만 아니라 데이터베이스 엔진에 따라 기타 에러도 무시될 수 있음을 주의하세요. 예를 들어, `insertOrIgnore`는 [MySQL의 strict 모드](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 하위 쿼리의 결과를 이용해 새 레코드를 삽입합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### 오토 인크리먼트 ID

테이블에 오토 인크리먼트 id가 있다면, `insertGetId` 메서드로 레코드를 삽입하고 바로 ID 값을 반환받을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서는 `insertGetId` 메서드가 오토 인크리먼트 컬럼명을 `id`로 가정합니다. 만약 다른 "시퀀스"에서 ID를 가져오고 싶다면, 두 번째 인수로 컬럼명을 지정하세요.

<a name="upserts"></a>
### 업서트(Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 새 값으로 갱신(update)합니다. 첫 번째 인수로는 삽입/수정할 값 배열, 두 번째 인수로는 테이블에서 레코드를 고유하게 식별하는 컬럼 배열, 세 번째 인수는 중복 레코드가 있다면 갱신할 컬럼 배열입니다:

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

위 쿼리는 두 레코드의 삽입을 시도합니다. 만약 `departure`, `destination` 컬럼 값이 동일한 레코드가 이미 존재한다면, 해당 레코드의 `price` 컬럼이 갱신됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 두 번째 인수의 컬럼에 "primary" 또는 "unique" 인덱스가 있어야 합니다. 또한, MariaDB와 MySQL 드라이버는 `upsert`의 두 번째 인수를 무시하고 항상 테이블의 "primary" 및 "unique" 인덱스를 기준으로 중복을 판단합니다.

<a name="update-statements"></a>
## Update 구문 (Update Statements)

레코드 삽입뿐만 아니라, 쿼리 빌더로 기존 레코드도 `update` 메서드로 갱신할 수 있습니다. 사용법은 `insert`와 유사하게 컬럼/값 쌍 배열을 넘기며, `update`는 영향을 받은 행의 개수를 반환합니다. `where`로 조건을 걸 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

해당하는 레코드가 있다면 갱신(update), 없으면 생성(insert)하려면 `updateOrInsert` 메서드를 사용합니다. 첫 번째 인수는 찾을 레코드의 조건 배열, 두 번째는 수정할 컬럼/값 쌍 배열입니다.

`updateOrInsert`는 첫 번째 인수의 컬럼/값 쌍으로 데이터베이스에서 레코드를 찾습니다. 있으면 두 번째 인수의 값으로 갱신, 없으면 두 인수의 값을 합쳐 새 레코드로 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

조건에 따라 업데이트/삽입 속성을 세밀하게 제어하고 싶다면, 두 번째 인수에 클로저를 줄 수도 있습니다:

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

JSON 컬럼을 업데이트할 때는 `->` 문법을 사용하여 JSON 객체 내부의 키를 선택적으로 수정할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소 연산

특정 컬럼의 값을 손쉽게 증가시키거나 감소시키는 메서드도 제공합니다. 두 메서드는 첫 번째 인수로 컬럼명을 받고, 두 번째 인수(선택적)로 증감할 수치(기본값 1)를 지정할 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 증감 연산과 동시에 다른 컬럼 값도 업데이트할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

여러 컬럼을 한 번에 증감하려면 `incrementEach`, `decrementEach` 메서드를 사용할 수 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문 (Delete Statements)

쿼리 빌더의 `delete` 메서드는 테이블의 레코드를 삭제할 때 사용합니다. `delete`는 삭제한 행의 수를 반환하며, "where" 절을 이용해 일부 레코드만 삭제할 수도 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더에는 "비관적 잠금(pessimistic locking)"을 구현하는 메서드도 있습니다. "공유 잠금(shared lock)"을 사용하려면 `sharedLock` 메서드를, "for update" 잠금을 쓰려면 `lockForUpdate` 메서드를 사용하세요:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는,

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금은 [트랜잭션](/docs/12.x/database#database-transactions) 안에서 사용하면 데이터 무결성을 더욱 안전하게 지킬 수 있습니다. 트랜잭션이 완료되기 전까지 해당 데이터는 다른 트랜잭션에서 변경할 수 없고, 실패 시 트랜잭션은 자동으로 롤백하며 잠금도 풀어줍니다:

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
## 재사용 가능한 쿼리 구성요소 (Reusable Query Components)

애플리케이션 곳곳에서 반복되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 활용해 재사용 가능한 객체로 분리할 수 있습니다. 아래는 동일한 목적의 쿼리가 두 번 등장하는 예시입니다:

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

여기서 목적지(destination) 필터링 로직을 공통 객체로 추출할 수 있습니다:

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

이제 쿼리 빌더의 `tap` 메서드를 이용해 이 객체를 쿼리에 적용할 수 있습니다:

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
#### 쿼리 파이프(Query Pipes)

`tap` 메서드는 항상 쿼리 빌더 객체를 반환합니다. 쿼리를 실제로 실행해 그 결과를 반환하는 객체로 추출하려면 `pipe` 메서드를 사용하세요.

예를 들어, 애플리케이션 전반에 걸쳐 [페이지네이션](/docs/12.x/pagination) 로직을 공유하고 싶을 때, 다음과 같은 쿼리 객체를 만들 수 있습니다. 아래 예시에서 `Paginate`는 쿼리 조건을 추가하는 것이 아니라 쿼리를 실행하고 페이지네이터를 반환합니다:

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

`pipe` 메서드를 사용하면 공유 페이지네이션 로직을 재사용할 수 있습니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리 빌더로 쿼리를 작성하는 중에 `dd` 및 `dump` 메서드를 사용하여 현재 쿼리 바인딩과 SQL을 출력할 수 있습니다. `dd`는 디버그 정보를 표시한 뒤 요청 처리를 중단하며, `dump`는 출력 후에도 요청 처리가 계속 진행됩니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`와 `ddRawSql` 메서드는 쿼리의 SQL문을 바인딩 값까지 모두 대입해 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```