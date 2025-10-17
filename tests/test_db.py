import pytest
import requests
from faker import Faker
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

import main
import models
from core.config import settings
from core.db_async import async_session

fake = Faker()

module_models = models
module_main = main
jsonplaceholder_url = (str(settings.jsonplaceholder.base_url))
users_data_url = 'users'
posts_data_url = 'posts'

pytestmark = pytest.mark.asyncio


def get_data(url):
    response = requests.get(url)
    return response.json()


@pytest.fixture(scope="module")
def users_data():
    return get_data(jsonplaceholder_url + users_data_url)


@pytest.fixture(scope="module")
def posts_data():
    return get_data(jsonplaceholder_url + posts_data_url)


def check_data_match(items_from_db, items_from_remote, args_mapping: dict):
    assert len(items_from_db) == len(items_from_remote)
    db_data = {
        item.id: [
            getattr(item, k)
            for k in args_mapping.keys()
        ]
        for item in items_from_db
    }
    remote_data = {
        item["id"]: [
            item[k]
            for k in args_mapping.values()
        ]
        for item in items_from_remote
    }
    assert db_data == remote_data


async def test_main(users_data, posts_data):
    await module_main.init_data()

    stmt_query_users = select(module_models.User).options(selectinload(module_models.User.posts))
    stmt_query_posts = select(module_models.Post).options(joinedload(module_models.Post.user))

    users = []
    posts = []

    async with async_session() as session:
        # there are problems with asyncio.gather in pytest :/
        # res_users, res_posts = await asyncio.gather(
        #     session.execute(stmt_query_users),
        #     session.execute(stmt_query_posts),
        # )
        res_users = await session.execute(stmt_query_users)
        res_posts = await session.execute(stmt_query_posts)

        users.extend(res_users.scalars())
        posts.extend(res_posts.scalars())

    assert len(posts) == len(posts_data)

    check_data_match(users, users_data, args_mapping=dict(
        full_name="name",
        username="username",
        email="email",
    ))
    check_data_match(posts, posts_data, args_mapping=dict(
        user_id="userId",
        title="title",
        body="body",
    ))

    for post in posts:
        # check relationships
        assert post.user in users
        assert post in post.user.posts
