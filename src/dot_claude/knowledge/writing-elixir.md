---
slug: writing-elixir
categories: [elixir]
priority: 1
description: Elixir style — pattern matching, tagged tuples, OTP, supervision trees, structs, typespecs.
applies_when:
  - writing Elixir code
  - designing OTP processes
  - handling errors in Elixir
  - designing structs
related: [coding-style, writing-tests]
---

# Elixir

## Pattern Matching

Prefer pattern matching in function heads over conditional logic inside function bodies:

```elixir
# WRONG: conditional logic inside the body
def handle_result(result) do
  if elem(result, 0) == :ok do
    elem(result, 1)
  else
    raise "failed"
  end
end

# CORRECT: pattern matching in function heads
def handle_result({:ok, value}), do: value
def handle_result({:error, reason}), do: raise "failed: #{reason}"
```

Rules:
- Use pattern matching to destructure data -- never use `elem/2` or `Map.get/2` for fields you know exist
- Use assertive (static) map access `map.key` for required keys, dynamic access `map[:key]` only for optional keys
- Use `[head | tail]` destructuring over `hd/1` and `tl/1`
- Match only what guards need in the function signature -- extract remaining fields inside the body
- Use `=` to bind the whole structure when you need both the parts and the whole: `%User{age: age} = user`

## Error Handling

Use `{:ok, result}` / `{:error, reason}` tuples for expected failures. Reserve exceptions for truly unexpected situations.

```elixir
# WRONG: exceptions for control flow
def read_config(path) do
  try do
    contents = File.read!(path)
    Jason.decode!(contents)
  rescue
    e -> {:error, Exception.message(e)}
  end
end

# CORRECT: pattern matching on tagged tuples
def read_config(path) do
  with {:ok, contents} <- File.read(path),
       {:ok, decoded} <- Jason.decode(contents) do
    {:ok, decoded}
  end
end
```

### Bang Functions

Follow the `foo` / `foo!` convention:
- `foo` returns `{:ok, result}` or `{:error, reason}` -- use when callers need to handle failure
- `foo!` raises on failure -- use when failure is unexpected and should crash the process

```elixir
def fetch_user(id) do
  case Repo.get(User, id) do
    nil -> {:error, :not_found}
    user -> {:ok, user}
  end
end

def fetch_user!(id) do
  case fetch_user(id) do
    {:ok, user} -> user
    {:error, reason} -> raise "failed to fetch user #{id}: #{reason}"
  end
end
```

### `with` Expressions

Keep `with` clauses focused. Avoid complex `else` blocks -- normalize errors in private helper functions instead:

```elixir
# WRONG: complex else block obscures which step failed
def process(input) do
  with {:ok, parsed} <- parse(input),
       {:ok, validated} <- validate(parsed) do
    {:ok, validated}
  else
    {:error, %Jason.DecodeError{}} -> {:error, :bad_json}
    {:error, :missing_field} -> {:error, :invalid}
    {:error, other} -> {:error, other}
  end
end

# CORRECT: normalize errors at the source
def process(input) do
  with {:ok, parsed} <- parse_input(input),
       {:ok, validated} <- validate(parsed) do
    {:ok, validated}
  end
end

defp parse_input(input) do
  case Jason.decode(input) do
    {:ok, parsed} -> {:ok, parsed}
    {:error, _} -> {:error, :bad_json}
  end
end
```

### Rules

- Never use `try/rescue` for expected error paths -- use `case` and pattern matching
- Use `{:error, atom}` or `{:error, {atom, details}}` -- never `{:error, "string"}`
- Let processes crash on unexpected errors -- the supervisor will restart them
- Use `with` for chaining multiple fallible operations, plain `case` for a single one

## Type Design

### Structs Over Maps

Never pass raw maps as domain data. Use structs with `@enforce_keys`:

```elixir
# WRONG: untyped map
def create_order(data) when is_map(data) do
  %{id: generate_id(), items: data[:items], total: data[:total]}
end

# CORRECT: typed struct
defmodule Order do
  @enforce_keys [:items, :total]
  defstruct [:id, :items, :total]
end

def create_order(%{items: items, total: total}) do
  %Order{id: generate_id(), items: items, total: total}
end
```

### Atoms Over Booleans

```elixir
# WRONG: what does `true` mean?
def send_message(msg, true), do: ...
def send_message(msg, false), do: ...

# CORRECT: semantic meaning
def send_message(msg, :urgent), do: ...
def send_message(msg, :normal), do: ...
```

### Make Invalid States Unrepresentable

Model variants as separate structs or tagged tuples, not optional fields:

```elixir
# WRONG: which fields are valid depends on status
defmodule Order do
  defstruct [:status, :items, :shipped_at, :tracking]
end

# CORRECT: each state carries exactly its data
defmodule PendingOrder do
  @enforce_keys [:items]
  defstruct [:items]
end

defmodule ShippedOrder do
  @enforce_keys [:items, :shipped_at, :tracking]
  defstruct [:items, :shipped_at, :tracking]
end
```

### Rules

- Use `@enforce_keys` for required struct fields
- Keep structs under 32 fields -- the BEAM switches from a flat tuple to a hash map beyond that, increasing memory usage
- Use atoms for fixed sets of known values, never dynamically create atoms from external input
- Use `String.to_existing_atom/1` if you must convert external strings to atoms

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Modules | PascalCase | `MyApp.UserService` |
| Functions, variables | snake_case | `parse_config` |
| Atoms | snake_case | `:user_not_found` |
| Constants (module attributes) | snake_case with `@` | `@max_retries` |
| Predicate functions | trailing `?` | `valid?`, `empty?` |
| Unsafe/raising functions | trailing `!` | `fetch!`, `decode!` |
| Macros | snake_case | `defstruct`, `is_valid` |
| Acronyms in PascalCase | One word | `HttpClient` not `HTTPClient` |

Naming patterns:
- Predicate functions return booleans and end with `?`
- Functions that raise on failure end with `!`
- Private helper functions use a leading `_` only when required by the compiler for unused variables
- Prefix context/boundary modules with the app name: `MyApp.Accounts`, `MyApp.Billing`

## Typespecs

Add `@spec` to all public functions. Use specific types, not `term()` or `any()`:

```elixir
# WRONG: no spec or overly generic
def calculate_total(items), do: ...

# CORRECT: specific types
@spec calculate_total([LineItem.t()]) :: Money.t()
def calculate_total(items), do: ...
```

Rules:
- Define `@type t :: %__MODULE__{}` for every struct
- Use `@opaque` for types whose internals should not be accessed by other modules
- Define custom types for domain concepts: `@type user_id :: pos_integer()`
- Run `dialyzer` in CI to catch type inconsistencies
- Use `@typedoc` for non-obvious custom types

## Testing

Use ExUnit. Mirror the source tree under `test/`.

### Structure

```elixir
defmodule MyApp.ParserTest do
  use ExUnit.Case, async: true

  describe "parse/1" do
    test "returns parsed result for valid input" do
      assert {:ok, %{name: "Alice"}} = Parser.parse(~s({"name": "Alice"}))
    end

    test "returns error for invalid JSON" do
      assert {:error, :bad_json} = Parser.parse("not json")
    end
  end
end
```

### Mocking

Use `Mox` for mocking -- it enforces explicit contracts via behaviours:

```elixir
# Define the behaviour
defmodule MyApp.HttpClient do
  @callback get(String.t()) :: {:ok, map()} | {:error, term()}
end

# In test_helper.exs
Mox.defmock(MyApp.MockHttpClient, for: MyApp.HttpClient)

# In tests
import Mox

setup :verify_on_exit!

test "fetches user data" do
  expect(MyApp.MockHttpClient, :get, fn _url ->
    {:ok, %{"name" => "Alice"}}
  end)

  assert {:ok, user} = MyApp.Users.fetch("123")
end
```

### Rules

- Always use `async: true` unless tests share global state
- Use `describe` blocks to group tests by function
- Test `{:ok, _}` and `{:error, _}` paths with equal rigor
- Use pattern matching in assertions: `assert {:ok, %User{name: "Alice"}} = result`
- Never mock modules you do not own -- wrap third-party APIs behind a behaviour and mock the wrapper
- Use `setup` and `setup_all` for shared test context, not repeated code in each test

## Module Organization

- Organize by domain/feature (contexts), not by type (models, controllers, views)
- Keep modules focused and small
- Use one module per file
- Use `defdelegate` to expose functions from child modules through a context boundary

```
lib/
  my_app/
    application.ex       -- OTP application, supervision tree
    accounts/
      accounts.ex        -- context boundary (public API)
      user.ex
      credential.ex
    billing/
      billing.ex         -- context boundary
      invoice.ex
      payment.ex
test/
  my_app/
    accounts/
      accounts_test.exs
    billing/
      billing_test.exs
```

### Module Layout

Order sections within a module consistently:

1. `@moduledoc`
2. `@behaviour` / `use` / `import` / `alias` / `require`
3. Module attributes (`@type`, `@enforce_keys`, `defstruct`, constants)
4. Public functions
5. Private functions
6. Callback implementations (if any)

## Processes & OTP

### When to Use a Process

Only use a process (GenServer, Agent, Task) when you need one of:
- Mutable state that must be shared across callers
- Concurrency or parallelism
- Error isolation (crash one thing without crashing another)
- A long-running background operation

```elixir
# WRONG: GenServer for pure computation
defmodule Calculator do
  use GenServer
  def add(pid, a, b), do: GenServer.call(pid, {:add, a, b})
  def handle_call({:add, a, b}, _from, state), do: {:reply, a + b, state}
end

# CORRECT: plain module function
defmodule Calculator do
  def add(a, b), do: a + b
end
```

### GenServer

- Wrap all process interaction (calls, casts, starts) in public functions in the same module -- never call `GenServer.call/2` from outside the module
- Use `call` for operations that need a response, `cast` only when you truly do not care about the result or ordering
- Extract only the data you need before sending messages -- message passing copies entire data structures

```elixir
# WRONG: sending the entire conn struct
spawn(fn -> log_request(conn) end)

# CORRECT: extract only what you need
ip = conn.remote_ip
spawn(fn -> log_request(ip) end)
```

### Supervision

- Always start long-running processes under a supervision tree
- Use `:one_for_one` unless processes have genuine dependencies
- Keep supervisors simple -- their only job is lifecycle management
- Split large applications into multiple supervisors by domain

## Pipelines

Use the pipe operator `|>` for chaining transformations. Do not use it for a single function call:

```elixir
# WRONG: single-step pipe
result = input |> String.trim()

# CORRECT: direct call
result = String.trim(input)

# CORRECT: multi-step pipe
result =
  input
  |> String.trim()
  |> String.downcase()
  |> String.replace(" ", "_")
```

Rules:
- Always use parentheses in piped function calls
- Start pipes with a raw value or variable, not a function call
- Each step in a pipe should do one transformation
- Avoid side-effectful functions in the middle of a pipe -- put them at the end

## Performance

- Use `Stream` for lazy evaluation of large collections -- avoid materializing intermediate lists
- Use `ETS` for shared read-heavy state instead of a GenServer bottleneck
- Use `Task.async_stream/3` for parallelizing independent I/O operations
- Use binary pattern matching for parsing binary data, not `String.split/2`
- Prefer `IO.iodata_to_binary/1` and iodata lists over repeated string concatenation
- Use `:persistent_term` for data written once and read many times
- Profile before optimizing -- use `:timer.tc/1`, `:fprof`, or Benchee

## Anti-Patterns to Avoid

- Using `try/rescue` for expected error paths -- use tagged tuples and pattern matching
- Dynamically creating atoms from user input -- atoms are never garbage collected
- Using a GenServer for pure computation with no state
- Spreading raw `GenServer.call/3` / `Agent.get/3` calls across many modules
- Returning different shapes from the same function based on options
- Using `Enum` functions with `elem/2` instead of pattern matching
- Bare `rescue` or `catch` that swallows all errors
- Starting processes outside of a supervision tree
- Stringly-typed errors (`{:error, "something went wrong"}`)
- Mutable default arguments via module attributes that hold references
