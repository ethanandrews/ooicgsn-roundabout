"""
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
"""

import factory
import random, string

from roundabout.parts.models import Part, PartType, Documentation, Revision

from faker import Faker
fake = Faker()

# Generate random Part Numbers in the correct format
def generate_part_number():
    return random.choice(string.digits) + '-' + random.choice(string.digits)


# Factories
class PartTypeFactory(factory.DjangoModelFactory):
    """
        Define Part Type Factory
    """
    class Meta:
        model = PartType


class PartFactory(factory.DjangoModelFactory):
    """
        Define Part Factory
    """
    part_number = factory.LazyFunction(generate_part_number)

    class Meta:
        model = Part
        django_get_or_create = ('part_number',)

    part_type = factory.SubFactory(PartTypeFactory)


class RevisionFactory(factory.DjangoModelFactory):
    """
        Define Revision Factory
    """
    class Meta:
        model = Revision

    part = factory.SubFactory(Part)


class DocumentationFactory(factory.DjangoModelFactory):
    """
        Define Documentatione Factory
    """
    class Meta:
        model = Documentation

    part = factory.SubFactory(Part)
