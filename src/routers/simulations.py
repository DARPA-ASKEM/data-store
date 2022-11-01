"""
router.simulations - does nothing yet
"""

from logging import Logger

from fastapi import APIRouter
from sqlalchemy.engine.base import Engine

logger = Logger(__file__)


def gen_router(engine: Engine, router_name: str) -> APIRouter:
    """
    Generate simulations router with given DB engine
    """
    router = APIRouter(prefix=router_name)

    @router.get("")
    def get_sims() -> str:
        """
        Mock simulations endpoint
        """
        logger.info(engine)
        return "SIMULATIONS NOT IMPLEMENTED!"

    return router
