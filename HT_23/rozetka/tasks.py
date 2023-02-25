"""Tasks"""
from celery import shared_task

from rozetka.models import ScrapingTask
from rozetka.scrape import RozetkaAPI, DataBaseOperations


@shared_task
def send_ids_to_rozetka(product_id):
    """ "Process send id's and get products from rozetka"""
    tasks = ScrapingTask.objects.get(id=product_id).products_id.split("\n")
    list_tasks = [task.strip("\r") for task in tasks]
    api = RozetkaAPI().get_item_data
    all_products_data = [api(pid) for pid in list_tasks if api(pid)]
    ScrapingTask.objects.get(id=product_id).delete()
    DataBaseOperations().write_products_to_db(all_products_data)
