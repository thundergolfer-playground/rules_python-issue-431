load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@pip//:requirements.bzl", "requirement")

py_library(
  name = "dataflow",
  srcs = ["dataflow.py"],
  deps = [
    requirement("google-auth"),
    requirement("google-auth-httplib2"),
    requirement("google-api-core"),
    requirement("google-api-python-client"),
    requirement("python-dateutil"),
  ],
  visibility = [
    "//crestone/luigi:__subpackages__",
  ],
)

py_test(
  name = "dataflow_test",
  srcs = ["dataflow_test.py"],
  deps = [
    ":dataflow",
    "//crestone/testing:gcp_responses",
    requirement("absl-py"),
  ],
)

py_library(
  name = "secrets",
  srcs = ["secrets.py"],
  visibility = [
    "//crestone/pjm:__pkg__",
    "//crestone/yes_energy:__pkg__",
  ],
  deps = [
    requirement("google-auth"),
    requirement("google-cloud-secret-manager"),
  ],
)

py_test(
  name = "secrets_test",
  srcs = ["secrets_test.py"],
  deps = [
    ":secrets",
    requirement("absl-py"),
    requirement("google-auth"),
    requirement("google-cloud-secret-manager"),
  ],
)

py_library(
  name = "storage",
  srcs = ["storage.py"],
  visibility = [
    "//crestone/caching:__pkg__",
  ],
  deps = [
    "//crestone/yes_energy:csv_coder",
    requirement("google-auth"),
    requirement("google-cloud-storage"),
    requirement("pandas"),
  ],
)

py_test(
  name = "storage_test",
  srcs = ["storage_test.py"],
  deps = [
    ":storage",
    requirement("absl-py"),
    requirement("pandas"),
  ],
)

py_library(
  name = "transfer",
  srcs = ["transfer.py"],
  deps = [
    ":secrets",
    requirement("google-auth"),
    requirement("google-auth-httplib2"),
    requirement("google-api-python-client"),
    requirement("python-dateutil"),
    requirement("pytz"),
  ],
  visibility = [
    "//crestone/luigi:__subpackages__",
  ],
)

py_test(
  name = "transfer_test",
  srcs = ["transfer_test.py"],
  deps = [
    ":secrets",
    ":transfer",
    "//crestone/testing:gcp_responses",
    requirement("absl-py"),
  ],
)