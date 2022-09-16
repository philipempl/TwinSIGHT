## things:attribute.notfound

```json
{
  "topic": "org.eclipse.ditto/fancy-thing/things/twin/errors",
  "headers": {
    "correlation-id": "<preserved-command-correlation-id>"
  },
  "path": "/",
  "value": {
    "status": 404,
    "error": "things:attribute.notfound",
    "message": "The attribute with key '/location' on the thing with ID 'org.eclipse.ditto:fancy-thing' could not be found or the requester had insufficient permissions to access it.",
    "description": "Check if the ID of the thing and the key of your requested attribute was correct and you have sufficient permissions."
  },
  "status": 404
}
```
