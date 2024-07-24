import weaviate.classes.config as wvc
from rag4p.integrations.weaviate.access_weaviate import AccessWeaviate

from rag4p_gui.data.content_store_metadata import ContentStoreMetadata
from rag4p_gui.data.content_store_metadata_service import ContentStoreMetadataService

META_DATA_COLLECTION_NAME = "Rag4pMeta"


class WeaviateContentStoreMetadataService(ContentStoreMetadataService):
    def __init__(self, access_weaviate: AccessWeaviate):
        self.access_weaviate = access_weaviate
        self.init_collection()

    def delete_meta_data(self, collection_name: str):
        doc_id = self._find_document_id(collection_name)
        if doc_id is not None:
            self._meta_coll().data.delete_by_id(doc_id)
        else:
            raise ValueError(f"Meta document with collection name {collection_name} does not exist")
        self.access_weaviate.delete_collection(collection_name)

    def get_all_meta_data(self) -> [ContentStoreMetadata]:
        meta_list = self._meta_coll().iterator()

        return [
            self._extract_content_store_metadata(meta.properties)
            for meta in meta_list
        ]

    def get_meta_data(self, collection_name: str) -> ContentStoreMetadata:
        meta = self._meta_coll().query.fetch_objects()
        for o in meta.objects:
            if o.properties["collectionName"] == collection_name:
                return self._extract_content_store_metadata(o.properties)

        raise ValueError(f"Meta document with collection name {collection_name} does not exist")

    def save_meta_data(self, meta: ContentStoreMetadata):
        weaviate_doc = {
            "collectionName": meta.collection_name,
            "splitter": meta.splitter,
            "chunkSize": meta.chunk_size if meta.chunk_size is not None else None,
            "embedder": meta.embedder,
            "embeddingModel": meta.embedding_model,
            "dataset": meta.dataset,
            "numDocuments": meta.num_documents,
            "numChunks": meta.num_chunks,
            "runningTime": meta.running_time,
            "createdAt": meta.created_at,
            "contentReader": meta.contentReader,
        }

        doc_id = self._find_document_id(meta.collection_name)
        if doc_id is not None:
            self._meta_coll().data.replace(doc_id, weaviate_doc)
        else:
            self._meta_coll().data.insert(weaviate_doc)

    def init_collection(self, force: bool = False):

        exists = self.access_weaviate.does_collection_exist(META_DATA_COLLECTION_NAME)
        if exists and force:
            self.access_weaviate.delete_collection(META_DATA_COLLECTION_NAME)
            exists = False
        if not exists:
            properties = [
                wvc.Property(name="collectionName", data_type=wvc.DataType.TEXT),
                wvc.Property(name="splitter", data_type=wvc.DataType.TEXT),
                wvc.Property(name="chunkSize", data_type=wvc.DataType.INT),
                wvc.Property(name="embedder", data_type=wvc.DataType.TEXT),
                wvc.Property(name="embeddingModel", data_type=wvc.DataType.TEXT),
                wvc.Property(name="dataset", data_type=wvc.DataType.TEXT),
                wvc.Property(name="numDocuments", data_type=wvc.DataType.INT),
                wvc.Property(name="numChunks", data_type=wvc.DataType.INT),
                wvc.Property(name="runningTime", data_type=wvc.DataType.NUMBER),
                wvc.Property(name="createdAt", data_type=wvc.DataType.DATE),
                wvc.Property(name="contentReader", data_type=wvc.DataType.TEXT),
            ]

            self.access_weaviate.client.collections.create(
                name=META_DATA_COLLECTION_NAME,
                properties=properties,
            )

    def _meta_coll(self):
        return self.access_weaviate.client.collections.get(META_DATA_COLLECTION_NAME)

    @staticmethod
    def _extract_content_store_metadata(meta):
        return ContentStoreMetadata(
            collection_name=meta["collectionName"],
            splitter=meta["splitter"],
            chunk_size=meta["chunkSize"],
            embedder=meta["embedder"],
            embedding_model=meta["embeddingModel"],
            dataset=meta["dataset"],
            num_documents=meta["numDocuments"],
            num_chunks=meta["numChunks"],
            running_time=meta["runningTime"],
            created_at=meta["createdAt"],
            contentReader=meta["contentReader"],
        )

    def _find_document_id(self, collection_name: str) -> str | None:
        meta = self._meta_coll().query.fetch_objects()
        for o in meta.objects:
            if o.properties["collectionName"] == collection_name:
                return o.uuid

        return None




