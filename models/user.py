from dataclasses import dataclass, field
from typing import List, Optional

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.base_class import mapper_registry, Base


@mapper_registry.mapped
@dataclass
class User(Base):
    name: str = field(metadata={"sa": Column(String, primary_key=True)})
    password: str = field(metadata={"sa": Column(String)})
