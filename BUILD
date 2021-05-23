load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@pip//:requirements.bzl", "requirement")

py_binary(
  name = "dataflow",
  srcs = ["dataflow.py"],
  deps = [
    requirement("google-auth"),
    requirement("google-auth-httplib2"),
    requirement("google-api-core"),
    requirement("google-api-python-client"),
    requirement("python-dateutil"),
  ],
)
