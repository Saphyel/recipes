from dataclasses import dataclass, field
from typing import List, Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base_class import mapper_registry, Base
from models.recipe import Recipe


@mapper_registry.mapped
@dataclass
class Chef(Base):
    name: str = field(metadata={"sa": Column(String, primary_key=True)})
    reddit: Optional[str] = field(default=None, metadata={"sa": Column(String)})
    instagram: Optional[str] = field(default=None, metadata={"sa": Column(String)})
    twitter: Optional[str] = field(default=None, metadata={"sa": Column(String)})
    recipes: List[Recipe] = field(default_factory=list, metadata={"sa": relationship("Recipe", lazy="joined")})
