from typing import Any
import json
import os

STARRED = "starred"

class Storage:
    def __init__(self, storage_path: str):
        self._storage_path: str = storage_path
        self._storage: dict[str, Any] = {}
        self._load()

    def _save(self):
        with open(self._storage_path, "w") as file:
            json.dump(self._storage, file)

    def _load(self):
        if not os.path.exists(self._storage_path):
            return

        with open(self._storage_path, "r") as file:
            self._storage = json.load(file)

    def get_starred_messages(self) -> list[int]:
        if STARRED not in self._storage:
            return []

        return self._storage[STARRED]

    def add_starred_message(self, message_id: int) -> None:
        if STARRED not in self._storage:
            self._storage[STARRED] = [message_id]
        else:
            self._storage[STARRED].append(message_id)

        self._save()
