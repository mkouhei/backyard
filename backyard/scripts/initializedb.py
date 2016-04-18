# -*- coding: utf-8 -*-
"""backyard.models.initializedb."""
import argparse

import transaction
from sqlalchemy import engine_from_config
from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )
from pyramid.scripts.common import parse_vars

from backyard.models.base import (
    DBSession,
    Base,
    )

from backyard.models.user import User


def parse_options():
    """parse options."""
    parser = argparse.ArgumentParser(description='help')
    parser.add_argument('config_uri',
                        help='configuration file; development.ini, etc.')
    parser.add_argument('options',
                        help='key=value options.',
                        action='store',
                        nargs='*')
    args = parser.parse_args()
    return args


def main():
    """main function."""
    args = parse_options()
    config_uri = args.config_uri
    options = parse_vars(args.options)
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        # each models configuration here.
        model = User(name='admin', email='admin@example.org')
        DBSession.add(model)
