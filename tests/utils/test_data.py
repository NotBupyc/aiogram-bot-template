from bot.database import models

from .updates import TEST_USER

_user = "test_user"


TEST_DB_USER = models.User(id=TEST_USER.id, username=TEST_USER.username)
