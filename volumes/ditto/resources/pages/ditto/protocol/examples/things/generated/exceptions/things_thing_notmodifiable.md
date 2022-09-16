## things:thing.notmodifiable

```json
{
  "topic": "org.eclipse.ditto/fancy-thing/things/twin/errors",
  "headers": {
    "correlation-id": "<preserved-command-correlation-id>"
  },
  "path": "/",
  "value": {
    "status": 403,
    "error": "things:thing.notmodifiable",
    "message": "The Thing with ID 'org.eclipse.ditto:fancy-thing' could not be modified as the requester had insufficient permissions (WRITE is required).",
    "description": "Check if the ID of your requested Thing was correct and you have sufficient permissions."
  },
  "status": 403
}
```
