#!/usr/bin/env python3
#
# Based on https://github.com/kno10/python-scan-eSCL
# and http://testcluster.blogspot.com/2014/03/scanning-from-escl-device-using-command.html

import logging
import requests
import argparse
from urllib.parse import urljoin

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

XML_REQUEST = """
<?xml version="1.0" encoding="UTF-8"?>
<scan:ScanSettings xmlns:pwg="http://www.pwg.org/schemas/2010/12/sm" xmlns:scan="http://schemas.hp.com/imaging/escl/2011/05/03">
  <pwg:Version>2.0</pwg:Version>
  <pwg:ScanRegions>
    <pwg:ScanRegion>
      <pwg:Height>3300</pwg:Height>
      <pwg:ContentRegionUnits>escl:ThreeHundredthsOfInches</pwg:ContentRegionUnits>
      <pwg:Width>2550</pwg:Width>
      <pwg:XOffset>0</pwg:XOffset>
      <pwg:YOffset>0</pwg:YOffset>
    </pwg:ScanRegion>
  </pwg:ScanRegions>
  <pwg:InputSource>Platen</pwg:InputSource>
  <scan:ColorMode>%s</scan:ColorMode>
</scan:ScanSettings>
""".strip()

def main(args):
    http = requests.Session()

    scanner_url = 'http://' + args.scanner_ip
    if args.port != 80:
        scanner_url += ':' + str(port)

    resp = http.post(
        urljoin(scanner_url, 'eSCL/ScanJobs'),
        data=XML_REQUEST % args.color_mode,
        headers={'Content-Type': 'text/xml'},
    )
    resp.raise_for_status()

    # status code is 201 so Requests won't follow Location
    # we just retrieve it from resp.headers
    result_url = urljoin(resp.headers['Location'] + '/', 'NextDocument')
    log.debug("Final document at: %s", result_url)

    resp = http.get(result_url)
    resp.raise_for_status()

    log.info("Scanning to: %s", args.outfile)
    with open(args.outfile, 'wb') as f:
        f.write(resp.content)

    log.info("Done!")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--outfile', default='scan.jpg', help='output file name [%(default)s]')
    ap.add_argument('-p', '--port', default=80, help='http port [%(default)s]')
    ap.add_argument('-c', '--color-mode', default='RGB24', help='Grayscale8 or RGB24 [%(default)s]')
    ap.add_argument('scanner_ip', help='IP address of the scanner')
    main(ap.parse_args())
