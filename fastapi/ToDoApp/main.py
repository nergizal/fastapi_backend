from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,HTTPException,Path
from starlette import status

import models
from models import Todos


app = FastAPI()
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@app.get("/")
async def read_all(db:db_dependency):
    return db.query(Todos).all()



#Özet Akış
#Kullanıcı /todo/3 gibi bir URL ile GET isteği atar.
#FastAPI todo_id = 3 olarak alır ve db dependency’sini oluşturur.
#Veritabanında Todos.id == 3 sorgusu çalışır.
#Kayıt varsa → JSON olarak döner.
#Kayıt yoksa → 404 hatası döner.

@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async  def read_todo(db: db_dependency, todo_id:int = Path(gt=0)): #path doğrulama yapmaya yarar
#SQLAlchemy ile veritabanında sorgu yapılıyor:
#db.query(Todos) → Todos tablosunu sorgula
#.filter(Todos.id == todo_id) → Sadece id değeri URL’den gelen todo_id ile eşleşen kayıtları al
#.first() → Eğer bir kayıt varsa onu getir, yoksa None döner
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail='Todo not found')


@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency,todo_request: TodoRequest):
    todo_model =Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()

#PUT genellikle mevcut bir kaynağı güncellemek için kullanılır.
#URL içindeki {todo_id} → Hangi Todo kaydının güncelleneceğini belirtir.
#Endpoint başarılı olduğunda HTTP 204 dönecek.
#db: db_dependency → Daha önce tanımlanan dependency, veritabanı oturumunu sağlıyor.
#todo_id: int → URL’den gelen path parametresi. Hangi Todo kaydını güncelleyeceğimizi belirtir.
#todo_request: TodoRequest → Kullanıcının gönderdiği JSON verisini temsil eden Pydantic model.








@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_id: int, todo_request: TodoRequest):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

#Kullanıcının gönderdiği todo_request verileriyle mevcut veritabanı kaydını güncelliyoruz.
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete =todo_request.complete

    db.add(todo_model)
    db.commit()



@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,todo_id: int = Path(gt=0)):
    todo_model =db.query(Todos).filter(Todos.id== todo_id).first()
    if todo_model is None:
        raise
    HTTPException(status_code=404,detail='Todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
