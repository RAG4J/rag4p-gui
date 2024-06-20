from rag4p.rag.store.content_store import ContentStore

from rag4p_gui.data.indexing_data import IndexingData
from rag4p_gui.integrations.opensearch.indexing import OpenSearchContentStoreMetadataService, update_template

from rag4p.integrations.opensearch.opensearch_client import OpenSearchClient
from rag4p.integrations.opensearch.opensearch_content_store import OpenSearchContentStore


class OpenSearchIndexingData(IndexingData):
    def __init__(self, opensearch_client: OpenSearchClient):
        super().__init__(metadata_service=OpenSearchContentStoreMetadataService(opensearch_client))
        self.opensearch_client = opensearch_client

    def _create_content_store(self) -> ContentStore:
        embedder_size = len(self.embedder.embed("test"))
        update_template(opensearch_client=self.opensearch_client,
                        index_name=self.collection_name,
                        dataset=self.dataset,
                        embedding_dimension=embedder_size)

        self.index_name = self.opensearch_client.create_index(provided_alias_name=self.collection_name)

        content_store = OpenSearchContentStore(opensearch_client=self.opensearch_client,
                                               embedder=self.embedder,
                                               index_name=self.index_name)
        return content_store

    def _after_indexing(self):
        self.opensearch_client.switch_alias_to(index_name=self.index_name,
                                               provided_alias_name=self.collection_name)
