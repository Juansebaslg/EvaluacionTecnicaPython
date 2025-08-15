from datetime import datetime, timezone
from app.core.config import settings

def _valid_payload(**overrides):
    data = {
        "message_id": "msg-1",
        "session_id": "session-a",
        "content": "hola foo mundo",
        "timestamp": datetime(2024,1,1,tzinfo=timezone.utc).isoformat(),
        "sender": "user",
    }
    data.update(overrides)
    return data

def test_post_message_success(client):
    payload = _valid_payload()
    r = client.post("/api/messages", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    data = body["data"]
    assert data["message_id"] == payload["message_id"]
    assert data["metadata"]["word_count"] >= 1
    # masked foo -> *** should appear
    assert "***" in data["content"]

def test_post_message_duplicate_id(client):
    payload = _valid_payload(message_id="dup-1")
    r1 = client.post("/api/messages", json=payload)
    assert r1.status_code == 200

    r2 = client.post("/api/messages", json=payload)
    assert r2.status_code == 409
    err = r2.json()
    assert err["status"] == "error"
    assert err["error"]["code"] == "DUPLICATE_MESSAGE_ID"

def test_post_message_invalid_sender(client):
    payload = _valid_payload(sender="robot")
    r = client.post("/api/messages", json=payload)
    assert r.status_code == 422
    body = r.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "INVALID_FORMAT"

def test_get_messages_basic(client):
    # create 2 messages
    r1 = client.post("/api/messages", json=_valid_payload(message_id="m1"))
    r2 = client.post("/api/messages", json=_valid_payload(message_id="m2", content="hola mundo"))
    assert r1.status_code == 200 and r2.status_code == 200

    r = client.get("/api/messages/session-a?limit=1&offset=0")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "success"
    data = body["data"]
    assert data["total"] == 2
    assert len(data["items"]) == 1

def test_get_messages_filter_sender(client):
    client.post("/api/messages", json=_valid_payload(message_id="mx1", sender="user"))
    client.post("/api/messages", json=_valid_payload(message_id="mx2", sender="system"))

    r = client.get("/api/messages/session-a?sender=user")
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["sender"] == "user"

def test_get_messages_invalid_sender_query(client):
    r = client.get("/api/messages/session-a?sender=robot")
    assert r.status_code == 422
    err = r.json()
    assert err["status"] == "error"
    assert err["error"]["code"] == "INVALID_FORMAT"
