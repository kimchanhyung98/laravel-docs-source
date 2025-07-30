# 데이터베이스: 쿼리 빌더 (Database: Query Builder)

- [소개](#introduction)
- [데이터베이스 쿼리 실행](#running-database-queries)
    - [결과 청크 처리(Chunking Results)](#chunking-results)
    - [결과를 늦게 스트리밍하기(Streaming Results Lazily)](#streaming-results-lazily)
    - [집계 함수(Aggregates)](#aggregates)
- [Select 문](#select-statements)
- [원시 표현식(Raw Expressions)](#raw-expressions)
- [조인(Joins)](#joins)
- [유니언(Unions)](#unions)
- [기본 Where 절(Basic Where Clauses)](#basic-where-clauses)
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
    - [전문 검색 Where 절](#full-text-where-clauses)
- [정렬, 그룹화, 제한과 오프셋](#ordering-grouping-limit-and-offset)
    - [정렬](#ordering)
    - [그룹화](#grouping)
    - [제한과 오프셋](#limit-and-offset)
- [조건부 절](#conditional-clauses)
- [삽입문(Insert Statements)](#insert-statements)
    - [업서트(Upserts)](#upserts)
- [업데이트문(Update Statements)](#update-statements)
    - [JSON 컬럼 업데이트](#updating-json-columns)
    - [증가 및 감소(Increment and Decrement)](#increment-and-decrement)
- [삭제문(Delete Statements)](#delete-statements)
- [비관적 잠금(Pessimistic Locking)](#pessimistic-locking)
- [디버깅(Debugging)](#debugging)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 데이터베이스 쿼리 빌더는 데이터베이스 쿼리를 생성하고 실행하기 위한 편리하고 유창한 인터페이스를 제공합니다. 이 도구는 애플리케이션 내 대부분의 데이터베이스 작업을 수행하는 데 사용되며, Laravel이 지원하는 모든 데이터베이스 시스템과 완벽히 호환됩니다.

Laravel 쿼리 빌더는 PDO 파라미터 바인딩을 사용하여 SQL 인젝션 공격으로부터 애플리케이션을 보호합니다. 따라서 쿼리 바인딩에 전달되는 문자열을 별도로 클린징하거나 세정할 필요가 없습니다.

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 쿼리에 참조되는 컬럼명, 특히 "order by" 컬럼명을 사용자 입력이 결정하도록 절대 허용해서는 안 됩니다.

<a name="running-database-queries"></a>
## 데이터베이스 쿼리 실행 (Running Database Queries)

<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 조회하기

`DB` 파사드가 제공하는 `table` 메서드를 사용하여 쿼리를 시작할 수 있습니다. `table` 메서드는 지정한 테이블에 대한 쿼리 빌더 인스턴스를 반환하며, 이 인스턴스를 통해 추가 제약 조건들을 연쇄 연결한 뒤 최종적으로 `get` 메서드를 호출하여 결과를 가져올 수 있습니다:

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

`get` 메서드는 쿼리 결과를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과 항목은 PHP의 `stdClass` 객체입니다. 각 열의 값은 해당 객체의 속성에 접근하여 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```

> [!NOTE]
> Laravel 컬렉션은 데이터 매핑과 축약에 매우 강력한 다양한 메서드를 제공합니다. Laravel 컬렉션에 대한 자세한 내용은 [컬렉션 문서](/docs/master/collections)를 참고하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 / 컬럼 조회하기

데이터베이스 테이블에서 단일 행만 조회하려면 `DB` 파사드의 `first` 메서드를 이용할 수 있습니다. 이 메서드는 하나의 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```

만약 일치하는 행이 없을 경우 `Illuminate\Database\RecordNotFoundException` 예외를 발생시키고 싶다면, `firstOrFail` 메서드를 사용하세요. 예외가 처리되지 않으면 404 HTTP 응답이 자동으로 클라이언트에 반환됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```

전체 행이 필요 없고 특정 값만 조회하고 싶으면 `value` 메서드를 사용하세요. 이 메서드는 지정된 컬럼의 값만 직접 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```

`id` 컬럼 값으로 단일 행을 조회하려면 `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```

<a name="retrieving-a-list-of-column-values"></a>
#### 단일 컬럼 값 목록 조회하기

단일 컬럼의 값만 모아서 `Illuminate\Support\Collection` 인스턴스로 받고 싶다면 `pluck` 메서드를 사용하세요. 예를 들어 사용자들의 `title` 컬렉션을 조회합니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```

두 번째 인자로 키로 사용할 컬럼명을 제공하면 결과 컬렉션의 키를 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리 (Chunking Results)

수천 건의 데이터 레코드를 처리해야 할 경우, `DB` 파사드에서 제공하는 `chunk` 메서드를 고려하세요. 이 메서드는 한 번에 작은 양씩 결과를 가져와서 각 청크를 클로저로 전달해 처리합니다. 예를 들어, `users` 테이블을 한 번에 100개씩 청크 단위로 가져오는 방법은 다음과 같습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```

클로저에서 `false`를 반환하면 이후 청크 처리를 중단할 수 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // 레코드 처리...

    return false;
});
```

청크 처리 중에 데이터베이스 레코드를 수정할 계획이라면 결과가 예상치 않게 바뀔 수 있습니다. 이 경우 `chunkById` 메서드를 사용하는 것이 가장 좋습니다. 이 메서드는 기본 키(id)를 기준으로 자동 페이징하여 결과를 안전하게 순회합니다:

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

`chunkById`와 `lazyById` 메서드는 자체적으로 쿼리에 "where" 조건을 추가하므로, 일반적으로 사용자 조건은 클로저 내에서 [논리적 그룹화](#logical-grouping)로 묶는 것이 좋습니다:

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
> 청크 콜백 내에서 레코드를 수정하거나 삭제할 경우, 기본 키 또는 외래 키 값 변경으로 인해 일부 레코드가 청크 결과에 포함되지 않을 수 있으니 주의하세요.

<a name="streaming-results-lazily"></a>
### 결과를 늦게 스트리밍하기 (Streaming Results Lazily)

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행하지만, 각 청크를 콜백에 전달하지 않고 [`LazyCollection`](/docs/master/collections#lazy-collections)을 반환하여 결과 전체를 스트림처럼 처리할 수 있게 해줍니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```

레코드 업데이트 작업이 필요하다면, `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 좋습니다. 이 메서드는 기본 키를 기준으로 자동 페이징합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```

> [!WARNING]
> 반복 처리 중 레코드 수정이나 삭제 시, 기본 키 및 외래 키 변경으로 인해 결과에서 누락되는 레코드가 발생할 수 있으니 주의하세요.

<a name="aggregates"></a>
### 집계 함수 (Aggregates)

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum` 같은 집계 값을 가져오기 위한 다양한 메서드를 제공합니다. 쿼리를 생성한 뒤 이들 메서드를 호출하세요:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```

물론, 이 메서드들은 다른 조건절과 조합하여 더욱 세밀한 집계 계산이 가능합니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```

<a name="determining-if-records-exist"></a>
#### 레코드 존재 유무 확인하기

쿼리 조건에 맞는 레코드 존재 여부를 확인할 때 `count` 대신 `exists` 또는 `doesntExist` 메서드를 사용하면 더 효율적입니다:

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
#### Select 절 지정하기

테이블에서 항상 모든 컬럼을 조회할 필요는 없습니다. `select` 메서드를 사용하면 쿼리를 위한 맞춤형 "select" 절을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```

`distinct` 메서드는 쿼리 결과에서 중복을 제거하도록 할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```

이미 쿼리 빌더 인스턴스가 있고 여기에 컬럼을 추가하려면 `addSelect` 메서드를 사용하세요:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```

<a name="raw-expressions"></a>
## 원시 표현식 (Raw Expressions)

가끔 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. 이럴 땐 `DB` 파사드가 제공하는 `raw` 메서드를 사용해 원시 문자열 표현식을 만들 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```

> [!WARNING]
> 원시 쿼리문은 문자열 그대로 쿼리에 삽입되므로 SQL 인젝션 취약점이 생기지 않도록 반드시 매우 조심해야 합니다.

<a name="raw-methods"></a>
### 원시 메서드 (Raw Methods)

`DB::raw` 대신 아래 메서드들을 통해 쿼리의 여러 부분에 원시 표현식을 삽입할 수 있습니다. **Laravel은 원시 표현식을 사용한 쿼리가 SQL 인젝션 취약점으로부터 안전하다고 보장하지 않습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있으며, 두 번째 인자로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```

<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw`와 `orWhereRaw` 메서드는 원시 "where" 절을 쿼리에 삽입할 때 사용합니다. 두 번째 인자로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```

<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw` 및 `orHavingRaw` 메서드는 "having" 절에 원시 문자열을 전달할 수 있습니다. 두 번째 인자로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```

<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절에 원시 문자열을 지정할 수 있습니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```

<a name="groupbyraw"></a>
### `groupByRaw`

`groupByRaw` 메서드는 `group by` 절에 원시 문자열을 지정할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```

<a name="joins"></a>
## 조인 (Joins)

<a name="inner-join-clause"></a>
#### 내부 조인(Inner Join) 절

기본적인 "inner join"을 수행하려면 쿼리 빌더 인스턴스에서 `join` 메서드를 사용하세요. 첫 번째 인자는 조인할 테이블 이름이고, 나머지 인자는 조인 조건으로 사용할 컬럼 제약입니다. 하나의 쿼리에서 여러 테이블을 조인하는 것도 가능합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```

<a name="left-join-right-join-clause"></a>
#### 왼쪽 조인(Left Join) / 오른쪽 조인(Right Join) 절

"inner join" 대신 "left join"이나 "right join"이 필요하면 `leftJoin` 또는 `rightJoin` 메서드를 사용하세요. 이들 메서드는 `join`과 동일한 인자 서명을 갖습니다:

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

`crossJoin` 메서드는 "cross join"을 수행할 때 사용합니다. 크로스 조인은 첫 번째 테이블과 조인하는 테이블 간의 카르테시안 곱을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```

<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 복잡한 조인 조건을 지정하려면 `join` 메서드의 두 번째 인자로 클로저를 전달하세요. 이 클로저는 "join" 절의 조건을 지정할 수 있는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받습니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```

조인 조건에 "where" 절을 사용하려면 `JoinClause` 인스턴스의 `where` 및 `orWhere` 메서드를 사용하세요. 이들 메서드는 컬럼과 값 간 비교를 수행합니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```

<a name="subquery-joins"></a>
#### 서브쿼리 조인 (Subquery Joins)

`joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용하여 쿼리를 서브쿼리와 조인할 수 있습니다. 세 메서드 모두 세 개의 인자를 받으며, 첫 번째는 서브쿼리, 두 번째는 서브쿼리의 테이블 별칭, 세 번째는 연관 컬럼을 정의하는 클로저입니다. 예를 들어 사용자 별로 가장 최근에 작성한 블로그 게시물의 `created_at` 타임스탬프를 포함하는 결과를 쿼리할 수 있습니다:

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

`joinLateral`과 `leftJoinLateral` 메서드를 사용하면 서브쿼리와 "lateral join"을 수행할 수 있습니다. 이들 메서드는 두 개의 인자를 받는데, 첫 번째는 서브쿼리, 두 번째는 테이블 별칭입니다. 조인 조건은 서브쿼리 내 `where` 절에서 지정합니다. 래터럴 조인은 각 행마다 평가되며, 서브쿼리 외부의 컬럼을 참조할 수 있습니다.

아래 예시는 사용자들과 각 사용자별 최근 세 개의 블로그 게시물을 함께 조회하는 예입니다. 각 사용자는 최대 3개의 행을 결과로 생성할 수 있습니다. 조인 조건은 서브쿼리 내 `whereColumn` 절을 통해 현재 사용자 행을 참조합니다:

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

쿼리 빌더는 두 개 이상의 쿼리를 "union"하는 편리한 메서드를 제공합니다. 예를 들어 초기 쿼리를 생성한 뒤 `union` 메서드로 다른 쿼리와 합칠 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$first = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($first)
    ->get();
```

`union` 외에도 `unionAll` 메서드가 제공되며, 이 메서드는 중복 결과를 제거하지 않고 단순 병합합니다. 서명(signature)은 `union`과 동일합니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절 (Basic Where Clauses)

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드는 쿼리에 "where" 절을 추가하는 데 사용됩니다. 가장 기본적인 호출은 세 개의 인자를 받는데, 첫 번째가 컬럼명, 두 번째가 연산자(데이터베이스가 지원하는 모든 연산 가능), 세 번째가 비교할 값입니다.

예를 들어 `votes` 컬럼 값이 `100`이고 `age`가 `35` 초과인 사용자를 조회하려면 다음과 같습니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```

편의를 위해, `=` 연산자인 경우 두 번째 인자에 값만 전달해도 됩니다. 이 경우 Laravel은 자동으로 `=` 연산자로 인식합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```

지원되는 연산자는 데이터베이스에 따라 다양하며, 아래처럼 다양한 연산자를 지정할 수 있습니다:

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

또한 여러 조건을 배열 형태로 전달할 수도 있습니다. 배열의 각 원소는 `where` 메서드에 전달되는 세 인자의 배열이어야 합니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```

> [!WARNING]
> PDO는 컬럼명 바인딩을 지원하지 않습니다. 따라서 사용자 입력이 쿼리의 컬럼명을 결정하도록 절대 허용해서는 안 됩니다. 특히 "order by" 컬럼명을 포함합니다.

> [!WARNING]
> MySQL과 MariaDB는 문자열과 숫자를 비교할 때 문자열을 자동으로 정수로 형 변환합니다. 비숫자 문자열은 `0`으로 변환되어 예상치 못한 결과를 초래할 수 있습니다. 예를 들어 테이블에 `secret` 컬럼 값이 `aaa`인 행이 있는데 `User::where('secret', 0)`을 실행하면 해당 행이 반환됩니다. 이런 상황을 피하려면 쿼리에서 사용하는 값들을 적절한 타입으로 미리 변환해야 합니다.

<a name="or-where-clauses"></a>
### Or Where 절

`where` 메서드를 연속해서 호출하면 "where" 절들은 `AND` 연산자로 묶입니다. 하지만 `orWhere` 메서드를 사용하면 `OR` 연산자로 조건을 추가할 수 있습니다. `orWhere` 메서드는 `where` 메서드와 동일한 인자를 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```

`orWhere` 절을 괄호로 묶어 그룹화해야 할 땐, `orWhere`에 클로저를 전달해 그룹을 지정할 수 있습니다:

```php
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
> 전역 스코프가 적용되는 상황에서 예상치 못한 쿼리 동작을 방지하려면 항상 `orWhere` 호출을 그룹으로 묶어야 합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드를 사용하면 주어진 쿼리 제약 조건 그룹을 부정할 수 있습니다. 예를 들어, 클리어런스 중이거나 가격이 10 미만인 제품은 제외시키는 쿼리는 다음과 같습니다:

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

한 번에 여러 컬럼에 같은 조건을 적용해야 할 때가 있습니다. 예를 들어 특정 목록 내 모든 컬럼 중 하나라도 지정된 패턴을 포함하는 레코드를 조회하려면 `whereAny` 메서드를 사용합니다:

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

위 쿼리는 다음 SQL을 생성합니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```

반대로 모든 컬럼이 조건을 만족해야 할 경우 `whereAll` 메서드를 사용합니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```

위 쿼리는 다음 SQL을 생성합니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```

`whereNone` 메서드는 지정한 컬럼 중 어느 것도 조건에 만족하지 않는 레코드를 조회합니다:

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

위 쿼리는 다음 SQL을 생성합니다:

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

Laravel은 JSON 컬럼 타입을 지원하는 데이터베이스에서 JSON 컬럼 쿼리를 지원합니다. MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, SQLite 3.39.0+가 이에 해당합니다. JSON 컬럼을 쿼리하려면 `->` 연산자를 사용합니다:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();
```

`whereJsonContains` 메서드를 사용하여 JSON 배열에서 특정 값을 찾을 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();
```

MariaDB, MySQL, PostgreSQL 데이터베이스인 경우 배열 형태로 다중 값을 탐색할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();
```

`whereJsonLength` 메서드는 JSON 배열의 길이를 조건으로 사용합니다:

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

`whereLike` 메서드는 문자열 패턴 매칭 "LIKE" 절을 추가할 때 사용합니다. 데이터베이스에 무관한 방식으로 문자열 매칭을 수행할 수 있으며, 대소문자 구분 옵션도 활성화할 수 있습니다. 기본은 대소문자 구분 없음입니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```

`caseSensitive` 인자를 `true`로 전달하면 대소문자 구분 검색이 활성화됩니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```

`orWhereLike` 메서드는 "or" 조건의 LIKE 절을 추가합니다:

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

`orWhereNotLike`는 "or NOT LIKE" 절을 추가합니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```

> [!WARNING]
> `whereLike`의 대소문자 구분 옵션은 현재 SQL Server에서는 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 컬럼 값이 지정 배열 안에 포함되는지 검사합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```

`whereNotIn`은 컬럼 값이 지정 배열에 포함되지 않는지 검사합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```

`whereIn`에 쿼리 객체를 두 번째 인자로 전달할 수도 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$users = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```

위 쿼리는 다음 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```

> [!WARNING]
> 대용량 정수 배열 바인딩이 필요한 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하면 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼이 두 값 사이에 있는지 검사합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```

**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼이 두 값 사이에 있지 않은지 검사합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```

**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns`는 같은 행 내 두 컬럼 값 사이에 컬럼 값이 있는지 검사합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

`whereNotBetweenColumns`는 같은 행 내 두 컬럼 값 밖에 컬럼 값이 있는지 검사합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```

**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull`은 지정 컬럼 값이 `NULL`인지 검사합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```

`whereNotNull`은 지정 컬럼 값이 `NULL`이 아닌지 검사합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```

**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate`는 컬럼 값이 특정 날짜인지 검사합니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```

`whereMonth`는 컬럼 값이 특정 월인지 검사합니다:

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```

`whereDay`는 컬럼 값이 특정 일인지 검사합니다:

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```

`whereYear`는 컬럼 값이 특정 연도인지 검사합니다:

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```

`whereTime`은 컬럼 값이 특정 시간과 일치하는지 검사합니다:

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```

**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast`와 `whereFuture` 메서드는 컬럼 값이 과거인지 미래인지 확인합니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```

`whereNowOrPast`와 `whereNowOrFuture`는 현재 시점 포함 과거/미래 조건을 검사합니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```

`whereToday`, `whereBeforeToday`, `whereAfterToday`는 각각 오늘, 오늘 이전, 오늘 이후인지 검사합니다:

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

`whereTodayOrBefore`와 `whereTodayOrAfter`는 오늘 포함 앞/뒤인지를 검사합니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```

**whereColumn / orWhereColumn**

`whereColumn`은 두 컬럼 값이 동일한지 검사합니다:

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

여러 컬럼 비교 조건을 배열로 전달하고 `and` 연산자로 묶을 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```

<a name="logical-grouping"></a>
### 논리적 그룹화 (Logical Grouping)

여러 "where" 절을 괄호로 묶어 쿼리의 논리적 그룹화를 명확히 해야 할 경우, `where` 메서드에 클로저를 전달하세요:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```

위 예제는 다음 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```

> [!WARNING]
> 전역 스코프 적용 시 예상치 못한 동작을 피하기 위해 `orWhere` 호출은 항상 그룹으로 묶어야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절 (Advanced Where Clauses)

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 작성할 수 있습니다. 클로저를 통해 내부 쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```

클로저 대신 쿼리 객체도 전달할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```

두 예제 모두 다음과 같은 SQL을 생성합니다:

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

서브쿼리 결과와 값을 비교하는 "where" 절을 만들고 싶으면 클로저와 값을 `where` 메서드에 넘기면 됩니다. 예를 들어, 최근 "membership" 타입이 특정 값인 사용자를 조회합니다:

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

또는 컬럼을 서브쿼리 결과와 비교할 수도 있습니다:

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```

<a name="full-text-where-clauses"></a>
### 전문 검색 Where 절 (Full Text Where Clauses)

> [!WARNING]
> 전문 검색 Where 절은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

`whereFullText`와 `orWhereFullText` 메서드를 사용하여 [전문 인덱스](/docs/master/migrations#available-index-types)가 설정된 컬럼에 전문 검색 조건을 추가할 수 있습니다. Laravel은 내부 데이터베이스 시스템에 맞게 적절하게 SQL 구문(예: `MATCH AGAINST`)으로 변환합니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```

<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한과 오프셋 (Ordering, Grouping, Limit and Offset)

<a name="ordering"></a>
### 정렬 (Ordering)

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 특정 컬럼으로 정렬하는 데 사용합니다. 첫 번째 인자는 정렬할 컬럼명, 두 번째 인자는 정렬 방향(`asc` 또는 `desc`)입니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```

복수 컬럼으로 정렬하려면 `orderBy`를 여러 번 호출하면 됩니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```

<a name="latest-oldest"></a>
#### `latest`와 `oldest` 메서드

`latest`와 `oldest` 메서드는 날짜 컬럼 기준으로 결과를 쉽게 정렬하게 해줍니다. 기본적으로 `created_at` 컬럼으로 정렬하며, 원하는 컬럼명을 인자로 전달할 수 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```

<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 메서드는 쿼리 결과를 무작위로 정렬합니다. 예를 들어 임의의 사용자를 가져올 때 사용합니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```

<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거하기

`reorder` 메서드를 호출하면 쿼리에 적용된 모든 "order by" 절이 제거됩니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```

`reorder` 메서드에 컬럼명과 방향을 넘기면 기존 "order by"를 모두 제거하고 새 정렬 조건을 적용합니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```

<a name="grouping"></a>
### 그룹화 (Grouping)

<a name="groupby-having"></a>
#### `groupBy`와 `having` 메서드

`groupBy`와 `having` 메서드는 쿼리 결과 그룹화에 사용됩니다. `having` 메서드 서명은 `where` 메서드와 유사합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```

`havingBetween` 메서드는 범위 내 값을 필터링할 때 유용합니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```

여러 컬럼으로 그룹화하려면 `groupBy`에 인자를 여러 개 전달하세요:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```

더 복잡한 `having` 조건은 [`havingRaw`](#raw-methods) 메서드를 참조하세요.

<a name="limit-and-offset"></a>
### 제한과 오프셋 (Limit and Offset)

<a name="skip-take"></a>
#### `skip`과 `take` 메서드

`skip`과 `take` 메서드를 사용해 쿼리 결과의 시작 위치 건수 조절이나 반환 레코드 개수를 제한할 수 있습니다:

```php
$users = DB::table('users')->skip(10)->take(5)->get();
```

동일한 기능의 `offset`과 `limit` 메서드도 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```

<a name="conditional-clauses"></a>
## 조건부 절 (Conditional Clauses)

특정 조건에 따라 쿼리 절을 적용하고 싶을 때 `when` 메서드를 사용하면 편리합니다. 예를 들어 HTTP 요청의 입력 값이 존재할 때만 `where` 절을 추가하려면 다음과 같이 합니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```

`when` 메서드는 첫 번째 인자가 `true`일 때만 클로저를 실행합니다. `false`면 클로저는 실행되지 않습니다.

세 번째 인자로 또 다른 클로저를 넘기면, 첫 번째 인자가 `false`일 때 실행 가능한 기본 동작도 정의할 수 있습니다. 예를 들어 정렬 기본값 설정하기:

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
## 삽입문 (Insert Statements)

쿼리 빌더는 `insert` 메서드를 통해 데이터베이스에 레코드를 삽입할 수 있습니다. `insert` 메서드는 컬럼명과 값을 키-값 배열로 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```

여러 레코드를 한꺼번에 삽입하려면 배열의 배열을 전달하세요:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```

`insertOrIgnore`는 삽입 도중 오류를 무시합니다. 중복 레코드 오류뿐만 아니라 DB 엔진에 따라 다른 오류도 무시될 수 있습니다. 예를 들어 MySQL에서 strict 모드를 우회합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```

`insertUsing`은 서브쿼리 결과를 이용해 새 레코드를 삽입할 때 사용합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->subMonth()));
```

<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

자동 증가 ID가 있는 테이블에서는 `insertGetId` 메서드를 사용해 레코드를 삽입하고 방금 생성한 ID를 얻을 수 있습니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```

> [!WARNING]
> PostgreSQL에서는 `insertGetId`가 기본적으로 `id`라는 자동 증가 컬럼 이름을 기대합니다. 다른 시퀀스에서 ID를 가져오려면 두 번째 매개변수로 컬럼명을 전달하세요.

<a name="upserts"></a>
### 업서트 (Upserts)

`upsert` 메서드는 존재하지 않는 레코드는 삽입하고, 기존 레코드는 지정한 값으로 업데이트합니다. 첫 번째 인자는 삽입 또는 업데이트할 값들의 배열, 두 번째 인자는 레코드를 고유하게 식별할 열 목록, 세 번째 인자는 업데이트할 열 목록입니다:

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

위 코드에서 `departure`와 `destination`이 같은 기존 레코드는 `price`가 업데이트됩니다.

> [!WARNING]
> SQL Server 외 모든 데이터베이스는 두 번째 인자의 컬럼들에 "primary" 또는 "unique" 인덱스가 있어야 합니다. MariaDB, MySQL 드라이버는 두 번째 인자를 무시하고 테이블의 "primary"와 "unique" 인덱스를 자동 사용합니다.

<a name="update-statements"></a>
## 업데이트문 (Update Statements)

쿼리 빌더의 `update` 메서드를 통해 기존 레코드를 업데이트할 수 있습니다. `update`는 컬럼-값 쌍 배열을 인자로 받고, 영향을 받은 행 수를 반환합니다. `where` 절로 업데이트 조건을 제한할 수도 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```

<a name="update-or-insert"></a>
#### 업데이트 또는 삽입 (Update or Insert)

기존 레코드가 있으면 업데이트하고, 없으면 삽입하는 작업을 원하면 `updateOrInsert` 메서드를 사용하세요. 두 개의 배열 인자를 받는데, 첫 번째에는 조건용 컬럼-값 쌍, 두 번째에는 업데이트할 컬럼-값 쌍이 들어갑니다.

`updateOrInsert`는 조건 배열로 레코드를 찾고, 존재하면 업데이트, 없으면 병합한 값으로 새 레코드를 삽입합니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```

또는 클로저를 두 번째 인자로 전달해 레코드 존재 여부에 따라 삽입 또는 업데이트할 속성을 동적으로 지정할 수 있습니다:

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

JSON 컬럼 내 특정 키를 업데이트할 땐 `->` 구문을 사용해야 하며, MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```

<a name="increment-and-decrement"></a>
### 증가 및 감소 (Increment and Decrement)

쿼리 빌더는 지정 컬럼 값을 손쉽게 증가 또는 감소하는 메서드를 제공합니다. 첫 인자로 컬럼명, 두 번째 인자로 증감량을 받습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```

증가/감소 작업 중 추가 컬럼도 같이 업데이트할 수 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```

또한 여러 컬럼에 한 번에 증감을 적용하는 `incrementEach`와 `decrementEach` 메서드도 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```

<a name="delete-statements"></a>
## 삭제문 (Delete Statements)

`delete` 메서드는 테이블에서 레코드를 삭제하며, 영향을 받은 행 수를 반환합니다. 삭제 대상 지정 시 `where` 절로 조건을 걸 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```

<a name="pessimistic-locking"></a>
## 비관적 잠금 (Pessimistic Locking)

쿼리 빌더는 `select` 문 실행 시 "비관적 잠금"을 수행하는 메서드를 제공합니다. `sharedLock` 메서드는 "공유 잠금"(shared lock)을 수행하여 트랜잭션이 커밋될 때까지 선택된 행의 수정을 막습니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```

`lockForUpdate` 메서드는 "for update" 잠금을 실행하여, 선택된 레코드가 다른 공유 잠금이나 수정에서 보호되도록 합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```

비관적 잠금은 [트랜잭션](/docs/master/database#database-transactions) 내에서 사용하는 게 좋습니다. 이렇게 하면 전체 작업이 완료될 때까지 잠금이 유지되어 데이터가 변경되지 않음을 보장하며, 작업 실패 시 잠금을 해제하고 롤백합니다:

```php
DB::transaction(function () {
    $sender = DB::table('users')
        ->lockForUpdate()
        ->find(1);

    $receiver = DB::table('users')
        ->lockForUpdate();
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

쿼리 작성 과정에서 현재 SQL과 바인딩 값을 확인하려면 `dd`와 `dump` 메서드를 사용하세요. `dd`는 정보를 출력 후 실행을 중단하고, `dump`는 출력 후 실행을 계속합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```

`dumpRawSql`과 `ddRawSql` 메서드는 바인딩이 쿼리에 삽입된 상태로 SQL을 출력합니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```