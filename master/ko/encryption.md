# 암호화

- [소개](#introduction)
- [구성](#configuration)
    - [암호화 키의 무중단 교체](#gracefully-rotating-encryption-keys)
- [Encrypter 사용하기](#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel의 암호화 서비스는 OpenSSL을 사용하여 AES-256 및 AES-128 암호화로 텍스트를 암호화하고 복호화할 수 있는 간단하고 편리한 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값은 메시지 인증 코드(MAC)를 사용해 서명되므로, 암호화된 후 해당 값이 수정되거나 위조될 수 없습니다.

<a name="configuration"></a>
## 구성

Laravel의 Encrypter를 사용하기 전에, `config/app.php` 설정 파일의 `key` 설정 옵션을 지정해야 합니다. 이 설정 값은 `APP_KEY` 환경 변수에 의해 결정됩니다. `php artisan key:generate` 명령어를 사용하여 이 변수의 값을 생성해야 하며, 이 명령어는 PHP의 보안 난수 생성기를 사용하여 애플리케이션에 암호학적으로 안전한 키를 만들어줍니다. 일반적으로, [Laravel 설치](/docs/{{version}}/installation) 과정에서 `APP_KEY` 환경 변수 값이 자동으로 생성됩니다.

<a name="gracefully-rotating-encryption-keys"></a>
### 암호화 키의 무중단 교체

애플리케이션의 암호화 키를 변경하면, 인증된 모든 사용자 세션이 로그아웃됩니다. 이는 모든 쿠키(세션 쿠키 포함)가 Laravel에 의해 암호화되기 때문입니다. 또한 이전 암호화 키로 암호화된 데이터를 더 이상 복호화할 수 없습니다.

이 문제를 완화하기 위해, Laravel에서는 애플리케이션의 `APP_PREVIOUS_KEYS` 환경 변수에 이전 암호화 키들을 나열할 수 있도록 지원합니다. 이 변수에는 이전 암호화 키들을 콤마(,)로 구분하여 나열할 수 있습니다:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

이 환경 변수를 설정하면, Laravel은 값을 암호화할 때는 항상 "현재" 암호화 키를 사용합니다. 그러나 값을 복호화할 때는 먼저 현재 키로 시도하고, 복호화가 실패하면 이전의 모든 키를 차례로 시도하여 복호화가 성공하는 키를 찾습니다.

이러한 무중단 복호화 방식 덕분에, 암호화 키를 교체하더라도 사용자들은 기존과 동일하게 애플리케이션을 사용할 수 있습니다.

<a name="using-the-encrypter"></a>
## Encrypter 사용하기

<a name="encrypting-a-value"></a>
#### 값 암호화하기

`Crypt` 파사드가 제공하는 `encryptString` 메서드를 사용해 값을 암호화할 수 있습니다. 모든 암호화된 값은 OpenSSL과 AES-256-CBC 암호 방식을 사용해 암호화됩니다. 또한 모든 암호화 값은 메시지 인증 코드(MAC)로 서명됩니다. 이 메시지 인증 코드는 악의적인 사용자가 값을 변조한 경우 복호화를 방지합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * 사용자의 DigitalOcean API 토큰을 저장합니다.
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
#### 값 복호화하기

`Crypt` 파사드가 제공하는 `decryptString` 메서드를 사용해 값을 복호화할 수 있습니다. 메시지 인증 코드가 올바르지 않은 경우 등 값이 정상적으로 복호화되지 않으면 `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```