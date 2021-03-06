from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Connect Solutions",
    description="Fornece Api-Biblia para soluções Connect Church",
    version="1.0.1"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', tags=["Index"])
async def index():
    return{
        'Project': 'Connect Solutions - Api Biblia',
        'language': 'Python3.9.1',
        'Data': '21/02/2021',
        'Description': 'Fornecer Biblia para Connect Solutions, versões nvi e acf.',
        'endpoints': {
            'versions': 'https://connectsolutions.herokuapp.com/versions',
            'books': 'https://connectsolutions.herokuapp.com/${version}/books',
            'chapter': 'https://connectsolutions.herokuapp.com/${version}/${book_id}/chapters',
            'text': 'https://connectsolutions.herokuapp.com/${version}/${book_id}/${chapter}/',
            'searchText': 'https://connectsolutions.herokuapp.com/${searchText}'
        }
    }

@app.get('/nvi/')
async def nvi():
    return{
        'endpoints': {
            'versions': 'https://connectsolutions.herokuapp.com/versions',
            'books': 'https://connectsolutions.herokuapp.com/${version}/books',
            'chapter': 'https://connectsolutions.herokuapp.com/${version}/${book_id}/chapters',
            'text': 'https://connectsolutions.herokuapp.com/${version}/${book_id}/${chapter}/',
            'searchText': 'https://connectsolutions.herokuapp.com/${searchText}'
        }
    }

@app.get('/acf/')
async def acf():
    return{
        'endpoints': {
            'versions': 'https://connectsolutions.herokuapp.com/versions',
            'books': 'https://connectsolutions.herokuapp.com/${version}/books',
            'chapter': 'https://connectsolutions.herokuapp.com/${version}/${book_id}/chapters',
            'text': 'https://connectsolutions.herokuapp.com/${version}/${book_id}/${chapter}/',
            'searchText': 'https://connectsolutions.herokuapp.com/${searchText}'
        }
    }


@app.get('/versions', tags=["Versão"])
async def version():
    obj = [
        {
            'id':1,
            'version': 'nvi'
        },
        {
            'id':2,
            'version':'acf'
        }
    ]
    return obj

@app.get('/nvi/books/')
async def book(db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    books = db.query(models.Books)
    return books.all()


@app.get('/nvi/{book_id}/chapters')
async def chapter(book_id: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    chapter = db.query(models.Nvi.chapter).distinct(models.Nvi.chapter)

    if book_id:
        chapter = chapter.filter(models.Nvi.book_id == book_id)
    chapter = chapter.offset(offset).limit(limit).all()
    return chapter

@app.get('/nvi/{book_id}/{chapter}' )
async def text(book_id: int = None, chapter: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100 ):
    nvi = db.query(models.Nvi.text)

    if book_id:
        nvi = nvi.filter(models.Nvi.book_id == book_id)
    if chapter:
        nvi = nvi.filter(models.Nvi.chapter == chapter)
    nvi = nvi.offset(offset).limit(limit).all()
    return nvi

@app.get('/acf/books/')
async def book(db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    books = db.query(models.Books)
    return books.all()


@app.get('/acf/{book_id}/chapters')
async def chapter(book_id: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    chapter = db.query(models.Nvi.chapter).distinct(models.Nvi.chapter)

    if book_id:
        chapter = chapter.filter(models.Nvi.book_id == book_id)
    chapter = chapter.offset(offset).limit(limit).all()
    return chapter

@app.get('/acf/{book_id}/{chapter}' )
async def text(book_id: int = None, chapter: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100 ):
    nvi = db.query(models.Nvi.text)

    if book_id:
        nvi = nvi.filter(models.Nvi.book_id == book_id)
    if chapter:
        nvi = nvi.filter(models.Nvi.chapter == chapter)
    nvi = nvi.offset(offset).limit(limit).all()
    return nvi

@app.get('/search/{search}', tags=["Mecanismo de Busca"])
async def search_word(search: str = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 1000):

    busca = db.query(models.Nvi)
    if search:
        busca = busca.filter(models.Nvi.text.like('% '+search+' %'))        
        busca = busca.offset(offset).limit(limit).all()
        return busca
    return{'message': 'word search not passed to parameter.'}
    


""" 
@app.get('/nvi/books', tags=["Books - Versão NVI"])
async def books(db: Session = Depends(get_db)):
    books = db.query(models.Books)
    return books.all()


@app.get('/nvi/chapter', tags=["Chapter - Versão NVI"])
async def chapter(book_id: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    chapter = db.query(models.Nvi.chapter).distinct(models.Nvi.chapter)

    if book_id:
        chapter = chapter.filter(models.Nvi.book_id == book_id)

    chapter = chapter.offset(offset).limit(limit).all()

    if chapter == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return chapter


@app.get('/nvi', tags=["Text - Versão NVI"])
async def text(book_id: int = None, chapter: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    '''
        Atributos passado pelo Path:
        book_id,
        chapter,
    '''
    nvi = db.query(models.Nvi.text)

    if book_id:
        nvi = nvi.filter(models.Nvi.book_id == book_id)

    if chapter:
        nvi = nvi.filter(models.Nvi.chapter == chapter)

    nvi = nvi.offset(offset).limit(limit).all()

    if nvi == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return nvi


@app.get('/acf/books', tags=["Books - Versão ACF"])
async def books(db: Session = Depends(get_db)):
    books = db.query(models.Books)
    return books.all()


@app.get('/acf/chapter', tags=["Chapter - Versão ACF"])
async def chapter(book_id: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
    chapter = db.query(models.Nvi.chapter).distinct(models.Nvi.chapter)

    if book_id:
        chapter = chapter.filter(models.Nvi.book_id == book_id)

    chapter = chapter.offset(offset).limit(limit).all()

    if chapter == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return chapter


@app.get('/acf', tags=["Text - Versão ACF"])
async def text(book_id: int = None, chapter: int = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 100):

    nvi = db.query(models.Nvi.text)

    if book_id:
        nvi = nvi.filter(models.Nvi.book_id == book_id)

    if chapter:
        nvi = nvi.filter(models.Nvi.chapter == chapter)

    nvi = nvi.offset(offset).limit(limit).all()

    if nvi == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return nvi
 
@app.get('/search', tags=["Mecanismo de Busca"])
async def search_word(search: str = None, db: Session = Depends(get_db), offset: int = 0, limit: int = 1000):

    busca = db.query(models.Nvi)

    if search:
        busca = busca.filter(models.Nvi.text.like('% '+search+' %'))        
        busca = busca.offset(offset).limit(limit).all()
        return busca
    return{'message': 'word search not passed to parameter.'}
 
 """