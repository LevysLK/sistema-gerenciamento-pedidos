from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]

APP_DIR = BASE_DIR / 'app'
DATA_DIR = BASE_DIR / 'data'
LOG_DIR = BASE_DIR / 'logs'
BACKUP_DIR = DATA_DIR / 'backups'

EXPORT_PRODUCT_JASON = DATA_DIR
REPOSITORY_PRODUCTS_JSON = DATA_DIR / 'products.json'
REPOSITORY_ORDERS_JSON = DATA_DIR / 'orders.json'

BACKUP_FILE = BACKUP_DIR / f'{datetime.now():%d-%m-%Y_%Hh%Mm}.json'

LOG_FILE = LOG_DIR / f'{datetime.now():%d-%m-%Y}.log'
