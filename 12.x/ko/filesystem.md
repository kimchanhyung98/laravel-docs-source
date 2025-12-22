# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 준비 사항](#driver-prerequisites)
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
    - [파일에 앞뒤로 내용 추가하기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 공개/비공개 설정](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 Frank de Jonge가 개발한 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지 덕분에 강력한 파일 시스템 추상화 기능을 제공합니다. Laravel의 Flysystem 통합 기능을 통해 로컬 파일 시스템, SFTP, Amazon S3 등 다양한 스토리지 옵션에 대해 간단히 드라이버를 사용할 수 있습니다. 더욱이, 이러한 스토리지 드라이버들은 동일한 API를 제공하므로 로컬 개발 환경과 운영 서버 간에 쉽게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서는 모든 파일 시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 스토리지 위치를 의미하며, 프레임워크에서 지원하는 각 드라이버에 대한 샘플 설정이 포함되어 있으니, 이를 원하는 스토리지 정보와 자격 증명에 맞게 수정하여 사용할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 동작하는 서버의 로컬 파일을 다루며, `sftp` 드라이버는 SSH 키 기반의 FTP에 사용됩니다. `s3` 드라이버는 Amazon S3 클라우드 스토리지 서비스를 사용합니다.

> [!NOTE]
> 원하는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크를 동시에 구성할 수도 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버 (The Local Driver)

`local` 드라이버를 사용할 때 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉터리를 기준으로 상대 경로로 동작합니다. 기본적으로 이 값은 `storage/app/private` 디렉터리로 설정되어 있습니다. 예를 들어, 아래와 같은 방식으로 파일을 저장하면 `storage/app/private/example.txt` 파일이 생성됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크 (The Public Disk)

애플리케이션의 `filesystems` 설정 파일에 기본으로 포함된 `public` 디스크는 외부에 공개될 파일을 저장하기 위한 용도입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 해당 파일은 `storage/app/public` 디렉터리에 저장됩니다.

만약 `public` 디스크가 `local` 드라이버를 사용 중이고, 웹에서 파일에 접근할 수 있도록 하려면, 원본 디렉터리인 `storage/app/public`을 대상으로 하여 대상 디렉터리인 `public/storage`에 심볼릭 링크를 생성해야 합니다.

심볼릭 링크를 생성하려면 다음 Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성한 이후에는 `asset` 헬퍼를 사용해서 해당 파일의 URL을 생성할 수 있습니다.

```php
echo asset('storage/file.txt');
```

추가 심볼릭 링크 또한 `filesystems` 설정 파일에서 구성할 수 있습니다. 설정된 각 링크는 `storage:link` 명령어를 실행할 때 함께 생성됩니다.

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

`storage:unlink` 명령어를 사용하면 설정된 심볼릭 링크를 제거할 수 있습니다.

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 사항 (Driver Prerequisites)

<a name="s3-driver-configuration"></a>
#### S3 드라이버 구성

S3 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 구성 배열은 `config/filesystems.php` 설정 파일에 있습니다. 일반적으로 아래와 같은 환경 변수를 통해 S3 정보를 설정하며, 이 환경 변수들은 `config/filesystems.php`에서도 참조됩니다.

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

이 환경 변수명은 AWS CLI와 동일한 네이밍 컨벤션을 따릅니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 구성

FTP 드라이버를 사용하기 전에는 Composer 패키지 매니저를 통해 Flysystem FTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와도 잘 동작하지만, 기본 `config/filesystems.php`에는 예시 구성이 포함되어 있지 않습니다. FTP 파일 시스템을 구성할 필요가 있다면 아래 예시를 참고하여 파일에 추가하세요.

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // Optional FTP Settings...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 구성

SFTP 드라이버를 사용하기 전에는 Composer 패키지 매니저를 통해 Flysystem SFTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 잘 동작하지만, 기본 `config/filesystems.php`에는 예시 구성이 포함되어 있지 않습니다. SFTP 파일 시스템이 필요하다면 아래 예시를 참고하여 추가할 수 있습니다.

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 기반 인증 및 암호문 설정...
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
### 스코프 및 읽기 전용 파일 시스템 (Scoped and Read-Only Filesystems)

스코프 디스크를 사용하면, 모든 경로에 지정한 경로 프리픽스가 자동으로 붙는 파일 시스템을 정의할 수 있습니다. 스코프 파일 시스템 디스크를 만들기 전에 Composer 패키지 매니저를 통해 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

`scoped` 드라이버를 사용하여, 기존 파일 시스템 디스크의 경로에 프리픽스를 적용하는 디스크 인스턴스를 사용할 수 있습니다. 예를 들어, 기존 `s3` 디스크를 특정 경로 프리픽스로 한정(스코프)하여 사용할 수 있습니다. 그러면 해당 스코프 디스크로 모든 파일 작업 시 지정한 프리픽스가 적용됩니다.

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크는 쓰기 작업이 허용되지 않는 파일 시스템 디스크를 만들 수 있습니다. `read-only` 설정 옵션을 사용하려면 Composer로 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-read-only "^3.0"
```

그 다음, 디스크의 설정 배열에 `read-only` 옵션을 포함할 수 있습니다.

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템 (Amazon S3 Compatible Filesystems)

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크에 대한 설정이 포함되어 있습니다. [Amazon S3](https://aws.amazon.com/s3/)와 연동하는 것 외에도, [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 등 S3 API 호환 스토리지 서비스와 연동할 수도 있습니다.

해당 서비스에 맞는 인증 정보를 입력한 뒤, 보통은 `endpoint` 설정만 변경하면 됩니다. 이 값은 주로 `AWS_ENDPOINT` 환경 변수로 지정합니다.

```php
'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기 (Obtaining Disk Instances)

`Storage` 파사드는 구성한 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 파사드의 `put` 메서드를 사용하여 기본 디스크에 아바타를 저장할 수 있습니다. 만약 `Storage` 파사드에서 `disk` 메서드 없이 메서드를 호출하면, 해당 메서드는 기본 디스크에 자동으로 전달됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크와 상호작용해야 하는 경우, `Storage` 파사드의 `disk` 메서드를 사용하여 특정 디스크를 지정해서 사용할 수 있습니다.

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크 (On-Demand Disks)

특정 설정이 `filesystems` 설정 파일에 미리 존재하지 않더라도, 런타임에 동적으로 디스크를 생성하고 싶을 때가 있습니다. 이를 위해 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달할 수 있습니다.

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

`get` 메서드는 파일의 내용을 가져오는 데 사용할 수 있습니다. 파일의 원시 문자열 데이터가 반환됩니다. 모든 파일 경로는 디스크의 "root" 위치에 대한 상대 경로로 지정해야 합니다.

```php
$contents = Storage::get('file.jpg');
```

가져오려는 파일이 JSON 형식인 경우, `json` 메서드를 사용하여 파일을 읽고 내용도 디코딩할 수 있습니다.

```php
$orders = Storage::json('orders.json');
```

`exists` 메서드는 파일이 디스크에 존재하는지 확인할 수 있습니다.

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 파일이 디스크에서 누락되었는지 확인합니다.

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드 (Downloading Files)

`download` 메서드는 사용자의 브라우저가 특정 경로의 파일을 강제로 다운로드하도록 하는 응답을 생성합니다. 두 번째 인수로 파일명을 지정할 수 있으며, 세 번째 인수에는 HTTP 헤더 배열을 전달할 수 있습니다.

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL (File URLs)

`url` 메서드를 통해 특정 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용하는 경우 일반적으로 경로 앞에 `/storage`를 붙여서 상대 URL을 반환합니다. `s3` 드라이버를 사용하는 경우 전체 경로의 외부 URL이 반환됩니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 사용하는 경우, 공개적으로 접근 가능한 모든 파일은 반드시 `storage/app/public` 디렉터리에 저장되어야 하며, [심볼릭 링크](#the-public-disk)를 생성해 `public/storage`에서 접근할 수 있도록 해야 합니다.

> [!WARNING]
> `local` 드라이버를 사용하는 경우, `url`의 반환값은 URL 인코딩이 적용되지 않습니다. 따라서 반드시 유효한 URL이 될 수 있는 파일명(영문, 숫자, 일부 특수문자)만을 사용해 파일을 저장할 것을 권장합니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

만약 `Storage` 파사드를 통해 생성되는 URL의 호스트를 변경하려면, 디스크의 설정 배열에서 `url` 옵션을 추가하거나 수정할 수 있습니다.

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

`temporaryUrl` 메서드를 사용해 `local`과 `s3` 드라이버로 저장된 파일에 대해 임시 접근 URL을 생성할 수 있습니다. 이 메서드는 파일 경로와 만료 시각을 지정하는 `DateTime` 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

애플리케이션 개발을 임시 URL 기능이 도입되기 전부터 시작했다면, 로컬 임시 URL 기능을 수동으로 활성화해야 할 수 있습니다. 이를 위해, `config/filesystems.php` 파일에서 `local` 디스크 설정 배열에 `serve` 옵션을 추가하세요.

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```

<a name="s3-request-parameters"></a>
#### S3 요청 파라미터 사용

추가적인 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, `temporaryUrl` 메서드의 세 번째 인수로 배열을 전달할 수 있습니다.

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

특정 스토리지 디스크에 대해 임시 URL 생성 방식을 커스터마이징하고 싶을 때, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 임시 URL을 지원하지 않는 디스크의 파일 다운로드 컨트롤러에서 임시 서명된 라우트를 활용할 수 있습니다. 이 메서드는 주로 서비스 프로바이더의 `boot` 메서드에서 호출해야 합니다.

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
> 임시 업로드 URL 생성을 지원하는 드라이버는 `s3` 드라이버에 한정됩니다.

클라이언트 사이드 애플리케이션에서 직접 파일을 업로드할 수 있도록 임시 업로드 URL이 필요하다면, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 파일 경로와 만료 시각을 위한 `DateTime` 인스턴스를 받으며, 요청 시 포함해야 할 헤더와 업로드 URL을 담은 연관 배열을 반환합니다.

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

이 메서드는 주로 Amazon S3 같은 클라우드 스토리지로 클라이언트에서 직접 파일을 업로드해야 하는 서버리스 환경에서 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터 (File Metadata)

Laravel은 파일의 읽기/쓰기에 더해, 파일 자체의 정보도 제공할 수 있습니다. 예를 들어, `size` 메서드를 사용하면 해당 파일의 바이트 단위 크기를 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 시각의 UNIX 타임스탬프를 반환합니다.

```php
$time = Storage::lastModified('file.jpg');
```

특정 파일의 MIME 타입은 `mimeType` 메서드로 확인할 수 있습니다.

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로 (File Paths)

`path` 메서드를 사용하면 특정 파일의 경로를 얻을 수 있습니다. `local` 드라이버에서는 파일의 절대 경로가, `s3` 드라이버에서는 S3 버킷 내의 상대 경로가 반환됩니다.

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장 (Storing Files)

`put` 메서드는 파일의 내용을 디스크에 저장하는 데 사용할 수 있습니다. 또한 PHP `resource`를 직접 전달할 수도 있으며, 이 경우 Flysystem의 스트림 지원 기능이 사용됩니다. 모든 파일 경로는 해당 디스크의 "root" 위치 기준으로 상대 경로로 지정해야 합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 쓰기 실패 처리 (Failed Writes)

만약 `put` 메서드(또는 기타 "쓰기" 작업)가 파일을 디스크에 저장하지 못했다면, `false`를 반환합니다.

```php
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```

원한다면, 파일 시스템 디스크 설정 배열에 `throw` 옵션을 정의할 수 있습니다. 이 값을 `true`로 지정하면, `put` 같은 "쓰기" 메서드에서 저장 작업이 실패할 경우 `League\Flysystem\UnableToWriteFile` 인스턴스를 예외로 던집니다.

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일에 앞뒤로 내용 추가하기 (Prepending and Appending To Files)

`prepend`와 `append` 메서드를 사용하면 파일의 맨 앞이나 맨 뒤에 내용을 추가할 수 있습니다.

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동 (Copying and Moving Files)

`copy` 메서드는 기존 파일을 새 위치에 복사할 때 사용합니다. `move` 메서드는 파일명을 변경하거나 새 위치로 옮길 때 사용합니다.

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍 (Automatic Streaming)

파일을 스트리밍 저장하면 메모리 사용량을 상당히 줄일 수 있습니다. Laravel이 자동으로 파일을 지정한 위치로 스트리밍 처리하게 하려면, `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드들은 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 전달받아 자동으로 파일을 스트리밍하여 저장합니다.

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 자동으로 고유 ID로 파일명을 지정...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 수동으로 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드에 대해 주의할 점:
- 디렉터리명만 지정하고 파일명은 지정하지 않을 경우, 고유 ID가 파일명으로 자동 생성됩니다.
- 파일의 확장자는 MIME 타입을 기반으로 결정됩니다.
- 실제 저장 후 반환되는 경로에는 생성된 파일명이 포함되어 있으므로, 데이터베이스에 이 경로를 저장할 수 있습니다.

또한, `putFile` 및 `putFileAs` 메서드는 저장 파일의 "공개 여부"를 지정하는 인수를 받을 수 있습니다. 이는 Amazon S3 등 클라우드 디스크에 저장된 파일을 URL로 공개하고자 할 때 유용합니다.

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드 (File Uploads)

웹 애플리케이션에서 가장 흔하게 파일 저장이 사용되는 사례 중 하나는 사용자가 업로드한 사진 및 문서 등입니다. Laravel은 업로드된 파일 인스턴스의 `store` 메서드를 이용해 파일 업로드와 저장을 매우 쉽게 처리할 수 있습니다. 원하는 저장 경로만 인자로 넘기면 됩니다.

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

위 예시에서 주의할 점은,
- 파일명은 지정하지 않았고 디렉터리명만 지정했습니다.
- 기본적으로 `store` 메서드는 고유 ID를 파일명으로 생성하고, 확장자는 MIME 타입을 통해 판단합니다.
- 반환값으로는 실제 저장 경로(파일명 포함)가 반환되어 데이터베이스에 바로 저장할 수 있습니다.

동일한 동작을 `Storage` 파사드의 `putFile` 메서드를 사용하여 수행할 수도 있습니다.

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정 (Specifying a File Name)

저장 파일명을 자동으로 지정하지 않고 직접 지정하려면, `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일명, (선택적으로) 디스크명을 인수로 받습니다.

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

동일한 동작을 `Storage` 파사드의 `putFileAs` 메서드로 수행할 수도 있습니다.

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 인쇄 불가능한(unprintable) 문자나 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 파일 저장 메서드에 경로를 넘기기 전에 파일 경로를 정제(정규화)할 것을 권장합니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드를 통해 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정 (Specifying a Disk)

기본적으로 업로드 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 사용하려면 두 번째 인수로 디스크명을 전달하세요.

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드의 경우, 디스크명을 세 번째 인수로 전달합니다.

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 업로드 파일의 기타 정보 (Other Uploaded File Information)

업로드된 파일의 원래 이름과 확장자를 가져오길 원한다면, `getClientOriginalName` 및 `getClientOriginalExtension` 메서드를 사용할 수 있습니다.

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

단, 이 메서드들은 안전하지 않습니다. 악의적인 사용자가 파일명이나 확장자를 조작할 수 있기 때문입니다. 따라서 일반적으로는 `hashName` 메서드로 고유하고 무작위의 파일명을 생성하고, `extension` 메서드로 MIME 타입에 기반한 확장자를 얻는 것을 권장합니다.

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하며 무작위 파일명 생성...
$extension = $file->extension(); // MIME 타입을 기반으로 한 파일 확장자...
```

<a name="file-visibility"></a>
### 파일 공개/비공개 설정 (File Visibility)

Laravel의 Flysystem 통합에서 "공개 여부(visibility)"는 다양한 플랫폼에 걸친 파일 권한의 추상화입니다. 파일은 `public` 또는 `private`로 선언할 수 있습니다. 파일이 `public`으로 선언된 경우 일반적으로 외부에서 접근 가능한 파일임을 의미합니다. 예를 들어, S3 드라이버를 사용할 경우 `public`으로 선언된 파일에 대해 URL을 가져올 수 있습니다.

파일을 저장할 때 `put` 메서드에서 visibility를 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 공개 여부 역시 `getVisibility`와 `setVisibility` 메서드로 조회 및 변경이 가능합니다.

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일을 사용할 때, `storePublicly` 및 `storePubliclyAs` 메서드를 통해 `public` 권한으로 저장할 수 있습니다.

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 공개 여부 (Local Files and Visibility)

`local` 드라이버를 사용할 경우, `public` [공개 여부](#file-visibility)는 디렉터리에는 `0755`, 파일에는 `0644` 권한으로 매핑됩니다. 권한 매핑은 애플리케이션의 `filesystems` 설정 파일에서 수정할 수 있습니다.

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

`delete` 메서드는 하나의 파일명 또는 파일명 배열을 인수로 받아 해당 파일들을 삭제합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면, 파일이 삭제될 디스크도 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리 (Directories)

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 조회 (Get All Files Within a Directory)

`files` 메서드는 지정된 디렉터리 내의 모든 파일 목록 배열을 반환합니다. 하위 디렉터리를 포함한 전체 파일 목록을 얻고 싶으면 `allFiles` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 폴더 조회 (Get All Directories Within a Directory)

`directories` 메서드는 지정된 디렉터리 내의 모든 하위 디렉터리 목록 배열을 반환합니다. 전체 하위 디렉터리(서브폴더)까지 모두 조회할 때는 `allDirectories` 메서드를 사용하면 됩니다.

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성 (Create a Directory)

`makeDirectory` 메서드는 지정한 경로에 디렉터리를 생성하며, 필요하면 하위 디렉터리도 함께 만듭니다.

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제 (Delete a Directory)

마지막으로, `deleteDirectory` 메서드는 디렉터리와 그 안의 모든 파일을 제거할 수 있습니다.

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트 (Testing)

`Storage` 파사드의 `fake` 메서드는 임시로 사용할 수 있는 더미(페이크) 디스크를 생성해 주며, `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합하면 파일 업로드 테스트를 매우 간단하게 할 수 있습니다. 예를 들어,

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

    // 파일이 저장되었는지 확인...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // 파일이 저장되지 않았는지 확인...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // 특정 디렉터리 내 파일 수가 예상한 값과 일치하는지 확인...
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

        // 파일이 저장되었는지 확인...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 파일이 저장되지 않았는지 확인...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉터리 내 파일 수가 예상한 값과 일치하는지 확인...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // 특정 디렉터리가 비어 있는지 확인...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉터리 내의 모든 파일을 테스트 후 삭제합니다. 만약 이 파일들을 보존하고 싶다면, `"persistentFake"` 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대한 자세한 정보는 [HTTP 테스트 문서의 파일 업로드 테스트](/docs/12.x/http-tests#testing-file-uploads) 항목을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD 확장 모듈](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템 (Custom Filesystems)

Laravel의 Flysystem 통합은 몇 가지 "드라이버"를 기본으로 지원하지만, Flysystem은 여기에 제한되지 않고 다양한 스토리지 시스템에 대한 어댑터도 제공합니다. 만약 추가 어댑터를 사용하는 커스텀 드라이버가 필요하다면, Laravel 애플리케이션에서 직접 생성할 수 있습니다.

커스텀 파일 시스템을 정의하려면 우선 사용할 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 유지 관리하는 Dropbox 어댑터를 프로젝트에 설치해 보겠습니다.

```shell
composer require spatie/flysystem-dropbox
```

그런 다음, 애플리케이션 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 해당 드라이버를 등록할 수 있습니다. 이때 `Storage` 파사드의 `extend` 메서드를 사용합니다.

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

`extend` 메서드의 첫 번째 인수는 드라이버의 이름이고, 두 번째 인수는 `$app`과 `$config` 변수를 받는 클로저입니다. 클로저는 반드시 `Illuminate\Filesystem\FilesystemAdapter`의 인스턴스를 반환해야 합니다. `$config` 변수는 지정한 디스크의 `config/filesystems.php` 설정 값들을 담고 있습니다.

확장 서비스 프로바이더를 작성해 등록한 이후에는, `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.

