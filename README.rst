downloaders
=========================================================================================
|pip| |downloads| |github|

Python package to handle the download of multiple types of files.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install downloaders

Usage examples
----------------------------------------------

.. code:: python

    from downloaders import BaseDownloader

    downloader = BaseDownloader()
    urls = [...]
    downloader.download(urls)


Troubleshooting
-----------------------------------------------

MacOS multiprocessing nightmare fuel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cupertino has a gift for us: somehow multiprocessing on MacOS in some specific
astral configurations that I have yet to fully understand, it will crash with the
following error:

.. code:: bash

    The process has forked and you cannot use this CoreFoundation functionality safely. You MUST exec().
    Break on __THE_PROCESS_HAS_FORKED_AND_YOU_CANNOT_USE_THIS_COREFOUNDATION_FUNCTIONALITY___YOU_MUST_EXEC__() to debug.

Apparently, this can be easily fixed by changing the way multiprocessing spawns
processes, that is:

.. code:: python

    import platform, multiprocessing

    if platform.system() == "Darwin":
        multiprocessing.set_start_method('spawn')

The aforementioned solution was proposed on `this StackOverflow question <https://stackoverflow.com/questions/30669659/multiproccesing-and-error-the-process-has-forked-and-you-cannot-use-this-corefou>`__.


.. |pip| image:: https://badge.fury.io/py/downloaders.svg
    :target: https://badge.fury.io/py/downloaders
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/downloaders
    :target: https://pepy.tech/project/downloaders
    :alt: Pypi total project downloads

.. |github| image:: https://github.com/lucacappelletti94/downloaders/actions/workflows/python.yml/badge.svg
    :target: https://github.com/lucacappelletti94/downloaders/actions
    :alt: Github Actions
