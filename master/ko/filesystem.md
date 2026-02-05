# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 준비](#driver-prerequisites)
    - [범위 지정 및 읽기 전용 파일 시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일 시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 조회](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일의 앞과 뒤에 내용 추가하기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성(visibility)](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지 덕분에 강력한 파일 시스템 추상화 기능을 제공합니다. Laravel의 Flysystem 통합 기능을 통해 로컬 파일 시스템, SFTP, Amazon S3와 쉽게 연동할 수 있는 간단한 드라이버를 제공합니다. 더욱이, 각각의 파일 시스템에 대해 동일한 API를 사용하므로, 로컬 개발 장비와 프로덕션 서버 간에 스토리지 옵션을 간편하게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일 시스템 "디스크(disk)"를 설정할 수 있습니다. 각 디스크는 특정한 저장 드라이버와 저장 위치를 의미합니다. 지원되는 각 드라이버에 대한 예제 설정이 설정 파일에 포함되어 있으므로, 이를 참고하여 저장소 환경 및 인증 정보를 반영하도록 수정할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버의 로컬 파일과 상호작용하며, `sftp` 드라이버는 SSH 키 기반의 FTP를 사용할 때 이용합니다. `s3` 드라이버는 Amazon의 S3 클라우드 저장소 서비스에 접근할 때 사용됩니다.

> [!NOTE]
> 원하는 만큼 여러 개의 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크도 만들 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버 (The Local Driver)

`local` 드라이버를 사용할 때, 모든 파일 작업은 `filesystems` 설정 파일에서 정의한 `root` 디렉터리를 기준으로 수행됩니다. 기본적으로 이 값은 `storage/app/private` 디렉터리로 설정되어 있습니다. 따라서 아래 메서드는 `storage/app/private/example.txt` 파일에 데이터를 기록합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크 (The Public Disk)

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 공개적으로 접근 가능한 파일을 저장하는 용도로 설계되었습니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일은 `storage/app/public`에 저장됩니다.

`public` 디스크가 `local` 드라이버를 사용할 때 웹에서 해당 파일에 접근할 수 있도록 하려면, 소스 디렉터리 `storage/app/public`에서 타겟 디렉터리 `public/storage`로 심볼릭 링크를 생성해야 합니다.

심볼릭 링크를 생성하려면 `storage:link` Artisan 명령어를 실행하세요:

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성한 후에는, `asset` 헬퍼를 사용해 해당 파일의 URL을 만들 수 있습니다:

```php
echo asset('storage/file.txt');
```

추가적인 심볼릭 링크를 `filesystems` 설정 파일에 지정할 수도 있습니다. 설정된 각 링크는 `storage:link` 명령어를 실행할 때 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

심볼릭 링크를 제거하려면 `storage:unlink` 명령어를 사용할 수 있습니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 (Driver Prerequisites)

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php` 설정 파일에 위치합니다. 일반적으로 해당 파일에서 참조하는 환경 변수에 S3 정보와 인증 정보를 아래와 같이 설정합니다:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경 변수 이름은 AWS CLI에서 사용하는 명명 규칙과 일치합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합 기능은 FTP와도 잘 동작하지만, 프레임워크의 기본 `config/filesystems.php`에는 FTP 예제 설정이 포함되어 있지 않습니다. FTP 파일 시스템을 설정하려면 아래 예제를 참고하세요:

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

SFTP 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 훌륭하게 동작하지만, 프레임워크의 기본 `config/filesystems.php`에 SFTP 예제 설정이 포함되어 있지 않습니다. SFTP 파일 시스템을 설정하려면 아래 예제를 참고하세요:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증용 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // 암호화 비밀번호가 포함된 SSH 키 기반 인증용 설정...
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
### 범위 지정 및 읽기 전용 파일 시스템 (Scoped and Read-Only Filesystems)

범위 지정된 디스크는 모든 경로가 지정한 경로 접두사로 자동으로 시작되는 파일 시스템을 정의할 수 있습니다. 범위 지정 파일 시스템 디스크를 만들기 전에 Composer 패키지 매니저를 통해 추가적인 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존 파일 시스템 디스크 중 하나에서 `scoped` 드라이버를 사용하여 경로 범위가 지정된 인스턴스를 정의할 수 있습니다. 예를 들어, 기존 `s3` 디스크를 특정 경로 접두사로 범위 지정하면, 이 디스크로 수행하는 모든 파일 작업에서 지정한 접두사가 자동으로 사용됩니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용(read-only)" 디스크는 쓰기 작업이 허용되지 않는 파일 시스템 디스크를 만들 수 있습니다. `read-only` 설정을 사용하기 전에 추가적인 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

이후, 디스크 설정 배열에 `read-only` 옵션을 추가할 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템 (Amazon S3 Compatible Filesystems)

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크에 대한 설정이 포함되어 있습니다. [Amazon S3](https://aws.amazon.com/s3/) 뿐만 아니라, [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 등 S3 호환 파일 스토리지 서비스와 상호작용할 때도 사용할 수 있습니다.

보통, 사용하고자 하는 서비스의 인증 정보로 디스크 설정을 수정한 후, `endpoint` 설정 값만 적절히 바꿔주면 됩니다. 이 값은 일반적으로 `AWS_ENDPOINT` 환경 변수로 지정합니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기 (Obtaining Disk Instances)

`Storage` 파사드를 사용하면 설정한 어느 디스크와도 상호작용할 수 있습니다. 예를 들어, 파사드의 `put` 메서드를 사용해 기본 디스크에 아바타를 저장할 수 있습니다. `disk` 메서드를 먼저 호출하지 않고 바로 `Storage` 파사드의 메서드를 실행하면, 해당 작업은 기본 디스크에 전달됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

애플리케이션이 여러 디스크와 상호작용해야 한다면, `Storage` 파사드의 `disk` 메서드를 사용하여 특정 디스크의 파일 작업을 할 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크 (On-Demand Disks)

실행 중에 특정 설정을 가진 디스크를 임시로 만들고 싶을 때, 해당 설정이 실제 애플리케이션의 `filesystems` 설정 파일에 없어도 됩니다. 이럴 경우, 설정 배열을 `Storage` 파사드의 `build` 메서드에 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 조회 (Retrieving Files)

`get` 메서드를 사용하면 파일의 내용을 가져올 수 있습니다. 이 메서드는 파일의 원본 문자열 내용을 반환합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 상대 경로를 지정해야 합니다:

```php
$contents = Storage::get('file.jpg');
```

조회하려는 파일이 JSON 형태라면, `json` 메서드를 사용하여 해당 파일을 가져오고 자동으로 내용을 디코딩할 수 있습니다:

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드는 디스크에 특정 파일이 존재하는지 확인할 수 있습니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 해당 파일이 디스크에 없는지 확인할 수 있습니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드 (Downloading Files)

`download` 메서드는 사용자의 브라우저에서 특정 경로의 파일을 강제로 다운로드하도록 하는 응답을 생성합니다. 두 번째 인수로 파일 이름을 지정하면, 다운로드 시 사용자에게 보일 파일 이름이 결정됩니다. 마지막 세 번째 인수로 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL (File URLs)

`url` 메서드를 사용하면 특정 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용하는 경우, 해당 경로 앞에 `/storage`가 자동으로 붙어 상대 URL이 반환됩니다. `s3` 드라이버를 사용할 경우, 완전한 원격 URL이 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 사용할 때, 공개적으로 접근 가능한 모든 파일은 반드시 `storage/app/public` 디렉터리에 있어야 하며, [심볼릭 링크를 생성](#the-public-disk)하여 `public/storage`가 `storage/app/public`을 가리키도록 해야 합니다.

> [!WARNING]
> `local` 드라이버 사용 시 `url`의 반환 값은 URL 인코딩되지 않습니다. 따라서 파일 이름을 만들 때는 항상 유효한 URL을 생성할 수 있도록 파일명을 지정하는 것이 좋습니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징 (URL Host Customization)

`Storage` 파사드로 생성되는 URL의 호스트를 변경하려면, 디스크의 설정 배열에 `url` 옵션을 추가하거나 수정하세요:

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

`temporaryUrl` 메서드를 사용하면, `local` 및 `s3` 드라이버로 저장된 파일에 대해 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL 만료 시점을 지정하는 `DateTime` 인스턴스를 인수로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

애플리케이션을 `local` 드라이버의 임시 URL 지원이 도입되기 전에 개발했다면, 로컬 임시 URL 사용을 별도로 활성화해야 할 수 있습니다. 이를 위해 `config/filesystems.php` 설정 파일에서 `local` 디스크 설정 배열에 `serve` 옵션을 추가하세요:

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

추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하면, 이러한 파라미터를 `temporaryUrl` 메서드의 세 번째 인수로 배열 형태로 전달할 수 있습니다:

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

특정 스토리지 디스크에 대해 임시 URL을 생성하는 방식을 커스터마이즈하려면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 임시 URL을 기본적으로 지원하지 않는 디스크의 파일을 다운로드하는 컨트롤러가 있는 경우 유용합니다. 이 메서드는 보통 서비스 제공자(ServiceProvider)의 `boot` 메서드에서 호출됩니다:

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

클라이언트 애플리케이션에서 파일을 직접 업로드할 수 있는 임시 URL을 만들어야 한다면, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 경로와 URL 만료 시점을 지정하는 `DateTime` 인스턴스를 인수로 받으며, 업로드 URL과 업로드 요청에 함께 포함할 헤더를 담은 연관 배열을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

이 메서드는 주로 클라이언트 애플리케이션이 Amazon S3와 같은 클라우드 저장소에 직접 파일을 업로드해야 하는 서버리스 환경에서 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터 (File Metadata)

Laravel은 파일의 읽기와 쓰기뿐 아니라, 파일 자체에 대한 정보도 제공할 수 있습니다. 예를 들어, `size` 메서드는 파일 크기를 바이트 단위로 반환합니다:

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
#### 파일 경로 (File Paths)

`path` 메서드를 사용하면 특정 파일의 경로를 가져올 수 있습니다. `local` 드라이버 사용 시에는 파일의 절대 경로를 반환하며, `s3` 드라이버 사용 시에는 S3 버킷 내에서의 상대 경로를 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장 (Storing Files)

`put` 메서드를 사용하면 파일 내용을 디스크에 저장할 수 있습니다. PHP의 `resource`를 인수로 전달할 수도 있는데, 이 경우 Flysystem의 기본 스트림 기능을 사용하여 저장이 이루어집니다. 모든 파일 경로는 디스크에 설정된 "root" 위치를 기준으로 상대 경로를 지정해야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 저장 실패 처리

`put` 메서드(또는 다른 "쓰기" 작업)가 파일을 디스크에 쓸 수 없을 때는, `false`가 반환됩니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```

원한다면, 파일 시스템 디스크의 설정 배열에 `throw` 옵션을 정의할 수 있습니다. 이 옵션을 `true`로 설정하면, `put`과 같은 "쓰기" 메서드가 실패할 경우 `League\Flysystem\UnableToWriteFile` 예외가 발생합니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일의 앞과 뒤에 내용 추가하기 (Prepending and Appending To Files)

`prepend`와 `append` 메서드를 사용하면 파일의 맨 앞이나 맨 뒤에 내용을 추가할 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동 (Copying and Moving Files)

`copy` 메서드는 기존 파일을 디스크의 새 위치로 복사할 때, `move` 메서드는 파일을 이름 변경하거나 새 위치로 이동할 때 사용합니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍 (Automatic Streaming)

파일을 스토리지로 스트리밍하면 메모리 사용량을 크게 줄일 수 있습니다. Laravel이 자동으로 파일을 지정한 저장 위치로 스트리밍하게 하려면, `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 자동으로 파일을 스트리밍합니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일 이름 자동 생성
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일 이름을 직접 지정
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드에 대해 주의할 점이 몇 가지 있습니다. 이 메서드는 디렉터리 이름만 지정하고 파일 이름은 지정하지 않았을 때, 기본적으로 고유한 ID를 파일 이름으로 생성합니다. 파일 확장자는 파일의 MIME 타입을 기준으로 정해집니다. 파일 경로(생성된 파일 이름 포함)는 `putFile` 메서드에서 반환되므로, 데이터베이스에 저장할 때 편리합니다.

또한 `putFile` 및 `putFileAs` 메서드는 저장되는 파일의 "가시성(visibility)"을 인수로 지정할 수 있습니다. Amazon S3 같은 클라우드 디스크에 파일을 저장하고, URL로 공개 접근을 허용하고 싶을 때 특히 유용합니다:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드 (File Uploads)

웹 애플리케이션에서는 사진, 문서와 같은 사용자 업로드 파일을 저장하는 일이 매우 흔합니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드를 사용하여 파일 저장을 아주 간편하게 처리할 수 있습니다. 원하는 저장 경로만 지정하면 됩니다:

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

이 예시에서 주의할 점은, 디렉터리 이름만 지정했을 뿐 파일 이름을 지정하지 않았다는 점입니다. 기본적으로 `store` 메서드는 고유한 ID를 파일 이름으로 자동 생성합니다. 파일의 확장자는 파일의 MIME 타입을 검사해 결정됩니다. `store` 메서드는 생성된 파일 이름을 포함한 경로를 반환하므로, 데이터베이스에 그대로 저장할 수 있습니다.

동일한 파일 저장 작업은 `Storage` 파사드의 `putFile` 메서드를 사용해 수행할 수도 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일 이름 지정하기

저장된 파일의 이름이 자동으로 할당되는 것이 싫다면, `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일 이름, (선택적) 디스크명을 인수로 받습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

동일 작업을 `Storage` 파사드의 `putFileAs` 메서드로도 처리할 수 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 출력 불가능하거나 잘못된 유니코드 문자가 파일 경로에서 자동으로 제거됩니다. 따라서 파일 저장 메서드에 값을 전달하기 전 경로를 정제하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드를 통해 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정하기

기본적으로 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 사용하려면 디스크 이름을 두 번째 인수로 전달하세요:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드를 사용하는 경우, 디스크 이름을 세 번째 인수로 전달하면 됩니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 그 밖의 업로드 파일 정보

업로드된 파일의 원래 이름과 확장자를 알고 싶으면, `getClientOriginalName`과 `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만, 이 메서드들은 악의적인 사용자가 임의로 파일 이름과 확장자를 조작할 수 있어 안전하지 않습니다. 이런 이유로, 주로 `hashName`과 `extension` 메서드를 사용해 업로드 파일의 이름과 확장자를 얻는 것이 더 안전합니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유의 랜덤 이름 생성
$extension = $file->extension(); // MIME 타입을 기준으로 파일의 확장자를 결정
```

<a name="file-visibility"></a>
### 파일 가시성(visibility) (File Visibility)

Laravel의 Flysystem 통합에서는 "가시성(visibility)"이 여러 플랫폼에서 파일 권한을 추상화한 개념입니다. 파일은 `public` 또는 `private` 중 하나로 선언할 수 있습니다. 파일이 `public`인 경우, 일반적으로 다른 사람이 접근할 수 있음을 의미합니다. 예를 들어 S3 드라이버 사용 시, `public` 파일의 URL을 쉽게 가져올 수 있습니다.

파일을 쓸 때 `put` 메서드로 가시성을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 가시성을 가져오거나 설정하려면, `getVisibility` 및 `setVisibility` 메서드를 사용할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드 파일을 다룰 때는 `storePublicly`와 `storePubliclyAs` 메서드로 업로드 파일을 `public` 가시성으로 저장할 수 있습니다:

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

`local` 드라이버를 사용할 때, `public` [가시성](#file-visibility)은 디렉터리에 `0755`, 파일에는 `0644` 권한을 의미합니다. `filesystems` 설정 파일에서 권한 매핑을 수정할 수 있습니다:

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

`delete` 메서드는 삭제할 파일 이름이나 파일 이름 배열을 인수로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면, 파일을 삭제할 디스크를 명시할 수도 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리 (Directories)

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 조회

`files` 메서드는 지정한 디렉터리 내의 모든 파일 목록을 배열로 반환합니다. 하위 디렉터리를 포함한 모든 파일 목록을 얻고 싶다면 `allFiles` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 하위 디렉터리 조회

`directories` 메서드는 지정한 디렉터리 내의 모든 하위 디렉터리 목록을 배열로 반환합니다. 하위 디렉터리의 하위까지 모두 포함한 목록은 `allDirectories` 메서드로 조회합니다:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성

`makeDirectory` 메서드는 지정한 디렉터리와 필요한 모든 하위 디렉터리를 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제

마지막으로, `deleteDirectory` 메서드는 디렉터리와 그 안의 모든 파일을 삭제할 때 사용합니다:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트 (Testing)

`Storage` 파사드의 `fake` 메서드를 사용하면, 임시 디스크를 쉽게 생성할 수 있습니다. 이를 `Illuminate\Http\UploadedFile`의 파일 생성 유틸리티와 조합하면 파일 업로드 기능 테스트를 훨씬 간단하게 할 수 있습니다. 예시:

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

    // 한 개 또는 여러 개 파일이 저장되었는지 확인...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 한 개 또는 여러 개 파일이 저장되지 않았는지 확인...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 특정 디렉터리 내 파일 개수가 예상과 일치하는지 확인...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // 특정 디렉터리가 비어 있는지 확인...
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

        // 한 개 또는 여러 개 파일이 저장되었는지 확인...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 한 개 또는 여러 개 파일이 저장되지 않았는지 확인...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉터리 내 파일 개수가 예상과 일치하는지 확인...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 특정 디렉터리가 비어 있는지 확인...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉터리 내 모든 파일을 삭제합니다. 이 파일을 유지하고 싶다면 "persistentFake" 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대한 자세한 정보는 [HTTP 테스트 문서의 파일 업로드 섹션](/docs/master/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템 (Custom Filesystems)

Laravel의 Flysystem 통합은 몇 가지 드라이버를 기본 지원하지만, Flysystem 자체는 더 다양한 저장소 시스템을 위한 어댑터가 존재합니다. Laravel 애플리케이션에서 이런 추가 어댑터를 사용하려면 커스텀 드라이버를 만들 수 있습니다.

커스텀 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가해봅시다:

```shell
composer require spatie/flysystem-dropbox
```

그 다음, 애플리케이션의 [서비스 프로바이더](/docs/master/providers) 중 하나의 `boot` 메서드에서 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용하세요:

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

`extend` 메서드의 첫 번째 인자는 드라이버의 이름이고, 두 번째 인자는 `$app`과 `$config` 변수를 받는 클로저입니다. 클로저는 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config` 변수에는 지정한 디스크의 `config/filesystems.php` 설정 값이 들어 있습니다.

확장 서비스 프로바이더를 만들고 등록했다면, 이제 `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.
