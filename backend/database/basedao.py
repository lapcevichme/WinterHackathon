from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from session import async_session_maker

ModelType = TypeVar("ModelType")

class BaseDao(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self._id_name = list(model.__table__.primary_key.columns.keys())[0]
        
    async def create_entity(self, data: Dict[str, Any]):
        async with async_session_maker() as session:
            obj = self.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
    
    async def get_entity_by_id(self, id: int):
        async with async_session_maker() as session:
            obj = await session.execute(select(self.model).where(getattr(self.model_db, self._id_name) == id))
            return obj.scalars().first()