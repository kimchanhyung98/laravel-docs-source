# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 지연 로딩으로 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [Select 구문](#select-statements)
- [Raw 표현식](#raw-expressions)
- [조인(Join)](#joins)
- [유니온(Unions)](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All / None 절](#where-any-all-none-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [기타 Where 절](#additional-where-clauses)
    - [논리적 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전체 텍스트 Where 절](#full-text-where-clauses)
- [정렬, 그룹화, 제한 및 오프셋](#ordering-grouping-limit-and-offset)
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
- [비관적 락](#pessimistic-locking)
- [재사용 가능한 쿼리 컴포넌트](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개

라라벨의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 편리하게 작성하고 실행할 수 있는, 유연하고 직관적인 인터페이스를 제공합니다. 이 쿼리 빌더는 애플리케이션 내에서 대부분의 데이터베이스 작업을 수행할 수 있으며, 라라벨이 지원하는 모든 데이터베이스 시스템에서 완벽하게 동작합니다.

라라벨 쿼리 빌더는 SQL 인젝션 공격으로부터 애플리케이션을 보호하기 위해 PDO의 파라미터 바인딩을 사용합니다. 쿼리 빌더에 바인딩되는 문자열은 별도로 정제(clean)하거나 변환(sanitize)할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조하는 컬럼 이름(특히 "order by" 컬럼 등)을 사용자 입력에 따라 동적으로 결정하는 것은 절대 피해야 합니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 가져오기

`DB` 파사드에서 제공하는 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 유연한(체이닝 가능한) 쿼리 빌더 인스턴스를 반환하며, 이 인스턴스를 통해 다양한 제약조건을 추가한 후 최종적으로 `get` 메서드를 사용해 쿼리 결과를 가져올 수 있습니다.

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

`get` 메서드는 각 쿼리 결과마다 PHP의 `stdClass` 객체로 이루어진 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 각 컬럼의 값은 해당 객체의 속성(property)으로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> 라라벨 컬렉션은 데이터를 맵핑하거나 집계(reduce)할 때 매우 강력한 다양한 메서드를 제공합니다. 컬렉션에 대한 더 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/컬럼 가져오기

데이터베이스 테이블에서 단일 행만 필요한 경우, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 조건에 맞는 행이 없을 때 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면, `firstOrFail` 메서드를 사용하면 됩니다. 이 예외가 캐치되지 않으면 라라벨은 자동으로 404 HTTP 응답을 클라이언트에게 반환합니다.

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없는 경우, `value` 메서드를 사용해 레코드에서 단일 값만 추출할 수 있습니다. 이 메서드는 지정한 컬럼의 값을 바로 반환합니다.

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기준으로 단일 행을 조회하려면 `find` 메서드를 사용하세요.

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 가져오기

특정 컬럼의 값만 모은 `Illuminate\Support\Collection` 인스턴스를 얻고 싶다면, `pluck` 메서드를 사용할 수 있습니다. 예를 들어, 다음은 사용자들의 타이틀만 컬렉션으로 가져옵니다.

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

두 번째 인수로 컬렉션의 키로 사용할 컬럼명을 지정할 수도 있습니다.

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기

수천 개의 데이터베이스 레코드를 다뤄야 할 때는 `DB` 파사드의 `chunk` 메서드를 사용하는 것이 좋습니다. 이 메서드는 일정 갯수의 결과만 한 번에 가져와서, 각 청크를 클로저로 넘겨서 처리할 수 있습니다. 예를 들어, `users` 테이블 전체를 한 번에 100개씩 청크로 나눠서 처리하면 다음과 같습니다.

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 추가적인 청크 처리를 중단할 수 있습니다.

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리를 하면서 데이터베이스 레코드를 업데이트하고 있다면, 청크 결과가 예상치 못하게 바뀔 수 있습니다. 청크 과정에서 레코드를 수정하려는 경우에는 `chunkById` 메서드를 사용하세요. 이 메서드는 자동으로 해당 테이블의 기본 키(primary key)를 기준으로 결과를 페이지네이션합니다.

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

`chunkById`, `lazyById` 메서드는 내부적으로 자체 "where" 조건을 추가하므로, [논리적 그룹화](#logical-grouping)에서처럼 사용자 조건을 클로저로 감싸는 것이 좋습니다.

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
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제하는 경우, 기본 키나 외래 키가 달라지면 청크 쿼리에 영향을 줄 수 있습니다. 이로 인해 일부 레코드가 청크 결과에 포함되지 않을 수도 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 로딩으로 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크 단위로 실행합니다. 하지만, 각 청크를 콜백에 넘기는 대신 `lazy()`는 [LazyCollection](/docs/12.x/collections#lazy-collections) 인스턴스를 반환하므로 결과 전체를 하나의 스트림처럼 다룰 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

또한 반복 중에 조회한 레코드를 수정할 계획이라면, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이들 메서드는 자동으로 기본 키(primary key)를 기준으로 결과를 페이지네이션합니다.

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 레코드를 반복하며 업데이트하거나 삭제하는 경우, 기본 키나 외래 키가 바뀌면 청크 쿼리에 영향을 주어 결과에서 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`과 같은 다양한 집계 추출 메서드를 제공합니다. 쿼리를 작성한 뒤 이들 메서드를 바로 호출할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

여러 조건을 조합해 집계 결과를 세밀하게 조정할 수도 있습니다.

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

쿼리 조건에 맞는 레코드가 존재하는지 확인하려면 `count` 대신 `exists`, `doesntExist` 메서드를 사용할 수 있습니다.

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

항상 테이블의 모든 컬럼을 선택할 필요는 없습니다. `select` 메서드를 사용하면 원하는 컬럼만 쿼리에서 선택할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 중복된 결과 없이 고유한 행만 반환할 수 있습니다.

```php
$users = DB::table('users')->distinct()->get();
```

쿼리 빌더 인스턴스가 이미 있고, 기존 select 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 활용하세요.

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식

가끔 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. 이럴 때는 `DB` 파사드에서 제공하는 `raw` 메서드로 raw 문자열 표현식을 만들 수 있습니다.

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 문자열 그대로 쿼리에 삽입되므로, SQL 인젝션 취약점이 발생하지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw`을 사용하는 대신, 다음과 같은 메서드를 이용해 쿼리의 다양한 부분에 raw 표현식을 삽입할 수 있습니다.  
**주의: 라라벨은 raw 표현식이 포함된 쿼리의 보안(SQL 인젝션 등)을 보장하지 않습니다.**

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

`whereRaw`와 `orWhereRaw` 메서드는 raw 형태의 "where" 절을 쿼리에 삽입할 수 있습니다. 두 번째 인수로 바인딩 배열을 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 사용할 수 있도록 합니다. 두 번째 인수로 바인딩 배열을 전달할 수 있습니다.

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 raw 문자열을 사용할 수 있습니다.

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 사용할 수 있도록 합니다.

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인(Join)

<a name="inner-join-clause"></a>
#### 내부 조인(Inner Join) 절

쿼리 빌더는 쿼리에 조인 구문을 추가하는 데도 사용할 수 있습니다. 기본적인 "내부 조인"은 쿼리 빌더 인스턴스에서 `join` 메서드를 사용해 수행합니다. 첫 번째 인수는 조인할 테이블 이름이고, 나머지 인수들은 조인 조건을 지정합니다. 하나의 쿼리에서 여러 테이블을 조인하는 것도 가능합니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### 왼쪽 조인 / 오른쪽 조인(Left Join / Right Join) 절

"내부 조인"이 아니라 "왼쪽 조인(left join)"이나 "오른쪽 조인(right join)"을 하고 싶다면, 각각 `leftJoin`, `rightJoin` 메서드를 사용하세요. 사용 방법은 `join`과 동일합니다.

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### 크로스 조인(Cross Join) 절

"크로스 조인"을 수행하려면 `crossJoin` 메서드를 사용하면 됩니다. 크로스 조인은 두 테이블 간의 카테시안 곱을 생성합니다.

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인(Advanced Join) 절

더 복잡한 조인 조건을 설정하고 싶다면, `join` 메서드의 두 번째 인수로 클로저를 전달하면 됩니다. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아, 조인 절에 다양한 제약조건을 지정할 수 있습니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에서 "where" 조건을 사용해야 한다면, `JoinClause` 인스턴스의 `where`, `orWhere` 메서드를 사용하면 됩니다. 두 컬럼이 아니라 값과 컬럼을 비교하게 됩니다.

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인(Subquery Joins)

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하면 서브쿼리와 조인할 수 있습니다. 이들 메서드는 각각 서브쿼리, 별칭(alias), 관련 컬럼을 지정할 수 있는 클로저를 받습니다. 예를 들어, 각 사용자별로 최근에 등록된 블로그 글의 `created_at` 타임스탬프까지 같이 조회하고 싶다면 다음과 같이 할 수 있습니다.

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
> Lateral 조인은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서만 지원됩니다.

`joinLateral`, `leftJoinLateral` 메서드를 사용하면 서브쿼리와 "lateral join"을 수행할 수 있습니다. 이 메서드들은 각각 서브쿼리와 별칭(alias) 두 가지 인수를 받습니다. 조인 조건은 서브쿼리 내에서 `where` 절로 명시해야 합니다. Lateral 조인은 각 행(row)마다 평가되며, 서브쿼리 외부의 컬럼도 참조할 수 있습니다.

예를 들어, 각 사용자와 그 사용자의 최근 블로그 글 3개를 함께 조회하려면 다음과 같이 할 수 있습니다. 각 사용자는 최대 3개의 포스트와 매칭될 수 있습니다. 조인 조건은 서브쿼리 내에서 `whereColumn`을 사용하여 현재 사용자와 매칭되도록 지정합니다.

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

쿼리 빌더는 두 개 이상의 쿼리를 "유니온(union)"으로 합치는 편리한 메서드도 제공합니다. 예를 들어, 첫 번째 쿼리를 만들고 `union` 메서드로 추가 쿼리들과 합칠 수 있습니다.

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도 `unionAll` 메서드가 있습니다. `unionAll`로 쿼리를 합치면 중복된 결과가 제거되지 않습니다. 두 메서드는 사용법이 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용해 쿼리에 "where" 조건을 추가할 수 있습니다. 가장 기본적인 `where` 호출은 세 개의 인수를 필요로 합니다. 첫 번째 인수는 컬럼명, 두 번째는 연산자(데이터베이스에서 지원하는 임의의 연산자 가능), 세 번째 인수는 비교할 값입니다.

예를 들어, 다음 쿼리는 `votes` 컬럼이 `100`이고, `age` 컬럼이 `35`보다 큰 사용자들을 조회합니다.

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의를 위해 컬럼이 `=` 값인지 검사하려는 경우, 두 번째 인수로 값을 주면 라라벨이 자동으로 `=` 연산자를 사용한다고 간주합니다.

```php
$users = DB::table('users')->where('votes', 100)->get();
```

배열을 전달해 여러 컬럼을 한 번에 빠르게 조건 조회할 수도 있습니다.

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

앞서 언급했듯이, 데이터베이스에서 지원하는 임의의 연산자를 사용할 수 있습니다.

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

조건 배열을 `where`에 넘기면 각 요소가 세 인수를 가지는 배열(컬럼, 연산자, 값)이어야 합니다.

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 그러므로 쿼리에서 참조하는 컬럼명(특히 "order by" 컬럼 등)을 사용자 입력으로 받는 일은 절대 하지 말아야 합니다.

> [!WARNING]
> MySQL과 MariaDB는 문자열-숫자 비교 시 문자열을 자동으로 정수로 형변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되어, 예기치 않은 결과가 발생할 수 있습니다. 예를 들어, 테이블의 `secret` 컬럼 값이 `aaa`인 경우 `User::where('secret', 0)`을 실행하면 이 행이 반환됩니다. 이를 방지하려면 쿼리에서 사용하는 모든 값을 적절한 타입으로 미리 변환하세요.

<a name="or-where-clauses"></a>

### Or Where 절

쿼리 빌더의 `where` 메서드를 연달아 호출하면, 각각의 "where" 절은 기본적으로 `and` 연산자로 이어집니다. 하지만 `orWhere` 메서드를 사용하면 해당 절을 `or` 연산자로 쿼리에 추가할 수 있습니다. `orWhere` 메서드는 `where` 메서드와 동일한 인수를 받습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

만약 괄호(())로 감싼 "or" 조건 그룹이 필요하다면, `orWhere`의 첫 번째 인수로 클로저를 전달할 수 있습니다.

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

위 예시는 다음과 같은 SQL을 생성합니다.

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 방지하기 위해 항상 `orWhere` 호출은 괄호로 그룹화해야 합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot`과 `orWhereNot` 메서드는 주어진 조건 그룹 전체를 부정(negate)할 때 사용합니다. 예를 들어, 아래 쿼리는 특가 상품이거나 가격이 10 미만인 상품을 제외합니다.

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

어떤 조건을 여러 컬럼에 동시에 적용하고 싶을 때가 있습니다. 예를 들어, 주어진 컬럼들 중 하나라도 지정한 값과 `LIKE` 연산이 일치하는 레코드를 얻고 싶을 수 있습니다. 이럴 때는 `whereAny` 메서드를 사용할 수 있습니다.

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

위 쿼리는 다음과 같은 SQL을 생성합니다.

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

비슷하게, `whereAll` 메서드를 사용하면 지정한 컬럼 모두가 동일한 조건을 만족하는 레코드를 조회할 수 있습니다.

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음과 같은 SQL을 생성합니다.

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드를 사용하면 주어진 컬럼들 중 어떤 것도 특정 조건과 일치하지 않는 레코드를 조회할 수 있습니다.

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

위 쿼리는 다음과 같은 SQL을 생성합니다.

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

라라벨은 JSON 컬럼 타입을 지원하는 데이터베이스에서도 JSON 컬럼 쿼리를 제공합니다. 현재 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+에서 지원합니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용하세요.

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열을 쿼리할 때는 `whereJsonContains`와 `whereJsonDoesntContain` 메서드를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL을 사용하는 경우 값 배열을 `whereJsonContains` 및 `whereJsonDoesntContain`에 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

또한 특정 JSON 키가 포함되었는지 또는 포함되지 않았는지를 조회하는 `whereJsonContainsKey` 및 `whereJsonDoesntContainKey` 메서드도 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이를 기준으로 쿼리할 때는 `whereJsonLength` 메서드를 사용할 수 있습니다.

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

`whereLike` 메서드는 패턴 매칭을 위해 쿼리에 "LIKE" 조건을 추가합니다. 이 메서드들은 데이터베이스 종류에 상관없이 문자열 매칭 쿼리를 수행할 수 있게 해주며, 대소문자 구분 여부도 토글할 수 있습니다. 기본적으로 문자열 매칭은 대소문자를 구분하지 않습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인자를 이용하여 대소문자를 구분하는 검색도 활성화할 수 있습니다.

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 LIKE 조건과 함께 "or" 절을 추가합니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 조건을 쿼리에 추가합니다.

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

유사하게, NOT LIKE가 포함된 "or" 절을 추가하려면 `orWhereNotLike`를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 검색은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 지정한 컬럼 값이 주어진 배열에 포함되어 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn` 메서드는 컬럼 값이 주어진 배열에 포함되어 있지 않은 경우를 확인합니다.

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn`의 두 번째 인수로 쿼리 객체를 전달할 수도 있습니다.

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 예시에서 생성되는 SQL은 아래와 같습니다.

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 많은 정수 바인딩 배열을 추가해야 할 경우, 메모리 사용량을 크게 줄이기 위해 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw`를 사용할 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼 값이 두 값 사이에 있는지 확인합니다.

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값 바깥에 있는지를 확인합니다.

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 컬럼 값이 같은 행의 두 컬럼 값들 사이에 있는지 확인합니다.

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 컬럼 값이 두 컬럼 값 바깥에 있음을 확인합니다.

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween` 메서드는 주어진 값이 동일 테이블 행 내 두 컬럼 값 사이에 있는지 확인합니다.

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`은 값이 두 컬럼 값 바깥에 있는지를 확인합니다.

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 지정 컬럼 값이 `NULL`인지 확인합니다.

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 값이 `NULL`이 아님을 확인합니다.

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값이 특정 날짜와 같은지 비교합니다.

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`는 특정 월과 비교합니다.

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay`는 월의 일(day)과 비교합니다.

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`는 연도와 비교합니다.

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`은 시간과 비교합니다.

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`와 `whereFuture`는 컬럼 값이 과거 혹은 미래인지 확인합니다.

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`와 `whereNowOrFuture`는 현재 시점까지(또는 현재 시점 포함 이후까지)를 검사합니다.

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 컬럼 값이 오늘, 오늘 이전, 오늘 이후인지 확인합니다.

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

이와 비슷하게, `whereTodayOrBefore`, `whereTodayOrAfter`를 사용하면 오늘 이전 혹은 오늘 이후(오늘을 포함)를 검사할 수 있습니다.

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼이 같은 값을 가지는지 확인합니다.

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 함께 전달할 수도 있습니다.

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

컬럼 비교를 배열로 전달할 수도 있으며, 이 경우 모든 비교는 `and`로 이어집니다.

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹핑

여러 "where" 절을 괄호로 묶어 논리적인 그룹을 만들어야 할 때가 있습니다. 특히, `orWhere` 메서드를 사용할 때는 예기치 않은 쿼리 결과를 방지하기 위해 항상 괄호로 묶는 것이 좋습니다. 이를 위해 `where` 메서드에 클로저를 전달할 수 있습니다.

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

이처럼 `where` 메서드에 클로저를 전달하면 쿼리 빌더는 해당 클로저 내부의 조건들을 괄호로 그룹핑합니다. 클로저는 쿼리 빌더 인스턴스를 받아, 그 안에서 원하는 조건들을 추가할 수 있습니다. 위 예시는 다음과 같은 SQL이 만들어집니다.

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 글로벌 스코프가 적용될 때 예기치 않은 동작을 방지하기 위해 항상 `orWhere` 호출은 괄호로 그룹화해야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 SQL의 "where exists" 절을 작성할 수 있게 해줍니다. `whereExists`는 클로저를 인수로 받으며, 클로저는 쿼리 빌더 인스턴스를 전달받아 "exists" 절 내부에 들어갈 쿼리를 정의할 수 있습니다.

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는, 클로저 대신 쿼리 객체를 직접 `whereExists` 메서드에 전달할 수도 있습니다.

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 예시 모두 다음과 같은 SQL을 생성합니다.

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

서브쿼리 결과와 값을 비교하는 "where" 절이 필요한 경우가 있습니다. 이럴 때는 `where` 메서드에 클로저와 비교값을 전달하세요. 예를 들어, 아래 쿼리는 주어진 타입의 최신 "membership"을 가진 모든 사용자를 조회합니다.

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

또는, 컬럼을 서브쿼리 결과와 비교하고 싶은 경우에는 컬럼명, 연산자, 클로저를 `where`에 함께 전달하면 됩니다. 아래 예시는 amount가 평균보다 작은 income 레코드를 조회합니다.

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
> 전문 검색(Full Text) where 절은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [전문 인덱스](/docs/12.x/migrations#available-index-types)가 있는 컬럼에 대해 전문 검색 "where" 절을 쿼리에 추가할 때 사용할 수 있습니다. 이런 메서드들은 라라벨에 의해 데이터베이스 시스템에 맞는 적절한 SQL로 변환됩니다. 예를 들어, MariaDB나 MySQL을 사용하는 애플리케이션의 경우 `MATCH AGAINST` 문이 생성됩니다.

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한(Limit) 및 오프셋(Offset)

<a name="ordering"></a>
### 정렬(Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드를 사용하면 결과를 지정한 컬럼의 값으로 정렬할 수 있습니다. 첫 번째 인수에는 정렬할 컬럼명을, 두 번째 인수에는 정렬 방향(오름차순: `asc`, 내림차순: `desc`)을 지정합니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼을 기준으로 정렬하고 싶다면 `orderBy`를 필요한 만큼 반복해서 사용하면 됩니다.

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향은 생략할 수 있으며, 기본값은 오름차순(asc)입니다. 내림차순으로 정렬하려면 두 번째 인자를 명시하거나, `orderByDesc`를 사용할 수 있습니다.

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

또한, `->` 연산자를 사용해 JSON 컬럼 내부의 값을 기준으로도 정렬이 가능합니다.

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드를 사용하면 날짜를 기준으로 손쉽게 정렬할 수 있습니다. 기본값으로는 테이블의 `created_at` 컬럼에 따라 정렬됩니다. 원하는 컬럼명을 전달해 특정 컬럼을 기준으로 정렬하는 것도 가능합니다.

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드를 사용하면 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어, 임의의 사용자를 가져오고 싶을 때 쓸 수 있습니다.

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬조건 제거

`reorder` 메서드는 이전에 지정한 모든 "order by" 절을 제거합니다.

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 호출 시 컬럼명과 방향을 전달하면 모든 기존 정렬 절을 제거하고 새로운 정렬 조건을 적용합니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

좀 더 편리하게, `reorderDesc` 메서드로 내림차순 정렬을 바로 적용할 수도 있습니다.

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹화(Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상한 대로 `groupBy`와 `having` 메서드를 사용해 쿼리 결과를 그룹화할 수 있습니다. `having` 메서드 사용법은 `where`와 비슷합니다.

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

`groupBy` 메서드에 여러 인수를 전달하면 여러 컬럼별로 그룹화할 수 있습니다.

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 절을 작성하려면 [havingRaw](#raw-methods) 메서드 항목을 참고하세요.

<a name="limit-and-offset"></a>
### Limit과 Offset

`limit`과 `offset` 메서드를 사용하면 쿼리 결과의 반환 개수를 제한하거나, 지정한 개수만큼 결과를 건너뛸 수 있습니다.

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절(Conditional Clauses)

때때로 쿼리 절을 특정 조건에 따라 쿼리에 적용하고 싶을 때가 있습니다. 예를 들어, HTTP 요청에서 특정 입력값이 있을 때만 `where` 절을 추가하고 싶을 수 있습니다. 이럴 때는 `when` 메서드를 사용합니다.

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인자가 `true`일 때만 전달한 클로저를 실행합니다. 만약 첫 번째 인자가 `false`라면, 클로저는 실행되지 않습니다. 위 예시에서, `when`에 전달된 클로저는 요청으로 들어온 `role` 필드가 존재하고 참으로 평가될 때만 호출됩니다.

세 번째 인수에 추가 클로저를 전달할 수도 있습니다. 이 클로저는 첫 번째 인수가 `false`일 때에만 실행됩니다. 아래 예시처럼 쿼리의 기본 정렬 조건을 설정할 때 활용할 수 있습니다.

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

쿼리 빌더의 `insert` 메서드를 사용하면 레코드를 데이터베이스 테이블에 삽입할 수 있습니다. `insert`는 컬럼명과 값의 배열을 인수로 받습니다.

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 배열의 배열을 전달하면 됩니다. 내부의 각 배열은 삽입할 레코드 하나를 의미합니다.

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드를 삽입할 때 발생하는 오류를 무시합니다. 이 메서드를 사용할 때는 중복 레코드 에러 및 데이터베이스 엔진에 따라 다른 종류의 에러도 무시될 수 있음을 이해해야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict mode를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다.

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 하위 쿼리를 통해 삽입할 데이터를 결정하여 새 레코드를 테이블에 삽입합니다.

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id 컬럼이 있다면, `insertGetId` 메서드를 사용해 레코드를 삽입한 후 생성된 id 값을 바로 가져올 수 있습니다.

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL을 사용할 경우, `insertGetId`는 자동 증가 컬럼명이 반드시 `id`이어야 합니다. 다른 "시퀀스"의 id를 가져오려면, 두 번째 파라미터로 컬럼명을 직접 지정하세요.

<a name="upserts"></a>
### 업서트(Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 값으로 갱신합니다. 첫 번째 인수는 삽입 또는 갱신할 값 배열, 두 번째 인수는 테이블 내 레코드를 고유하게 식별할 컬럼(또는 컬럼 배열), 세 번째 인수는 중복 레코드가 존재할 때 업데이트할 컬럼 배열입니다.

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

위 예시에서, 라라벨은 두 개의 레코드를 삽입 시도합니다. 만약 동일한 `departure`와 `destination` 값의 레코드가 이미 있으면 해당 레코드의 `price` 컬럼만 갱신합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert`의 두 번째 인수에 포함된 컬럼이 반드시 "primary" 또는 "unique" 인덱스를 가져야 합니다. 또한 MariaDB와 MySQL 드라이버는 두 번째 인수를 무시하고, 항상 테이블의 "primary" 및 "unique" 인덱스가 존재 여부 탐지에 사용됩니다.

<a name="update-statements"></a>
## Update 문

쿼리 빌더는 데이터 삽입 외에도 `update` 메서드를 활용해 기존 레코드를 수정할 수 있습니다. `update` 메서드는 갱신할 컬럼과 값 쌍의 배열을 받아들입니다. 반환값은 영향을 받은 행의 수입니다. `where` 절을 추가해서 특정 레코드만 수정할 수도 있습니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update 또는 Insert

데이터베이스에 기존 레코드가 있으면 갱신하고, 없다면 새로 생성하고 싶을 수도 있습니다. 이럴 때는 `updateOrInsert` 메서드를 사용합니다. 이 메서드는 두 개의 인수를 받으며, 첫 번째는 조건을 지정하는 컬럼-값 쌍의 배열, 두 번째는 갱신할(또는 삽입할) 컬럼-값 쌍의 배열입니다.

`updateOrInsert` 메서드는 첫 번째 인수로 전달한 조건에 맞는 레코드를 찾아 있으면 두 번째 인수의 값으로 업데이트합니다. 해당하는 레코드가 없으면 두 인수가 병합된 데이터로 새 레코드가 삽입됩니다.

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

조건에 따라 갱신 또는 삽입할 속성을 클로저로 동적으로 지정할 수도 있습니다.

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
### JSON 컬럼 값 갱신

JSON 컬럼을 업데이트할 때는 `->` 문법을 써서 JSON 객체 내부의 특정 키 값을 업데이트해야 합니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다.

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 컬럼값 증가 및 감소

쿼리 빌더는 지정한 컬럼의 값을 더하거나 뺄 수 있는 편리한 메서드도 제공합니다. `increment`, `decrement` 메서드는 최소한 변경할 컬럼명을 받으며, 두 번째 인수로 증가 또는 감소시킬 값도 지정할 수 있습니다.

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

필요하다면 증가 또는 감소 작업과 함께 다른 컬럼도 동시에 수정할 수 있습니다.

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한 `incrementEach`, `decrementEach` 메서드를 사용해 여러 컬럼을 한 번에 증가 또는 감소시킬 수도 있습니다.

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 문

쿼리 빌더의 `delete` 메서드를 사용하면 테이블에서 레코드를 삭제할 수 있습니다. `delete`는 영향을 받은 행의 수를 반환합니다. "where" 절을 추가해 특정 조건에 맞는 행만 삭제할 수도 있습니다.

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금(Pessimistic Locking)

쿼리 빌더는 `select` 쿼리 실행 시 "비관적 잠금"을 위해 활용할 수 있는 몇 가지 함수를 제공합니다. "공유 잠금(shared lock)"을 적용하려면 `sharedLock` 메서드를 사용하세요. 공유 잠금이 걸린 행은 트랜잭션이 끝날 때까지 변경될 수 없습니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또는, `lockForUpdate` 메서드를 사용할 수도 있습니다. "for update" 잠금은 대상 레코드를 다른 트랜잭션에서 수정하거나 공유 잠금과 함께 선택하는 것을 모두 막습니다.

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금은 [트랜잭션](/docs/12.x/database#database-transactions) 내에서 사용하는 것이 권장됩니다. 이렇게 해야 전체 작업이 끝날 때까지 데이터 상태가 변하지 않게 되고, 만약 오류가 발생하면 변경사항과 잠금이 자동으로 롤백됩니다.

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

애플리케이션 전반에서 반복되는 쿼리 로직이 많다면, 쿼리 빌더의 `tap`, `pipe` 메서드를 활용해 로직을 재사용 가능한 객체로 분리할 수 있습니다. 예를 들어, 애플리케이션 내에 아래와 같이 서로 다른 두 쿼리가 있다고 가정해 보겠습니다.

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

위 예시에서 쿼리마다 공통적으로 사용되는 목적지(destination) 필터링 처리를 재사용 가능한 객체로 추출할 수 있습니다.

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

이제 쿼리 빌더의 `tap` 메서드를 통해 해당 객체의 로직을 쿼리에 적용할 수 있습니다.

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

`tap` 메서드는 항상 쿼리 빌더 인스턴스를 반환합니다. 만약 쿼리를 실행하고 그 결과를 반환하는 객체로 분리하고 싶다면, `pipe` 메서드를 사용할 수 있습니다.

예를 들어, 애플리케이션 전체에서 공유되는 [페이지네이션](/docs/12.x/pagination) 로직을 담은 쿼리 객체가 있다고 가정해 보겠습니다. `DestinationFilter`가 쿼리에 조건만 추가했다면, 이 `Paginate` 객체는 쿼리를 실제로 실행해 페이지네이터 인스턴스를 반환합니다.

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

쿼리 빌더의 `pipe` 메서드를 사용하면 이 객체를 적용해 페이지네이션 로직을 공유할 수 있습니다.

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅

쿼리를 만들 때 `dd`와 `dump` 메서드를 사용해 현재 쿼리 바인딩 정보와 SQL을 확인할 수 있습니다. `dd` 메서드는 디버그 정보를 출력한 후 실행을 멈추고, `dump` 메서드는 디버그 정보만 출력하고 요청 처리를 계속합니다.

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql` 및 `ddRawSql` 메서드를 호출하면 파라미터 바인딩이 모두 치환된 쿼리 SQL을 직접 출력해 볼 수 있습니다.

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```