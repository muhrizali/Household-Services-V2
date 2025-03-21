from apps import celery_app as app

@app.task
def hellow():
    return "Hello"

@app.task
def add(a, b):
    return a + b
