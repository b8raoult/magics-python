# (C) Copyright 2012-2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
#

import ctypes
import ctypes.util

import sys
import os

import numpy as np
from numpy.ctypeslib import ndpointer
from functools import partial

#
#  This Python interface needs to find the Magics library
#
#  We first search LD_LIBRARY_PATH. If you have strange behaviours,
#  check your $LD_LIBRARY_PATH.
#  This is only required on Linux! Therefore we do not have to check
#  on MacOS the DYLD_LIBRARY_PATH or for *.dylib.
#
lib = None
for directory in os.environ.get("LD_LIBRARY_PATH","").split(":"):
    fullname = os.path.join(directory,"libMagPlus.so")
    if os.path.exists(fullname):
        lib = fullname
        break

#
#  if not overwritten test if instlled version exist and use it
#
#if lib is None:
#    installname = "@CMAKE_INSTALL_PREFIX@/@INSTALL_LIB_DIR@/libMagPlus@CMAKE_SHARED_LIBRARY_SUFFIX@"
#    if os.path.exists(installname):
#        lib = installname

#
# If LD_LIBRARY_PATH does not contain path to Magics and it is not where you installed,
# we search the standard system locations
#
if lib is None:
    lib = ctypes.util.find_library("MagPlus")

# as last resort throw exception
if lib is None:
    raise Exception("Magics library could not be found")

dll  = ctypes.CDLL(lib)
#libc = ctypes.CDLL(ctypes.util.find_library("c"))


#def get_version():
#    return dll.getMagicsVersionString()


class FILE(ctypes.Structure):
    pass


FILE_p = ctypes.POINTER(FILE)

######################## String conversions ##########################

def _string_to_char(x):
    return x.encode()


def _char_to_string(x):
    return x.decode()


def _convert_strings(fn):

    convert = False

    for a in fn.argtypes:
        if a is c_char_p:
            convert = True

    if fn.restype is c_char_p:
        convert = True

    if not convert:
        return fn

    def wrapped(*args):

        new_args = []
        for a, t in zip(args, fn.argtypes):
            if t is c_char_p:
                a = string_to_char(a)
            new_args.append(a)

        r = fn(*new_args)
        if fn.restype is c_char_p:
            r = char_to_string(r)
        return r

    return wrapped

if sys.version_info[0] > 2:
    convert_strings = _convert_strings
    char_to_string = _char_to_string
    string_to_char = _string_to_char
else:
    convert_strings = lambda x: x
    char_to_string = lambda x: x
    string_to_char = lambda x: x





####################################################################
c_int = ctypes.c_int
c_int_p = ctypes.POINTER(c_int)

c_double = ctypes.c_double
c_double_p = ctypes.POINTER(c_double)

c_char = ctypes.c_char
c_char_p = ctypes.c_char_p

c_void_p = ctypes.c_void_p


####################################################################
def checked_error_in_last_paramater(fn):

    def wrapped(*args):
        err = c_int(0)
        err_p = ctypes.cast(ctypes.addressof(err), c_int_p)
        params = [a for a in args]
        params.append(err_p)

        result = fn(*params)
        if err.value:
            raise MagicsError(err)
        return result

    return wrapped


def checked_return_code(fn):

    def wrapped(*args):
        err = fn(*args)
        if err:
            raise MagicsError(err)

    return wrapped


####################################################################

def return_type(fn, ctype):

    def wrapped(*args):
        result = ctype()
        result_p = ctypes.cast(ctypes.addressof(result), ctypes.POINTER(ctype))
        params = [a for a in args]
        params.append(result_p)
        fn(*params)
        return result.value

    return wrapped

####################################################################

@checked_return_code
def init():
    return dll.mag_open()

####################################################################


@checked_return_code
def finalize():
    return dll.mag_close()

####################################################################

@checked_return_code
def coast():
    return dll.mag_coast()


####################################################################
@checked_return_code
def grib():
    return dll.mag_grib()

@checked_return_code
def get_version():
    return dll.getMagicsVersionString()


#metagrib = dll.mag_metagrib
#metagrib.restype = ctypes.c_char_p
#metagrib.argtypes = None


#metanetcdf = dll.mag_metanetcdf
#metanetcdf.restype = ctypes.c_char_p
#metanetcdf.argtypes = None


####################################################################

@checked_return_code
def cont():
    return dll.mag_cont()

####################################################################

@checked_return_code
def legend():
    return dll.mag_legend()


####################################################################

@checked_return_code
def odb():
    return dll.mag_odb()


####################################################################

@checked_return_code
def obs():
    return dll.mag_obs()


####################################################################

@checked_return_code
def raw():
    return dll.mag_raw()


####################################################################

@checked_return_code
def netcdf():
    return dll.mag_netcdf()

####################################################################

@checked_return_code
def image():
    return dll.mag_image()


####################################################################

@checked_return_code
def plot():
    return dll.mag_plot()

####################################################################

@checked_return_code
def text():
    return dll.mag_text()


####################################################################

@checked_return_code
def wind():
    return dll.mag_wind()


####################################################################

@checked_return_code
def line():
    return dll.mag_line()


####################################################################

@checked_return_code
def symb():
    return dll.mag_symb()


####################################################################

@checked_return_code
def boxplot():
    return dll.mag_boxplot()


####################################################################

@checked_return_code
def taylor():
    return dll.mag_taylor()

####################################################################

@checked_return_code
def tephi():
    return dll.mag_tephi()

####################################################################

@checked_return_code
def graph():
    return dll.mag_graph()


####################################################################

@checked_return_code
def axis():
    return dll.mag_axis()

####################################################################

@checked_return_code
def geo():
    return dll.mag_geo()


####################################################################

@checked_return_code
def mimport():
    return dll.mag_import()


####################################################################

@checked_return_code
def info():
    return dll.mag_info()


####################################################################

@checked_return_code
def minput():
    return dll.mag_input()


####################################################################

@checked_return_code
def eps():
    return dll.mag_eps()


####################################################################
###
###  Please note: these two functions changed compared to the previous SWIG based Python interface
###
@checked_return_code
def metgraph():
    return dll.mag_metgraph()


@checked_return_code
def epsinput():
    return  dll.mag_epsinput()

####################################################################
###
###  Please note: this function was called mmetbufr to the previous SWIG based Python interface
###
@checked_return_code
def metbufr():
    return dll.mag_metbufr()

####################################################################

@checked_return_code
def epsgraph():
    return dll.mag_epsgraph()


####################################################################

@checked_return_code
def epscloud():
    return dll.mag_epscloud()

####################################################################

@checked_return_code
def epslight():
    return dll.mag_epslight()


####################################################################

@checked_return_code
def epsplumes():
    return dll.mag_epsplumes()


####################################################################

@checked_return_code
def epswind():
    return dll.mag_epswind()


####################################################################

@checked_return_code
def epswave():
    return dll.mag_epswave()

####################################################################

@checked_return_code
def epsbar():
    return dll.mag_epsbar()

####################################################################

@checked_return_code
def epsshading():
    return dll.mag_epsshading()


####################################################################

@checked_return_code
def wrepjson():
    return dll.mag_wrepjson()

####################################################################

@checked_return_code
def geojson():
    return dll.mag_geojson()

####################################################################

@checked_return_code
def mapgen():
    return dll.mag_mapgen()


####################################################################

@checked_return_code
def mtable():
    return  dll.mag_table()

####################################################################

@checked_return_code
def seti(name, value):
    name = string_to_char(name)
    return dll.mag_seti(name, value)


####################################################################
@checked_return_code
def set1i(name,data):
#    array = np.empty((size,), dtype=np.float64)
#    array_p = array.ctypes.data_as(c_double_p)
#    _set1r(name, array_p, size)
    size = len(data)
    name = string_to_char(name)
    array_p = (ctypes.c_int * size)(*data)
    return dll.mag_set1i(ctypes.c_char_p(name), array_p, size)
    return None

####################################################################

array_2d_int = ndpointer(dtype=np.int,ndim=2, flags='CONTIGUOUS')
set2i = dll.mag_set2i
set2i.restype = None
set2i.argtypes = (c_char_p, array_2d_int, c_int, c_int)
set2i = convert_strings(set2i)

####################################################################

setr = dll.mag_setr
setr.restype = None
setr.argtypes = (c_char_p, c_double)
setr = convert_strings(setr)

####################################################################
@checked_return_code
def set1r(name,data):
    size = len(data)
    name = string_to_char(name)
    array_p = (ctypes.c_double * size)(*data)
    return dll.mag_set1r(ctypes.c_char_p(name), array_p, size)


####################################################################

array_2d_double = ndpointer(dtype=np.double,ndim=2, flags='CONTIGUOUS')
set2r = dll.mag_set2r
set2r.restype = None
set2r.argtypes = (c_char_p, array_2d_double, c_int, c_int)
set2r = convert_strings(set2r)

####################################################################

setc = dll.mag_setc
setc.restype = None
setc.argtypes = (c_char_p, c_char_p)
setc = convert_strings(setc)

####################################################################
@checked_return_code
def set1c(name,data):
    new_data=[]
    for s in data:
       new_data.append(string_to_char(s))
    name = string_to_char(name)
    data_p = (c_char_p * (len(new_data)))(*new_data)
    return dll.mag_set1c(ctypes.c_char_p(name), data_p, len(new_data))

####################################################################

#enqi = dll.mag_enqi
#enqi.restype  = c_int
#enqi.argtypes = (c_char_p,)

####################################################################

#enqr = dll.mag_enqr
#enqr.restype = c_double
#enqr.argtypes = (c_char_p,)

####################################################################

#enqc = dll.mag_enqc
#enqc.restype = None
#enqc.argtypes = (c_char_p,)
#enqc = convert_strings(enqc)

####################################################################

new_page = dll.mag_new
new_page.restype = None
new_page.argtypes = (c_char_p,)
new_page = convert_strings(new_page)

####################################################################

reset = dll.mag_reset
reset.restype = None
reset.argtypes = (c_char_p,)
reset = convert_strings(reset)

####################################################################

class MagicsError(Exception):

    def __init__(self, err):
        super(MagicsError, self).__init__("Magics Error - No Plot Produced!!! (%s)" % err)

####################################################################


#if __name__ == "__main__":
#    print "..."