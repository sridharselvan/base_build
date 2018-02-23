# -*- coding: utf-8 -*-

"""

    Module :mod:``


    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
from __future__ import absolute_import, unicode_literals
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
from celery import Celery
from celery import bootsteps
from kombu import Consumer, Exchange, Queue
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.environ import (
    get_rabbitmq_details,
    get_queue_details
)
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


RMQ_EXCHANGE_NAME = 'test_exchange'


class GeneralConsumerHelper(object):

    all_queues = get_queue_details()


class LoggerConsumer(bootsteps.ConsumerStep, GeneralConsumerHelper):

    def get_consumers(self, channel):

        _queue_name, _durable = self.__class__.all_queues['central_logger_queue']

        _durable = True if _durable == 'durable_true' else False

        queue = Queue(
            name=_queue_name,
            exchange=Exchange(RMQ_EXCHANGE_NAME),
            routing_key=_queue_name,
            durable=_durable
        )

        return [
            Consumer(
                channel,
                queues=[queue],
                callbacks=[self.on_publish],
                accept=['json']
            )
        ]

    def on_publish(self, body, message):
        print 'Received message: {0!r}'.format(body)
        message.ack()


class SchedulerConsumer(bootsteps.ConsumerStep, GeneralConsumerHelper):

    def get_consumers(self, channel):

        _queue_name, _durable = self.__class__.all_queues['scheduler_queue']

        _durable = True if _durable == 'durable_true' else False

        queue = Queue(
            name=_queue_name,
            exchange=Exchange(RMQ_EXCHANGE_NAME),
            routing_key=_queue_name,
            durable=_durable
        )

        return [
            Consumer(
                channel,
                queues=[queue],
                callbacks=[self.on_publish],
                accept=['json']
            )
        ]

    def on_publish(self, body, message):
        print 'Received message: {0!r}'.format(body)
        message.ack()


application =  Celery('celery_app', broker='amqp://', backend='amqp://', include=['celery_app.tasks'])

application.steps['consumer'].add(LoggerConsumer)
application.steps['consumer'].add(SchedulerConsumer)



#queue_name = 't_q' #get_queue_details()['central_logger_queue'][0]
#my_queue = Queue(queue_name, Exchange('exchange_a'), queue_name)
#app = Celery(broker='amqp://')
#
#class MyConsumerStep(bootsteps.ConsumerStep):
#
#    def get_consumers(self, channel):
#        return [Consumer(channel,
#                         queues=[my_queue],
#                         callbacks=[self.handle_message],
#                         accept=['json'])]
#
#    def handle_message(self, body, message):
#        print 'Received message: {0!r}'.format(body)
#        message.ack()
#
#import pdb; pdb.set_trace() ## XXX: Remove This
#app.steps['consumer'].add(MyConsumerStep)
#
#def send_me_a_message(who, producer=None):
#    with app.producer_or_acquire(producer) as producer:
#        producer.publish(
#            {'hello': who},
#            serializer='json',
#            exchange=my_queue.exchange,
#            routing_key=queue_name,
#            declare=[my_queue],
#            retry=True,
#            virtual_host='/'
#        )
#
#send_me_a_message('world!')
