---
slug: designing-testable-cpp-robotics
categories: [languages, testing, architecture]
priority: 2
description: Design C++ and ROS 2 components with explicit seams, deterministic lifetimes, and pure decision logic so correctness can be verified without hardware.
applies_when:
  - designing testable C++ components
  - generating or reviewing ROS 2 robotics code
  - isolating hardware, time, concurrency, or platform dependencies
  - building automated validation for generated C++ code
related: [writing-cpp, writing-tests, sans-io, hexagonal-architecture]
source: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
---

# Design Testable C++ Robotics Code

Every component containing decision logic must run without ROS, hardware,
networking, wall-clock time, or sleeping. Keep ROS 2 and platform APIs in thin
adapters; represent perception, controller state, commands, configuration, and
failures as explicit value types. Given identical state, input, and elapsed time,
core logic should return identical output and new state.

Choose seams deliberately:

- Runtime interfaces suit hardware and service boundaries.
- Template or concept parameters suit lightweight, performance-sensitive
  dependencies.
- Link seams suit C APIs, vendor libraries, and legacy embedded code.

Do not over-template application logic or introduce inheritance solely for
mocks. Inject clocks, filesystems, networks, and device APIs; never bury globals,
singleton state, `now()`, `sleep_for()`, environment access, or vendor calls
inside business logic.

Use RAII for every thread, lock, socket, file, and device handle. Background work
must have explicit ownership, bounded waits, shutdown semantics, and
deterministic joining. Constructors establish invariants; separate `start()`
operations perform fallible side effects.

Expose failures and state transitions through typed results and explicit enums
rather than logs, booleans, or scattered callback state. Validate injected
configuration immediately. Encode safety limits as executable invariants and use
unit-safe types for time and physical quantities.

Verify in layers: deterministic unit and property tests, component tests,
compiler checks, sanitizers, recorded-data replay, simulation, ROS integration,
then hardware-in-the-loop. Keep headers thin so testability remains practical at
compile time. Reject generated controller code that directly uses ROS APIs,
unmanaged threads, unbounded operations, hardware access, or hidden fault states.
