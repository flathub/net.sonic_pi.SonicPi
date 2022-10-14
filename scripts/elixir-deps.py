#!/usr/bin/env python3

# How to generate the elixir-dependencies.json file (for new versions of Sonic Pi):
#
# Requirements:
#
# * A fress copy of Sonic Pi source code (from git or tarball) for the desired version
# * A working Elixir environment (check by running `mix`)
#
# Procedure:
# Change to the Sonic Pi directory and _from_there_, run this script, for example:
# `cd sonic-pi`
# `../net.sonic_pi.SonicPi/scripts/elixir-dependencies.py`
# Note that that will overwrite the files `cache.ets` and `sources/elixir-dependencies.json`.
# You shouldn't change those files manually (your changes will be lost).

import os
import shutil
import glob
import hashlib
import json
from pathlib import Path
from hashlib import sha256

# Change to the tau directory and get the dependencies
os.chdir('app/server/beam/tau')
os.environ["MIX_ENV"] = "prod"
os.environ["HEX_HOME"] = "./downloads"
os.system('mix deps.clean --all')
os.system('mix deps.get')
os.chdir('downloads')

flatpak_dir = Path(os.path.dirname(__file__)) / '..'
# Copy cache file
ets_file = flatpak_dir / 'cache.ets'
shutil.copy('cache.ets', ets_file)
print(f'{ets_file.resolve()} written.')

# Generate dependency list
dependencies = [
    {
            'type': 'file',
            'url': f'https://repo.hex.pm/tarballs/{os.path.basename(filename)}',
            'dest': ".hex/packages/hexpm",
            'sha256': hashlib.sha256(Path(filename).read_bytes()).hexdigest()
    } for filename in sorted(glob.glob('packages/**/*.tar'))
    ] + [{ 'type': 'file', 'path': 'cache.ets', 'dest': '.hex' }]

# Write it to the JSON file
json_file = flatpak_dir / 'sources' / 'elixir-dependencies.json'
json.dump(dependencies, open(json_file, 'w'), indent = 4)
print(f'{json_file.resolve()} written.')
