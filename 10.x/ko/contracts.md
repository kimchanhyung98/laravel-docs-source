# Contracts

- [소개](#introduction)
    - [Contracts와 Facades의 차이](#contracts-vs-facades)
- [Contracts를 사용해야 할 때](#when-to-use-contracts)
- [Contracts를 사용하는 방법](#how-to-use-contracts)
- [Contract 참고 목록](#contract-reference)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 "contracts"는 프레임워크가 제공하는 핵심 서비스들을 정의하는 인터페이스 집합입니다. 예를 들어, `Illuminate\Contracts\Queue\Queue` contract는 작업을 큐잉하기 위해 필요한 메서드를 정의하며, `Illuminate\Contracts\Mail\Mailer` contract는 이메일 전송에 필요한 메서드를 정의합니다.

각 contract는 프레임워크에서 제공하는 구현체와 연동됩니다. 예를 들어, Laravel은 여러 드라이버를 갖춘 큐 구현체와 [Symfony Mailer](https://symfony.com/doc/6.0/mailer.html)를 기반으로 한 메일러 구현체를 제공합니다.

모든 Laravel contracts는 [전용 GitHub 저장소](https://github.com/illuminate/contracts)에 모여 있습니다. 이 저장소는 사용 가능한 모든 contracts를 빠르게 참조할 수 있는 지점이자, Laravel 서비스와 상호작용하는 패키지를 만들 때 활용할 수 있는 독립적인 패키지로 제공됩니다.

<a name="contracts-vs-facades"></a>
### Contracts와 Facades의 차이 (Contracts vs. Facades)

Laravel의 [facades](/docs/10.x/facades)와 헬퍼 함수는 contracts를 서비스 컨테이너에서 타입 힌트로 명시하고 해결할 필요 없이, Laravel 서비스를 간단히 사용할 수 있는 방법을 제공합니다. 대부분 경우, 각 facade는 대응하는 contract가 존재합니다.

facades와 달리 클래스 생성자에서 명시적으로 주입할 필요가 없는 반면, contracts는 클래스가 명확한 의존성을 가지도록 정의할 수 있습니다. 일부 개발자는 명시적 의존성 정의를 선호하여 contracts를 사용하고, 다른 개발자들은 facades의 편리함을 선호합니다. **일반적으로 대부분 애플리케이션은 개발 중에 facades를 사용하는 데 큰 문제가 없습니다.**

<a name="when-to-use-contracts"></a>
## Contracts를 사용해야 할 때 (When to Use Contracts)

contracts와 facades를 사용할지 여부는 본인과 개발 팀의 선호에 달려 있습니다. contracts와 facades 둘 다 견고하고 잘 테스트된 Laravel 애플리케이션을 만드는 데 사용할 수 있습니다. contracts와 facades는 상호 배타적이지 않으며, 애플리케이션의 일부는 facades를 사용하고 일부는 contracts에 의존해도 문제 없습니다. 중요한 것은 클래스가 수행할 책임을 명확히 유지하는 것입니다. 그렇게 하면 contracts와 facades 사용 간 실질적인 차이는 거의 없음을 알게 될 것입니다.

일반적으로, 대다수 애플리케이션은 개발 중에 facades를 문제 없이 사용할 수 있습니다. 만약 여러 PHP 프레임워크와 통합되는 패키지를 개발한다면, 패키지의 `composer.json`에서 Laravel의 구체적인 구현체를 요구하지 않고도 Laravel 서비스와 통합을 정의할 수 있는 `illuminate/contracts` 패키지를 사용하는 것이 좋습니다.

<a name="how-to-use-contracts"></a>
## Contracts를 사용하는 방법 (How to Use Contracts)

그렇다면 contract 구현체를 어떻게 얻을 수 있을까요? 사실 매우 간단합니다.

Laravel에서 컨트롤러, 이벤트 리스너, 미들웨어, 큐 작업, 라우트 클로저 등 다양한 유형의 클래스는 [서비스 컨테이너](/docs/10.x/container)를 통해 해결됩니다. 따라서 contract 구현체를 얻으려면, 해결되는 클래스의 생성자에서 해당 인터페이스를 타입 힌트로 명시하면 됩니다.

예로, 아래 이벤트 리스너 코드를 보세요:

```
<?php

namespace App\Listeners;

use App\Events\OrderWasPlaced;
use App\Models\User;
use Illuminate\Contracts\Redis\Factory;

class CacheOrderInformation
{
    /**
     * Create a new event handler instance.
     */
    public function __construct(
        protected Factory $redis,
    ) {}

    /**
     * Handle the event.
     */
    public function handle(OrderWasPlaced $event): void
    {
        // ...
    }
}
```

이벤트 리스너가 해결될 때 서비스 컨테이너는 클래스 생성자의 타입 힌트를 읽어 해당 타입에 맞는 적절한 값을 주입합니다. 서비스 컨테이너에 대해 더 알고 싶으면 [공식 문서](/docs/10.x/container)를 참조하세요.

<a name="contract-reference"></a>
## Contract 참고 목록 (Contract Reference)

아래 표는 Laravel의 모든 contracts와 그에 대응하는 facades를 빠르게 참고할 수 있도록 정리한 것입니다:

| Contract                                                                                                                                               | 참조하는 Facade            |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| [Illuminate\Contracts\Auth\Access\Authorizable](https://github.com/illuminate/contracts/blob/10.x/Auth/Access/Authorizable.php)                 |  &nbsp;                   |
| [Illuminate\Contracts\Auth\Access\Gate](https://github.com/illuminate/contracts/blob/10.x/Auth/Access/Gate.php)                                 | `Gate`                    |
| [Illuminate\Contracts\Auth\Authenticatable](https://github.com/illuminate/contracts/blob/10.x/Auth/Authenticatable.php)                         |  &nbsp;                   |
| [Illuminate\Contracts\Auth\CanResetPassword](https://github.com/illuminate/contracts/blob/10.x/Auth/CanResetPassword.php)                       | &nbsp;                    |
| [Illuminate\Contracts\Auth\Factory](https://github.com/illuminate/contracts/blob/10.x/Auth/Factory.php)                                         | `Auth`                    |
| [Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/10.x/Auth/Guard.php)                                             | `Auth::guard()`           |
| [Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/10.x/Auth/PasswordBroker.php)                           | `Password::broker()`      |
| [Illuminate\Contracts\Auth\PasswordBrokerFactory](https://github.com/illuminate/contracts/blob/10.x/Auth/PasswordBrokerFactory.php)             | `Password`                |
| [Illuminate\Contracts\Auth\StatefulGuard](https://github.com/illuminate/contracts/blob/10.x/Auth/StatefulGuard.php)                             | &nbsp;                    |
| [Illuminate\Contracts\Auth\SupportsBasicAuth](https://github.com/illuminate/contracts/blob/10.x/Auth/SupportsBasicAuth.php)                     | &nbsp;                    |
| [Illuminate\Contracts\Auth\UserProvider](https://github.com/illuminate/contracts/blob/10.x/Auth/UserProvider.php)                               | &nbsp;                    |
| [Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/10.x/Bus/Dispatcher.php)                                     | `Bus`                     |
| [Illuminate\Contracts\Bus\QueueingDispatcher](https://github.com/illuminate/contracts/blob/10.x/Bus/QueueingDispatcher.php)                     | `Bus::dispatchToQueue()`  |
| [Illuminate\Contracts\Broadcasting\Factory](https://github.com/illuminate/contracts/blob/10.x/Broadcasting/Factory.php)                         | `Broadcast`               |
| [Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/10.x/Broadcasting/Broadcaster.php)                 | `Broadcast::connection()` |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcast](https://github.com/illuminate/contracts/blob/10.x/Broadcasting/ShouldBroadcast.php)         | &nbsp;                    |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcastNow](https://github.com/illuminate/contracts/blob/10.x/Broadcasting/ShouldBroadcastNow.php)   | &nbsp;                    |
| [Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/10.x/Cache/Factory.php)                                       | `Cache`                   |
| [Illuminate\Contracts\Cache\Lock](https://github.com/illuminate/contracts/blob/10.x/Cache/Lock.php)                                             | &nbsp;                    |
| [Illuminate\Contracts\Cache\LockProvider](https://github.com/illuminate/contracts/blob/10.x/Cache/LockProvider.php)                             | &nbsp;                    |
| [Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/10.x/Cache/Repository.php)                                 | `Cache::driver()`         |
| [Illuminate\Contracts\Cache\Store](https://github.com/illuminate/contracts/blob/10.x/Cache/Store.php)                                           | &nbsp;                    |
| [Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/10.x/Config/Repository.php)                               | `Config`                  |
| [Illuminate\Contracts\Console\Application](https://github.com/illuminate/contracts/blob/10.x/Console/Application.php)                           | &nbsp;                    |
| [Illuminate\Contracts\Console\Kernel](https://github.com/illuminate/contracts/blob/10.x/Console/Kernel.php)                                     | `Artisan`                 |
| [Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/10.x/Container/Container.php)                           | `App`                     |
| [Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/10.x/Cookie/Factory.php)                                     | `Cookie`                  |
| [Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/10.x/Cookie/QueueingFactory.php)                     | `Cookie::queue()`         |
| [Illuminate\Contracts\Database\ModelIdentifier](https://github.com/illuminate/contracts/blob/10.x/Database/ModelIdentifier.php)                 | &nbsp;                    |
| [Illuminate\Contracts\Debug\ExceptionHandler](https://github.com/illuminate/contracts/blob/10.x/Debug/ExceptionHandler.php)                     | &nbsp;                    |
| [Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/10.x/Encryption/Encrypter.php)                         | `Crypt`                   |
| [Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/10.x/Events/Dispatcher.php)                               | `Event`                   |
| [Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/10.x/Filesystem/Cloud.php)                                 | `Storage::cloud()`        |
| [Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/10.x/Filesystem/Factory.php)                             | `Storage`                 |
| [Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/10.x/Filesystem/Filesystem.php)                       | `Storage::disk()`         |
| [Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/10.x/Foundation/Application.php)                     | `App`                     |
| [Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/10.x/Hashing/Hasher.php)                                     | `Hash`                    |
| [Illuminate\Contracts\Http\Kernel](https://github.com/illuminate/contracts/blob/10.x/Http/Kernel.php)                                           | &nbsp;                    |
| [Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/10.x/Mail/MailQueue.php)                                     | `Mail::queue()`           |
| [Illuminate\Contracts\Mail\Mailable](https://github.com/illuminate/contracts/blob/10.x/Mail/Mailable.php)                                       | &nbsp;                    |
| [Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/10.x/Mail/Mailer.php)                                           | `Mail`                    |
| [Illuminate\Contracts\Notifications\Dispatcher](https://github.com/illuminate/contracts/blob/10.x/Notifications/Dispatcher.php)                 | `Notification`            |
| [Illuminate\Contracts\Notifications\Factory](https://github.com/illuminate/contracts/blob/10.x/Notifications/Factory.php)                       | `Notification`            |
| [Illuminate\Contracts\Pagination\LengthAwarePaginator](https://github.com/illuminate/contracts/blob/10.x/Pagination/LengthAwarePaginator.php)   | &nbsp;                    |
| [Illuminate\Contracts\Pagination\Paginator](https://github.com/illuminate/contracts/blob/10.x/Pagination/Paginator.php)                         | &nbsp;                    |
| [Illuminate\Contracts\Pipeline\Hub](https://github.com/illuminate/contracts/blob/10.x/Pipeline/Hub.php)                                         | &nbsp;                    |
| [Illuminate\Contracts\Pipeline\Pipeline](https://github.com/illuminate/contracts/blob/10.x/Pipeline/Pipeline.php)                               | `Pipeline`                 |
| [Illuminate\Contracts\Queue\EntityResolver](https://github.com/illuminate/contracts/blob/10.x/Queue/EntityResolver.php)                         | &nbsp;                    |
| [Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/10.x/Queue/Factory.php)                                       | `Queue`                   |
| [Illuminate\Contracts\Queue\Job](https://github.com/illuminate/contracts/blob/10.x/Queue/Job.php)                                               | &nbsp;                    |
| [Illuminate\Contracts\Queue\Monitor](https://github.com/illuminate/contracts/blob/10.x/Queue/Monitor.php)                                       | `Queue`                   |
| [Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/10.x/Queue/Queue.php)                                           | `Queue::connection()`     |
| [Illuminate\Contracts\Queue\QueueableCollection](https://github.com/illuminate/contracts/blob/10.x/Queue/QueueableCollection.php)               | &nbsp;                    |
| [Illuminate\Contracts\Queue\QueueableEntity](https://github.com/illuminate/contracts/blob/10.x/Queue/QueueableEntity.php)                       | &nbsp;                    |
| [Illuminate\Contracts\Queue\ShouldQueue](https://github.com/illuminate/contracts/blob/10.x/Queue/ShouldQueue.php)                               | &nbsp;                    |
| [Illuminate\Contracts\Redis\Factory](https://github.com/illuminate/contracts/blob/10.x/Redis/Factory.php)                                       | `Redis`                   |
| [Illuminate.Contracts\Routing\BindingRegistrar](https://github.com/illuminate/contracts/blob/10.x/Routing/BindingRegistrar.php)                 | `Route`                   |
| [Illuminate.Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/10.x/Routing/Registrar.php)                               | `Route`                   |
| [Illuminate.Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/10.x/Routing/ResponseFactory.php)                   | `Response`                |
| [Illuminate.Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/10.x/Routing/UrlGenerator.php)                         | `URL`                     |
| [Illuminate.Contracts\Routing\UrlRoutable](https://github.com/illuminate/contracts/blob/10.x/Routing/UrlRoutable.php)                           | &nbsp;                    |
| [Illuminate.Contracts.Session\Session](https://github.com/illuminate/contracts/blob/10.x/Session/Session.php)                                   | `Session::driver()`       |
| [Illuminate.Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/10.x/Support/Arrayable.php)                               | &nbsp;                    |
| [Illuminate.Contracts\Support\Htmlable](https://github.com/illuminate/contracts/blob/10.x/Support/Htmlable.php)                                 | &nbsp;                    |
| [Illuminate.Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/10.x/Support/Jsonable.php)                                 | &nbsp;                    |
| [Illuminate.Contracts\Support\MessageBag](https://github.com/illuminate/contracts/blob/10.x/Support/MessageBag.php)                             | &nbsp;                    |
| [Illuminate.Contracts\Support.MessageProvider](https://github.com/illuminate/contracts/blob/10.x/Support/MessageProvider.php)                   | &nbsp;                    |
| [Illuminate.Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/10.x/Support/Renderable.php)                             | &nbsp;                    |
| [Illuminate.Contracts\Support\Responsable](https://github.com/illuminate/contracts/blob/10.x/Support/Responsable.php)                           | &nbsp;                    |
| [Illuminate.Contracts\Translation\Loader](https://github.com/illuminate/contracts/blob/10.x/Translation/Loader.php)                             | &nbsp;                    |
| [Illuminate.Contracts\Translation\Translator](https://github.com/illuminate/contracts/blob/10.x/Translation/Translator.php)                     | `Lang`                    |
| [Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/10.x/Validation/Factory.php)                             | `Validator`               |
| [Illuminate\Contracts\Validation\ImplicitRule](https://github.com/illuminate/contracts/blob/10.x/Validation/ImplicitRule.php)                   | &nbsp;                    |
| [Illuminate\Contracts\Validation\Rule](https://github.com/illuminate/contracts/blob/10.x/Validation/Rule.php)                                   | &nbsp;                    |
| [Illuminate.Contracts\Validation\ValidatesWhenResolved](https://github.com/illuminate/contracts/blob/10.x/Validation/ValidatesWhenResolved.php) | &nbsp;                    |
| [Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/10.x/Validation/Validator.php)                         | `Validator::make()`       |
| [Illuminate.Contracts.View.Engine](https://github.com/illuminate/contracts/blob/10.x/View/Engine.php)                                           | &nbsp;                    |
| [Illuminate.Contracts.View.Factory](https://github.com/illuminate/contracts/blob/10.x/View/Factory.php)                                         | `View`                    |
| [Illuminate.Contracts.View.View](https://github.com/illuminate/contracts/blob/10.x/View/View.php)                                               | `View::make()`            |