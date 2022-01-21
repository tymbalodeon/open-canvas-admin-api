from canvasapi import Canvas
from config.config import PROD_KEY, PROD_URL, TEST_KEY, TEST_URL

from .constants import ACCOUNT


def get_canvas(test=False):
    return Canvas(TEST_URL if test else PROD_URL, TEST_KEY if test else PROD_KEY)


def get_account(test=False, account=None):
    return get_canvas(test).get_account(account if account else ACCOUNT)
