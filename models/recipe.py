from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime

from db.base_class import mapper_registry, Base


@mapper_registry.mapped
@dataclass
class Recipe(Base):
    title: str = field(metadata={"sa": Column(String, primary_key=True)})
    image: Optional[str] = field(default=None, metadata={"sa": Column(String)})
    active_cook: Optional[int] = field(default=None, metadata={"sa": Column(Integer)})
    total_cook: Optional[int] = field(default=None, metadata={"sa": Column(Integer)})
    serves: Optional[int] = field(default=None, metadata={"sa": Column(Integer)})
    description: Optional[str] = field(default=None, metadata={"sa": Column(String)})
    instructions: Optional[str] = field(default=None, metadata={"sa": Column(String)})
    url: Optional[str] = field(default=None, metadata={"sa": Column(String)})
    category_name: Optional[str] = field(default=None, metadata={"sa": Column(ForeignKey("category.name"), index=True)})
    profile_name: Optional[str] = field(default=None, metadata={"sa": Column(ForeignKey("profile.name"))})
    updated: Optional[datetime] = field(default=None, metadata={"sa": Column(DateTime(timezone=True))})
    created: datetime = field(default=datetime.utcnow(), metadata={"sa": Column(DateTime(timezone=True))})
