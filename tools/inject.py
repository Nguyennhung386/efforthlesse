import sys,json,re
src,lib,ids,out=sys.argv[1:5]
s=open(src,encoding='utf-8').read()
L=open(lib,encoding='utf-8').read(); I=open(ids,encoding='utf-8').read()
s=re.sub(r'/\*LIB\*/.*?/\*END\*/',lambda m:'/*LIB*/'+L+'/*END*/',s,count=1,flags=re.S)
s=re.sub(r'/\*IDS\*/.*?/\*END\*/',lambda m:'/*IDS*/'+I+'/*END*/',s,count=1,flags=re.S)
open(out,'w',encoding='utf-8').write(s)
