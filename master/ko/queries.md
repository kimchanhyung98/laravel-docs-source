# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크 단위로 가져오기](#chunking-results)
    - [지연 스트리밍 결과 조회](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 문](#select-statements)
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
    - [벡터 유사도 절](#vector-similarity-clauses)
- [정렬, 그룹화, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [제한 및 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 문](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [Update 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가/감소 연산](#increment-and-decrement)
- [Delete 문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행하기 위한 편리하고 유연한 인터페이스를 제공합니다. 이 쿼리 빌더를 사용하면 애플리케이션의 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템에서 완벽하게 동작합니다.

Laravel 쿼리 빌더는 PDO의 파라미터 바인딩을 사용하여 SQL 인젝션 공격에 애플리케이션이 노출되는 것을 방지합니다. 따라서, 쿼리 빌더를 사용할 때 쿼리 바인딩에 전달되는 문자열을 별도로 정제하거나 필터링할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자의 입력이 쿼리에서 참조하는 컬럼명(예: "order by" 컬럼)에 영향을 주도록 하면 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회

`DB` 파사드의 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 플루언트 쿼리 빌더 인스턴스를 반환하며, 쿼리에 추가 조건을 체이닝한 뒤, 마지막으로 `get` 메서드를 사용해 결과를 조회할 수 있습니다:

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

`get` 메서드는 쿼리 결과를 담은 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체로 표현됩니다. 각 컬럼 값은 객체 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑 및 축약에 강력한 메서드들을 제공합니다. 자세한 내용은 [컬렉션 문서](/docs/master/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 조회

테이블에서 한 행만 조회할 필요가 있다면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

매치되는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외가 잡히지 않으면, 클라이언트에게 자동으로 404 HTTP 응답이 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않고 한 컬럼의 값만 조회할 경우 `value` 메서드를 사용하면, 해당 컬럼의 값을 바로 반환받을 수 있습니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 행을 조회할 때는 `find` 메서드를 활용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 리스트 조회

특정 컬럼들의 값들만이 담긴 `Illuminate\Support\Collection` 인스턴스가 필요하다면, `pluck` 메서드를 사용할 수 있습니다. 예를 들어, 유저의 직함만 담긴 컬렉션을 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인수로 결과 컬렉션의 키로 사용할 컬럼을 지정할 수도 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 가져오기

수천 개 이상의 데이터베이스 레코드를 다뤄야 할 때는, `DB` 파사드의 `chunk` 메서드 사용을 고려하세요. 이 메서드는 쿼리 결과를 한 번에 일정량씩 가져와 각 청크 단위로 클로저에 전달합니다. 예를 들어, `users` 테이블 전체를 100개씩 나눠서 조회할 수 있습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리가 중단됩니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중에 데이터베이스 레코드를 업데이트한다면, 처리되는 결과가 예측과 다르게 바뀔 수 있습니다. 조회한 레코드를 업데이트할 계획이라면 `chunkById` 메서드를 사용하세요. 이 메서드는 기본키 기준으로 결과를 자동 페이지네이션합니다:

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

`chunkById`와 `lazyById` 메서드는 쿼리 실행 시 자체적으로 "where" 절을 추가하므로, 직접 조건을 추가할 때는 보통 [논리적 그룹화](#logical-grouping)를 위해 클로저로 감싸는 것이 좋습니다:

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
> 청크 콜백 내부에서 레코드를 업데이트/삭제할 경우, 기본키나 외래키가 변경되면 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 결과에서 누락될 가능성이 있습니다.

<a name="streaming-results-lazily"></a>
### 지연 스트리밍 결과 조회

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크로 처리하지만, 각 청크를 콜백에 넘기지 않고, 전체 결과를 하나의 [LazyCollection](/docs/master/collections#lazy-collections)으로 스트리밍합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

조회 데이터에 대해 반복 처리와 동시에 값을 업데이트할 계획이라면, 대신 `lazyById` 또는 `lazyByIdDesc` 메서드 사용이 더욱 안전합니다. 이 메서드들은 결과를 자동으로 기본키 기준으로 페이지네이션 처리합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 중 레코드를 업데이트/삭제할 경우, 기본키나 외래키가 변경되면 쿼리 결과에 영향을 주어 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등 다양한 집계 함수 메서드를 제공합니다. 쿼리 작성 후 이들 메서드를 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

다른 조건절과 조합하여 집계 값을 세밀하게 조정할 수도 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 판단

제약 조건에 부합하는 레코드가 존재하는지 확인할 때는 `count` 대신 `exists` 및 `doesntExist` 메서드를 사용할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## Select 문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### Select 절 지정

데이터베이스 테이블의 모든 컬럼을 조회하지 않고, 일부 컬럼만 선택하고 싶다면 `select` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 쿼리 결과를 중복 없이 반환하도록 강제할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있다면, 기존 select 절에 컬럼을 추가하고 싶을 때는 `addSelect` 메서드를 사용하세요:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 (Raw Expressions)

가끔 쿼리에 임의의 문자열을 삽입할 필요가 있다면, `DB` 파사드의 `raw` 메서드로 Raw 문자열 표현식을 생성할 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 문은 쿼리에 문자열 그대로 주입되므로, SQL 인젝션 위험이 생기지 않게 각별히 주의하세요.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 메서드 대신 아래 메서드들로 쿼리의 다양한 부분에 Raw 표현식을 삽입할 수 있습니다. **Laravel은 Raw 표현식이 포함된 쿼리의 보안(SQL 인젝션 등)을 보장하지 않습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있는 메서드로, 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`, `orWhereRaw` 메서드는 쿼리에 Raw "where" 절을 추가합니다. 두 번째 인수로 바인딩 배열을 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`, `orHavingRaw` 메서드는 "having" 절에 Raw 문자열을 사용할 수 있게 해줍니다. 두 번째 인수로 바인딩 배열 사용이 가능합니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 Raw 문자열을 적용할 수 있게 합니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 Raw 문자열을 직접 지정할 수 있습니다:

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

쿼리 빌더로 조인 절도 추가할 수 있습니다. 기본 "inner join"을 수행하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. 첫 번째 인수는 조인할 테이블 이름, 나머지 인수는 조인의 컬럼 조건입니다. 하나의 쿼리에서 여러 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join" 또는 "right join"을 원한다면, `leftJoin`, `rightJoin` 메서드를 사용하세요. 사용법 및 시그니처는 `join`과 동일합니다:

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

"cross join"을 수행하려면 `crossJoin` 메서드를 사용하세요. Cross join은 첫 번째 테이블과 두 번째 테이블 간의 카티션 곱을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 조인 절도 구현할 수 있습니다. `join`의 두 번째 인수로 클로저를 전달하면, 해당 클로저에는 `Illuminate\Database\Query\JoinClause` 인스턴스가 주어져 'join' 절에 추가 제약조건을 설정할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 조건이 필요할 때는, `JoinClause` 인스턴스의 `where`, `orWhere` 메서드를 사용할 수 있습니다. 두 컬럼 대신, 컬럼과 값을 비교하게 됩니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드로 쿼리와 서브쿼리를 조인할 수 있습니다. 각 메서드는 서브쿼리, 별칭, 관련 컬럼을 정의하는 클로저 3가지를 인수로 받습니다. 아래 예시는 각 유저 레코드에 사용자가 가장 최근에 작성한 게시글의 `created_at` 타임스탬프를 포함하는 쿼리입니다:

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

`joinLateral`, `leftJoinLateral` 메서드를 사용하여 서브쿼리와 함께 "lateral join"을 수행할 수 있습니다. 각 메서드는 2개의 인수(서브쿼리, 별칭)를 받고, 조인 조건은 서브쿼리 내 `where` 절에서 지정해야 합니다. Lateral join은 각 행마다 평가되며, 서브쿼리 밖의 컬럼도 참조할 수 있습니다.

예를 들어, 각 유저별 최신 3개의 게시글을 함께 조회하는 쿼리는 다음과 같습니다:

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

쿼리 빌더는 두 개 이상의 쿼리 결과를 "유니온(union)" 하는 방법도 제공합니다. 처음 쿼리를 만든 뒤, `union` 메서드로 더 많은 쿼리를 결합할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 외에, 쿼리 결과의 중복을 제거하지 않는 `unionAll` 메서드도 제공됩니다. 두 메서드의 사용법은 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용하여 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 호출 형태는 3개의 인수를 받습니다. 첫 번째는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 모든 연산자 사용 가능), 세 번째는 비교값입니다.

예를 들어 다음 쿼리는 `votes` 컬럼 값이 `100`이고, `age` 컬럼 값이 `35`보다 큰 유저만 조회합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

`=` 연산자로 비교할 경우, 두 번째 인수에 값을 바로 넘기면 자동으로 `=` 연산자가 사용됩니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

배열로 여러 컬럼에 대해 빠르게 조건을 지정할 수도 있습니다:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

데이터베이스에서 지원하는 다른 연산자도 자유롭게 사용 가능합니다:

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

`where` 함수의 인수로 다차원 배열을 넘길 수도 있습니다. 배열의 각 요소는 일반적으로 `where`에 전달하는 3개의 인수 배열입니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 쿼리에서 참조하는 컬럼명을 사용자 입력에 맡겨서는 안 됩니다. "order by" 컬럼도 마찬가지입니다.

> [!WARNING]
> MySQL, MariaDB에서는 문자열-숫자 비교 시 자동으로 문자열을 정수로 형변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되어 예기치 않은 결과가 나올 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 경우 `User::where('secret', 0)` 실행 시 해당 행이 반환됩니다. 값 사용 시 반드시 타입을 명확히 변환해서 사용하세요.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드를 체이닝할 경우, "where" 절들은 `and` 연산자로 연결됩니다. 그러나 `orWhere` 메서드를 사용하면 쿼리에 `or` 연산자로 절을 추가할 수 있습니다. `orWhere`의 인수는 `where`와 동일합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

괄호로 "or" 조건을 감싸야 할 때는, `orWhere`의 첫 번째 인수로 클로저를 넘기면 됩니다:

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

위 예시의 SQL:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 예상치 못한 동작을 방지하려면, 항상 `orWhere` 호출은 묶어서 그룹화하는 것이 좋습니다. 전역 스코프가 적용될 때에도 안전합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`, `orWhereNot` 메서드로 쿼리 제약 조건의 부정을 처리할 수 있습니다. 예를 들어, 아래 쿼리는 clearance 상품이거나 10 미만의 가격을 가진 상품을 제외합니다:

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

여러 컬럼에 동일한 쿼리 조건을 적용하고 싶을 때, 예를 들어 여러 컬럼 중 하나라도 특정 값과 `LIKE` 일치하는 레코드만 가져오고 싶을 때 `whereAny` 메서드를 사용할 수 있습니다:

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

위 쿼리는 아래 SQL을 생성합니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

비슷하게, `whereAll` 메서드는 지정한 모든 컬럼이 조건에 부합해야 하는 경우 사용합니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

SQL 결과:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 지정한 컬럼 중 어느 것도 조건에 부합하지 않는 레코드만 반환합니다:

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

SQL 결과:

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

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+)에서 JSON 컬럼 조회도 지원합니다. JSON 컬럼을 조회할 때는 `->` 연산자를 사용하세요:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

JSON 배열을 조회할 때는 `whereJsonContains`, `whereJsonDoesntContain` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL을 사용할 경우, 값 배열도 전달 가능합니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

JSON 키 존재 여부로 결과를 조회하려면, `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

또한 JSON 배열의 길이로 결과를 필터링하려면 `whereJsonLength` 메서드를 사용할 수 있습니다:

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

`whereLike` 메서드는 문자열 패턴 매칭을 위한 "LIKE" 절을 쿼리에 추가할 수 있습니다. 이 메서드는 데이터베이스와 무관하게 대소문자 구분이 없는 경우가 기본이며, 대소문자 구분 여부(caseSensitive)를 지정할 수 있습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

대소문자 구분 검색이 필요하다면 `caseSensitive` 인자를 true로 지정하세요:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 "or" 조건과 LIKE를 결합할 때 사용합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 조건, `orWhereNotLike`는 "or"와 결합된 NOT LIKE 조건에 사용됩니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();

$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색(caseSensitive)는 현재 SQL Server에서 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 컬럼 값이 지정한 배열 중 하나에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 배열에 해당하지 않는 값을 찾을 때 사용합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn` 메서드의 두 번째 인수로 쿼리 객체도 사용할 수 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위의 SQL 결과:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 대용량 정수 배열을 쿼리에 바인딩해야 한다면, 메모리 사용을 줄이기 위해 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하세요.

**whereBetween / orWhereBetween**

`whereBetween`은 컬럼 값이 두 값 사이에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값의 범위 밖에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 동일 행 내 두 컬럼의 값 사이에 대상 컬럼 값이 포함되는지 검사합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 값이 두 컬럼 값의 범위 밖에 있는 경우에 사용합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween`은 지정한 값이 동일 행 내 두 컬럼 사이에 있는지 검사합니다:

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`은 값이 범위 밖일 때 사용합니다:

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼값이 `NULL`인지 확인합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼값이 `NULL`이 아님을 확인합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼값이 날짜와 일치하는지 비교합니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`, `whereDay`, `whereYear`, `whereTime`은 각각 월, 일, 연, 시각에 따라 비교합니다:

```php
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

`wherePast`, `whereFuture`는 컬럼값이 과거인지, 미래인지 확인합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`, `whereNowOrFuture`는 현재를 포함하여 과거 또는 미래인지 확인합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 각각 오늘인지, 오늘 이전인지, 오늘 이후인지 조건을 줍니다:

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

비슷하게, `whereTodayOrBefore`, `whereTodayOrAfter`는 오늘을 포함한 조건을 제공합니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼의 값이 같은지 검증합니다:

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

여러 컬럼 비교 조건을 배열로 전달해 `and`로 결합할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화

여러 "where" 절을 괄호로 묶어 논리적 그룹화를 해야 할 때가 있습니다. 사실, `orWhere`는 항상 괄호로 그룹화하는 것이 바람직합니다. 이를 위해 `where`에 클로저를 전달하세요:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

클로저를 `where`에 전달하면 쿼리 빌더는 새 조건 그룹의 시작을 인식합니다. 위 예시의 SQL:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 예상치 않은 쿼리 동작 방지를 위해, `orWhere`는 항상 그룹화해서 사용하세요. 전역 스코프가 적용될 때 유용합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하여 "where exists" SQL 절을 만들 수 있습니다. 이 메서드는 클로저를 인수로 받아, 해당 클로저에 쿼리 빌더 인스턴스를 전달합니다. 이 쿼리가 "exists" 절 안에 들어갑니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는 클로저 대신 쿼리 객체를 바로 전달해도 됩니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예시 모두 아래와 같은 SQL이 생성됩니다:

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

때로는, 서브쿼리 결과와 값을 비교하는 "where" 절이 필요할 수 있습니다. 이럴 때는 `where`에 클로저와 값을 같이 전달하세요. 아래는 지정한 타입의 "membership"을 최근에 가진 유저를 조회하는 예시입니다:

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

또는 컬럼과 서브쿼리 결과를 비교해야 할 때, 컬럼명·연산자·클로저를 전달하면 됩니다:

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

`whereFullText`, `orWhereFullText` 메서드는 [전체 텍스트 인덱스](/docs/master/migrations#available-index-types)가 적용된 컬럼에 대해 전체 텍스트 검색을 할 수 있도록 해줍니다. 이 메서드는 사용 중인 데이터베이스에 맞게 SQL을 자동 변환합니다. MariaDB 또는 MySQL에서는 `MATCH AGAINST` 구문을 생성합니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="vector-similarity-clauses"></a>
### 벡터 유사도 절

> [!NOTE]
> 벡터 유사도 절은 현재 `pgvector` 확장을 사용하는 PostgreSQL 커넥션에서만 지원됩니다. 벡터 컬럼 및 인덱스 정의는 [마이그레이션 문서](/docs/master/migrations#available-column-types)를 참고하세요.

`whereVectorSimilarTo` 메서드는 코사인 유사도를 기준으로 결과를 필터링하며, 관련도순으로 정렬합니다. `minSimilarity` 임계값은 `0.0`~`1.0` 사이의 값이며, 1.0에 가까울수록 더 유사합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

벡터 인수로 일반 문자열을 제공하면, Laravel은 [Laravel AI SDK](/docs/master/ai-sdk#embeddings)를 통해 자동으로 임베딩을 생성합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

기본적으로 `whereVectorSimilarTo`는 유사도 순 정렬도 함께 수행합니다. 정렬을 비활성화하려면 `order` 인수를 `false`로 설정하세요:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```

더 세밀한 제어가 필요하다면, `selectVectorDistance`, `whereVectorDistanceLessThan`, `orderByVectorDistance` 메서드들을 개별적으로 사용할 수 있습니다:

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
## 정렬, 그룹화, 제한 및 오프셋 (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 지정한 컬럼으로 정렬할 수 있도록 합니다. 첫 번째 인수는 정렬할 컬럼명이며, 두 번째 인수는 정렬 방향(asc 또는 desc)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼으로 정렬하려면 `orderBy`를 중첩 호출하면 됩니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 기본적으로 오름차순(asc)이며, 내림차순으로 정렬할 경우 두 번째 인수를 지정하거나 `orderByDesc`를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

JSON 컬럼 내부 값을 기준으로 정렬할 때는 `->` 연산자를 사용합니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest`, `oldest` 메서드

`latest`, `oldest` 메서드는 날짜 기준으로 쉽고 빠르게 정렬할 수 있게 해줍니다. 기본적으로 `created_at` 컬럼 기준이지만, 원하는 컬럼명을 전달할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 랜덤 정렬

`inRandomOrder` 메서드는 결과를 무작위로 정렬할 수 있게 해줍니다. 예를 들어, 랜덤 유저를 하나 조회하려면 다음과 같이 합니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거

`reorder` 메서드는 이전에 적용한 "order by" 절을 모두 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

새롭게 정렬하려면 컬럼명 및 방향을 전달하면 됩니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

빠르게 내림차순 정렬만 하려면 `reorderDesc`를 사용할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화 (Grouping)

<a name="groupby-having"></a>
#### `groupBy`, `having` 메서드

`groupBy`, `having` 메서드를 사용하면 결과를 클러스터링하고 필터링할 수 있습니다. `having`의 시그니처는 `where` 메서드와 비슷합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween`으로 특정 범위 내의 결과만 필터링할 수도 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy`에 여러 컬럼을 전달해 복합 그룹화를 할 수 있습니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 고급 having 문법은 [havingRaw](#raw-methods) 메서드를 활용하세요.

<a name="limit-and-offset"></a>
### 제한 및 오프셋 (Limit and Offset)

`limit`, `offset` 메서드를 통해 쿼리 결과 수를 제한하거나 지정한 수만큼 결과를 건너뛰게 할 수 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

조건에 따라 쿼리 절을 적용하고 싶을 때(예: HTTP 요청 값이 있을 때만 where 적용), `when` 메서드를 사용할 수 있습니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when`은 첫 번째 인수가 true일 때만 클로저를 실행합니다. false라면 클로저는 실행되지 않습니다. 위 예시에서 `role` 필드가 값이 있을 경우에만 where 조건이 적용됩니다.

세 번째 인수로 'false'일 때 실행할 클로저도 줄 수 있습니다. 다음은 조건에 따라 기본 정렬을 선택하는 예시입니다:

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
## Insert 문 (Insert Statements)

쿼리 빌더의 `insert` 메서드를 사용하여 테이블에 레코드를 삽입할 수 있습니다. `insert`는 컬럼명과 데이터로 이루어진 배열을 인자로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 다차원 배열을 사용하세요. 각 배열이 한 레코드에 해당합니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 데이터베이스에 기록할 때 발생하는 에러를 무시하고 넘어갑니다. 이때 중복 레코드 오류는 무시되고, 데이터베이스 엔진에 따라 다른 오류도 무시될 수 있습니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict mode를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 서브쿼리 결과로 새 레코드를 테이블에 삽입할 때 사용합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id가 있을 경우, `insertGetId` 메서드를 사용해 레코드 삽입 후 ID를 바로 반환받을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 때 `insertGetId` 메서드는 자동 증가 컬럼명이 반드시 `id` 여야 합니다. 다른 "시퀀스"에서 ID를 가져오려면 두 번째 인수로 해당 컬럼명을 전달해야 합니다.

<a name="upserts"></a>
### 업서트 (Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입(insert)하고, 이미 존재하는 레코드는 특정 컬럼값으로 업데이트(update)합니다. 첫 번째 인수는 삽입/업데이트할 값들의 배열, 두 번째는 테이블 내에서 레코드 식별용 컬럼, 세 번째는 중복 레코드가 있을 때 업데이트할 컬럼들입니다:

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

위 예시에서, `departure`와 `destination` 컬럼 값이 같은 레코드가 이미 있으면, 해당 레코드의 `price`만 업데이트됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 두 번째 인수의 컬럼에 "primary" 또는 "unique" 인덱스를 요구합니다. MariaDB나 MySQL은 두 번째 인수를 무시하고 테이블의 "primary"와 "unique" 인덱스만으로 기존 레코드를 감지합니다.

<a name="update-statements"></a>
## Update 문 (Update Statements)

쿼리 빌더는 record 삽입뿐만 아니라, 기존 레코드의 값을 변경할 때도 사용할 수 있습니다. `update` 메서드는 업데이트할 컬럼명과 값이 담긴 배열을 받아 실행하며, 영향을 받은 행 수를 반환합니다. 필요하다면 `where` 조건으로 업데이트 대상을 제한하세요:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

이미 존재하는 레코드를 업데이트하거나, 없을 경우 새 레코드를 삽입하고 싶으면 `updateOrInsert` 메서드를 사용하세요. 첫 번째 인수는 검색 조건, 두 번째 인수는 업데이트할 컬럼과 값입니다.

`updateOrInsert`는 첫 번째 인수 조건으로 레코드를 찾습니다. 있으면 두 번째 인수로 값을 업데이트, 없으면 두 조건과 값을 합쳐 새 레코드를 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

업데이트/삽입 데이터 구성을 클로저로 동적으로 지정할 수도 있습니다:

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

JSON 컬럼을 업데이트할 때는 `->` 구문을 사용해 해당 키의 값을 지정하세요. 이 동작은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가/감소 연산

쿼리 빌더는 지정한 컬럼의 값을 증감시키는 간편 메서드도 제공합니다. 첫 번째 인수는 변경할 컬럼명, 두 번째는 변경할 수(기본: 1)입니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면, 증감 연산과 함께 다른 컬럼도 추가로 업데이트할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한, `incrementEach`, `decrementEach`로 여러 컬럼을 한 번에 증감시킬 수 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 문 (Delete Statements)

쿼리 빌더의 `delete` 메서드는 레코드를 삭제하며, 삭제된 레코드 수를 반환합니다. 삭제 대상은 "where" 조건으로 제한할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 select 문 실행 시 "비관적 잠금"을 위한 함수도 제공합니다. "공유 잠금"을 사용하려면 `sharedLock` 메서드를 호출하세요. 공유 잠금이 걸린 행은 트랜잭션이 커밋될 때까지 다른 곳에서 수정할 수 없습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는 `lockForUpdate` 메서드로 "for update" 잠금을 사용할 수 있습니다. 이 잠금은 선택된 레코드가 수정될 수 없도록 하며, 다른 공유 잠금 쿼리에도 선택되지 않습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금 쿼리는 [트랜잭션](/docs/master/database#database-transactions) 구문 내에 사용하는 것이 좋습니다. 이렇게 하면, 전체 작업이 완료될 때까지 안전하게 데이터가 유지됩니다. 오류 시, 트랜잭션이 자동으로 롤백되고 잠금도 해제됩니다:

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

애플리케이션 전반에 공통된 쿼리 로직이 반복된다면 쿼리 빌더의 `tap` 및 `pipe` 메서드로 재사용 객체로 추출할 수 있습니다. 예를 들어, 아래 두 쿼리에서 목적지(destination)별 필터링 로직이 중복됩니다:

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

공통된 목적지 필터링을 별도의 재사용 객체로 뽑아낼 수 있습니다:

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

그리고 쿼리 빌더의 `tap` 메서드에 이 객체를 전달해 사용할 수 있습니다:

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
#### Query Pipe

`tap` 메서드는 항상 쿼리 빌더를 반환합니다. 쿼리를 실행하고 값(예: 페이지네이터)을 반환하는 객체로 추출하고 싶다면 `pipe` 메서드를 사용합니다.

다음은 애플리케이션에서 공통적으로 사용되는 [페이지네이션](/docs/master/pagination) 로직을 담은 쿼리 객체입니다. `DestinationFilter`는 쿼리 조건만 적용하지만, 아래 `Paginate` 객체는 쿼리를 실행하여 페이지네이터를 반환합니다:

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

쿼리 빌더의 `pipe` 메서드로 위 객체를 활용하여 공통 페이지네이션 로직을 쉽게 적용할 수 있습니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리 빌더로 쿼리를 만드는 과정에서 `dd`, `dump` 메서드를 호출하여 현재 쿼리의 바인딩 및 SQL을 바로 확인할 수 있습니다. `dd`는 디버그 정보를 보여주고 실행을 중단하며, `dump`는 정보를 보여준 후에도 요청을 계속 진행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`, `ddRawSql` 메서드는 모든 파라미터 바인딩이 적용된 SQL을 바로 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
