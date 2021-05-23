from __future__ import absolute_import

import os
import re

from datetime import datetime
from enum import Enum
from typing import Dict, List

from dateutil import parser as date_parser
from google.auth import credentials
from googleapiclient import discovery

class JobStatus(Enum):
  """A summary of job states.

  https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.jobs#Job.JobStatus
  """
  UNKNOWN = 1
  SUCCESS = 2
  FAILURE = 3

class DataflowMonitor(object):
  """Interacts with Google Cloud dataflows."""

  def __init__(
      self, credentials: credentials.Credentials,
      project_id: str, template_dir: str):
    """Creates a monitor with application default credentials.

    More context on default credentials:
    https://github.com/googleapis/google-auth-library-python/blob/master/google/auth/_default.py#L222

    Args:
      credentials: Google credentials as returned by goog.auth.default()
      project_id: The GCP project ID where the job resides.
      template_dir: The GCS templates directory.
    """
    self._credentials = credentials
    self._project_id = project_id
    self._template_dir = template_dir
    self._client = discovery.build(
      'dataflow', 'v1b3', credentials=credentials, cache_discovery=False)

  def launch_dataflow(self, template_name: str) -> str:
    """Launches a Cloud Dataflow job from a template and returns the id.

    Args:
      template_name: The name of the template in GCS.

    Returns:
      The string ID of the started job.

    Raises:
      Raises an HTTPError if there is a problem finding the job.
    """
    template_path = os.path.join(self._template_dir, template_name)
    sanitized = re.sub(r'\W+', '', template_name).replace('_', '-')
    job_name = ('run-' + sanitized)[:32]
    response = self._client.projects().templates().launch(
      projectId=self._project_id,
      gcsPath=template_path,
      body={
        'jobName': job_name
      }).execute()
    return response['job']['id']

  def get_job_status(self, job_id: str) -> JobStatus:
    """Returns the state of the specific job.

    Args:
      job_id: The ID of the job to check on.

    Returns:
      A JobStatus enum.

    Raise:
      Raises an HTTPError if there is a problem finding the job.
    """
    response = self._client.projects().jobs().get(
      projectId=self._project_id,
      jobId=job_id).execute()
    state = response['currentState']
    if state == 'JOB_STATE_DONE':
      return JobStatus(2)
    elif state == 'JOB_STATE_FAILED' or state == 'JOB_STATE_CANCELLED':
      return JobStatus(3)
    return JobStatus(1)