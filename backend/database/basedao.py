from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from database import async_session_maker
import uuid
ModelType = TypeVar("ModelType")

class BaseDao(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self._id_name = list(model.__table__.primary_key.columns.keys())[0]
        self.async_session_maker = async_session_maker
        
    async def create_entity(self, data: Dict[str, Any]):
        async with self.async_session_maker() as session:
            obj = self.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
    
    async def get_entity_by_id(self, id: uuid.UUID):
        async with self.async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(getattr(self.model, self._id_name) == id)
            )
            return result.scalars().first()
        
    async def get_entities(self):
        async with self.async_session_maker() as session:
            result = await session.execute(
                select(self.model)
            )
            return result.scalars().all()
        

    async def get_by_username(self, username: str):
        async with self.async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(self.model.username == username)
            )
            return result.scalars().first()
    async def get_by_email(self, email: str):
        async with self.async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(self.model.email == email)
            )
            return result.scalars().first()
    async def get_by_name(self, name: str):
        async with self.async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(self.model.name == name)
            )
            return result.scalars().first()
    
    async def get_all_name_by_rare(self, rare:str):
        async with self.async_session_maker() as session:
            result = await session.execute(select(self.model).where(self.model.rare == rare))
        return result.scalars().all()
    
    async def update_entity(self, id: uuid.UUID, data: Dict[str, Any]):
        async with self.async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(getattr(self.model, self._id_name) == id)
            )
            obj = result.scalars().first()
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                await session.commit()
                await session.refresh(obj)
            return obj
    
    async def delete_entity_by_id(self, id: uuid.UUID):
        async with self.async_session_maker() as session:
            result = await session.execute(
                select(self.model).where(getattr(self.model, self._id_name) == id)
            )
            obj = result.scalars().first()
            if obj:
                await session.delete(obj)
                await session.commit()
            return obj