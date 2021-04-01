from dataclasses import dataclass, field
from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base_class import mapper_registry, Base
from models.recipe import Recipe


@mapper_registry.mapped
@dataclass
class User(Base):
    name: str = field(
        default=None,
        metadata={"sa": Column(String, primary_key=True)}
    )
    reddit: str = field(
        default=None,
        metadata={"sa": Column(String)}
    )
    instagram: str = field(
        default=None,
        metadata={"sa": Column(String)}
    )
    twitter: str = field(
        default=None,
        metadata={"sa": Column(String)}
    )
    recipes: List[Recipe] = field(
        default_factory=list,
        metadata={"sa": relationship("Recipe")}
    )
