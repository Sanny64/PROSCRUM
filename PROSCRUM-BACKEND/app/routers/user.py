from fastapi import Response, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=list[models.UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    users = db.query(schemas.User).all()
    print(users)
    return users

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = schemas.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"result": new_user}

@router.get("/{id}", response_model=models.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.user_id != id and current_user.role_id < 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    
    user = db.query(schemas.User).filter(schemas.User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.user_id != id and current_user.role_id < 4:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    
    delete_query = db.query(schemas.User).filter(schemas.User.user_id == id)

    if delete_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_user(id: int, user: models.UserUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.user_id != id and current_user.role_id < 4:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    
    user_query = db.query(schemas.User).filter(schemas.User.user_id == id)

    updated_user = user_query.first()

    if updated_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    user_query.update(user.model_dump(), synchronize_session=False)

    db.commit()

    return {"result": user_query.first()}