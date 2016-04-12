# -*- coding: utf-8 -*-
"""backyard.models.initializedb."""
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    User,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: {0} <config_uri> [var=value]\n'
          '(example: {1} development.ini")'.format(cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        # each models configuration here.
        model = User(name='admin', email='admin@example.org')
        DBSession.add(model)
