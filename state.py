from typing import TypedDict, List, Dict, Optional


class State(TypedDict):
    conversation: List[Dict[str, str]]
    call_status: str
    language: Optional[str]
    summary: Optional[str]
