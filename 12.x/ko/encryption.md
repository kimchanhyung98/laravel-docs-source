# 암호화(Encryption)

- [소개](#introduction)
- [설정](#configuration)
    - [암호화 키를 무중단으로 교체하기](#gracefully-rotating-encryption-keys)
- [Encrypter 사용하기](#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel의 암호화 서비스는 OpenSSL을 활용하여 AES-256 및 AES-128 암호화를 통해 텍스트를 쉽게 암호화하고 복호화할 수 있는 간편한 인터페이스를 제공합니다. Laravel에서 암호화된 모든 값은 메시지 인증 코드(MAC)로 서명되어 있기 때문에, 암호화된 후에는 값이 변경되거나 변조될 수 없습니다.

<a name="configuration"></a>
## 설정

Laravel의 암호화 도구를 사용하기 전에, `config/app.php` 설정 파일의 `key` 설정 옵션을 반드시 지정해야 합니다. 이 설정 값은 `APP_KEY` 환경 변수에서 관리됩니다. `php artisan key:generate` 명령어를 사용해 이 변수의 값을 생성해야 하는데, `key:generate` 명령어는 PHP의 안전한 랜덤 바이트 생성기를 활용해 암호학적으로 안전한 키를 생성해 줍니다. 일반적으로 [Laravel 설치](/docs/{{version}}/installation) 시점에 `APP_KEY` 환경 변수의 값이 자동으로 생성됩니다.

<a name="gracefully-rotating-encryption-keys"></a>
### 암호화 키를 무중단으로 교체하기

애플리케이션의 암호화 키를 변경하면, 인증 중인 모든 사용자 세션이 로그아웃됩니다. 이는 세션 쿠키를 포함한 모든 쿠키가 Laravel에서 암호화되기 때문입니다. 또한 이전 암호화 키로 암호화된 기존 데이터는 더 이상 복호화할 수 없게 됩니다.

이 문제를 완화하기 위해, Laravel에서는 애플리케이션의 `APP_PREVIOUS_KEYS` 환경 변수에 이전 암호화 키 목록을 지정할 수 있습니다. 이 변수에는 이전 암호화 키를 쉼표로 구분하여 나열할 수 있습니다:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

이 환경 변수를 설정하면, Laravel은 값을 암호화할 때는 항상 "현재" 암호화 키를 사용합니다. 하지만 값을 복호화할 때는 먼저 현재 키로 시도하고, 복호화에 실패하면 나열된 이전 키들로 순차적으로 시도하여, 복호화에 성공하는 키를 찾습니다.

이러한 방식의 유연한 복호화 덕분에, 암호화 키를 교체하더라도 사용자는 애플리케이션을 계속해서 중단 없이 사용할 수 있습니다.

<a name="using-the-encrypter"></a>
## Encrypter 사용하기

<a name="encrypting-a-value"></a>
#### 값 암호화하기

`Crypt` 파사드에서 제공하는 `encryptString` 메서드를 사용하여 값을 암호화할 수 있습니다. 모든 암호화는 OpenSSL과 AES-256-CBC 암호화 알고리즘을 사용합니다. 또한 모든 암호화된 값은 메시지 인증 코드(MAC)로 서명됩니다. 통합된 메시지 인증 코드는 악의적인 사용자가 변조한 값에 대해 복호화를 방지합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * 사용자를 위한 DigitalOcean API 토큰을 저장합니다.
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

암호화된 값을 복호화하려면 `Crypt` 파사드가 제공하는 `decryptString` 메서드를 사용할 수 있습니다. 만약 값이 올바르게 복호화되지 않거나, 메시지 인증 코드가 유효하지 않은 경우 `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다.

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```
