from typing import Optional

from fastapi import FastAPI , Path, Query,HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date =published_date

class BookRequest(BaseModel):
    id: Optional[int]=Field(description='Id is not needed on create',default=None)
    #Yani bu şu demek pydantic book istek nesnemzie özel alan doğrulaması ekledik
    title: str = Field(min_length=3) #en az üç karakterden oluşması gerekiyor
    author: str = Field( min_length=1)
    description: str =Field(min_length=1,max_length=100)
    rating: int = Field(gt=-0, lt=6)
    published_date: int =Field(gt=1999,lt=2031)

    model_config ={
        "json_schema_extra":{
            "example":{
                "title":"A new book",
                "author":"codingwithnergiz",
                "description": "A new description of  book",
                "rating": 5

            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithnergiz', 'a very nice book', 5,published_date=2012),
    Book(2, 'Computer Science Pro', 'codingwithnergiz', 'a very nice book', 5,published_date=2012),
    Book(3, 'Computer Science Pro', 'codingwithnergiz', 'a very nice book', 5,published_date=2012),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#kitap kimliğine göre bir kitabı bulmamızı sağlayan yeni bir api uç noktası
@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id:int= Path(gt =0)):
    for book in BOOKS:
        if book.id ==book_id:
            return book
        raise HTTPException(status_code=404,detail="Item not found")


@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return =[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
        return  books_to_return

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))
    return new_book.__dict__


def find_book_id(book:Book):
  book.id =1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
  return book

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed =False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] =book
            book_changed=True
        if not book_changed:
            raise HTTPException(status_code=404,detail="Item not found")

@app.delete("books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed =False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed=True
            break
        if not book_changed:
           raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/published-date/{published_date}",status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date:int=Query(gt=1999,lt=2031)):
    books_filtered = [book.__dict__ for book in BOOKS if book.published_date == published_date]
    return books_filtered
