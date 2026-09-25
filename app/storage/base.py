"""
Abstract Storage Provider Base Class.
Defines mandatory interface for file persistence strategies (Local, AWS S3, Google Cloud Storage, Azure Blob).
"""

from abc import ABC, abstractmethod


class StorageProvider(ABC):
    """Abstract storage interface enforcing modular storage providers."""

    @abstractmethod
    async def save(self, content: bytes, original_filename: str, subfolder: str = "") -> tuple[str, str, str]:
        """
        Saves file content to storage.
        
        :param content: Binary file content
        :param original_filename: Name of the uploaded file
        :param subfolder: Optional target subfolder directory
        :return: Tuple of (stored_filename, relative_path, absolute_path)
        """
        pass

    @abstractmethod
    async def read(self, relative_path: str) -> bytes:
        """
        Reads binary file content from storage.
        
        :param relative_path: Relative storage path
        :return: File binary content
        """
        pass

    @abstractmethod
    async def delete(self, relative_path: str) -> bool:
        """
        Deletes file from storage if present.
        
        :param relative_path: Relative storage path
        :return: True if deleted, False if file did not exist
        """
        pass

    @abstractmethod
    async def exists(self, relative_path: str) -> bool:
        """
        Checks if file exists at relative path.
        
        :param relative_path: Relative storage path
        :return: True if file exists, False otherwise
        """
        pass

    @abstractmethod
    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Generates a collision-resistant filename preserving file extension.
        
        :param original_filename: Original user filename
        :return: UUID-based unique filename
        """
        pass

    @abstractmethod
    def get_absolute_path(self, relative_path: str) -> str:
        """
        Resolves absolute path on target storage system.
        
        :param relative_path: Relative path
        :return: Absolute file path
        """
        pass

    @abstractmethod
    def get_relative_path(self, absolute_path: str) -> str:
        """
        Converts absolute path to storage-root relative path.
        
        :param absolute_path: Absolute file path
        :return: Relative path
        """
        pass
