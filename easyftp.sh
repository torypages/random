#!/bin/bash
set -e;

# I purposely do not clean this up. Footprint is incredibly minor and
# helps not wget from GitHub too much.
tmp_path="/tmp/easyftp-A071D9DA01C98556297DCCFD2F244hEQW4rWdRBs"
url_prefix="https://raw.githubusercontent.com/"
url_prefix=$url_prefix"torypages/pyftpdlib/easyftpscript-0.1/pyftpdlib/"
files=( "__init__.py"  "__main__.py" "_compat.py" "authorizers.py"
        "filesystems.py" "handlers.py" "ioloop.py" "log.py" "servers.py" )

export PYTHONPATH="$tmp_path:$PYTHONPATH"
orig_path=`pwd`

if [ ! -f $tmp_path ] && [ ! -d $tmp_path ]; then
  mkdir $tmp_path
fi

cd $tmp_path

if [ ! -f "pyftpdlib" ] && [ ! -d "pyftpdlib" ]; then
  mkdir "pyftpdlib";
fi

cd "pyftpdlib";

for i in "${files[@]}"; do
  if [ ! -f "$i" ] && [ ! -d "$i" ]; then
    wget "$url_prefix$i"
  fi
done

cd $orig_path
python2 -m pyftpdlib $@
