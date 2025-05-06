# 해싱(Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호와 해시가 일치하는지 검증하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호가 다시 해시되어야 하는지 확인하기](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/{{version}}/facades)는 사용자의 비밀번호를 안전하게 저장할 수 있도록 Bcrypt와 Argon2 해싱을 제공합니다. [Laravel 어플리케이션 스타터 킷](/docs/{{version}}/starter-kits) 중 하나를 사용하고 있다면, 기본적으로 Bcrypt가 회원가입과 인증에 사용됩니다.

Bcrypt는 비밀번호 해싱에 적합한 선택지입니다. Bcrypt는 "작업 계수(work factor)"를 조정할 수 있어, 하드웨어 성능이 증가함에 따라 해시 생성 시간을 늘릴 수 있습니다. 비밀번호를 해싱할 때는 느릴수록 좋습니다. 알고리즘이 비밀번호를 해싱하는 데 오래 걸릴수록, 악의적인 사용자가 모든 가능한 문자열 해시 값을 사전 생성(레인보우 테이블)하여 공격하는 데도 더 오래 걸립니다.

<a name="configuration"></a>
## 설정

애플리케이션의 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 구성됩니다. 현재 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i 및 Argon2id 변종) 드라이버를 지원합니다.

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱

비밀번호를 해싱하려면 `Hash` 파사드의 `make` 메서드를 호출하면 됩니다:

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
        // 새로운 비밀번호 길이를 검증합니다...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 계수 조정

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드의 `rounds` 옵션을 통해 작업 계수(work factor)를 조정할 수 있습니다. 하지만, Laravel에서 관리하는 기본 작업 계수 설정도 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 계수 조정

Argon2 알고리즘을 사용하는 경우, `make` 메서드의 `memory`, `time`, `threads` 옵션을 통해 작업 계수를 조정할 수 있습니다. 하지만, Laravel에서 제공하는 기본 값도 대부분의 애플리케이션에 적합합니다:

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
### 비밀번호와 해시가 일치하는지 검증하기

`Hash` 파사드의 `check` 메서드를 사용하면, 주어진 평문 비밀번호 문자열이 특정 해시 값과 일치하는지 확인할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호가 다시 해시되어야 하는지 확인하기

`Hash` 파사드의 `needsRehash` 메서드는 해당 비밀번호 해시에 사용된 작업 계수가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정에서 이러한 체크를 수행할 수도 있습니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```