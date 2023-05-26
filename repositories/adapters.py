from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):
    """Base adapter class."""
    @staticmethod
    def find(path: str, data: dict, default: Any = None):
        """Find a element inside data using a provided path.

        :param element: Path to element.
        :type element: str
        :param data: Data to search into.
        :type data: dict
        :param default: Return if value is not found, defaults to None
        :type default: Any, optional
        :return: Value found on provided path.
        :rtype: _type_
        """
        keys = path.split('.')
        rv = data
        try:
            for key in keys:
                rv = rv[key]
            return rv
        except TypeError:
            return default

    @classmethod
    @abstractmethod
    def from_data(cls, data: Any):
        """Parse provided data."""


class CommitAdapter(BaseAdapter):
    """Adapter for Github commit raw data"""
    @classmethod
    def from_data(cls, data: dict) -> dict:
        """Parse commit raw data from Github api response to dict with only required fields.

        :param data: Commit raw data from Github api
        :type data: dict
        :return: Dict containing only required data from commit.
        :rtype: dict
        """
        fields = {
            "message": "commit.message",
            "sha": "sha",
            "author": "commit.author.name",
            "url": "url",
            "date": "commit.author.date",
            "avatar": "author.avatar_url"
        }

        return {key: cls.find(path, data) for key, path in fields.items()}
