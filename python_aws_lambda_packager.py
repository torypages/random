#!/usr/bin/env python
import argparse
import os
import pip
import shutil
import subprocess
import tempfile
import sys

'''
This is a very simplified version of what is found here
https://github.com/nficano/python-lambda

It focuses on only creating a unit of self contained Python in the form of
a zip file, leaving out the parts regarding AWS Lambda.

The intention is still to use the compiled artifact with AWS Lambda.

It will look for a requirements file in the same directory as your main script.

By default the script will actually relaunch itself inside a virtualenv.
This is done to facilitate the installing of pip packages.
'''

def main(args):
    # Make sure paths are full paths.
    args.src = os.path.abspath(os.path.expanduser(args.src))
    if args.artifact_out:
        args.artifact_out = os.path.abspath(
            os.path.expanduser(args.artifact_out))

    # Keep note of current working directory.
    src_dir = os.path.dirname(args.src)

    # Set requirements file.
    requirements_file = 'requirements.txt'
    if args.requirements_file:
        requirements_file = args.requirements_file
    requirements_file = os.path.join(src_dir, requirements_file)

    # Use this for staging files prior to zipping.
    tmpdir = tempfile.mkdtemp()

    # Location of resulting zip file.
    module_name = args.src[len(src_dir) + 1:].split('.')[0]
    artifact_out = os.path.join(os.getcwd(), module_name)
    if args.artifact_out:
        out_artifact = args.artifact_out

    # Copy over script(s) to staging area.
    os.chdir(src_dir)
    for f in filter(lambda x: os.path.isfile(x), os.listdir(src_dir)):
        shutil.copy(f, tmpdir)

    # Install requirements into virtualenv / staging area.
    requirements = open(requirements_file, 'r')
    for requirement in requirements:
        requirement = requirement.strip()
        if not requirement:
            continue
        pip.main(['install', requirement, '-t', tmpdir, '--ignore-installed'])

    # Set the permissions.
    if args.permissions:
        subprocess.call(('chmod -R {} {}'.format(args.permissions,
                                                 tmpdir)).split())

    # Finally, make the archive.
    print("Creating zip", artifact_out)
    shutil.make_archive(artifact_out, 'zip', tmpdir)

    # Clean up after ourselves.
    shutil.rmtree(tmpdir)
    if args.virtualenv_clean:
        shutil.rmtree(args.virtualenv_clean)


def relaunch_in_virtualenv():
    # Create a temp virtual env and call this script again.
    tmpdir = tempfile.mkdtemp()
    cmd_str = 'virtualenv {}'.format(tmpdir)
    subprocess.call(cmd_str.split())
    this_script = os.path.abspath(__file__)
    python_exec = os.path.join(tmpdir, 'bin', 'python')
    args_str = ' '.join(sys.argv[1:])
    new_args = '--skip-virtualenv --virtualenv-clean={}'.format(tmpdir)
    args_str = '{} {}'.format(args_str, new_args)
    cmd_str = '{} {} {}'.format(python_exec, this_script, args_str)
    subprocess.call(cmd_str.split())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', required=True, type=str,
                        help='The main module of your script.')
    parser.add_argument('--requirements-file', required=False, type=str,
                        help='Python requirements file.')
    parser.add_argument('--artifact-out', required=False, type=str,
                        help='The resulting zip file. '
                             'Do not supply and extension.')
    parser.add_argument('--permissions', required=False, type=str,
                        help='Permissions to be used with chmod.')
    parser.add_argument('--skip-virtualenv', action='store_true',
                        help='Do not create a virtual env.')
    parser.add_argument('--virtualenv-clean', required=False, type=str,
                        default=True,
                        help='This path will be deleted/cleaned.')

    args = parser.parse_args()

    if not args.skip_virtualenv:
        relaunch_in_virtualenv()
    else:
        main(args)
