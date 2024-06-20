from rag4p.integrations.opensearch.index_components import ComponentTemplate, ComponentSettings, \
    ComponentDynamicMappings, ComponentMappings
from rag4p.integrations.opensearch.opensearch_client import OpenSearchClient
from rag4p.integrations.opensearch.opensearch_template import OpenSearchTemplate

from rag4p_gui.data.content_store_metadata import ContentStoreMetadata
from rag4p_gui.data.content_store_metadata_service import ContentStoreMetadataService


class LuminisComponentTemplate(ComponentTemplate):
    def __init__(self, name: str, index_name: str, embedding_dimension: int):
        version = 1
        component_names = ["common_settings", "luminis_mappings", "common_dynamic_mappings"]
        super().__init__(name=name, version=version, index_name=index_name, component_names=component_names,
                         embedding_dimension=embedding_dimension)


class TeqnationComponentTemplate(ComponentTemplate):
    def __init__(self, name: str, index_name: str, embedding_dimension: int):
        version = 1
        component_names = ["common_settings", "teqnation_mappings", "common_dynamic_mappings"]
        super().__init__(name=name, version=version, index_name=index_name, component_names=component_names,
                         embedding_dimension=embedding_dimension)


class LuminisComponentMappings(ComponentMappings):
    def __init__(self):
        version = 1
        name = "luminis_mappings"
        mappings = {
            "title": {
                "type": "text"
            },
            "content": {
                "type": "text"
            },
            "date": {
                "type": "date"
            },
            "tags": {
                "type": "keyword"
            }
        }
        super().__init__(name=name, version=version, mappings=mappings)


class TeqnationComponentMappings(ComponentMappings):
    def __init__(self):
        version = 3
        name = "teqnation_mappings"
        mappings = {
            "title": {
                "type": "text"
            },
            "speakers": {
                "type": "text"
            },
            "room": {
                "type": "text"
            },
            "time": {
                "type": "text"
            },
            "tags": {
                "type": "keyword"
            }
        }
        super().__init__(name=name, version=version, mappings=mappings)


def update_template(opensearch_client: OpenSearchClient, index_name: str, dataset: dict, embedding_dimension: int):
    if dataset["name"] in ["Luminis Wordpress All", "Luminis Wordpress Few"]:
        index_template = LuminisComponentTemplate(name=f"{index_name}_index_template",
                                                  index_name=index_name,
                                                  embedding_dimension=embedding_dimension)
        component_mappings = LuminisComponentMappings()
    elif dataset["name"] in ["Teqnation sessions"]:
        index_template = TeqnationComponentTemplate(name=f"{index_name}_index_template",
                                                    index_name=index_name,
                                                    embedding_dimension=embedding_dimension)
        component_mappings = TeqnationComponentMappings()
    else:
        raise ValueError(f"Dataset {dataset['name']} is not supported.")

    # TODO - the version is specific to the code of the components
    component_settings = ComponentSettings(name="common_settings", version=1, settings={})
    component_dyn_mappings = ComponentDynamicMappings(name="common_dynamic_mappings", version=1, dynamic_mappings=[])

    opensearch_template = OpenSearchTemplate(client=opensearch_client,
                                             index_template=index_template,
                                             component_settings=component_settings,
                                             component_dyn_mappings=component_dyn_mappings,
                                             component_mappings=component_mappings)

    opensearch_template.create_update_template()


META_DATA_COLLECTION_NAME = "rag4p-meta"


class OpenSearchContentStoreMetadataService(ContentStoreMetadataService):

    def __init__(self, opensearch_client: OpenSearchClient):
        self.opensearch_client = opensearch_client
        self.init_collection()

    def init_collection(self, force: bool = False):
        client = self.opensearch_client.client()

        exists = client.indices.exists(index=META_DATA_COLLECTION_NAME)
        if exists and force:
            client.indices.delete(index=META_DATA_COLLECTION_NAME)
            exists = False
        if not exists:
            response = client.indices.create(index=META_DATA_COLLECTION_NAME, body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "collection_name": {"type": "keyword"},
                        "splitter": {"type": "keyword"},
                        "chunkSize": {"type": "integer"},
                        "embedder": {"type": "keyword"},
                        "embedding_model": {"type": "keyword"},
                        "dataset": {"type": "keyword"},
                        "num_documents": {"type": "integer"},
                        "num_chunks": {"type": "integer"},
                        "running_time": {"type": "float"},
                        "created_at": {"type": "date"},
                        "content_reader": {"type": "text"},
                    }
                }
            })

            print(response)

    def save_meta_data(self, meta: ContentStoreMetadata):
        client = self.opensearch_client.client()
        doc = {
            "collection_name": meta.collection_name,
            "splitter": meta.splitter,
            "chunkSize": meta.chunk_size if meta.chunk_size is not None else None,
            "embedder": meta.embedder,
            "embedding_model": meta.embedding_model,
            "dataset": meta.dataset,
            "num_documents": meta.num_documents,
            "num_chunks": meta.num_chunks,
            "running_time": meta.running_time,
            "created_at": meta.created_at,
            "content_reader": meta.contentReader,
        }

        client.index(index=META_DATA_COLLECTION_NAME, body=doc, id=meta.collection_name)

    def get_meta_data(self, collection_name: str) -> ContentStoreMetadata:
        client = self.opensearch_client.client()
        response = client.get(index=META_DATA_COLLECTION_NAME, id=collection_name)
        return self._extract_metadata(response)

    def get_all_meta_data(self) -> [ContentStoreMetadata]:
        client = self.opensearch_client.client()
        response = client.search(index=META_DATA_COLLECTION_NAME, body={"query": {"match_all": {}}, "size": 100})
        if response["hits"]["total"]["value"] == 0:
            return []
        return [self._extract_metadata(hit) for hit in response["hits"]["hits"]]

    def _extract_metadata(self, hit):
        return ContentStoreMetadata(
            collection_name=hit["_source"]["collection_name"],
            splitter=hit["_source"]["splitter"],
            chunk_size=hit["_source"]["chunkSize"],
            embedder=hit["_source"]["embedder"],
            embedding_model=hit["_source"]["embedding_model"],
            dataset=hit["_source"]["dataset"],
            num_documents=hit["_source"]["num_documents"],
            num_chunks=hit["_source"]["num_chunks"],
            running_time=hit["_source"]["running_time"],
            created_at=hit["_source"]["created_at"],
            contentReader=hit["_source"]["content_reader"]
        )


if __name__ == "__main__":
    from rag4p.util.key_loader import KeyLoader
    from rag4p.integrations.opensearch.connection_builder import build_aws_search_service
    from dotenv import load_dotenv

    load_dotenv()

    key_loader = KeyLoader()
    opensearch_conn = build_aws_search_service(stack_name=key_loader.get_property("OPENSEARCH_STACK_NAME"),
                                               application_prefix=key_loader.get_property("OPENSEARCH_APP_PREFIX"))
    opensearch_client = OpenSearchClient(opensearch_conn)

    meta_service = OpenSearchContentStoreMetadataService(opensearch_client)
    meta_service.init_collection(force=True)


