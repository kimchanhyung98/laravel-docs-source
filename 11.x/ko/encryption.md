# 암호화 (Encryption)

- [소개](#introduction)
- [설정](#configuration)
    - [암호화 키 원활한 교체](#gracefully-rotating-encryption-keys)
- [Encrypter 사용법](#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel의 암호화 서비스는 OpenSSL을 통해 AES-256 및 AES-128 암호화를 사용하여 텍스트를 간단하고 편리하게 암호화 및 복호화할 수 있는 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값에는 메시지 인증 코드(MAC)가 서명되어 있어, 암호화된 이후에는 내부 값이 수정되거나 변조될 수 없습니다.

<a name="configuration"></a>
## 설정

Laravel의 Encrypter를 사용하기 전에 `config/app.php` 설정 파일에서 `key` 구성 옵션을 설정해야 합니다. 이 구성 값은 `APP_KEY` 환경 변수에 의해 결정됩니다. 이 변수 값은 `php artisan key:generate` 명령어로 생성하는 것이 좋습니다. `key:generate` 명령어는 PHP의 안전한 무작위 바이트 생성기를 사용해 애플리케이션에 암호학적으로 안전한 키를 생성하기 때문입니다. 일반적으로 `APP_KEY` 환경 변수 값은 [Laravel 설치 과정](/docs/11.x/installation) 중에 자동 생성됩니다.

<a name="gracefully-rotating-encryption-keys"></a>
### 암호화 키 원활한 교체

애플리케이션의 암호화 키를 변경하면, 모든 인증된 사용자 세션은 로그아웃됩니다. 이는 세션 쿠키를 포함한 모든 쿠키가 Laravel에서 암호화되기 때문입니다. 또한, 이전 암호화 키로 암호화된 데이터는 더 이상 복호화할 수 없습니다.

이 문제를 해결하기 위해, Laravel은 애플리케이션의 `APP_PREVIOUS_KEYS` 환경 변수에 이전 암호화 키들을 나열할 수 있도록 지원합니다. 이 변수는 콤마(,)로 구분된 이전의 모든 암호화 키 목록을 포함할 수 있습니다:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

이 환경 변수를 설정하면 Laravel은 항상 암호화할 때 현재 키를 사용합니다. 하지만 복호화할 때는 먼저 현재 키로 시도하고, 실패하면 이전 키들을 차례로 시도하여 복호화를 시도합니다.

이런 원활한 복호화 처리 방식 덕분에 암호화 키를 교체하더라도 사용자가 애플리케이션 사용에 중단 없이 계속할 수 있습니다.

<a name="using-the-encrypter"></a>
## Encrypter 사용법

<a name="encrypting-a-value"></a>
#### 값 암호화

`Crypt` 파사드에서 제공하는 `encryptString` 메서드를 사용하여 값을 암호화할 수 있습니다. 모든 암호화된 값은 OpenSSL과 AES-256-CBC 암호화 방식으로 암호화됩니다. 더불어, 암호화된 값에는 메시지 인증 코드(MAC)가 서명되어 있어, 악의적인 사용자가 데이터의 무결성을 훼손하면 복호화가 차단됩니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();

        return redirect('/secrets');
    }
}
```

<a name="decrypting-a-value"></a>
#### 값 복호화

`Crypt` 파사드의 `decryptString` 메서드를 사용해 암호화된 값을 복호화할 수 있습니다. 만약 값이 정상적으로 복호화되지 않으면, 예를 들어 메시지 인증 코드가 유효하지 않은 경우에는 `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다:

```
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```
