from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models.user import User, UserCreate, UserResponse
from auth import verify_api_key

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a new user")
def create_user(user: UserCreate, session: Session = Depends(get_session),api_key: str = Depends(verify_api_key)):
    # check if the api key is valid
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    # check if the user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/", response_model=List[UserResponse], summary="Get all users")
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users