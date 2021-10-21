from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
import requests

import db
import models
import twitter
import fb
import os

sched = BlockingScheduler()

def send_tg_alarm(message):
    requests.post(
            'https://api.telegram.org/bot{token}/sendMessage?chat_id={tui}&text={text}'.format(
                token=os.environ.get('ALLERT_BOT_TOKEN'),
                tui=os.environ.get('ADMIN_TUI'),
                text=message,
            ))

def pop_plus_item():
    with db.SessionLocal() as session:
        plus = session.query(models.PlusItem).first()
        if plus:
            session.delete(plus)
            session.commit()
            return plus.url, plus.discription, plus.image_url


def pop_premium_item():
    with db.SessionLocal() as session:
        premium = session.query(models.PremiumItem).first()
        if premium:
            session.delete(premium)
            session.commit()
            return premium.url, premium.discription, premium.image_url


@logger.catch
@sched.scheduled_job('cron', hour=13)
def plus_task_run():
    logger.info('Plus items sending') 
    plus_item = pop_plus_item()
    if not plus_item:
        return
    twitter.twi(*plus_item)
    fb.post(*plus_item)


@logger.catch
@sched.scheduled_job('cron', hour=15)
def premium_task_run():
    logger.info('Premium items sending') 
    premium_item = pop_premium_item()
    if not premium_item:
        return
    twitter.twi(*premium_item)
    fb.post(*premium_item)

if __name__ == "__main__":
    logger.add(sink=send_tg_alarm)
    sched.start()
