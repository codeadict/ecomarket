from __future__ import print_function

import datetime
from decimal import Decimal
import json
import logging
import tempfile

from dateutil.parser import parse as date_parse
from sailthru.sailthru_client import (
        SailthruClient as SailthruClientBase,
        get_signature_hash,
)

from django.conf import settings
from django.utils import timezone

from marketplace.models import Country

from mailing_lists.constants import BatchStatus
from mailing_lists.integrations.sailthru import SailthruError, ApiKeyNotSet

logger = logging.getLogger(__name__)


class ExportFailed(SailthruError):
    pass


class PollFailed(SailthruError):
    pass


def _encoder_default(obj):
    encoders = [
        ((datetime.date, datetime.datetime), lambda date: date.isoformat()),
        (Country, lambda country: country.title),
        (Decimal, lambda number: str(number)),
    ]
    for types, encoder in encoders:
        if isinstance(obj, types):
            return encoder(obj)
    raise TypeError("Unable to serialise {}!".format(repr(obj)))


class SailthruClient(SailthruClientBase):

    def _prepare_json_payload(self, data):
        payload = {
            'api_key': self.api_key,
            'format': 'json',
            'json': json.dumps(data, default=_encoder_default),
        }
        signature = get_signature_hash(payload, self.secret)
        payload['sig'] = signature
        return payload


class BatchJobAPI(object):

    def __init__(self, provider):
        if provider != "sailthru":
            raise NotImplementedError("Only Sailthru implemented at present")
        if settings.SAILTHRU_API_KEY in [None, '']:
            raise ApiKeyNotSet()
        self.api = SailthruClient(
            settings.SAILTHRU_API_KEY, settings.SAILTHRU_API_SECRET)

    def submit_job(self, job, json_output=None):
        with tempfile.NamedTemporaryFile(suffix=".txt") as fh:
            for item in job.get_data():
                subscribe = item.pop("subscribe", True)
                try:
                    st_item = {
                        "email": item.pop("email"),
                        "lists": item.pop("lists"),
                        "vars": item,
                    }
                except KeyError:
                    continue
                json_data = json.dumps(st_item, default=_encoder_default)
                print(json_data, file=fh)
                if json_output:
                    print(json_data, file=json_output)
            fh.seek(0)
            response = self.api.api_post("job", {
                "job": "update",
                # This looks a bit weird, but it's how the sailthru library
                # works
                "file": fh.name,
            }, ["file"])
        if not response.is_ok():
            error = response.get_error()
            raise ExportFailed(error.message, error.code)
        data = response.response.json
        # Sometimes we just get {'job': 'update'} from the backend
        # Other times we get {u'status': u'pending', u'update': [],
        #                     u'job_id': u'something', u'name': u'Bulk Update'}
        # Dunno why...
        job.status = BatchStatus.from_api_text(data.get("status", "pending"))
        job.remote_id = data.get('job_id')
        job.submitted = timezone.now()
        job.save()

    def check_status(self, job):
        response = self.api.api_get("job", {"job_id": job.remote_id})
        if not response.is_ok():
            error = response.get_error()
            raise PollFailed(error.message, error.code)
        data = response.response.json
        job.status = BatchStatus.from_api_text(data["status"])
        if "start_time" in data and data["start_time"]:
            # TODO: Is this wasteful? We should keep the start time the same
            # between local and remote...
            job.submitted = date_parse(data["start_time"])
        if "end_time" in data and data["end_time"]:
            job.completed = date_parse(data["end_time"])
        job.save()
        return job.status
