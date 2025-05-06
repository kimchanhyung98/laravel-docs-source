# 데이터베이스: 쿼리 빌더

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크로 처리하기](#chunking-results)
    - [지연(lazy) 스트리밍](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Joins)](#joins)
- [유니온(Unions)](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any/All/None 절](#where-any-all-none-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가 Where 절](#additional-where-clauses)
    - [논리 그룹핑](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전문 검색 Where 절](#full-text-where-clauses)
- [정렬, 그룹핑, Limit, Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹핑](#grouping)
    - [Limit과 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [Upsert](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가/감소 연산](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 락킹](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 편리하고 유창한 인터페이스를 제공하여 데이터베이스 쿼리를 작성하고 실행할 수 있도록 해줍니다. 이 빌더를 사용해 애플리케이션의 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템에서 완벽하게 동작합니다.

Laravel의 쿼리 빌더는 PDO 파라미터 바인딩을 이용하여 SQL 인젝션 공격으로부터 앱을 보호합니다. 쿼리 바인딩에 전달되는 문자열을 따로 청소하거나 정제할 필요는 없습니다.

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서 "order by" 컬럼을 포함해 쿼리에 참조되는 컬럼 이름을 사용자 입력에 의해 결정하도록 해선 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 가져오기

`DB` 파사드에서 제공하는 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table` 메서드는 해당 테이블에 대한 유창한 쿼리 빌더 인스턴스를 반환하며, 여기에 추가적인 제약조건을 체이닝하고 마지막으로 `get` 메서드를 호출해 결과를 조회할 수 있습니다.

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

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체입니다. 각 컬럼 값은 객체의 프로퍼티로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel의 컬렉션은 데이터 매핑과 축약(reduce)에 매우 강력한 메서드를 제공합니다. 자세한 내용은 [컬렉션 문서](/docs/{{version}}/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 가져오기

데이터베이스 테이블에서 한 개의 행만 조회하려면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 일치하는 행이 없을 때 `Illuminate\Database\RecordNotFoundException` 예외를 발생시켜 404 HTTP 응답을 자동으로 반환하고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

행 전체가 필요하지 않고 특정 컬럼 값만 필요하다면 `value` 메서드를 사용해 직접 컬럼 값을 추출할 수 있습니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 이용해 단일 행을 가져오려면 `find` 메서드를 사용하세요.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 리스트 가져오기

특정 컬럼 값 목록이 담긴 `Illuminate\Support\Collection`을 얻고 싶다면 `pluck` 메서드를 사용하세요. 아래 예제에서는 사용자 title 목록을 조회합니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드에 두 번째 인수를 전달하여 결과 컬렉션의 키로 사용할 컬럼을 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크로 처리하기

수천 건의 데이터베이스 레코드를 다루어야 한다면, `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 한번에 작은 청크로 나눠서 클로저로 넘겨 처리할 수 있습니다. 예를 들어, 한 번에 100개의 레코드씩 `users` 테이블 전체를 처리하려면 다음과 같이 할 수 있습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 추가 청크 처리를 중단할 수 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크로 처리하면서 데이터베이스 레코드를 업데이트하는 경우, 결과가 예기치 않게 바뀔 수 있습니다. 청크 처리를 하면서 해당 레코드를 업데이트할 계획이라면 항상 `chunkById` 메서드를 사용하는 것이 가장 좋습니다. 이 메서드는 기본키 값에 따라 결과를 자동으로 페이지네이션합니다.

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

`chunkById` 또는 `lazyById` 메서드는 쿼리에 자체적으로 "where" 조건을 추가하므로, 직접 지정하는 조건들은 [논리적으로 그룹핑](#logical-grouping)해야 합니다.

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
> 청크 콜백 내부에서 레코드의 기본키나 외래키를 변경하는 경우 쿼리에 영향을 미칠 수 있습니다. 이로 인해 일부 레코드가 청크 결과에 포함되지 않을 수도 있습니다.

<a name="streaming-results-lazily"></a>
### 지연(lazy) 스트리밍

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행합니다. 하지만 콜백으로 청크를 넘기는 대신 [LazyCollection](/docs/{{version}}/collections#lazy-collections)을 반환하여 하나의 스트림처럼 결과를 다룰 수 있습니다.

```php
use Illuminate\Support\Facades.DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

청크 처리 시 조회한 레코드를 업데이트할 계획이라면, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 좋습니다. 이 메서드들은 기본키 기준으로 자동으로 페이지네이션합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복문 내에서 레코드를 업데이트 또는 삭제할 때, 기본키나 외래키 값을 변경하면 쿼리 결과에 영향을 미칠 수 있으니 주의하세요.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 메서드를 제공합니다. 원하는 쿼리를 구성한 뒤 이 메서드들을 호출할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

또한 조건절 등 다른 구문과 결합하여 집계값을 세밀하게 조정할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

특정 조건을 만족하는 레코드의 존재 여부만 확인하려면 `count` 대신 `exists` 및 `doesntExist` 메서드를 사용할 수 있습니다.

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

항상 테이블의 모든 컬럼을 조회할 필요는 없습니다. `select` 메서드를 사용하여 원하는 컬럼을 명시적으로 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드는 결과값의 중복을 제거할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 기존 select 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용할 수 있습니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

가끔 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. `DB` 파사드의 `raw` 메서드를 사용해 raw 문자열 표현식을 만들 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 문자열로 바로 쿼리에 삽입되므로, SQL 인젝션 취약점이 생기지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 사용 외에도 아래와 같은 메서드들을 사용해 쿼리의 다양한 부분에 raw 표현식을 삽입할 수 있습니다. **Raw 표현식이 포함된 쿼리는 SQL 인젝션으로부터 보호됨을 Laravel이 보장하지 않으니 반드시 주의하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw`는 `addSelect(DB::raw(...))` 대신 사용할 수 있으며, 두 번째 인수로 바인딩 배열을 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw` / `orWhereRaw`

`whereRaw`와 `orWhereRaw`는 쿼리에 raw "where" 절을 주입할 때 사용합니다. 바인딩 배열을 두 번째 인수로 받을 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw` / `orHavingRaw`

`havingRaw`, `orHavingRaw`는 "having" 절의 값으로 raw 문자열을 사용할 때 씁니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw`는 "order by" 절의 값을 raw 문자열로 지정합니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절의 값을 raw 문자열로 지정할 때 사용합니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Joins)

<a name="inner-join-clause"></a>
#### Inner Join 구문

쿼리 빌더에서 조인 구문도 추가할 수 있습니다. 기본적인 "inner join"은 쿼리 빌더 인스턴스의 `join` 메서드를 사용하는데, 첫 번째 인수는 조인할 테이블 이름, 나머지 인수들은 조인 조건을 나타냅니다. 한 쿼리에서 여러 테이블을 조인할 수도 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### Left Join / Right Join 구문

"inner join" 대신 "left join"이나 "right join"을 하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 메서드 시그니처는 `join`과 동일합니다.

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### Cross Join 구문

"cross join"을 수행하려면 `crossJoin` 메서드를 사용할 수 있습니다. cross join은 첫 번째 테이블과 두 번째 테이블 간의 데카르트 곱(Cartesian product)을 만듭니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 구문

더 복잡한 join 조건도 지정할 수 있습니다. `join`의 두 번째 인수로 클로저를 전달하면 됩니다. 해당 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아 "join" 절의 조건을 설정할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 구문을 사용하려면 `JoinClause` 인스턴스의 `where`와 `orWhere` 메서드를 사용할 수 있습니다. 이 메서드들은 두 컬럼을 비교하는 게 아니라, 컬럼과 값을 비교합니다.

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용해 쿼리에 서브쿼리를 조인할 수 있습니다. 이들 메서드는 서브쿼리, 테이블 별칭, 그리고 관련 컬럼을 정의하는 클로저를 인수로 받습니다. 아래 예제는 각 사용자의 최종 블로그 게시글 생성 시간도 함께 조회하는 방법입니다.

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
> Lateral join은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서만 지원합니다.

`joinLateral`, `leftJoinLateral` 메서드를 사용하여 서브쿼리와 lateral join을 수행할 수 있습니다. 이들 메서드는 서브쿼리와 별칭을 인수로 받으며, 조인 조건은 서브쿼리의 `where` 절에서 지정합니다. Lateral join은 각 행마다 평가되며, 서브쿼리 외부 컬럼도 참조할 수 있습니다.

이 예제는 사용자와 그 사용자의 최근 3개 블로그 포스트를 조회합니다. 각 사용자는 최대 3개의 행이 결과로 나옵니다.

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
## 유니온(Unions)

쿼리 빌더는 여러 쿼리를 "union"으로 합치는 것도 쉽게 할 수 있습니다. 예를 들어, 초기 쿼리를 만들고 `union` 메서드로 다른 쿼리와 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드와 더불어, 중복 결과를 제거하지 않는 `unionAll` 메서드도 있습니다. 시그니처는 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용해 "where" 절을 추가할 수 있습니다. 가장 기본적인 사용법은 세 개의 인자를 받으며, 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 비교할 값입니다.

예를 들어, 아래 쿼리는 `votes` 컬럼이 `100`이고 `age`가 35보다 큰 사용자를 조회합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의상, 컬럼 값이 특정 값인지(= 연산) 확인할 때는 두 번째 인수에 바로 값을 전달할 수 있습니다. Laravel이 자동으로 `=` 연산자를 추론합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

지원하는 연산자는 데이터베이스에 따라 다르며, 아래 예시처럼 다른 연산자도 사용할 수 있습니다.

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

여러 조건을 배열로 전달할 수도 있습니다. 배열의 각 요소는 세 개 인자가 담긴 배열이어야 합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않으므로, 쿼리의 컬럼 이름("order by" 포함)을 사용자 입력에 따라 동적으로 지정해서는 안 됩니다.

> [!WARNING]
> MySQL과 MariaDB는 문자열-숫자 비교에 대해 자동으로 타입 캐스팅을 수행합니다. 숫자가 아닌 문자열은 `0`으로 간주되어 예상치 못한 결과가 나올 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 경우 `User::where('secret', 0)` 쿼리가 해당 행을 반환할 수 있으니, 쿼리 사용 전에 값의 타입을 적절히 맞춰야 합니다.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드를 계속 체이닝하면 조건들은 `and` 연산으로 합쳐집니다. `orWhere` 메서드를 사용하면 조건들을 `or` 연산으로 연결할 수 있습니다. 사용법은 `where`와 동일합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호 내에 "or" 조건을 그룹화하고 싶으면, 첫 번째 인수로 클로저를 전달하세요.

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

위의 코드는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 예상치 못한 동작을 방지하려면 항상 `orWhere`는 그룹핑해서 사용해야 합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`와 `orWhereNot` 메서드는 쿼리 조건 그룹을 부정할 때 사용합니다. 예를 들어, 아래 쿼리는 할인 중이거나 가격이 10 미만인 상품을 제외합니다.

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

여러 컬럼에 동일한 조건을 손쉽게 적용하려면 `whereAny`, `whereAll`, `whereNone` 메서드를 사용할 수 있습니다.

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

`whereAll`은 모든 컬럼이 조건을 만족할 때 조회할 때 사용합니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone`은 지정 컬럼 중 어느 것도 조건에 해당하지 않을 때 조회할 때 사용합니다.

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

Laravel은 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+ 와 같이 JSON 컬럼타입을 지원하는 DB에서 JSON 컬럼 조회도 지원합니다. JSON 컬럼을 조회하려면 `->` 연산자를 사용하세요.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열을 조회할 땐 `whereJsonContains`를 이용하세요.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL을 사용한다면 값의 배열을 두 번째 인수로 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

배열 길이에 따라 조회하려면 `whereJsonLength` 메서드를 사용하세요.

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

`whereLike` 메서드는 LIKE 패턴 매칭을 위한 "LIKE" 절을 쿼리에 추가합니다. 데이터베이스에 상관없이 문자열 매칭 쿼리를 손쉽게 사용할 수 있으며, 대소문자 구분도 인자로 조정할 수 있습니다. 기본적으로는 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

대소문자 구분 검색을 하려면 `caseSensitive` 인자를 사용하세요.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`는 "or" 절과 함께 LIKE 조건을 추가할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 절을 추가합니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

`orWhereNotLike`도 동일하게 사용하세요.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> SQL Server에서는 `whereLike`의 대소문자 구분 검색이 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 지정한 컬럼 값이 배열 내에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 값이 배열에 포함되어 있지 않은지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn`의 두 번째 인수로 쿼리 객체도 전달할 수 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

이는 다음과 같은 SQL을 생성합니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 대용량 정수 바인딩 배열을 쿼리에 추가할 때는 `whereIntegerInRaw`, `whereIntegerNotInRaw`를 사용하면 메모리 사용량을 대폭 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값 바깥에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 컬럼 값이 같은 행의 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 값이 두 컬럼 값 바깥에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼 값이 `NULL`이 아닌지 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼의 날짜 값과 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`는 컬럼의 월 정보와 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay`는 월 중 일(day)과 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`는 컬럼의 연도와 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`은 시간 값과 비교할 때 사용합니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`와 `whereFuture`는 컬럼 값이 과거 또는 미래에 해당하는지 확인할 때 사용합니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`와 `whereNowOrFuture`는 지금 또는 그 이전/이후에 포함하는지 확인합니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 오늘, 오늘 이전, 오늘 이후 여부를 각각 판단합니다.

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

`whereTodayOrBefore`, `whereTodayOrAfter`도 유사하게 사용합니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼이 동일한지 비교합니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자도 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 컬럼 비교도 배열로 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹핑

여러 "where" 절을 괄호로 묶어 논리적으로 그룹핑해야 할 때가 있습니다. 특히 `orWhere`는 항상 괄호로 그룹핑하는 것이 좋습니다. 이럴 때는 `where` 메서드에 클로저를 전달하면 됩니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

클로저가 query builder 인스턴스를 받고, 그 안에 추가 제약조건을 구성해 그룹핑합니다. 위 예시는 아래 SQL로 변환됩니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프가 적용된 경우, `orWhere`는 항상 논리 그룹핑해서 사용해야 예기치 않은 동작을 피할 수 있습니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 SQL의 "where exists" 절을 작성할 수 있게 해줍니다. 클로저로 내부에 들어갈 쿼리를 지정할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는 클로저 대신 쿼리 객체를 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 예제 모두 아래 SQL을 생성합니다.

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

서브쿼리의 결과와 값을 비교하는 "where" 절을 만들고자 할 때가 있습니다. 예를 들어, 특정 유형의 최근 "membership"을 가진 사용자를 찾기 위해 아래와 같이 작성할 수 있습니다.

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

혹은 컬럼과 서브쿼리 결과를 비교하고자 할 때는, 컬럼, 연산자, 클로저를 차례로 전달하면 됩니다. 예를 들어, 평균보다 적은 금액의 소득 레코드를 찾으려면:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 검색 Where 절

> [!WARNING]
> 전문(Full Text) 검색 Where 절은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [Full Text 인덱스](/docs/{{version}}/migrations#available-index-types)가 설정된 컬럼에서 전문 검색을 할 때 사용합니다. Laravel이 DBMS별로 알맞은 SQL로 변환해줍니다(MariaDB, MySQL은 `MATCH AGAINST`).

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹핑, Limit, Offset

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy`는 쿼리 결과를 특정 컬럼 기준으로 정렬할 때 사용합니다. 첫 번째 인수는 컬럼명, 두 번째 인수는 정렬 방향(`asc`, `desc`)입니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼으로 정렬할 때는 `orderBy`를 여러 번 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest`와 `oldest` 메서드

`latest`, `oldest`를 사용하면 손쉽게 날짜별로 정렬할 수 있습니다. 기본적으로는 `created_at` 컬럼 기준이며, 임의의 컬럼을 지정할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder`는 결과를 무작위로 정렬합니다. 예를 들어 임의의 사용자를 조회할 때 사용합니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거

`reorder` 메서드는 이전에 적용된 모든 "order by" 조건을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder`에 컬럼과 방향을 전달하면 기존 order를 모두 제거하고 새 정렬을 지정할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹핑

<a name="groupby-having"></a>
#### `groupBy` 와 `having` 메서드

`groupBy`와 `having` 메서드는 쿼리 결과를 그룹핑할 때 사용합니다. `having`의 시그니처는 `where`와 유사합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween`을 사용하면 결과가 특정 범위 내에 있을 때 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 컬럼으로 그룹핑하려면 인수를 여러 개 전달하면 됩니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 having 문은 [havingRaw](#raw-methods) 참조.

<a name="limit-and-offset"></a>
### Limit과 Offset

<a name="skip-take"></a>
#### `skip`, `take` 메서드

`skip`과 `take`를 이용해 쿼리 결과 개수를 제한하거나 지정 개수만큼 건너뛸 수 있습니다.

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

동등한 기능의 `limit`, `offset` 메서드도 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

특정 조건에 따라 쿼리절을 적용하고 싶을 때가 있습니다. 예컨대, 입력값이 있을 때만 `where` 구문을 추가하려면 `when` 메서드를 사용하세요.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when`은 첫 번째 인수가 true일 때만 클로저를 실행합니다. false면 실행하지 않습니다. 위 예시에서는 `role` 필드가 true로 평가될 때만 클로저가 실행됩니다.

세 번째 인수로 클로저를 전달하면, 첫 인수가 false일 때만 실행됩니다. 예를 들어 기본 정렬을 설정하고 싶다면:

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
## Insert 구문

쿼리 빌더의 `insert` 메서드를 이용해 테이블에 레코드를 삽입할 수 있습니다. `insert`는 컬럼명과 값을 담은 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

배열의 배열을 넘기면 여러 행을 한 번에 삽입할 수 있습니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore`는 삽입 중 오류가 발생해도 무시하고 계속 진행합니다. 이때, 중복인 레코드 오류와 DB 엔진에 따라 다른 오류도 무시됩니다. 예컨대 MySQL의 strict 모드도 우회됩니다. 자세한 내용은 [MySQL 공식 문서](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 참고하세요.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing`은 서브쿼리 결과를 활용하여 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동증가 ID

테이블이 auto-increment id 컬럼을 갖고 있다면, `insertGetId`로 레코드를 삽입하면서 바로 그 id를 반환받을 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서는 `insertGetId`가 기본적으로 `id` 컬럼에서 auto-increment 값을 조회합니다. 다른 시퀀스 컬럼을 사용하고 싶으면 두 번째 인수로 컬럼명을 넘기세요.

<a name="upserts"></a>
### Upsert

`upsert` 메서드는 없는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 값으로 갱신합니다. 첫 인수는 삽입/업데이트할 값 배열, 두 번째는 테이블에서 레코드를 고유하게 식별할 컬럼 목록, 세 번째는 이미 존재하는 경우 변경할 컬럼 배열입니다.

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

위 예시에서 Laravel은 두 개의 레코드를 삽입하려고 시도합니다. 하지만 같은 `departure`, `destination` 값의 레코드가 이미 존재하면 해당 레코드의 `price` 컬럼만 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert`의 두 번째 인수 컬럼에 "primary" 또는 "unique" 인덱스가 필요합니다. MariaDB, MySQL은 이 인수를 무시하고, 테이블의 기본키/유니크 인덱스로만 기존 레코드를 판별합니다.

<a name="update-statements"></a>
## Update 구문

쿼리 빌더를 사용해 기존 레코드도 업데이트할 수 있습니다. `update`는 컬럼과 값 쌍의 배열을 인수로 받으며, 영향을 받은 행 개수를 반환합니다. `where` 등 조건절로 제한할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update or Insert

기존 레코드를 업데이트하고, 없으면 새로 삽입하고 싶을 땐 `updateOrInsert`를 사용하세요. 조건 배열과 업데이트/삽입할 값 배열을 각각 전달합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

존재하는 레코드와 새로운 레코드 각각에 대해 삽입 및 업데이트 내용을 다르게 설정하려면 클로저를 전달할 수도 있습니다.

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

JSON 컬럼을 업데이트할 때는 `->` 구문을 써서 JSON 객체 내 특정 키만 갱신할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가/감소 연산

특정 컬럼의 값을 증가시키거나 감소시키는 편리한 메서드가 있습니다. 최소 1개의 인수(조작할 컬럼명)를 받고, 두 번째 인수로 증가/감소시킬 수치를 줄 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 다른 컬럼도 동시에 업데이트할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

`incrementEach`, `decrementEach`로 여러 컬럼을 한 번에 증가/감소시킬 수도 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문

쿼리 빌더의 `delete` 메서드를 이용해 레코드를 삭제할 수 있습니다. 영향을 받은 행 개수를 반환합니다. 먼저 "where" 절로 대상을 제한할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 락킹

쿼리 빌더에는 `select` 문 실행 시 "비관적 락킹"을 위한 메서드도 포함되어 있습니다. "공유 락"으로 실행하려면 `sharedLock` 메서드를 사용하세요. 공유 락은 트랜잭션이 완료될 때까지 선택한 행의 수정을 막습니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 `lockForUpdate`를 사용하면 "for update" 락이 설정되어, 해당 레코드가 수정되거나 타 공유 락으로 선택되는 것도 막을 수 있습니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

권장사항은 [트랜잭션](/docs/{{version}}/database#database-transactions) 내부에서 비관적 락을 사용하는 것입니다. 이렇게 하면 트랜잭션 도중 조회된 데이터가 변경되지 않고, 실패 시에는 자동으로 롤백 및 락 해제가 이뤄집니다.

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

애플리케이션 곳곳에서 반복되는 쿼리 로직이 있다면 빌더의 `tap` 및 `pipe` 메서드를 사용해 재사용 가능한 객체로 분리할 수 있습니다. 예를 들어, 아래와 같이 동일한 필터링 로직이 여러 쿼리에 반복된다면

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

아래처럼 destination 필터만 객체로 분리해 재사용할 수 있습니다.

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

이제 쿼리 빌더의 `tap` 메서드로 해당 객체를 적용하면 됩니다.

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

`tap` 메서드는 항상 쿼리 빌더 인스턴스를 반환합니다. 쿼리를 실행하여 다른 값을 반환하는 객체를 추출하고 싶다면 `pipe`를 사용하세요.

예를 들어, 아래처럼 페이지네이션 로직을 담은 쿼리 객체가 있다면,  

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

빌더의 `pipe` 메서드를 활용해 아래와 같이 사용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리 작성 중 `dd`와 `dump` 메서드로 SQL과 바인딩 값을 출력해 디버깅할 수 있습니다. `dd`는 정보를 출력하고 실행을 중단하며, `dump`는 출력 후 요청이 계속 진행됩니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`, `ddRawSql` 메서드를 호출하면 바인딩 값을 치환한 실제 SQL을 바로 출력할 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
