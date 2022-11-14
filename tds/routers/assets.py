"""
tds.router.models - crud operations for models
"""

import json
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from tds.autogen import orm
from tds.autogen.schema import ProjectAsset
from tds.db import (
    entry_exists,
    request_rdb,
)
from tds.operation import create, retrieve

logger = Logger(__name__)
router = APIRouter()


@router.get("")
def get_assets(count: int, rdb: Engine = Depends(request_rdb)):
    """
    Get a count of persons
    """
    print(count)
    with Session(rdb) as session:
        return (
            session.query(orm.ProjectAsset)
            .order_by(orm.ProjectAsset.id.asc())
            .limit(count)
            .all()
        )


@router.get("/{id}", **retrieve.fastapi_endpoint_config)
def get_project_asset(id: int, rdb: Engine = Depends(request_rdb)) -> ProjectAsset:
    """
    Retrieve model
    """
    if entry_exists(rdb.connect(), orm.ProjectAsset, id):
        with Session(rdb) as session:
            project_asset = session.query(orm.ProjectAsset).get(id)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ProjectAsset.from_orm(project_asset)


@router.post("", **create.fastapi_endpoint_config)
def create_asset(payload: ProjectAsset, rdb: Engine = Depends(request_rdb)) -> dict:
    """
    Create asset and return its ID
    """
    with Session(rdb) as session:
        asset_payload = payload.dict()
        print(asset_payload)
        # pylint: disable-next=unused-variable
        project_asset = orm.ProjectAsset(**asset_payload)
        print("here")
        print(project_asset)
        session.add(project_asset)
        session.commit()
        id: int = project_asset.id

    logger.info("new asset created: %i", id)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "location": f"/api/assets/{id}",
            "content-type": "application/json",
        },
        content=json.dumps({"id": id}),
    )
