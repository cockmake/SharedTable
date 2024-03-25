# celery -A celery_task worker -P eventlet
# -D 后台运行
# -E 在启动worker时开启事件监控
from celery import Celery
from celery.app.control import Control

from settings import BROKER, RESULT_BACKEND, CPU_CORES, RESULT_EXPIRES, TASK_SOFT_TIME_LIMIT, TASK_TIME_LIMIT, \
    WORKER_MAX_TASKS_PER_CHILD, LOGLEVEL, WORKER_REDIRECT_STDOUTS_LEVEL, WORKER_REDIRECT_STDOUTS, \
    WORKER_PREFETCH_MULTIPLIER
from utils import send_email_to_user

celery_app = Celery('celery_app', broker=BROKER, backend=RESULT_BACKEND)
celery_app.conf.update(
    worker_concurrency=CPU_CORES,  # 根据CPU核心数调整
    result_expires=RESULT_EXPIRES,
    task_soft_time_limit=TASK_SOFT_TIME_LIMIT,  # 任务软时间限制
    task_time_limit=TASK_TIME_LIMIT,  # 任务硬时间限制
    worker_max_tasks_per_child=WORKER_MAX_TASKS_PER_CHILD,  # 每个worker执行50个任务后重启
    loglevel=LOGLEVEL,  # 设置日志级别 WARNING
    worker_redirect_stdouts_level=WORKER_REDIRECT_STDOUTS_LEVEL,  # 设置日志级别 WARNING
    worker_redirect_stdouts=WORKER_REDIRECT_STDOUTS,  # 日志文件为当前目录下的celery.log
    worker_prefetch_multiplier=WORKER_PREFETCH_MULTIPLIER,  # 根据任务类型调整预取数量
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    accept_content=['json'],  # 接受的内容类型
    result_serializer='json',
    timezone='Asia/Shanghai',  # 设置为上海时区
    enable_utc=False,  # 如果你想要使用本地时区而不是 UTC，设置为 False
    task_acks_late=True,  # 确保任务不丢失

    # worker -P 使用eventlet线程池 'prefork' 适合cpu密集型 'eventlet' 适合io密集型
    # worker -E 开启监控
)
celery_controller = Control(celery_app)


@celery_app.task
def celery_send_email(user_email, subject, content):
    result = send_email_to_user(user_email, subject, content)
    if result:
        return "邮件发送成功"
    return "邮件发送失败"
