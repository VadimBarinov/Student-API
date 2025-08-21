from fastapi import APIRouter, HTTPException, status, Response

from app.routes.users.auth import RefreshTokenSystem
from app.routes.users.dao import UserDAO
from app.dependencies import SessionDep, CurrentUser, CurrentAdminUser, RefreshTokenDep
from app.routes.users.rb import RBUpdateRolesToUserDep
from app.routes.users.schemas import SUserRegister, SUserAuth, SUserGet, SAddOrDeleteRoleToUser

router = APIRouter(
    prefix="/auth",
    tags=["Auth",],
)


@router.post("/register/", summary="Регистрация пользователя")
async def register_user(session: SessionDep, user_data: SUserRegister) -> dict:
    token_system = RefreshTokenSystem()
    user = await UserDAO.find_one_or_none(session=session, email=user_data.email)
    if user:
        raise HTTPException(
            detail="Пользователь с таким E-mail уже существует",
            status_code=status.HTTP_409_CONFLICT,
        )
    user_dict = user_data.model_dump()
    user_dict["password"] = token_system.get_password_hash(user_data.password)
    await UserDAO.add(session=session, **user_dict)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login/", summary="Авторизация пользователя")
async def auth_user(response: Response, session: SessionDep, user_data: SUserAuth) -> dict:
    token_system = RefreshTokenSystem()
    check_user = await token_system.authenticate_user(
        session=session,
        email=user_data.email,
        password=user_data.password
    )
    if check_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная почта или пароль"
        )
    # Если данные пользователя получены, то генерируем JWT токен
    token_pair = token_system.create_token_pair(check_user.id)
    # Записываем сгенерированный токен в куку
    for key, value in token_pair.items():
        response.set_cookie(key=key, value=value, httponly=True)
    return token_pair


@router.get("/refresh/", summary="Refresh access token")
async def refresh_access_token(response: Response, refresh_token: RefreshTokenDep) -> dict:
    token_system = RefreshTokenSystem()
    token_pair = token_system.refresh_access_token(refresh_token=refresh_token)
    # Обновляем токен в куки
    for key, value in token_pair.items():
        response.set_cookie(key=key, value=value, httponly=True)
    return token_pair


@router.get("/me/", summary="Получение данных о пользователе")
async def get_me(session: SessionDep, user_data: CurrentUser) -> SUserGet:
    return user_data


@router.post("/logout/", summary="Выйти из системы")
async def logout_current_user(response: Response) -> dict:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    response.delete_cookie(key="token_type")
    response.delete_cookie(key="expires_in")
    return {"message": "Пользователь успешно вышел из системы!"}


@router.post("/get_all_users/", summary="Получить всех пользователей. Доступно только для администратора")
async def get_all_users(session: SessionDep, user_data: CurrentAdminUser) -> list[SUserGet]:
    result = await UserDAO.find_all(session=session)
    return result


@router.post("/add_role_to_user/", summary="Добавить роль пользователю с указанным ID")
async def add_role_to_user(session: SessionDep, user_data: CurrentAdminUser, user: SAddOrDeleteRoleToUser) -> dict:
    result = await UserDAO.add_or_delete_role(
        session=session,
        user_id=user.user_id,
        role_name=user.role_name,
        new_value=True,
    )
    if result:
        return {"message": f"Роль {user.role_name} успешно добавлена пользователю с ID {user.user_id}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось добавить роль пользователю. Введены некорректные данные!"
        )


@router.delete("/delete_role_for_user/", summary="Удалить роль пользователю с указанным ID")
async def delete_role_from_user(session: SessionDep, user_data: CurrentAdminUser, user: SAddOrDeleteRoleToUser) -> dict:
    result = await UserDAO.add_or_delete_role(
        session=session,
        user_id=user.user_id,
        role_name=user.role_name,
        new_value=False,
    )
    if result:
        return {"message": f"Роль {user.role_name} успешно удалена у пользователя с ID {user.user_id}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить роль у пользователя. Введены некорректные данные!"
        )


@router.put("/update_all_user_roles/", summary="Изменить роли пользователя")
async def update_all_user_roles(session: SessionDep, user_data: CurrentAdminUser, user: RBUpdateRolesToUserDep) -> dict:
    result = await UserDAO.update(
        session=session,
        filter_by={"id": user.id},
        **user.to_dict(),
    )
    if result:
        return {"message": f"Роли успешно обновлены у пользователя с ID {user.id}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось обновить роли пользователя!"
        )
