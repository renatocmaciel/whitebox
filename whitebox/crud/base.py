from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from whitebox.core.db import Base
import datetime

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, _id: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == _id).first()

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_first_by_filter(self, db: Session, **kwargs: Any) -> Optional[ModelType]:
        return db.query(self.model).filter_by(**kwargs).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        date_now = datetime.datetime.utcnow()
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, created_at=date_now, updated_at=date_now)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_many(
        self, db: Session, *, obj_list: List[CreateSchemaType]
    ) -> List[ModelType]:
        date_now = datetime.datetime.utcnow()
        obj_list_in_data = jsonable_encoder(obj_list)
        db_obj_list = list(
            map(
                lambda x: self.model(**x, created_at=date_now, updated_at=date_now),
                obj_list_in_data,
            )
        )
        db.add_all(db_obj_list)
        db.commit()
        for obj in db_obj_list:
            db.refresh(obj)
        return db_obj_list

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        date_now = datetime.datetime.utcnow()
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        setattr(db_obj, "updated_at", date_now)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, _id: str):
        db.query(self.model).filter(self.model.id == _id).delete()
        db.commit()
        return
