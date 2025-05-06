# Database: 쿼리 빌더

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과 청크 처리](#chunking-results)
    - [게으르게 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인](#joins)
- [유니온](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All 절](#where-any-all-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가 Where 절](#additional-where-clauses)
    - [논리 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전문 검색(Full Text) Where 절](#full-text-where-clauses)
- [정렬, 그룹화, Limit 및 Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit과 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [Upserts](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행하는 데 편리하고 플루언트한 인터페이스를 제공합니다. 애플리케이션 내에서 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템에서 완벽히 동작합니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 쿼리 빌더에 전달되는 문자열은 별도로 정제하거나 이스케이프할 필요가 없습니다.

> [!WARNING]  
> PDO는 컬럼 이름을 바인딩하는 것을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에서 참조되는 컬럼명(예: "order by" 컬럼)을 직접 결정하도록 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 가져오기

`DB` 파사드에서 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정된 테이블에 대한 플루언트 쿼리 빌더 인스턴스를 반환하므로, 추가로 제약 조건을 체이닝하고 마지막에 `get` 메서드로 결과를 조회할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자를 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```

`get` 메서드는 쿼리 결과가 담긴 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각각의 결과는 PHP `stdClass` 객체입니다. 각 컬럼의 값은 객체의 프로퍼티로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]  
> Laravel 컬렉션은 데이터 매핑 및 축소를 위한 매우 강력한 다양한 메서드를 제공합니다. Laravel 컬렉션에 대한 더 자세한 내용은 [컬렉션 문서](/docs/{{version}}/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 값 가져오기

데이터베이스 테이블에서 단일 행만 필요하다면, `DB` 파사드의 `first` 메서드를 사용하세요. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

전체 행이 필요하지 않고 하나의 값만 추출하고 싶다면, `value` 메서드를 사용할 수 있습니다. 이 메서드는 해당 컬럼의 값을 바로 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 가져오기

특정 컬럼 값들의 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 다음 예제에서는 사용자 타이틀만 모아 컬렉션으로 조회합니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

결과 컬렉션의 키로 사용될 컬럼을 두 번째 인수로 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

수천 건의 데이터베이스 레코드를 다루어야 한다면, `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 결과를 한 번에 소량씩 가져와서 각 청크를 클로저로 전달해 처리합니다. 예를 들어, 모든 `users` 테이블을 100건씩 청크로 조회할 수 있습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades.DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리가 중단됩니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리 ...

    return false;
});
```

청크 처리 중 레코드를 업데이트할 계획이면, `chunkById` 메서드를 대신 사용하는 것이 안전합니다. 이 메서드는 기본 키 기준으로 결과를 자동으로 페이지네이션합니다:

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

> [!WARNING]  
> 청크 내에서 데이터를 업데이트하거나 삭제할 경우, 기본 키 또는 외래 키가 변경되면 결과가 달라질 수 있습니다. 이로 인해 일부 레코드가 청크 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 게으르게 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크로 실행합니다. 하지만 각 청크를 콜백에 전달하는 대신, `lazy()`는 [`LazyCollection`](/docs/{{version}}/collections#lazy-collections)를 반환하여 결과를 하나의 스트림처럼 다룰 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

조회 중 레코드를 업데이트할 계획이라면, `lazyById` 또는 `lazyByIdDesc`를 사용하는 것이 더 적합합니다. 이들은 결과를 기본 키 기준으로 자동으로 페이지네이션합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]  
> 반복 중 레코드를 수정(업데이트/삭제)할 때 기본 키나 외래 키 값이 변하면 청크 결과에서 일부 레코드가 누락될 수 있으므로 주의하세요.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`과 같은 집계 값을 조회할 수 있는 다양한 메서드를 제공합니다. 쿼리 빌드 후 이 메서드들을 호출하면 됩니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 집계 메서드에 다른 조건들을 추가할 수도 있습니다:

```php
$price = DB::table('orders')
            ->where('finalized', 1)
            ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

`count` 메서드 대신, 조건을 만족하는 레코드가 존재하는지 확인하려면 `exists` 또는 `doesntExist` 메서드를 사용할 수 있습니다:

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
#### Select 절 지정하기

모든 컬럼을 조회하지 않고 특정 컬럼만 선택하고 싶을 때에는 `select` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
            ->select('name', 'email as user_email')
            ->get();
```

`distinct` 메서드를 이용하면 중복 없이 결과를 받을 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있는 경우, `addSelect` 메서드로 컬럼을 추가할 수 있습니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

때로는 쿼리에 임의의 문자열을 삽입해야 할 수도 있습니다. 이때는 `DB` 파사드의 `raw` 메서드를 사용하여 raw 문자열 표현식을 생성할 수 있습니다:

```php
$users = DB::table('users')
             ->select(DB::raw('count(*) as user_count, status'))
             ->where('status', '<>', 1)
             ->groupBy('status')
             ->get();
```

> [!WARNING]  
> Raw 구문은 문자열 그대로 쿼리에 삽입됩니다. SQL 인젝션 취약점이 생기지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 대신, 다음 메서드들을 사용해 쿼리의 다양한 부분에 raw 표현식을 삽입할 수 있습니다. **참고: Raw 표현식이 포함된 쿼리는 SQL 인젝션으로부터 보호된다고 Laravel이 보장하지 않습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
                ->selectRaw('price * ? as price_with_tax', [1.0825])
                ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 쿼리에 raw "where" 절을 삽입할 수 있습니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
                ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
                ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 및 `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 지정할 수 있습니다:

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

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 지정할 수 있습니다:

```php
$orders = DB::table('orders')
                ->select('city', 'state')
                ->groupByRaw('city, state')
                ->get();
```

<a name="joins"></a>
## 조인

<a name="inner-join-clause"></a>
#### Inner Join 절

쿼리 빌더는 쿼리에 join 구문도 추가할 수 있습니다. 기본 "inner join"을 하려면 `join` 메서드를 사용하세요. 첫 번째 인수는 조인할 테이블명이고, 나머지는 조인 조건에 사용될 컬럼입니다. 한 쿼리에서 여러 테이블을 join할 수도 있습니다:

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

"inner join"이 아닌 "left join" 또는 "right join"을 사용하려면 각각 `leftJoin`, `rightJoin` 메서드를 사용하세요. 시그니처는 `join`과 동일합니다:

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

"cross join"을 수행하려면 `crossJoin` 메서드를 사용할 수 있습니다. Cross join은 두 테이블 간의 카티션 곱을 생성합니다:

```php
$sizes = DB::table('sizes')
            ->crossJoin('colors')
            ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 join 절도 지정할 수 있습니다. 시작하려면, `join` 메서드의 두 번째 인수에 클로저를 전달하세요. 해당 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받으며, 이를 통해 "join" 절에 조건을 추가할 수 있습니다:

```php
DB::table('users')
        ->join('contacts', function (JoinClause $join) {
            $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
        })
        ->get();
```

join 내에서 "where" 절을 쓰고 싶다면, `JoinClause` 인스턴스의 `where` 또는 `orWhere` 메서드를 사용하세요. 이 메서드들은 컬럼끼리 비교하는 대신 컬럼과 값을 비교합니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용해 쿼리를 서브쿼리와 조인할 수 있습니다. 각 메서드는 서브쿼리, 테이블 별칭, 컬럼 연결을 정의하는 클로저, 총 3개의 인수를 받습니다. 다음 예제에서는 각 사용자가 가장 최근 작성한 블로그 게시물의 `created_at` 타임스탬프가 포함된 사용자를 조회합니다:

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

`joinLateral` 및 `leftJoinLateral` 메서드를 사용해 서브쿼리와 "lateral join"을 할 수 있습니다. 이 메서드들은 서브쿼리와 테이블 별칭, 두 가지 인수를 받습니다. 조인 조건은 전달된 서브쿼리의 `where` 절 내에서 지정하세요. Lateral 조인은 각 행마다 평가되어 서브쿼리 외부의 컬럼을 참조할 수 있습니다.

예시에서는 각 사용자 및 사용자의 최근 3개 블로그 포스트를 가져옵니다. 조인 조건은 서브쿼리의 `whereColumn`에서 현재 사용자 행을 참조합니다:

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
## 유니온

쿼리 빌더는 여러 쿼리를 "union"으로 합치는 메서드도 제공합니다. 예를 들어, 초기 쿼리를 만든 뒤 `union` 메서드로 다른 쿼리를 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
            ->whereNull('first_name');

$users = DB::table('users')
            ->whereNull('last_name')
            ->union($first)
            ->get();
```

`union` 외에도 `unionAll` 메서드가 있습니다. `unionAll`은 중복 결과를 제거하지 않습니다. 시그니처는 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드로 쿼리에 "where" 조건을 추가할 수 있습니다. 가장 기본적인 호출은 컬럼명, 연산자, 비교값, 세 가지 인수가 필요합니다.

예를 들어, 다음 쿼리는 `votes` 컬럼이 100이고, `age` 컬럼이 35보다 큰 사용자를 조회합니다:

```php
$users = DB::table('users')
                ->where('votes', '=', 100)
                ->where('age', '>', 35)
                ->get();
```

특정 값과 `=` 조건만 비교할 경우, 두 번째 인수로 값을 바로 넘겨도 되고 이 때 연산자는 기본으로 `=`가 적용됩니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

데이터베이스에서 지원하는 다른 연산자도 사용할 수 있습니다:

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

조건 배열을 `where` 메서드에 넘겨 여러 조건을 한 번에 적용할 수도 있습니다. 각 배열 요소는 보통 3개 인자가 담긴 배열이어야 합니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]  
> PDO는 컬럼 이름 바인딩을 지원하지 않으므로, 사용자 입력이 쿼리에서 참조되는 컬럼명을 직접 결정하도록 허용해서는 안 됩니다.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드를 체이닝하면 조건은 기본적으로 `and`로 결합됩니다. 하지만, `orWhere` 메서드를 사용하면 쿼리 절을 `or`로 결합할 수 있으며, 인수는 `where`와 동일합니다:

```php
$users = DB::table('users')
                ->where('votes', '>', 100)
                ->orWhere('name', 'John')
                ->get();
```

`or` 조건을 괄호로 묶어서 그룹화하고 싶다면, 첫 번째 인수로 클로저를 넘길 수 있습니다:

```php
$users = DB::table('users')
            ->where('votes', '>', 100)
            ->orWhere(function (Builder $query) {
                $query->where('name', 'Abigail')
                      ->where('votes', '>', 50);
            })
            ->get();
```

위 예시는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]  
> 전역 스코프가 적용될 때 예상치 못한 동작을 방지하기 위해 항상 `orWhere`를 그룹화하세요.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 쿼리 조건 그룹을 부정할 때 사용합니다. 예를 들어, 다음 쿼리는 클리어런스 상품 또는 가격이 10 미만인 상품을 제외합니다:

```php
$products = DB::table('products')
                ->whereNot(function (Builder $query) {
                    $query->where('clearance', true)
                          ->orWhere('price', '<', 10);
                })
                ->get();
```

<a name="where-any-all-clauses"></a>
### Where Any / All 절

하나의 조건을 여러 컬럼에 적용하고 싶을 때 사용할 수 있습니다. 예를 들어, 여러 컬럼 중 하나라도 `LIKE` 조건을 만족하는 레코드를 조회하려면 `whereAny`를 사용하세요:

```php
$users = DB::table('users')
            ->where('active', true)
            ->whereAny([
                'name',
                'email',
                'phone',
            ], 'LIKE', 'Example%')
            ->get();
```

위 쿼리는 다음 SQL과 같습니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

반대로 모든 컬럼이 조건을 만족하는 경우만 조회하려면 `whereAll`을 사용할 수 있습니다:

```php
$posts = DB::table('posts')
            ->where('published', true)
            ->whereAll([
                'title',
                'content',
            ], 'LIKE', '%Laravel%')
            ->get();
```

위 쿼리는 다음 SQL과 같습니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

<a name="json-where-clauses"></a>
### JSON Where 절

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MySQL 5.7+, PostgreSQL, SQL Server 2016, SQLite 3.39.0+)에서 JSON 컬럼 쿼리 역시 지원합니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용하세요:

```php
$users = DB::table('users')
                ->where('preferences->dining->meal', 'salad')
                ->get();
```

JSON 배열을 쿼리하려면 `whereJsonContains`를 사용할 수 있습니다:

```php
$users = DB::table('users')
                ->whereJsonContains('options->languages', 'en')
                ->get();
```

MySQL이나 PostgreSQL을 사용할 경우, 배열로 값의 목록을 전달할 수 있습니다:

```php
$users = DB::table('users')
                ->whereJsonContains('options->languages', ['en', 'de'])
                ->get();
```

JSON 배열의 길이로 쿼리하려면 `whereJsonLength` 메서드를 사용할 수 있습니다:

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

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
           ->whereBetween('votes', [1, 100])
           ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값의 범위를 벗어나는지 확인합니다:

```php
$users = DB::table('users')
                    ->whereNotBetween('votes', [1, 100])
                    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`은 테이블 내 두 컬럼 값을 기준으로 범위를 지정할 수 있습니다:

```php
$patients = DB::table('patients')
                       ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

`whereNotBetweenColumns`은 값이 두 컬럼 범위 밖에 있는지 확인합니다:

```php
$patients = DB::table('patients')
                       ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
                       ->get();
```

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 컬럼 값이 지정한 배열 내에 있는지 확인합니다:

```php
$users = DB::table('users')
                    ->whereIn('id', [1, 2, 3])
                    ->get();
```

`whereNotIn`은 컬럼 값이 지정한 배열 외에 있는지 확인합니다:

```php
$users = DB::table('users')
                    ->whereNotIn('id', [1, 2, 3])
                    ->get();
```

서브쿼리도 인수로 넘길 수 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
                    ->whereIn('user_id', $activeUsers)
                    ->get();
```

위 예제는 다음 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]  
> 많은 정수 바인딩을 사용하는 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 이용해 메모리 사용량을 대폭 줄일 수 있습니다.

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

특정 날짜와 값을 비교하려면 `whereDate`를 사용하세요:

```php
$users = DB::table('users')
                ->whereDate('created_at', '2016-12-31')
                ->get();
```

특정 월을 비교하려면 `whereMonth`:

```php
$users = DB::table('users')
                ->whereMonth('created_at', '12')
                ->get();
```

특정 일을 비교하려면 `whereDay`:

```php
$users = DB::table('users')
                ->whereDay('created_at', '31')
                ->get();
```

특정 연도를 비교하려면 `whereYear`:

```php
$users = DB::table('users')
                ->whereYear('created_at', '2016')
                ->get();
```

특정 시간을 비교하려면 `whereTime`:

```php
$users = DB::table('users')
                ->whereTime('created_at', '=', '11:20:45')
                ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼이 같은 값인지 확인합니다:

```php
$users = DB::table('users')
                ->whereColumn('first_name', 'last_name')
                ->get();
```

비교 연산자도 쓸 수 있습니다:

```php
$users = DB::table('users')
                ->whereColumn('updated_at', '>', 'created_at')
                ->get();
```

여러 컬럼 비교도 가능합니다:

```php
$users = DB::table('users')
                ->whereColumn([
                    ['first_name', '=', 'last_name'],
                    ['updated_at', '>', 'created_at'],
                ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화

여러 "where" 절을 괄호로 묶어 그룹화해야 원하는 논리적 결과를 얻을 수 있습니다. 특히, `orWhere`를 사용할 때 올바른 결과를 위해 항상 괄호로 묶어야 합니다. 클로저를 `where`에 넘기면 됩니다:

```php
$users = DB::table('users')
           ->where('name', '=', 'John')
           ->where(function (Builder $query) {
               $query->where('votes', '>', 100)
                     ->orWhere('title', '=', 'Admin');
           })
           ->get();
```

위 예시는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]  
> 전역 스코프가 적용될 때 예상치 못한 행동을 방지하려면 항상 `orWhere` 호출을 그룹화하세요.

<a name="advanced-where-clauses"></a>
### 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" SQL 구문을 작성할 수 있게 해줍니다. 클로저는 쿼리 빌더 인스턴스를 받아, "exists" 절 안에 들어가는 쿼리를 지정할 수 있습니다:

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

두 예제 모두 다음 SQL을 생성합니다:

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

서브쿼리 결과와 값을 비교하는 "where" 절을 만들고 싶을 때, 클로저와 값을 `where`에 넘겨서 처리할 수 있습니다. 예를 들어, 아래 쿼리는 각 사용자가 특정 타입의 가장 최근 "membership"이 있는지를 조회합니다:

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

또는 컬럼을 서브쿼리 결과와 비교할 경우, 컬럼명, 연산자, 클로저 순서로 넘길 수 있습니다. 다음은 평균 금액보다 적은 수입을 찾는 예시입니다:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 검색(Full Text) Where 절

> [!WARNING]  
> 전문 검색 where 절은 현재 MySQL, PostgreSQL에서만 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [전문 색인(Full Text Index)](/docs/{{version}}/migrations#available-index-types)가 적용된 컬럼에 전문 검색 "where" 절을 추가할 수 있습니다. 이 메서드는 데이터베이스별로 적합한 SQL로 변환되며, 예를 들어 MySQL은 `MATCH AGAINST` 절을 생성합니다:

```php
$users = DB::table('users')
           ->whereFullText('bio', 'web developer')
           ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, Limit 및 Offset

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 특정 컬럼을 기준으로 쿼리 결과를 정렬할 수 있습니다. 첫 번째 인수는 정렬할 컬럼명, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->get();
```

여러 컬럼으로 정렬하려면 `orderBy`를 반복해서 호출하세요:

```php
$users = DB::table('users')
                ->orderBy('name', 'desc')
                ->orderBy('email', 'asc')
                ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드를 통해 날짜 기준 결과 정렬이 쉽습니다. 기본적으로는 `created_at` 컬럼 기준 오름차순/내림차순 정렬되며, 컬럼명을 지정할 수도 있습니다:

```php
$user = DB::table('users')
                ->latest()
                ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드는 쿼리 결과를 임의로 정렬할 수 있게 합니다. 예를 들어 랜덤 사용자를 조회할 때 사용합니다:

```php
$randomUser = DB::table('users')
                ->inRandomOrder()
                ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 이전에 적용된 모든 "order by" 절을 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

새로운 정렬을 적용하려면 `reorder`에 컬럼명과 방향을 넘기세요:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`와 `having`을 사용해 결과를 그룹화할 수 있습니다. `having`은 `where` 메서드와 유사하게 사용할 수 있습니다:

```php
$users = DB::table('users')
                ->groupBy('account_id')
                ->having('account_id', '>', 100)
                ->get();
```

`havingBetween`을 사용하면 그룹 결과에 범위 필터를 적용할 수 있습니다:

```php
$report = DB::table('orders')
                ->selectRaw('count(id) as number_of_orders, customer_id')
                ->groupBy('customer_id')
                ->havingBetween('number_of_orders', [5, 15])
                ->get();
```

`groupBy`에 여러 인수를 지정해 여러 컬럼으로 그룹화할 수 있습니다:

```php
$users = DB::table('users')
                ->groupBy('first_name', 'status')
                ->having('account_id', '>', 100)
                ->get();
```

더 고급 `having` 구문은 [`havingRaw`](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit과 Offset

<a name="skip-take"></a>
#### `skip` 및 `take` 메서드

쿼리에서 반환되는 결과 수를 제한하거나 결과의 일부를 건너뛰고 싶을 때는 `skip`(건너뛰기), `take`(제한) 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

또는 `limit`(제한)과 `offset`(오프셋)을 사용할 수도 있습니다. 이 메서드들은 각각 `take`와 `skip`과 기능적으로 동일합니다:

```php
$users = DB::table('users')
                ->offset(10)
                ->limit(5)
                ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절

어떤 조건에 따라 쿼리의 일부 절만 적용하고 싶을 때가 있습니다. 예를 들어, 입력값이 있을 때만 `where` 구문을 추가하려면 `when` 메서드를 사용할 수 있습니다:

```php
$role = $request->string('role');

$users = DB::table('users')
                ->when($role, function (Builder $query, string $role) {
                    $query->where('role_id', $role);
                })
                ->get();
```

`when` 메서드는 첫 인자가 true일 때만 클로저를 실행합니다. false면 실행하지 않습니다. 예제에서는 요청에 `role` 필드가 있는 경우에만 클로저가 실행됩니다.

세 번째 인수로 또 다른 클로저를 넘기면, 첫 인수가 false일 때만 해당 클로저가 실행됩니다. 이를 활용해 쿼리의 기본 정렬을 지정할 수도 있습니다:

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

쿼리 빌더는 `insert` 메서드로도 레코드를 추가할 수 있습니다. 배열로 컬럼명과 값을 넘깁니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드 추가도 가능합니다. 각 배열이 한 레코드를 의미합니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore`는 삽입 중 오류를 무시합니다. 중복 오류 등 일부 오류는 무시될 수 있습니다(특히 MySQL strict mode 참고):

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing`은 서브쿼리로 삽입할 데이터를 결정해 새 레코드를 추가합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 auto-increment id가 있을 경우, `insertGetId`로 레코드 추가 후 ID를 바로 조회할 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]  
> PostgreSQL에서 `insertGetId`는 컬럼명이 반드시 `id`여야 합니다. 다른 시퀀스에서 ID를 조회하려면 두 번째 인수로 컬럼명을 지정하세요.

<a name="upserts"></a>
### Upserts

`upsert`는 존재하지 않는 레코드를 삽입, 이미 존재하면 지정한 값으로 업데이트합니다. 첫 번째 인수는 삽입/업데이트 값, 두 번째는 레코드를 고유하게 식별할 컬럼(들), 세 번째는 업데이트할 컬럼 목록입니다:

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

위 예에서, `departure`와 `destination`이 같은 레코드가 있으면 `price`만 업데이트됩니다.

> [!WARNING]  
> `upsert`의 두 번째 인수 컬럼은 SQL Server를 제외한 모든 DB에서 "primary"나 "unique" 인덱스를 요구합니다. MySQL 드라이버는 두 번째 인수를 무시하며, 테이블의 primary/unique 인덱스만 사용합니다.

<a name="update-statements"></a>
## Update 구문

레코드 추가뿐 아니라, `update` 메서드로 기존 레코드도 수정할 수 있습니다. 수정할 컬럼과 값을 배열로 넘기며, `where`로 쿼리를 제한할 수 있습니다. 반환값은 영향을 받은 행의 개수입니다:

```php
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 업데이트 또는 삽입

특정 조건의 레코드가 있다면 업데이트하고, 아니면 추가(insert)하고 싶을 때는 `updateOrInsert` 메서드를 사용할 수 있습니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

<a name="updating-json-columns"></a>
### JSON 컬럼 업데이트

JSON 컬럼을 업데이트할 때는 `->` 문법을 써서 내부 키를 지정하면 됩니다. 이 작업은 MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
              ->where('id', 1)
              ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

쿼리 빌더는 컬럼의 값을 증가/감소시키는 편리한 메서드들도 제공합니다. `increment`, `decrement` 메서드는 첫 번째 인수로 컬럼명을, 두 번째 인수로 값을 넣을 수 있습니다(생략 시 1):

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 동시에 다른 컬럼도 업데이트할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, 여러 컬럼을 한 번에 증가/감소시킬 때는 `incrementEach`, `decrementEach`를 사용할 수 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문

쿼리 빌더의 `delete` 메서드는 레코드를 삭제할 수 있게 해줍니다. 반환값은 영향을 받은 행의 수입니다. `where` 절로 삭제 대상을 제한할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

테이블 전체의 데이터를 삭제하고, 자동 증가 ID를 리셋하려면 `truncate` 메서드를 사용할 수 있습니다:

```php
DB::table('users')->truncate();
```

<a name="table-truncation-and-postgresql"></a>
#### 테이블 Truncate와 PostgreSQL

PostgreSQL 데이터베이스에서 truncate 명령을 실행하면 `CASCADE` 동작이 적용됩니다. 즉, 외래 키 제약이 걸린 다른 테이블의 관련 레코드도 동시에 삭제됩니다.

<a name="pessimistic-locking"></a>
## 비관적 잠금

쿼리 빌더는 SELECT 쿼리 수행 시 "비관적 잠금"을 위한 몇 가지 기능도 제공합니다. "공유 잠금(shared lock)"을 실행하려면 `sharedLock` 메서드를 사용하세요. 이는 트랜잭션이 커밋될 때까지 레코드 수정이 불가능하게 합니다:

```php
DB::table('users')
        ->where('votes', '>', 100)
        ->sharedLock()
        ->get();
```

또는, "for update" 잠금은 `lockForUpdate`로 실행할 수 있습니다. 이는 다른 트랜잭션이 해당 레코드를 수정하거나 공유 잠금으로 선택하지 못하게 합니다:

```php
DB::table('users')
        ->where('votes', '>', 100)
        ->lockForUpdate()
        ->get();
```

<a name="debugging"></a>
## 디버깅

쿼리 빌드 중 `dd` 및 `dump` 메서드를 사용해 현재 쿼리 바인딩과 SQL을 확인할 수 있습니다. `dd`는 덤프 후 실행을 중단하고, `dump`는 이후 코드도 계속 실행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드는 파라미터가 삽입된 완전한 SQL을 보여줍니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
