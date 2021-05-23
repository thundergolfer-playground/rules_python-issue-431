# rules_python-issue-431

[#431](https://github.com/bazelbuild/rules_python/issues/431)

> "ModuleNotFoundError when depending on multiple Google projects"

This reproduction repo is based off of https://github.com/JoshuaCrestone/RulesPythonImportIssues.

At the moment I can't reproduce the error. `bazel run //:dataflow` succeeeds.
