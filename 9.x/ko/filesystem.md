# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 필수 조건](#driver-prerequisites)
    - [스코프 및 읽기 전용 파일시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞/뒤에 내용 추가](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 만든 훌륭한 PHP 패키지인 [Flysystem](https://github.com/thephpleague/flysystem)의 덕분에 강력한 파일시스템 추상화를 제공합니다. Laravel의 Flysystem 통합은 로컬 파일시스템, SFTP, Amazon S3와 작업할 수 있는 간단한 드라이버를 제공합니다. 더욱이, 각 스토리지 시스템에 대해 동일한 API를 사용하기 때문에 로컬 개발 환경과 프로덕션 서버 간에 이 스토리지 옵션을 쉽게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정

Laravel의 파일시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 저장 위치를 나타냅니다. 지원되는 각 드라이버에 대한 예제 구성이 설정 파일에 포함되어 있어 스토리지 설정과 인증 정보를 원하는 대로 수정할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버에 로컬로 저장된 파일과 상호작용하며, `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스에 기록하는 데 사용됩니다.

> [!NOTE]
> 필요에 따라 원하는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크가 있을 수도 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉터리를 기준으로 상대 경로로 처리됩니다. 기본적으로 이 값은 `storage/app` 디렉터리로 설정되어 있습니다. 따라서 아래 메서드는 `storage/app/example.txt` 위치에 파일을 작성합니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 공개적으로 접근 가능한 파일을 위한 용도입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며 파일을 `storage/app/public`에 저장합니다.

이 파일들을 웹에서 접근 가능하게 하려면 `public/storage`에서 `storage/app/public`으로의 심볼릭 링크를 생성해야 합니다. 이러한 폴더 구조 규칙을 사용하면, [Envoyer](https://envoyer.io)와 같은 무중단 배포 시스템을 사용할 때 공개 파일들을 쉽게 공유할 수 있는 단일 디렉터리에 보관할 수 있습니다.

다음의 Artisan 명령어로 심볼릭 링크를 생성할 수 있습니다:

```shell
php artisan storage:link
```

한 번 파일이 저장되고 심볼릭 링크가 만들어지면 `asset` 헬퍼를 이용해 파일에 대한 URL을 생성할 수 있습니다:

```
echo asset('storage/file.txt');
```

`filesystems` 설정 파일에서 추가 심볼릭 링크를 구성할 수도 있습니다. `storage:link` 명령이 실행될 때 설정한 모든 링크가 생성됩니다:

```
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

<a name="driver-prerequisites"></a>
### 드라이버 필수 조건

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하려면 먼저 Composer로 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0"
```

S3 드라이버 설정 정보는 `config/filesystems.php`에 위치합니다. 이 파일에는 S3 드라이버 예제 구성 배열이 포함되어 있으며, 자신의 S3 인증 정보와 설정에 맞게 자유롭게 수정할 수 있습니다. 편의를 위해 이 환경 변수들은 AWS CLI와 동일한 이름 규칙을 따릅니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하려면 Composer로 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와 잘 작동하지만, 기본 `filesystems.php` 설정 파일에는 FTP 샘플 구성이 포함되어 있지 않습니다. FTP 파일시스템을 구성하려면 아래 예제를 참조하세요:

```
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

SFTP 드라이버를 사용하려면 Composer로 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 잘 작동하지만, 기본 `filesystems.php` 설정 파일에는 SFTP 샘플 구성이 포함되어 있지 않습니다. SFTP 파일시스템을 구성하려면 아래 예제를 참조하세요:

```
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키 기반 인증 설정 (암호화 비밀번호 포함)...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

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

스코프 디스크는 모든 경로에 자동으로 특정 접두어가 붙는 파일시스템을 정의할 수 있게 해줍니다. 스코프 파일시스템 디스크를 생성하려면 추가 Flysystem 패키지를 Composer로 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

기존의 파일시스템 디스크에 대해 스코프 인스턴스를 생성하려면 `scoped` 드라이버를 사용하는 디스크를 정의하세요. 예를 들어, 기존 `s3` 디스크를 특정 경로 접두어로 스코프하는 디스크를 만들 수 있으며, 이 스코프 디스크를 통해 이루어지는 모든 파일 작업에 지정한 접두어가 자동으로 적용됩니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"읽기 전용" 디스크는 쓰기 작업이 허용되지 않는 파일시스템 디스크를 만들 수 있게 해줍니다. `read-only` 구성 옵션을 사용하려면 추가 Flysystem 패키지를 Composer로 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

그다음, 디스크 구성 배열 중 하나 이상에 `read-only` 옵션을 포함할 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

애플리케이션의 기본 `filesystems` 설정 파일에는 `s3` 디스크 구성이 포함되어 있습니다. 이 디스크는 Amazon S3와 상호작용하는 데 사용될 뿐만 아니라 [MinIO](https://github.com/minio/minio)나 [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/)와 같은 S3 호환 파일 스토리지 서비스와의 상호작용에도 사용할 수 있습니다.

일반적으로, 해당 서비스의 인증 정보에 맞게 디스크의 인증 정보를 업데이트한 뒤 `endpoint` 구성 옵션 값만 변경하면 됩니다. 이 옵션 값은 보통 `AWS_ENDPOINT` 환경 변수로 지정됩니다:

```
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
#### MinIO

Laravel의 Flysystem 통합이 MinIO 사용 시 올바른 URL을 생성하려면, 앱의 로컬 URL과 버킷명을 URL 경로에 포함하는 `AWS_URL` 환경 변수를 정의해야 합니다:

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> MinIO 사용 시 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성은 지원되지 않습니다.

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드를 사용해 구성한 어떤 디스크와도 상호작용할 수 있습니다. 예를 들어 `put` 메서드를 사용하면 기본 디스크에 아바타를 저장할 수 있습니다. `disk` 메서드를 호출하지 않고 `Storage` 파사드 메서드를 호출하면 이 메서드는 자동으로 기본 디스크에서 실행됩니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크와 상호작용하는 앱이라면, `disk` 메서드를 사용해 특정 디스크에 있는 파일을 조작할 수 있습니다:

```
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

경우에 따라 `filesystems` 구성 파일에 등록되어 있지 않은 설정으로 런타임에 디스크를 생성하고 싶을 수도 있습니다. 이때는 `Storage` 파사드의 `build` 메서드에 구성 배열을 전달하면 됩니다:

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

`get` 메서드는 파일 내용을 가져오는 데 사용됩니다. 이 메서드는 파일의 원본 문자열 내용을 반환합니다. 모든 파일 경로는 디스크의 “root” 위치 기준으로 지정해야 한다는 점을 기억하세요:

```
$contents = Storage::get('file.jpg');
```

`exists` 메서드는 디스크에 파일이 존재하는지 확인할 때 사용합니다:

```
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 디스크에 파일이 없는지 확인할 때 사용합니다:

```
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 주어진 경로의 파일을 강제로 다운로드하도록 응답을 생성합니다. 두 번째 인자로는 다운로드 시 보여질 파일명을 지정할 수 있고, 세 번째 인자로는 HTTP 헤더 배열을 전달할 수 있습니다:

```
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 사용해 주어진 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용할 경우 보통 `/storage`가 경로 앞에 붙은 상대 URL을 반환하며, `s3` 드라이버 사용할 경우 완전한 원격 URL을 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버 사용 시 공개적으로 접근할 파일은 `storage/app/public`에 위치해야 하며, [심볼릭 링크 생성](#the-public-disk)으로 `public/storage`가 `storage/app/public`을 가리켜야 합니다.

> [!WARNING]
> `local` 드라이버 사용 시 `url` 메서드 반환값은 URL 인코딩되지 않습니다. 따라서 항상 올바른 URL이 생성될 수 있도록 파일명을 안전하게 설정할 것을 권장합니다.

<a name="temporary-urls"></a>
#### 임시 URL

`temporaryUrl` 메서드를 사용하면 `s3` 드라이버로 저장된 파일에 대해 만료 시한이 있는 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL 만료 시각을 `DateTime` 인스턴스로 받습니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

추가 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 지정하려면 이들 파라미터 배열을 세 번째 인자로 넘기면 됩니다:

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

특정 스토리지 디스크에서 임시 URL 생성 방식을 맞춤 설정하고 싶다면 `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 통상적으로 임시 URL을 지원하지 않는 디스크에 저장된 파일을 다운로드하도록 하는 컨트롤러에서 사용할 수 있습니다. 보통 이 메서드는 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 부트스트랩 애플리케이션 서비스를 실행합니다.
     *
     * @return void
     */
    public function boot()
    {
        Storage::disk('local')->buildTemporaryUrlsUsing(function ($path, $expiration, $options) {
            return URL::temporarySignedRoute(
                'files.download',
                $expiration,
                array_merge($options, ['path' => $path])
            );
        });
    }
}
```

<a name="url-host-customization"></a>
#### URL 호스트 커스터마이징

`Storage` 파사드에서 생성된 URL의 호스트를 미리 정의하고 싶다면, 디스크 구성 배열에 `url` 옵션을 추가할 수 있습니다:

```
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
],
```

<a name="file-metadata"></a>
### 파일 메타데이터

Laravel은 파일의 읽기 및 쓰기뿐만 아니라 파일 자체에 대한 정보를 제공할 수도 있습니다. 예를 들어, `size` 메서드로 파일 크기를 바이트 단위로 얻을 수 있습니다:

```
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 UNIX 타임스탬프를 반환합니다:

```
$time = Storage::lastModified('file.jpg');
```

특정 파일의 MIME 타입은 `mimeType` 메서드로 얻을 수 있습니다:

```
$mime = Storage::mimeType('file.jpg')
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용하면 특정 파일의 경로를 얻을 수 있습니다. `local` 드라이버 사용 시 절대 파일 경로를 반환하고, `s3` 드라이버 사용 시 S3 버킷 내 파일의 상대 경로를 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 파일 내용을 디스크에 저장하는 데 사용됩니다. PHP `resource` 타입을 `put` 메서드에 전달할 수도 있는데, 이 경우 Flysystem의 스트림 기능을 활용합니다. 모든 파일 경로는 디스크 설정의 "root" 기준으로 지정해야 합니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
#### 저장 실패

`put` 메서드(또는 다른 "쓰기" 작업 메서드)가 파일을 저장하지 못하면 `false`가 반환됩니다:

```
if (! Storage::put('file.jpg', $contents)) {
    // 파일을 디스크에 저장하지 못했습니다...
}
```

원한다면 파일시스템 디스크 구성 배열에 `throw` 옵션을 정의할 수 있습니다. 이 옵션이 `true`로 설정되면, `put` 같은 쓰기 메서드가 실패할 때 `League\Flysystem\UnableToWriteFile` 예외를 던집니다:

```
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
### 파일 앞/뒤에 내용 추가

`prepend`, `append` 메서드는 각각 파일의 시작 부분이나 끝 부분에 내용을 추가할 때 사용합니다:

```
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 디스크 내 새 위치로 복사하고, `move` 메서드는 파일을 새 위치로 이동하거나 이름을 변경할 때 사용합니다:

```
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 스트리밍하여 저장하면 메모리 사용량이 크게 줄어듭니다. 원하는 경우 `putFile` 또는 `putFileAs` 메서드를 사용해 파일을 자동으로 스트리밍하여 저장할 수 있습니다. 이들 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받습니다:

```
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명을 자동으로 고유 ID로 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 수동으로 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드에 대해 중요한 점을 두 가지 짚으면, 파일명 대신 디렉터리 이름만 지정했다는 점과, 메서드가 파일 확장자를 MIME 타입으로부터 자동으로 판단한다는 점입니다. `putFile`은 저장 위치의 경로를 반환하므로, 이 경로를 데이터베이스에 저장할 때 생성된 파일명도 함께 저장할 수 있습니다.

`putFile`, `putFileAs` 메서드는 저장된 파일의 "가시성"을 지정할 수 있는 인수를 받습니다. 이는 Amazon S3와 같은 클라우드 디스크에 파일을 저장할 때 공개 접근을 허용하는 데 유용합니다:

```
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 사용자 업로드 파일(예: 사진, 문서)을 저장하는 것은 흔한 경우입니다. Laravel은 업로드된 파일 인스턴스의 `store` 메서드를 사용해 업로드된 파일을 쉽게 저장할 수 있게 합니다. `store` 메서드에 저장할 경로를 넘겨 호출하면 됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자 아바타를 업데이트합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

예시에서 중요한 점은 파일명 대신 디렉터리만 지정했다는 점입니다. 기본적으로 `store` 메서드는 고유 ID를 파일명으로 생성하고, 파일 확장자는 MIME 타입에 기반해 결정합니다. `store`는 저장된 파일 경로를 반환하기 때문에, 이를 데이터베이스에 포함해 저장할 수 있습니다.

동일한 작업을 `Storage` 파사드의 `putFile` 메서드를 사용해 수행할 수도 있습니다:

```
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정하기

자동 지정된 파일명이 싫다면 `storeAs` 메서드를 사용하세요. 이 메서드는 경로, 파일명, 선택적으로 디스크명을 인수로 받습니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드의 `putFileAs` 메서드를 이용해 동일한 작업을 할 수도 있습니다:

```
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 인쇄 불가능하거나 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 Laravel의 파일 저장 메서드에 경로를 전달하기 전에 파일 경로를 정리하는 것을 권장합니다. 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정하기

기본적으로 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 지정하려면, `store`의 두 번째 인자로 디스크명을 넘기면 됩니다:

```
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드를 사용할 때는 세 번째 인자로 디스크명을 전달합니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 업로드된 파일의 추가 정보

업로드된 파일의 원래 이름과 확장자를 얻으려면 `getClientOriginalName`과 `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

하지만 이 메서드들은 파일명과 확장자가 악의적으로 조작될 수 있어서 안전하지 않은 것으로 간주됩니다. 보통은 `hashName`과 `extension` 메서드를 사용하는 것이 좋습니다. `hashName`은 고유하고 무작위적인 이름을 생성하며, `extension`은 파일 MIME 타입에 기반해 확장자를 결정합니다:

```
$file = $request->file('avatar');

$name = $file->hashName(); // 고유한 무작위 이름 생성
$extension = $file->extension(); // MIME 타입 기반 확장자 결정
```

<a name="file-visibility"></a>
### 파일 가시성

Laravel의 Flysystem 통합에서 "가시성"은 다양한 플랫폼 간의 파일 권한 추상화입니다. 파일은 `public` 또는 `private`으로 선언할 수 있습니다. `public` 파일은 일반적으로 다른 사람들이 접근할 수 있도록 허용한다는 의미입니다. 예를 들어, S3 드라이버 사용 시 `public` 파일은 URL로 접근할 수 있습니다.

파일을 쓸 때 `put` 메서드에서 가시성을 지정할 수 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일에 대해서는 `getVisibility`, `setVisibility` 메서드로 가시성을 확인하거나 변경할 수 있습니다:

```
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일을 다룰 때는 `storePublicly`와 `storePubliclyAs` 메서드를 사용해 `public` 가시성으로 저장할 수 있습니다:

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

`local` 드라이버 사용 시 `public` [가시성](#file-visibility)은 디렉터리에 대해 `0755` 권한, 파일에 대해 `0644` 권한으로 변환됩니다. 권한 매핑은 애플리케이션의 `filesystems` 설정 파일에서 수정할 수 있습니다:

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

`delete` 메서드는 단일 파일명 또는 삭제할 파일명 배열을 인자로 받습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요 시 파일을 삭제할 디스크를 지정할 수도 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 가져오기

`files` 메서드는 주어진 디렉터리 안의 모든 파일을 배열로 반환합니다. 하위 디렉터리를 포함한 모든 파일을 가져오려면 `allFiles` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 폴더 가져오기

`directories` 메서드는 주어진 디렉터리 내 모든 하위 디렉터리를 배열로 반환합니다. 또한, 하위 폴더까지 포함된 모든 디렉터리를 가져오려면 `allDirectories` 메서드를 사용할 수 있습니다:

```
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성

`makeDirectory` 메서드는 필요한 하위 디렉터리를 포함해 지정한 디렉터리를 생성합니다:

```
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제

`deleteDirectory` 메서드는 디렉터리와 그 안의 모든 파일을 삭제합니다:

```
Storage::deleteDirectory($directory);
```

<a name="custom-filesystems"></a>
## 커스텀 파일시스템

Laravel의 Flysystem 통합은 기본적으로 여러 "드라이버"를 지원하지만, Flysystem은 다양한 추가 스토리지 시스템 어댑터를 제공합니다. 이 중 하나를 Laravel 애플리케이션에서 사용하려면 커스텀 드라이버를 만들 수 있습니다.

우선 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티가 유지하는 Dropbox 어댑터를 프로젝트에 추가해보겠습니다:

```shell
composer require spatie/flysystem-dropbox
```

다음으로는 애플리케이션의 [서비스 프로바이더](/docs/9.x/providers) 중 하나의 `boot` 메서드에서 `Storage` 파사드의 `extend` 메서드를 사용해 드라이버를 등록합니다:

```
<?php

namespace App\Providers;

use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\ServiceProvider;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     *
     * @return void
     */
    public function boot()
    {
        Storage::extend('dropbox', function ($app, $config) {
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

`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 두 번째 인자는 `$app`과 `$config` 변수를 받는 클로저입니다. 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config` 변수에는 `config/filesystems.php`에서 지정한 디스크 설정 값이 포함됩니다.

확장 서비스 프로바이더를 생성 및 등록하면, `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.