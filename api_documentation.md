# PrintFlow Assistant API Documentation

**Base URL:** `http://localhost:8080/api/v1`

---

## Endpoints

### Health Check

**Endpoint:** `GET /api/v1/health`

**Response:**
```json
{
  "status": "ok"
}
```

---

### Chat

**Endpoint:** `POST /api/v1/chat`

**Request:**
```json
{
  "message": "Is API access available on the Starter plan?"
}
```

**Response:**
```json
{
  "response": "No, API access is not available on the Starter plan. API access is available on the Pro plan (60 requests per minute) and Enterprise plan (600 requests per minute)."
}
```

**Field Details:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `message` | string | Yes | User question. Must not be empty. |

**Error Responses:**

| Status | Error |
|--------|-------|
| 400 | Invalid or empty message |
| 500 | Server error |

---

## Examples

### cURL
```bash
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What file formats do you support?"}'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8080/api/v1/chat",
    json={"message": "How do I add team members?"}
)
print(response.json()["response"])
```

### JavaScript
```javascript
const response = await fetch("http://localhost:8080/api/v1/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "What's the storage limit on Pro?" })
});

const data = await response.json();
console.log(data.response);
```

---

## Response Examples

**Feature Query:**
```json
{
  "response": "Variable data printing (VDP) is available on Pro and Enterprise plans."
}
```

**How-To Query:**
```json
{
  "response": "To fix an ERR_BLEED pre-flight failure, add 3mm bleed to all sides in your design software and re-export."
}
```

**Invalid Request:**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "Chat message cannot be empty.",
      "type": "value_error"
    }
  ]
}
```

---

## API Documentation

Access auto-generated API docs at:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
