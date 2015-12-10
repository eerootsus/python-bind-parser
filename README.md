# Python BIND parser

Simple Python script to get an overview of which IP addresses are bound to which domain names.
This is a quick prototype so do not expect any performance or proper handling of different scenarios.

## Requirements
* Python 2.7
* [dnspython](http://www.dnspython.org)


## Usage
`python parse.py [filenames]`

For example: `python parse.py bind/*` or `python parse.py example.com`


## Output
Will produce a simple list into `stdout`:

```
93.184.216.34
    example.com
    www.example.com
```

## Limitations
* File names are used for top level domain, eg. a valid filename would be `example.com`
* A and CNAME records are parsed