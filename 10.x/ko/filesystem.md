# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 획득](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞/뒤에 쓰기](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [테스트](#testing)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 만든 훌륭한 PHP 패키지인 [Flysystem](https://github.com/thephpleague/flysystem)을 기반으로 강력한 파일 시스템 추상화를 제공합니다. Laravel의 Flysystem 통합은 로컬 파일 시스템, SFTP, Amazon S3 등을 다루기 위한 간단한 드라이버를 제공하며, 각 저장소 시스템에 대해 같은 API를 사용하므로 로컬 개발 환경과 프로덕션 서버 사이에서 저장 옵션을 쉽게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정

Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일 시스템 "디스크"를 설정할 수 있으며, 각 디스크는 특정 저장 드라이버와 저장 위치를 나타냅니다. 지원되는 각 드라이버에 대한 설정 예시가 포함되어 있으니, 이를 바탕으로 여러분의 저장소 환경과 자격증명에 맞게 설정을 변경하세요.

`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버에 로컬로 저장된 파일과 상호작용하며, `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스와 연동됩니다.

> [!NOTE]  
> 원하는 만큼 디스크를 구성할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크를 가질 수도 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 경우, 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉터리를 기준으로 합니다. 기본값은 `storage/app` 디렉터리로 설정되어 있습니다. 따라서 아래 코드는 `storage/app/example.txt`에 파일을 씁니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 웹에서 공개적으로 접근할 파일을 위한 용도로 설계되었습니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일을 `storage/app/public`에 저장합니다.

이 파일들을 웹에서 접근 가능하도록 만들려면 `public/storage`를 `storage/app/public`으로 심볼릭 링크를 생성해야 합니다. 이런 폴더 구성을 사용하면 [Envoyer](https://envoyer.io)와 같은 무중단 배포 시스템에서 파일을 쉽게 공유할 수 있습니다.

심볼릭 링크는 Artisan 명령어 `storage:link`로 생성할 수 있습니다:

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성하면, `asset` 헬퍼를 이용해 파일에 대한 URL을 만들 수 있습니다:

```
echo asset('storage/file.txt');
```

`filesystems` 설정 파일에서 추가적인 심볼릭 링크를 구성할 수도 있으며, `storage:link` 명령어를 실행할 때 설정된 모든 링크가 생성됩니다:

```
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

구성된 심볼릭 링크를 제거하려면 `storage:unlink` 명령어를 사용할 수 있습니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하기 전에, Composer 패키지 관리자를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 드라이버 설정은 `config/filesystems.php` 파일에 위치하며, 예시 배열이 포함되어 있어 자신의 S3 자격증명과 설정에 따라 수정할 수 있습니다. 환경 변수는 AWS CLI에서 사용하는 명명 규칙과 동일하게 되어 있어 편리합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에, Composer를 통해 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel Flysystem 통합은 FTP와도 잘 작동하지만, 기본 `filesystems.php`에는 FTP 예시 설정이 포함되어 있지 않습니다. FTP 파일시스템을 설정하려면 다음 예시를 사용할 수 있습니다:

```
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // 선택적 설정 ...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하기 전에, Composer를 통해 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel Flysystem 통합은 SFTP와도 잘 작동하지만, 기본 `filesystems.php`에는 SFTP 예시 설정이 포함되어 있지 않습니다. SFTP 파일시스템을 설정하려면 다음 예시를 사용할 수 있습니다:

```
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 기반 인증 설정 (암호 포함)...
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

스코프 디스크(scoped disks)는 모든 경로가 지정된 접두사로 자동으로 접두사화되는 파일시스템을 정의할 때 사용합니다. 스코프 파일시스템 디스크를 생성하려면 Composer로 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존의 파일 시스템 디스크 중 하나를 스코프 인스턴스로 만들고 싶은 경우, `scoped` 드라이버를 사용하는 디스크를 정의하면 됩니다. 예를 들어, 기존 `s3` 디스크를 특정 경로 접두사로 스코핑할 수 있습니다. 그 후 스코프 디스크를 사용할 때 모든 파일 작업은 지정된 접두사를 사용합니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크는 쓰기 작업을 허용하지 않는 파일 시스템 디스크를 만들 때 사용합니다. `read-only` 설정을 사용하기 전에 Composer로 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

그 후, 하나 이상의 디스크 구성 배열에 `read-only` 옵션을 포함시킬 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

기본적으로 `filesystems` 설정 파일에 `s3` 디스크가 구성되어 있습니다. 이 디스크를 사용하여 Amazon S3와 통신할 뿐만 아니라, [MinIO](https://github.com/minio/minio)나 [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/) 같은 S3 호환 스토리지 서비스와도 상호작용할 수 있습니다.

보통은 디스크 자격증명을 해당 서비스에 맞게 업데이트하고, `endpoint` 설정 값만 수정하면 됩니다. 이 값은 보통 `AWS_ENDPOINT` 환경 변수로 설정합니다:

```
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

Laravel의 Flysystem 통합이 MinIO 사용 시 올바른 URL을 생성하려면, `AWS_URL` 환경 변수를 애플리케이션의 로컬 URL과 버킷 이름을 포함하도록 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]  
> MinIO에서 `temporaryUrl` 메서드를 이용해 임시 스토리지 URL을 생성하는 것은 지원되지 않습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 획득

`Storage` 퍼사드를 사용하면 설정해 둔 모든 디스크와 상호작용할 수 있습니다. 예를 들어 기본 디스크에 아바타를 저장할 때는 `put` 메서드를 사용할 수 있습니다. `disk` 메서드를 호출하지 않고 `Storage` 퍼사드의 메서드를 호출하면 기본 디스크에 적용됩니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

애플리케이션에서 여러 디스크를 사용할 경우, 작업하고자 하는 특정 디스크를 `disk` 메서드로 지정할 수 있습니다:

```
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

때로는 애플리케이션 `filesystems` 설정 파일에 없더라도, 런타임에 특정 설정값으로 디스크를 생성하고 싶을 때가 있습니다. 이 경우 `Storage` 퍼사드의 `build` 메서드에 구성 배열을 전달하여 디스크를 생성할 수 있습니다:

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

`get` 메서드는 파일 내용을 가져올 때 사용하며, 파일의 원본 문자열 내용을 반환합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 지정해야 합니다:

```
$contents = Storage::get('file.jpg');
```

가져오는 파일이 JSON 형식인 경우, `json` 메서드를 사용하여 파일을 불러오고 디코딩할 수 있습니다:

```
$orders = Storage::json('orders.json');
```

`exists` 메서드는 해당 파일이 디스크에 존재하는지 확인할 때 사용합니다:

```
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 해당 파일이 디스크에 존재하지 않는지 확인할 때 사용합니다:

```
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 주어진 경로의 파일을 강제로 다운로드하도록 응답을 생성합니다. 두 번째 인자로는 사용자가 보게 될 파일명을 지정할 수 있으며, 세 번째 인자로는 HTTP 헤더 배열을 전달할 수 있습니다:

```
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드는 주어진 파일의 URL을 얻을 때 사용합니다. `local` 드라이버를 사용하는 경우, 주로 `/storage` 경로를 접두사로 붙여 상대 URL을 반환합니다. `s3` 드라이버라면 완전한 원격 URL이 반환됩니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 사용할 때 공개 접근이 필요한 모든 파일은 `storage/app/public` 디렉터리에 놓아야 하며, [심볼릭 링크 생성](#the-public-disk)도 반드시 진행해야 합니다.

> [!WARNING]  
> `local` 드라이버에서 `url` 메서드가 반환하는 값은 URL 인코딩된 형태가 아닙니다. 따라서 URL이 유효하게 생성되도록 파일명에 특수 문자가 없게 저장하는 것이 좋습니다.

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 퍼사드로 생성하는 URL의 호스트를 미리 정의하고 싶다면, 디스크 설정 배열에 `url` 옵션을 추가할 수 있습니다:

```
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
],
```

<a name="temporary-urls"></a>
### 임시 URL

`temporaryUrl` 메서드를 사용하면 `s3` 드라이버로 저장된 파일에 대한 만료 기간이 제한된 임시 URL을 생성할 수 있습니다. 만료 시간을 지정하는 `DateTime` 인스턴스를 두 번째 인자로 전달합니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

추가 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, 세 번째 인자로 배열로 넘길 수 있습니다:

```
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->addMinutes(5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

특정 스토리지 디스크에 대해 임시 URL 생성 방식을 커스터마이징하고 싶다면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 보통은 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다. 예시:

```
<?php

namespace App\Providers;

use DateTime;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 부트스트랩(초기화) 메서드
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

클라이언트 측 애플리케이션이 파일을 직접 업로드할 수 있도록 임시 업로드 URL을 생성해야 한다면, `temporaryUploadUrl` 메서드를 사용하세요. 경로와 만료 시간(DateTime)을 인자로 받고, 업로드 URL과 업로드 요청에 포함시킬 헤더를 포함하는 연관 배열을 반환합니다:

```
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->addMinutes(5)
);
```

이 기능은 서버리스 환경에서 클라이언트가 Amazon S3 같은 클라우드 스토리지에 직접 파일을 업로드할 때 매우 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터

Laravel은 파일을 읽고 쓰는 것 외에도 파일 자체에 관한 정보를 제공할 수 있습니다. 예를 들어, `size` 메서드는 파일 크기를 바이트 단위로 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 마지막 수정 시간을 UNIX 타임스탬프로 반환합니다:

```
$time = Storage::lastModified('file.jpg');
```

`mimeType` 메서드는 주어진 파일의 MIME 타입을 반환합니다:

```
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용하면 지정된 파일의 경로를 얻을 수 있습니다. `local` 드라이버의 경우 파일의 절대 경로를 반환하며, `s3` 드라이버라면 S3 버킷 내의 상대 경로를 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 디스크에 파일 내용을 저장할 때 사용합니다. PHP `resource`도 전달할 수 있으며, Flysystem의 스트림 기능을 활용합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 지정하세요:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 실패한 쓰기 작업 처리

`put` 메서드(또는 기타 쓰기 작업)가 파일을 저장하지 못하면 `false`를 반환합니다:

```
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 디스크에 쓸 수 없었음...
}
```

원한다면 디스크 설정 배열에 `throw` 옵션을 `true`로 설정할 수도 있습니다. 그러면 `put` 같은 쓰기 메서드가 실패할 때 `League\Flysystem\UnableToWriteFile` 예외를 던집니다:

```
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일 앞/뒤에 쓰기

`prepend` 및 `append` 메서드는 파일의 앞부분 또는 뒷부분에 내용을 추가할 수 있습니다:

```
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 디스크 내 기존 파일을 새로운 위치로 복사할 때 사용하며, `move` 메서드는 이름 변경 또는 새 위치로 파일을 이동할 때 사용합니다:

```
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

스토리지에 파일을 스트리밍하면 메모리 사용량이 크게 줄어듭니다. `putFile` 또는 `putFileAs` 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 자동으로 스트리밍하여 파일을 저장합니다:

```
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명을 고유 ID로 자동 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 수동으로 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드는 디렉터리명만 지정하고 파일명을 지정하지 않으면 고유한 ID를 파일명으로 생성합니다. 파일 확장자는 MIME 타입을 조사해 결정하며, 저장된 파일 경로(생성된 파일명 포함)를 반환합니다.

`putFile`와 `putFileAs`는 파일 가시성(Visibility)을 지정하는 인수도 받을 수 있으며, 특히 Amazon S3 같은 클라우드 디스크에 파일을 저장할 때 공개 접근 가능하도록 설정하는 데 유용합니다:

```
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 흔한 저장 사례는 사용자가 업로드한 사진, 문서 등을 저장하는 것입니다. Laravel은 업로드된 파일 인스턴스에 `store` 메서드를 호출하는 것으로 쉽게 저장할 수 있습니다. 저장할 경로를 인자로 전달하세요:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자 아바타 업데이트
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

이 예시에서 중요한 점은 디렉터리명만 지정하고 파일명은 지정하지 않았다는 것입니다. 기본적으로 `store` 메서드는 파일명으로 사용할 고유 ID를 생성하며, 확장자는 MIME 타입을 기반으로 결정됩니다. 저장된 경로(생성된 파일명 포함)를 데이터베이스에 저장할 수 있습니다.

앞선 예제와 같은 작업은 `Storage` 퍼사드의 `putFile` 메서드를 호출해도 동일하게 수행할 수 있습니다:

```
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정

자동 생성되는 파일명이 아니라 직접 지정하고 싶다면, 경로, 파일명, 그리고 (선택적으로) 디스크명을 인자로 받는 `storeAs` 메서드를 사용할 수 있습니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

위와 동일한 작업은 `Storage` 퍼사드의 `putFileAs` 메서드로도 수행할 수 있습니다:

```
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]  
> 출력 불가능하거나 유효하지 않은 유니코드 문자들은 파일 경로에서 자동으로 제거됩니다. 따라서, Laravel의 파일 저장 메서드에 경로를 넘기기 전에 파일 경로를 정리하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드를 사용해 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

기본적으로 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 지정하려면 `store` 메서드 두 번째 인자로 디스크명을 전달하세요:

```
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드를 사용할 경우, 디스크명은 세 번째 인자로 전달합니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 기타 업로드된 파일 정보

업로드된 파일의 원본 이름과 확장자를 얻으려면 `getClientOriginalName`과 `getClientOriginalExtension` 메서드를 사용하세요:

```
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만 이 메서드들은 파일명과 확장자를 조작한 악의적 사용자에 의해 변조될 수 있으므로 안전하지 않습니다. 그래서 보통 `hashName`과 `extension` 메서드를 사용해 무작위 고유명과 MIME 타입 기반 확장자를 얻는 것을 권장합니다:

```
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 무작위인 이름 생성
$extension = $file->extension(); // MIME 타입에 기반해 확장자 결정
```

<a name="file-visibility"></a>
### 파일 가시성

Laravel의 Flysystem 통합에서 "가시성(visibility)"은 여러 플랫폼 간 파일 권한을 추상화한 개념입니다. 파일은 `public` 또는 `private`으로 선언할 수 있습니다. `public`으로 설정하면 일반적으로 외부에서 접근 가능해야 할 파일임을 의미합니다. 예를 들어, S3 드라이버에서 `public` 파일은 URL을 통해 접근할 수 있습니다.

`put` 메서드로 파일을 쓸 때 가시성을 지정할 수 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 가시성은 `getVisibility`과 `setVisibility` 메서드로 조회 및 변경할 수 있습니다:

```
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일과 작업할 때는 `storePublicly` 및 `storePubliclyAs` 메서드를 사용해 `public` 가시성을 지정하며 저장할 수 있습니다:

```
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일과 가시성

`local` 드라이버 사용 시 `public` 가시성은 디렉터리는 `0755` 권한, 파일은 `0644` 권한으로 매핑됩니다. 애플리케이션의 `filesystems` 설정 파일에서 권한 매핑을 변경할 수 있습니다:

```
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
],
```

<a name="deleting-files"></a>
## 파일 삭제

`delete` 메서드는 단일 파일명 또는 삭제할 파일 이름들의 배열을 인자로 받을 수 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면 삭제할 파일의 디스크를 지정할 수도 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 가져오기

`files` 메서드는 특정 디렉터리 내 모든 파일을 배열로 반환합니다. 하위 디렉터리 포함 모든 파일을 가져오려면 `allFiles` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 하위 디렉터리 가져오기

`directories` 메서드는 특정 디렉터리 내부 하위 디렉터리를 배열로 반환합니다. 또한 `allDirectories` 메서드로 하위 디렉터리를 포함한 모든 디렉터리를 가져올 수 있습니다:

```
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성

`makeDirectory` 메서드는 지정된 디렉터리와 필요한 모든 하위 디렉터리를 생성합니다:

```
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제

`deleteDirectory` 메서드는 디렉터리와 그 안의 모든 파일을 삭제합니다:

```
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
## 테스트

`Storage` 퍼사드의 `fake` 메서드는 파일 업로드 테스트를 쉽게 할 수 있도록 가짜 디스크를 생성해줍니다. `Illuminate\Http\UploadedFile` 클래스의 파일 생성 도구와 결합해 매우 편리합니다. 예시는 다음과 같습니다:

```
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

        // 하나 이상의 파일이 저장되었는지 검증...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 존재하지 않는 파일이 저장되지 않았음을 검증...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉터리가 비어있는지 검증...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉터리 내 모든 파일을 삭제합니다. 파일을 유지하고 싶다면 대신 `persistentFake` 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 관한 더 자세한 내용은 [HTTP 테스트 문서 내 파일 업로드](https://laravel.kr/docs/10.x/http-tests#testing-file-uploads) 부분을 참고하세요.

> [!WARNING]  
> `image` 메서드 호출에는 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
## 커스텀 파일시스템

Laravel의 Flysystem 통합은 기본적인 여러 "드라이버"를 기본 지원하지만, Flysystem은 이외에 다양한 어댑터를 제공합니다. 이러한 추가 어댑터를 Laravel 애플리케이션에서 사용하기 위해 커스텀 드라이버를 만들 수 있습니다.

커스텀 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가하려면:

```shell
composer require spatie/flysystem-dropbox
```

다음으로, 애플리케이션의 [서비스 프로바이더](/docs/10.x/providers) 중 하나의 `boot` 메서드에서 `Storage` 퍼사드의 `extend` 메서드를 사용해 드라이버를 등록합니다:

```
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
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
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

`extend` 메서드의 첫 인자는 드라이버 이름이며, 두 번째 인자는 `$app`과 `$config` 변수를 받는 클로저입니다. 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 하며, `$config`에는 `config/filesystems.php`에 지정된 해당 디스크 설정 값들이 포함되어 있습니다.

확장자의 서비스 프로바이더를 생성 및 등록한 후, `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용해 디스크를 구성할 수 있습니다.