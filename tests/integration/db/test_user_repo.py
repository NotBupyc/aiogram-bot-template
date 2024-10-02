from bot.database import Repositories
from tests.integration.db.data import TEST_USER


async def test_get_user_by_id(repo: Repositories):
    us = await repo.users.create(id=TEST_USER.id, username=TEST_USER.username)

    user = await repo.users.get(TEST_USER.id)

    assert user is not None

    assert user.id == us.id
    assert user.username == us.username


async def test_get_user_by_username(repo: Repositories):
    users = await repo.users.get_users_by_username(TEST_USER.username)

    assert TEST_USER.id in [i.id for i in users]
