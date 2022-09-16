## things:feature.desiredProperty.notmodifiable

```json
{
  "topic": "org.eclipse.ditto/fancy-thing/things/twin/errors",
  "headers": {
    "correlation-id": "<preserved-command-correlation-id>"
  },
  "path": "/",
  "value": {
    "status": 403,
    "error": "things:feature.desiredProperty.notmodifiable",
    "message": "The desired property with JSON Pointer '/x' of the Feature with ID 'accelerometer' on the Thing with ID 'org.eclipse.ditto:fancy-thing' could not be modified as the requester had insufficient permissions to modify it (WRITE is required).",
    "description": "Check if the ID of the Thing, the Feature ID and the key of your requested desired property was correct and you have sufficient permissions."
  },
  "status": 403
}
```