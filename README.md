# Downloaders

![PyPI version](https://badge.fury.io/py/downloaders.svg)
![Downloads](https://pepy.tech/badge/downloaders)
![GitHub Actions](https://github.com/lucacappelletti94/downloaders/actions/workflows/python.yml/badge.svg)

Python package to handle the download of multiple types of files.

## How do I install this package?

As usual, just download it using pip:

```shell
pip install downloaders
```

## Usage examples

```python
from downloaders import BaseDownloader

downloader = BaseDownloader()
urls = [...]
downloader.download(urls)
```

## Troubleshooting

### MacOS multiprocessing nightmare fuel

Cupertino has a gift for us: somehow, under certain specific astral configurations on MacOS (which I have yet to fully understand), multiprocessing will crash with the following error:

```bash
The process has forked and you cannot use this CoreFoundation functionality safely. You MUST exec().
Break on __THE_PROCESS_HAS_FORKED_AND_YOU_CANNOT_USE_THIS_COREFOUNDATION_FUNCTIONALITY___YOU_MUST_EXEC__() to debug.
```

Apparently, this can be easily fixed by changing the way multiprocessing spawns processes:

```python
import platform, multiprocessing

if platform.system() == "Darwin":
    multiprocessing.set_start_method('spawn')
```

The aforementioned solution was proposed on [this StackOverflow question](https://stackoverflow.com/questions/30669659/multiproccesing-and-error-the-process-has-forked-and-you-cannot-use-this-corefou).
