# 해싱(Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호가 해시와 일치하는지 검증](#verifying-that-a-password-matches-a-hash)
    - [비밀번호가 재해시(rehash)되어야 하는지 확인](#determining-if-a-password-needs-to-be-rehashed)
- [해시 알고리즘 검증](#hash-algorithm-verification)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/{{version}}/facades)는 사용자 비밀번호 저장을 위한 안전한 Bcrypt 및 Argon2 해싱 기능을 제공합니다. [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 사용하는 경우, 회원가입 및 인증 기본 해싱 알고리즘으로 Bcrypt가 사용됩니다.

Bcrypt는 "작업 인자(work factor)"를 조정할 수 있기 때문에 비밀번호 해싱에 매우 적합합니다. 즉, 하드웨어 성능이 증가할수록 해시 생성에 소요되는 시간을 증가시킬 수 있습니다. 비밀번호를 해시할 때는 느린 것이 좋습니다. 알고리즘이 비밀번호 해싱에 더 오랜 시간이 걸릴수록 악의적인 사용자가 무차별 대입 공격에 사용할 수 있는 모든 문자열의 해시값 목록인 "레인보우 테이블"을 생성하는 데 더 많은 시간이 걸립니다.

<a name="configuration"></a>
## 설정

기본적으로 Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 그러나 [argon](https://en.wikipedia.org/wiki/Argon2) 및 [argon2id](https://en.wikipedia.org/wiki/Argon2) 등 여러 다른 해싱 드라이버도 지원합니다.

애플리케이션의 해싱 드라이버는 `HASH_DRIVER` 환경 변수를 사용해 지정할 수 있습니다. 하지만 Laravel의 해싱 드라이버 옵션 전체를 직접 커스터마이즈하고 싶다면, `config:publish` Artisan 명령어로 전체 `hashing` 설정 파일을 퍼블리시해야 합니다:

```shell
php artisan config:publish hashing
```

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱

`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해시할 수 있습니다:

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
        // 새로운 비밀번호 길이 검증...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 인자(work factor) 조정

Bcrypt 알고리즘을 사용할 경우, `make` 메서드에서 `rounds` 옵션을 활용해 알고리즘의 작업 인자를 직접 조정할 수 있습니다. 그러나 Laravel이 관리하는 기본 작업 인자는 대부분의 애플리케이션에서 적절합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 인자(work factor) 조정

Argon2 알고리즘을 사용할 경우, `make` 메서드에서 `memory`, `time`, `threads` 옵션으로 작업 인자를 조정할 수 있습니다. 하지만 Laravel이 관리하는 기본값도 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이러한 옵션에 대한 자세한 내용은 [공식 PHP Argon 해싱 문서](https://secure.php.net/manual/en/function.password-hash.php)를 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 검증

`Hash` 파사드가 제공하는 `check` 메서드를 사용하면 특정 평문 문자열이 지정된 해시값과 일치하는지 검증할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호가 재해시(rehash)되어야 하는지 확인

`Hash` 파사드의 `needsRehash` 메서드를 사용하면 해시를 생성할 때 사용된 작업 인자가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정에서 이 검사를 수행하기도 합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
## 해시 알고리즘 검증

해시 알고리즘 변조를 방지하기 위해, Laravel의 `Hash::check` 메서드는 우선 주어진 해시값이 애플리케이션에서 선택된 해시 알고리즘으로 생성된 것인지 검증합니다. 만약 알고리즘이 다르다면 `RuntimeException` 예외가 발생합니다.

이는 대부분의 애플리케이션에서 기대되는 동작이며, 해싱 알고리즘이 변경되지 않았다는 것을 전제로 합니다. 다양한 알고리즘이 입력되는 경우 악의적인 공격의 신호가 될 수 있습니다. 하지만 한 알고리즘에서 다른 알고리즘으로 마이그레이션하는 등, 애플리케이션에서 여러 해싱 알고리즘을 지원해야 하는 경우에는 `HASH_VERIFY` 환경 변수를 `false`로 설정하여 해시 알고리즘 검증을 비활성화할 수 있습니다:

```ini
HASH_VERIFY=false
```