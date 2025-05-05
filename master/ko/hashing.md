# 해싱(Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱하기](#hashing-passwords)
    - [비밀번호가 해시와 일치하는지 확인하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호의 재해시(재해싱) 필요 여부 판단하기](#determining-if-a-password-needs-to-be-rehashed)
- [해시 알고리즘 검증](#hash-algorithm-verification)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/{{version}}/facades)는 사용자 비밀번호 저장을 위한 안전한 Bcrypt와 Argon2 해싱을 제공합니다. [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits) 중 하나를 사용 중이라면, 기본적으로 Bcrypt가 회원가입 및 인증에 사용됩니다.

Bcrypt는 비밀번호 해싱에 매우 좋은 선택입니다. 그 이유는 "작업 계수(work factor)"가 조정 가능하므로, 하드웨어 성능이 높아짐에 따라 해시 생성에 걸리는 시간을 늘릴 수 있기 때문입니다. 비밀번호 해싱에서는 느릴수록 좋습니다. 알고리즘이 비밀번호를 해싱하는 데 더 오래 걸릴수록, 악의적인 사용자가 모든 가능한 문자열 해시 값의 "레인보우 테이블"을 생성하는 데 더 많은 시간이 소요되어, 애플리케이션을 대상으로 한 무차별 대입 공격을 어렵게 만듭니다.

<a name="configuration"></a>
## 설정

기본적으로, Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 그러나 [`argon`](https://en.wikipedia.org/wiki/Argon2)과 [`argon2id`](https://en.wikipedia.org/wiki/Argon2)를 포함한 여러 가지 다른 해싱 드라이버도 지원합니다.

애플리케이션의 해싱 드라이버는 `HASH_DRIVER` 환경 변수로 지정할 수 있습니다. 하지만 Laravel의 해싱 드라이버 옵션 전체를 커스터마이즈 하고 싶다면, `config:publish` Artisan 명령어를 사용해 전체 `hashing` 설정 파일을 게시해야 합니다:

```shell
php artisan config:publish hashing
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱하기

`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * 사용자의 비밀번호를 업데이트합니다.
     */
    public function update(Request $request): RedirectResponse
    {
        // 새 비밀번호 길이 유효성 검사...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 계수 조정하기

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션을 이용해 작업 계수를 관리할 수 있습니다. 다만, Laravel이 기본적으로 관리하는 작업 계수는 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 계수 조정하기

Argon2 알고리즘을 사용하는 경우에는, `make` 메서드에서 `memory`, `time`, `threads` 옵션을 통해 작업 계수를 조절할 수 있습니다. 하지만 Laravel에서 관리하는 기본값 역시 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이러한 옵션에 대한 더 자세한 정보는 [공식 PHP의 Argon 해싱 문서](https://secure.php.net/manual/en/function.password-hash.php)를 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 확인하기

`Hash` 파사드의 `check` 메서드를 사용하면 주어진 평문 문자열이 해당 해시와 일치하는지 검증할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호의 재해시(재해싱) 필요 여부 판단하기

`Hash` 파사드의 `needsRehash` 메서드를 사용하면, 해싱에 사용된 작업 계수가 바뀌었는지(즉, 비밀번호를 재해싱해야 하는지) 판단할 수 있습니다. 일부 애플리케이션에서는 인증 과정에서 이 검사를 수행하기도 합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
## 해시 알고리즘 검증

해시 알고리즘 조작을 방지하기 위해, Laravel의 `Hash::check` 메서드는 먼저 주어진 해시가 애플리케이션에서 선택한 해싱 알고리즘으로 생성되었는지 검증합니다. 만약 알고리즘이 다를 경우, `RuntimeException` 예외가 발생합니다.

이는 대부분의 애플리케이션에서 기대되는 동작으로, 해싱 알고리즘이 변경될 일이 없고, 서로 다른 알고리즘은 악의적인 공격일 수 있기 때문입니다. 그러나, 하나의 애플리케이션 내에서 여러 해싱 알고리즘을 지원해야 할 경우(예: 알고리즘 이전 중), `HASH_VERIFY` 환경 변수를 `false`로 설정하여 해시 알고리즘 검증을 비활성화할 수 있습니다:

```ini
HASH_VERIFY=false
```
