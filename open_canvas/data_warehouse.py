from open_canvas.config.config import (
    DATA_WAREHOUSE_PASSWORD,
    DATA_WAREHOUSE_SERVICE,
    DATA_WAREHOUSE_USERNAME,
)
from cx_Oracle import connect


def get_data_warehouse_cursor():
    return connect(
        DATA_WAREHOUSE_USERNAME, DATA_WAREHOUSE_PASSWORD, DATA_WAREHOUSE_SERVICE
    ).cursor()
