from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import oauth2
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash
from sqlalchemy.orm import joinedload

router = APIRouter(tags=["Authentication"])
get_db = database.get_db


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.username == request.username)
        .first()
    )
    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials"
        )
    # generate a jwt token and return it
    access_token = token.create_access_token(data={"sub": user.username})
    # Inside your login endpoint function
    refresh_token = token.create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


# @router.get("/me", response_model=schemas.ShowUser)
# def get_current_user(
#     db: Session = Depends(get_db),
#     user: schemas.ShowUserOnly = Depends(oauth2.get_current_user),
# ):
#     # Query the database for the current user's details along with the contact details
#     me = (
#         db.query(models.User).filter(models.User.username == user.username)
#         .first()
#     )

#     # Check if the user was found
#     if not me:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Create ShowUser from the ORM model and add contact details
#     user_data = schemas.ShowUser.from_orm(me)
   
#     return user_data


@router.post("/refresh")
def refresh_token(refresh_request: schemas.RefreshToken, db: Session = Depends(get_db)):
    refresh_token = refresh_request.refresh_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = token.verify_refresh_token(refresh_token, credentials_exception)
    user = (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )
    access_token = token.create_access_token(data={"sub": username})
    # print(f"New access token: {access_token}")
    # print(token.verify_token(access_token, credentials_exception))
    # print(token.verify_refresh_token(refresh_token, credentials_exception))
    # print(username)
    return {"access_token": access_token, "token_type": "bearer"}
