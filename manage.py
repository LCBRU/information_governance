#!/usr/bin/env python
from dotenv import load_dotenv

# Load environment variables from '.env' file.
load_dotenv()

import os
from migrate.versioning.shell import main
from app.config import BaseConfig

if __name__ == "__main__":
    main(repository="migrations", url=BaseConfig.SQLALCHEMY_DATABASE_URI, debug="True")
