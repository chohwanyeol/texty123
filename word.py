import zipfile
import re

docx = zipfile.ZipFile('/content/drive/MyDrive/Colab Notebooks/블록체인 워드.docx')
content = docx.read('word/document.xml').decode('utf-8')
cleaned = re.sub('<(.|\n)*?>','',content)
print(cleaned)
