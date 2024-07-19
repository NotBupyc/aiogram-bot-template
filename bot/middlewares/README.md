# Middlewares
### More about Middleware:

[DOC](https://docs.aiogram.dev/en/latest/dispatcher/middlewares.html)

[MasterGroosha Book](https://mastergroosha.github.io/aiogram-3-guide/filters-and-middlewares/)


## The list of pre-installed middleware
1. `ThrottlingMiddleware` - middleware for anti-flood. Working on `cachetools`
2. `GetRepo` - Create a sqlalchemy session and throws it into the handler.
example:
```python
from bot.database import Repositories
from aiogram import Router, types

router = Router()

@router.message(...)
async def example_handler(message: types.Message, repo: Repositories):
    user = repo.users.get_by_user_id(message.from_user.id)
    ...

```
3. `GetUser` - Get user from db and throws it into the handler. By default, each handler receives the user from the database.
```python
from bot.database.models import User

@router.message()
async def example_handler(message: types.Message, repo: Repositories, user: User):
    print(user)
    ...
3. ```
If the user is not required in the handler, set the flags to False
```python
@router.message(..., flags={'user': False})
async def example_handler(message: types.Message, repo: Repositories):
    ...
```
If you need to load sqlalchemy model relationships, use the user_options flag and pass the desired relationships in a list
```python
from sqlalchemy.orm import relationship

class User(BaseModel):
    ...
    relationhip = relationship(...)

@router.message(..., flags={'user_options': [User.relationhip]})
async def example_handler(message: types.Message, repo: Repositories, user: User):
    ...
```

4. `GetChat` - The same as with get User, but by default, each handler does not receive a chat from database
If you need a chat from the database in the handler:
```python
from bot.database.models import Chat
@router.message(..., flags={'chat': True})
async def example_handler(message: types.Message, repo: Repositories, chat: Chat):
    print(chat)
```
