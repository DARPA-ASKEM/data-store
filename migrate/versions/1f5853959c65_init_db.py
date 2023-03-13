"""Init db

Revision ID: 1f5853959c65
Revises:
Create Date: 2023-02-22 14:12:14.238575

"""
# pylint: disable=no-member, invalid-name
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1f5853959c65"
down_revision = None
branch_labels = None
depends_on = None


# Alembic 1.9.4 does not support dropping enums on downgrade on autogen. So,
# ... we separate enum declarations from upgrade.
def drop_enums(*enums: sa.Enum):
    """
    Drop a list of enums
    """
    for enum in enums:
        enum.drop(op.get_bind(), checkfirst=True)


intermediate_source = sa.Enum("mrepresentationa", "skema", name="intermediatesource")
intermediate_format = sa.Enum(
    "bilayer", "gromet", "other", "sbml", name="intermediateformat"
)
resource_type = sa.Enum(
    "datasets",
    "intermediates",
    "models",
    "plans",
    "publications",
    "simulation_runs",
    name="resourcetype",
)
extracted_type = sa.Enum("equation", "figure", "table", name="extractedtype")
taggable_type = sa.Enum(
    "datasets",
    "features",
    "intermediates",
    "model_parameters",
    "models",
    "projects",
    "publications",
    "qualifiers",
    "simulation_parameters",
    "simulation_plans",
    "simulation_runs",
    name="taggabletype",
)
role = sa.Enum("author", "contributor", "maintainer", "other", name="role")
ontological_field = sa.Enum("obj", "unit", name="ontologicalfield")
resource_type = sa.Enum(
    "datasets",
    "intermediates",
    "models",
    "plans",
    "publications",
    "simulation_runs",
    name="resourcetype",
)
relation_type = sa.Enum(
    "BEGINS_AT",
    "CITES",
    "COMBINED_FROM",
    "CONTAINS",
    "COPIED_FROM",
    "DECOMPOSED_FROM",
    "DERIVED_FROM",
    "EDITED_FROM",
    "EQUIVALENT_OF",
    "EXTRACTED_FROM",
    "GENERATED_BY",
    "GLUED_FROM",
    "IS_CONCEPT_OF",
    "PARAMETER_OF",
    "REINTERPRETS",
    "STRATIFIED_FROM",
    "USES",
    name="relationtype",
)
provenance_type = sa.Enum(
    "Concept",
    "Dataset",
    "Intermediate",
    "Model",
    "ModelParameter",
    "ModelRevision",
    "Plan",
    "PlanParameter",
    "Project",
    "Publication",
    "SimulationRun",
    name="provenancetype",
)
value_type = sa.Enum("binary", "bool", "float", "int", "str", name="valuetype")


def upgrade() -> None:
    """
    Initialize tables as they were in v0.3.8
    """

    op.create_table(
        "active_concept",
        sa.Column("curie", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("curie"),
    )
    op.create_table(
        "intermediate",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "source",
            intermediate_source,
            nullable=False,
        ),
        sa.Column(
            "type",
            intermediate_format,
            nullable=False,
        ),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "model_framework",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("semantics", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "model_state",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("content", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "person",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("org", sa.String(), nullable=True),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("is_registered", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "publication",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("xdd_uri", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "software",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("storage_uri", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.Column(
            "resource_type",
            resource_type,
            nullable=True,
        ),
        sa.Column(
            "role",
            role,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["person.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dataset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("deprecated", sa.Boolean(), nullable=True),
        sa.Column("sensitivity", sa.Text(), nullable=True),
        sa.Column("quality", sa.Text(), nullable=True),
        sa.Column("temporal_resolution", sa.String(), nullable=True),
        sa.Column("geospatial_resolution", sa.String(), nullable=True),
        sa.Column("annotations", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("maintainer", sa.Integer(), nullable=False),
        sa.Column(
            "simulation_run", sa.Boolean(), server_default="False", nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["maintainer"],
            ["person.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "extraction",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("publication_id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            extracted_type,
            nullable=False,
        ),
        sa.Column("data", sa.LargeBinary(), nullable=False),
        sa.Column("img", sa.LargeBinary(), nullable=False),
        sa.ForeignKeyConstraint(
            ["publication_id"],
            ["publication.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "model_description",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("framework", sa.String(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("state_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["framework"],
            ["model_framework.name"],
        ),
        sa.ForeignKeyConstraint(
            ["state_id"],
            ["model_state.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "model_runtime",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("left", sa.String(), nullable=False),
        sa.Column("right", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["left"],
            ["model_framework.name"],
        ),
        sa.ForeignKeyConstraint(
            ["right"],
            ["model_framework.name"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "ontology_concept",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("curie", sa.String(), nullable=False),
        sa.Column(
            "type",
            taggable_type,
            nullable=False,
        ),
        sa.Column("object_id", sa.Integer(), nullable=False),
        sa.Column("status", ontological_field, nullable=False),
        sa.ForeignKeyConstraint(
            ["curie"],
            ["active_concept.curie"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "project_asset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.Column(
            "resource_type",
            resource_type,
            nullable=False,
        ),
        sa.Column("external_ref", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "provenance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "relation_type",
            relation_type,
            nullable=False,
        ),
        sa.Column("left", sa.Integer(), nullable=False),
        sa.Column(
            "left_type",
            provenance_type,
            nullable=False,
        ),
        sa.Column("right", sa.Integer(), nullable=False),
        sa.Column(
            "right_type",
            provenance_type,
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("concept", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["person.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "feature",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "value_type",
            value_type,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "model_parameter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "type",
            value_type,
            nullable=False,
        ),
        sa.Column("default_value", sa.String(), nullable=True),
        sa.Column("state_variable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["model_id"],
            ["model_description.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "qualifier",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "value_type",
            value_type,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "simulation_plan",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model_id", sa.Integer(), nullable=False),
        sa.Column("simulator", sa.String(), nullable=False),
        sa.Column("query", sa.String(), nullable=False),
        sa.Column("content", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["model_id"],
            ["model_description.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "qualifier_xref",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("qualifier_id", sa.Integer(), nullable=False),
        sa.Column("feature_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["feature.id"],
        ),
        sa.ForeignKeyConstraint(
            ["qualifier_id"],
            ["qualifier.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "simulation_run",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("simulator_id", sa.Integer(), nullable=False),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("success", sa.Boolean(), nullable=True),
        sa.Column("dataset_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("response", sa.LargeBinary(), nullable=True),
        sa.ForeignKeyConstraint(
            ["simulator_id"],
            ["simulation_plan.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "simulation_parameter",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column(
            "type",
            value_type,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["simulation_run.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """
    Drop all tables and enums (LOSSY)
    """
    op.drop_table("simulation_parameter")
    op.drop_table("simulation_run")
    op.drop_table("qualifier_xref")
    op.drop_table("simulation_plan")
    op.drop_table("qualifier")
    op.drop_table("model_parameter")
    op.drop_table("feature")
    op.drop_table("provenance")
    op.drop_table("project_asset")
    op.drop_table("ontology_concept")
    op.drop_table("model_runtime")
    op.drop_table("model_description")
    op.drop_table("extraction")
    op.drop_table("dataset")
    op.drop_table("association")
    op.drop_table("software")
    op.drop_table("publication")
    op.drop_table("project")
    op.drop_table("person")
    op.drop_table("model_state")
    op.drop_table("model_framework")
    op.drop_table("intermediate")
    op.drop_table("active_concept")
    drop_enums(
        intermediate_source,
        intermediate_format,
        resource_type,
        extracted_type,
        taggable_type,
        role,
        ontological_field,
        resource_type,
        relation_type,
        provenance_type,
        value_type,
    )
