# Writing Tests

## Best Practices

### Implementation Details

Never write tests that test implementation details. These tests fail when the code changes, not when the actual feature changes, resulting in a flakey and unreliable test suite.

### Black Box

Treat the unit/stack that you are testing as a black box. Pass it inputs and expect outputs. For example, if you are writing an integration test to verify a particular email gets sent, you should pass in the appropriate parameters and mock the email API so that you can capture the expected API request being made. This gives the test the most amount of surface area and has a better likelihood of capturing bugs while being cheap to write.

### Isolation

Never write tests that are covered by other tests. It's always better to write less tests that cover more surface area (but are only testing one thing) so that if a feature regresses, it's easy to find the single test that is failing instead of having to parse through the noise of tests that are all failling because they are covering the same point of failure.

### Editing Tests

It is ALWAYS ok to rewrite/refactor tests to make the test suite more robust as you add new features.
