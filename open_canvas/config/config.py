from configparser import ConfigParser

config = ConfigParser()
config.read("config/config.ini")

DJANGO_SECTION = "django"
DEBUG_VALUE = config.getboolean(DJANGO_SECTION, "debug", fallback=False)
SECRET_KEY_VALUE = config.get(DJANGO_SECTION, "secret_key", raw=True)


def get_config_section_values(section):
    return (config.get(section, option) for option in config.options(section))


(
    DATA_WAREHOUSE_USERNAME,
    DATA_WAREHOUSE_PASSWORD,
    DATA_WAREHOUSE_SERVICE,
) = get_config_section_values("data_warehouse")
LIB_DIR = config.get("cx_oracle", "lib_dir")
PROD_URL, PROD_KEY, TEST_URL, TEST_KEY = get_config_section_values("canvas")
