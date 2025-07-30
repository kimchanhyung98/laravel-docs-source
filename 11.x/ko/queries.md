# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행하기](#running-database-queries)
    - [결과를 청크 단위로 처리하기](#chunking-results)
    - [결과를 지연 스트리밍하기](#streaming-results-lazily)
    - [집계 함수](#aggregates)
- [셀렉트 문](#select-statements)
- [원시 표현식 (Raw Expressions)](#raw-expressions)
- [조인](#joins)
- [유니언 (Unions)](#unions)
- [기본 Where 절](#basic-where-clauses)
    - [Where 절](#where-clauses)
    - [Or Where 절](#or-where-clauses)
    - [Where Not 절](#where-not-clauses)
    - [Where Any / All / None 절](#where-any-all-none-clauses)
    - [JSON Where 절](#json-where-clauses)
    - [추가 Where 절](#additional-where-clauses)
    - [논리 그룹화](#logical-grouping)
- [고급 Where 절](#advanced-where-clauses)
    - [Where Exists 절](#where-exists-clauses)
    - [서브쿼리 Where 절](#subquery-where-clauses)
    - [전문 텍스트 Where 절](#full-text-where-clauses)
- [정렬, 그룹화, Limit 및 Offset](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [Limit 및 Offset](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [Insert 문](#insert-statements)
    - [업서트 (Upserts)](#upserts)
- [Update 문](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소](#increment-and-decrement)
- [Delete 문](#delete-statements)
- [비관적 잠금 (Pessimistic Locking)](#pessimistic-locking)
- [디버깅](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 작성하고 실행하는 데 편리하고 플루언트한 인터페이스를 제공합니다. 애플리케이션에서 대부분의 데이터베이스 작업을 수행하는 데 사용할 수 있으며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽하게 작동합니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 애플리케이션을 SQL 인젝션 공격으로부터 보호합니다. 쿼리 바인딩에 전달되는 문자열을 별도로 정리하거나 필터링할 필요가 없습니다.

> [!WARNING]  
> PDO는 컬럼 이름 바인딩을 지원하지 않으므로, 사용자 입력이 쿼리에서 참조하는 컬럼명, 특히 "order by" 컬럼명에 영향을 미치지 않도록 해야 합니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행하기 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블의 모든 행 조회하기

`DB` 파사드가 제공하는 `table` 메서드를 사용해 쿼리를 시작할 수 있습니다. `table` 메서드는 해당 테이블에 대한 플루언트 쿼리 빌더 인스턴스를 반환하므로 추가 조건을 연결할 수 있고, 최종적으로 `get` 메서드로 쿼리 결과를 조회할 수 있습니다:

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

`get` 메서드는 PHP의 `stdClass` 객체 인스턴스들을 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 각 결과의 컬럼값은 객체의 속성으로 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]  
> Laravel 컬렉션은 데이터를 매핑하거나 축소하는 데 매우 강력한 여러 메서드를 제공합니다. 더 자세한 내용은 [컬렉션 문서](/docs/11.x/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 단일 행 또는 컬럼 조회하기

데이터베이스 테이블에서 단일 행만 조회하고 싶다면, `DB` 파사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

일치하는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키면서 단일 행을 조회하려면 `firstOrFail` 메서드를 사용할 수 있습니다. 이 예외가 잡히지 않으면 자동으로 404 HTTP 응답이 클라이언트에 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 아닌 단일 컬럼 값을 추출하려면 `value` 메서드를 사용할 수 있습니다. 이 메서드는 컬럼의 값을 직접 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 컬럼 값 목록 조회하기

단일 컬럼의 값 목록을 포함하는 `Illuminate\Support\Collection` 인스턴스를 조회하려면 `pluck` 메서드를 사용할 수 있습니다. 아래 예제에서는 사용자 타이틀 목록을 조회합니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

두 번째 인수로 키로 사용할 컬럼명을 지정할 수도 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과를 청크 단위로 처리하기 (Chunking Results)

수천 건의 데이터베이스 레코드를 다뤄야 할 때는 `DB` 파사드의 `chunk` 메서드 사용을 고려하세요. 이 메서드는 결과를 작은 청크 단위로 조회하며, 각각을 클로저로 전달해 처리할 수 있습니다. 예를 들어, `users` 테이블 전체를 100개씩 청크 단위로 조회하는 예시입니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 추가 청크 처리를 중단할 수 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드를 처리...

    return false;
});
```

청크 처리 중에 데이터 업데이트가 필요한 경우, 결과가 예기치 않게 변할 수 있으므로 `chunkById` 메서드 사용이 권장됩니다. 이 메서드는 레코드의 기본 키를 기준으로 페이징합니다:

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

`chunkById`와 `lazyById` 메서드는 쿼리에 자체적인 "where" 조건을 추가하므로, 자신의 조건도 [논리 그룹화](#logical-grouping)하여 클로저 내부에 묶는 것이 좋습니다:

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
> 청크 콜백 내부에서 레코드를 업데이트하거나 삭제할 경우, 기본 키나 외래 키 변경으로 인해 쿼리 결과에서 일부 레코드가 누락될 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 지연 스트리밍하기 (Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백으로 넘기는 대신 [`LazyCollection`](/docs/11.x/collections#lazy-collections)을 반환해 결과를 일괄 스트림으로 다룰 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

반복 중에 레코드를 변경하는 경우, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이들은 레코드의 기본 키 기준으로 자동 페이징합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]  
> 반복 중에 레코드를 업데이트하거나 삭제할 경우, 기본 키나 외래 키 변경으로 인해 결과에서 일부 레코드가 누락될 수 있습니다.

<a name="aggregates"></a>
### 집계 함수 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 같은 다양한 집계 메서드를 제공합니다. 쿼리를 구성한 뒤 바로 이들 메서드를 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 다른 조건과 결합해서 집계 값을 세밀하게 계산할 수도 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인하기

`count` 메서드 대신 `exists`와 `doesntExist` 메서드를 사용해 조건에 맞는 레코드 존재 여부를 확인할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```

<a name="select-statements"></a>
## 셀렉트 문 (Select Statements)

<a name="specifying-a-select-clause"></a>
#### Select 절 지정하기

데이터베이스 테이블에서 모든 컬럼을 조회하지 않고 특정 컬럼만 선택하려면, `select` 메서드를 사용해 쿼리의 select 절을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드는 결과에서 중복을 제거하도록 강제합니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있을 때, 기존 select에 컬럼을 추가하려면 `addSelect` 메서드를 사용하세요:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## 원시 표현식 (Raw Expressions)

쿼리에 임의 문자열을 삽입하고 싶을 때 `DB` 파사드의 `raw` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]  
> 원시 표현식은 SQL 인젝션 취약점이 발생할 수 있으므로 매우 주의해서 사용해야 합니다.

<a name="raw-methods"></a>
### 원시 메서드

`DB::raw` 대신 쿼리의 여러 부분에 원시 표현식을 삽입할 때 아래 메서드들을 사용할 수 있습니다. **원시 표현식을 사용하는 쿼리는 SQL 인젝션으로부터 완벽한 보호를 Laravel이 보장하지 않는다는 점을 꼭 기억하세요.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw`는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw` / `orWhereRaw`

원시 "where" 절을 주입할 때 사용합니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw` / `orHavingRaw`

원시 "having" 절을 넣을 때 사용합니다. 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

원시 "order by" 절을 제공할 때 사용합니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`group by` 절에 원시 문자열을 제공할 때 사용합니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### 내부 조인 (Inner Join) 절

쿼리 빌더를 사용해 조인 절을 추가할 수 있습니다. 기본 "inner join"을 수행하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. 첫 번째 인자는 조인할 테이블 이름이며, 나머지 인자는 조인 컬럼 제약 조건을 지정합니다. 한 쿼리에서 여러 테이블을 조인할 수도 있습니다:

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

"inner join" 대신 "left join"이나 "right join"을 원하면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 시그니처는 `join` 메서드와 같습니다:

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```

<a name="cross-join-clause"></a>
#### 크로스 조인 (Cross Join) 절

`crossJoin` 메서드를 사용하면 "cross join"을 수행할 수 있으며, 두 테이블의 데카르트 곱(Cartesian Product)이 생성됩니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

`join` 메서드의 두 번째 인자로 클로저를 전달해 더 복잡한 조인 조건을 지정할 수 있습니다. 클로저는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받고, 이 인스턴스를 통해 조인 제약 조건을 설정합니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인에 "where" 조건을 사용하려면, `JoinClause` 인스턴스의 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 이때 비교는 컬럼 대 컬럼이 아니라 컬럼 대 값으로 수행됩니다:

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

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용해 서브쿼리를 조인할 수 있습니다. 각각 세 개의 인자를 받는데, 서브쿼리, 서브쿼리 별칭, 그리고 조인 컬럼을 정의하는 클로저입니다. 아래 예시처럼, 각 사용자에 대해 가장 최근 게시글의 `created_at` 타임스탬프가 포함된 사용자 컬렉션을 조회할 수 있습니다:

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
#### 래터럴 조인 (Lateral Joins)

> [!WARNING]  
> 래터럴 조인은 현재 PostgreSQL, MySQL 8.0.14 이상, SQL Server에서 지원됩니다.

`joinLateral`과 `leftJoinLateral` 메서드로 "래터럴 조인"을 할 수 있습니다. 두 인자를 받는데, 서브쿼리와 별칭입니다. 조인 조건은 서브쿼리 내부 `where` 절에서 지정해야 합니다. 래터럴 조인은 각 행마다 평가되며, 서브쿼리 외부의 컬럼을 참조할 수 있습니다.

예를 들어, 각 사용자의 가장 최근 블로그 게시글 최대 3개를 함께 조회하는 예시입니다. 사용자 당 최대 세 개의 행이 반환됩니다. 조인 조건은 서브쿼리 내 `whereColumn`에서 현재 사용자 행을 참조합니다:

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

쿼리 빌더는 두 개 이상의 쿼리를 "union" 하는 편리한 메서드를 제공합니다. 예를 들어, 초기 쿼리를 만들고 `union` 메서드로 다른 쿼리와 결합할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 메서드 외에도 `unionAll` 메서드를 사용할 수 있습니다. `unionAll`은 중복 결과를 제거하지 않고 합칩니다. 시그니처는 `union`과 같습니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드로 쿼리에 "where" 절을 추가할 수 있습니다. 가장 기본적인 호출 형태는 3개의 인수를 받는데, 첫 번째는 컬럼명, 두 번째는 연산자, 세 번째는 비교할 값입니다.

예를 들어, `votes` 컬럼이 100과 같고 `age` 컬럼이 35 초과인 사용자 조회 쿼리입니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

`=` 연산자인 경우 두 번째 인수에 값을 바로 넣는 것을 편의상 지원합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

데이터베이스가 지원하는 어떠한 연산자도 사용할 수 있습니다:

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

`where` 메서드에 조건 배열을 전달할 수도 있습니다. 배열의 각 원소는 세 개 요소(컬럼, 연산자, 값)를 담은 배열입니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]  
> PDO는 컬럼 이름 바인딩을 지원하지 않으므로, 사용자 입력이 쿼리에서 참조하는 컬럼명, 특히 "order by" 컬럼명에 영향을 미치지 않도록 해야 합니다.

> [!WARNING]  
> MySQL과 MariaDB는 문자열-숫자 비교에서 문자열을 자동으로 정수로 형변환합니다. 이때 숫자가 아닌 문자열은 `0`으로 변환되어 예상치 못한 결과가 발생할 수 있습니다. 예를 들어, `secret` 컬럼 값이 `aaa`인 행에 대해 `User::where('secret', 0)`를 실행하면 해당 행이 조회됩니다. 이를 방지하려면 쿼리 사용 전 값을 적절한 타입으로 명시적 형변환해야 합니다.

<a name="or-where-clauses"></a>
### Or Where 절

여러 개의 `where`를 연결하면 기본적으로 `and` 연산자로 결합됩니다. 그러나 `orWhere` 메서드를 사용하면 `or` 연산자로 연결할 수 있습니다. `orWhere`는 `where`와 동일한 인수를 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

`orWhere`에 클로저를 전달해 괄호로 그룹화할 수도 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
        })
    ->get();
```

위 예는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```

> [!WARNING]  
> 전역 스코프가 적용될 때 예상치 못한 동작을 막기 위해 `orWhere` 호출은 항상 그룹화해서 사용하는 것이 좋습니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 주어진 쿼리 조건 그룹을 부정하는 데 사용됩니다. 예를 들어, 아래 쿼리는 세일 상품이거나 가격이 10 미만인 상품은 제외하고 조회합니다:

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

여러 컬럼에 동일한 조건을 적용하고 싶은 상황이 있습니다. 예를 들어, 주어진 컬럼 목록 중 하나라도 특정 패턴과 일치하는 값이 있는 행을 조회하려면 `whereAny`를 사용하세요:

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

반대로, 모든 컬럼이 조건에 일치해야 하면 `whereAll`을 사용합니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음과 같습니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone`은 모든 컬럼이 조건에 부합하지 않아야 하는 경우 사용합니다:

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

생성되는 SQL 예시:

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

JSON 컬럼 타입을 지원하는 데이터베이스에서는 JSON 컬럼 내부 값을 조회할 수 있습니다. 지원하는 DB로는 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+가 있습니다. `->` 연산자를 사용해 JSON 경로를 지정합니다:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

JSON 배열에서 값을 포함하는지 확인하려면 `whereJsonContains`를 사용하세요:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL에서는 배열을 넘겨 복수 값을 지정할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

배열 길이를 기준으로 조회하려면 `whereJsonLength`를 사용하세요:

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

`whereLike` 메서드는 패턴 매칭을 위한 "LIKE" 절을 추가합니다. 데이터베이스 독립적으로 문자열 매칭 쿼리를 수행하며 대소문자 구분 여부를 설정할 수 있습니다. 기본적으로 대소문자를 구분하지 않습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인자에 `true`를 주면 대소문자 구분 검색을 활성화할 수 있습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike`는 "or" 절에서 LIKE 조건을 추가합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```

`whereNotLike`는 "NOT LIKE" 절을 추가합니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```

`orWhereNotLike`는 "or" 절에서 NOT LIKE 조건을 추가합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]  
> SQL Server에서는 `whereLike`의 대소문자 구분 옵션이 현재 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn`은 특정 컬럼 값이 배열 내에 포함되는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 배열에 값이 포함되어 있지 않은 경우를 확인합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

두 번째 인수에 쿼리 객체를 넘길 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

생성 SQL 예시:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]  
> 큰 정수 배열을 쿼리에 바인딩할 경우, 메모리 사용량을 크게 줄이려면 `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하는 것이 좋습니다.

**whereBetween / orWhereBetween**

두 값 사이에 컬럼 값이 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

두 값 사이에 컬럼 값이 없는지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

동일 행 내 두 컬럼 값 사이에 다른 컬럼 값이 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

해당 범위 밖에 값이 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

컬럼 값이 `NULL`인지 확인합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

반대로 `NULL`이 아닌지도 확인할 수 있습니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

날짜, 월, 일, 연도, 시간 단위로 컬럼 값을 비교할 수 있습니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();

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

컬럼 값이 과거인지 미래인지 확인할 수 있습니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

현재 시각을 포함하는 과거, 미래도 검사 가능합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

오늘인지, 오늘 이전 또는 이후인지 검사할 수도 있습니다:

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

포함하는 형태도 지원합니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

두 컬럼 값이 같은지 비교합니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```

연산자를 포함한 비교도 할 수 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```

여러 컬럼 조건 배열로 AND 연산자 결합도 가능합니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리 그룹화

여러 where 절을 괄호로 묶어 그룹화해야 할 경우가 많습니다. 특히 `orWhere`를 사용할 때는 쿼리 동작이 예상치 못하게 될 수 있으므로 반드시 괄호로 묶어야 합니다. 이럴 때는 `where` 메서드에 클로저를 전달합니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

`where`에 클로저를 전달하면 괄호로 묶이는 제약 조건 그룹이 생성됩니다. 위 예제는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]  
> 전역 스코프 사용 시 예상치 못한 동작을 막기 위해 `orWhere` 호출은 항상 그룹화해서 사용하는 것이 권장됩니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드는 "where exists" 절을 작성할 때 사용합니다. 인자로 클로저를 받는데, 클로저는 쿼리 빌더 인스턴스를 받아 "exists" 절 안에 넣을 쿼리를 정의합니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

클로저 대신 쿼리 객체를 직접 넘겨도 됩니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

위 두 예제는 다음 SQL을 생성합니다:

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

서브쿼리 결과와 값을 비교하는 where 절을 만들어야 할 때가 있습니다. `where` 메서드에 클로저와 값을 넘기면 가능합니다. 예를 들어, 특정 타입의 최근 membership이 있는 사용자를 조회하는 쿼리입니다:

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

또는 컬럼과 서브쿼리 결과를 비교할 수도 있습니다. 예를 들어, 금액이 평균보다 작은 수입 기록을 조회합니다:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 텍스트 Where 절

> [!WARNING]  
> 전문 텍스트 Where 절은 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText`와 `orWhereFullText` 메서드는 [전문 텍스트 인덱스](/docs/11.x/migrations#available-index-types)가 있는 컬럼을 대상으로 전문 텍스트 검색을 추가합니다. Laravel이 기반 DBMS에 맞는 SQL로 변환합니다. MariaDB와 MySQL에서는 `MATCH AGAINST` 문이 생성됩니다:

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

`orderBy` 메서드로 쿼리 결과를 특정 컬럼으로 정렬할 수 있습니다. 첫번째 인수는 정렬 대상 컬럼명, 두번째 인수는 `asc` 또는 `desc`로 정렬 방향을 정합니다:

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

<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 메서드

`latest`와 `oldest` 메서드는 기본적으로 `created_at` 컬럼 기준으로 결과를 정렬합니다. 정렬할 컬럼명을 직접 전달할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드로 쿼리 결과를 무작위로 정렬할 수 있습니다. 예를 들어 무작위 사용자를 조회할 때 이용합니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거하기

`reorder` 메서드는 쿼리에 적용된 모든 "order by" 절을 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 호출 시 콜럼 및 정렬 방향을 지정하면 기존 "order by" 절을 제거하고 새로운 정렬을 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화 (Grouping)

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

`groupBy`와 `having` 메서드로 쿼리를 그룹화할 수 있습니다. `having` 시그니처는 `where`와 유사합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드로 범위 필터링도 가능합니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

`groupBy`에 여러 인수를 넘겨 다중 컬럼 그룹화도 가능합니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

복잡한 `having` 절은 [`havingRaw`](#raw-methods) 메서드를 참조하세요.

<a name="limit-and-offset"></a>
### Limit 및 Offset

<a name="skip-take"></a>
#### `skip` 및 `take` 메서드

`skip`과 `take` 메서드로 쿼리 결과 제한 및 건너뛰기 설정이 가능합니다:

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

기능적으로 동일한 `limit`과 `offset` 메서드를 사용할 수도 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

특정 조건에 따라 쿼리 절을 적용하고 싶을 때가 있습니다. 예를 들어, HTTP 요청에 특정 입력이 있을 때만 `where` 절을 추가하는 경우입니다. 이런 상황에 `when` 메서드를 사용합니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when`은 첫 번째 인수가 `true`일 때만 클로저를 실행하고, `false`면 클로저를 실행하지 않습니다. 위 예에서는 `role` 필드가 존재하고 값이 `true`로 판정될 때만 where 절이 추가됩니다.

`when`에 세 번째 인수로 또 다른 클로저를 전달할 수 있는데, 이는 첫 번째 인수가 `false`일 때 실행됩니다. 이를 이용해 기본 정렬 방식을 설정하는 예시입니다:

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

쿼리 빌더는 `insert` 메서드로 데이터베이스 테이블에 레코드를 삽입할 수 있습니다. `insert`는 컬럼명과 값의 배열을 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한 번에 삽입하려면 배열 배열을 넘깁니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore`는 삽입 중 발생하는 오류를 무시합니다. 중복 레코드 오류 뿐 아니라, 데이터베이스 엔진에 따라 기타 오류도 무시될 수 있음을 유의하세요. 예를 들어, MySQL의 엄격 모드를 우회합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing`은 서브쿼리 결과를 사용해 새 레코드를 삽입할 때 사용됩니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

자동 증가하는 `id` 컬럼이 있는 테이블에 레코드를 삽입하고, 생성된 ID를 받고 싶으면 `insertGetId` 메서드를 사용하세요:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]  
> PostgreSQL에서는 `insertGetId`가 기본 증가 컬럼 이름을 `id`로 기대합니다. 다른 시퀀스에서 ID를 받고 싶으면 두 번째 인수로 컬럼명을 지정할 수 있습니다.

<a name="upserts"></a>
### 업서트 (Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고 이미 존재하는 레코드는 지정한 컬럼을 업데이트합니다. 첫 번째 인수는 삽입/업데이트할 값의 배열, 두 번째 인수는 레코드를 고유하게 식별하는 컬럼 목록, 세 번째 인수는 업데이트할 컬럼 배열입니다:

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

위 예에서는 `departure`와 `destination` 컬럼 값이 일치하는 레코드가 있으면 `price` 컬럼을 업데이트하고, 없으면 새 레코드가 삽입됩니다.

> [!WARNING]  
> SQL Server를 제외한 모든 데이터베이스는 `upsert`의 두 번째 인수 배열 컬럼에 "primary" 또는 "unique" 인덱스가 있어야 합니다. MariaDB와 MySQL은 해당 인수를 무시하고 테이블의 기본 "primary" 및 "unique" 인덱스만 사용해 기존 레코드를 감지합니다.

<a name="update-statements"></a>
## Update 문 (Update Statements)

데이터 삽입 외에도 `update` 메서드로 기존 레코드를 갱신할 수 있습니다. `update`는 컬럼과 값 쌍 배열을 받고, 영향을 받은 행 수를 반환합니다. `where` 절로 작성 대상을 제한할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 업데이트 또는 삽입

기존 레코드는 업데이트하고, 없으면 새로 삽입해야 할 때 `updateOrInsert` 메서드를 사용합니다. 두 개 인수를 받는데, 첫 번째는 레코드 조회 조건 배열, 두 번째는 업데이트 또는 삽입할 컬럼 및 값 배열입니다.

`updateOrInsert`는 첫 번째 인수 조건에 일치하는 레코드를 찾아 있으면 갱신하고, 없으면 두 인수를 합친 속성으로 새 레코드를 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

존재 여부에 따라 갱신 및 삽입할 속성을 맞춤 설정하려면 클로저를 쓸 수 있습니다:

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

JSON 컬럼을 업데이트할 때는 `->` 구문으로 키를 지정해야 합니다. MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소

쿼리 빌더는 컬럼 값을 증가 또는 감소시키는 편리한 메서드를 지원합니다. 최소 한 인수로 대상 컬럼명, 두 번째 인수로 증감할 양을 줄 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

추가 컬럼도 함께 갱신할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

여러 컬럼을 한 번에 증감하려면 `incrementEach`와 `decrementEach` 메서드를 사용하세요:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## Delete 문 (Delete Statements)

`delete` 메서드를 사용해 테이블에서 레코드를 삭제할 수 있습니다. 삭제된 행 수를 반환하며, `where` 절로 삭제 조건을 제약할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 문 실행 시 "비관적 잠금"을 지원하는 메서드도 제공합니다. "공유 잠금"을 적용하려면 `sharedLock` 메서드를 호출하세요. 공유 잠금이 설정된 행은 트랜잭션이 완료될 때까지 수정할 수 없습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

"for update" 잠금을 적용하려면 `lockForUpdate` 메서드를 사용합니다. 이 잠금은 다른 공유 잠금과 동시에 선택되거나 수정되는 것을 방지합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금은 [트랜잭션](/docs/11.x/database#database-transactions) 내에서 사용하는 것이 좋습니다. 이렇게 하면, 데이터가 완전한 작업이 끝날 때까지 변경되지 않으며, 실패 시 트랜잭션 롤백과 함께 잠금이 자동 해제됩니다:

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

<a name="debugging"></a>
## 디버깅 (Debugging)

쿼리를 작성하는 중간에 현재 쿼리 바인딩과 SQL을 출력하고 싶으면 `dd`와 `dump` 메서드를 사용할 수 있습니다. `dd`는 출력 후 실행을 중단하고, `dump`는 계속 진행합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql` 메서드는 바인딩이 치환된 완전한 SQL 문을 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```