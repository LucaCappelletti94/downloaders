from typing import Union, List, Dict
import requests
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count
import os
import pandas as pd
from ..extractors import AutoExtractor
from ..utils import is_iterable


class BaseDownloader:
    """Base class for making downloaders."""

    def __init__(
        self,
        process_number: int = -1,
        block_size: int = 32768,
        auto_extract: bool = True,
        delete_original_after_extraction: bool = False,
        max_description_size: int = 50,
        cache: bool = True,
        target_directory: str = "downloads",
        description_pattern="Downloading to {}",
        crash_early: bool = True,
        verbose: int = 1
    ):
        """Create new BaseDownloader.

        Parameters
        ------------------
        process_number: int = -1,
            Number of processes to use.
            If the given number is -1, we use all the available processes.
        block_size: int = 32768,
            The dimension of the block size to download in stream.
        auto_extract: bool = True,
            Wether to automatically extract the encountered files.
        delete_original_after_extraction: bool = False,
            Wether to delete the downloaded file after extraction.
        max_description_size: int = 50,
            Maximum length of the description in the loading bar.
        cache: bool = True,
            Wether to use cache or not.
        target_directory: str = "downloads",
            Position where to store the downloaded files.
        description_pattern="Downloading to {}",
            Pattern to use for the loading bar description.
        crash_early: bool = True,
            Wether if the download should stop at the earliest crash.
        verbose: int = 1
            The level of verbosity.
            With level 1, the overall loading bar is showed.
            With level 2, also the download of each element is showed.
        """
        if not isinstance(process_number, int) or process_number == 0:
            raise ValueError(
                "The given process number is not a strictly positive integer."
            )
        self._process_number = process_number if process_number > 0 else cpu_count()
        self._block_size = block_size
        self._auto_extract = auto_extract
        self._max_description_size = max_description_size - \
            len(description_pattern)
        self._cache = cache
        self._target_directory = target_directory
        self._description_pattern = description_pattern
        self._crash_early = crash_early
        if isinstance(verbose, bool):
            verbose = int(verbose)
        self._verbose = verbose
        if self._process_number == 1 and self._verbose == 1:
            self._verbose = 2
        self._extractor = AutoExtractor(
            cache=self._cache,
            delete_original_after_extraction=delete_original_after_extraction
        )

    def destination_path(self, request: requests.Request, url: str) -> str:
        """Return path to where to store the file."""
        # TODO: extend this method to be more stable.
        file_name = request.headers.get('content-disposition', None)
        if file_name is None:
            file_name = url.split("/")[-1]
            file_name = file_name.split("?")[0]
        return os.path.join(
            self._target_directory,
            file_name
        )

    def build_loading_bar(self, file_size: int, path: str) -> "TQDM":
        """Return loading bar.

        Parameters
        ---------------------
        file_size: int,
            Size of the file in bytes.
        path: str,
            Path where the file is expected to be stored.

        Returns
        ---------------------
        TQDM loading bar.
        """
        if len(path) > self._max_description_size:
            path = "{}...{}".format(
                path[:self._max_description_size//2],
                path[-self._max_description_size//2:]
            )
        return tqdm(
            total=file_size,
            unit='iB',
            unit_scale=True,
            desc=self._description_pattern.format(path),
            dynamic_ncols=True,
            leave=False,
            disable=not self._verbose > 1
        )

    def is_cached(self, destination: str) -> bool:
        """Return boolean representing if given path is cached."""
        if not self._cache:
            return False
        return os.path.exists(destination) or self._extractor.can_extract(destination) and self._extractor.is_cached(
            self._extractor.destination_path(destination)
        )

    def _download(self, url: str, destination: str = None) -> Dict:
        """Download file at given url showing a loading bar.

        Parameters
        ----------------------
        url: str,
            The url from where to download the data.
        destination: str = None,
            The path where to store the data.
            If none, it is attempted to assign a proper one.

        Raises
        ----------------------
        ValueError,
            If the request has not a status code 200 (success).

        Returns
        ----------------------
        Dictionary with metadata relative to the download.
        """
        status_code = None
        file_size = None
        bar = None
        success = False
        cached = False
        exception = ""
        downloaded_file_size = 0
        extration_metadata = {}
        try:
            try:
                request = None
                if destination is None:
                    # If the destination was not given, we try to assign one by using
                    # the request metadata and the url.
                    request = requests.get(url, stream=True)
                    destination = self.destination_path(request, url)
                # If the file is not cached we proceed to the download.
                if not self.is_cached(destination):
                    # If the request object was not already constructed.
                    if request is None:
                        request = requests.get(url, stream=True)
                    # Get the status
                    status_code = request.status_code
                    # Obtain the file size
                    file_size = int(request.headers.get('content-length', 0))
                    # We create the loading bar object.
                    bar = self.build_loading_bar(file_size, destination)
                    # If the directory is not already built we create it.
                    directory = os.path.dirname(os.path.abspath(destination))
                    if directory:
                        os.makedirs(directory, exist_ok=True)
                    # If the user hits ctrl-c during the download we want
                    # to remove the partial downloaded file.
                    with open(destination, "wb") as f:
                        for data in request.iter_content(self._block_size):
                            data_block = len(data)
                            bar.update(data_block)
                            downloaded_file_size += data_block
                            f.write(data)
                    bar.close()
                    # If the request has failed, we remove the file.
                    if status_code != 200:
                        raise ValueError(
                            "Request to url {url} finished with status code {status}.".format(
                                url=url,
                                status=request.status_code
                            )
                        )
                    # If we have reached this point, than the download has
                    # been a success.
                    success = True
                else:
                    # If the file is cached we approximate the values by
                    # making some assumptions.
                    # First, if the file exists, then it was downloaded,
                    # hence the status code must have been 200.
                    status_code = 200
                    # The file size, if the download has not failed, must
                    # have the size of the downloaded file.
                    # Still, the file might have been removed in the meantime
                    # and still exists in its extracted form.
                    # If that is the case, we leave it to None.
                    if os.path.exists(destination):
                        file_size = os.path.getsize(destination)
                    # The downloaded file size, if the download has not failed,
                    # must have the size of the downloaded file.
                    downloaded_file_size = file_size
                    # The file has been loaded from the cache.
                    cached = True
                    # Since it is cached it is definitely a success
                    success = True
                if self._auto_extract and self._extractor.can_extract(destination):
                    extration_metadata = self._extractor.extract(
                        destination
                    )
            # If something fails, we remove the failed download.
            except (Exception, KeyboardInterrupt) as e:
                # If the download has crashed or has been interrupted
                # we have to remove the partially downloaded file.
                if os.path.exists(destination):
                    os.remove(destination)
                # If the bar was created we need to close it down.
                if bar is not None:
                    bar.close()
                raise e
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            # If the download has crashed and it is required to crash early
            # we raise the captured exception.
            if self._crash_early:
                raise e
            else:
                exception = str(e)
        # Compose the metadata dictionary.
        return {
            "status_code": status_code,
            "file_size": file_size,
            "downloaded_file_size": downloaded_file_size,
            "url": url,
            "destination": destination,
            "success": success,
            "cached": cached,
            "exception": exception,
            **{
                "extraction_{}".format(key): value
                for key, value in extration_metadata.items()
            }
        }

    def _download_wrapper(self, kwargs: Dict) -> Dict:
        """Method to wrap keywords call to _download method."""
        return self._download(**kwargs)

    def download(
        self,
        urls: Union[str, List[str]],
        paths: Union[str, List[str]] = None,
    ) -> pd.DataFrame:
        """Download file at given url showing a loading bar.

        Parameters
        ----------------------
        urls: Union[str, List[str]],
            The url(s) from where to download the data.
        paths: Union[str, List[str]] = None,
            The path(s) where to store the data.
            If none, it is attempted to assign a proper one.

        Raises
        ----------------------
        ValueError,
            If the request has not a status code 200 (success).

        Returns
        ----------------------
        Dataframe with report on the operations executed.
        """
        if isinstance(urls, str):
            urls = [urls]
        if is_iterable(urls):
            urls = list(urls)
        if paths is not None and isinstance(paths, str):
            paths = [paths]
        if is_iterable(paths):
            paths = list(paths)
        if isinstance(urls, list) and isinstance(paths, list) and len(urls) != len(paths):
            raise ValueError(
                "The urls and paths lists must have the same length."
            )
        # Use the minimum amount of processes.
        process_number = min(len(urls), self._process_number)
        # Create the tasks generator
        tasks = (
            dict(
                url=urls[i],
                destination=None if paths is None else paths[i]
            )
            for i in range(len(urls))
        )
        desc = "Downloading files"
        # If only one process is required, we don't create a Pool
        if process_number == 1:
            report = pd.DataFrame([
                self._download_wrapper(task)
                for task in tqdm(
                    tasks,
                    desc=desc,
                    dynamic_ncols=True,
                    disable=not self._verbose > 0 or len(urls) == 1,
                    total=len(urls),
                    leave=False
                )
            ])
        else:
            # Start the process pool
            with Pool(process_number) as p:
                # Execute the downloads and compose the report document.
                report = pd.DataFrame(tqdm(
                    p.imap(
                        self._download_wrapper,
                        tasks
                    ),
                    desc=desc,
                    dynamic_ncols=True,
                    disable=not self._verbose > 0,
                    total=len(urls),
                    leave=False
                ))
                # Clean up the pool
                p.close()
                p.join()
        # Return report
        return report
