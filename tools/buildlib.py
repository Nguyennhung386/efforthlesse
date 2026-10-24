import json,re,sys,collections
d=json.load(open(sys.argv[1]))
if isinstance(d,list): d=d[0]
if 'text' in d: d=json.loads(d['text'])
fs=[x['name'] for x in d['entries'] if x['type']=='file']
A='Tài liệu bài học luyện nói tiếng Anh như người bản ngữ - EffortlessEnglishClub.vn/'
E=A+'Luyện nói tiếng Anh như người bản ngữ Effortless English/'
B='Tài liệu tham khảo và hướng dẫn học phương pháp Effortless English - Ajhoge.vn/'
base=lambda p:p.rsplit('/',1)[-1]
stem=lambda p:base(p).rsplit('.',1)[0]
def nat(s): return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)',s)]
KIND={'main':'Bài chính','vocabulary':'Từ vựng','ms':'Mini story','pov':'Góc nhìn','com':'Bình luận'}
def lessons(cid,audio_prefix,dirpat,ebook,zipdir=None):
    les={}
    for f in fs:
        m=re.match(re.escape(audio_prefix)+dirpat+r' (\d+)/(.+\.mp3)$',f)
        if m: les.setdefault(int(m.group(1)),{'a':[],'p':[],'z':None})['a'].append(f)
        if zipdir:
            m=re.match(re.escape(zipdir)+r'.+ Lesson (\d+)\.zip$',f)
            if m: les.setdefault(int(m.group(1)),{'a':[],'p':[],'z':None})['z']=f
        m=re.match(re.escape(ebook)+r'0*(\d+)[ _]([^/]+)/(.+\.pdf)$',f)
        if m:
            L=les.setdefault(int(m.group(1)),{'a':[],'p':[],'z':None}); L['p'].append(f); L.setdefault('t',m.group(2))
    out=[]
    for n in sorted(les):
        L=les[n]; L['a'].sort(key=nat); L['p'].sort(key=nat)
        title=None
        if L['a']:
            m=re.match(r'\d+[a-z] (.+?)(?: \d)? \(',base(L['a'][0])); title=m.group(1) if m else stem(L['a'][0])
        else: title=L.get('t','Lesson %d'%n).strip()
        title=title[:1].upper()+title[1:]
        out.append({'n':n,'title':title,
          'audio':[[stem(a),a] for a in L['a']],
          'pdf':[[stem(p).replace('_',' '),p] for p in L['p']],
          'zip':L['z']})
    return out
lib=[
 {'id':'original','name':'Original English','year':2007,'lessons':lessons('o',E+'(1) Original English Audio (2007)/mp3/','Original English Lesson',E+'audio ebook/1 Original English Lessons/')},
 {'id':'flow','name':'Flow English','year':2008,'lessons':lessons('f',E+'(2) Flow English Audio (2008)/','Flow English Lesson',E+'audio ebook/2 Flow English Lessons/')},
 {'id':'business','name':'Business English','year':2009,'lessons':lessons('b',E+'(3) Business English Audio (2009)/','Business English Lesson',E+'audio ebook/3 Business English Lessons/')},
 {'id':'power','name':'Power English','year':2010,'lessons':lessons('p',E+'(4) Power English Audio (2010)/','Power English Lesson',E+'audio ebook/4 Power English Lessons/',E+'(4) Power English Audio (2010)/')},
 {'id':'real','name':'Real English','year':2011,'lessons':lessons('r',E+'(5) Real English Audio (2011)/','Real English Lesson',E+'audio ebook/5 Real English Lessons/',E+'(5) Real English Audio (2011)/')},
]
# pronunciation units
pr=[f for f in fs if f.startswith(E+'(6) Pronunciation Audio (2018)/')]
units=collections.OrderedDict()
for f in sorted(pr,key=nat):
    m=re.search(r'Unit (\d+)',base(f)); k=int(m.group(1)) if m else 0
    units.setdefault(k,[]).append(f)
lib.append({'id':'pron','name':'Pronunciation','year':2018,'lessons':[{'n':k,'title':('Unit %02d'%k) if k else 'Introduction','audio':[[stem(f),f] for f in v if f.endswith('.mp3')],'pdf':[[stem(f),f] for f in v if f.endswith('.pdf')],'zip':None} for k,v in units.items()]})
ws=sorted([f for f in fs if f.startswith(A+'Luyện phát âm chuẩn giọng Mỹ Pronunciation Workshop/')],key=nat)
lib.append({'id':'workshop','name':'Pronunciation Workshop','year':None,'lessons':[{'n':i+1,'title':stem(f),'video':[[stem(f),f]],'audio':[],'pdf':[],'zip':None} for i,f in enumerate(ws) if re.search(r'\.(mp4|avi|mp3|pdf)$',f)]})
P=A+'Tiếng Anh giao tiếp cho người mới bắt đầu Pimsleur English/'
pim=[]
for sub,lab in [('(1) Pimsleur English Listening Audio/','Listening'),('(2) Pimsleur English Reading Audio/','Reading')]:
    for f in sorted([f for f in fs if f.startswith(P+sub) and f.endswith('.mp3')],key=nat):
        pim.append({'n':len(pim)+1,'title':stem(f).replace('Pimsleur English ',''),'audio':[[stem(f),f]],'pdf':[],'zip':None,'part':lab})
lib.append({'id':'pimsleur','name':'Pimsleur English','year':None,'books':[[stem(f),f] for f in fs if f.startswith(P) and f.count('/')==P.count('/') and f.endswith('.pdf')],'lessons':pim})
meth=[{'n':0,'title':'Tài liệu hướng dẫn','audio':[],'pdf':[[stem(f),f] for f in sorted(fs,key=nat) if f.startswith(B) and f.count('/')==B.count('/') and f.endswith('.pdf')],'zip':None}]
for sub in ['7 Quy luật học nói tiếng Anh (video)','Câu chuyện thành công (video)','Hệ thống học tiếng Anh (video)']:
    v=sorted([f for f in fs if f.startswith(B+sub+'/')],key=nat)
    meth.append({'n':len(meth),'title':sub.replace(' (video)',''),'audio':[[stem(f),f] for f in v if f.endswith('.mp3')],'video':[[stem(f),f] for f in v if re.search(r'\.(mp4|avi)$',f)],'pdf':[[stem(f),f] for f in v if f.endswith('.pdf')],'zip':None})
lib.append({'id':'method','name':'Phương pháp','year':None,'lessons':meth})
json.dump(lib,open('lib.json','w'),ensure_ascii=False)
for c in lib:
    L=c['lessons']; print(c['id'],len(L),sum(len(x['audio']) for x in L),'audio',sum(len(x['pdf']) for x in L),'pdf',sum(len(x.get('video',[])) for x in L),'vid',sum(1 for x in L if x.get('zip')),'zip')
print(json.dumps(lib[0]['lessons'][0],ensure_ascii=False)[:600]); print(json.dumps(lib[1]['lessons'][13],ensure_ascii=False)[:900]); print(json.dumps(lib[3]['lessons'][0],ensure_ascii=False)[:600])
