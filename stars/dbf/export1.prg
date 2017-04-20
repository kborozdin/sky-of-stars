m.dbfDir=addbs(justpath(sys(16)))

sele sele('bright')
use (m.dbfDir+'bright') alias 'bright'

m.h=fcre(m.dbfDir+'data1.txt')
scan
	=fwri(m.h,allt(alf)+','+allt(del)+chr(13)+chr(10))
ends
=fclo(m.h)
