# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [로컬 드라이버](#the-local-driver)
    - [퍼블릭 디스크](#the-public-disk)
    - [드라이버 사전 조건](#driver-prerequisites)
    - [Amazon S3 호환 파일시스템](#amazon-s3-compatible-filesystems)
    - [캐싱](#caching)
- [디스크 인스턴스 가져오기](#obtaining-disk-instances)
    - [온디맨드 디스크](#on-demand-disks)
- [파일 조회하기](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [커스텀 파일시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개

Laravel은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 기반으로 강력한 파일시스템 추상화를 제공합니다. Laravel Flysystem 통합은 로컬 파일시스템, SFTP, Amazon S3와 작업할 수 있는 간단한 드라이버를 제공합니다. 더욱 좋은 점은 로컬 개발 환경과 프로덕션 서버 사이에 저장소 옵션을 손쉽게 전환할 수 있다는 점입니다. 각 시스템별 API가 동일하기 때문입니다.

<a name="configuration"></a>
## 설정

Laravel의 파일시스템 설정 파일은 `config/filesystems.php`에 위치합니다. 이 파일에서 모든 파일시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 저장 위치를 나타냅니다. 각 지원 드라이버에 대한 예제 설정이 포함되어 있어 필요에 맞게 저장소 설정 및 인증 정보를 수정할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버의 로컬 파일과 상호작용하며, `s3` 드라이버는 Amazon S3 클라우드 스토리지 서비스에 쓰기 위해 사용됩니다.

> [!TIP]
> 원하는 만큼 여러 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크도 가질 수 있습니다.

<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 경우 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉토리를 기준으로 이루어집니다. 기본값은 `storage/app` 디렉토리로 설정되어 있습니다. 따라서 다음 메서드는 `storage/app/example.txt`에 파일을 씁니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### 퍼블릭 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 웹에서 공개적으로 접근 가능한 파일을 위한 용도입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, `storage/app/public`에 파일을 저장합니다.

웹에서 이러한 파일에 접근하려면 `public/storage`에서 `storage/app/public`으로 심볼릭 링크를 만들어야 합니다. 이 폴더 구조를 사용하면 [Envoyer](https://envoyer.io)와 같은 무중단 배포 시스템에서 배포 시 같은 디렉토리를 공유하기 때문에 공개 접근 파일을 한 곳에 모아 관리하기 좋습니다.

심볼릭 링크를 생성하려면 `storage:link` Artisan 명령어를 실행하세요:

```
php artisan storage:link
```

파일이 저장되고 심볼릭 링크가 생성되면 `asset` 헬퍼로 파일 URL을 쉽게 생성할 수 있습니다:

```
echo asset('storage/file.txt');
```

`filesystems` 설정 파일에서 추가 심볼릭 링크를 구성할 수 있습니다. 설정된 모든 링크는 `storage:link` 명령어 실행 시 생성됩니다:

```
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 조건

<a name="composer-packages"></a>
#### 컴포저 패키지

S3 또는 SFTP 드라이버를 사용하기 전에 적절한 패키지를 Composer를 통해 설치해야 합니다:

- Amazon S3: `composer require --with-all-dependencies league/flysystem-aws-s3-v3 "^1.0"`
- SFTP: `composer require league/flysystem-sftp "~1.0"`

성능 향상을 위해 캐시 어댑터를 설치할 수도 있습니다:

- CachedAdapter: `composer require league/flysystem-cached-adapter "~1.0"`

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버 설정은 `config/filesystems.php` 설정 파일에 존재합니다. 이 파일은 S3 드라이버용 예제 설정 배열을 포함하고 있으며, 자신에게 맞게 S3 인증 정보와 환경 변수를 수정하여 사용할 수 있습니다. 환경 변수 이름은 AWS CLI의 명명 규칙과 일치해 편리합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

Laravel의 Flysystem 통합은 FTP와도 잘 작동하지만, 프레임워크 기본 `filesystems.php` 설정 파일에는 FTP 설정 예제가 포함되어 있지 않습니다. FTP 파일시스템 설정이 필요하다면 아래 예제를 참고하세요:

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

Laravel의 Flysystem 통합은 SFTP와도 잘 작동하지만, 기본 `filesystems.php` 설정 파일에 SFTP 예제 설정이 포함되어 있지 않습니다. SFTP 파일시스템 설정이 필요하다면 다음 예제를 참고하세요:

```
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),
    
    // 기본 인증 설정...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // 암호화 비밀번호가 있는 SSH 키 기반 인증 설정...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'password' => env('SFTP_PASSWORD'),

    // 선택적 SFTP 설정...
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT'),
    // 'timeout' => 30,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일시스템

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크 설정이 포함되어 있습니다. 이 디스크를 Amazon S3와 상호작용하는 것뿐만 아니라, [MinIO](https://github.com/minio/minio)나 [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/) 등 S3 호환 저장 서비스와도 사용할 수 있습니다.

일반적으로, 해당 서비스의 인증 정보에 맞게 디스크 자격증명을 업데이트한 후, `url` 설정값을 수정하는 것만으로 사용할 수 있습니다. 이 값은 보통 `AWS_ENDPOINT` 환경 변수를 통해 정의됩니다:

```
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="caching"></a>
### 캐싱

디스크에 캐싱을 활성화하려면 디스크 설정에 `cache` 지시자를 추가할 수 있습니다. `cache` 옵션은 캐시 저장소 이름(`store`), 만료 시간(초 단위, `expire`), 그리고 캐시 접두어(`prefix`)를 포함한 배열이어야 합니다:

```
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
## 디스크 인스턴스 가져오기

`Storage` 파사드를 사용하여 설정된 디스크와 상호작용할 수 있습니다. 예를 들면, 기본 디스크에 아바타를 저장할 때 `put` 메서드를 사용할 수 있습니다. `disk` 메서드를 먼저 호출하지 않고 `Storage` 파사드의 메서드를 호출하면 기본 디스크에 전달됩니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

여러 디스크를 사용하는 경우, 특정 디스크로 작업하려면 `Storage` 파사드의 `disk` 메서드를 사용합니다:

```
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### 온디맨드 디스크

때로는 애플리케이션 `filesystems` 설정 파일에 없는 디스크 구성을 런타임에 생성해 사용하고 싶을 수 있습니다. 이럴 때 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달하여 디스크를 생성할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## 파일 조회하기

`get` 메서드는 파일의 내용을 가져오는 데 사용됩니다. 파일의 원시 문자열 내용이 반환됩니다. 모든 파일 경로는 디스크의 "root" 위치에 대해 상대 경로로 지정해야 합니다:

```
$contents = Storage::get('file.jpg');
```

`exists` 메서드로 디스크에 파일이 존재하는지 확인할 수 있습니다:

```
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

`missing` 메서드는 파일이 없는 경우를 확인할 때 사용합니다:

```
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 해당 경로의 파일을 다운로드하도록 강제하는 응답을 생성합니다. 두 번째 인수로는 다운로드 시 사용자에게 표시할 파일명을 지정할 수 있습니다. 세 번째 인수로는 HTTP 헤더 배열을 전달할 수 있습니다:

```
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
### 파일 URL

`url` 메서드로 특정 파일의 URL을 얻을 수 있습니다. `local` 드라이버 사용 시 주로 `/storage`를 경로 앞에 붙인 상대 URL을 반환합니다. `s3` 드라이버 사용 시에는 완전한 원격 URL을 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

`local` 드라이버 사용 시, 공개 접근 가능한 파일은 `storage/app/public`에 위치해야 하며, `public/storage`에 [심볼릭 링크](#the-public-disk)를 생성해 두어야 합니다.

> [!NOTE]
> `local` 드라이버로 `url` 메서드를 사용할 때 반환값은 URL 인코딩 처리되어 있지 않습니다. 따라서 파일명에 URL에 유효한 문자만 사용하도록 해야 합니다.

<a name="temporary-urls"></a>
#### 임시 URL

`temporaryUrl` 메서드를 사용하면 `s3` 드라이버로 저장된 파일에 대해 임시 URL을 생성할 수 있습니다. 만료 시간을 나타내는 `DateTime` 인스턴스를 두 번째 인수로 받습니다:

```
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

추가 [S3 요청 파라미터](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 지정하려면 세 번째 인수로 배열을 전달할 수 있습니다:

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

특정 스토리지 디스크에서 임시 URL 생성 방식을 커스터마이즈해야 할 경우, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 보통 서비스 프로바이더의 `boot` 메서드에서 이 메서드를 호출합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
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

`Storage` 파사드로 URL 생성 시 미리 정해진 호스트가 필요하면, 디스크 설정 배열에 `url` 옵션을 추가할 수 있습니다:

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

파일을 읽고 쓰는 것 외에도 Laravel은 파일 자체에 대한 정보도 제공합니다. 예를 들어 `size` 메서드는 파일 크기를 바이트 단위로 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

`lastModified` 메서드는 파일이 마지막으로 수정된 시점을 UNIX 타임스탬프 형식으로 반환합니다:

```
$time = Storage::lastModified('file.jpg');
```

<a name="file-paths"></a>
#### 파일 경로

`path` 메서드를 사용하면 파일 경로를 얻을 수 있습니다. `local` 드라이버일 경우 절대 경로를, `s3` 드라이버일 경우 S3 버킷 내 상대 경로를 반환합니다:

```
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
## 파일 저장

`put` 메서드는 디스크에 파일 내용을 저장하는 데 사용합니다. PHP `resource`도 전달할 수 있어 Flysystem의 스트림 기능을 활용합니다. 모든 파일 경로는 디스크 설정의 "root" 위치에 대해 상대 경로여야 합니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="automatic-streaming"></a>
#### 자동 스트리밍

스토리지로 파일을 스트리밍하면 메모리 사용량이 크게 감소합니다. Laravel이 자동으로 파일 스트리밍을 처리하게 하려면 `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 지정한 위치로 파일을 스트리밍합니다:

```
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// 파일명에 대해 고유 ID를 자동 생성...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// 파일명을 지정하여 저장...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

`putFile` 메서드는 디렉터리명만 지정하고 파일명은 자동으로 고유 ID를 생성합니다. 파일 확장자는 MIME 타입에 따라 결정됩니다. 마침내 저장된 경로(생성된 파일명 포함)를 반환합니다.

`putFile`과 `putFileAs`에 "visibility"(가시성)를 지정하는 인수도 전달할 수 있습니다. 특히 Amazon S3 같은 클라우드 디스크에서 파일을 공개 접근 가능하게 설정할 때 유용합니다:

```
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="prepending-appending-to-files"></a>
#### 파일 앞/뒤에 내용 추가

`prepend`와 `append` 메서드를 이용해 파일의 앞이나 뒤에 데이터를 작성할 수 있습니다:

```
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
#### 파일 복사 및 이동

`copy` 메서드는 기존 파일을 새 경로로 복사하는 데 사용되며, `move` 메서드는 파일 이름 변경이나 새 경로로 이동하는 데 사용됩니다:

```
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="file-uploads"></a>
### 파일 업로드

웹 앱에서 파일 저장의 가장 흔한 용도 중 하나는 사용자 업로드 파일(사진, 문서 등)을 저장하는 것입니다. Laravel은 업로드된 파일 인스턴스의 `store` 메서드를 통해 손쉽게 저장할 수 있게 합니다. 해당 메서드에 저장할 경로를 전달하세요:

```
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

위 예제에서 디렉토리명만 지정하고 파일명은 지정하지 않았는데, 기본적으로 `store`는 고유 ID를 파일명으로 생성합니다. 확장자는 MIME 타입을 기준으로 결정됩니다. 저장된 파일의 전체 경로(생성된 파일명 포함)를 반환하므로 데이터베이스에 경로를 저장할 수 있습니다.

동일한 작업을 `Storage` 파사드의 `putFile` 메서드로도 수행할 수 있습니다:

```
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
#### 파일명 직접 지정하기

자동으로 파일명이 생성되는 것을 원하지 않으면 `storeAs` 메서드를 대상으로 대신 사용할 수 있습니다. 이 메서드는 저장할 경로, 파일명, (선택적으로) 디스크를 인수로 받습니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

`Storage` 파사드에서는 `putFileAs`가 같은 역할을 합니다:

```
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!NOTE]
> 출력 불가능하거나 유효하지 않은 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 Laravel 파일 저장 메서드에 전달하기 전 파일 경로를 정리하는 것을 권장합니다. 경로는 내부적으로 `League\Flysystem\Util::normalizePath` 메서드로 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 직접 지정하기

기본적으로 업로드 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 지정하려면 `store` 메서드의 두 번째 인수로 디스크 이름을 전달하세요:

```
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

`storeAs` 메서드 이용 시에는 디스크명을 세 번째 인수로 전달합니다:

```
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
#### 업로드된 파일 추가 정보

업로드된 파일의 원래 이름과 확장자를 가져오려면 `getClientOriginalName`과 `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

다만, 위 메서드는 사용자가 파일명과 확장자를 조작할 수 있어서 안전하지 않으므로, 일반적으로는 `hashName`과 `extension` 메서드를 사용하는 것이 더 안전합니다:

```
$file = $request->file('avatar');

$name = $file->hashName(); // 고유하고 임의의 이름 생성
$extension = $file->extension(); // MIME 타입 기반 확장자 결정
```

<a name="file-visibility"></a>
### 파일 가시성 (Visibility)

Laravel의 Flysystem 통합에서 "가시성"은 여러 플랫폼에 걸친 파일 권한 추상화입니다. 파일은 `public` 또는 `private`으로 선언할 수 있습니다. 파일이 `public`일 경우 일반적으로 다른 사용자도 접근할 수 있음을 의미합니다. 예를 들어 S3 드라이버 사용 시, `public` 파일에 대해 URL을 가져올 수 있습니다.

`put` 메서드로 파일을 쓸 때 가시성을 지정할 수 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

이미 저장된 파일의 가시성은 `getVisibility` 및 `setVisibility` 메서드로 확인하거나 변경할 수 있습니다:

```
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

업로드된 파일을 처리할 때는 `storePublicly`와 `storePubliclyAs` 메서드를 사용해 `public` 가시성을 지정하며 저장할 수 있습니다:

```
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
#### 로컬 파일 및 가시성

`local` 드라이버 사용 시 `public` [가시성](#file-visibility)은 디렉토리에 대해 `0755` 권한, 파일에 대해 `0644` 권한을 의미합니다. 애플리케이션의 `filesystems` 설정 파일에서 권한 매핑을 수정할 수 있습니다:

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

`delete` 메서드는 삭제할 파일명 하나 또는 여러 파일 배열을 인수로 받습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

필요하면 삭제 대상 디스크를 명시할 수도 있습니다:

```
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
## 디렉토리

<a name="get-all-files-within-a-directory"></a>
#### 디렉토리 내 모든 파일 가져오기

`files` 메서드는 지정한 디렉토리에 있는 모든 파일을 배열로 반환합니다. 하위 디렉토리를 포함해 모든 파일을 가져오려면 `allFiles` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
#### 디렉토리 내 모든 디렉토리 가져오기

`directories` 메서드는 지정한 디렉토리에 있는 하위 디렉토리 배열을 반환합니다. 하위 디렉토리를 포함해 모든 디렉토리를 가져오려면 `allDirectories` 메서드를 사용합니다:

```
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
#### 디렉토리 생성

`makeDirectory` 메서드는 필요한 하위 디렉토리를 포함하여 지정한 디렉토리를 생성합니다:

```
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
#### 디렉토리 삭제

`deleteDirectory` 메서드는 디렉토리와 그 안의 모든 파일을 삭제합니다:

```
Storage::deleteDirectory($directory);
```

<a name="custom-filesystems"></a>
## 커스텀 파일시스템

Laravel의 Flysystem 통합은 여러 "드라이버"를 기본 지원하지만, Flysystem은 더 많은 저장 시스템용 어댑터를 가지고 있습니다. 추가 어댑터를 사용하려면 커스텀 드라이버를 만들 수 있습니다.

커스텀 파일시스템 정의를 위해서는 Flysystem 어댑터가 필요합니다. 예를 들어 커뮤니티에서 관리하는 Dropbox 어댑터를 프로젝트에 추가해보겠습니다:

```
composer require spatie/flysystem-dropbox
```

이후, 애플리케이션의 [서비스 프로바이더](/docs/{{version}}/providers) 중 하나의 `boot` 메서드에서 `Storage` 파사드의 `extend` 메서드를 사용해 드라이버를 등록합니다:

```
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
     * 애플리케이션 서비스 부트스트래핑.
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

`extend` 메서드 첫 번째 인수는 드라이버 이름이며, 두 번째 인수는 `$app`과 `$config`를 전달받는 클로저입니다. 클로저는 `League\Flysystem\Filesystem` 인스턴스를 반환해야 합니다. `$config`는 `config/filesystems.php`에서 해당 디스크에 정의된 설정 값입니다.

커스텀 드라이버를 정의한 서비스 프로바이더를 등록한 후, `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.