from rag4p.integrations.opensearch.index_components import ComponentTemplate, ComponentSettings, \
    ComponentDynamicMappings, ComponentMappings
from rag4p.integrations.opensearch.opensearch_client import OpenSearchClient
from rag4p.integrations.opensearch.opensearch_template import OpenSearchTemplate


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
