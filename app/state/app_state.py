from dataclasses import dataclass

@dataclass
class AppState:
    user_name: str | None = None
    theme_mode: str = "light"  # "light" | "dark"
    selected_index: int = 0
