from abc import ABC, abstractmethod
from typing import Type

from db.db import async_session_maker
from repositories.tasks import TasksRepository
from repositories.users import UsersRepository
from repositories.knows import KnowsRepository
from repositories.comments import CommentsRepository
from repositories.likes import LikesRepository
from repositories.feedback import FeedbackRepository


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    users: Type[UsersRepository]
    tasks: Type[TasksRepository]
    knows: Type[KnowsRepository]
    comments: Type[CommentsRepository]
    likes: Type[LikesRepository]
    feedback: Type[FeedbackRepository]
    
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.tasks = TasksRepository(self.session)
        self.knows = KnowsRepository(self.session)
        self.comments = CommentsRepository(self.session)
        self.likes = LikesRepository(self.session)
        self.feedback = FeedbackRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
