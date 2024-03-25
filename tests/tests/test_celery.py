#Test celery

import pytest

from src.tasks import registry_task_test


@pytest.mark.celery(result_backend='redis://redis')
def test_celery(celery_app, celery_worker):
  '''Test task celery'''

  assert registry_task_test.delay(data={
    "email": "user_test_celery@mail.com",
    "password": "qweasd",
    "first_name": "string",
    "last_name": "string",
    "role": [
      "admin"
    ]
}).get(timeout=10) == None