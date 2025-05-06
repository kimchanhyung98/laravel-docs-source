# 계약(Contracts)

- [소개](#introduction)
    - [계약 vs 파사드](#contracts-vs-facades)
- [계약을 언제 사용해야 하는가](#when-to-use-contracts)
- [계약을 어떻게 사용하는가](#how-to-use-contracts)
- [계약 참고 문서](#contract-reference)

<a name="introduction"></a>
## 소개

라라벨의 "계약(Contracts)"은 프레임워크에서 제공하는 핵심 서비스를 정의하는 일련의 인터페이스입니다. 예를 들어, `Illuminate\Contracts\Queue\Queue` 계약은 작업을 큐잉하기 위해 필요한 메서드들을 정의하며, `Illuminate\Contracts\Mail\Mailer` 계약은 이메일을 전송하기 위해 필요한 메서드들을 정의합니다.

각 계약에는 프레임워크에서 제공되는 해당 구현체가 있습니다. 예를 들어, 라라벨은 다양한 드라이버로 구성된 큐 구현체와 [Symfony Mailer](https://symfony.com/doc/6.0/mailer.html) 기반의 메일러 구현체를 제공합니다.

모든 라라벨 계약은 [전용 GitHub 저장소](https://github.com/illuminate/contracts)에 위치합니다. 이를 통해 사용 가능한 모든 계약을 빠르게 참고할 수 있으며, 라라벨 서비스와 연동되는 패키지를 만들 때 독립적으로 사용할 수 있는 패키지로 활용할 수 있습니다.

<a name="contracts-vs-facades"></a>
### 계약 vs 파사드

라라벨의 [파사드](/docs/{{version}}/facades)와 헬퍼 함수는 서비스 컨테이너에서 계약을 타입힌트 하거나 직접 주입하지 않아도 라라벨의 서비스를 간단히 사용할 수 있는 방법입니다. 대부분의 경우 각 파사드에는 동등한 계약이 존재합니다.

파사드는 클래스의 생성자에 명시적으로 선언하지 않아도 되지만, 계약은 클래스의 명시적 의존성을 정의할 수 있습니다. 일부 개발자는 이처럼 의존성을 직접 선언하는 방식을 선호하여 계약을 사용하고, 다른 개발자는 파사드의 편리함을 선호합니다. **일반적으로, 대부분의 애플리케이션은 개발 중 파사드를 사용해도 문제되지 않습니다.**

<a name="when-to-use-contracts"></a>
## 계약을 언제 사용해야 하는가

계약과 파사드 중 무엇을 사용할지는 개인의 취향과 개발팀의 선호에 따라 다릅니다. 계약과 파사드 모두 견고하고 잘 테스트된 라라벨 애플리케이션을 만드는 데 사용할 수 있으며, 이 두 방법은 상호배타적이지 않습니다. 애플리케이션의 일부는 파사드를, 다른 부분은 계약에 의존할 수 있습니다. 클래스의 책임이 명확하게 분리되어 있다면, 계약과 파사드 중 무엇을 사용하든 실질적인 차이는 거의 없습니다.

일반적으로, 대부분의 애플리케이션은 개발 중에 파사드를 사용해도 무방합니다. 만약 여러 PHP 프레임워크와 통합되는 패키지를 개발하고 있다면, `illuminate/contracts` 패키지를 사용하여 라라벨 서비스와의 연동에 필요한 계약만을 의존성으로 걸고, 라라벨의 구체적 구현체를 패키지의 `composer.json`에 명시하지 않아도 됩니다.

<a name="how-to-use-contracts"></a>
## 계약을 어떻게 사용하는가

그렇다면, 계약의 구현체는 어떻게 받아올 수 있을까요? 매우 간단합니다.

라라벨의 다양한 클래스(컨트롤러, 이벤트 리스너, 미들웨어, 큐 작업, 라우트 클로저 등)는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석됩니다. 따라서, 계약의 구현체가 필요하다면, 해당 클래스의 생성자에서 인터페이스를 "타입힌트"하기만 하면 됩니다.

예를 들어, 다음의 이벤트 리스너 코드를 보세요.

```php
<?php

namespace App\Listeners;

use App\Events\OrderWasPlaced;
use App\Models\User;
use Illuminate\Contracts\Redis\Factory;

class CacheOrderInformation
{
    /**
     * Redis 팩토리 구현체.
     *
     * @var \Illuminate\Contracts\Redis\Factory
     */
    protected $redis;

    /**
     * 새로운 이벤트 핸들러 인스턴스를 생성합니다.
     *
     * @param  \Illuminate\Contracts\Redis\Factory  $redis
     * @return void
     */
    public function __construct(Factory $redis)
    {
        $this->redis = $redis;
    }

    /**
     * 이벤트를 처리합니다.
     *
     * @param  \App\Events\OrderWasPlaced  $event
     * @return void
     */
    public function handle(OrderWasPlaced $event)
    {
        //
    }
}
```

이벤트 리스너가 해석될 때, 서비스 컨테이너는 생성자의 타입힌트를 읽고 적절한 구현체를 자동으로 주입합니다. 서비스 컨테이너에 대해 더 자세히 알고 싶다면 [해당 문서](/docs/{{version}}/container)를 참고하세요.

<a name="contract-reference"></a>
## 계약 참고 문서

아래 표는 모든 라라벨 계약과 이에 대응하는 파사드의 간단한 참고 목록입니다.

| 계약(Contract)                                                                                                                                                  | 참조 파사드              |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|
| [Illuminate\Contracts\Auth\Access\Authorizable](https://github.com/illuminate/contracts/blob/{{version}}/Auth/Access/Authorizable.php)                        |  &nbsp;               |
| [Illuminate\Contracts\Auth\Access\Gate](https://github.com/illuminate/contracts/blob/{{version}}/Auth/Access/Gate.php)                                        | `Gate`                |
| [Illuminate\Contracts\Auth\Authenticatable](https://github.com/illuminate/contracts/blob/{{version}}/Auth/Authenticatable.php)                                |  &nbsp;               |
| [Illuminate\Contracts\Auth\CanResetPassword](https://github.com/illuminate/contracts/blob/{{version}}/Auth/CanResetPassword.php)                              | &nbsp;                |
| [Illuminate\Contracts\Auth\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Auth/Factory.php)                                                | `Auth`                |
| [Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/{{version}}/Auth/Guard.php)                                                    | `Auth::guard()`       |
| [Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/{{version}}/Auth/PasswordBroker.php)                                  | `Password::broker()`  |
| [Illuminate\Contracts\Auth\PasswordBrokerFactory](https://github.com/illuminate/contracts/blob/{{version}}/Auth/PasswordBrokerFactory.php)                    | `Password`            |
| [Illuminate\Contracts\Auth\StatefulGuard](https://github.com/illuminate/contracts/blob/{{version}}/Auth/StatefulGuard.php)                                    | &nbsp;                |
| [Illuminate\Contracts\Auth\SupportsBasicAuth](https://github.com/illuminate/contracts/blob/{{version}}/Auth/SupportsBasicAuth.php)                            | &nbsp;                |
| [Illuminate\Contracts\Auth\UserProvider](https://github.com/illuminate/contracts/blob/{{version}}/Auth/UserProvider.php)                                      | &nbsp;                |
| [Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/{{version}}/Bus/Dispatcher.php)                                            | `Bus`                 |
| [Illuminate\Contracts\Bus\QueueingDispatcher](https://github.com/illuminate/contracts/blob/{{version}}/Bus/QueueingDispatcher.php)                            | `Bus::dispatchToQueue()`|
| [Illuminate\Contracts\Broadcasting\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Broadcasting/Factory.php)                                | `Broadcast`           |
| [Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/{{version}}/Broadcasting/Broadcaster.php)                        | `Broadcast::connection()`|
| [Illuminate\Contracts\Broadcasting\ShouldBroadcast](https://github.com/illuminate/contracts/blob/{{version}}/Broadcasting/ShouldBroadcast.php)                | &nbsp;                |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcastNow](https://github.com/illuminate/contracts/blob/{{version}}/Broadcasting/ShouldBroadcastNow.php)          | &nbsp;                |
| [Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Cache/Factory.php)                                              | `Cache`               |
| [Illuminate\Contracts\Cache\Lock](https://github.com/illuminate/contracts/blob/{{version}}/Cache/Lock.php)                                                    | &nbsp;                |
| [Illuminate\Contracts\Cache\LockProvider](https://github.com/illuminate/contracts/blob/{{version}}/Cache/LockProvider.php)                                    | &nbsp;                |
| [Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/{{version}}/Cache/Repository.php)                                        | `Cache::driver()`     |
| [Illuminate\Contracts\Cache\Store](https://github.com/illuminate/contracts/blob/{{version}}/Cache/Store.php)                                                  | &nbsp;                |
| [Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/{{version}}/Config/Repository.php)                                      | `Config`              |
| [Illuminate\Contracts\Console\Application](https://github.com/illuminate/contracts/blob/{{version}}/Console/Application.php)                                  | &nbsp;                |
| [Illuminate\Contracts\Console\Kernel](https://github.com/illuminate/contracts/blob/{{version}}/Console/Kernel.php)                                            | `Artisan`             |
| [Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/{{version}}/Container/Container.php)                                  | `App`                 |
| [Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Cookie/Factory.php)                                            | `Cookie`              |
| [Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/{{version}}/Cookie/QueueingFactory.php)                            | `Cookie::queue()`     |
| [Illuminate\Contracts\Database\ModelIdentifier](https://github.com/illuminate/contracts/blob/{{version}}/Database/ModelIdentifier.php)                        | &nbsp;                |
| [Illuminate\Contracts\Debug\ExceptionHandler](https://github.com/illuminate/contracts/blob/{{version}}/Debug/ExceptionHandler.php)                            | &nbsp;                |
| [Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/{{version}}/Encryption/Encrypter.php)                                | `Crypt`               |
| [Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/{{version}}/Events/Dispatcher.php)                                      | `Event`               |
| [Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/{{version}}/Filesystem/Cloud.php)                                        | `Storage::cloud()`    |
| [Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Filesystem/Factory.php)                                    | `Storage`             |
| [Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/{{version}}/Filesystem/Filesystem.php)                              | `Storage::disk()`     |
| [Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/{{version}}/Foundation/Application.php)                            | `App`                 |
| [Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/{{version}}/Hashing/Hasher.php)                                            | `Hash`                |
| [Illuminate\Contracts\Http\Kernel](https://github.com/illuminate/contracts/blob/{{version}}/Http/Kernel.php)                                                  | &nbsp;                |
| [Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/{{version}}/Mail/MailQueue.php)                                            | `Mail::queue()`       |
| [Illuminate\Contracts\Mail\Mailable](https://github.com/illuminate/contracts/blob/{{version}}/Mail/Mailable.php)                                              | &nbsp;                |
| [Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/{{version}}/Mail/Mailer.php)                                                  | `Mail`                |
| [Illuminate\Contracts\Notifications\Dispatcher](https://github.com/illuminate/contracts/blob/{{version}}/Notifications/Dispatcher.php)                        | `Notification`        |
| [Illuminate\Contracts\Notifications\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Notifications/Factory.php)                              | `Notification`        |
| [Illuminate\Contracts\Pagination\LengthAwarePaginator](https://github.com/illuminate/contracts/blob/{{version}}/Pagination/LengthAwarePaginator.php)          | &nbsp;                |
| [Illuminate\Contracts\Pagination\Paginator](https://github.com/illuminate/contracts/blob/{{version}}/Pagination/Paginator.php)                                | &nbsp;                |
| [Illuminate\Contracts\Pipeline\Hub](https://github.com/illuminate/contracts/blob/{{version}}/Pipeline/Hub.php)                                                | &nbsp;                |
| [Illuminate\Contracts\Pipeline\Pipeline](https://github.com/illuminate/contracts/blob/{{version}}/Pipeline/Pipeline.php)                                      | &nbsp;                |
| [Illuminate\Contracts\Queue\EntityResolver](https://github.com/illuminate/contracts/blob/{{version}}/Queue/EntityResolver.php)                                | &nbsp;                |
| [Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Queue/Factory.php)                                              | `Queue`               |
| [Illuminate\Contracts\Queue\Job](https://github.com/illuminate/contracts/blob/{{version}}/Queue/Job.php)                                                      | &nbsp;                |
| [Illuminate\Contracts\Queue\Monitor](https://github.com/illuminate/contracts/blob/{{version}}/Queue/Monitor.php)                                              | `Queue`               |
| [Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/{{version}}/Queue/Queue.php)                                                  | `Queue::connection()` |
| [Illuminate\Contracts\Queue\QueueableCollection](https://github.com/illuminate/contracts/blob/{{version}}/Queue/QueueableCollection.php)                      | &nbsp;                |
| [Illuminate\Contracts\Queue\QueueableEntity](https://github.com/illuminate/contracts/blob/{{version}}/Queue/QueueableEntity.php)                              | &nbsp;                |
| [Illuminate\Contracts\Queue\ShouldQueue](https://github.com/illuminate/contracts/blob/{{version}}/Queue/ShouldQueue.php)                                      | &nbsp;                |
| [Illuminate\Contracts\Redis\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Redis/Factory.php)                                              | `Redis`               |
| [Illuminate\Contracts\Routing\BindingRegistrar](https://github.com/illuminate/contracts/blob/{{version}}/Routing/BindingRegistrar.php)                        | `Route`               |
| [Illuminate\Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/{{version}}/Routing/Registrar.php)                                      | `Route`               |
| [Illuminate\Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/{{version}}/Routing/ResponseFactory.php)                          | `Response`            |
| [Illuminate\Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/{{version}}/Routing/UrlGenerator.php)                                | `URL`                 |
| [Illuminate\Contracts\Routing\UrlRoutable](https://github.com/illuminate/contracts/blob/{{version}}/Routing/UrlRoutable.php)                                  | &nbsp;                |
| [Illuminate\Contracts\Session\Session](https://github.com/illuminate/contracts/blob/{{version}}/Session/Session.php)                                          | `Session::driver()`   |
| [Illuminate\Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Arrayable.php)                                      | &nbsp;                |
| [Illuminate\Contracts\Support\Htmlable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Htmlable.php)                                        | &nbsp;                |
| [Illuminate\Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Jsonable.php)                                        | &nbsp;                |
| [Illuminate\Contracts\Support\MessageBag](https://github.com/illuminate/contracts/blob/{{version}}/Support/MessageBag.php)                                    | &nbsp;                |
| [Illuminate\Contracts\Support\MessageProvider](https://github.com/illuminate/contracts/blob/{{version}}/Support/MessageProvider.php)                          | &nbsp;                |
| [Illuminate\Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Renderable.php)                                    | &nbsp;                |
| [Illuminate\Contracts\Support\Responsable](https://github.com/illuminate/contracts/blob/{{version}}/Support/Responsable.php)                                  | &nbsp;                |
| [Illuminate\Contracts\Translation\Loader](https://github.com/illuminate/contracts/blob/{{version}}/Translation/Loader.php)                                    | &nbsp;                |
| [Illuminate\Contracts\Translation\Translator](https://github.com/illuminate/contracts/blob/{{version}}/Translation/Translator.php)                            | `Lang`                |
| [Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/{{version}}/Validation/Factory.php)                                    | `Validator`           |
| [Illuminate\Contracts\Validation\ImplicitRule](https://github.com/illuminate/contracts/blob/{{version}}/Validation/ImplicitRule.php)                          | &nbsp;                |
| [Illuminate\Contracts\Validation\Rule](https://github.com/illuminate/contracts/blob/{{version}}/Validation/Rule.php)                                          | &nbsp;                |
| [Illuminate\Contracts\Validation\ValidatesWhenResolved](https://github.com/illuminate/contracts/blob/{{version}}/Validation/ValidatesWhenResolved.php)        | &nbsp;                |
| [Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/{{version}}/Validation/Validator.php)                                | `Validator::make()`   |
| [Illuminate\Contracts\View\Engine](https://github.com/illuminate/contracts/blob/{{version}}/View/Engine.php)                                                  | &nbsp;                |
| [Illuminate\Contracts\View\Factory](https://github.com/illuminate/contracts/blob/{{version}}/View/Factory.php)                                                | `View`                |
| [Illuminate\Contracts\View\View](https://github.com/illuminate/contracts/blob/{{version}}/View/View.php)                                                      | `View::make()`        |