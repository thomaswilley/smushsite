import sys
import argparse
import os
from bs4 import BeautifulSoup
import datauri
import mimetypes

def generate_datauri_for_website(infile, path_prefix="", parser="html.parser", ignore_http_resources=True):
    # ignore_http_resources=False would downloading each locally as stage, converting it, etc. for now just ignore leave as todo.
    if not ignore_http_resources:
        raise NotImplementedError
        return None

    with open(infile, 'r') as f:
        content = f.read()

    soup = BeautifulSoup(content, parser)
    # process scripts
    scripts = soup.findAll('script')
    for obj in scripts:
        src_path = obj['src']
        if not src_path.startswith("http"): # for now assuming ignore_http_resources=True
            src_path = "{}{}".format(path_prefix, src_path)
            obj['src'] = datauri.generate_datauri_from_file(src_path)

    # todo: process tags: images, css, etc.
    return soup.decode('utf-8').replace('\n','')

def main():
    parser = argparse.ArgumentParser(description='Convert a static website into a Data URI (https://en.wikipedia.org/wiki/Data_URI_scheme)')
    parser.add_argument('infile')
    parser.add_argument('--path-prefix')
    args = parser.parse_args()

    prefix = args.path_prefix or ""
    sys.stdout.write(generate_datauri_for_website(args.infile, prefix) or "")

if __name__ == '__main__':
    main()
