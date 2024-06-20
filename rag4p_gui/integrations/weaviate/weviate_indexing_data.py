from rag4p.rag.store.content_store import ContentStore

from rag4p_gui.data.indexing_data import IndexingData
from rag4p_gui.integrations.weaviate.indexing import WeaviateContentStoreMetadataService

from rag4p.integrations.weaviate.access_weaviate import AccessWeaviate
from rag4p.integrations.weaviate.weaviate_content_store import WeaviateContentStore
from rag4p.integrations.weaviate.chunk_collection import weaviate_properties


class WeaviateIndexingData(IndexingData):
    def __init__(self, access_weaviate: AccessWeaviate):
        super().__init__(metadata_service=WeaviateContentStoreMetadataService(access_weaviate))
        self.access_weaviate = access_weaviate

    def _create_content_store(self) -> ContentStore:
        content_store = WeaviateContentStore(weaviate_access=self.access_weaviate,
                                             embedder=self.embedder,
                                             collection_name=self.collection_name)
        self.access_weaviate.force_create_collection(collection_name=self.collection_name,
                                                     properties=weaviate_properties(self.additional_properties))

        return content_store
