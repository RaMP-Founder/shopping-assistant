# memory.py
import json
import time
import fakeredis

redis_client = fakeredis.FakeStrictRedis()

def get_history(session_id: str):
    raw = redis_client.get(f"session:{session_id}")
    if not raw:
        return []
    try:
        return json.loads(raw)
    except:
        return []

def append_history(session_id: str, role: str, text: str):
    key = f"session:{session_id}"
    history = get_history(session_id)
    history.append({
        "role": role,
        "text": text,
        "ts": int(time.time())
    })
    redis_client.set(key, json.dumps(history))