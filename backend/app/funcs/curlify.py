"""
From https://github.com/ofw/curlify/blob/master/curlify.py
"""
from typing import Any, List, Tuple

import requests

from app.utils import overwrite_docker_url


def to_curl(
    request: requests.models.PreparedRequest,
    compressed: bool = False,
    verify: bool = True,
    overwrite_url: bool = True,
) -> str:
    """
    Returns string with curl command by provided request object
    Parameters
    ----------
    compressed : bool
        If `True` then `--compressed` argument will be added to result
    """
    parts: List[Tuple[Any, Any]] = [("curl", None), ("-X", request.method)]

    for k, v in sorted(request.headers.items()):
        parts += [("-H", "{0}: {1}".format(k, v))]

    if request.body:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        parts += [("-d", body)]

    if compressed:
        parts += [("--compressed", None)]

    if not verify:
        parts += [("--insecure", None)]

    url = request.url
    if overwrite_url:
        url = overwrite_docker_url(url)
    parts += [(None, url)]

    flat_parts: List[Any] = []
    for k, v in parts:
        if k:
            flat_parts.append(k)
        if v:
            flat_parts.append("'{0}'".format(v))

    return " ".join(flat_parts)
