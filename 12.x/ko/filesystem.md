# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사용 전 준비사항](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일 시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일 시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일에 앞/뒤에 추가로 쓰기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 공개/비공개](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 Frank de Jonge가 개발한 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일 시스템 추상화 기능을 제공합니다. Laravel의 Flysystem 통합은 로컬 파일 시스템, SFTP, Amazon S3 작업을 위한 간단한 드라이버를 제공합니다. 더욱이, 각 시스템마다 동일한 API를 사용하므로, 로컬 개발 머신과 상용 서버 간에 스토리지 옵션을 간편하게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 있습니다. 이 파일에서 모든 파일 시스템 "디스크"를 구성할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 스토리지 위치를 나타냅니다. 각 지원 드라이버에 대한 예시 설정이 이미 포함되어 있으므로, 자신의 스토리지 환경과 인증 정보에 맞게 수정하면 됩니다.

`local` 드라이버는 Laravel 애플리케이션이 동작하는 서버의 로컬 파일을 다루고, `sftp` 드라이버는 SSH 키 기반의 FTP로 사용합니다. `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스를 사용합니다.

> [!NOTE]
> 원하는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 여러 개의 디스크에 사용할 수도 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버 (The Local Driver)

`local` 드라이버를 사용할 때, 모든 파일 작업은 `filesystems` 설정 파일에 정의한 `root` 디렉터리를 기준으로 상대 경로로 작동합니다. 기본적으로 이 값은 `storage/app/private` 디렉터리로 설정되어 있습니다. 즉, 아래의 예시 메서드는 `storage/app/private/example.txt` 파일에 내용을 저장합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크 (The Public Disk)

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 외부에 공개적으로 접근 가능한 파일을 저장하기 위해 사용됩니다. 기본적으로, `public` 디스크는 `local` 드라이버를 사용하며 파일은 `storage/app/public`에 저장됩니다.

`public` 디스크가 `local` 드라이버를 사용하는 경우, 이 파일들을 웹에서 접근 가능하게 하려면 `storage/app/public` 원본 디렉터리에서 `public/storage` 대상 디렉터리로 심볼릭 링크를 생성해야 합니다.

심볼릭 링크를 만들려면 `storage:link` 아티즌 명령어를 사용하세요:

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성한 후, `asset` 헬퍼를 사용해 파일에 대한 URL을 생성할 수 있습니다:

```php
echo asset('storage/file.txt');
```

추가 심볼릭 링크는 `filesystems` 설정 파일에서 정의할 수 있습니다. 설정한 모든 링크는 `storage:link` 명령 실행 시 함께 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

설정한 심볼릭 링크를 삭제하려면 `storage:unlink` 명령어를 사용합니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사용 전 준비사항 (Driver Prerequisites)

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하려면, Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php` 파일에 있습니다. 일반적으로 다음 환경 변수를 사용해 S3 정보를 입력하며, 이 변수들은 `config/filesystems.php` 파일에서 참조됩니다:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경 변수들은 AWS CLI에서 사용하는 명명 규칙과 일치합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하려면, Composer 패키지 매니저로 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 연동은 FTP와도 잘 동작하지만, 프레임워크 기본 `config/filesystems.php` 파일에는 샘플 설정이 포함되어 있지 않습니다. FTP 파일 시스템 설정이 필요한 경우, 아래와 같이 구성할 수 있습니다:

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

SFTP 드라이버를 사용하려면, Composer 패키지 매니저로 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 연동은 SFTP와도 잘 동작하지만, 프레임워크 기본 `config/filesystems.php` 파일에는 샘플 설정이 포함되어 있지 않습니다. SFTP 파일 시스템이 필요하다면 다음 예시와 같이 구성할 수 있습니다:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 기반 인증 및 암호 설정...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // 파일/디렉터리 권한 관련 설정...
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
### 스코프 및 읽기 전용 파일 시스템 (Scoped and Read-Only Filesystems)

스코프 디스크는 모든 경로가 자동으로 지정한 경로 접두사(prefix)로 시작하는 파일 시스템을 정의할 수 있게 해줍니다. 스코프 파일 시스템 디스크를 생성하려면 Composer 패키지 매니저로 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존 파일 시스템 디스크에 대해 `scoped` 드라이버를 이용하면, 지정한 경로 접두사로 스코프된 인스턴스를 만들 수 있습니다. 예를 들어, 기존 `s3` 디스크를 특정 경로로 제한(scoping)하면, 해당 스코프 디스크로 파일을 저장할 때마다 지정한 접두사가 자동으로 적용됩니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용(read-only)" 디스크를 사용하면, 쓰기 작업이 허용되지 않는 파일 시스템 디스크를 생성할 수 있습니다. `read-only` 옵션을 이용하려면 Composer로 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

이후 디스크 설정 배열에 `read-only` 옵션을 추가하여 사용할 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템 (Amazon S3 Compatible Filesystems)

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크에 대한 설정이 포함되어 있습니다. 이 디스크를 사용해 [Amazon S3](https://aws.amazon.com/s3/) 뿐만 아니라, [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 등 S3 호환 파일 저장 서비스를 사용할 수 있습니다.

디스크의 인증 정보를 원하는 서비스에 맞게 수정한 후에는, 일반적으로 `endpoint` 설정 값만 변경하면 됩니다. 이 값은 주로 `AWS_ENDPOINT` 환경 변수로 정의합니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

MinIO에서 Laravel의 Flysystem 통합이 올바른 URL을 생성하도록 하려면, `AWS_URL` 환경 변수 값을 애플리케이션의 로컬 URL과 동기화하고, 버킷 이름을 URL 경로에 포함하세요:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> 클라이언트에서 `endpoint`에 접근할 수 없는 경우, `temporaryUrl` 메서드를 사용한 임시 스토리지 URL 생성이 MinIO에서 동작하지 않을 수 있습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기 (Obtaining Disk Instances)

`Storage` 파사드를 사용하면 설정한 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 파사드의 `put` 메서드로 기본 디스크에 아바타를 저장할 수 있습니다. 먼저 `disk` 메서드를 호출하지 않고 바로 `Storage` 파사드의 메서드를 호출하면, 기본 디스크로 동작이 전달됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크와 상호작용해야 하는 경우, `disk` 메서드로 특정 디스크를 지정할 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크 (On-Demand Disks)

특정 설정을 따로 파일에 기록하지 않고 런타임에 바로 디스크를 생성하고 싶을 때는, 설정 배열을 `Storage` 파사드의 `build` 메서드로 전달하세요:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 가져오기 (Retrieving Files)

`get` 메서드를 사용하면 파일 내용을 불러올 수 있습니다. 이 메서드는 파일의 원시 문자열 내용을 반환합니다. 모든 파일 경로는 반드시 디스크의 "root" 기준 상대 경로로 지정해야 합니다:

```php
$contents = Storage::get('file.jpg');
```

가져오는 파일이 JSON 형식이라면, `json` 메서드를 사용해 파일을 읽고 내용을 디코딩할 수 있습니다:

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드는 디스크에 특정 파일이 존재하는지 확인할 수 있습니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 디스크에서 파일이 존재하지 않는지 확인할 수 있습니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드 (Downloading Files)

`download` 메서드를 사용하면 지정한 경로의 파일을 강제로 브라우저가 다운로드하도록 응답을 생성합니다. 다운로드 시 표시될 파일명은 두 번째 인수로 전달합니다. 세 번째 인수로 HTTP 헤더 배열도 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL (File URLs)

특정 파일의 URL을 구하려면 `url` 메서드를 사용하면 됩니다. `local` 드라이버를 쓸 경우, 일반적으로 `/storage`를 경로 앞에 붙인 상대 URL이 반환됩니다. `s3` 드라이버를 쓸 경우, 완전히 접근이 가능한 원격 URL이 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 사용할 경우, 외부에서 접근 가능한 파일은 모두 `storage/app/public` 디렉터리에 위치해야 하며, [심볼릭 링크 생성](#the-public-disk)을 통해 `public/storage`와 연결해야 웹을 통한 접근이 가능합니다.

> [!WARNING]
> `local` 드라이버를 사용할 때 `url`의 반환 값은 URL 인코딩이 되지 않습니다. 따라서 항상 URL로 쓸 수 있는 이름으로 파일을 저장하는 것이 좋습니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드로 생성되는 URL의 호스트를 변경하거나 커스터마이징하려면, 디스크 설정 배열의 `url` 옵션을 추가하거나 변경할 수 있습니다:

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
### 임시 URL (Temporary URLs)

`temporaryUrl` 메서드를 사용하면, `local` 및 `s3` 드라이버로 저장한 파일에 임시로 접근할 수 있는 URL을 만들 수 있습니다. 이 메서드는 파일 경로와 URL 만료 시점을 나타내는 `DateTime` 인스턴스를 인수로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

임시 URL 기능이 `local` 드라이버에 도입되기 전에 개발을 시작한 경우, 해당 기능을 직접 활성화해야 할 수 있습니다. 이를 위해 `config/filesystems.php`에서 `local` 디스크 설정 배열에 `serve` 옵션을 추가합니다:

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

추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요한 경우, 이 파라미터 배열을 `temporaryUrl` 메서드의 세 번째 인수로 전달하면 됩니다:

```php
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->plus(minutes: 5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

<a name="customizing-temporary-urls"></a>
#### 임시 URL 커스터마이징

특정 스토리지 디스크에 대해 임시 URL 생성 방식을 커스터마이징해야 할 경우, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 일반적으로 임시 URL을 지원하지 않는 디스크에서 파일 다운로드를 허용하는 컨트롤러가 있다면, 이 방법을 유용하게 사용할 수 있습니다. 일반적으로 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

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

클라이언트에서 파일을 직접 클라우드 스토리지(예: Amazon S3)로 업로드하도록 임시 URL이 필요하다면, `temporaryUploadUrl` 메서드를 사용하세요. 이 메서드는 경로와 만료 시점(`DateTime` 인스턴스)을 인수로 받고, 업로드 URL과 업로드 요청에 포함해야 할 헤더 배열이 포함된 연관 배열을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

이 기능은 주로 서버리스 환경에서 클라이언트가 직접 클라우드 스토리지에 파일을 업로드해야 할 때 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터 (File Metadata)

Laravel은 파일 읽기/쓰기에 더해, 파일 자체에 대한 정보도 제공합니다. 예를 들어, `size` 메서드는 파일 크기(바이트 단위)를 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 시간의 UNIX 타임스탬프를 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```

파일의 MIME 타입은 `mimeType` 메서드로 확인할 수 있습니다:

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용하면 특정 파일의 경로를 얻을 수 있습니다. `local` 드라이버를 사용할 경우 파일의 절대 경로가 반환되며, `s3` 드라이버의 경우 버킷 내의 상대 경로가 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장 (Storing Files)

`put` 메서드를 사용하면 파일 시스템에 파일 내용을 저장할 수 있습니다. PHP의 `resource` 타입을 직접 `put` 메서드에 전달하면 Flysystem이 스트림 기능을 사용합니다. 모든 파일 경로는 디스크별로 설정한 "root" 기준 상대 경로로 지정해야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 저장 실패 처리

`put` 메서드(및 기타 파일 "쓰기" 연산)이 파일을 디스크에 쓸 수 없는 경우, `false`를 반환합니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```

필요하다면 디스크 설정 배열에 `throw` 옵션을 정의할 수 있습니다. 이 옵션이 `true`로 설정되면, `put`과 같은 "쓰기" 메서드에서 쓰기에 실패할 때 `League\Flysystem\UnableToWriteFile` 예외가 발생합니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일에 앞/뒤에 추가로 쓰기 (Prepending and Appending To Files)

`prepend`와 `append` 메서드를 통해 파일 맨 앞이나 맨 뒤에 내용을 쓸 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동 (Copying and Moving Files)

`copy` 메서드는 기존 파일을 디스크 내 새로운 위치로 복사하고, `move` 메서드는 기존 파일을 다른 위치로 이동하거나 이름을 변경할 때 사용합니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍 (Automatic Streaming)

파일을 스트리밍하여 저장하면 메모리 사용량을 크게 줄일 수 있습니다. Laravel이 자동으로 파일 스트리밍을 관리하도록 하려면, `putFile` 또는 `putFileAs` 메서드를 사용하세요. 이 메서드는 `Illuminate\Http\File`이나 `Illuminate\Http\UploadedFile` 인스턴스를 받아, 지정 위치에 파일을 자동 스트리밍해 저장합니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명에 고유한 ID 자동 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 직접 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드는 파일명 대신 디렉터리명만 전달하면 됩니다. 파일명은 고유한 ID로 자동 생성되며, 확장자는 파일의 MIME 타입에서 결정합니다. 이 메서드는 파일의 전체 경로를 반환하므로, 데이터베이스에 저장할 때 경로와 생성된 파일명을 함께 저장할 수 있습니다.

`putFile`과 `putFileAs` 메서드는 저장할 파일의 "visibility"를 지정하는 인수도 받을 수 있습니다. S3와 같이 URL 접근이 필요한 클라우드 디스크에서는 이 옵션이 특히 유용합니다:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드 (File Uploads)

웹 애플리케이션에서 가장 일반적인 파일 저장 케이스는 사진, 문서 등 사용자가 업로드하는 파일을 저장하는 것입니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드를 사용해 손쉽게 업로드 파일을 저장할 수 있습니다. 저장할 위치의 경로를 인수로 넘기면 됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * Update the avatar for the user.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

이 예시에서는 디렉터리명만 지정했지, 파일명을 따로 지정하지 않은 것에 주의하세요. `store` 메서드는 고유한 ID로 파일명을 자동 생성합니다. 확장자는 파일의 MIME 타입에서 추론되며, 이 메서드는 전체 경로를 반환하므로 경로와 생성 파일명을 DB 등에 저장할 수 있습니다.

또한 아래처럼 `Storage` 파사드의 `putFile` 메서드로 동일한 파일 저장 작업을 할 수 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정하기

자동으로 파일명을 부여받고 싶지 않다면, `storeAs` 메서드를 사용하세요. 이 메서드는 경로, 파일명, (선택적) 디스크를 인수로 받습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

또는 동일한 작업을 `Storage` 파사드의 `putFileAs`로 수행할 수 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 인쇄 불가능한 문자 및 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 Laravel의 파일 저장 메서드에 경로를 전달하기 전에, 파일 경로를 필터링/정규화하는 것을 권장합니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정하기

업로드 파일의 기본 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 사용하려면, 두 번째 인수로 디스크명을 전달하면 됩니다:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드에서는 세 번째 인수로 디스크명을 전달할 수 있습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 업로드 파일의 기타 정보

업로드 파일의 원본 파일명과 확장자를 가져오려면 `getClientOriginalName`, `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만, 이 메서드들은 파일명과 확장자가 악의적인 사용자가 조작할 수 있으므로 안전하지 않습니다. 따라서 실제 업로드의 이름/확장자를 얻으려면 `hashName`, `extension` 메서드를 사용하는 것을 권장합니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유 ID로 무작위 이름 생성...
$extension = $file->extension(); // MIME 타입 기준 확장자 추출...
```

<a name="file-visibility"></a>
### 파일 공개/비공개 (File Visibility)

Laravel의 Flysystem 연동에서 "visibility"는 여러 플랫폼의 파일 권한을 추상화한 개념입니다. 파일은 `public`(공개) 또는 `private`(비공개)로 선언할 수 있습니다. 예를 들어, S3 드라이버에서 `public`으로 지정된 파일은 URL로 접근할 수 있습니다.

파일을 저장할 때는 `put` 메서드에서 visibility를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 visibility는 `getVisibility`와 `setVisibility` 메서드로 확인 및 변경할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드 파일을 다룰 때는 `storePublicly`, `storePubliclyAs` 메서드를 사용하면 `public` visibility로 업로드할 수 있습니다:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일 및 공개/비공개 권한

`local` 드라이버를 사용할 때, `public` [visibility](#file-visibility)는 디렉터리 `0755`, 파일 `0644` 권한으로 매핑됩니다. 이 권한은 `filesystems` 설정 파일에서 변경할 수 있습니다:

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
## 파일 삭제 (Deleting Files)

`delete` 메서드는 삭제할 파일명을 하나 또는 여러 개의 배열로 받을 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면, 파일을 삭제할 디스크를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리 (Directories)

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 가져오기

`files` 메서드는 지정한 디렉터리 내의 모든 파일을 배열로 반환합니다. 하위 디렉터리까지 전체 파일 목록을 원한다면 `allFiles` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 하위 디렉터리 가져오기

`directories` 메서드는 지정한 디렉터리 내의 하위 디렉터리 목록을 반환합니다. 하위 디렉터리까지 전체 목록을 원하면 `allDirectories` 메서드를 사용할 수 있습니다:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성

`makeDirectory` 메서드는 지정한 디렉터리 및 필요한 모든 하위 디렉터리를 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제

`deleteDirectory` 메서드는 디렉터리 및 하위 모든 파일을 삭제합니다:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트 (Testing)

`Storage` 파사드의 `fake` 메서드를 이용하면 테스트용 가짜 디스크를 생성할 수 있으며, `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 함께 사용하면 파일 업로드 테스트가 매우 간단해집니다. 예시:

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

    // 하나 또는 여러 파일이 저장되었는지 확인...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 하나 또는 여러 파일이 저장되지 않았는지 확인...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 주어진 디렉터리 내 파일 개수가 예상과 일치하는지 확인...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 주어진 디렉터리가 비어있는지 확인...
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

        // 하나 또는 여러 파일이 저장되었는지 확인...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 하나 또는 여러 파일이 저장되지 않았는지 확인...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 주어진 디렉터리 내 파일 개수가 예상과 일치하는지 확인...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 주어진 디렉터리가 비어있는지 확인...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉터리의 모든 파일을 삭제합니다. 이러한 파일을 유지하고 싶다면 "persistentFake" 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 관한 자세한 내용은 [HTTP 테스트 문서의 파일 업로드](/docs/12.x/http-tests#testing-file-uploads) 부분을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템 (Custom Filesystems)

Laravel의 Flysystem 연동은 여러 "드라이버"를 기본 지원하지만, Flysystem은 이외에도 다양한 어댑터를 지원합니다. 추가 어댑터를 사용하고 싶다면 커스텀 드라이버를 직접 만들 수 있습니다.

커스텀 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가합니다:

```shell
composer require spatie/flysystem-dropbox
```

이후, [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다:

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

`extend` 메서드의 첫 번째 인수는 드라이버명이며, 두 번째 인수는 `$app`과 `$config`를 받는 클로저입니다. 이 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 하며, `$config` 배열에는 `config/filesystems.php`의 해당 디스크 설정값이 들어 있습니다.

확장 서비스 프로바이더를 만들고 등록했다면, `config/filesystems.php`에서 `dropbox` 드라이버를 사용할 수 있습니다.

