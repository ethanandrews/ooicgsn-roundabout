#!/bin/bash

# Copyright (C) 2019-2020 Woods Hole Oceanographic Institution
#
# This file is part of the Roundabout Database project ("RDB" or 
# "ooicgsn-roundabout").
#
# ooicgsn-roundabout is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# ooicgsn-roundabout is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ooicgsn-roundabout in the COPYING.md file at the project root.
# If not, see <http://www.gnu.org/licenses/>.


# Script to rebuild all Django containers and run migrate/collectstatic to deploy
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

if [ -e production.yml ]
then
    docker-compose -f production.yml up -d --no-deps --build django
    docker-compose -f production.yml run --rm django python manage.py migrate
    docker-compose -f production.yml run --rm django python manage.py collectstatic --noinput
fi

if [ -e production-demo-site.yml ]
then
    docker-compose -f production-demo-site.yml up -d --no-deps --build django_demo
    docker-compose -f production-demo-site.yml run --rm django_demo python manage.py migrate
    docker-compose -f production-demo-site.yml run --rm django_demo python manage.py collectstatic --noinput
fi

if [ -e production-generic-site.yml ]
then
    docker-compose -f production-generic-site.yml up -d --no-deps --build django_generic
    docker-compose -f production-generic-site.yml run --rm django_generic python manage.py migrate
    docker-compose -f production-generic-site.yml run --rm django_generic python manage.py collectstatic --noinput
fi

if [ -e production-rov-site.yml ]
then
    docker-compose -f production-rov-site.yml up -d --no-deps --build django_rov
    docker-compose -f production-rov-site.yml run --rm django_rov python manage.py migrate
    docker-compose -f production-rov-site.yml run --rm django_rov python manage.py collectstatic --noinput
fi
