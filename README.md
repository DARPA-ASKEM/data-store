# ASKEM Data Store API

## Usage

The API can be started by simply calling

```
docker compose up
```
(Please note that any changes in the `src/generated` directory
will forbid the API from starting.)

## Development

To simply start the server, run:
```
docker compose --profile dev up
```
which will also start a development instance of Postgres.

The server will not start if the generated model files are dirty i.e.
out of sync data model version or a non autogenerated change to the
file contents. (Version is tracked using the DBML project `Note`).

To generate new model files, run:
```
model-build generate ./askem.dbml ./src/generated
```

and check if they are valid by running

```
model-build check CURRENT_SEMANTIC_VERSION ./src/generated
```

If the tables don't exist yet it in Postgres, make sure to POST to the `/admin/db/init`
endpoint.

## ASKEM Data Model

![The generated graphic](./img/askem.png)

ERD was created using [DBML](https://www.dbml.org/home/) and rendered and edited using [dbdiagram](https://dbdiagram.io/)
