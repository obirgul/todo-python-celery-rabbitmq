# from typing import Optional
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from src.common.schemas import MMRInputSchema
from src.tasks.celery_worker import celery, process_data  # , process_multiple
from src.settings import logger

router = APIRouter()


@router.get("/tasks/{task_id}")
def tasks(task_id):
    task = celery.AsyncResult(task_id)
    logger.info("Started: TaskStatusAPI")
    state = task.state
    logger.info("Task: state: %r", state)
    if state == 'PENDING':
        response = {'queue_state': state, 'status': 'Process is ongoing...'}
    elif state == 'SUCCESS':
        response = {'queue_state': state, 'result': task.wait()}
    else:
        response = {'queue_state': state, 'result': task.wait()}
    return response


@router.post("/data_processing")
def data_processing(req: MMRInputSchema):
    data = jsonable_encoder(req)
    logger.info("Started: DataProcessingAPI")
    task = process_data.delay(data)

    logger.info("Task: %s", task)
    return {'task_id': task.id, 'status': 'Process is ongoing...', 'input': req.json()}
