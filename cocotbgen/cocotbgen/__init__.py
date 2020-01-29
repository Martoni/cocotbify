#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  28/01/2020
#-----------------------------------------------------------------------------
#  Copyright (2020)  Armadeus Systems
#-----------------------------------------------------------------------------
""" cocotbgen
"""

import os
from os import path
import sys
from string import Template
import getopt

class CocoTBGen(object):
    """
    """
    COCOTBGENPATH = "" #TODO: manage this with correct installer
    TEMPLATES = {
            "Makefile": "Makefile",
            "testmodule": "test_MODULE.py"
            }
    def __init__(self, modulename, filename, simuname):
        fpath, fname = path.split(path.abspath(path.expanduser(filename)))
        self._filename = fname
        self._modulename = modulename
        self._filenamenoext = fname.split('.')[0]
        self._filepath = fpath
        self._pathlist = self._path_to_list(self._filepath)
        self._parse_project_path()
        # get project path root
        self._fullfilepath = path.join(fpath, fname)
        self._simuname = simuname
        self._pathwritten = []

    def _path_to_list(self, apath):
        if apath == '' or apath == '/' or path == '\\':
            return []
        else:
            rootpath, head = path.split(apath)
            return self._path_to_list(rootpath) + [head]
    def _parse_project_path(self):
        index = None
        for i in range(len(self._pathlist)):
            pl=self._pathlist
            if pl[i] == 'src' and pl[i+1] == 'main' and pl[i+2] == 'scala':
                index = i
                break
        if index is None:
            raise Exception(f"Wrong path {pl}")
        self._index = index
        self._rootproject = path.join(*pl[:i])
        self._packagepath = path.join(*pl[i+3:])

    def _get_template_dir(self):
        modulepath = path.split(__file__)[0]
        templatepath = path.split(modulepath)[0]
        return path.join("/", templatepath, "templates")

    def parse(self):
        if not os.access(self._fullfilepath, os.R_OK):
            raise Exception(f"Can't open {self._fullfilepath}")
        raise Exception(f"TODO: parse file {self._filename}")

    def generate_dirs(self):
        dirpath = self.get_dir_path()
        if not path.exists(dirpath):
            os.mkdir(dirpath)

    def get_dir_path(self):
        return path.join('/', self._rootproject, 'cocotb',
                self._packagepath, self._filenamenoext)

    def generate_makefile(self):
        tpdir = self._get_template_dir()
        mpath = path.join("/", tpdir, self.TEMPLATES['Makefile'])
        with open(mpath, 'r') as fp:
            maketemplate = fp.read()
        tmake = Template(maketemplate)
        packagesubpath="/".join(['..']*(len(self._pathlist)-self._index - 3))
        packagedir="/".join(self._pathlist[self._index+3:])
        packagename=".".join(self._pathlist[self._index+3:])
        subs = dict(simu=self._simuname,
                    modulename=self._modulename,
                    sourcename=self._filename,
                    packagesubpath=packagesubpath,
                    packagedir=packagedir,
                    filenamenoext=self._filenamenoext,
                    packagename=packagename
                    )
        astr = tmake.substitute(subs)
        makefilepath = os.path.join(self.get_dir_path(), 'Makefile')
        with open(makefilepath, 'w') as fp:
            fp.write(astr)
        print(f"Makefile generated in {makefilepath}")
        self._pathwritten.append(makefilepath)

    def generate_testfile(self):
        tpdir = self._get_template_dir()
        mpath = path.join("/", tpdir, self.TEMPLATES['testmodule'])
        with open(mpath, 'r') as fp:
            testmodule = fp.read()
        ttest = Template(testmodule)
        subs = dict(modulename=self._modulename)
        astr = ttest.substitute(subs)
        testpath = os.path.join(self.get_dir_path(), f"test_{self._filenamenoext}.py")
        with open(testpath, 'w') as fp:
            fp.write(astr)
        print(f"test_{self._filenamenoext}.py generated in {testpath}")
        self._pathwritten.append(testpath)

    def generate_files(self):
        self.generate_dirs()
        self.generate_makefile()
        self.generate_testfile()

    def git_add(self):
        import subprocess
        for apath in self._pathwritten:
            dirpath, filename = path.split(apath)
            subprocess.run(["git", "add", filename], cwd=dirpath)
            print(f"file {filename} added in git")


def usages():
    """ Display usages """
    print("Usage :")
    print("$ python3 cocotbgen [options]")
    print("-h, --help              print this usage message")
    print("-s, --simu=[icarus]     give simulator used (default Icarus)")
    print("-m, --modulename=MODULE give the module name")
    print("                        if name given, source will not be parsed")
    print("-f, --file=[filepath]   give filename [mandatory]")
    print("-g, --git=[y,n]         set 'y' to git add file generated")

def main(argv):
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")
    try:
        opts, args = getopt.getopt(argv, "s:hf:g:m:",
                       ["simu=", "help", "file=", "git=", "modulename="])
    except getopt.GetoptError as err:
        print(err)
        usages()
        sys.exit(2)

    simuname = "icarus"
    filename = None
    gitopt = False
    modulename = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usages()
            sys.exit()
        elif opt in ("-s", "--simu"):
            simuname = arg
        elif opt in ("-f", "--file"):
            filename = arg
        elif opt in ("-g", "--git"):
            if arg == 'y':
                gitopt = True
        elif opt in ("-m", "--modulename"):
            modulename = arg

    if filename is None:
        usages()
        raise Exception("Give Chisel Scala source file name")

    extname = filename.split(".")[-1]
    if extname != "scala" :
        usages()
        raise Exception(f"Wrong file extension '.{extname}', should be '.scala'")

    ctbg = CocoTBGen(modulename, filename, simuname)
    if modulename is None:
        ctbg.parse()
    ctbg.generate_files()
    if gitopt:
        ctbg.git_add()

if __name__ == "__main__":
    main(sys.argv[1:])
