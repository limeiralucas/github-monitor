from abc import ABC, abstractmethod
from typing import Any


class BaseAdapter(ABC):
    """Base adapter class."""
    @staticmethod
    def find(element, json):
        """Find data inside json dict using json paths."""
        keys = element.split('.')
        rv = json
        for key in keys:
            rv = rv[key]
        return rv

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
            "date": "commit.author.date"
        }

        return {key: cls.find(path, data) for key, path in fields.items()}
