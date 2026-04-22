---
slug: testing-pyramid
categories: [quality]
priority: 2
description: A project should have many fast unit tests, fewer integration tests, and only a small number of UI tests.
applies_when:
  - designing a test suite
  - balancing unit vs integration tests
  - speeding up CI
related: []
source: https://lawsofsoftwareengineering.com/laws/testing-pyramid/
---

# Testing Pyramid

> A project should have many fast unit tests, fewer integration tests, and only a small number of UI tests.

## Key Takeaways

- Unit testing is where you start. Unit tests are run as separate functions and execute quickly. That means you can afford to write lots of unit tests.
- After the unit tests, there must be an integration test layer. These verify the integration of modules. You will require fewer integration tests than unit tests.
- End-to-end tests at the top simulate real-world user scenarios. They are essential but slow and expensive to maintain.
- Organizing tests this way, you receive quick feedback (most tests are quick unit tests), and when your UI test fails, there’s a better chance it’s due to a real problem

## Source

Dr. Milan Milanović — [Laws of Software Engineering](https://lawsofsoftwareengineering.com/laws/testing-pyramid/)
