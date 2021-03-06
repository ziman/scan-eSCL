# scan-eSCL

Scan from eSCL-enabled printers.

## Synopsis

```
usage: scan.py [-h] [-o OUTFILE] [-p PORT] [-c COLOR_MODE] scanner_ip

positional arguments:
  scanner_ip            IP address of the scanner

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file name [scan.jpg]
  -p PORT, --port PORT  http port [80]
  -c COLOR_MODE, --color-mode COLOR_MODE
                        Grayscale8 or RGB24 [RGB24]
```

## Motivation

I wanted to scan from my Canon Pixma TS5050. I found these two resources:

* http://testcluster.blogspot.com/2014/03/scanning-from-escl-device-using-command.html

* https://github.com/kno10/python-scan-eSCL

However, I found the Python script too complicated for my needs; I know the IP
address of my printer and I don't need zeroconf and all the automagic.
Furthermore, I wanted a tidier, more up-to-date Python 3 script.

## Protocol description

It's cool you can have a RESTful interface to a scanner.

1. `POST` a `text/xml` to `/eSCL/ScanJobs` to create a scan job.
2. Receive `HTTP 201`, where the `Location` header gives you the job URL.
3. You can `DELETE` that job URL to cancel it.
4. You can `GET $job_url/NextDocument` to obtain a JPEG file.
   This automatically closes the job.

## License

3-clause BSD.
