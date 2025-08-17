<<<<<<< HEAD
# Chat Messages API (FastAPI + SQLite)

API RESTful para procesar y almacenar mensajes de chat. Cumple con la evaluación técnica: validación, procesamiento (filtro simple), almacenamiento en SQLite, manejo de errores y pruebas.

## Requisitos
- Python 3.10+

## Instalación y ejecución
```bash
# 1) Clonar/descargar este repo
# 2) Crear y activar entorno virtual
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 3) Instalar dependencias
pip install -r requirements.txt

# 4) Ejecutar
uvicorn app.main:app --reload
```

Visita la documentación interactiva en:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints
### POST `/api/messages`
- Recibe un mensaje con el esquema:
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```
- Valida y procesa (filtra palabras prohibidas, agrega metadatos) y almacena en DB.
- Respuesta de éxito:
```json
{
  "status": "success",
  "data": {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system",
    "metadata": {
      "word_count": 6,
      "character_count": 32,
      "processed_at": "2023-06-15T14:30:01Z"
    }
  }
}
```

### GET `/api/messages/{session_id}`
- Recupera mensajes por sesión con paginación `limit`/`offset` y filtro opcional por `sender` (`user` o `system`).
- Devuelve `total`, `limit`, `offset` y `items` (lista de mensajes con metadatos).

## Manejo de errores
Los errores devuelven:
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FORMAT",
    "message": "Formato de mensaje inválido",
    "details": "El campo 'sender' debe ser 'user' o 'system'"
  }
}
```
## Ejemplos de Uso

Crear un mensaje

``` Request

curl -X POST "http://127.0.0.1:8000/api/messages" \
  -H "Content-Type: application/json" \
  -H "x-api-key: mysecretkey" \
  -d '{
    "message_id": "msg-001",
    "session_id": "session-123",
    "content": "Hola mundo desde la API",
    "timestamp": "2024-08-14T16:00:00",
    "sender": "user"
  }'
```
``` Response (201 Created)

{
  "status": "success",
  "data": {
    "message_id": "msg-001",
    "session_id": "session-123",
    "content": "Hola mundo desde la API 🚀",
    "timestamp": "2024-08-14T16:00:00",
    "sender": "user",
    "metadata": {
      "word_count": 5,
      "character_count": 27,
      "processed_at": "2025-08-17T18:00:00"
    }
  }
}
```
Listar mensajes de una sesión

``` Request

curl -X GET "http://127.0.0.1:8000/api/messages/session-123?limit=5&offset=0" \
  -H "x-api-key: mysecretkey"
```

``` Response (200 OK)

{
  "status": "success",
  "data": {
    "total": 1,
    "limit": 5,
    "offset": 0,
    "items": [
      {
       "message_id": "msg-001",
        "session_id": "session-123",
        "content": "Hola mundo desde la API",
        "timestamp": "2024-08-14T16:00:00",
        "sender": "user",
        "metadata": {
          "word_count": 5,
          "character_count": 27,
          "processed_at": "2025-08-17T18:00:00"
        }
      }
    ]
  }
}
```

## Pruebas
```bash
pytest
```
Se incluye cobertura (`pytest-cov`). Objetivo: 80%+.

## Estructura del proyecto
```
app/
  api/
    routes/
      health.py
      messages.py
    deps.py
  core/
    config.py
    errors.py
  db/
    base.py
    models.py
    repositories.py
  schemas/
    message.py
  services/
    processing.py
  main.py
tests/
  test_health.py
  test_processing.py
  test_messages.py
```

## Variables de entorno
Copia `.env.example` a `.env` si quieres personalizar el archivo de BD u otros parámetros.
Por defecto, usa `sqlite:///./app.db`.

## Docker
```bash
docker build -t chat-messages-api .
docker run -p 8000:8000 chat-messages-api
```

## Notas
- El filtrado de palabras es básico (lista de términos configurables).
- El contenido se guarda **ya filtrado**.
- Los metadatos se almacenan como columnas para consultas eficientes.
=======
# EvaluacionTecnicaPython
>>>>>>> 8b9cabacbdff91a9505a99a794dca082dc77f1aa
