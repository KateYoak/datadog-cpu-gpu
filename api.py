import os
from time import time

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_payload import MetricsPayload
from datadog_api_client.v1.model.point import Point
from datadog_api_client.v1.model.series import Series

configuration = Configuration(
    host = "https://api.datadoghq.com"
)
configuration.api_key['apiKeyAuth'] = 'd7462bee7cd1e9b787301c15fcd5ae30'
host = os.uname()[1]

def submit_metric(metric, type, tag, value):
    body = MetricsPayload(
        series=[
            Series(
                metric=metric,
                type=type,
                points=[Point([time(), value])],
                tags=[tag],
                host=host
            )
        ]
    )

    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.submit_metrics(body=body)

        print(metric, type, tag, value, response)

def start_timer():
    '''Start timer and return it, so submit_timer_metric can be called later.
       This is useful for the first call to this api package
    '''
    return time()

def submit_timer_metric(start_time, metric, type='guage', tag='test:cpu_gpu_data_science'):
    '''
        Given start time, submits the metric with the time interval.
        Returns the start time, i.e. starts the timer for the next submission
    '''
    submit_metric(metric, type, tag, time() - start_time)
    return time() 

