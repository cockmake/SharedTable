# celery -A celery_task worker -P eventlet -E
from celery import Celery
from celery.app.control import Control

from settings import BROKER, RESULT_BACKEND, CPU_CORES
from utils import send_email_to_user

celery_app = Celery('celery_app', broker=BROKER, backend=RESULT_BACKEND)
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    # 结果保存时间为1h
    result_expires=60 * 60,
    task_serializer='json',
    accept_content=['json'],  # 接受的内容类型
    result_serializer='json',
    timezone='Asia/Shanghai',  # 设置为上海时区
    enable_utc=False,  # 如果你想要使用本地时区而不是 UTC，设置为 False
    worker_concurrency=CPU_CORES,  # 根据CPU核心数调整
    task_acks_late=True,  # 确保任务不丢失
    worker_prefetch_multiplier=1,  # 根据任务类型调整预取数量
    task_soft_time_limit=20,  # 任务软时间限制
    task_time_limit=40,  # 任务硬时间限制
    worker_max_tasks_per_child=50,  # 每个worker执行50个任务后重启
    loglevel='WARNING',  # 设置日志级别 WARNING
    worker_redirect_stdouts_level='WARNING',  # 设置日志级别 WARNING
    worker_redirect_stdouts='celery.log',  # 日志文件为当前目录下的celery.log
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

