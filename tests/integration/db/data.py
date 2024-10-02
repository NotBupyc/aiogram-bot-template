import random

from bot.database.models import User


TEST_USER = User(id=1, username="1")

LIST_TEST_USERS = [User(id=i, username=None if random.randint(1, 3) == 3 else str(i)) for i in range(100)]
