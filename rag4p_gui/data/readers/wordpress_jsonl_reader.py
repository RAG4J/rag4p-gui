import os.path

from rag4p.indexing.input_document import InputDocument
from rag4p.indexing.jsonl_content_reader import JsonlContentReader


class WordpressJsonlReader(JsonlContentReader):

    def __init__(self, file_name: str):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the data folder
        data_dir = os.path.join(current_dir, '..', '..', '..', 'data')

        # Construct the path to the file
        file_path = os.path.join(data_dir, file_name)

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        super().__init__(file_path=file_path)

    def map_to_input_document(self, data) -> InputDocument:
        properties = {
            "post_id": data['post_id'],
            "title": data['title'],
            "url": data['url'],
            "updated_at": data['updated_at'] + '+02:00',
            "tags": data['tags'],
            "categories": data['categories']
        }
        document_id = str(data["post_id"])
        document = InputDocument(
            document_id=document_id,
            text=data["body"],
            properties=properties
        )
        return document
