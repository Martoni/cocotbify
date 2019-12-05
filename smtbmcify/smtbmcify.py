#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  04/12/2019
#-----------------------------------------------------------------------------
""" Adding formal rules to verilog generated module by chisel3
"""

import sys
import getopt


class DbgFormalParse(object):
    """ parsing class for dbgformal files
    """

    BEGIN="//BeginModule:"
    END="//EndModule:"

    def __init__(self, filename):
        self._filename = filename
        self._rulesdict = {}
        self._parse()

    def _parse(self):
        currentModule = None
        with open(self._filename) as fp:
            for line in fp:
                if line[0:len(self.BEGIN)] == self.BEGIN:
                    if currentModule is not None:
                        raise Exception(f"Parse error: no end module" +
                                        "line for {currentModule}")
                    currentModule = line.split(":")[1].strip()
                    if self._rulesdict.get(currentModule, None) is not None:
                        raise Exception("Only one module can be described")
                    self._rulesdict[currentModule] = ""
                if currentModule is not None:
                    self._rulesdict[currentModule] += line
                if line[0:len(self.END)] == self.END:
                    currentModule = None
    
    def get_module(self, modulename):
        return self._rulesdict.get(modulename, "")


class ModuleParse(object):
    MODULE="module"
    ENDMODULE="endmodule"

    def __init__(self):
        pass

    def parse_line(self, line):
        """ return line type:
        - module_begin
        - module_end
        - None
        """
        mtype=None
        if line[0:len(self.MODULE)] == self.MODULE:
            mtype="module_begin"
            module_name = line.strip().split(" ")[1].strip("(")
            return mtype, module_name
        if line[0:len(self.ENDMODULE)] == self.ENDMODULE:
            mtype="module_end"
            return mtype, None
        # default line
        return None, None

def usage():
    print("Usages:")
    print("$ python smtbmcify.py [options]")
    print("-h, --help             print this help message")
    print("-v, --verilog=module.v verilog module to read")
    print("-f, --formal=formal.sv formals rules")
    print("-o, --output=name.sv   output filename, default is moduleFormal.sv")
 

if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:f:o:",
                                   ["help", "verilog=",
                                    "formal=", "output="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    verilogfname = None
    formalfname = None
    outputfname = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ["-v", "--verilog"]:
            verilogfname = arg
        elif opt in ["-f", "--formal"]:
            formalfname = arg
        elif opt in ["-o", "--output"]:
            outputfname = arg
    if verilogfname is None:
        print("ERROR: Give verilog filename with -v option")
        usage()
        sys.exit()
    if formalfname is None:
        print("ERROR: Give Formal filename with -f option")
        usage()
        sys.exit()

    verilogname = verilogfname.split(".")[0]
    if outputfname is None:
        outputfname = verilogname + "Formal.sv"
    print(f"Generating file {outputfname}")
    dbgfparse = DbgFormalParse(formalfname)
    print(f"{len(dbgfparse._rulesdict)} module will be filled :")
    print("{}".format("\n".join(dbgfparse._rulesdict.keys())))
    mp = ModuleParse()

    with open(verilogfname, 'r') as vf:
        with open(outputfname, 'w') as of:
            module_parsed = None
            for line in vf:
                mtype, modulename = mp.parse_line(line)
                if module_parsed is None:
                    if mtype == "module_begin":
                        module_parsed = modulename
                    of.write(line)
                elif mtype == "module_end":
                    if module_parsed is not None:
                        text = dbgfparse.get_module(module_parsed)
                        of.write(text)
                        of.write(mp.ENDMODULE + "\n")
                    else:
                        of.write(line)
                    module_parsed = None
                else:
                    of.write(line)
