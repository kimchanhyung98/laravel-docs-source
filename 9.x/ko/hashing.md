# 해싱

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호와 해시 일치 여부 확인](#verifying-that-a-password-matches-a-hash)
    - [비밀번호 재해싱 필요 여부 판단](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/{{version}}/facades)는 사용자 비밀번호 저장을 위한 안전한 Bcrypt 및 Argon2 해싱을 제공합니다. 만약 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 사용하고 있다면, 등록과 인증 과정에 기본적으로 Bcrypt가 사용됩니다.

Bcrypt는 비밀번호 해싱에 매우 적합한 선택입니다. 그 이유는 "작업 인자(work factor)"를 조정할 수 있기 때문인데, 이는 하드웨어 성능이 향상됨에 따라 해시 생성 소요 시간을 늘릴 수 있다는 의미입니다. 비밀번호를 해싱할 때는 느린 것이 오히려 좋습니다. 해시 알고리즘이 비밀번호를 해싱하는 데 시간이 오래 걸릴수록, 악의적인 사용자가 가능한 모든 문자열 해시 값을 미리 생성해 두는 "무지개 테이블" 공격이 어려워집니다. 느린 해싱은 무차별 대입 공격으로부터 애플리케이션을 더 잘 보호해줍니다.

<a name="configuration"></a>
## 설정

애플리케이션의 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 지정할 수 있습니다. 현재 지원되는 드라이버는 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i 및 Argon2id 변종)입니다.

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱

비밀번호를 해싱하려면 `Hash` 파사드의 `make` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * 사용자의 비밀번호를 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        // 새 비밀번호의 길이를 검증하세요...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 인자(work factor) 조정

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션을 통해 작업 인자를 설정할 수 있습니다. 하지만 Laravel에서 관리하는 기본값이 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 인자(work factor) 조정

Argon2 알고리즘을 사용하는 경우, `make` 메서드에서 `memory`, `time`, `threads` 옵션을 활용해 작업 인자를 조정할 수 있습니다. 그러나 Laravel이 제공하는 기본값도 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> **참고**
> 이러한 옵션에 대한 자세한 내용은 [공식 PHP Argon 해싱 문서](https://secure.php.net/manual/en/function.password-hash.php)를 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호와 해시 일치 여부 확인

`Hash` 파사드의 `check` 메서드를 사용하면 입력한 평문 문자열이 특정 해시와 일치하는지 확인할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호 재해싱 필요 여부 판단

`Hash` 파사드의 `needsRehash` 메서드를 사용하면 비밀번호가 해싱된 이후로 해싱기의 작업 인자가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정 중에 이 확인을 수행하기도 합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```