from datetime import datetime, timezone
from itertools import islice
from typing import Iterable

import click


def batched(iterable: Iterable, size: int) -> Iterable[tuple]:
    """
    Batches an iterable into chunks of at most size. This is literally just a copy of
    the python3.12 itertools.batched function, but we're running on <3.12, so we can't
    use it :(.

    :param iterable: the iterable to batch up
    :param size: the maximum size of the batches (the last batch may be smaller)
    :return: yields tuples
    """
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, size)):
        yield batch


def log(message: str, **kwargs):
    """
    Logs the given message using click.secho. All kwargs are passed through so refer to
    the click docs for information on how to use them.

    :param message: the message to print
    :param kwargs: the styling kwargs for click to use
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    click.secho(f"[{now}] {message}", **kwargs)
