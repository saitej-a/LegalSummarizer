from django.shortcuts import render
import pymupdf
from summa import summarizer
from transformers import pipeline
import io
# Create your views here.
def extsum(text):
    return summarizer.summarize(text, ratio=0.2)
def abssum(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
def index(request):
    if request.method == 'POST':
        
        if request.FILES:
            docfile=request.FILES['file']
            #saving the file in memory temporarily
            with open('tempfile.pdf','wb+') as destination:
                for chunk in docfile.chunks():
                    destination.write(chunk)
            doc = pymupdf.open(destination) 
            text = doc[0].get_text()
            
            doc.close()
            destination.close()
            # os.remove(destination.name)
            if request.POST['method']=='0':
                summary =extsum(text)
                return render(request, 'index.html', {'summary': summary})
            else:
                summary = abssum(text)
                return render(request, 'index.html', {'summary': summary})
        elif request.POST['text']:
            text = request.POST['text']
            if request.POST['method']=='0':

                summary =extsum(text)
                print(f'{summary=},{text=}')
                return render(request, 'index.html', {'summary': summary})
            else:
                summary = abssum(text)
                return render(request, 'index.html', {'summary': summary})
        else:
            text = "No file or text provided."
        # Render the extracted text in a template
        return render(request, 'index.html', {'summary': text})
    return render(request, 'index.html')