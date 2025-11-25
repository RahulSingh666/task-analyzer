from django.http import HttpResponse
from pathlib import Path

def frontend(request):
    index = (Path(__file__).resolve().parent.parent / '../frontend/index.html').resolve()
    return HttpResponse(index.read_text(encoding='utf-8'))
