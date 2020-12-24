downloaders
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability|
|code_climate_maintainability| |pip| |downloads|

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

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes
get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

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

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/downloaders.png
   :target: https://travis-ci.org/LucaCappelletti94/downloaders
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_downloaders&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_downloaders
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_downloaders&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_downloaders
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_downloaders&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_downloaders
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/downloaders/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/downloaders?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/downloaders.svg
    :target: https://badge.fury.io/py/downloaders
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/downloaders
    :target: https://pepy.tech/project/downloaders
    :alt: Pypi total project downloads

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/35fb30e0228dbd2a03cc/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/downloaders/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/35fb30e0228dbd2a03cc/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/downloaders/test_coverage
    :alt: Code Climate Coverage
