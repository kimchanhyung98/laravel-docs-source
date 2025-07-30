# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [스코프 지정 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 조회](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞뒤에 내용 추가](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [테스트](#testing)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge의 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일시스템 추상화를 제공합니다. Laravel의 Flysystem 통합은 로컬 파일시스템, SFTP, Amazon S3와 작업할 수 있는 간단한 드라이버들을 제공합니다. 더 좋은 점은, 각 스토리지 옵션 간 API가 동일하기 때문에 로컬 개발환경과 운영 서버 간 스토리지를 손쉽게 전환할 수 있다는 것입니다.

<a name="configuration"></a>
## 설정

Laravel의 파일시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 파일시스템 "디스크"들을 모두 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 위치를 나타냅니다. 지원하는 각 드라이버에 대한 예시 설정도 포함되어 있으며, 이를 바탕으로 자신의 스토리지 환경에 맞게 설정 및 자격증명을 조정할 수 있습니다.

- `local` 드라이버는 Laravel 애플리케이션이 실행되는 서버에 로컬로 저장된 파일과 상호작용합니다.
- `sftp` 드라이버는 SSH 키 기반 FTP에 사용됩니다.
- `s3` 드라이버는 Amazon S3 클라우드 스토리지 서비스에 쓰기 작업을 수행합니다.

> [!NOTE]
> 원하는 만큼 여러 디스크를 설정할 수 있고, 동일한 드라이버를 사용하는 디스크도 여러 개 지정할 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때, 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉토리를 기준으로 합니다. 기본값은 `storage/app/private` 디렉토리입니다. 따라서 다음 코드는 `storage/app/private/example.txt` 파일에 기록합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 외부에 공개될 파일을 위한 디스크입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며 `storage/app/public`에 파일을 저장합니다.

만약 `local` 드라이버를 사용하는 `public` 디스크의 파일을 웹에서 접근 가능하게 하려면, `storage/app/public` 소스 디렉토리에서 `public/storage` 타깃 디렉토리로 심볼릭 링크를 생성해야 합니다.

아티즌 명령어 `storage:link`를 통해 심볼릭 링크를 만들 수 있습니다:

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크가 생성되면, `asset` 헬퍼로 파일에 대한 URL을 만들 수 있습니다:

```php
echo asset('storage/file.txt');
```

심볼릭 링크는 `filesystems` 설정 파일에서 추가로 정의할 수도 있으며, `storage:link` 명령 실행 시 설정된 모든 링크가 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

`storage:unlink` 명령어로 설정된 심볼릭 링크를 제거할 수도 있습니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버 사용 전에는 Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

`config/filesystems.php` 설정 파일에 S3 디스크 구성 배열이 있습니다. 보통 S3 자격증명 정보는 다음 환경변수를 통해 설정하며, 이 변수들이 설정 파일에서 참조됩니다:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경변수들은 AWS CLI에서 사용하는 명명 규칙과 같습니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버 사용 전에는 Composer로 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와 잘 작동하지만, 기본 `config/filesystems.php` 설정 파일에는 기본 FTP 설정 예제가 포함되어 있지 않습니다. FTP 파일시스템을 설정하려면 아래 예제를 사용할 수 있습니다:

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

SFTP 드라이버 사용 전에는 Composer로 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와 훌륭히 작동하지만, 기본 설정 파일에 SFTP 예제는 포함되어 있지 않습니다. 필요하다면 아래 예제를 참고해 SFTP 파일시스템 설정이 가능합니다:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 기반 인증 및 암호...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // 파일 / 디렉토리 권한 설정...
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
### 스코프 지정 및 읽기 전용 파일시스템

스코프 지정 디스크는 모든 경로 앞에 지정한 접두사를 자동으로 붙이는 파일시스템을 정의할 수 있습니다. 스코프 지정 파일시스템 디스크를 만들기 전에 별도의 Flysystem 패키지를 Composer로 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

예를 들어, 기존 `s3` 디스크를 특정 경로 접두사로 한정하는 스코프 디스크를 만들면, 해당 스코프 디스크로 모든 파일 작업 시 지정한 접두사가 붙게 됩니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

읽기 전용 디스크는 쓰기 작업을 허용하지 않는 파일시스템 디스크를 만들 수 있습니다. 이를 사용하려면 별도의 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

그 다음, 디스크 설정 배열에 `read-only` 옵션을 포함할 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크 구성이 포함되어 있습니다. 이 디스크는 [Amazon S3](https://aws.amazon.com/s3/)뿐만 아니라 [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 같은 S3 호환 스토리지 서비스와도 사용할 수 있습니다.

디스크 자격증명을 해당 서비스에 맞게 변경한 뒤, 일반적으로 `endpoint` 구성 옵션만 서비스 주소로 업데이트하면 됩니다. 이 옵션은 보통 `AWS_ENDPOINT` 환경변수로 설정됩니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

MinIO를 사용할 때 Laravel의 Flysystem 통합이 올바른 URL을 생성하도록 하려면, `AWS_URL` 환경변수를 애플리케이션 로컬 URL과 버킷 이름이 포함된 경로로 정의하는 것이 좋습니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> MinIO를 사용할 때 `temporaryUrl` 메서드로 임시 스토리지 URL을 생성할 경우, `endpoint`가 클라이언트에서 접근 가능하지 않으면 작동하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드를 사용하면 설정한 디스크들과 상호작용할 수 있습니다. 예를 들어, 기본 디스크에 아바타를 저장하려면 `put` 메서드를 사용할 수 있습니다. `disk` 메서드를 호출하지 않으면 기본 디스크가 자동으로 사용됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크를 사용할 경우, `Storage` 파사드에서 `disk` 메서드로 특정 디스크를 지정해 파일 작업이 가능합니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

가끔 애플리케이션의 `filesystems` 설정 파일에 존재하지 않는 설정을 사용해 런타임에 디스크를 생성하고 싶을 수 있습니다. 이를 위해 `Storage` 파사드의 `build` 메서드에 구성 배열을 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 조회

`get` 메서드를 사용해 파일 내용을 조회할 수 있으며, 파일의 원시 문자열 콘텐츠가 반환됩니다. 파일 경로는 디스크의 "root" 위치를 기준으로 지정해야 합니다:

```php
$contents = Storage::get('file.jpg');
```

파일 내용이 JSON인 경우, `json` 메서드를 사용해 파일을 읽고 디코딩할 수 있습니다:

```php
$orders = Storage::json('orders.json');
```

파일 존재 여부는 `exists` 메서드로 확인할 수 있습니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

파일이 존재하지 않는지 확인하려면 `missing` 메서드를 사용합니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 지정된 경로의 파일을 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인자로 사용자에게 보여질 파일 이름을 지정할 수 있으며, 세 번째 인자에는 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 사용하면 주어진 파일의 URL을 가져올 수 있습니다. `local` 드라이버의 경우 보통 경로 앞에 `/storage`가 붙어 상대 URL을 반환합니다. `s3` 드라이버를 사용할 경우 완전한 원격 URL을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버 이용 시, 공개 접근이 필요한 파일은 모두 `storage/app/public`에 저장되어야 하며, `public/storage`에 심볼릭 링크가 생성되어 있어야 합니다.

> [!WARNING]
> `local` 드라이버에서 `url` 메서드가 반환하는 값은 URL 인코딩되지 않으므로, 항상 올바른 URL을 생성하기 위해서는 파일 이름에 유효한 문자를 사용하는 것이 좋습니다.

<a name="url-host-customization"></a>
#### URL 호스트 변경

`Storage` 파사드가 생성하는 URL의 호스트를 변경하고 싶다면, 디스크 구성 배열에 `url` 옵션을 추가하거나 수정할 수 있습니다:

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

`temporaryUrl` 메서드를 사용하면 `local` 및 `s3` 드라이버에서 저장된 파일에 접근 가능한 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL 만료 시점을 지정하는 `DateTime` 인스턴스를 인수로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

임시 URL 지원이 도입되기 이전에 개발을 시작한 경우, `local` 드라이버에서 임시 URL 기능을 활성화해야 할 수 있습니다. 이때는 `config/filesystems.php`에서 `local` 디스크 설정에 `serve` 옵션을 추가하세요:

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

추가 [S3 요청 매개변수](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 지정해야 할 경우, `temporaryUrl` 메서드의 세 번째 인자로 해당 배열을 전달할 수 있습니다:

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
#### 임시 URL 커스터마이징

특정 스토리지 디스크에 대해 임시 URL 생성 방식을 커스터마이징하려면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 임시 URL을 기본적으로 지원하지 않는 디스크의 파일을 컨트롤러에서 다운로드하게 하려는 경우에 유용합니다. 이 메서드는 보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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
> 임시 업로드 URL 생성 기능은 `s3` 드라이버에서만 지원됩니다.

클라이언트 측 애플리케이션에서 직접 파일을 업로드 할 수 있는 임시 URL이 필요한 경우, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 경로와 만료 시간을 받으며, 업로드 URL과 요청 헤더를 포함하는 연관 배열을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 방법은 주로 서버리스 환경에서 클라이언트가 Amazon S3와 같은 클라우드 스토리지에 직접 업로드할 때 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일의 읽기/쓰기 이외에도 Laravel은 파일에 관한 정보를 제공합니다. 예를 들어, `size` 메서드는 파일 크기를 바이트 단위로 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 시점의 UNIX 타임스탬프를 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```

파일의 MIME 타입은 `mimeType` 메서드로 확인할 수 있습니다:

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용하면 주어진 파일의 경로를 얻을 수 있습니다. `local` 드라이버를 사용하는 경우 절대 경로를 반환하며, `s3` 드라이버를 사용할 때는 S3 버킷 내 상대 경로를 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 디스크에 파일 내용을 저장할 때 사용합니다. PHP `resource`도 `put` 메서드에 전달할 수 있으며, 이 경우 Flysystem의 스트림 지원을 이용합니다. 모든 파일 경로는 해당 디스크의 "root" 위치를 기준으로 지정해야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 실패한 쓰기 작업 처리

`put` 메서드(또는 다른 쓰기 작업)가 디스크에 파일을 쓸 수 없으면 `false`를 반환합니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 디스크에 쓸 수 없었음을 처리...
}
```

`throw` 옵션을 파일시스템 디스크 설정 배열에 정의하면, 이 옵션을 `true`로 설정한 경우 쓰기 작업 실패 시 `League\Flysystem\UnableToWriteFile` 예외를 발생시키도록 할 수 있습니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일 앞뒤에 내용 추가

`prepend`와 `append` 메서드는 각각 파일의 시작 부분이나 끝 부분에 내용을 쓸 때 사용합니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 디스크 내 새 위치로 복사하고, `move` 메서드는 파일 이름 변경 혹은 이동 작업에 사용됩니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일 저장 시 메모리 사용량을 크게 줄이기 위해 스트리밍을 활용할 수 있습니다. `putFile` 또는 `putFileAs` 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 파일을 자동으로 스트리밍합니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일 이름을 자동으로 고유 ID 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일 이름 직접 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드의 중요한 점은 파일 이름 대신 디렉토리만 지정했을 때, 기본적으로 고유 ID를 생성하여 파일 이름으로 사용한다는 점입니다. 확장자는 MIME 유형을 분석해 정해집니다. 반환 값은 저장된 경로이며, 데이터베이스에 저장할 때 유용합니다.

`putFile`과 `putFileAs` 메서드는 세 번째 인자로 저장할 파일의 "visibility" (가시성)도 지정할 수 있습니다. 예를 들어, Amazon S3 같은 클라우드 디스크에 공개 접근 가능한 파일을 저장하려 할 때 유용합니다:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 흔히 사용하는 케이스 중 하나는 사용자가 업로드한 사진이나 문서 같은 파일을 저장하는 것입니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드를 사용해 손쉽게 파일을 저장할 수 있습니다. 원하는 저장 경로를 인자로 전달하세요:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자 아바타를 업데이트합니다.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

이 예제에서 디렉토리명만 지정하고 파일명은 명시하지 않은 점에 주목하세요. `store` 메서드는 기본적으로 고유 ID를 파일명으로 생성하고, 확장자는 MIME 타입을 기반으로 지정합니다. 반환된 경로는 생성된 파일명을 포함하므로 데이터베이스에 저장할 수 있습니다.

위와 동일한 작업을 `Storage` 파사드의 `putFile` 메서드를 통해서도 할 수 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일 이름 직접 지정

파일 이름 자동 할당을 원치 않는 경우 `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 저장할 경로, 파일 이름, 그리고 선택적인 디스크명을 인자로 받습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드의 `putFileAs` 메서드도 위와 같은 작업을 수행합니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 출력 불가능하거나 잘못된 유니코드 문자는 파일 경로에서 자동 제거됩니다. 따라서 파일 경로를 Laravel 파일 스토리지 메서드에 넘기기 전에 정제하는 것을 권장합니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

`store` 메서드는 기본적으로 기본 디스크를 사용합니다. 다른 디스크를 사용하려면 두 번째 인자로 디스크명을 전달하세요:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드의 경우, 세 번째 인자로 디스크명을 전달할 수 있습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 업로드된 파일 기타 정보

업로드된 파일의 원래 이름과 확장자를 얻으려면 `getClientOriginalName` 와 `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만 이 메서드들은 파일명과 확장자가 악의적인 사용자에 의해 조작될 가능성이 있으므로 보안상 안전하지 않습니다. 따라서 일반적으로는 해시 이름과 확장자를 반환하는 `hashName` 및 `extension` 메서드를 사용하는 것이 좋습니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 무작위로 생성된 이름...
$extension = $file->extension(); // MIME 타입에 따른 확장자 판별...
```

<a name="file-visibility"></a>
### 파일 가시성

Laravel의 Flysystem 통합에서 "가시성(visibility)"은 여러 플랫폼에서 파일 권한을 추상화한 개념입니다. 파일은 `public` 또는 `private` 상태로 지정할 수 있습니다. `public`으로 지정된 파일은 대체로 외부에서 접근 가능함을 의미합니다. 예를 들어, S3 드라이버 사용 시 `public` 파일에 대해 URL을 얻을 수 있습니다.

파일 저장 시 `put` 메서드의 세 번째 인자로 가시성을 설정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일은 `getVisibility` 및 `setVisibility` 메서드로 가시성을 조회하거나 변경할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일에 대해서는 `storePublicly` 및 `storePubliclyAs` 메서드로 `public` 가시성으로 저장할 수 있습니다:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 가시성

`local` 드라이버에서 `public` 가시성은 디렉토리 권한 `0755`, 파일 권한 `0644`로 변환됩니다. 권한 매핑은 `filesystems` 설정 파일에서 수정할 수 있습니다:

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
## 파일 삭제

`delete` 메서드는 삭제할 파일명 하나 또는 배열을 인자로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요시, 삭제할 디스크를 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉토리

<a name="get-all-files-within-a-directory"></a>
#### 디렉토리 내 모든 파일 가져오기

`files` 메서드는 지정한 디렉토리 안의 모든 파일 목록을 배열로 반환합니다. 하위 디렉토리까지 포함한 모든 파일을 얻으려면 `allFiles` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉토리 내 모든 하위 디렉토리 가져오기

`directories` 메서드는 지정한 디렉토리 내 모든 하위 디렉토리를 배열로 반환합니다. 하위 디렉토리를 포함한 전체 디렉토리 목록이 필요하면 `allDirectories` 메서드를 사용하세요:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉토리 생성

`makeDirectory` 메서드는 필요한 하위 디렉토리까지 포함해 지정한 디렉토리를 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉토리 삭제

`deleteDirectory` 메서드는 디렉토리와 그 안의 모든 파일을 삭제합니다:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 파사드의 `fake` 메서드는 테스트용 임시 디스크를 쉽게 생성할 수 있도록 지원합니다. 이를 통해 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합해 파일 업로드 테스트가 간소화됩니다. 예를 들어:

```php
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('albums can be uploaded', function () {
    Storage::fake('photos');

    $response = $this->json('POST', '/photos', [
        UploadedFile::fake()->image('photo1.jpg'),
        UploadedFile::fake()->image('photo2.jpg')
    ]);

    // 하나 이상의 파일이 저장됐는지 검증...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 존재하지 않는 파일이 저장되지 않았는지 검증...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 특정 디렉토리 내 파일 개수가 기대한 수와 일치하는지 검증...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 특정 디렉토리가 비어있는지 검증...
    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
});
```

```php
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

        // 하나 이상의 파일이 저장됐는지 검증...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 존재하지 않는 파일이 저장되지 않았는지 검증...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉토리 내 파일 개수가 기대한 수와 일치하는지 검증...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 특정 디렉토리가 비어있는지 검증...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉토리 내 모든 파일을 삭제합니다. 파일을 보존하려면 `persistentFake` 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 관한 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 관련 내용](/docs/12.x/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드를 사용하려면 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일시스템

Laravel의 Flysystem 통합은 기본적으로 몇 가지 "드라이버"를 지원하지만, Flysystem은 더 많은 어댑터를 지원합니다. 애플리케이션에서 이런 추가 어댑터를 사용하려면 커스텀 드라이버를 만들 수 있습니다.

커스텀 파일시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어 커뮤니티가 유지하는 Dropbox 어댑터를 프로젝트에 추가하려면:

```shell
composer require spatie/flysystem-dropbox
```

그 다음, 애플리케이션 내 서비스 프로바이더의 `boot` 메서드에서 `Storage` 파사드의 `extend` 메서드를 이용해 드라이버를 등록합니다:

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
     * 애플리케이션 서비스 등록 메서드.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩 메서드.
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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이고, 두 번째 인자는 `$app`과 `$config`를 받는 클로저입니다. 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 하며, `$config`는 `config/filesystems.php`의 해당 디스크 설정값을 포함합니다.

이 확장 서비스 프로바이더를 생성 및 등록한 후, `config/filesystems.php` 구성에서 `dropbox` 드라이버를 사용할 수 있습니다.