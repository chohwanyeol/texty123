from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from konlpy.tag import Komoran
import textrank
import pdf
import image
import ppt
import os
import numpy
import cv2



web_site = Flask(__name__)
web_site.secret_key = 'random string'


@web_site.route('/')
def index(text = "",text_out = ""):
	return render_template('index.html', text = text,text_out = text_out)


@web_site.route('/inputText')
def input_text():
  
  text = request.args.get("text")
  print(text)
  
  choose = request.args.get("choose")
  print(choose)

  if text == "":
    flash('텍스트를 먼저 입력 해주세요.')
    return render_template('index.html',text = text)
  elif choose == "none":
    flash('요약 비율을 선택 해주세요.')
    return render_template('index.html',text = text)
  


  tr = textrank.TextRank()

  tagger = Komoran()
  stopword =set([('있','VV'),('하','VV'),('되','VV')])
  tr.loadSents(textrank.RawSentence(text), 
             lambda sent: filter(lambda x:x not in stopword and x[1] in ('NNG', 'NNP', 'VV', 'VA'), tagger.pos(sent)))
  tr.build()
  #ranks = tr.rank()
  #for k in sorted(ranks, key=ranks.get, reverse=True)[:100]:
  #    print("\t".join([str(k), str(ranks[k]), str(tr.dictCount[k])]))
  text_out = tr.summarize(int(choose) / 100)



  return render_template('index.html',text = text, text_out=text_out, choose = choose)

@web_site.route('/file',  methods=['GET', 'POST'])
def input_file():
  f = request.files["fileB"]
  print(str(f))
  if '.pdf' in str(f):
    text = pdf.extract_text_from_pdf(f)
    return render_template('index.html', text = text,text_out ="")

  elif '.jpg' in str(f) or '.png' in str(f) or '.PNG' in str(f) : 
    f = request.files["fileB"].read()
    npimg = numpy.fromstring(f,numpy.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    text = image.main(img)
    return render_template('index.html', text = text,text_out ="")



  elif '.pptx' in str(f):
  
    #f.save(secure_filename(f.filename))
    text = ppt.pptx(f)
    return render_template('index.html', text = text,text_out ="")


  
  #elif '.word' in str(f):






web_site.run(host='0.0.0.0', port=8080)