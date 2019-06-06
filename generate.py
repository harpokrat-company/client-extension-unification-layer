#!/usr/bin/env python3

import argparse
import json
import shutil

template_values = {
    ''
}

def readfile(path: str) -> str:
    with open(path, 'r') as f:
        contents = f.read()
        return contents

def generate_chrome(project_path: str):
    chrome_out_path = "./chrome/"
    manifest_path = project_path + "/manifest.json"
    manifest_out_path = chrome_out_path + "/manifest.json"
    manifest_str = readfile(manifest_path)
    manifest = json.loads(manifest_str)
    try:
        manifest['background']['scripts'].append("browser-polyfill.js")
    except KeyError:
        print("missing background scripts definition")
    try:
        for i in manifest['content_scripts']:
            i['js'].append("browser-polyfill.js")
    except KeyError:
        print("missing content scripts definition")
    manifest_out_str = json.dumps(manifest, sort_keys=True, indent=4)
    popup_path = project_path + "/" + manifest['browser_action']['default_popup']
    popup_out_path = chrome_out_path + "/" + manifest['browser_action']['default_popup']
    popup_str = readfile(popup_path)
    popup_out_str = popup_str.replace('<script', '<script src"browser-polyfill.js"></script> <script')
    shutil.rmtree(chrome_out_path, True)
    shutil.copytree(project_path, chrome_out_path)
    shutil.copy("browser-polyfill.js", chrome_out_path + "/browser-polyfill.js")
    with open(popup_out_path, 'w') as f:
        f.write(popup_out_str)
    with open(manifest_out_path, 'w') as f:
        f.write(manifest_out_str)
    print("Generating chrome extension")

def generate_firefox():
    print("Generating firefox extension")

available_browsers = {
    'chrome': generate_chrome,
    # 'firefox': generate_firefox
}

def main():
    parser = argparse.ArgumentParser(description='Generate web extensions for a specified browser, using a given templated project. Used for HPK.')
    parser.add_argument('project_path', metavar='project_path', type=str, nargs=1, help='the path of the project to generate')
    parser.add_argument('browsers', metavar='browser', type=str, nargs='+', help='browser(s) to generate extension(s) for')
    args = parser.parse_args()
    for i in args.browsers:
        available_browsers[i](args.project_path[0])

    return 0

if __name__ == "__main__":
    exit(main())
