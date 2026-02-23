# Coding Style

## Comments

- NEVER include "historical" comments that will become irrelevant to whomever is reviewing the code at the present time.
- Prefer not to use comments. The code could itself should be simple and understandable enought that it is self documenting.
- If you feel that you must use a comment, add the comment and then refactor the code to make it self documenting so the comment is no longer needed.

## Testing

- NEVER test implementation details. Tests should test behaviours/features and should only fail when a "feature" or "behaviour" is broken, not when the implementation of the feature/behaviour is changed.
- Tests SHOULD NOT overlap one another. If there is a regression in the behaviour/feature, only one test should fail which to make it easy to find what is failing. 

## Types

- Care about types, use them to your advantage. Types are a powerful tool for ensuring correctness and preventing bugs.
- When creating types, think about the mental model each type will create (e.g., does this type have a clear role/responsibility within the codebase given all the other types). If the mental model is unclear, consider refactoring the code to make it more clear.

## Immutability

ALWAYS create new objects, NEVER mutate:

```javascript
// WRONG: Mutation
function updateUser(user, name) {
  user.name = name  // MUTATION!
  return user
}

// CORRECT: Immutability
function updateUser(user, name) {
  return {
    ...user,
    name
  }
}
```

## File Organization

MANY SMALL FILES > FEW LARGE FILES:
- High cohesion, low coupling
- 200-400 lines typical, 800 max
- Extract utilities from large components
- Organize by feature/domain, not by type

## Error Handling

ALWAYS handle errors comprehensively:

```typescript
try {
  const result = await riskyOperation()
  return result
} catch (error) {
  console.error('Operation failed:', error)
  throw new Error('Detailed user-friendly message')
}
```
