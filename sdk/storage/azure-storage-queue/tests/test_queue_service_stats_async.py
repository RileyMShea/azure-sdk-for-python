# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import unittest
import asyncio

from azure.storage.queue.aio import QueueServiceClient
from azure.core.pipeline.transport import AioHttpTransport
from multidict import CIMultiDict, CIMultiDictProxy

from queuetestcase import (
    QueueTestCase,
    record,
    TestMode
)

SERVICE_UNAVAILABLE_RESP_BODY = '<?xml version="1.0" encoding="utf-8"?><StorageServiceStats><GeoReplication><Status' \
                                '>unavailable</Status><LastSyncTime></LastSyncTime></GeoReplication' \
                                '></StorageServiceStats> '


class AiohttpTestTransport(AioHttpTransport):
    """Workaround to vcrpy bug: https://github.com/kevin1024/vcrpy/pull/461
    """
    async def send(self, request, **config):
        response = await super(AiohttpTestTransport, self).send(request, **config)
        if not isinstance(response.headers, CIMultiDictProxy):
            response.headers = CIMultiDictProxy(CIMultiDict(response.internal_response.headers))
            response.content_type = response.headers.get("content-type")
        return response


# --Test Class -----------------------------------------------------------------
class QueueServiceStatsTestAsync(QueueTestCase):
    # --Helpers-----------------------------------------------------------------
    def _assert_stats_default(self, stats):
        self.assertIsNotNone(stats)
        self.assertIsNotNone(stats.geo_replication)

        self.assertEqual(stats.geo_replication.status, 'live')
        self.assertIsNotNone(stats.geo_replication.last_sync_time)

    def _assert_stats_unavailable(self, stats):
        self.assertIsNotNone(stats)
        self.assertIsNotNone(stats.geo_replication)

        self.assertEqual(stats.geo_replication.status, 'unavailable')
        self.assertIsNone(stats.geo_replication.last_sync_time)

    @staticmethod
    def override_response_body_with_unavailable_status(response):
        response.http_response.text = lambda: SERVICE_UNAVAILABLE_RESP_BODY

    # --Test cases per service ---------------------------------------

    async def _test_queue_service_stats_f(self):
        # Arrange
        url = self._get_queue_url()
        credential = self._get_shared_key_credential()
        qsc = QueueServiceClient(url, credential=credential, transport=AiohttpTestTransport())

        # Act
        stats = await qsc.get_service_stats()

        # Assert
        self._assert_stats_default(stats)

    @record
    def test_queue_service_stats_f(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_queue_service_stats_f())

    async def _test_queue_service_stats_when_unavailable(self):
        # Arrange
        url = self._get_queue_url()
        credential = self._get_shared_key_credential()
        qsc = QueueServiceClient(url, credential=credential, transport=AiohttpTestTransport())

        # Act
        stats = await qsc.get_service_stats(
            raw_response_hook=self.override_response_body_with_unavailable_status)

        # Assert
        self._assert_stats_unavailable(stats)

    @record
    def test_queue_service_stats_when_unavailable(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_queue_service_stats_when_unavailable())
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
