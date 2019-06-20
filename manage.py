"""Application entry point"""
from flask import jsonify
from redis.exceptions import ConnectionError

from config import AppConfig
from main import create_app, celery_app

# application object
app = create_app(AppConfig)


@app.route('/celery/health')
def celery_stats():
    """Tests that celery is up and running by checking
    if it has `sample_scheduler` scheduled as a task"""

    message = None
    inspector = celery_app.control.inspect()

    try:
        tasks = inspector.registered_tasks()
        message = {
            "tasks": tasks,
            "status": "Celery up",
        }
    except ConnectionError:
        message = {"status": "Redis server down"}
    except Exception:
        message = {"status": "Celery down"}

    return jsonify(dict(message=message)), 200


if __name__ == '__main__':
    app.run()
