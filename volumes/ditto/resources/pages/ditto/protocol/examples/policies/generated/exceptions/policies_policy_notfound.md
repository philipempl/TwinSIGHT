## policies:policy.notfound

```json
{
  "topic": "org.eclipse.ditto/the_policy_id/policies/errors",
  "headers": {
    "correlation-id": "<preserved-command-correlation-id>"
  },
  "path": "/",
  "value": {
    "status": 404,
    "error": "policies:policy.notfound",
    "message": "The Policy with ID 'org.eclipse.ditto:the_policy_id' could not be found or requester had insufficient permissions to access it.",
    "description": "Check if the ID of your requested Policy was correct and you have sufficient permissions."
  },
  "status": 404
}
```
