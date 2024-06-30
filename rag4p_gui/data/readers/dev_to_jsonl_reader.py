import json
import os
import datetime

from rag4p.indexing.input_document import InputDocument
from rag4p.indexing.jsonl_content_reader import JsonlContentReader

from rag4p_gui.util.file_util import normalize_path


class DevToJsonlReader(JsonlContentReader):
    def __init__(self, file_name: str):
        path_to_file = os.path.join('..', '..', '..', 'data', file_name)
        file_path = normalize_path(os.path.realpath(__file__), path_to_file)

        super().__init__(file_path=file_path)

    def map_to_input_document(self, data) -> InputDocument:
        published_at = datetime.datetime.fromtimestamp(data["published_at"])

        # Convert the datetime object to an ISO formatted date string
        iso_date_string = published_at.isoformat() + 'Z'

        properties = {
            "title": data["title"],
            "published_at": iso_date_string,
            "author": data["user"],
            "url": data["url"],
            "tags": data["tags"]
        }
        document_id = data["title"].lower().replace(" ", "-")
        document = InputDocument(
            document_id=document_id,
            text=data["details"] if "details" in data else "",
            properties=properties
        )
        return document
