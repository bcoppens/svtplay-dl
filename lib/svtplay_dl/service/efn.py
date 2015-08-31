from __future__ import absolute_import
import re
import copy

from svtplay_dl.service import Service, OpenGraphThumbMixin
from svtplay_dl.fetcher.hls import HLS, hlsparse
from svtplay_dl.log import log


class Efn(Service, OpenGraphThumbMixin):
    supported_domains_re = ["www.efn.se"]

    def get(self, options):
        data = self.get_urldata()

        match = re.search('data-hls="([^"]+)"', self.get_urldata())
        if not match:
            log.error("Cant find video info")
            return

        streams = hlsparse(self.http.request("get", match.group(1)))
        if streams:
            for n in list(streams.keys()):
                yield HLS(copy.copy(options), streams[n], n)