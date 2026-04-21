# Coding Style

## Comments

- Do not write comments. If code needs a comment to be understood, refactor the code to be self-documenting instead.
- NEVER include historical comments (e.g., "changed from X to Y", "added for bug #123", "previously this was..."). These become irrelevant immediately.

## Types

- Never use Any, unknown, untyped dictionaries/maps or any generic types -- narrow down to specific types instead.
- Each type should represent a single domain concept with a single responsibility.
- Prefer reusing/extending existing types when the domain concept is the same, instead of creating new ones.
- Prefer flat types over deeply nested ones. Avoid generics/type parameters unless reuse across 2+ call sites demands it.

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
