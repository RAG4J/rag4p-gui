from abc import ABC, abstractmethod

from rag4p_gui.data.content_store_metadata import ContentStoreMetadata


class ContentStoreMetadataService(ABC):

    @abstractmethod
    def init_collection(self, force: bool = False):
        """
        Initialize the collection to store the information about available content sets. This methode checks if the
        collection already exists and creates it if it does not exist. If the collection already exists, it will be
        deleted and recreated if the force parameter is set to True.
        :return:
        """
        pass

    @abstractmethod
    def save_meta_data(self, meta: ContentStoreMetadata):
        """
        Save the metadata of a content set. If the name of the content set already exists in the collection, the
        metadata will be updated.
        :param meta: The metadata of the content set.
        :return:
        """
        pass

    @abstractmethod
    def get_meta_data(self, collection_name: str) -> ContentStoreMetadata:
        """
        Get the metadata of a content set.
        :param collection_name: The name of the content set.
        :return: The metadata of the content set.
        """
        pass

    @abstractmethod
    def get_all_meta_data(self) -> [ContentStoreMetadata]:
        """
        Get the metadata of all content sets.
        :return: The metadata of all content sets.
        """
        pass
