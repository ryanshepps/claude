# Writing Tests

## Best Practices

### Implementation Details

NEVER test implementation details (e.g., internal function calls, private method names, internal data structures). Tests should only fail when a behaviour is broken, not when the implementation behind it changes.

### Black Box

Treat the unit/stack that you are testing as a black box. Pass it inputs and expect outputs. For example, if you are writing an integration test to verify a particular email gets sent, you should pass in the appropriate parameters and mock the email API so that you can capture the expected API request being made. This gives the test the most amount of surface area and has a better likelihood of capturing bugs while being cheap to write.

### Isolation

Tests should not overlap. Each behaviour should be covered by exactly one test so that a regression produces exactly one failure.

### Editing Tests

It is ALWAYS ok to rewrite/refactor tests to make the test suite more robust as you add new features.
