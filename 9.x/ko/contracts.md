# Contracts (컨트랙트)

- [소개](#introduction)
    - [컨트랙트와 파사드의 차이](#contracts-vs-facades)
- [컨트랙트를 사용해야 할 때](#when-to-use-contracts)
- [컨트랙트 사용법](#how-to-use-contracts)
- [컨트랙트 참조](#contract-reference)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 "컨트랙트"는 프레임워크가 제공하는 핵심 서비스들을 정의하는 인터페이스들의 집합입니다. 예를 들어, `Illuminate\Contracts\Queue\Queue` 컨트랙트는 작업 큐잉에 필요한 메서드들을 정의하고, `Illuminate\Contracts\Mail\Mailer` 컨트랙트는 이메일 전송에 필요한 메서드들을 정의합니다.

각 컨트랙트에는 프레임워크가 제공하는 구체적인 구현체가 존재합니다. 예를 들어, Laravel은 다양한 드라이버를 지원하는 큐 구현체와 [Symfony Mailer](https://symfony.com/doc/6.0/mailer.html)를 기반으로 한 메일러 구현체를 제공합니다.

모든 Laravel 컨트랙트는 [별도의 GitHub 저장소](https://github.com/illuminate/contracts)에 존재합니다. 이는 사용 가능한 모든 컨트랙트를 빠르게 참조할 수 있도록 해주며, Laravel 서비스와 상호작용하는 패키지를 만들 때 별도로 의존할 수 있는 독립적인 패키지를 제공합니다.

<a name="contracts-vs-facades"></a>
### 컨트랙트와 파사드의 차이 (Contracts Vs. Facades)

Laravel의 [파사드](/docs/9.x/facades)와 헬퍼 함수는 컨테이너에서 컨트랙트를 타입힌트하거나 해결할 필요 없이 Laravel 서비스를 쉽게 사용할 수 있는 방법을 제공합니다. 대부분의 경우, 각 파사드에는 대응하는 컨트랙트가 있습니다.

파사드는 클래스 생성자에서 명시적으로 요구하지 않아도 되지만, 컨트랙트는 클래스의 명시적인 의존성을 정의할 수 있게 해줍니다. 일부 개발자들은 이런 방식으로 의존성을 명확히 정의하는 것을 선호하며 이 때문에 컨트랙트를 선호하는 반면, 다른 개발자들은 파사드의 간편함을 더 좋아합니다. **대부분의 애플리케이션은 개발 중에는 파사드를 사용하는 데 문제가 없습니다.**

<a name="when-to-use-contracts"></a>
## 컨트랙트를 사용해야 할 때 (When To Use Contracts)

컨트랙트와 파사드 중 무엇을 사용할지는 개인 취향과 팀의 선호도에 따라 결정됩니다. 컨트랙트와 파사드 모두 강력하고 잘 테스트된 Laravel 애플리케이션을 만드는 데 사용할 수 있습니다. 이 둘은 상호 배타적이지 않습니다. 애플리케이션의 일부는 파사드를 사용하고, 일부는 컨트랙트를 사용할 수 있습니다. 클래스가 자신의 책임에 집중하고 있다면 컨트랙트와 파사드 사용 간에 실제 차이를 거의 느끼지 못할 것입니다.

일반적으로, 대부분의 애플리케이션은 개발 과정에서 문제 없이 파사드를 사용할 수 있습니다. 만약 여러 PHP 프레임워크와 통합하는 패키지를 개발하는 경우, 패키지의 `composer.json` 파일에 Laravel의 구체 구현체를 명시하지 않고도 Laravel 서비스와의 통합을 정의하려면 `illuminate/contracts` 패키지를 사용하는 것이 좋습니다.

<a name="how-to-use-contracts"></a>
## 컨트랙트 사용법 (How To Use Contracts)

그러면, 컨트랙트의 구현체를 어떻게 얻을 수 있을까요? 사실 아주 간단합니다.

Laravel에서 컨트롤러, 이벤트 리스너, 미들웨어, 큐 작업, 라우트 클로저 등 많은 종류의 클래스는 [서비스 컨테이너](/docs/9.x/container)를 통해 해결됩니다. 따라서, 컨트랙트의 구현체를 얻으려면 해당 클래스를 생성할 때 생성자에서 인터페이스를 타입힌트하면 됩니다.

예를 들어, 다음 이벤트 리스너를 살펴보세요:

```
<?php

namespace App\Listeners;

use App\Events\OrderWasPlaced;
use App\Models\User;
use Illuminate\Contracts\Redis\Factory;

class CacheOrderInformation
{
    /**
     * The Redis factory implementation.
     *
     * @var \Illuminate\Contracts\Redis\Factory
     */
    protected $redis;

    /**
     * Create a new event handler instance.
     *
     * @param  \Illuminate\Contracts\Redis\Factory  $redis
     * @return void
     */
    public function __construct(Factory $redis)
    {
        $this->redis = $redis;
    }

    /**
     * Handle the event.
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

이벤트 리스너가 해결될 때, 서비스 컨테이너가 클래스 생성자의 타입힌트를 읽어 적절한 값을 주입합니다. 서비스 컨테이너에 객체를 등록하는 방법에 대해 더 알고 싶으면 [공식 문서](https://laravel.kr/docs/9.x/container)를 참고하세요.

<a name="contract-reference"></a>
## 컨트랙트 참조 (Contract Reference)

다음 표는 Laravel의 모든 컨트랙트와 대응하는 파사드를 빠르게 참조할 수 있게 정리한 것입니다:

| 컨트랙트                                                                                                                                               | 대응 파사드               |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| [Illuminate\Contracts\Auth\Access\Authorizable](https://github.com/illuminate/contracts/blob/9.x/Auth/Access/Authorizable.php)                         |  &nbsp;                   |
| [Illuminate\Contracts\Auth\Access\Gate](https://github.com/illuminate/contracts/blob/9.x/Auth/Access/Gate.php)                                         | `Gate`                    |
| [Illuminate\Contracts\Auth\Authenticatable](https://github.com/illuminate/contracts/blob/9.x/Auth/Authenticatable.php)                               |  &nbsp;                   |
| [Illuminate\Contracts\Auth\CanResetPassword](https://github.com/illuminate/contracts/blob/9.x/Auth/CanResetPassword.php)                             | &nbsp;                    |
| [Illuminate\Contracts\Auth\Factory](https://github.com/illuminate/contracts/blob/9.x/Auth/Factory.php)                                                 | `Auth`                    |
| [Illuminate\Contracts\Auth\Guard](https://github.com/illuminate/contracts/blob/9.x/Auth/Guard.php)                                                     | `Auth::guard()`           |
| [Illuminate\Contracts\Auth\PasswordBroker](https://github.com/illuminate/contracts/blob/9.x/Auth/PasswordBroker.php)                                 | `Password::broker()`      |
| [Illuminate\Contracts\Auth\PasswordBrokerFactory](https://github.com/illuminate/contracts/blob/9.x/Auth/PasswordBrokerFactory.php)                   | `Password`                |
| [Illuminate\Contracts\Auth\StatefulGuard](https://github.com/illuminate/contracts/blob/9.x/Auth/StatefulGuard.php)                                   | &nbsp;                    |
| [Illuminate\Contracts\Auth\SupportsBasicAuth](https://github.com/illuminate/contracts/blob/9.x/Auth/SupportsBasicAuth.php)                           | &nbsp;                    |
| [Illuminate\Contracts\Auth\UserProvider](https://github.com/illuminate/contracts/blob/9.x/Auth/UserProvider.php)                                       | &nbsp;                    |
| [Illuminate\Contracts\Bus\Dispatcher](https://github.com/illuminate/contracts/blob/9.x/Bus/Dispatcher.php)                                             | `Bus`                     |
| [Illuminate\Contracts\Bus\QueueingDispatcher](https://github.com/illuminate/contracts/blob/9.x/Bus/QueueingDispatcher.php)                           | `Bus::dispatchToQueue()`  |
| [Illuminate\Contracts\Broadcasting\Factory](https://github.com/illuminate/contracts/blob/9.x/Broadcasting/Factory.php)                                 | `Broadcast`               |
| [Illuminate\Contracts\Broadcasting\Broadcaster](https://github.com/illuminate/contracts/blob/9.x/Broadcasting/Broadcaster.php)                       | `Broadcast::connection()` |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcast](https://github.com/illuminate/contracts/blob/9.x/Broadcasting/ShouldBroadcast.php)               | &nbsp;                    |
| [Illuminate\Contracts\Broadcasting\ShouldBroadcastNow](https://github.com/illuminate/contracts/blob/9.x/Broadcasting/ShouldBroadcastNow.php)         | &nbsp;                    |
| [Illuminate\Contracts\Cache\Factory](https://github.com/illuminate/contracts/blob/9.x/Cache/Factory.php)                                               | `Cache`                   |
| [Illuminate\Contracts\Cache\Lock](https://github.com/illuminate/contracts/blob/9.x/Cache/Lock.php)                                                     | &nbsp;                    |
| [Illuminate\Contracts\Cache\LockProvider](https://github.com/illuminate/contracts/blob/9.x/Cache/LockProvider.php)                                     | &nbsp;                    |
| [Illuminate\Contracts\Cache\Repository](https://github.com/illuminate/contracts/blob/9.x/Cache/Repository.php)                                         | `Cache::driver()`         |
| [Illuminate\Contracts\Cache\Store](https://github.com/illuminate/contracts/blob/9.x/Cache/Store.php)                                                   | &nbsp;                    |
| [Illuminate\Contracts\Config\Repository](https://github.com/illuminate/contracts/blob/9.x/Config/Repository.php)                                       | `Config`                  |
| [Illuminate\Contracts\Console\Application](https://github.com/illuminate/contracts/blob/9.x/Console/Application.php)                                 | &nbsp;                    |
| [Illuminate\Contracts\Console\Kernel](https://github.com/illuminate/contracts/blob/9.x/Console/Kernel.php)                                           | `Artisan`                 |
| [Illuminate\Contracts\Container\Container](https://github.com/illuminate/contracts/blob/9.x/Container/Container.php)                                 | `App`                     |
| [Illuminate\Contracts\Cookie\Factory](https://github.com/illuminate/contracts/blob/9.x/Cookie/Factory.php)                                             | `Cookie`                  |
| [Illuminate\Contracts\Cookie\QueueingFactory](https://github.com/illuminate/contracts/blob/9.x/Cookie/QueueingFactory.php)                           | `Cookie::queue()`         |
| [Illuminate\Contracts\Database\ModelIdentifier](https://github.com/illuminate/contracts/blob/9.x/Database/ModelIdentifier.php)                       | &nbsp;                    |
| [Illuminate\Contracts\Debug\ExceptionHandler](https://github.com/illuminate/contracts/blob/9.x/Debug/ExceptionHandler.php)                           | &nbsp;                    |
| [Illuminate\Contracts\Encryption\Encrypter](https://github.com/illuminate/contracts/blob/9.x/Encryption/Encrypter.php)                               | `Crypt`                   |
| [Illuminate\Contracts\Events\Dispatcher](https://github.com/illuminate/contracts/blob/9.x/Events/Dispatcher.php)                                     | `Event`                   |
| [Illuminate\Contracts\Filesystem\Cloud](https://github.com/illuminate/contracts/blob/9.x/Filesystem/Cloud.php)                                         | `Storage::cloud()`        |
| [Illuminate\Contracts\Filesystem\Factory](https://github.com/illuminate/contracts/blob/9.x/Filesystem/Factory.php)                                   | `Storage`                 |
| [Illuminate\Contracts\Filesystem\Filesystem](https://github.com/illuminate/contracts/blob/9.x/Filesystem/Filesystem.php)                             | `Storage::disk()`         |
| [Illuminate\Contracts\Foundation\Application](https://github.com/illuminate/contracts/blob/9.x/Foundation/Application.php)                           | `App`                     |
| [Illuminate\Contracts\Hashing\Hasher](https://github.com/illuminate/contracts/blob/9.x/Hashing/Hasher.php)                                           | `Hash`                    |
| [Illuminate\Contracts\Http\Kernel](https://github.com/illuminate/contracts/blob/9.x/Http/Kernel.php)                                                 | &nbsp;                    |
| [Illuminate\Contracts\Mail\MailQueue](https://github.com/illuminate/contracts/blob/9.x/Mail/MailQueue.php)                                           | `Mail::queue()`           |
| [Illuminate\Contracts\Mail\Mailable](https://github.com/illuminate/contracts/blob/9.x/Mail/Mailable.php)                                             | &nbsp;                    |
| [Illuminate\Contracts\Mail\Mailer](https://github.com/illuminate/contracts/blob/9.x/Mail/Mailer.php)                                                 | `Mail`                    |
| [Illuminate\Contracts\Notifications\Dispatcher](https://github.com/illuminate/contracts/blob/9.x/Notifications/Dispatcher.php)                       | `Notification`            |
| [Illuminate\Contracts\Notifications\Factory](https://github.com/illuminate/contracts/blob/9.x/Notifications/Factory.php)                           | `Notification`            |
| [Illuminate\Contracts\Pagination\LengthAwarePaginator](https://github.com/illuminate/contracts/blob/9.x/Pagination/LengthAwarePaginator.php)         | &nbsp;                    |
| [Illuminate\Contracts\Pagination\Paginator](https://github.com/illuminate/contracts/blob/9.x/Pagination/Paginator.php)                             | &nbsp;                    |
| [Illuminate\Contracts\Pipeline\Hub](https://github.com/illuminate/contracts/blob/9.x/Pipeline/Hub.php)                                               | &nbsp;                    |
| [Illuminate\Contracts\Pipeline\Pipeline](https://github.com/illuminate/contracts/blob/9.x/Pipeline/Pipeline.php)                                   | &nbsp;                    |
| [Illuminate\Contracts\Queue\EntityResolver](https://github.com/illuminate/contracts/blob/9.x/Queue/EntityResolver.php)                             | &nbsp;                    |
| [Illuminate\Contracts\Queue\Factory](https://github.com/illuminate/contracts/blob/9.x/Queue/Factory.php)                                           | `Queue`                   |
| [Illuminate\Contracts\Queue\Job](https://github.com/illuminate/contracts/blob/9.x/Queue/Job.php)                                                     | &nbsp;                    |
| [Illuminate\Contracts\Queue\Monitor](https://github.com/illuminate/contracts/blob/9.x/Queue/Monitor.php)                                           | `Queue`                   |
| [Illuminate\Contracts\Queue\Queue](https://github.com/illuminate/contracts/blob/9.x/Queue/Queue.php)                                               | `Queue::connection()`     |
| [Illuminate\Contracts\Queue\QueueableCollection](https://github.com/illuminate/contracts/blob/9.x/Queue/QueueableCollection.php)                   | &nbsp;                    |
| [Illuminate\Contracts\Queue\QueueableEntity](https://github.com/illuminate/contracts/blob/9.x/Queue/QueueableEntity.php)                           | &nbsp;                    |
| [Illuminate\Contracts\Queue\ShouldQueue](https://github.com/illuminate/contracts/blob/9.x/Queue/ShouldQueue.php)                                   | &nbsp;                    |
| [Illuminate\Contracts\Redis\Factory](https://github.com/illuminate/contracts/blob/9.x/Redis/Factory.php)                                           | `Redis`                   |
| [Illuminate\Contracts\Routing\BindingRegistrar](https://github.com/illuminate/contracts/blob/9.x/Routing/BindingRegistrar.php)                     | `Route`                   |
| [Illuminate\Contracts\Routing\Registrar](https://github.com/illuminate/contracts/blob/9.x/Routing/Registrar.php)                                   | `Route`                   |
| [Illuminate\Contracts\Routing\ResponseFactory](https://github.com/illuminate/contracts/blob/9.x/Routing/ResponseFactory.php)                       | `Response`                |
| [Illuminate\Contracts\Routing\UrlGenerator](https://github.com/illuminate/contracts/blob/9.x/Routing/UrlGenerator.php)                             | `URL`                     |
| [Illuminate\Contracts\Routing\UrlRoutable](https://github.com/illuminate/contracts/blob/9.x/Routing/UrlRoutable.php)                               | &nbsp;                    |
| [Illuminate\Contracts\Session\Session](https://github.com/illuminate/contracts/blob/9.x/Session/Session.php)                                       | `Session::driver()`       |
| [Illuminate\Contracts\Support\Arrayable](https://github.com/illuminate/contracts/blob/9.x/Support/Arrayable.php)                                   | &nbsp;                    |
| [Illuminate\Contracts\Support\Htmlable](https://github.com/illuminate/contracts/blob/9.x/Support/Htmlable.php)                                     | &nbsp;                    |
| [Illuminate\Contracts\Support\Jsonable](https://github.com/illuminate/contracts/blob/9.x/Support/Jsonable.php)                                     | &nbsp;                    |
| [Illuminate\Contracts\Support\MessageBag](https://github.com/illuminate/contracts/blob/9.x/Support/MessageBag.php)                                 | &nbsp;                    |
| [Illuminate\Contracts\Support\MessageProvider](https://github.com/illuminate/contracts/blob/9.x/Support/MessageProvider.php)                       | &nbsp;                    |
| [Illuminate\Contracts\Support\Renderable](https://github.com/illuminate/contracts/blob/9.x/Support/Renderable.php)                                 | &nbsp;                    |
| [Illuminate\Contracts\Support\Responsable](https://github.com/illuminate/contracts/blob/9.x/Support/Responsable.php)                               | &nbsp;                    |
| [Illuminate\Contracts\Translation\Loader](https://github.com/illuminate/contracts/blob/9.x/Translation/Loader.php)                                 | &nbsp;                    |
| [Illuminate\Contracts\Translation\Translator](https://github.com/illuminate/contracts/blob/9.x/Translation/Translator.php)                         | `Lang`                    |
| [Illuminate\Contracts\Validation\Factory](https://github.com/illuminate/contracts/blob/9.x/Validation/Factory.php)                                 | `Validator`               |
| [Illuminate\Contracts\Validation\ImplicitRule](https://github.com/illuminate/contracts/blob/9.x/Validation/ImplicitRule.php)                       | &nbsp;                    |
| [Illuminate\Contracts\Validation\Rule](https://github.com/illuminate/contracts/blob/9.x/Validation/Rule.php)                                       | &nbsp;                    |
| [Illuminate\Contracts\Validation\ValidatesWhenResolved](https://github.com/illuminate/contracts/blob/9.x/Validation/ValidatesWhenResolved.php)     | &nbsp;                    |
| [Illuminate\Contracts\Validation\Validator](https://github.com/illuminate/contracts/blob/9.x/Validation/Validator.php)                             | `Validator::make()`       |
| [Illuminate\Contracts\View\Engine](https://github.com/illuminate/contracts/blob/9.x/View/Engine.php)                                                 | &nbsp;                    |
| [Illuminate\Contracts\View\Factory](https://github.com/illuminate/contracts/blob/9.x/View/Factory.php)                                             | `View`                    |
| [Illuminate\Contracts\View\View](https://github.com/illuminate/contracts/blob/9.x/View/View.php)                                                   | `View::make()`            |