from dataclasses import dataclass

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import registry

mapper_registry = registry()


@dataclass
class Base:
    __sa_dataclass_metadata_key__ = "sa"

    @declared_attr  # type: ignore[misc]
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # type: ignore[attr-defined]
