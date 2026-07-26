from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dal.repository.slug_repository import SlugRepository
from app.services.slug_links_service import SlugLinksService
from app.utlis.slug_generator import SlugGenerator


async def get_db_session(request: Request):
    session_factory = request.app.state.db.session_factory

    async with session_factory() as session:
        yield session

def get_slug_generator():
    return SlugGenerator()

def get_slug_repo(session: AsyncSession = Depends(get_db_session)):
    return SlugRepository(session)

def get_slug_service(
        slug_gen: SlugGenerator = Depends(get_slug_generator),
        slug_repo: SlugRepository = Depends(get_slug_repo)
):
    return SlugLinksService(slug_gen, slug_repo)