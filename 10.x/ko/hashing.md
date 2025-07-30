# 해싱 (Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱하기](#hashing-passwords)
    - [비밀번호가 해시와 일치하는지 검증하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호를 다시 해싱해야 하는지 확인하기](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
## 소개

Laravel의 `Hash` [파사드](/docs/10.x/facades)는 사용자 비밀번호 저장을 위해 안전한 Bcrypt와 Argon2 해싱을 제공합니다. 만약 [Laravel 애플리케이션 스타터 키트](/docs/10.x/starter-kits) 중 하나를 사용한다면, 기본적으로 등록과 인증에 Bcrypt가 사용됩니다.

Bcrypt는 비밀번호 해싱에 매우 적합한 선택입니다. 그 이유는 "작업 계수(work factor)"를 조절할 수 있어, 하드웨어 성능 향상에 따라 해시 생성에 필요한 시간을 늘릴 수 있기 때문입니다. 비밀번호를 해싱할 때는 느린 것이 좋습니다. 해싱 알고리즘이 비밀번호를 처리하는 데 시간이 오래 걸릴수록, 악의적인 사용자가 애플리케이션 공격에 쓰이는 무차별 대입 공격에 사용할 수 있는 모든 문자열 해시 값을 미리 계산해 저장하는 "레인보우 테이블"을 만드는 데도 시간이 오래 걸리기 때문입니다.

<a name="configuration"></a>
## 설정

애플리케이션의 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 구성됩니다. 현재 지원되는 드라이버는 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i 및 Argon2id 변형)입니다.

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱하기

`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * 사용자 비밀번호를 업데이트합니다.
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

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드의 `rounds` 옵션을 통해 작업 계수(work factor)를 조절할 수 있습니다. 하지만 Laravel에서 기본으로 관리하는 작업 계수는 대부분의 애플리케이션에 적합합니다:

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 계수 조정하기

Argon2 알고리즘을 사용하는 경우, `make` 메서드의 `memory`, `time`, `threads` 옵션으로 작업 계수를 설정할 수 있습니다. 하지만 기본 값은 대부분의 애플리케이션에 적합하게 Laravel에서 관리됩니다:

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]  
> 옵션에 관한 더 자세한 내용은 [PHP 공식 문서의 Argon 해싱](https://secure.php.net/manual/en/function.password-hash.php)을 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 검증하기

`Hash` 파사드의 `check` 메서드를 사용하면, 주어진 평문 문자열이 특정 해시와 일치하는지 확인할 수 있습니다:

```
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호를 다시 해싱해야 하는지 확인하기

`Hash` 파사드의 `needsRehash` 메서드를 사용하면, 비밀번호가 해싱된 이후 해시 알고리즘의 작업 계수가 변경되어 비밀번호를 다시 해싱해야 하는지 판단할 수 있습니다. 일부 애플리케이션은 인증 과정 중 이 검사를 수행하기도 합니다:

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```