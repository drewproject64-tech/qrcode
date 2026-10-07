import json
import os
from pathlib import Path
from typing import Any

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = DATA_DIR / "state.json"

DEFAULT_STATE = {
    "redirect_enabled": False,
    "promo_text": "LEER BIEN 🎖️\n\nSI TE UNES A ESTE  CANAL  GANARÁS  DINERO SI SIGUES LOS PASOS GRATIS ✅⬇️\n\n1- https://t.me/+mwvAYvIHQnpkMTU0\n\n2- https://t.me/+D3DCl-6EOvIwODkx\n\n☝️CUANDO LO COMPLETES  MÁNDAME CAPTURA DE QUE TE HAS UNIDO EN @tepasolanoticia ☝️\n\nPON OK CUANDO TE UNAS",
    "promo_image": "assets/promo.jpg",
}

def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        save_state(DEFAULT_STATE)
        return dict(DEFAULT_STATE)
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return {**DEFAULT_STATE, **data}
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT_STATE)

def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def get_state() -> dict[str, Any]:
    return load_state()

def update_state(**changes: Any) -> dict[str, Any]:
    state = load_state()
    state.update(changes)
    save_state(state)
    return state
