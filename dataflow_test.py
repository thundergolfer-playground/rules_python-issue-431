from __future__ import absolute_import

from datetime import datetime
import os

from absl import flags
from absl.testing import absltest
from crestone.gcp import dataflow
from crestone.testing import gcp_responses
from unittest import mock
from urllib import error

class DataflowMonitorTest(absltest.TestCase):

  @mock.patch('googleapiclient.discovery.build')
  def test_launch_error_no_template(self, mock_api):
    creds = {}
    project_id = gcp_responses.PROJECT_ID
    projects = mock_api.return_value.projects
    launch = projects.return_value.templates.return_value.launch
    execute = launch.return_value.execute

    err = RuntimeError()
    execute.side_effect = [err]
    with self.assertRaises(RuntimeError):
      monitor = dataflow.DataflowMonitor(creds, project_id, 'gs://templates')
      monitor.launch_dataflow('fake_template')
    self.assertRegex(str(launch.call_args), 'run-fake-template')

  @mock.patch('googleapiclient.discovery.build')
  def test_launch_template(self, mock_api):
    creds = {}
    project_id = gcp_responses.PROJECT_ID
    projects = mock_api.return_value.projects
    launch = projects.return_value.templates.return_value.launch
    execute = launch.return_value.execute
    execute.return_value = gcp_responses.START_DATAFLOW_TEMPLATE_JOB_RESPONSE

    monitor = dataflow.DataflowMonitor(creds, project_id, 'gs://templates')
    job_id = monitor.launch_dataflow('fake_template')
    self.assertEqual(
      job_id, gcp_responses.START_DATAFLOW_TEMPLATE_JOB_RESPONSE['job']['id'])
    self.assertRegex(str(launch.call_args), 'run-fake-template')

  @mock.patch('googleapiclient.discovery.build')
  def test_get_job_status_error_no_job_id(self, mock_api):
    creds = {}
    project_id = gcp_responses.PROJECT_ID
    projects = mock_api.return_value.projects
    get = projects.return_value.jobs.return_value.get
    execute = get.return_value.execute

    err = RuntimeError()
    execute.side_effect = [err]
    with self.assertRaises(RuntimeError):
      monitor = dataflow.DataflowMonitor(creds, project_id, 'gs://templates')
      monitor.get_job_status('fake_job_id')
    self.assertRegex(str(get.call_args), 'fake_job_id')

  @mock.patch('googleapiclient.discovery.build')
  def test_get_job_status_running(self, mock_api):
    creds = {}
    project_id = gcp_responses.PROJECT_ID
    projects = mock_api.return_value.projects
    get = projects.return_value.jobs.return_value.get
    execute = get.return_value.execute
    execute.return_value = gcp_responses.DATAFLOW_RUNNING_RESPONSE

    monitor = dataflow.DataflowMonitor(creds, project_id, 'gs://templates')
    status = monitor.get_job_status('fake_job_id')
    self.assertEqual(dataflow.JobStatus(1), status)
    self.assertRegex(str(get.call_args), 'fake_job_id')

  @mock.patch('googleapiclient.discovery.build')
  def test_get_job_status_success(self, mock_api):
    creds = {}
    project_id = gcp_responses.PROJECT_ID
    projects = mock_api.return_value.projects
    get = projects.return_value.jobs.return_value.get
    execute = get.return_value.execute
    execute.return_value = gcp_responses.DATAFLOW_DONE_RESPONSE

    monitor = dataflow.DataflowMonitor(creds, project_id, 'gs://templates')
    status = monitor.get_job_status('fake_job_id')
    self.assertEqual(dataflow.JobStatus(2), status)
    self.assertRegex(str(get.call_args), 'fake_job_id')

  @mock.patch('googleapiclient.discovery.build')
  def test_get_job_status_failure(self, mock_api):
    creds = {}
    project_id = gcp_responses.PROJECT_ID
    projects = mock_api.return_value.projects
    get = projects.return_value.jobs.return_value.get
    execute = get.return_value.execute
    execute.return_value = gcp_responses.DATAFLOW_FAILED_RESPONSE

    monitor = dataflow.DataflowMonitor(creds, project_id, 'gs://templates')
    status = monitor.get_job_status('fake_job_id')
    self.assertEqual(dataflow.JobStatus(3), status)
    self.assertRegex(str(get.call_args), 'fake_job_id')


if __name__ == '__main__':
  absltest.main()