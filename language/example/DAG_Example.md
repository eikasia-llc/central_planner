# Software Release Cycle
- id: release_cycle
- status: active

## Development
- id: phase.dev
- status: in-progress

### Backend Implementation
- id: dev.backend
- status: done

### Frontend Implementation
- id: dev.frontend
- status: in-progress
- blocked_by: [dev.backend]

## Testing
- id: phase.testing
- status: todo
- blocked_by: [phase.dev]

### Unit Tests
- id: test.unit
- status: todo
- blocked_by: [dev.backend, dev.frontend]

### Integration Tests
- id: test.integration
- status: todo
- blocked_by: [test.unit]

## Deployment
- id: phase.deploy
- status: blocked
- blocked_by: [phase.testing]
