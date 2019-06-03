#! /usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  10/03/2016
#-----------------------------------------------------------------------------
""" class cocotbify
"""
import sys
import getopt

TIMESCALE = "`timescale 1ps/1ps"


def usages():
    """ print usages """
    print("Usages:")
    print("cocotbify.py [options]")
    print("-h, --help     print this help")
    print("-v, --verilog  verilog filename to modify")

def topname(filename):
    """ top module name is the last in file """
    lines = []
    with open(vfilename, 'rw') as vfile:
       for line in vfile:
           if line[0:6] == "module":
               lines.append(line)
    return lines[-1].split('(')[0].split(' ')[-1]

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv:", ["help", "verilog"])
    except getopt.GetoptError:
        usages()
        sys.exit(2)

    if opts == []:
        usages()
        sys.exit(0)

    for opt, arg in opts:
        if opt in ["-v", "verilog"]:
            vfilename = arg
        else:
            usages()
            sys.exit(2)

    topname = topname(vfilename)

    with open(vfilename) as vfile:
        sourcefile = vfile.read().split('\n')

    if sourcefile[0] == TIMESCALE:
        raise Exception("Already cocotbifyied")

    cocotbstr = """
`ifdef COCOTB_SIM
initial begin
  $dumpfile ("%s.vcd");
  $dumpvars (0, %s);
  #1;
end
`endif
    """%(topname, topname)

    cocotbifyied = TIMESCALE + "\n" +\
                   "\n".join(sourcefile[:-2]) +\
                   "\n" + cocotbstr + "\n" +\
                   "endmodule"

    with open(vfilename, 'w') as vfile:
        vfile.write(cocotbifyied)
