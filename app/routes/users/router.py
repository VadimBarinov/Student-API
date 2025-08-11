from fastapi import APIRouter, HTTPException, status, Response

from app.routes.users.auth import get_password_hash, authenticate_user, create_access_token
from app.routes.users.dao import UserDAO
from app.routes.users.schemas import SUserRegister, SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth",],
)


@router.post("/register/", summary="Регистрация пользователя")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            detail="Пользователь с таким E-mail уже существует",
            status_code=status.HTTP_409_CONFLICT,
        )
    user_dict = user_data.dict()
    user_dict["password"] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login/", summary="Авторизация пользователя")
async def auth_user(response: Response, user_data: SUserAuth) -> dict:
    check_user = await authenticate_user(email=user_data.email, password=user_data.password)
    if check_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная почта или пароль"
        )
    # Если данные пользователя получены, то генерируем JWT токен
    access_token = create_access_token({"sub": str(check_user.id)})
    # Записываем сгенерированный токен в куку
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}