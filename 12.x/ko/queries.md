# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계 함수 사용하기](#aggregates)
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
    - [추가적인 Where 절](#additional-where-clauses)
    - [논리적 그룹핑](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전체 텍스트 Where 절](#full-text-where-clauses)
- [정렬, 그룹핑, 제한, 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹핑](#grouping)
    - [Limit과 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 구문](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [Update 구문](#update-statements)
    - [JSON 컬럼 업데이트하기](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 구문](#delete-statements)
- [비관적 잠금](#pessimistic-locking)
- [재사용 가능한 쿼리 구성요소](#reusable-query-components)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행하기 위한 편리하고 유연한 인터페이스를 제공합니다. 이 쿼리 빌더는 애플리케이션에서 대부분의 데이터베이스 작업을 수행할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템에서 완벽하게 동작합니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 안전하게 보호합니다. 쿼리 빌더에 전달하는 문자열을 별도로 정제하거나 필터링할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리에 참조되는 컬럼명(예: "order by" 컬럼 등)을 결정하도록 허용해서는 절대 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 조회하기

쿼리를 시작하려면 `DB` 파사드가 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 주어진 테이블에 대한 유연한 쿼리 빌더 인스턴스를 반환하며, 여기에 추가 제약 조건을 체이닝해서 쿼리 결과를 `get` 메서드로 최종적으로 가져올 수 있습니다:

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

`get` 메서드는 쿼리 결과를 담고 있는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP의 `stdClass` 객체입니다. 각 컬럼 값은 객체의 속성처럼 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터를 매핑하거나 축소하는 데 매우 강력한 다양한 메서드를 제공합니다. Laravel 컬렉션에 대한 자세한 내용은 [컬렉션 문서](/docs/12.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행/단일 값 조회하기

데이터베이스 테이블에서 단일 행만 조회하려면 `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 `stdClass` 객체 한 개를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

조회 조건에 맞는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 던지게 하려면 `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외가 처리되지 않으면, 클라이언트에게 404 HTTP 응답이 자동으로 전송됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요하지 않고 특정 컬럼 값만 조회하려면 `value` 메서드를 사용할 수 있습니다. 이 메서드는 지정한 컬럼의 값을 바로 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값을 기준으로 단일 행을 가져오려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

특정 컬럼 값만으로 이루어진 `Illuminate\Support\Collection` 인스턴스를 받고 싶다면 `pluck` 메서드를 사용하세요. 아래 예시는 사용자 타이틀 목록을 가져오는 예입니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

`pluck` 메서드의 두 번째 인수로 컬렉션의 키로 사용할 컬럼명을 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기

수천 개의 데이터베이스 레코드를 다뤄야 할 경우, `DB` 파사드가 제공하는 `chunk` 메서드 사용을 권장합니다. 이 메서드는 결과를 소규모 청크로 나누어 한 번에 하나의 청크씩 클로저로 넘깁니다. 다음은 100개씩 전체 `users` 테이블을 청크 단위로 조회하는 예입니다:

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
    // 레코드 처리

    return false;
});
```

청크 처리 도중 결과 레코드를 업데이트한다면, 청크 결과가 예기치 않게 변할 수 있습니다. 조회된 레코드를 바로 업데이트할 경우에는 항상 `chunkById` 메서드를 사용하는 게 가장 안전합니다. 이 메서드는 자동으로 기본 키를 기준으로 페이지네이션합니다:

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

`chunkById` 및 `lazyById` 메서드는 쿼리에 자체적으로 "where" 조건을 추가하므로, 여러분이 직접 조건을 추가할 때는 보통 [논리적 그룹핑](#logical-grouping)을 클로저로 묶는 것이 좋습니다:

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
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제할 때, 기본 키 또는 외래 키가 변경되면 청크 쿼리에 영향을 미칠 수 있습니다. 이로 인해 일부 레코드가 청크 결과에서 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)처럼 쿼리를 청크 단위로 실행합니다. 그러나 각 청크를 콜백으로 전달하는 대신 `lazy()` 메서드는 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환하여 결과를 하나의 스트림처럼 다룰 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

조회한 레코드를 반복 처리하면서 업데이트할 계획이라면, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 안전합니다. 이 메서드들은 자동으로 기본 키 기준으로 페이지네이션합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 처리 도중 레코드를 업데이트하거나 삭제할 때, 기본 키 또는 외래 키가 변경되면 청크 쿼리에 영향을 미칠 수 있습니다. 이로 인해 일부 레코드가 결과에서 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수 사용하기

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 등과 같은 집계 값을 조회하기 위한 다양한 메서드를 제공합니다. 쿼리를 구성한 후 이 메서드들을 호출하면 됩니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

이 메서드들은 다른 절과 함께 결합하여 집계 값을 좀 더 세부적으로 조정할 수 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

쿼리의 조건에 맞는 레코드가 존재하는지 단순히 확인하고 싶다면, `count` 대신 `exists`와 `doesntExist` 메서드를 사용할 수 있습니다:

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
#### Select 절 지정하기

데이터베이스 테이블의 모든 컬럼을 항상 선택할 필요는 없습니다. `select` 메서드를 사용하여 쿼리에서 선택할 컬럼을 직접 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드를 사용하면 쿼리가 중복 없는 결과를 반환하도록 강제할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고, 기존 select 절에 컬럼을 추가하고 싶다면 `addSelect` 메서드를 사용하면 됩니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## Raw 표현식 (Raw Expressions)

때로는 쿼리에 임의의 문자열을 삽입해야 할 경우가 있습니다. 이런 경우, `DB` 파사드가 제공하는 `raw` 메서드를 사용하여 raw 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> Raw 구문은 문자열로 쿼리에 삽입되므로, SQL 인젝션 취약점이 발생하지 않도록 각별히 주의해야 합니다.

<a name="raw-methods"></a>
### Raw 메서드

`DB::raw` 메서드 대신 쿼리의 다양한 부분에 raw 표현식을 삽입하는 아래의 메서드들도 사용할 수 있습니다. **raw 표현식을 사용하는 쿼리는 Laravel이 SQL 인젝션 취약점을 방지해줄 수 없다는 점을 꼭 기억해야 합니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 이 메서드는 옵션으로 바인딩 배열을 두 번째 인수로 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드를 사용하면 쿼리에 raw "where" 절을 삽입할 수 있습니다. 이 메서드들도 두 번째 인수로 바인딩 배열을 옵션으로 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드는 "having" 절에 raw 문자열을 값으로 사용할 수 있게 해줍니다. 두 번째 인수로 바인딩 배열을 옵션으로 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 raw 문자열을 값으로 사용할 수 있습니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 raw 문자열을 값으로 사용할 수 있습니다:

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

쿼리 빌더를 사용하여 쿼리에 조인 절을 추가할 수도 있습니다. 기본 "inner join"을 하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. 첫 번째 인수는 조인할 테이블의 이름이고, 뒤의 인수들은 조인을 위한 컬럼 제약 조건을 지정합니다. 하나의 쿼리에서 여러 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join"이나 "right join"을 사용하려면 `leftJoin`, `rightJoin` 메서드를 사용하세요. 이 메서드들은 `join` 메서드와 동일한 시그니처를 가집니다:

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

"cross join"을 수행하려면 `crossJoin` 메서드를 사용하면 됩니다. 크로스 조인은 첫 번째 테이블과 조인 대상 테이블 간의 데카르트 곱(모든 조합)을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 Join 절

더 복잡한 조인 절을 지정하고 싶을 때는 `join` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받아 "join" 절에 제약 조건을 설정할 수 있습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인 내에서 "where" 절을 사용하고 싶다면, `JoinClause` 인스턴스가 제공하는 `where`, `orWhere` 메서드를 사용할 수 있습니다. 이 경우 두 컬럼을 비교하는 대신, 컬럼과 값을 비교합니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하여 쿼리를 서브쿼리와 조인할 수 있습니다. 이들 메서드는 각각 서브쿼리, 테이블 별칭, 관련 컬럼을 정의하는 클로저를 인수로 받습니다. 아래 예시는 각 사용자 레코드에 해당 사용자가 가장 최근에 발행한 블로그 글의 `created_at` 타임스탬프를 함께 조회하는 방법입니다:

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
#### 래터럴 조인(Lateral Joins)

> [!WARNING]
> 래터럴 조인은 현재 PostgreSQL, MySQL >= 8.0.14, SQL Server에서만 지원됩니다.

`joinLateral`, `leftJoinLateral` 메서드를 사용하면 서브쿼리와 "래터럴 조인(lateral join)"을 수행할 수 있습니다. 이 메서드들은 각각 서브쿼리와 테이블 별칭을 인수로 받습니다. 조인 조건은 주어진 서브쿼리의 `where` 구문 내에서 지정해야 합니다. 래터럴 조인은 각 행마다 평가되며, 서브쿼리 밖의 컬럼도 참조할 수 있습니다.

아래 예시는 각 사용자와 해당 사용자의 최신 블로그 글 3개를 가져오는 쿼리입니다. 각 사용자는 최대 3개의 결과 행을 가질 수 있습니다. 조인 조건은 서브쿼리 내의 `whereColumn` 절에서 현재 사용자 행을 참조합니다:

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
## 유니온(Union) (Unions)

쿼리 빌더는 두 개 이상의 쿼리를 "유니온(union)"하는 편리한 메서드를 제공합니다. 예를 들어, 초기 쿼리를 만든 후 `union` 메서드를 이용해 추가 쿼리와 결합할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도, `unionAll` 메서드가 제공됩니다. `unionAll`로 결합된 쿼리는 중복 결과가 제거되지 않습니다. `unionAll` 메서드는 `union`과 동일한 시그니처를 가집니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용하여 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 사용 방식은 세 개의 인수를 받으며, 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 비교할 값입니다.

예를 들어, 다음 쿼리는 `votes` 컬럼이 `100`이고 `age` 컬럼이 `35`보다 큰 사용자들을 조회합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의를 위해, 컬럼이 특정 값과 `=` 연산자로 비교되는 경우라면 두 번째 인수에 값을 바로 넘길 수 있으며, Laravel이 연산자를 `=`로 자동 적용합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

여러 컬럼을 한 번에 조건으로 지정하려면 연관 배열을 `where` 메서드의 인수로 전달할 수도 있습니다:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```

위에서도 언급했듯이, 데이터베이스 시스템이 지원하는 여러 연산자를 사용할 수 있습니다:

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

여러 개의 조건을 배열로 전달할 수도 있습니다. 각 배열 요소는 `where` 메서드에 전달하는 세 개의 인수를 담은 배열이어야 합니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않으므로, 사용자 입력이 쿼리에서 참조되는 컬럼명을 결정하도록 해서는 절대 안 됩니다("order by" 컬럼 등 포함).

> [!WARNING]
> MySQL과 MariaDB는 문자열과 숫자를 비교할 때 자동으로 문자열을 정수로 변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`으로 변환되어, 예기치 못한 결과가 발생할 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 행에서 `User::where('secret', 0)`을 실행하면 해당 행이 반환됩니다. 이런 현상을 방지하려면 쿼리 사용 전 값의 타입을 반드시 올바르게 변환하세요.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드를 연달아 체이닝하면 "and" 연산자로 조건이 결합됩니다. 그러나 쿼리에 "or" 연산자를 사용하려면 `orWhere` 메서드를 사용하세요. `orWhere` 메서드는 `where`와 동일한 인수들을 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

"or" 조건을 괄호로 논리적 그룹으로 묶고 싶다면, `orWhere`의 첫 번째 인수로 클로저를 전달하세요:

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

위 예시는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]
> 예상치 못한 동작을 방지하기 위해, `orWhere` 호출은 항상 그룹화하는 것이 좋습니다(글로벌 스코프가 적용될 때 문제가 발생할 수 있음).

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 특정 그룹의 쿼리 제약 조건을 부정(반전)할 때 사용할 수 있습니다. 아래 쿼리는 세일 중이거나 가격이 10 미만인 상품을 제외시킵니다:

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

하나의 조건을 여러 컬럼에 동시에 적용해야 할 때, 즉 주어진 목록 내 어느 컬럼이라도 특정 값을 만족하는 레코드를 조회하고 싶다면 `whereAny` 메서드를 사용할 수 있습니다:

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

비슷하게, `whereAll` 메서드를 사용하면 주어진 모든 컬럼이 특정 값을 만족하는 레코드만 조회할 수 있습니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음과 같이 변환됩니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 주어진 목록의 모든 컬럼이 조건을 만족하지 않는 레코드만 조회합니다:

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

위 쿼리는 다음과 같습니다:

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

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스(MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+ 등)에서 JSON 컬럼 쿼리를 지원합니다. JSON 컬럼 쿼리는 `->` 연산자를 사용합니다:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```

JSON 배열 내에 값이 있는지 쿼리하려면 `whereJsonContains` 및 `whereJsonDoesntContain` 메서드를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL을 사용한다면 배열을 넘겨 여러 값이 있는지 한번에 검사할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```

추가로, 특정 JSON 키의 존재 여부로 결과를 조회하려면 `whereJsonContainsKey` 및 `whereJsonDoesntContainKey` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```

마지막으로, JSON 배열의 길이로 쿼리하려면 `whereJsonLength` 메서드를 사용하세요:

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

`whereLike` 메서드는 쿼리에 "LIKE" 절을 추가하여 패턴 매칭을 할 수 있습니다. 이 메서드는 데이터베이스에 상관없이 문자열 매칭 쿼리를 할 수 있으며, 대소문자 구분 여부도 설정 가능합니다. 기본적으로 대소문자는 구분하지 않습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인수로 대소문자 구분 검색도 가능합니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 "or" 절로 LIKE 조건을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 절을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

`orWhereNotLike`는 "or"절로 NOT LIKE 조건을 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 옵션은 SQL Server에서는 현재 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 특정 컬럼의 값이 주어진 배열 내에 포함되어 있는지 검사합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 컬럼 값이 주어진 배열에 포함되지 않은 경우만 조회합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn`의 두 번째 인수로 쿼리 객체를 넘겨 서브쿼리로도 사용할 수 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 쿼리는 다음 SQL로 변환됩니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 쿼리에 대량의 정수 바인딩을 추가해야 한다면 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼 값이 두 값 사이에 있는지 검사합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween`은 컬럼 값이 두 값 바깥에 있는지만 검사합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 한 컬럼 값이 동일 행의 두 다른 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`은 한 컬럼 값이 두 다른 컬럼 값 밖에 있는지만 검사합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween`은 주어진 값이 동일 행의 두 컬럼 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```

`whereValueNotBetween`은 주어진 값이 두 컬럼 값 바깥에 있는지만 검사합니다:

```php
$patients = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 컬럼 값이 `NULL`인 행만 조회합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 컬럼 값이 `NULL`이 아닌 행만 조회합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값을 날짜와 비교할 수 있습니다:

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

`whereDay`는 특정 일(day)과 비교합니다:

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`는 특정 연도와 비교합니다:

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`은 컬럼 값을 특정 시각과 비교합니다:

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`와 `whereFuture`는 컬럼 값이 과거/미래 날짜인지 확인합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`와 `whereNowOrFuture`는 현재 날짜 및 시간 포함 여부도 검사합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 각각 오늘, 오늘 이전, 오늘 이후의 값을 검사합니다:

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

`whereTodayOrBefore`, `whereTodayOrAfter`로 오늘 포함 이전/이후 값도 검사할 수 있습니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`을 통해 두 컬럼의 값이 같은지 확인할 수 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

비교 연산자를 함께 넘길 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 컬럼 간 비교는 배열로 넘기면 됩니다. 모든 조건이 "and"로 결합됩니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹핑

여러 "where" 절을 괄호로 묶어 논리적 그룹을 만들고 싶을 때가 있습니다. 특히, `orWhere`를 사용할 때 항상 괄호로 그룹핑하는 것이 예기치 않은 동작을 방지할 수 있습니다. 이를 위해서는 `where`의 인수로 클로저를 전달하면 됩니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위와 같이 클로저를 전달하면 쿼리 빌더는 제약 조건 그룹을 시작합니다. 클로저 내에서는 쿼리 빌더 인스턴스를 사용하여 그룹 내부의 조건을 작성할 수 있습니다. 결과적으로 다음 SQL이 생성됩니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 예상치 못한 동작을 방지하기 위해, `orWhere` 호출은 항상 괄호로 그룹핑하세요(글로벌 스코프가 적용될 때 특히 주의).

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 만들 수 있습니다. `whereExists`는 쿼리 빌더 인스턴스를 받는 클로저를 인수로 받아, "exists" 절 내부에 배치될 쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

또는, 클로저 대신 쿼리 객체를 바로 넘길 수도 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 예제들은 모두 다음의 SQL을 생성합니다:

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

때로는 "where" 절에서 서브쿼리 결과와 값을 비교해야 하는 상황이 있습니다. 이럴 때는 클로저와 값을 `where` 메서드에 전달합니다. 예를 들어, 아래 쿼리는 지정된 타입의 최신 "membership"이 있는 모든 사용자를 조회합니다:

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

또는, 컬럼과 서브쿼리 결과를 비교하고자 한다면 컬럼명, 연산자, 클로저를 `where`에 전달하면 됩니다. 아래 예시는 금액이 평균값보다 작은 모든 소득 레코드를 조회합니다:

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
> 전체 텍스트 Where 절은 현재 MariaDB, MySQL, PostgreSQL만 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [전체 텍스트 인덱스](/docs/12.x/migrations#available-index-types)가 설정된 컬럼에 대해 전체 텍스트 "where" 절을 추가합니다. 이 메서드들은 사용 중인 데이터베이스 시스템에 맞게 적합한 SQL로 변환됩니다. 예를 들어, MariaDB나 MySQL을 사용하는 경우 `MATCH AGAINST` 절이 생성됩니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹핑, 제한, 오프셋 (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 주어진 컬럼으로 결과를 정렬할 수 있습니다. 첫 번째 인수는 정렬할 컬럼명, 두 번째 인수는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

여러 컬럼에 대해 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

정렬 방향 인수는 생략할 수 있으며, 기본값은 오름차순(asc)입니다. 내림차순 정렬을 하고 싶다면 두 번째 인수를 지정하거나, `orderByDesc`를 사용할 수도 있습니다:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```

또한, `->` 연산자를 사용하여 JSON 컬럼 내 값을 기준으로 정렬할 수 있습니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest`와 `oldest` 메서드

`latest`와 `oldest` 메서드를 사용하면 날짜 기준으로 쉽게 정렬할 수 있습니다. 기본적으로 테이블의 `created_at` 컬럼을 기준으로 정렬하지만, 정렬 조건 컬럼을 직접 지정할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬(Random Ordering)

`inRandomOrder` 메서드로 쿼리 결과를 임의 순서로 정렬할 수 있습니다. 예를 들어, 임의의 사용자를 한 명 조회하려면 다음과 같이 합니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 조건 제거하기

`reorder` 메서드를 사용하면 쿼리에 적용된 모든 "order by" 절을 제거할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 호출 시 컬럼과 방향을 넘겨주면 기존 정렬은 모두 제거되고, 새로운 정렬 조건만 적용됩니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

내림차순 재정렬을 간단하게 하려면 `reorderDesc`도 사용할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```

<a name="grouping"></a>
### 그룹핑

<a name="groupby-having"></a>
#### `groupBy`와 `having` 메서드

`groupBy`와 `having` 메서드를 사용해 결과를 그룹핑할 수 있습니다. `having` 메서드는 `where` 메서드와 유사한 시그니처를 가집니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween`을 이용해 지정된 범위 내에서 필터링할 수도 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 컬럼을 그룹핑 조건으로 사용할 때는 `groupBy`에 여러 인수를 넘기면 됩니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 구문은 [havingRaw](#raw-methods) 메서드를 참고하세요.

<a name="limit-and-offset"></a>
### Limit과 Offset

`limit`과 `offset` 메서드를 사용하면 쿼리 결과의 개수를 제한하거나, 일정 개수의 결과를 건너뛸 수 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

특정 조건에 따라 쿼리의 일부 절만을 적용하고 싶은 경우가 있습니다. 예를 들어, HTTP 요청에 특정 입력값이 있을 때만 `where` 절을 추가하고 싶을 때, `when` 메서드를 사용할 수 있습니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인수가 `true`일 때만 지정된 클로저를 실행합니다. 위 예시에서는 요청에 `role` 필드가 존재하고 값이 있을 때만 클로저가 호출됩니다.

세 번째 인수로 다른 클로저를 넘기면, 첫 번째 인수가 `false`일 때만 호출됩니다. 이를 이용해 쿼리의 기본 정렬 옵션 등도 구성할 수 있습니다:

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

쿼리 빌더는 `insert` 메서드를 통해 테이블에 레코드를 삽입할 수 있습니다. `insert` 메서드는 컬럼명과 값의 배열을 인수로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 배열의 배열을 넘기면 됩니다. 각 배열이 삽입할 한 레코드가 됩니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore` 메서드는 레코드를 삽입할 때 오류(예: 중복 레코드 등)를 그냥 무시합니다. 이 메서드를 사용할 때는 중복 레코드 오류는 무시되고, 데이터베이스 엔진에 따라 다른 종류의 오류도 무시될 수 있음을 유의해야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 strict mode를 우회](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing` 메서드는 삽입할 데이터를 서브쿼리 결과로 결정하여 레코드를 삽입합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 id 컬럼이 있다면, `insertGetId` 메서드로 레코드를 삽입 후 즉시 해당 id를 가져올 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL 사용 시 `insertGetId` 메서드는 자동 증가 컬럼명을 `id`로 예상합니다. 다른 "sequence"에서 id를 가져오고 싶다면 컬럼명을 두 번째 인수로 넘겨야 합니다.

<a name="upserts"></a>
### 업서트(Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 이미 존재하는 레코드는 지정한 값으로 업데이트합니다. 첫 번째 인수는 삽입 또는 업데이트할 값, 두 번째 인수는 레코드를 고유하게 식별하는 컬럼 목록, 세 번째 인수는 중복된 레코드가 있으면 업데이트할 컬럼 배열입니다:

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

위 예시에서, `departure`와 `destination` 값이 같은 레코드가 이미 있다면 해당 레코드의 `price` 값만 업데이트됩니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert`의 두 번째 인수 컬럼이 "primary" 또는 "unique" 인덱스를 가져야 합니다. MariaDB 및 MySQL 드라이버는 두 번째 인수를 무시하고 자동으로 테이블의 "primary", "unique" 인덱스를 사용해 기존 레코드를 감지합니다.

<a name="update-statements"></a>
## Update 구문 (Update Statements)

데이터 삽입 외에도, 쿼리 빌더로 기존 레코드를 `update` 메서드를 통해 수정할 수 있습니다. `update` 메서드는 수정할 컬럼값 쌍의 배열을 받으며, 변경된 행의 갯수를 반환합니다. `where` 절을 이용해 업데이트 대상을 제한할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### Update or Insert

기존에 레코드가 있다면 업데이트하고, 없으면 새로 생성하고 싶을 때는 `updateOrInsert` 메서드를 사용할 수 있습니다. 이 메서드는 두 가지 인수를 받는데, 첫 번째 배열은 레코드를 찾기 위한 조건, 두 번째 배열은 업데이트할 컬럼값 쌍입니다.

`updateOrInsert`는 첫 번째 조건으로 레코드를 찾고, 있으면 두 번째 값을 사용해 업데이트하며, 없으면 두 조건을 합쳐 새 레코드를 만듭니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

매칭된 레코드 여부에 따라 업데이트 또는 삽입할 속성을 클로저로 동적으로 지정할 수도 있습니다:

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
### JSON 컬럼 업데이트하기

JSON 컬럼을 업데이트할 때는 `->` 구문을 사용해 JSON 객체 내의 특정 키만 수정할 수 있습니다. 이 기능은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

쿼리 빌더는 지정한 컬럼 값을 쉽게 증가시키거나 감소시키는 메서드도 제공합니다. 각 메서드는 적어도 컬럼명을 받으며, 두 번째 인수로 증가(감소)할 수치를, 더 나아가 추가로 업데이트할 컬럼도 지정할 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

추가 컬럼을 함께 수정하고자 한다면 세 번째 인수에 배열을 넘길 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

여러 컬럼을 한 번에 증가(감소)시켜야 한다면 `incrementEach`, `decrementEach` 메서드를 사용할 수도 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 구문 (Delete Statements)

쿼리 빌더의 `delete` 메서드는 테이블에서 레코드를 삭제할 때 사용합니다. `delete`는 삭제된 행의 개수를 반환합니다. `where` 절을 추가해서 특정 행만 삭제할 수도 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 구문 실행 시 "비관적 잠금"을 위한 몇 가지 함수도 제공합니다. "공유 잠금(shared lock)"으로 실행하려면 `sharedLock` 메서드를 사용하세요. 공유 잠금은 트랜잭션이 완료될 때까지 선택된 행이 수정되는 것을 방지합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

또 다른 방법으로, `lockForUpdate` 메서드는 "for update" 잠금을 걸어서 행이 수정 또는 다른 공유 잠금의 대상으로 선택되지 않도록 막습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

반드시 필요한 것은 아니지만, 비관적 잠금 코드는 [트랜잭션](/docs/12.x/database#database-transactions)으로 감싸는 것이 권장됩니다. 이렇게 하면 데이터가 작업 완료 시까지 데이터베이스에서 변경되지 않게 되고, 실패 발생 시 롤백과 동시에 잠금도 자동 해제됩니다:

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

애플리케이션 전역에서 반복되는 쿼리 로직이 있다면, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 통해 재사용 가능한 객체로 추출할 수 있습니다. 다음과 같이 동일한 조건이 반복되는 쿼리가 있을 때:

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

공통인 목적지 필터링 로직을 다음과 같이 객체로 추출할 수 있습니다:

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

이후 쿼리 빌더의 `tap` 메서드를 사용해 해당 객체의 로직을 쿼리에 적용할 수 있습니다:

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

`tap` 메서드는 언제나 쿼리 빌더를 반환합니다. 쿼리를 실행하고 다른 값을 반환하는 객체로 추출하고 싶다면 `pipe` 메서드를 사용할 수 있습니다.

예를 들어, 다음과 같이 전체 애플리케이션에서 공통적으로 사용하는 [페이지네이션](/docs/12.x/pagination) 로직을 갖는 쿼리 객체가 있다면, 이 객체는 쿼리 조건만 적용하는 `DestinationFilter`와는 달리 쿼리를 실제 실행해 paginator 인스턴스를 반환하게 됩니다:

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

`pipe` 메서드를 사용하면 이 객체를 통한 공통 페이지네이션 로직도 쉽게 재사용할 수 있습니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리를 빌드하는 중에는 `dd` 및 `dump` 메서드를 사용하면 현재 쿼리의 바인딩과 SQL을 확인할 수 있습니다. `dd` 메서드는 디버그 정보를 출력 후 실행을 멈추며, `dump`는 정보를 출력하지만 계속 실행을 진행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql`을 사용하면 쿼리의 모든 파라미터 바인딩이 제대로 치환된 SQL문을 출력할 수 있습니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
