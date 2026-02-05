---
paths:
  - "**/*.rs"
  - "**/Cargo.toml"
  - "**/Cargo.lock"
  - "**/{clippy,rustfmt}.toml"
---

# Rust

## Ownership & Borrowing

Prefer borrowing over cloning. Clone is a code smell unless justified:

- Accept `&str` over `String` in function parameters
- Accept `&[T]` over `Vec<T>` in function parameters
- Accept `&Path` over `&PathBuf` in function parameters
- Use `&self` methods by default; only use `&mut self` or `self` when needed
- Return owned types from constructors and builders; return references from accessors
- Never clone to satisfy the borrow checker -- restructure the code instead

```rust
// WRONG: overly specific parameter type
fn process(data: String) { /* ... */ }

// CORRECT: accepts &str, &String, String slices, etc.
fn process(data: &str) { /* ... */ }
```

## Error Handling

Use `thiserror` in libraries for typed error enums. Use `anyhow` in application/binary code for ergonomic propagation.

```rust
// WRONG: stringly-typed errors
fn parse(input: &str) -> Result<Config, String>

// CORRECT: library code with typed errors
#[derive(Debug, thiserror::Error)]
pub enum ParseError {
    #[error("invalid syntax at line {line}")]
    InvalidSyntax { line: usize },
    #[error(transparent)]
    Io(#[from] std::io::Error),
}

// CORRECT: application code with anyhow
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let contents = std::fs::read_to_string(path)
        .context("failed to read config file")?;
    Ok(toml::from_str(&contents)?)
}
```

Rules:
- Never use `.unwrap()` in production code. Use `.expect("reason")` only for true invariants
- Use the `?` operator for propagation, not manual `match` on Result/Option
- Add context with `.context()` when propagating errors up the stack
- Model error variants based on what the caller needs to do, not which internal function failed

## Type Design

### Make Invalid States Unrepresentable

Use enums and the type system so only valid states can exist:

```rust
// WRONG: invalid states are representable
struct Connection {
    socket: Option<TcpStream>,
    is_connected: bool, // can be true when socket is None!
}

// CORRECT: invalid states are impossible
enum Connection {
    Disconnected { address: String, port: u16 },
    Connected { address: String, port: u16, socket: TcpStream },
}
```

### Enums Over Booleans

```rust
// WRONG: what does `true` mean?
fn send_message(msg: &str, is_urgent: bool) { /* ... */ }

// CORRECT: semantic meaning
enum Priority { Normal, Urgent }
fn send_message(msg: &str, priority: Priority) { /* ... */ }
```

### Structs
- Derive standard traits liberally: `#[derive(Debug, Clone, PartialEq, Eq)]`
- Implement `Default` for structs with sensible defaults
- Use the builder pattern for structs with many optional fields
- Use `#[non_exhaustive]` on public enums/structs in libraries

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Crates | kebab-case | `my-crate` |
| Modules | snake_case | `auth_service` |
| Types (struct, enum, trait) | PascalCase | `HttpResponse` |
| Functions, methods | snake_case | `parse_config` |
| Constants, statics | SCREAMING_SNAKE_CASE | `MAX_RETRIES` |
| Type parameters | Single uppercase | `T`, `E`, `K`, `V` |
| Lifetimes | Short lowercase | `'a`, `'de` |
| Acronyms in PascalCase | One word | `Uuid` not `UUID` |

Method prefixes:
- `as_` -- cheap ref-to-ref conversion (free)
- `to_` -- expensive conversion, may allocate
- `into_` -- ownership-consuming conversion
- `is_`/`has_` -- boolean query
- `with_` -- builder-style secondary constructor
- `try_` -- fallible operation returning Result
- No `get_` prefix on getters: use `fn name(&self)` not `fn get_name(&self)`
- Primary constructor is `new`, secondary constructors are `with_*`

## Testing

### Unit Tests
Place in a `#[cfg(test)]` module at the bottom of the file they test:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_input_returns_error() {
        let result = parse("");
        assert!(matches!(result, Err(ParseError::EmptyInput)));
    }
}
```

### Integration Tests
Place in a top-level `tests/` directory. They can only access the crate's public API.

### Doc Tests
Write doc tests on all public API items. They serve as both documentation and tests:

```rust
/// Adds two numbers.
///
/// # Examples
///
/// ```
/// use my_crate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 { a + b }
```

Use `#` to hide boilerplate setup lines in doc tests.

### Property-Based Testing
Use `proptest` for testing invariants over random inputs:
- Serialization/deserialization roundtrips
- Algebraic properties (commutativity, associativity)
- Parser correctness (parse then format is identity)

### Rules
- Use `assert_eq!`/`assert_ne!` over `assert!` when comparing values -- error messages are far more informative
- Test error conditions as rigorously as success cases
- Use `#[should_panic(expected = "...")]` to test expected panics
- Test behavior, not implementation details

## Module Organization

- Keep `main.rs` thin -- move all logic into `lib.rs` for testability and reuse
- Use `pub use` re-exports in `lib.rs` to create a clean public API
- Organize by domain/feature, not by type
- Avoid deep nesting -- two or three module levels is usually sufficient
- Prefer the mod.rs-free style (Rust 2018+): `models.rs` alongside `models/` directory
- Keep modules focused and small

```
src/
  lib.rs          -- public API, re-exports
  main.rs         -- thin entry point
  config.rs
  error.rs
  models/
    user.rs
    order.rs
  services/
    auth.rs
    payment.rs
tests/
  integration_test.rs
```

## Advanced Patterns

### Newtype Pattern
Wrap primitives for type safety at zero runtime cost:

```rust
struct UserId(u64);
struct OrderId(u64);

// Compiler prevents: get_order(order_id, user_id)
fn get_order(user_id: UserId, order_id: OrderId) -> Order { /* ... */ }
```

Also use newtypes for validated construction:

```rust
struct NonEmptyString(String);

impl NonEmptyString {
    pub fn new(s: String) -> Option<Self> {
        if s.is_empty() { None } else { Some(Self(s)) }
    }

    pub fn as_str(&self) -> &str { &self.0 }
}
```

### Typestate Pattern
Encode valid state transitions in the type system so invalid transitions are compile errors:

```rust
struct Locked;
struct Unlocked;
struct Door<State> { _state: PhantomData<State> }

impl Door<Locked>   { fn unlock(self) -> Door<Unlocked> { /* ... */ } }
impl Door<Unlocked> { fn lock(self) -> Door<Locked> { /* ... */ } }
// door.open() on Door<Locked> is a compile error
```

### Traits
- Prefer static dispatch (generics) over dynamic dispatch (`dyn Trait`) unless you need heterogeneous collections
- Keep traits small and focused -- one method per trait is often ideal
- Use associated types when there is exactly one natural implementation per type
- Provide default method implementations where possible
- Use `impl Trait` in return position when the caller does not need to name the concrete type

## Clippy & Linting

- CI runs `cargo clippy -- -D warnings` (configured in VPM)
- Enable `clippy::pedantic` in Cargo.toml and selectively allow noisy lints
- Never enable `clippy::restriction` as a group -- cherry-pick individual lints
- Use `#![forbid(unsafe_code)]` at the crate root for crates that should never use unsafe

## Unsafe Code

- Minimize and isolate: wrap unsafe code in safe abstractions with safe public APIs
- Keep unsafe blocks as small as possible
- Every `unsafe fn` must have a `# Safety` doc section explaining the invariants
- Test with Miri: `cargo +nightly miri test`

## Performance

- Use `Vec::with_capacity(n)` when size is known
- Prefer iterators over manual indexing -- enables compiler optimizations
- Chain iterator adaptors instead of collecting into intermediate Vecs
- Use `Cow<'a, T>` to defer allocation to only when mutation is needed
- Use `&str` for read-only string parameters, `String::with_capacity()` for building
- Always benchmark before optimizing -- use `criterion` for microbenchmarks
- Use `#[inline]` sparingly; the compiler usually makes better inlining decisions

## Anti-Patterns to Avoid

- Excessive `.clone()` to satisfy the borrow checker -- restructure instead
- Stringly-typed errors (`Result<T, String>`)
- `.unwrap()` in production paths
- Using `Deref`/`DerefMut` to emulate inheritance
- Boolean function parameters -- use enums
- Macro overuse -- prefer functions and generics
- Premature abstraction -- only genericize with 2+ concrete use cases
