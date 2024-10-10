import json
import os

from rag4p.indexing.input_document import InputDocument
from rag4p.indexing.jsonl_content_reader import JsonlContentReader

from rag4p_gui.util.file_util import normalize_path


class JFallJsonlReader(JsonlContentReader):
    def __init__(self, file_name: str):
        path_to_file = os.path.join('..', '..', '..', 'data', file_name)
        file_path = normalize_path(os.path.realpath(__file__), path_to_file)

        super().__init__(file_path=file_path)

    def map_to_input_document(self, data) -> InputDocument:
        properties = {
            "speakers": data["speakers"],
            "title": data["title"],
            "room": data["room"],
            "time": data["time"],
            "tags": data["tags"]
        }
        document_id = data["title"].lower().replace(" ", "-")
        document = InputDocument(
            document_id=document_id,
            text=data["description"] if "description" in data else "",
            properties=properties
        )
        return document
