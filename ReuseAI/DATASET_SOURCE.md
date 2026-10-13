# Real dataset source

Primary corpus: **CodeSearchNet**.

Official repository:
https://github.com/github/CodeSearchNet

Public Hugging Face mirror used by the downloader:
https://huggingface.co/datasets/Nan-Do/code-search-net-python

The Hugging Face dataset card describes this as the Python portion of CodeSearchNet, containing open-source functions with comments found at GitHub. It reports 455,243 training rows and fields including repository, path, function name, code, language, docstring, SHA, URL and partition.

Important: the generated local `component_id` values are local identifiers created by ReuseAI. They are not original CodeSearchNet IDs.

The downloader does not invent code or project names. If the network/dataset cannot be reached, it fails instead of creating placeholder rows.
