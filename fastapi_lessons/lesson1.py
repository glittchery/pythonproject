from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class BookSchema(BaseModel):
    title: str
    author: str

books = [
    {
        "id": 1,
        "title": "Ассинхронность Python",
        "author": "Matthew",
    },
    {
        "id": 2,
        "title": "Backend разработка в Python",
        "author": "Артём",
    },
]


@app.get("/books",
         tags=["Книги"],
         summary="Получить все книги"
         )
def read_books():
    return books


# @app.get("/books/{book_id}",
#          tags=["Книги"],
#          summary="Получить выбранную книгу"
#          )
# def get_book(book_id: int):
#     for book in books:
#         if book["id"] == book_id:
#             return book
#     raise HTTPException(status_code=404, detail="Книга не найдена")



@app.put("/books/{book_id}")
def change_book(book_id: int, new_info: BookSchema):
    for book in books:
        if book["id"] == book_id:
            book["title"] = new_info.title
            book["author"] = new_info.author
            return {"success": True, "message": "Информация изменена успешно"}
    return HTTPException(status_code=404, detail="Книга не найдена")


@app.post("/books",
          tags=["Книги"],
          summary="Добавить книгу"
          )
def create_book(new_book: BookSchema):
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author,
    })
    return {"success": True, "message": "Книга успешно добавлена"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"success": True, "message": "Книга успешно удалена"}
    return HTTPException(status_code=404, detail="Книга не найдена")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
