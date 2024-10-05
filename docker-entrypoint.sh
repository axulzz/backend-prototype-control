#!/bin/sh

python manage.py migrate
python manage.py loaddata fixtures/*.json

if [ ${DJANGO_ENV} == 'production' ]
then
  python manage.py collectstatic --noinput
  python manage.py compilemessages
else
  # then run the CMD passed as command-line arguments
  exec "$@"
fi