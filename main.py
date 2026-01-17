from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str

books = {
    1: {"title": "The Witcher", "author": "Sapkowski"},
    2: {"title": "Harry Potter", "author": "J.K. Rowling"}
}

@app.get("/books", response_model=dict[int, Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]

@app.post("/books", response_model=Book)
def create_book(book: Book):
    new_id = max(books.keys()) + 1
    books[new_id] = book.dict()
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated: Book):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    books[book_id] = updated.dict()
    return updated

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books.pop(book_id)
