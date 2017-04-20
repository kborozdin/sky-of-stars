m.dbfDir=justpath(sys(16))
m.txtDir=addbs(justpath(m.dbfDir))+'txt\'

sele sele('bright')
use (addbs(m.dbfDir)+'bright') alias 'bright'

dime aTxt(1)
=adir(aTxt,'*.txt')

for m.i=1 to alen(aTxt,1)
	appe from (m.txtDir+aTxt(i,1)) type sdf
	m.s=subs(aTxt(m.i,1),1,3)
	repl for empt(co) co with m.s
endf
