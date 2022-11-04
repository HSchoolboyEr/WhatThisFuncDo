# Some usable commands Radare2 shell


List all functions
```
afl 
```

 seek to address
```
s [addr] 
```

Print disassembled function sym.boost_acosh 
```
pif sym.boost_acosh 
pifj sym.boost_acosh > result.json
```

basic blocks of currient func
```
agf 
```

agfg - graph to Graph Modelling Language
```
agfg
agfg > result.gml
```
