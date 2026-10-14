"""Base repository with common database operations."""
from typing import Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
    
    async def create(self, **kwargs) -> ModelType:
        """Create a new record."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    async def get(self, id: Union[UUID, str, int]) -> Optional[ModelType]:
        """Get record by ID."""
        return await self.db.get(self.model, id)
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """Get all records with pagination."""
        result = await self.db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def update(self, id: Union[UUID, str, int], **kwargs) -> Optional[ModelType]:
        """Update a record."""
        instance = await self.get(id)
        if instance:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(instance, key, value)
            await self.db.commit()
            await self.db.refresh(instance)
        return instance
    
    async def delete(self, id: Union[UUID, str, int]) -> bool:
        """Delete a record."""
        instance = await self.get(id)
        if instance:
            await self.db.delete(instance)
            await self.db.commit()
            return True
        return False
    
    async def count(self) -> int:
        """Count total records."""
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar() or 0
