"""
tds.schema.provenance - API facing provenance schema
"""
import datetime
from enum import Enum
from typing import Dict, List, Optional, Type

from pydantic import BaseModel, Field

# pylint: disable=missing-class-docstring
from tds.db.helpers import (
    graph_appreviations,
    return_graph_relations,
    return_graph_types,
)

# graph_types=return_graph_types()


class Provenance(BaseModel):

    id: Optional[int] = None
    timestamp: datetime.datetime = datetime.datetime.now()
    relation_type: str
    left: int
    left_type: str
    right: int
    right_type: str
    user_id: Optional[int]
    concept: Optional[str]

    class Config:
        orm_mode = True


class NodeSchema(BaseModel):
    type: str
    id: int
    uuid: str


class ProvenancePayload(BaseModel):
    root_id: Optional[int] = Field(default=1)
    root_type: Optional[str] = Field(default="Publication")
    user_id: Optional[int]
    curie: Optional[str]
    edges: Optional[bool] = Field(default=False)
    nodes: Optional[bool] = Field(default=True)
    types: List[str] = Field(
        default=[
            type
            for type in return_graph_types()
            if type not in ["Concept", "ModelRevision", "Project"]
        ]
    )
    hops: Optional[int] = Field(default=15)
    limit: Optional[int] = Field(default=1000)
    verbose: Optional[bool] = Field(default=False)


provenance_type_to_abbr = graph_appreviations()


class ProvenanceSearchTypes(str, Enum):

    artifacts_created_by_user = "artifacts_created_by_user"
    child_nodes = "child_nodes"
    concept = "concept"
    concept_counts = "concept_counts"
    connected_nodes = "connected_nodes"
    derived_models = "derived_models"
    model_to_primitive = "model_to_primitive"
    parent_model_revisions = "parent_model_revisions"
    parent_models = "parent_models"
    parent_nodes = "parent_nodes"
