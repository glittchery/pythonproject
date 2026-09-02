from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy import select


app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


class BookAddSchema(BaseModel):
    title: str
    author:str

class BookSchema(BookAddSchema):
    id: int

@app.post("/books")
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title = data.title,
        author = data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True, "message": "Книга успешно добавлена"}


class PaginationParams(BaseModel):
    limit: int = Field(5, ge=0, le=100, description="Количество эл-ов на странице")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")

PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]


@app.get("/books")
async def get_book(session: SessionDep, pagination: PaginationDep) -> list[BookSchema]:
    query = select(BookModel).limit(pagination.limit).offset(pagination.offset)
    result = await session.execute(query)
    return result.scalars().all()


