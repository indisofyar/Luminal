from .base import *

import dj_database_url

DEBUG = False
DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}

CORS_ALLOWED_ORIGINS = [
    "https://luminal-rho.vercel.app",
]