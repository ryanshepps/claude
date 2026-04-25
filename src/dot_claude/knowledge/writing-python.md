---
slug: writing-python
categories: [languages]
priority: 1
description: Python 3.10+ style — type annotations, dataclasses, pytest, error handling, module organization.
applies_when:
  - writing Python code
  - reviewing Python code
  - setting up a Python project
  - writing Python tests
related: [coding-style, writing-tests]
---

# Python

## Type Annotations

Every function signature must have type annotations. Use modern syntax (Python 3.10+):

- Use `list[str]` not `List[str]`, `dict[str, int]` not `Dict[str, int]`
- Use `X | None` not `Optional[X]`, `X | Y` not `Union[X, Y]`
- Annotate return types, including `-> None`
- Use `Self` for methods that return their own type
- Never use `Any` -- narrow to a specific type or protocol
- Use `typing.Protocol` for structural subtyping instead of ABC when you only need a few methods

```python
# WRONG: no annotations, legacy syntax
from typing import Optional, List
def process(items, flag=False): ...

# CORRECT: modern annotations
def process(items: list[str], flag: bool = False) -> dict[str, int]: ...
```

Run `mypy --strict` or `pyright` in CI. Use `# type: ignore[code]` only when unavoidable and always with the specific error code.

## Error Handling

Raise and catch specific exceptions. Never use bare `except:` or `except Exception:` as a catch-all in business logic.

```python
# WRONG: swallows everything
try:
    result = parse(data)
except Exception:
    return None

# CORRECT: catch what you expect, chain exceptions
try:
    result = parse(data)
except ParseError as exc:
    raise ConfigError(f"invalid config in {path}") from exc
```

Prefer EAFP (try/except) over LBYL (check-then-act) when failure is rare. Use LBYL when the check is cheap and the exception would be ambiguous. Keep `try` blocks narrow.

```python
# EAFP -- Pythonic when missing keys are rare
try:
    value = mapping[key]
except KeyError:
    handle_missing()

# Best -- use APIs that handle it
value = mapping.get(key, default)
```

### Custom Exceptions

Define a base exception per package. Subclass for specific errors. Name with an `Error` suffix. Place in a dedicated `errors.py` for larger packages.

### Rules

- Always chain exceptions with `raise X from exc` to preserve the traceback
- Never return `None` to signal failure -- raise an exception
- Use `contextlib.suppress(SomeError)` instead of empty `except` blocks
- Always use `with` statements for resources (files, connections, locks)

## Type Design

### Dataclasses Over Raw Dicts

Never pass untyped dicts as data containers. Use `dataclasses` for internal data, `pydantic.BaseModel` for external boundaries (API input, config files):

```python
# WRONG: untyped bag of keys
def create_user(data: dict) -> dict:
    return {"id": generate_id(), **data}

# CORRECT: typed, immutable domain object
@dataclass(frozen=True, slots=True)
class User:
    id: UserId
    name: str
    email: str
```

### Rules

- Use `frozen=True` by default. Use tuples over lists for fixed-size sequences
- Use `slots=True` (3.10+) for memory efficiency
- If you define `__eq__` manually, you **must** define `__hash__` -- otherwise the class breaks in `set`/`dict`. Frozen dataclasses handle this automatically
- Every domain class should have a meaningful `__repr__`
- Use `@functools.total_ordering` to define only `__eq__` and one comparison operator

### Enums Over Strings and Booleans

```python
# WRONG: stringly-typed, typo-prone
def send(msg: str, priority: str) -> None: ...

# CORRECT: enum
class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

def send(msg: str, priority: Priority) -> None: ...
```

Use `StrEnum` (3.11+) when the enum must serialize as its string value.

### Make Invalid States Unrepresentable

Model variants with unions of dataclasses, not optional fields:

```python
# WRONG: which fields are valid depends on status
@dataclass
class Order:
    status: str
    shipped_at: datetime | None = None
    tracking: str | None = None

# CORRECT: each state carries exactly its own data
@dataclass(frozen=True)
class PendingOrder:
    items: list[Item]

@dataclass(frozen=True)
class ShippedOrder:
    items: list[Item]
    shipped_at: datetime
    tracking: str

Order = PendingOrder | ShippedOrder
```

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Packages | lowercase, no underscores | `mypackage` |
| Modules | snake_case | `auth_service.py` |
| Classes, Exceptions, Type Aliases | PascalCase | `HttpResponse` |
| Functions, methods, variables | snake_case | `parse_config` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRIES` |
| Type variables | PascalCase | `T`, `KeyT`, `ResponseT` |
| Private | leading underscore | `_internal_helper` |

Method prefixes:
- `is_`/`has_` -- boolean query
- `to_` -- conversion returning a new type
- `from_` -- alternate constructor (`@classmethod`)
- `_` prefix -- internal, not part of the public API
- No `get_`/`set_` prefix: use `@property` for computed attributes

## Testing

Use `pytest`. Do not use `unittest.TestCase` unless integrating with legacy code. Mirror the source tree under a top-level `tests/` directory.

### Fixtures

Prefer factory fixtures over complex object literals:

```python
@pytest.fixture
def make_user() -> Callable[..., User]:
    def _make(name: str = "alice", role: Role = Role.MEMBER) -> User:
        return User(id=UserId(uuid4()), name=name, role=role)
    return _make
```

### Rules

- Use `@pytest.mark.parametrize` to cover multiple cases without duplicating test functions
- Use `pytest.raises(SomeError, match="pattern")` to verify exceptions
- Never mock what you don't own -- wrap third-party APIs behind your own interface and mock that
- Test behavior, not implementation details

## Module Organization

- Use the `src/` layout for packages that will be distributed
- Keep `__init__.py` files minimal -- use them for public re-exports only
- Define `__all__` in `__init__.py` to declare the public API explicitly
- Organize by domain/feature, not by layer
- Avoid circular imports by depending on abstractions (protocols) rather than concrete modules

```
project-root/
  pyproject.toml
  src/
    mypackage/
      __init__.py       -- public API re-exports, __all__
      config.py
      errors.py
      models/
        user.py
        order.py
      services/
        auth.py
        payment.py
  tests/
    conftest.py
    models/
      test_user.py
    services/
      test_auth.py
```

## Concurrency

Python's GIL determines which concurrency model to use:

| Model | Use When | GIL Impact |
|---|---|---|
| `asyncio` | I/O-bound (network, disk) | Single-threaded, no GIL contention |
| `threading` | I/O-bound, no async support | GIL released during I/O waits |
| `multiprocessing` | CPU-bound (computation) | Separate processes, no GIL |

- Never block the event loop with CPU work -- offload to `loop.run_in_executor()`
- Use `asyncio.TaskGroup` (3.11+) over `asyncio.gather` -- it cancels siblings on failure
- Never mix `asyncio.run()` calls -- one event loop per thread

## Pattern Matching (3.10+)

Use `match`/`case` for destructuring data, not as a replacement for simple `if`/`elif`:

- Always include a wildcard `case _:` fallback
- Order patterns from most specific to most general
- Use guards (`case x if x > 0:`) for conditional logic

## Performance

- Use generators and `itertools` for large sequences -- avoid materializing full lists
- Generators are single-use -- materialize to a list if you need multiple passes
- Never return a generator from a function that owns a resource (e.g., an open file)
- Use `dict`/`set` for membership checks, not `list`
- Prefer `str.join()` over repeated string concatenation
- Use `functools.lru_cache` for expensive pure functions
- Profile before optimizing -- use `cProfile` or `py-spy`, not intuition

## Linting & Formatting

- Use `ruff` for linting and formatting (replaces flake8, isort, black)
- Run `mypy --strict` or `pyright` in CI with zero tolerance for errors
- Configure all tools in `pyproject.toml`, not scattered config files

## Anti-Patterns to Avoid

- Bare `except:` or `except Exception:` that silently swallows errors
- Mutable default arguments -- use `None` sentinel instead (`def f(items: list[str] | None = None)`)
- Wildcard imports (`from module import *`)
- Global mutable state
- Deep inheritance hierarchies -- prefer composition and protocols
- Using `dict` as a data container when a dataclass would do
