## policies:resource.notmodifiable

```json
{
  "topic": "org.eclipse.ditto/the_policy_id/policies/errors",
  "headers": {
    "correlation-id": "<preserved-command-correlation-id>"
  },
  "path": "/",
  "value": {
    "status": 403,
    "error": "policies:resource.notmodifiable",
    "message": "The Resource '/the_resource_path' of the PolicyEntry with Label 'the_label' on the Policy with ID 'org.eclipse.ditto:the_policy_id' could not be modified as the requester had insufficient permissions.",
    "description": "Check if the ID of the Policy, the Label of the PolicyEntry and the path of your requested Resource was correct and you have sufficient permissions."
  },
  "status": 403
}
```
