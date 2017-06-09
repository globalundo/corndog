"""This module allows to access datadog metrics as Postgresql foreign table """
from multicorn import ForeignDataWrapper
from datadog import initialize, api
import time


class DatadogForeignDataWrapper(ForeignDataWrapper):
    """Main wrapper class for multicorn"""

    def __init__(self, options, columns):
        """Init columns and initialize datadog api connection"""
        super(DatadogForeignDataWrapper, self).__init__(options, columns)
        initialize(
            api_key=options['api_key'],
            app_key=options['app_key']
        )
        self.columns = columns

    def execute(self, quals, columns):
        """Parse postgresql query, fetch and yield the results from datadog"""

        # Default params
        params = {}
        params['scope'] = ''
        params['query'] = 'system.cpu.idle{*}'
        params['startdate'] = int(time.time()) - 3600
        params['enddate'] = params['startdate'] + 3600

        # Set assignment quals
        for qual in quals:
            if qual.operator == '=':
                params[qual.field_name] = qual.value

        results = api.Metric.query(
            start=params['startdate'],
            end=params['enddate'],
            query=params['query']
        )
        for series in results['series']:
            scope = series['scope']
            for timestamp, value in series['pointlist']:
                yield {
                    'timestamp': int(timestamp)//1000,
                    'value': value,
                    'startdate': params['startdate'],
                    'enddate': params['enddate'],
                    'query': params['query'],
                    'scope': scope,
                }

