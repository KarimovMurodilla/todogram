from schemas.knows import KnowsSchemaAdd
from utils.repository import AbstractRepository
from utils.unitofwork import IUnitOfWork


class KnowsService:
    async def add_know(self, uow: IUnitOfWork, know: KnowsSchemaAdd, user):
        knows_dict = know.model_dump()
        knows_dict['user_id'] = user.id
        knows_dict['first_name'] = user.first_name
        
        async with uow:
            know_id = await uow.knows.add_one(knows_dict)
            await uow.commit()
            return know_id

    async def get_knows(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            knows = await uow.knows.find_all_by(user_id=user_id)
            return knows
        
    async def get_all_knows(self, uow: IUnitOfWork):
        async with uow:
            knows = await uow.knows.find_all()
            return knows