# smtbmcify

This script add somes assert/assume rules under a verilog module. To use it a
file with rules should be given in parameter

```
Usages:
$ python smtbmcify.py [options]
-h, --help             print this help message
-v, --verilog=module.v verilog module to read
-f, --formal=formal.sv formals rules
-o, --output=name.sv   output filename, default is moduleFormal.sv
```

Formal file format must begin with tag:
```Verilog
//BeginModule:ModuleName
```

And end with tag:
```Verilog
//EndModule:ModuleName
```

smtbmcify will find module named `ModuleName` in `module.v` given in parameter
and copy all lines between above tag. 
