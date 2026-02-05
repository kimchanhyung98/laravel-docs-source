# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 게으르게 스트리밍하기](#streaming-results-lazily)
    - [집계 함수 사용하기](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식 사용하기](#raw-expressions)
- [조인(Join)](#joins)
- [합집합(Unions)](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All / None 절](#where-any-all-none-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가적인 Where 절](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전체 텍스트 Where 절](#full-text-where-clauses)
- [정렬, 그룹화, Limit 및 Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [Upserts](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더(Query Builder)는 데이터베이스 쿼리를 생성하고 실행하는 데 편리하면서도 유연한 인터페이스를 제공합니다. 이 쿼리 빌더는 애플리케이션에서 대부분의 데이터베이스 작업에 사용할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템에서 완벽하게 동작합니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩(Parameter Binding)을 사용하여, SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호합니다. 쿼리 빌더에 전달하는 문자열을 별도로 정제하거나 세척할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명을 바인딩하는 것을 지원하지 않습니다. 따라서 사용자 입력으로 쿼리에서 참조할 컬럼명(예: "order by" 컬럼 등)이 결정되도록 해서는 절대 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회

`DB` 파사드의 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 유연한 쿼리 빌더 인스턴스를 반환합니다. 쿼리 빌더 인스턴스를 통해 다양한 조건을 체이닝할 수 있으며, 마지막에 `get` 메서드를 호출하여 결과를 조회합니다.

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

`get` 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 쿼리 결과의 각 행은 PHP의 `stdClass` 객체 형태로 포함됩니다. 각 컬럼 값은 객체의 속성처럼 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel의 컬렉션에는 데이터를 매핑하거나 축소(리듀스)할 수 있는 강력한 메서드가 다양하게 제공됩니다. 컬렉션에 관한 자세한 내용은 [컬렉션 문서](/docs/master/collections)를 참조하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 또는 컬럼 조회

데이터베이스 테이블에서 단일 행만 조회하고 싶다면, `DB` 파사드의 `first` 메서드를 이용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

특정 조건에 맞는 행이 없으면 `Illuminate\Database\RecordNotFoundException`를 발생시켜 예외를 던지고 싶다면, `firstOrFail` 메서드를 사용할 수 있습니다. `RecordNotFoundException`이 처리되지 않으면, 클라이언트에게 404 HTTP 응답이 자동으로 반환됩니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없이 하나의 값만 뽑아오고 싶을 때는 `value` 메서드를 사용합니다. 이 메서드는 해당 컬럼의 값을 바로 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하고 싶다면, `find` 메서드를 사용할 수 있습니다.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값의 목록 조회

단일 컬럼의 값들만 `Illuminate\Support\Collection` 형태로 받고 싶을 땐, `pluck` 메서드를 이용합니다. 아래 예시에서는 사용자들의 직함(title)을 컬렉션으로 추출합니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck`의 두 번째 인수로 컬렉션의 키로 사용할 컬럼명을 지정할 수 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기

수천 개 이상의 데이터베이스 레코드를 다루어야 할 경우, `DB` 파사드에서 제공하는 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 작은 단위로 나누어 한 번에 일정 개수씩 조회하며, 각각의 청크를 콜백에 전달하여 효율적으로 처리할 수 있습니다. 아래는 전체 `users` 테이블을 100개씩 청크로 가져오는 예시입니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

콜백에서 `false`를 반환하면 이후 청크 처리가 중단됩니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크로 가져온 레코드를 업데이트할 경우, 예상치 못한 방식으로 청크 내용이 달라질 수 있습니다. 조회한 데이터를 청크로 나누면서 동시에 업데이트할 계획이라면, 항상 `chunkById` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드는 레코드의 기본 키를 기준으로 자동으로 결과를 페이지네이션합니다.

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

`chunkById`와 `lazyById` 메서드는 쿼리에 자체적으로 "where" 조건을 추가하므로, 보통 [논리적으로 그룹화](#logical-grouping)된 조건을 클로저 내부에 작성하는 것이 좋습니다.

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
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제할 때, 기본 키 또는 외래 키가 변경되면 청크 쿼리에 영향을 줄 수 있습니다. 그 결과, 일부 레코드가 청크 결과에 포함되지 않을 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 게으르게 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백으로 전달하는 것이 아니라 [LazyCollection](/docs/master/collections#lazy-collections)을 반환합니다. 이를 통해 결과 전체를 하나의 스트림처럼 다룰 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

마찬가지로, 반복 중에 레코드를 업데이트할 계획이라면 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 안전합니다. 이들 메서드는 기본 키를 기준으로 자동 페이지네이션합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 중 레코드를 업데이트하거나 삭제하면, 기본 키 또는 외래 키 변경이 쿼리 결과에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 결과에 포함되지 않을 수 있습니다.

<a name="aggregates"></a>
### 집계 함수 사용하기

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 함수를 제공합니다. 쿼리를 작성한 후 이러한 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

다른 조건문과 결합하여 집계 값을 정밀하게 산출할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

쿼리 조건에 해당하는 레코드가 존재하는지 확인하려면, `count` 대신 `exists`나 `doesntExist` 메서드를 사용할 수 있습니다.

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

항상 모든 컬럼을 조회할 필요는 없습니다. `select` 메서드를 사용하면 쿼리에 필요한 컬럼만 선택적으로 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드는 쿼리 결과를 중복 없이 반환하도록 강제합니다.

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 기존 Select 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용하면 됩니다.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 사용하기 (Raw Expressions)

쿼리 내에 임의 문자열을 삽입해야 할 경우, `DB` 파사드의 `raw` 메서드를 사용하여 raw 문자열 표현식을 생성할 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 쿼리에 문자열로 그대로 삽입됩니다. 따라서 SQL 인젝션 취약점이 발생하지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 관련 메서드

`DB::raw`를 사용하는 대신, 쿼리의 다양한 부분에 raw 표현식을 삽입할 수 있도록 다음 메서드들도 사용할 수 있습니다. **Raw 표현식을 사용할 경우, SQL 인젝션 방지가 보장되지 않으니 각별한 주의가 필요합니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw`는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 옵션으로 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 쿼리의 "where" 절에 raw 구문을 삽입합니다. 이 메서드들도 마찬가지로 두 번째 인수로 바인딩 배열을 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 및 `orHavingRaw` 메서드는 "having" 절의 값으로 raw 문자열을 지정할 수 있습니다. 마찬가지로 바인딩 배열을 두 번째 인수로 전달 가능합니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 raw 문자열을 삽입할 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 사용할 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Join) (Joins)

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더에서도 조인 절을 추가할 수 있습니다. 기본 "inner join"을 수행하려면, 쿼리 빌더 인스턴스에서 `join` 메서드를 사용합니다. 첫 번째 인수는 조인할 테이블명, 나머지 인수는 조인의 컬럼 조건입니다. 한 쿼리 내에 여러 테이블을 조인할 수도 있습니다.

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

"inner join" 대신 "left join" 또는 "right join"을 하고 싶다면, 각각 `leftJoin`, `rightJoin` 메서드를 사용하면 됩니다. 메서드 시그니처는 `join`과 동일합니다.

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

`crossJoin` 메서드를 사용하면 "cross join(교차 조인)"을 수행할 수 있습니다. 이는 두 테이블의 카테시안 곱(Cartesian Product)을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 조인 조건이 필요하다면, `join`의 두 번째 인수로 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 전달받으며, 그 안에서 조인 조건을 자유롭게 설정할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인 조건에 "where" 조건을 추가하고 싶다면 `JoinClause` 인스턴스의 `where`와 `orWhere` 메서드를 사용할 수 있습니다. 이 경우 두 컬럼이 아닌, 컬럼 대 값의 비교가 이뤄집니다.

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면, 쿼리를 서브쿼리로 조인할 수 있습니다. 각 메서드는 3개의 인수를 받습니다: 서브쿼리, 테이블 별칭, 그리고 연관 컬럼을 정의하는 클로저입니다. 아래 예시는 각 사용자 레코드에 해당 유저가 게시한 최신 블로그 포스트의 `created_at` 타임스탬프를 포함하도록 조회합니다.

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
> Lateral 조인은 현재 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서 지원됩니다.

`joinLateral` 및 `leftJoinLateral` 메서드를 사용하면, 서브쿼리와 "lateral join"을 수행할 수 있습니다. 각 메서드는 2개의 인수(서브쿼리와 별칭)를 받습니다. 조인 조건은 서브쿼리 내의 `where` 절에서 지정해야 합니다. Lateral 조인은 각 행마다 평가되며, 서브쿼리 외부의 컬럼도 참조할 수 있습니다.

아래 예시는 각 사용자의 최대 세 개의 최신 블로그 포스트를 포함하여 결과를 조회합니다. 조인 조건은 서브쿼리 내 `whereColumn`을 사용해 현재 사용자 행을 참조합니다.

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
## 합집합(Unions) (Unions)

쿼리 빌더는 두 개 이상의 쿼리를 "union"으로 합칠 수 있는 편리한 메서드를 제공합니다. 예를 들어, 초기 쿼리를 생성한 뒤 `union` 메서드로 추가 쿼리와 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 외에도, `unionAll` 메서드도 제공합니다. `unionAll`로 합쳐진 쿼리는 중복된 결과가 제거되지 않습니다. `unionAll` 메서드의 사용법은 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용해 "where" 절을 쿼리에 추가할 수 있습니다. 가장 기본적인 사용은 세 개의 인수(컬럼명, 연산자, 비교값)를 받습니다.

아래 쿼리는 `votes` 컬럼이 `100`이고, `age` 컬럼이 `35`보다 큰 사용자들을 조회합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

간편하게 `=` 연산자를 쓰고 싶다면 값만 두 번째 인수로 전달해도 됩니다. 그러면 Laravel이 `=` 연산자를 자동으로 사용합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

여러 컬럼에 대해 한번에 조건을 주고 싶다면, 연관 배열을 `where`의 인수로 넘길 수 있습니다.

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

앞서 설명했듯, 데이터베이스 시스템에서 지원하는 모든 연산자를 사용할 수 있습니다.

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

조건 배열의 각 요소에 3개 요소(컬럼명, 연산자, 값)가 들어간 배열을 넣어 여러 조건을 처리할 수도 있습니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명을 바인딩할 수 없습니다. 따라서 쿼리에 참조하는 컬럼명이 사용자 입력에 의해 결정되면 안 됩니다. ("order by" 컬럼 등 포함)

> [!WARNING]
> MySQL과 MariaDB에서는 문자열-숫자 비교 시 문자열을 숫자로 자동 변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되어 예기치 않은 결과가 나올 수 있습니다. 예를 들어, 테이블에 `secret` 컬럼이 `aaa`이고, `User::where('secret', 0)`을 실행하면 해당 행이 조회됩니다. 이를 방지하려면 쿼리 전에 반드시 값의 타입을 명확히 맞춰야 합니다.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드들을 체이닝하면 각 "where" 절이 `and`로 이어집니다. 그러나 `orWhere`를 사용하면, 쿼리에 `or`로 절을 추가할 수 있습니다. `orWhere` 역시 `where`와 동일한 인수를 받습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 "or" 조건을 묶고 싶다면, `orWhere`의 첫 번째 인수로 클로저를 넘기면 됩니다.

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

위 예시의 SQL은 다음과 같이 생성됩니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 피하려면, 항상 `orWhere`를 그룹화할 것을 권장합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`과 `orWhereNot` 메서드는 쿼리 조건 그룹을 부정할 때 사용할 수 있습니다. 예를 들어, 다음 쿼리는 특가 상품이거나 가격이 10보다 작은 상품을 제외시킵니다.

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

같은 조건을 여러 컬럼에 동시에 적용해야 할 때가 있습니다. 예를 들어, 특정 값이 여러 컬럼 중 하나에라도 포함된 레코드를 모두 조회하고 싶다면, `whereAny` 메서드를 사용할 수 있습니다.

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

비슷하게, `whereAll` 메서드는 여러 컬럼이 모두 주어진 조건을 만족하는 레코드를 조회합니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

이 쿼리는 다음의 SQL을 만듭니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 여러 컬럼 중 어느 것도 조건을 만족하지 않는 레코드를 조회합니다.

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

생성되는 SQL:

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

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)의 JSON 컬럼을 직접 조회할 수 있습니다. 조회 시에는 `->` 연산자를 사용합니다.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

`whereJsonContains` 및 `whereJsonDoesntContain` 메서드를 사용해 JSON 배열을 조회할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL 데이터베이스에서는 값 배열을 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한, JSON 키의 존재 여부를 검사하려면 `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이를 조건으로 조회할 때는 `whereJsonLength` 메서드를 사용합니다.

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```

<a name="additional-where-clauses"></a>
### 추가적인 Where 절

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

`whereLike` 메서드는 패턴 매칭을 위한 "LIKE" 절을 쿼리에 추가합니다. 이 메서드들은 데이터베이스에 상관없이 문자열 매칭 쿼리를 사용할 수 있으며, 기본적으로 대소문자 구분 없이 검사합니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수를 통해 대소문자 구분 검색을 활성화할 수 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`는 "or"와 함께 LIKE 조건을 추가합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 조건으로 부정 패턴 매칭 쿼리를 추가합니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

마찬가지로 `orWhereNotLike`는 "or"와 함께 "NOT LIKE" 조건을 추가합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색(caseSensitive)은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 특정 컬럼의 값이 지정한 배열 내에 있는지를 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 컬럼의 값이 주어진 배열에 포함되지 않아야 함을 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn`의 두 번째 인수로 쿼리 객체를 전달할 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 쿼리는 다음 SQL이 생성됩니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 대용량의 정수 배열을 바인딩해야 할 때는 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼의 값이 두 값 사이에 있는지를 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼의 값이 두 값 범위 밖에 있는지를 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 컬럼의 값이 같은 행의 두 컬럼 사이에 있는지를 검사합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 컬럼의 값이 같은 행의 두 컬럼 범위 밖에 있는지를 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween`은 주어진 값이 같은 행 내의 두 컬럼 값 사이에 있는지를 검사합니다.

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`은 값이 두 컬럼 값 범위 밖에 있는지를 검사합니다.

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 컬럼 값이 `NULL`임을 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼 값이 `NULL`이 아님을 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 컬럼 값을 특정 날짜와 비교합니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`는 컬럼 값을 특정 달(month)과 비교합니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay`는 컬럼 값을 특정 일(day)과 비교합니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`는 컬럼 값을 특정 연도와 비교합니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`은 컬럼 값을 특정 시간과 비교합니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`, `whereFuture`는 컬럼 값이 과거/미래에 해당하는지 확인합니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture`는 현재 시점을 포함하여 과거/미래를 검사합니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 각각 오늘/오늘 이전/오늘 이후인지 확인합니다.

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

`whereTodayOrBefore`, `whereTodayOrAfter`는 오늘을 포함해 이전/이후인지 확인합니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn` 메서드는 두 컬럼 값이 같은지를 비교합니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 추가로 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

컬럼 비교 조건의 배열을 넘겨서 여러 컬럼을 and로 비교할 수 있습니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

여러 "where" 절을 괄호로 묶어 논리적 그룹을 만드는 것이 필요할 때가 있습니다. 특히 `orWhere` 메서드는 항상 괄호로 그룹핑하는 것이 예기치 않은 동작을 방지할 수 있어 좋습니다. 클로저를 `where`에 전달하면 그룹핑을 시작할 수 있습니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위와 같이 클로저를 `where`에 전달하면 조건 그룹이 쿼리의 괄호로 묶입니다. 생성되는 SQL 예시는 다음과 같습니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 글로벌 스코프 적용 시 예기치 않은 쿼리 동작을 방지하려면, 항상 `orWhere` 호출 시 그룹화를 하는 것이 좋습니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" SQL 절을 작성할 때 사용합니다. 이 메서드는 클로저를 인수로 받아, 해당 클로저 내부에서 쿼리 빌더 인스턴스로 exists 절 안에 들어갈 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

클로저 대신 쿼리 객체를 직접 넘길 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 예시 모두 다음의 SQL을 생성합니다.

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

때로는 "where" 절에서 서브쿼리 결과를 값과 비교해야 할 때가 있습니다. 이럴 땐 `where`에 클로저와 값을 함께 전달하면 됩니다. 아래 예시는 최근에 특정 유형의 "membership"을 가진 모든 사용자를 조회하는 쿼리입니다.

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

혹은 컬럼 값을 서브쿼리 결과와 비교해야 한다면, 컬럼, 연산자, 그리고 클로저 세 개를 `where`에 전달하면 됩니다. 예를 들어, 금액이 평균보다 작은 모든 수입(Income)을 조회하려면 다음과 같이 합니다.

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
> 전체 텍스트 Where 절은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [전체 텍스트 인덱스](/docs/master/migrations#available-index-types)가 활성화된 컬럼에 전체 텍스트 "where" 절을 추가합니다. 이 메서드들은 데이터베이스에 맞게 SQL로 변환됩니다. 예를 들어 MariaDB/MySQL에서는 `MATCH AGAINST` 구문이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, Limit 및 Offset (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 결과를 특정 컬럼 기준으로 정렬하게 합니다. 첫 번째 인수는 정렬할 컬럼명, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼으로 정렬하려면 `orderBy`를 여러 번 반복해서 호출하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 기본값이 오름차순이며, 내림차순으로 정렬하려면 두 번째 인수를 지정하거나 `orderByDesc`를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

또한 `->` 연산자를 이용해 JSON 컬럼 내부의 값을 기준으로 정렬할 수도 있습니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드는 날짜 기준으로 손쉽게 정렬이 가능합니다. 기본적으로 `created_at` 컬럼을 기준으로 정렬됩니다. 원하는 컬럼명을 전달할 수도 있습니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder` 메서드는 쿼리 결과를 임의로 랜덤하게 정렬할 수 있습니다. 예를 들어, 무작위로 사용자를 한 명 가져오려면 다음과 같이 합니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 삭제

`reorder` 메서드는 이전에 적용한 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

컬럼과 정렬 방향을 전달하면, 기존 모든 "order by"를 제거하고 새로운 정렬을 적용할 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

편의를 위해 `reorderDesc` 메서드를 사용하면 내림차순 정렬로 쉽게 바꿀 수 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화 (Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`와 `having` 메서드는 쿼리 결과를 그룹짓는 데 사용합니다. `having`의 사용법은 `where`와 비슷합니다.

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드를 사용해 특정 범위에 들어가는 결과만 필터링할 수 있습니다.

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy`에 여러 인수를 넘겨 여러 컬럼으로 그룹화할 수 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 having 구문이 필요하다면 [havingRaw](#raw-methods) 메서드를 참조하세요.

<a name="limit-and-offset"></a>
### Limit 및 Offset

`limit`과 `offset` 메서드를 사용하면 쿼리 결과 개수를 제한하거나, 특정 개수만큼 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

입력값이 있을 때만 쿼리 절을 적용하는 등, 조건에 따라 쿼리의 일부만 추가하고 싶을 때가 있습니다. 이럴 때는 `when` 메서드를 사용하면 됩니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 참일 때만 클로저를 실행합니다. 거짓인 경우 클로저가 실행되지 않습니다. 위 예시에서는, 요청에 `role` 필드가 있을 때에만 해당 쿼리 절이 삽입됩니다.

`when` 메서드의 세 번째 인수로 클로저를 하나 더 전달할 수 있습니다. 이 클로저는 첫 번째 인수가 거짓인 경우에만 실행됩니다. 아래 예시는 이 기능을 이용해 기본 정렬 순서를 설정하는 방법을 보여줍니다.

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

쿼리 빌더는 `insert` 메서드를 통해 데이터베이스 테이블에 레코드를 삽입할 수 있습니다. `insert`는 컬럼명과 값의 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 이중 배열(배열의 배열)을 전달하면 됩니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드 삽입 중 오류가 발생해도 해당 오류를 무시합니다. 이 메서드를 사용할 경우, 중복 레코드 등 일부 오류가 무시될 수 있고, 데이터베이스 엔진에 따라 다른 오류도 무시될 수 있습니다. 예를 들어, `insertOrIgnore`는 [MySQL strict mode를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리로 결정된 데이터를 사용해 레코드를 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id 컬럼이 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입한 뒤 ID 값을 바로 가져올 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서는 `insertGetId`가 자동 증가 컬럼 이름을 `id`로 가정합니다. 다른 시퀀스에서 ID를 조회하려면 두 번째 인수로 컬럼명을 직접 전달해야 합니다.

<a name="upserts"></a>
### Upserts

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 값으로 업데이트합니다. 첫 번째 인수는 삽입/업데이트할 값 배열이며, 두 번째 인수는 레코드를 고유하게 식별할 컬럼(여러 컬럼 가능) 목록입니다. 세 번째 인수는 일치하는 레코드가 이미 있을 때 업데이트할 컬럼 목록입니다.

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

위 예시에서, `departure`와 `destination` 컬럼 값이 동일한 레코드가 이미 있으면 해당 레코드의 `price` 만 업데이트됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는, `upsert` 메서드의 두 번째 인수 컬럼들이 반드시 "primary" 또는 "unique" 인덱스를 가져야 합니다. 또한, MariaDB와 MySQL 드라이버에서는 두 번째 인수로 지정한 컬럼을 무시하고, 항상 테이블의 "primary" 및 "unique" 인덱스를 사용합니다.

<a name="update-statements"></a>
## Update 구문 (Update Statements)

기존 레코드도 쿼리 빌더의 `update` 메서드를 통해 쉽게 변경할 수 있습니다. `insert`와 마찬가지로 컬럼명과 값을 담은 배열을 인수로 받으며, 반환 값은 영향을 받은 행(row)의 개수입니다. 필요한 경우 `where`로 조건을 지정할 수 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

동일 조건의 레코드가 있을 때는 업데이트, 없으면 새로 생성하고 싶을 때는 `updateOrInsert` 메서드를 사용할 수 있습니다. 이 메서드는 두 개의 인수(조건 배열, 업데이트할 컬럼 배열)를 받습니다.

`updateOrInsert`는 첫 번째 인수로 전달한 컬럼-값 쌍을 이용해 레코드를 찾고, 있으면 두 번째 인수 값으로 업데이트, 없으면 두 인수를 병합한 값으로 새로 삽입합니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

업데이트/삽입 데이터(속성)를 동적으로 지정하고 싶다면 클로저를 인수로 전달할 수 있습니다. 이때 클로저는 존재여부(`$exists`)에 따라 값을 반환합니다.

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

JSON 컬럼을 업데이트할 때는 `->` 문법을 사용해 JSON 객체 내의 키를 변경할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

쿼리 빌더에서는 주어진 컬럼의 값을 간단히 증가시키거나 감소시키는 `increment`, `decrement` 메서드를 제공합니다. 첫 번째 인수는 수정할 컬럼이며, 두 번째 인수로 증가/감소시킬 값을 지정할 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 증가 또는 감소와 동시에 다른 컬럼도 업데이트할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

여러 컬럼을 동시에 증가 또는 감소시키려면 `incrementEach`, `decrementEach` 메서드를 사용합니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문 (Delete Statements)

쿼리 빌더의 `delete` 메서드를 사용해 레코드를 삭제할 수 있습니다. 반환 값은 삭제된 행의 개수입니다. 삭제 전 "where"로 조건을 추가해 대상 레코드를 지정할 수 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 구문 실행 시 "비관적 잠금"을 지원하는 몇 가지 메서드를 제공합니다. "공유 잠금(shared lock)"으로 실행하려면 `sharedLock`를 호출하세요. 공유 잠금은 트랜잭션이 커밋될 때까지 조회된 행을 수정할 수 없도록 만듭니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 `lockForUpdate`를 사용해 "for update" 잠금을 걸면, 해당 레코드를 다른 트랜잭션에서 수정하거나 공유 잠금으로 조회하지 못하게 할 수 있습니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금은 꼭 필수는 아니지만, [트랜잭션](/docs/master/database#database-transactions) 내에서 사용하는 것이 권장됩니다. 이렇게 하면 전체 작업이 끝날 때까지 데이터가 변경되지 않으므로 데이터 정합성이 보장됩니다. 만약 작업에 실패하면 트랜잭션이 자동으로 롤백하고 잠금도 해제합니다.

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

애플리케이션 전역에서 반복적으로 사용되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 활용해 해당 로직을 재사용 가능한 객체로 추출할 수 있습니다. 아래와 같은 쿼리가 여러 곳에 반복된다고 가정해보겠습니다.

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

공통적으로 들어가는 목적지(destionation) 필터링 부분을 재사용 가능한 컴포넌트로 추출할 수 있습니다.

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

이제 쿼리 빌더의 `tap` 메서드로 해당 객체의 로직을 쿼리에 적용할 수 있습니다.

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

`tap` 메서드는 항상 쿼리 빌더를 반환하지만, 쿼리를 실행하고 다른 값을 반환하는 객체로 추출하고 싶을 때는 `pipe` 메서드를 사용할 수 있습니다.

아래는 [페이지네이션](/docs/master/pagination) 로직을 담은 쿼리 객체 예시입니다. `DestinationFilter`와 달리, `Paginate` 객체는 쿼리를 실제로 실행하고 paginator 인스턴스를 반환합니다.

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

쿼리 빌더의 `pipe` 메서드를 사용해 공통 페이지네이션 로직도 쉽게 적용할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리를 빌드하는 도중 `dd` 및 `dump` 메서드를 사용하면 현재 쿼리의 바인딩과 SQL을 쉽게 출력할 수 있습니다. `dd`는 디버그 정보를 출력 후 즉시 실행을 중지하며, `dump`는 출력을 하면서도 요청 실행을 계속 진행합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql` 메서드는 쿼리의 SQL에 모든 파라미터 바인딩이 실제 값으로 치환된 형태로 출력합니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
