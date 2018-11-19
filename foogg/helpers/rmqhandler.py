import requests
import pika
errs = (
    pika.exceptions.ConnectionClosed,
    pika.exceptions.ProbableAccessDeniedError
)


class RmqHandler:
    '''
    This class will automatically handle the reconnection issues and timeouts for you.
    Simply pass the queue name, with option to specify ip, port, password and user
    credentials if required.
    You can also ask for a prefetch count which by default is set to 1 to fetch one message
    from queue in one request
    '''

    def __init__(
            self, name, ip='127.0.0.1', pwd='guest',
            user='guest', port=5672, prefetch_count=1):

        self.QUEUE = name
        self.URI = f'http://{user}:{pwd}@{ip}:15672/api/queues/%2f/{name}'

        self.prefetch_count = prefetch_count
        pika_creds = pika.PlainCredentials(user, pwd)
        self._params = pika.connection.ConnectionParameters(
            host=ip,
            port=port,
            credentials=pika_creds
        )
        self._conn = None
        self._channel = None
        self.connect()

    @property
    def count(self):
        resp = requests.get(self.URI)
        resp = resp.json()
        return resp.get('messages', 0)

    def connect(self):
        if not self._conn or self._conn.is_closed:
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()
            self._channel.basic_qos(prefetch_count=self.prefetch_count)
            self._channel.queue_declare(
                self.QUEUE,
                durable=True
            )

    def _publish(self, job):
        self._channel.basic_publish(
            '',
            self.QUEUE,
            job
        )

    def seek_job(self):
        try:
            method, properties, job = self._channel.basic_get(
                queue=self.QUEUE
            )
        except errs:
            self.connect()
            method, properties, job = self._channel.basic_get(
                queue=self.QUEUE
            )

        if job:
            job = str(job, encoding='utf-8')
            try:
                self._channel.basic_ack(
                    delivery_tag=method.delivery_tag)
            except errs:
                self.connect()
                self._channel.basic_ack(
                    delivery_tag=method.delivery_tag)
        else:
            job = None
        return job

    def publish_job(self, job):
        """Publish job, will automatically reconnect if necessary."""

        try:
            self._publish(job)
        except:
            self.connect()
            self._publish(job)

    def close(self):
        if self._conn and self._conn.is_open:
            self._conn.close()
