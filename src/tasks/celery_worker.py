import random
import time
from celery import Celery, group  # , signature
from celery.utils.log import get_task_logger

from src.settings import config

celery = Celery("celery_app", broker=config.CELERY_BROKER)
celery.conf.update({'CELERY_RESULT_BACKEND': config.CELERY_RESULT_BACKEND})
# celery.conf.task_routes = {'src.tasks.celery_worker': {'queue': 'default_queue'}}
# celery.conf.task_default_queue = 'default_queue'
logger = get_task_logger(__name__)


class MyBaseClassForTask(celery.Task):
    autoretry_for = (Exception, KeyError, ValueError)  # will retry for only these exceptions
    # dont_autoretry_for = (SyntaxError, )
    retry_kwargs = {'max_retries': 10}
    retry_backoff = True  # retry after 2s, 4s, 8s, 16s
    countdown = 5
    task_time_limit = 60 * 60  # 1 hour
    task_soft_time_limit = 45 * 60  # 45 minutes

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        # exc (Exception) - The exception raised by the task.
        # args (Tuple) - Original arguments for the task that failed.
        # kwargs (Dict) - Original keyword arguments for the task that failed.
        """
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@celery.task
def error_handler(request, exc, traceback):
    logger.error('Task {0} raised exception: {1!r}\n{2!r}'.format(request.id, exc, traceback))


# , retry_kwargs={'max_retries': 7, 'countdown': 5}
@celery.task(bind=True, base=MyBaseClassForTask, on_failure=error_handler)
def process_data(self, data: dict):
    logger.info(f"Started: process_data - {data}")
    try:
        sleep = 30 * random.random()
        if sleep > 15:
            raise ValueError("TEST")
        time.sleep(sleep)
        return {"success": "ok", "sleep": round(sleep, 2), 'id': self.request.id, 'input_data': data}
    except Exception as e:
        logger.info(f"Error: process_data - {e}")
        logger.error(e)
        raise self.retry(exc=e, countdown=5)


@celery.task(bind=True, on_failure=error_handler)
def process_multiple(self, ):
    logger.info("Process bulk data: %s", self)
    # batches = [signature("process_data") for i in range(30)]
    # jobs = process_data.chunks(list(range(10)), 7).group()
    jobs = group([
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
        process_data.s(),
    ], link_error=error_handler.s(),
    )
    result = jobs.apply_async()
    logger.info("jobs, %r", jobs)
    return {"succes": "ok", "results": result}
