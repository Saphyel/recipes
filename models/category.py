from dataclasses import dataclass, field

from sqlalchemy import Column, String

from db.base_class import mapper_registry, Base


@mapper_registry.mapped
@dataclass
class Category(Base):
    name: str = field(
        default=None,
        metadata={"sa": Column(String, primary_key=True)}
    )
