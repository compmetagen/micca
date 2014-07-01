## This code is written by Davide Albanese, <davide.albanese@gmail.com>
## Copyright (C) 2013 Fondazione Edmund Mach
## Copyright (C) 2013 Davide Albanese

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import os.path


def rfile(string):
    estring = os.path.expandvars(os.path.expanduser(string))
    if not os.path.isfile(estring):
        msg = "file %s doesn't exist or it is not a regular file" % string
        raise argparse.ArgumentTypeError(msg)
    return estring


def wfile(string):
    estring = os.path.expandvars(os.path.expanduser(string))
    d = os.path.dirname(os.path.abspath(estring))
    if not os.path.isdir(d):
        msg = "directory %s doesn't exist" % d
        raise argparse.ArgumentTypeError(msg)
    return estring


def wdir(string):
    estring = os.path.expandvars(os.path.expanduser(string))
    try: 
        os.makedirs(estring)
    except OSError:
        if not os.path.isdir(estring):
            msg = "directory %s cannot be created" % string
            raise argparse.ArgumentTypeError(msg)
    return estring
