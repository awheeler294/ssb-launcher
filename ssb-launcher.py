#!/usr/bin/env python3
import argparse
import json
import os, os.path
import subprocess
import sys

parser = argparse.ArgumentParser(prog='ssb-launcher',
                                 description='''Launch a browser in single-site mode pointed at the provided URL.
                                                Currently only supports Chromium based browsers.
                                                Can customize the browser profile used, and the name of the process.''')
parser.add_argument('app_url',
                    help="url of app to run. Must be a full url, e.g. https://youtube.com")
parser.add_argument('-p', '--profile_name',
                    help="Name of the Chromium profile to use. If not specified it will use the last logged-in profile")
parser.add_argument('-b', '--browser', default="chromium-browser",
                    help="Browser executable to run. Default to chromium")
parser.add_argument('-n', '--process_name',
                    help="Name of the process. Default is the normal name of the browser process.")
parser.add_argument('-a', '--profile_path',
                    help="Full path to the directory containing the browser profiles. Defaults to $HOME/.config/chromium")
args = parser.parse_args()

app_url = args.app_url
profile_name = args.profile_name
browser_executable = args.browser
process_name = args.process_name
profile_path = args.profile_path

if not profile_path:
    home = os.environ["HOME"]
    profile_path = os.path.join(home, ".config", "chromium")

def read(f):
    with open(f) as src:
        data = json.loads(src.readline())
        return data.get('profile').get('name')

def get_profile_dir(profile_name, profile_path):
    for root, dirs, files in os.walk(profile_path):
        for f in files:
            if f.startswith("Preferences"):
                f = os.path.join(root, f)
                pr_name = read(f)
                if pr_name == profile_name:
                    pr_dir = root.split("/")[-1]
                    return pr_dir

command = "{}".format(browser_executable)

if profile_name:
    profile_dir = get_profile_dir(profile_name, profile_path)

    if not profile_dir:
        sys.exit("Could not find any profile named '{}' in path {}".format(profile_name, profile_path))

    command = "{} --profile-directory='{}'".format(command, profile_dir)

if process_name:
    command="exec -a {} {}".format(process_name, command)

command = "{} --app={}".format(command, app_url)

try:
    print("command: {}".format(command))
    subprocess.Popen(["/bin/bash", "-c", command])

except subprocess.CalledProcessError:
    pass
