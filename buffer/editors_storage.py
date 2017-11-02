from typing import Dict

EDITORS = dict()  # type: Dict[int, str]


class MultipleEditors(RuntimeError):
    pass


def add_buffer_editor(buffer_id: int, channel_id: str):
    if buffer_id in EDITORS:
        raise MultipleEditors("Cannot add another editor to {} buffer"
                              .format(buffer_id))

    EDITORS[buffer_id] = str(channel_id)


def get_buffer_editor(buffer_id: int) -> str:
    return EDITORS.get(buffer_id, None)


def remove_buffer_editors(buffer_id: int):
    EDITORS.pop(buffer_id, None)
