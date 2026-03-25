# Java

## Modern Language Features

Use modern Java (21+) features as the baseline. Records, sealed classes, and pattern matching are not optional -- they are the expected way to write Java.

### Records

Use records for immutable data carriers instead of traditional POJOs:

```java
public record Point(int x, int y) {}
```

Rules:
- Use records for all immutable data carriers -- DTOs, value objects, API responses
- Add compact constructors for validation, not separate factory methods
- Records are shallowly immutable -- ensure fields are themselves immutable types
- Use records with sealed interfaces for algebraic data types

### Sealed Classes

Use sealed interfaces to define closed type hierarchies:

```java
public sealed interface Shape permits Circle, Rectangle, Triangle { double area(); }
public record Circle(double radius) implements Shape { public double area() { return Math.PI * radius * radius; } }
public record Rectangle(double width, double height) implements Shape { public double area() { return width * height; } }
public record Triangle(double base, double height) implements Shape { public double area() { return 0.5 * base * height; } }
```

### Pattern Matching

Use pattern matching with `instanceof` and `switch` to eliminate explicit casting:

```java
// Exhaustive switch with sealed types -- no default needed
double area = switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    case Triangle t -> 0.5 * t.base() * t.height();
};
```

## Error Handling

Use unchecked exceptions for programming errors. Use checked exceptions only when the caller can reasonably recover.

```java
public class UserNotFoundException extends RuntimeException {
    private final UserId userId;
    public UserNotFoundException(UserId userId) {
        super("User not found: " + userId);
        this.userId = userId;
    }
    public UserId userId() { return userId; }
}
```

Rules:
- Define a base exception per module/package, subclass for specific errors
- Always include context (IDs, parameters) in exception fields -- not just the message
- Never catch `Exception` or `Throwable` in business logic -- catch specific types
- Never swallow exceptions with empty catch blocks
- Use try-with-resources for all `AutoCloseable` resources -- never manually close in `finally`
- Prefer unchecked exceptions. Use checked exceptions only at system boundaries (I/O, network) where the caller has a meaningful recovery strategy
- Chain exceptions with `throw new XException("context", cause)` to preserve the stack trace

## Null Handling & Optional

Treat `null` as a bug. Use `Optional` as a return type to represent absent values -- never as a field, parameter, or collection element.

```java
public Optional<User> findUser(UserId id) {
    return Optional.ofNullable(userMap.get(id));
}

// Use map/orElseThrow -- never Optional.get()
return findUser(id)
    .map(User::name)
    .orElseThrow(() -> new UserNotFoundException(id));
```

Rules:
- Never use `Optional.get()` -- use `orElseThrow()`, `orElse()`, `map()`, or `ifPresent()`
- Use `orElseGet()` instead of `orElse()` when the default is expensive to compute
- Never use `Optional` as a method parameter, constructor argument, or record component
- Return empty collections instead of `Optional<List<T>>` -- an empty list IS the "no result" case
- `Optional` is not `Serializable` -- never use it as a field in persistent or transferable objects

## Type Design

### Make Invalid States Unrepresentable

Use sealed interfaces and records so only valid states can exist:

```java
// WRONG: invalid states are representable
public class Order {
    private String status;
    private Instant shippedAt;  // null when not shipped
    private String tracking;    // null when not shipped
}

// CORRECT: each state carries exactly its own data
public sealed interface Order permits PendingOrder, ShippedOrder {}

public record PendingOrder(List<Item> items) implements Order {}

public record ShippedOrder(
    List<Item> items,
    Instant shippedAt,
    String tracking
) implements Order {}
```

### Enums Over Booleans and Strings

```java
// WRONG: what does true mean?
void sendMessage(String msg, boolean urgent) { /* ... */ }

// CORRECT: semantic meaning
enum Priority { NORMAL, URGENT }
void sendMessage(String msg, Priority priority) { /* ... */ }
```

Use enums with fields and methods instead of switch-on-string logic:

```java
public enum HttpMethod {
    GET(false), POST(true), PUT(true), DELETE(false);
    private final boolean hasBody;
    HttpMethod(boolean hasBody) { this.hasBody = hasBody; }
    public boolean hasBody() { return hasBody; }
}
```

### Immutability

Prefer immutable objects. Use records, `List.of()`, `Map.of()`, `Set.of()`, and `Collections.unmodifiable*` to prevent mutation:

```java
// WRONG: mutable, leaks internal state
public class Team {
    private final List<String> members;
    public List<String> members() { return members; }
}

// CORRECT: defensive immutable copy
public record Team(List<String> members) {
    public Team {
        members = List.copyOf(members);
    }
}
```

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Packages | lowercase, reverse domain | `com.example.auth` |
| Classes, Interfaces, Enums, Records | PascalCase | `HttpResponse` |
| Methods, variables | camelCase | `parseConfig` |
| Constants (`static final`) | SCREAMING_SNAKE_CASE | `MAX_RETRIES` |
| Type parameters | Single uppercase or short PascalCase | `T`, `E`, `K`, `V` |
| Acronyms in PascalCase | One word | `Uuid` not `UUID`, `HttpClient` not `HTTPClient` |

Method prefixes:
- `is`/`has`/`can`/`should` -- boolean query, return `boolean`
- `get` -- getter (use only for JavaBean compatibility; prefer bare name in records)
- `to` -- conversion returning a new type (`toString`, `toList`)
- `of`/`from` -- static factory constructor (`List.of()`, `Instant.from()`)
- `create`/`new` -- factory method when `of` is ambiguous
- `find`/`lookup` -- query that may return `Optional`
- No `get`/`set` in records -- records use bare accessor names: `point.x()` not `point.getX()`

## Testing

Use JUnit 5. Do not use JUnit 4 or `TestCase` unless maintaining legacy code.

```java
class UserServiceTest {
    @Test
    void rejectsBlankUsername() {
        var ex = assertThrows(ValidationException.class, () -> UserService.createUser(""));
        assertEquals("username must not be blank", ex.getMessage());
    }
}
```

Rules:
- Use `assertAll()` to group related assertions -- reports all failures, not just the first
- Use `assertThrows()` instead of `@Test(expected = ...)` -- it returns the exception for further inspection
- Use AssertJ for complex assertions over raw JUnit asserts
- Use `@ParameterizedTest` with `@CsvSource`/`@MethodSource` to eliminate test duplication
- Name test methods descriptively: `rejectsBlankUsername`, not `testCreateUser1`
- One behavior per test method. Use `assertAll()` only for closely related checks on the same result
- Never mock what you don't own -- wrap third-party APIs behind your own interface and mock that
- Use `@Nested` classes to group tests by scenario or feature
- Test behavior, not implementation details

## Package Organization

Organize by domain/feature, not by layer. Group `User`, `UserService`, `UserRepository`, and `UserController` together in `com.example.user/` -- not spread across `controllers/`, `services/`, `repositories/`.

Rules:
- Package names are always lowercase, no underscores
- Never use wildcard imports (`import com.example.*`)
- Keep packages focused -- if a package has 20+ classes, split by subdomain
- Use package-private (default) visibility aggressively -- only `public` what must be public
- Declare module boundaries with `module-info.java` for larger projects

## Concurrency

### Virtual Threads (Java 21+)

Use virtual threads for I/O-bound work. They make blocking-style code scale without reactive frameworks:

```java
// CORRECT: virtual thread per task for I/O-bound work
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    var future1 = executor.submit(() -> fetchUser(userId));
    var future2 = executor.submit(() -> fetchOrders(userId));
    return new UserProfile(future1.get(), future2.get());
}
```

### Rules
- Use virtual threads for I/O-bound tasks (network, disk, database)
- Use platform threads only for CPU-bound computation
- Never use `synchronized` with virtual threads -- use `ReentrantLock` instead (pinning risk on < Java 24)
- Never share mutable state between threads -- use immutable objects or thread-safe collections
- Use `CompletableFuture` for composing async pipelines when you need transformations/chaining
- Prefer `ConcurrentHashMap` over `Collections.synchronizedMap()`

## Streams

Use streams for declarative data transformations. Use loops for simple iterations or when mutation is unavoidable:

```java
var activeUserNames = users.stream()
    .filter(User::isActive)
    .map(User::name)
    .sorted()
    .toList();
```

Rules:
- Never use streams for side effects -- use a loop instead
- Prefer `toList()` (Java 16+) over `collect(Collectors.toList())`
- Use `Stream.of()` and `Stream.concat()` over creating intermediate lists
- Avoid nested streams -- extract inner operations to a method
- Use parallel streams only for CPU-bound work on large datasets (10k+ elements) and benchmark first

## Performance

- Prefer `StringBuilder` for building strings in loops, `String.join()` for simple concatenation
- Use `List.of()`, `Map.of()`, `Set.of()` for small immutable collections -- they are more memory-efficient
- Use `EnumSet` and `EnumMap` instead of `HashSet`/`HashMap` when keys are enums
- Specify initial capacity for `HashMap` and `ArrayList` when size is known
- Prefer `switch` expressions over `if-else` chains -- the compiler generates a tableswitch/lookupswitch
- Avoid autoboxing in hot paths -- use primitive specializations (`IntStream`, `OptionalInt`)
- Always benchmark before optimizing -- use JMH for microbenchmarks, not `System.nanoTime()`

## Linting & Formatting

- Use Spotless with the Palantir Java Format enforced in CI -- never debate formatting
- Run Error Prone or SpotBugs in CI to catch common bugs at compile time
- Use `@Override` on every overriding method -- the compiler catches accidental overloads
- Suppress warnings only with `@SuppressWarnings("specific-warning")` and never `"all"`
- Enable `-Xlint:all` compiler warnings

## Anti-Patterns to Avoid

- Raw types (`List` instead of `List<String>`)
- Mutable DTOs with getters/setters -- use records
- Premature optimization without profiling -- benchmark with JMH first
