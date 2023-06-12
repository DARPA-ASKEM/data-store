#!/usr/bin/env bash


echo "Running migrations."
alembic -c migrate/alembic.ini upgrade head
echo "Completed Postgres migrations."

echo "Running Elasticsearch index build"
python migrate/start_elasticsearch.py

if [[ "$SEED_DATA" == "true" ]] ; then
  echo "Seeding Data"
  python migrate/seed_data.py
fi
# To Troubleshoot the migration container, uncomment the following lines:
#touch /logger.log
#tail -f /logger.log
echo "Booting TDS API."
exit 0
