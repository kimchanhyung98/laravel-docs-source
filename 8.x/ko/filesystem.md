# 파일 스토리지

- [소개](#introduction)
- [구성](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [Amazon S3 호환 파일 시스템](#amazon-s3-compatible-filesystems)
    - [캐싱](#caching)
- [디스크 인스턴스 얻기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 가져오기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉터리](#directories)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge의 놀라운 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일 시스템 추상화 계층을 제공합니다. Laravel의 Flysystem 통합을 통해 로컬 파일 시스템, SFTP, Amazon S3와 간편하게 연동할 수 있는 드라이버를 제공합니다. 더욱이, 개발 환경이나 운영 서버에서 파일 시스템 API가 동일하게 동작하므로, 저장 옵션을 간단하게 전환할 수 있습니다.

<a name="configuration"></a>
## 구성

Laravel의 파일 시스템 구성 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일 시스템 "디스크"를 구성할 수 있습니다. 각 디스크는 특정 저장 드라이버와 저장 위치를 나타냅니다. 지원하는 각 드라이버에 대한 예제 구성이 포함되어 있으므로, 자신의 저장 방식과 인증 정보를 반영하여 수정하시면 됩니다.

`local` 드라이버는 Laravel 애플리케이션이 동작하는 서버의 로컬 스토리지와 상호작용하며, `s3` 드라이버는 Amazon S3 클라우드 스토리지 서비스에 데이터를 저장하는 데 사용됩니다.

> {tip} 원하는 만큼 디스크를 구성할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크도 지정 가능합니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때, 모든 파일 작업은 `filesystems` 구성 파일의 `root` 디렉터리를 기준으로 수행됩니다. 기본적으로 이 값은 `storage/app` 디렉터리로 설정되어 있습니다. 따라서, 다음 방식으로 `storage/app/example.txt` 파일이 생성됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 구성 파일에 포함된 `public` 디스크는 외부에서 접근해야 하는 파일을 저장하기 위한 용도입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일을 `storage/app/public`에 저장합니다.

이 파일들을 웹에서 접근 가능하게 하려면, `public/storage`에서 `storage/app/public`로 심볼릭 링크를 생성해야 합니다. 이 디렉터리 구조를 따름으로써, [Envoyer](https://envoyer.io)와 같은 무중단 배포 시스템에서도 배포 시 퍼블릭 파일을 손쉽게 공유할 수 있습니다.

심볼릭 링크를 만들려면, `storage:link` Artisan 명령어를 실행하세요:

```
php artisan storage:link
```

파일 저장과 심볼릭 링크 생성 후에는, `asset` 헬퍼를 사용해 해당 파일의 URL을 생성할 수 있습니다:

```php
echo asset('storage/file.txt');
```

더 많은 심볼릭 링크가 필요하다면, `filesystems` 구성 파일에 추가할 수 있습니다. 구성된 각 링크는 `storage:link` 명령어 실행 시 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="composer-packages"></a>
#### Composer 패키지

S3 또는 SFTP 드라이버를 사용하기 전에 Composer 패키지 관리자를 통해 관련 패키지를 설치해야 합니다:

- Amazon S3: `composer require --with-all-dependencies league/flysystem-aws-s3-v3 "^1.0"`
- SFTP: `composer require league/flysystem-sftp "~1.0"`

성능 향상을 위해 캐시 어댑터를 선택적으로 설치할 수도 있습니다:

- CachedAdapter: `composer require league/flysystem-cached-adapter "~1.0"`

<a name="s3-driver-configuration"></a>
#### S3 드라이버 구성

S3 드라이버 설정 정보는 `config/filesystems.php` 구성 파일에 위치합니다. 이 파일에는 S3 드라이버용 예시 배열이 포함되어 있으며, 자신의 S3 설정 및 인증 정보로 자유롭게 수정하여 사용할 수 있습니다. 환경변수 이름은 AWS CLI와 동일하게 맞춰져 있어 편리합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 구성

Laravel의 Flysystem 통합은 FTP와도 잘 작동합니다. 하지만, 기본 `filesystems.php` 구성 파일에는 예시가 포함되어 있지 않습니다. FTP 파일 시스템을 설정하려면 다음 예시를 참고하세요:

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
#### SFTP 드라이버 구성

Laravel의 Flysystem 통합은 SFTP와도 잘 작동합니다. 기본 `filesystems.php` 구성 파일에 예시가 포함되어 있지 않으므로, 아래 예제를 참고하여 SFTP 파일 시스템을 설정할 수 있습니다:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),
    
    // 기본 인증을 위한 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // SSH 키와 암호를 이용한 인증 설정...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'password' => env('SFTP_PASSWORD'),

    // 선택적 SFTP 설정...
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT'),
    // 'timeout' => 30,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템

기본적으로 애플리케이션의 `filesystems` 구성 파일에는 `s3` 디스크 구성이 포함되어 있습니다. 이를 통해 Amazon S3 뿐만 아니라 [MinIO](https://github.com/minio/minio), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/) 등 S3 호환 저장 서비스와도 상호 연동이 가능합니다.

해당 서비스의 인증정보로 디스크 설정을 업데이트한 후에는 주로 `url` 구성 옵션 값만 수정하면 됩니다. 이 값은 대부분 `AWS_ENDPOINT` 환경변수로 정의합니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="caching"></a>
### 캐싱

특정 디스크에 대한 캐싱을 활성화하려면, 디스크 구성 옵션에 `cache` 지시어를 추가할 수 있습니다. `cache` 옵션은 캐시 스토어 이름(`store`), 만료 시간(`expire`, 초 단위), 캐시 접두사(`prefix`)를 포함한 배열입니다:

```php
's3' => [
    'driver' => 's3',

    // 기타 디스크 옵션...

    'cache' => [
        'store' => 'memcached',
        'expire' => 600,
        'prefix' => 'cache-prefix',
    ],
],
```

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 파사드를 사용하여 구성한 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 기본 디스크에 아바타를 저장하려면 `put` 메서드를 사용합니다. `Storage` 파사드에서 `disk` 메서드를 호출하지 않고 메서드를 호출하면, 해당 메서드는 자동으로 기본 디스크에 전달됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크를 사용할 때는 `Storage` 파사드의 `disk` 메서드로 특정 디스크를 선택하여 파일 작업을 할 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

실행 중에 특정 구성으로 디스크를 만들어야 할 때, 해당 설정이 `filesystems` 구성 파일에 존재하지 않더라도 `Storage` 파사드의 `build` 메서드에 구성 배열을 전달해 디스크를 생성할 수 있습니다:

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

`get` 메서드를 사용하여 파일의 내용을 가져올 수 있습니다. 이 메서드는 파일의 원시 문자열 데이터를 반환합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 지정해야 함을 기억하세요:

```php
$contents = Storage::get('file.jpg');
```

파일이 디스크에 존재하는지 확인하려면 `exists` 메서드를 사용합니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 파일이 디스크에서 존재하지 않는지 확인합니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 지정된 경로의 파일을 강제로 다운로드하도록 하는 응답을 생성합니다. 두 번째 인자로 파일명을 지정하면, 다운로드 시 사용자에게 표시되는 파일 이름을 지정할 수 있습니다. 세 번째 인자로 HTTP 헤더 배열도 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드를 사용하여 지정된 파일의 URL을 얻을 수 있습니다. `local` 드라이버 사용 시에는 기본적으로 `/storage` 경로가 붙은 상대 URL을 반환하고, `s3` 드라이버 사용 시에는 완전한 원격 URL이 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버를 사용할 경우, 외부에 공개해야 할 모든 파일은 반드시 `storage/app/public` 디렉터리에 위치해야 하며, 추가로 [심볼릭 링크를 생성](#the-public-disk)해야 합니다.

> {note} `local` 드라이버에서 `url`의 반환값은 URL 인코딩되지 않습니다. 따라서, 항상 유효한 URL이 될 수 있는 파일명을 사용하여 저장하는 것을 권장합니다.

<a name="temporary-urls"></a>
#### 임시 URL

`temporaryUrl` 메서드를 사용하면 `s3` 드라이버로 저장된 파일에 대해 유효기간이 있는 임시 URL을 생성할 수 있습니다. 이 메서드는 경로와 만료시각(`DateTime` 인스턴스)를 인자로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

추가 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, 세 번째 인자로 배열을 전달할 수 있습니다:

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

특정 디스크에 대해 임시 URL 생성 방식을 커스텀하고 싶다면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 임시 URL을 기본적으로 지원하지 않는 디스크에 대해 컨트롤러를 통해 다운로드하도록 할 때 유용합니다. 보통 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
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

`Storage` 파사드로 생성되는 URL의 호스트를 미리 정의하고 싶다면, 디스크 구성 배열에 `url` 옵션을 추가하세요:

```php
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
],
```

<a name="file-metadata"></a>
### 파일 메타데이터

파일의 읽기/쓰기뿐만 아니라 Laravel은 파일 자체에 대한 정보도 제공합니다. 예를 들어, `size` 메서드는 파일 크기(바이트)를 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 UNIX 타임스탬프를 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용하면 지정된 파일의 경로를 얻을 수 있습니다. `local` 드라이버 사용 시 절대 경로가, `s3` 드라이버 사용 시 S3 버킷 내의 상대 경로가 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 파일 내용을 디스크에 저장하는 데 사용할 수 있습니다. PHP의 `resource`를 `put` 메서드에 전달하면 Flysystem의 스트림을 사용할 수 있습니다. 모든 파일 경로는 해당 디스크의 "root" 설정을 기준으로 한다는 점을 기억하세요:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="automatic-streaming"></a>
#### 자동 스트리밍

스트리밍 방식으로 파일을 저장하면 메모리 사용량이 크게 줄어듭니다. 특정 파일을 저장 경로로 스트리밍하려면, `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 대상 위치로 자동으로 파일을 스트리밍합니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명에 고유 ID 자동 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명 수동 지정...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드와 관련하여 주의할 점이 있습니다. 위 예시에서는 디렉터리 이름만 지정했고, 파일명은 지정하지 않았습니다. 기본적으로 이 방법은 고유한 ID를 파일명으로 생성합니다. 파일 확장자는 MIME 타입을 검사하여 자동 결정됩니다. 이 메서드는 저장된 파일의 전체 경로(생성된 파일명 포함)를 반환하므로, 데이터베이스에 경로를 저장할 수 있습니다.

`putFile`과 `putFileAs` 메서드는 저장 파일의 "가시성" 인자를 받아, 생성되는 파일에 대한 공개 설정을 조정할 수 있습니다. Amazon S3 같은 클라우드 디스크에 저장하며 URL로 공개 접근을 이용하려면 유용합니다:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="prepending-appending-to-files"></a>
#### 파일 앞/뒤에 쓰기

`prepend`와 `append` 메서드를 이용해 파일의 맨 앞 또는 맨 뒤에 텍스트를 쓸 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
#### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 디스크 내 새로운 위치로 복사하며, `move` 메서드는 기존 파일을 새 위치로 이동 또는 이름을 변경할 수 있습니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 가장 많이 사용하는 파일 저장 예시는 사용자 업로드 파일(사진, 문서 등) 저장입니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드를 이용해 손쉽게 파일 저장이 가능합니다. 원하는 저장 경로와 함께 `store` 메서드를 호출하세요:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * 사용자의 아바타를 업데이트합니다.
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

이 예시에서도 디렉터리 이름만 지정했고 파일명은 지정하지 않았음을 알 수 있습니다. 기본적으로 `store` 메서드는 고유한 ID를 파일명으로 생성하며, 확장자는 MIME 타입으로 자동 판별됩니다. 반환 값은 저장된 파일의 전체 경로입니다.

`Storage` 파사드의 `putFile` 메서드를 호출해 동일한 저장 작업을 수행할 수도 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 지정

자동으로 파일명이 정해지는 것이 아닌, 원하는 파일명으로 저장하려면 `storeAs` 메서드를 사용하세요. 첫 번째는 경로, 두 번째는 파일명, 세 번째(선택)는 디스크명입니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드에 `putFileAs` 메서드를 사용해 같은 작업을 할 수도 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> {note} 인쇄 불가 문자 또는 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 파일 경로를 Laravel 파일 저장 메서드에 넘기기 전에 미리 정제하는 것을 권장합니다. 파일 경로는 `League\Flysystem\Util::normalizePath`로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

기본적으로 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크에 저장하려면 두 번째 인자로 디스크명을 넘기세요:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드 사용 시에는 세 번째 인자로 디스크명을 전달하면 됩니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 기타 업로드 파일 정보

업로드된 파일의 원래 이름이나 확장자가 필요하다면, `getClientOriginalName`과 `getClientOriginalExtension` 메서드를 사용하세요:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

그러나 이 메서드는 사용자가 악의적으로 파일명과 확장자를 변조할 수 있으므로 안전하지 않습니다. 대신, `hashName`과 `extension` 메서드를 사용하는 것이 좋습니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // 고유 무작위 이름 생성...
$extension = $file->extension(); // MIME 타입을 기반으로 확장자 반환...
```

<a name="file-visibility"></a>
### 파일 가시성

Laravel의 Flysystem 통합에서 "가시성"이란 다양한 플랫폼의 파일 권한을 추상화한 개념입니다. 파일은 보통 `public` 또는 `private`로 선언할 수 있습니다. `public`로 선언하면 다른 사용자가 접근할 수 있게 됨을 의미합니다. 예를 들어, S3 드라이버 사용 시 `public` 파일은 URL로 접근이 가능합니다.

`put` 메서드로 파일을 저장할 때 가시성을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 가시성은 `getVisibility`, `setVisibility` 메서드로 확인 및 변경할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드 파일을 다룰 때, `storePublicly`와 `storePubliclyAs`를 사용해 `public` 가시성으로 저장할 수도 있습니다:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일 & 가시성

`local` 드라이버 사용 시, `public` [가시성](#file-visibility)은 디렉터리에는 `0755`, 파일에는 `0644` 권한으로 매핑됩니다. 이 권한 맵핑 값은 `filesystems` 구성 파일에서 변경할 수 있습니다:

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
],
```

<a name="deleting-files"></a>
## 파일 삭제

`delete` 메서드는 하나의 파일명이나 파일명 배열을 받아 삭제를 수행합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하다면 파일이 삭제되어야 할 디스크를 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉터리

<a name="get-all-files-within-a-directory"></a>
#### 디렉터리 내 모든 파일 가져오기

`files` 메서드는 주어진 디렉터리의 모든 파일을 배열로 반환합니다. 하위 디렉터리까지 포함한 모든 파일 목록이 필요하다면 `allFiles` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉터리 내 모든 하위 디렉터리 가져오기

`directories` 메서드는 특정 디렉터리의 하위 디렉터리 목록을 배열로 반환합니다. 또한 `allDirectories` 메서드를 사용하면, 모든 하위 디렉터리와 재귀적으로 그 하위 디렉터리도 모두 가져올 수 있습니다:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉터리 생성

`makeDirectory` 메서드는 필요한 하위 디렉터리까지 포함하여 지정된 디렉터리를 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉터리 삭제

`deleteDirectory` 메서드는 지정한 디렉터리와 그 안의 모든 파일을 삭제합니다:

```php
Storage::deleteDirectory($directory);
```

<a name="custom-filesystems"></a>
## 커스텀 파일 시스템

Laravel의 Flysystem 통합은 다양한 "드라이버"를 기본으로 지원하지만, Flysystem은 그 외에도 여러 저장소에 사용할 수 있는 다양한 어댑터를 보유하고 있습니다. 추가 어댑터를 사용하려면 커스텀 드라이버를 직접 만들 수도 있습니다.

커스텀 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가한다고 가정해봅니다:

```
composer require spatie/flysystem-dropbox
```

다음으로, 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나의 `boot` 메서드에서 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\ServiceProvider;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        Storage::extend('dropbox', function ($app, $config) {
            $client = new DropboxClient(
                $config['authorization_token']
            );

            return new Filesystem(new DropboxAdapter($client));
        });
    }
}
```

`extend` 메서드의 첫 번째 인자는 드라이버 이름, 두 번째는 `$app`과 `$config`를 인자로 받는 클로저입니다. 클로저는 반드시 `League\Flysystem\Filesystem`의 인스턴스를 반환해야 합니다. `$config` 인자는 지정된 디스크에 대해 `config/filesystems.php`에 정의된 값을 담고 있습니다.

확장 서비스 프로바이더를 생성하고 등록했다면, 이제 `config/filesystems.php` 구성 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.