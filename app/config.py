import os
import pathlib
from dataclasses import dataclass

# ── Provider switch ──────────────────────────────────────────────────────────
# Change this one variable to switch providers.
# Options: "haiku" | "openrouter" | "ollama"
# DEFAULT IS "haiku" — CodeCrafters submissions always use haiku.
ACTIVE_PROVIDER = "haiku"

# ── Load ai.env without third-party dependencies ─────────────────────────────
def _load_env_file() -> None:
    env_path = pathlib.Path(__file__).parent.parent / "ai.env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

_load_env_file()

# ── Provider definitions ──────────────────────────────────────────────────────
@dataclass
class ProviderConfig:
    model: str
    base_url: str
    api_key: str
    requires_real_key: bool

_PROVIDERS: dict[str, ProviderConfig] = {
    "haiku": ProviderConfig(
        model="anthropic/claude-haiku-4.5",
        base_url="https://openrouter.ai/api/v1",
        api_key="",              # resolved at call time in get_client_config()
        requires_real_key=True,
    ),
    "openrouter": ProviderConfig(
        model="stepfun/step-3.5-flash:free",
        base_url="https://openrouter.ai/api/v1",
        api_key="",              # resolved at call time in get_client_config()
        requires_real_key=True,
    ),
    "ollama": ProviderConfig(
        model="granite4:3b",
        base_url="http://localhost:11434/v1",
        api_key="ollama",        # placeholder — Ollama doesn't validate this
        requires_real_key=False,
    ),
}

def get_client_config() -> ProviderConfig:
    """Return config for the active provider. Raises RuntimeError if invalid."""
    if ACTIVE_PROVIDER not in _PROVIDERS:
        raise RuntimeError(
            f"Unknown provider {ACTIVE_PROVIDER!r}. Choose from: {list(_PROVIDERS)}"
        )
    config = _PROVIDERS[ACTIVE_PROVIDER]
    if config.requires_real_key:
        # Read from environment at call time so the value is always current.
        # _load_env_file() already ran at import time and populated os.environ.
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                f"Provider {ACTIVE_PROVIDER!r} requires OPENROUTER_API_KEY but it is not set. Check ai.env."
            )
        # Respect OPENROUTER_BASE_URL if the environment provides one
        # (CodeCrafters injects this; the original code also read it).
        base_url = os.environ.get("OPENROUTER_BASE_URL", config.base_url).strip()
        import dataclasses
        config = dataclasses.replace(config, api_key=api_key, base_url=base_url)
    return config
