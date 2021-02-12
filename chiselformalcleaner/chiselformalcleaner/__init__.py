""" class chiselformalcleaner
"""
import sys
import getopt

TIMESCALE = "`timescale 1ps/1ps"


DELETE_STRING = """  wire  ResetCounter_clock; // @[Formal.scala 14:36]
  wire  ResetCounter_reset; // @[Formal.scala 14:36]
  wire [31:0] ResetCounter_numResets; // @[Formal.scala 14:36]
  wire [31:0] ResetCounter_timeSinceReset; // @[Formal.scala 14:36]
  wire [31:0] TestCase_testCase; // @[Formal.scala 20:32]
  ResetCounter ResetCounter ( // @[Formal.scala 14:36]
    .clock(ResetCounter_clock),
    .reset(ResetCounter_reset),
    .numResets(ResetCounter_numResets),
    .timeSinceReset(ResetCounter_timeSinceReset)
  );
  TestCase TestCase ( // @[Formal.scala 20:32]
    .testCase(TestCase_testCase)
  );
  assign ResetCounter_clock = clock; // @[Formal.scala 15:25]
  assign ResetCounter_reset = reset; // @[Formal.scala 16:25]"""



def usages():
    """ print usages """
    print("Usages:")
    print("chiselformalcleaner.py [options]")
    print("-h, --help             print this help")
    print("-v, --verilog          verilog filename to modify")
    print("-o, --output filename  output filename")

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hv:o:",
                                  ["help", "verilog=", "output="])
    except getopt.GetoptError:
        usages()
        sys.exit(2)

    if opts == []:
        usages()
        sys.exit(0)

    vfilename = None
    outputname = None
    for opt, arg in opts:
        if opt in ["-v", "--verilog"]:
            vfilename = arg
        elif opt in ["-o", "--output"]:
            outputname = arg
        else:
            usages()
            sys.exit(2)

    assert vfilename is not None, "Please give a verilog input file name"
    assert outputname is not None, "Please give a output file name"

    dstring = iter(DELETE_STRING.split('\n'))

    with open(vfilename) as vfile, open(outputname, 'w') as ofile:
        deleting = False
        dline = next(dstring)
        for line in vfile:
            print(">{}<".format(dline))
            print("#{}#".format(line))
            if dline[:20].strip() == line[:20].strip():
                try:
                    dline = next(dstring)
                except StopIteration as err:
                    pass
            else:
                ofile.write(line)

    print("{} written".format(outputname))

if __name__ == "__main__":
    main(sys.argv[1:])
