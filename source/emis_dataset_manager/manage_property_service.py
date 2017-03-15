#!/usr/bin/env python
import os.path
import sys
### import requests
try:
    # Python 3
    from urllib.parse import urlsplit
except ImportError:
    # Python 2
    from urlparse import urlsplit
import docopt
import lue
import manage_dataset


doc_string = """\
Manage the property service

usage:
    {command} <uri> (scan|remove) [<arguments>...]
    {command} --help

options:
    -h --help   Show this screen
    --version   Show version

Commands:
    scan    Scan files or directories and add property resources to service
    remove  Remove property resources

See '{command} help <command>' for more information on a specific
command.
""".format(
        command = os.path.basename(sys.argv[0]))


scan_doc_string = """\
Scan one or more files or directories for LUE datasets containing properties

usage:
    {command} <uri> scan [--rewrite_path=<pattern>] <file>...
    {command} <uri> scan --help

options:
    -h --help       Show this screen
    --rewrite_path=<pattern>  Replace prefix of certain paths

arguments:
    file    Names of files and/or directories to scan

This command scans datasets for properties. Properties found which are
not yet present in the service are added. Properties found which are
already present in the service are not touched. Properties present in
the service which are not in the scanned directory are also not touched.

The names of files and/or directories can be passed. Filenames must point
to LUE dataset. Directory-names must point to directories. All LUE datasets
present in the directory will be scanned.

Optionally, the prefix of dataset pathnames can be replaced by some
other prefix. This allows for scanning of local datasets that are
mounted into a container at some other path. To use this feature,
a <from_prefix>:<to_prefix> pattern must be passed.
""".format(
        command = os.path.basename(sys.argv[0]))


def scan(
        uri,
        argv):
    arguments = docopt.docopt(scan_doc_string, argv=argv)
    pathnames = arguments["<file>"]
    rewrite_path = arguments["--rewrite_path"]
    rewrite_path = [] if rewrite_path is None else rewrite_path.split(":")

    manage_dataset.scan(uri, pathnames, rewrite_path)


remove_doc_string = """\
Remove property resources

usage:
    {command} <uri> remove [<properties>...]
    {command} <uri> remove --help

options:
    -h --help       Show this screen
    properties      Properties to remove
""".format(
        command = os.path.basename(sys.argv[0]))


def remove(
        uri,
        argv):
    arguments = docopt.docopt(remove_doc_string, argv=argv)
    properties = arguments["<properties>"]

    ### response = requests.get(uri)

    ### if response.status_code != 200:
    ###     raise RuntimeError("cannot get collection of properties")

    ### parts = urlsplit(uri)
    ### uri = "{}://{}".format(parts.scheme, parts.netloc)
    ### available_properties = response.json()["properties"]
    ### properties_to_remove = []

    ### if not properties:
    ###     # Remove all properties.
    ###     properties_to_remove = available_properties
    ### else:
    ###     # Filter available properties by the ones passed in.
    ###     uris = [property["_links"]["self"] for property in \
    ###         available_properties]

    ###     for property_uri in properties:
    ###         idx = uris.index(property_uri)

    ###         if idx == -1:
    ###             raise RuntimeError("property to remove does not exist")

    ###         properties_to_remove.append(available_properties[idx])

    ### for property in properties_to_remove:
    ###     delete_uri = uri + property["_links"]["self"]
    ###     response = requests.delete(delete_uri)

    ###     if response.status_code != 204:
    ###         raise RuntimeError("cannot delete property")


if __name__ == "__main__":
    arguments = docopt.docopt(doc_string, version="0.0.0", options_first=True)
    uri = arguments["<uri>"]

    if arguments["remove"]:
        command = "remove"
    elif arguments["scan"]:
        command = "scan"

    argv = [uri] + [command] + arguments["<arguments>"]
    functions = {
        "remove": remove,
        "scan": scan,
    }

    status = 1

    try:
        functions[command](uri, argv)
        status = 0
    except SystemExit:
        raise
    except RuntimeError as exception:
        sys.stderr.write("{}\n".format(exception))

    # status = docker_base.call_subcommand(functions[command], uri, argv)

    sys.exit(status)
