from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime

from db.base_class import mapper_registry, Base


@mapper_registry.mapped
@dataclass
class Recipe(Base):
    title: str = field(
        default=None,
        metadata={"sa": Column(String, primary_key=True)}
    )
    image: str = field(default=None, metadata={"sa": Column(String)})
    active_cook: int = field(default=None, metadata={"sa": Column(Integer)})
    total_cook: int = field(default=None, metadata={"sa": Column(Integer)})
    serves: int = field(default=None, metadata={"sa": Column(Integer)})
    description: str = field(default=None, metadata={"sa": Column(String)})
    instructions: str = field(default=None, metadata={"sa": Column(String)})
    url: str = field(default=None, metadata={"sa": Column(String)})
    category_name: str = field(
        default=None,
        metadata={"sa": Column(ForeignKey('category.name'), index=True)}
    )
    user_name: str = field(
        default=None,
        metadata={"sa": Column(String)}
    )
    updated: datetime = field(
        default=None,
        metadata={"sa": Column(DateTime(timezone=True))}
    )
    created: datetime = field(
        default=datetime.utcnow(),
        metadata={"sa": Column(DateTime(timezone=True))}
    )
