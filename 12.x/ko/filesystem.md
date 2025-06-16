# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 획득](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장하기](#storing-files)
    - [파일에 내용 앞뒤로 추가하기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 공개 여부](#file-visibility)
- [파일 삭제하기](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

라라벨은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일시스템 추상화 계층을 제공합니다. 라라벨 Flysystem 통합 기능은 로컬 파일시스템, SFTP, Amazon S3 등 로컬 및 원격 스토리지에 쉽게 접근할 수 있도록 다양한 드라이버를 지원합니다. 각 시스템별 API가 동일하게 유지되기 때문에, 로컬 개발 환경과 운영 서버 간에 스토리지 옵션을 손쉽게 변경할 수 있습니다.

<a name="configuration"></a>
## 설정

라라벨의 파일시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정한 스토리지 드라이버와 저장 위치를 의미합니다. 각 드라이버별 예시 설정이 설정 파일에 포함되어 있으니, 이를 수정하여 원하는 스토리지 방식과 인증 정보를 반영할 수 있습니다.

`local` 드라이버는 라라벨 애플리케이션이 실행 중인 서버의 로컬 파일을 다루며, `sftp` 드라이버는 SSH 키 기반 FTP를 위한 것입니다. `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스에 파일을 쓰는 데 사용됩니다.

> [!NOTE]
> 원하는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크도 모두 만들 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때는 모든 파일 작업이 `filesystems` 설정 파일에서 지정한 `root` 디렉터리를 기준으로 상대 경로로 이루어집니다. 기본적으로 이 경로는 `storage/app/private` 디렉터리입니다. 따라서, 아래 예제 메서드는 `storage/app/private/example.txt` 파일에 데이터를 기록합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 웹에서 공개적으로 접근 가능한 파일을 저장할 때 사용하도록 설계되었습니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일은 `storage/app/public` 위치에 저장됩니다.

`public` 디스크가 `local` 드라이버를 사용하고 있고, 해당 파일들을 웹에서 접근할 수 있도록 하려면, 소스 디렉터리인 `storage/app/public`에서 대상 디렉터리인 `public/storage`로 심볼릭 링크를 생성해야 합니다.

심볼릭 링크를 만들 때는 `storage:link` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성했다면, 이제 `asset` 헬퍼를 이용해 해당 파일의 URL을 생성할 수 있습니다.

```php
echo asset('storage/file.txt');
```

추가적인 심볼릭 링크를 `filesystems` 설정 파일에 구성할 수도 있습니다. 설정한 각 링크는 `storage:link` 명령어를 실행할 때 한 번에 모두 만들어집니다.

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

설정한 심볼릭 링크들을 삭제하려면 `storage:unlink` 명령어를 사용할 수 있습니다.

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php` 설정 파일에 포함되어 있습니다. 보통은 아래 환경 변수들을 사용해 S3 정보와 인증 정보를 설정하며, 이 값들은 `config/filesystems.php` 설정 파일에서 참조합니다.

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경 변수들은 AWS CLI에서 사용하는 네이밍 컨벤션과 동일하게 맞춰져 있습니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem FTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-ftp "^3.0"
```

라라벨의 Flysystem 통합은 FTP 사용 시에도 잘 작동하지만, 프레임워크 기본 `config/filesystems.php`에는 샘플 설정이 포함되어 있지는 않습니다. FTP 파일시스템을 설정하려면 아래의 예시 구성을 사용할 수 있습니다.

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // 선택적 FTP 설정...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem SFTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

라라벨 Flysystem 통합은 SFTP 사용 시에도 잘 작동하지만, 프레임워크의 기본 `config/filesystems.php` 파일에는 샘플 설정이 포함되어 있지 않습니다. SFTP 파일시스템을 설정하려면 아래 예시 설정을 사용할 수 있습니다.

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 정보를 위한 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // 암호화 비밀번호가 포함된 SSH 키 기반 인증 설정...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // 파일/디렉터리 권한 설정...
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // 선택적 SFTP 설정...
    // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
    // 'maxTries' => 4,
    // 'passphrase' => env('SFTP_PASSPHRASE'),
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT', ''),
    // 'timeout' => 30,
    // 'useAgent' => true,
],
```

<a name="scoped-and-read-only-filesystems"></a>
### 스코프 및 읽기 전용 파일시스템

스코프 디스크를 사용하면 모든 경로를 지정한 경로 접두어로 자동으로 시작하도록 파일시스템을 정의할 수 있습니다. 스코프 파일시스템 디스크를 만들기 전에 Composer 패키지 매니저를 통해 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존 파일시스템 디스크의 경로에 스코프를 걸고 싶을 때는 `scoped` 드라이버를 사용하는 디스크를 설정하면 됩니다. 예를 들어, 기존 `s3` 디스크에 특정 경로 접두어가 항상 붙는 디스크를 만들 수 있는데, 스코프가 적용된 디스크를 통해 파일 작업을 하면 지정한 접두어가 항상 사용됩니다.

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크를 사용하면 파일 쓰기 작업이 불가능한 파일시스템 디스크를 만들 수 있습니다. `read-only` 설정 옵션을 사용하려면 Composer를 통해 별도의 Flysystem 패키지를 추가적으로 설치해야 합니다.

```shell
composer require league/flysystem-read-only "^3.0"
```

이후, 디스크의 설정 배열에 `read-only` 옵션을 추가하면 됩니다.

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

애플리케이션의 기본 `filesystems` 설정 파일에는 이미 `s3` 디스크에 대한 설정이 포함되어 있습니다. 이 디스크는 [Amazon S3](https://aws.amazon.com/s3/)와 연동할 수 있을 뿐만 아니라, [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 등 S3 호환 파일 스토리지 서비스와도 연동할 수 있습니다.

대부분의 경우, 사용할 서비스의 인증 정보와 일치하도록 디스크의 인증 정보를 변경한 후, `endpoint` 설정 값만 업데이트하면 됩니다. 이 값은 보통 `AWS_ENDPOINT` 환경 변수로 정의합니다.

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

MinIO를 사용할 때 라라벨 Flysystem 통합 기능이 올바른 URL을 생성하려면, 환경 변수 `AWS_URL`의 값을 애플리케이션의 로컬 URL에 버킷 이름이 포함된 경로로 맞춰주어야 합니다.

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> MinIO 사용 시 클라이언트가 `endpoint`에 접근할 수 없는 경우, `temporaryUrl` 메서드로 임시 스토리지 URL을 생성하는 기능이 정상적으로 동작하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 획득

`Storage` 파사드를 사용하면 설정된 모든 디스크와 손쉽게 상호작용할 수 있습니다. 예를 들어 기본 디스크에 아바타 파일을 저장하려면, `Storage` 파사드의 `put` 메서드를 사용할 수 있습니다. `disk` 메서드를 먼저 호출하지 않으면, 호출된 메서드는 자동으로 기본 디스크에 전달됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크를 사용하는 경우, `Storage` 파사드의 `disk` 메서드를 통해 특정 디스크의 파일을 다룰 수 있습니다.

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

특정 설정이 `filesystems` 설정 파일에 명시되어 있지 않더라도, 실행 시점에 직접 설정 배열을 전달하여 즉시 사용할 디스크를 만들고 싶을 때가 있습니다. 이럴 때는 `Storage` 파사드의 `build` 메서드에 설정 배열을 넘기면 됩니다.

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 가져오기

`get` 메서드를 사용해 파일의 내용을 가져올 수 있습니다. 이 메서드는 파일의 순수 문자열 내용을 반환합니다. 모든 파일 경로는 해당 디스크의 "root" 위치를 기준으로 상대 경로로 지정해야 합니다.

```php
$contents = Storage::get('file.jpg');
```

가져온 파일이 JSON 형식이라면 `json` 메서드를 사용해 파일 내용을 가져오고, 디코딩된 배열로 받을 수 있습니다.

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드를 사용하면 특정 디스크에 해당 파일이 존재하는지 확인할 수 있습니다.

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 특정 파일이 디스크에 존재하지 않는지 확인할 수 있습니다.

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저에서 파일을 강제로 다운로드하도록 하는 응답을 생성합니다. `download` 메서드의 두 번째 인자로 파일명을 지정하면, 파일을 다운로드받는 사용자에게 보일 파일이름이 결정됩니다. 마지막 세 번째 인자로는 HTTP 헤더의 배열을 전달할 수 있습니다.

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 사용하면 특정 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용할 때는 일반적으로 `/storage`가 해당 경로 앞에 붙어 상대적인 URL을 반환합니다. `s3` 드라이버를 사용하는 경우에는 완전한 원격 URL이 반환됩니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 사용할 경우, 공개적으로 접근 가능한 모든 파일은 `storage/app/public` 디렉터리에 두어야 하며, [심볼릭 링크를 생성](#the-public-disk)하여 `public/storage`가 `storage/app/public`을 가리키도록 해야 합니다.

> [!WARNING]
> `local` 드라이버를 사용할 때는 `url`의 반환값이 URL 인코딩되지 않습니다. 따라서 올바른 URL이 생성되도록, 파일 이름을 정할 때 항상 유효한 URL이 만들어질 수 있도록 해야 합니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이즈

`Storage` 파사드를 이용해 생성되는 URL의 호스트를 변경하고 싶으면, 디스크 설정 배열에 `url` 옵션을 추가하거나 수정하면 됩니다.

```php
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
    'throw' => false,
],
```

<a name="temporary-urls"></a>
### 임시 URL

`temporaryUrl` 메서드를 이용하면 `local` 및 `s3` 드라이버를 사용하는 파일들에 대해 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 함께 해당 URL이 만료될 시점을 지정하는 `DateTime` 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

애플리케이션을 `local` 드라이버의 임시 URL 지원이 도입되기 이전에 개발했다면, 로컬 임시 URL 기능을 별도로 활성화해야 할 수 있습니다. 활성화하려면 `config/filesystems.php` 파일의 `local` 디스크 설정 배열에 `serve` 옵션을 추가하세요.

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```

<a name="s3-request-parameters"></a>
#### S3 요청 파라미터

필요에 따라 추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 지정해야 한다면, `temporaryUrl` 메서드의 세 번째 인자로 파라미터 배열을 전달할 수 있습니다.

```php
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->addMinutes(5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

<a name="customizing-temporary-urls"></a>
#### 임시 URL 커스터마이즈

특정 스토리지 디스크에 대해 임시 URL을 커스터마이즈해서 생성하고 싶을 때는 `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 일반적으로 임시 URL을 지원하지 않는 디스크로 파일 다운로드를 허용하는 컨트롤러가 있다면 유용합니다. 보통 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

```php
<?php

namespace App\Providers;

use DateTime;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Storage::disk('local')->buildTemporaryUrlsUsing(
            function (string $path, DateTime $expiration, array $options) {
                return URL::temporarySignedRoute(
                    'files.download',
                    $expiration,
                    array_merge($options, ['path' => $path])
                );
            }
        );
    }
}
```

<a name="temporary-upload-urls"></a>
#### 임시 업로드 URL

> [!WARNING]
> 임시 업로드 URL을 생성하는 기능은 `s3` 드라이버에서만 지원됩니다.

클라이언트 애플리케이션에서 직접 파일 업로드가 필요할 때 임시로 업로드 가능한 URL을 만들어야 할 수 있습니다. 이때는 `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 경로와 해당 URL의 만료 시점을 지정하는 `DateTime` 인스턴스를 인자로 받습니다. 반환값은 업로드 URL과 업로드 요청에 추가해야 하는 헤더가 포함된 연관 배열이며, 아래처럼 구조 분해 할당으로 각각의 값을 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 메서드는 주로 서버리스 환경처럼 클라이언트 애플리케이션이 직접 Amazon S3 같은 클라우드 스토리지에 파일을 업로드해야 할 때 유용하게 쓰입니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일을 읽고 쓰는 것 외에도, 라라벨은 파일 자체의 다양한 정보를 제공할 수 있습니다. 예를 들어, `size` 메서드를 이용하면 파일의 크기를 바이트 단위로 알 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 해당 파일이 마지막으로 수정된 시점의 UNIX 타임스탬프를 반환합니다.

```php
$time = Storage::lastModified('file.jpg');
```

`mimeType` 메서드를 사용하면 특정 파일의 MIME 타입을 알 수 있습니다.

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 이용하면 특정 파일의 경로를 얻을 수 있습니다. `local` 드라이버를 사용하는 경우, 파일의 절대 경로가 반환되고, `s3` 드라이버의 경우 S3 버킷 내에서의 상대 경로가 반환됩니다.

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장하기

`put` 메서드를 사용하면 디스크에 파일 내용을 저장할 수 있습니다. 또한, PHP의 `resource`를 `put` 메서드에 전달하면 Flysystem 내부의 스트림 기능을 사용할 수 있습니다. 모든 파일 경로는 해당 디스크에 설정된 "root" 위치를 기준으로 상대적으로 지정해야 합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 쓰기 실패 처리

`put`(혹은 기타 "쓰기" 작업) 메서드가 파일을 디스크에 저장하지 못하는 경우, 이 메서드는 `false`를 반환합니다.

```php
if (! Storage::put('file.jpg', $contents)) {
    // 파일이 디스크에 쓰여지지 못했습니다...
}
```

원한다면, 파일시스템 디스크의 설정 배열에 `throw` 옵션을 추가할 수 있습니다. 이 옵션을 `true`로 설정하면, `put`과 같은 "쓰기" 메서드가 실패할 때 `League\Flysystem\UnableToWriteFile` 인스턴스를 예외로 던집니다.

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일에 내용 앞뒤로 추가하기

`prepend`와 `append` 메서드를 사용하면 파일의 시작 또는 끝에 데이터를 쓸 수 있습니다.

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 디스크 내 다른 위치로 복사할 수 있고, `move` 메서드는 기존 파일의 이름을 바꾸거나 새로운 위치로 이동할 때 사용할 수 있습니다.

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 저장소에 스트리밍하면 메모리 사용량을 크게 줄일 수 있습니다. 파일을 저장소에 자동으로 스트리밍하려면 `putFile` 또는 `putFileAs` 메서드를 사용하면 됩니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 인자로 받아, 원하는 위치로 자동 스트리밍합니다.

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명에 대해 고유 ID 자동 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 직접 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드에 대해 꼭 알아야 할 사항이 몇 가지 있습니다. 우선 메서드에 디렉터리 이름만 지정했고 파일명은 지정하지 않았다는 점을 확인하세요. 기본적으로 `putFile` 메서드는 파일명을 위한 고유 ID를 자동으로 생성합니다. 파일의 확장자는 파일의 MIME 타입을 기반으로 자동 결정됩니다. 메서드는 파일 경로(생성된 파일명 포함)를 반환하므로, 이 경로를 데이터베이스 등에 저장할 수 있습니다.

`putFile` 및 `putFileAs` 메서드는 저장되는 파일의 "공개 여부(visibility)"를 지정하는 인자도 받을 수 있습니다. S3와 같은 클라우드 디스크에 파일을 저장하고, 생성된 URL로 공개적으로 접근할 수 있도록 하려면 유용합니다.

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 가장 일반적인 파일 저장 예시는 사용자가 업로드한 사진이나 문서를 저장하는 경우입니다. 라라벨에서는 업로드된 파일 인스턴스의 `store` 메서드를 이용해 파일을 아주 쉽게 저장할 수 있습니다. 이때 원하는 저장 경로를 인자로 넘기면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자의 아바타를 업데이트합니다.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

이 예시에서 주의할 점이 몇 가지 있습니다. 우선 경로만 지정했을 뿐 파일명은 직접 입력하지 않았음을 알 수 있습니다. 기본적으로 `store` 메서드는 파일명으로 고유 ID를 자동 생성합니다. 파일의 확장자는 MIME 타입을 측정해서 결정되고, 메서드는 파일 경로(고유 파일명 포함)를 반환하여 데이터베이스 등에 저장할 수 있게 해줍니다.

위와 동일한 파일 저장 작업을 `Storage` 파사드의 `putFile` 메서드로도 수행할 수 있습니다.

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>

#### 파일 이름 지정하기

저장되는 파일의 이름이 자동으로 할당되는 것을 원하지 않는다면, `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일 이름, (선택적으로) 디스크를 인수로 받습니다.

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

위 예제와 동일하게 파일을 저장하려면 `Storage` 파사드의 `putFileAs` 메서드를 사용할 수도 있습니다.

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 인쇄할 수 없는 문자(unprintable character)와 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 라라벨의 파일 저장 메서드에 경로를 전달하기 전에 파일 경로를 미리 정제(sanitize)하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드를 통해 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정하기

기본적으로 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 사용하고 싶다면, 디스크 이름을 `store` 메서드의 두 번째 인수로 전달하면 됩니다.

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드를 사용할 때는 세 번째 인수로 디스크 이름을 지정할 수 있습니다.

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 기타 업로드 파일 정보 얻기

업로드된 파일의 원래 이름과 확장자를 얻고 싶다면, `getClientOriginalName`과 `getClientOriginalExtension` 메서드를 사용할 수 있습니다.

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만, `getClientOriginalName`과 `getClientOriginalExtension` 메서드는 잠재적으로 악의적인 사용자가 파일명과 확장자를 임의로 조작할 수 있기 때문에 안전하지 않습니다. 따라서 일반적으로는 이름과 확장자를 얻을 때 `hashName`과 `extension` 메서드를 사용하는 것이 좋습니다.

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 무작위로 생성된 이름...
$extension = $file->extension(); // MIME 타입 기반으로 확장자를 결정...
```

<a name="file-visibility"></a>
### 파일 공개 범위(Visibility)

라라벨의 Flysystem 통합에서는 "공개 범위(visibility)"를 여러 플랫폼에서의 파일 권한 개념을 추상화합니다. 파일은 `public`(공개) 또는 `private`(비공개)로 설정할 수 있습니다. 파일을 `public`으로 선언하면 일반적으로 다른 사용자도 접근할 수 있음을 의미합니다. 예를 들어 S3 드라이버를 사용할 때 공개 파일의 URL을 가져올 수 있습니다.

파일을 쓸 때는 `put` 메서드에서 공개 범위를 설정할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 공개 범위는 `getVisibility`와 `setVisibility` 메서드로 가져오거나 변경할 수 있습니다.

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일을 다룰 때는 `storePublicly`와 `storePubliclyAs` 메서드를 사용해 `public` 공개 범위로 저장할 수 있습니다.

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 공개 범위

`local` 드라이버를 사용할 때, [공개 범위](#file-visibility)에서 `public`은 디렉터리의 경우 `0755` 권한, 파일의 경우 `0644` 권한을 의미합니다. 이 권한 매핑은 애플리케이션의 `filesystems` 설정 파일에서 변경할 수 있습니다.

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app'),
    'permissions' => [
        'file' => [
            'public' => 0644,
            'private' => 0600,
        ],
        'dir' => [
            'public' => 0755,
            'private' => 0700,
        ],
    ],
    'throw' => false,
],
```

<a name="deleting-files"></a>
## 파일 삭제하기

`delete` 메서드는 삭제할 파일 이름 하나 또는 파일 이름의 배열을 받을 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면, 파일이 삭제되어야 할 디스크를 지정할 수도 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 가져오기

`files` 메서드는 주어진 디렉터리 내의 모든 파일을 배열로 반환합니다. 하위 디렉터리를 포함한 모든 파일 목록이 필요하다면 `allFiles` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 하위 디렉터리 가져오기

`directories` 메서드는 주어진 디렉터리 내 모든 하위 디렉터리를 배열로 반환합니다. 또, `allDirectories` 메서드를 이용하면 하위 디렉터리까지 포함한 전체 목록을 얻을 수 있습니다.

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성하기

`makeDirectory` 메서드는 필요한 하위 디렉터리까지 포함해서 지정한 디렉터리를 생성합니다.

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제하기

마지막으로, `deleteDirectory` 메서드를 사용해서 지정한 디렉터리와 그 안의 모든 파일을 제거할 수 있습니다.

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드는 테스트용 가짜 디스크를 쉽게 만들 수 있게 해줍니다. 이 기능은 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합해 파일 업로드 테스트를 크게 단순화해줍니다. 예를 들어:

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('albums can be uploaded', function () {
    Storage::fake('photos');

    $response = $this->json('POST', '/photos', [
        UploadedFile::fake()->image('photo1.jpg'),
        UploadedFile::fake()->image('photo2.jpg')
    ]);

    // 하나 이상의 파일이 저장되었는지 확인...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 하나 이상의 파일이 저장되지 않았는지 확인...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 특정 디렉터리 내 파일 개수가 예상과 일치하는지 확인...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 특정 디렉터리가 비어있는지 확인...
    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_albums_can_be_uploaded(): void
    {
        Storage::fake('photos');

        $response = $this->json('POST', '/photos', [
            UploadedFile::fake()->image('photo1.jpg'),
            UploadedFile::fake()->image('photo2.jpg')
        ]);

        // 하나 이상의 파일이 저장되었는지 확인...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 하나 이상의 파일이 저장되지 않았는지 확인...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉터리 내 파일 개수가 예상과 일치하는지 확인...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 특정 디렉터리가 비어있는지 확인...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉터리의 모든 파일을 삭제합니다. 만약 이러한 파일을 보존하고 싶다면, `"persistentFake"` 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대한 더 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 관련 섹션](/docs/12.x/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드를 사용하려면 [GD 확장 모듈](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일시스템 사용하기

라라벨의 Flysystem 통합은 여러 가지 "드라이버"를 기본적으로 지원하지만, Flysystem은 여기에 제한되지 않으며 다양한 다른 스토리지 시스템에 대한 어댑터도 제공합니다. 이러한 추가 어댑터를 라라벨 애플리케이션에서 사용하고 싶다면 커스텀 드라이버를 직접 만들 수 있습니다.

커스텀 파일시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가해보겠습니다.

```shell
composer require spatie/flysystem-dropbox
```

그 다음, 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers) 중 하나의 `boot` 메서드에서 드라이버를 등록합니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Contracts\Foundation\Application;
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\ServiceProvider;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Storage::extend('dropbox', function (Application $app, array $config) {
            $adapter = new DropboxAdapter(new DropboxClient(
                $config['authorization_token']
            ));

            return new FilesystemAdapter(
                new Filesystem($adapter, $config),
                $adapter,
                $config
            );
        });
    }
}
```

`extend` 메서드의 첫 번째 인수는 드라이버의 이름, 두 번째 인수는 `$app`과 `$config` 변수를 받는 클로저입니다. 이 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config` 변수에는 해당 디스크에 대해 `config/filesystems.php`에 정의된 값들이 담깁니다.

확장한 서비스 프로바이더를 생성하고 등록했다면, 이제 `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.