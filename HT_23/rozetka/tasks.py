"""Tasks"""
from celery import shared_task

from rozetka.models import ScrapingTask
from rozetka.scrape import RozetkaAPI, DataBaseOperations


@shared_task
def send_ids_to_rozetka(list_pid: list):
    """Process send id's and get products from rozetka"""
    api = RozetkaAPI().get_item_data
    all_products_data = [api(pid) for pid in list_pid if api(pid)]
    DataBaseOperations().write_products_to_db(all_products_data)
