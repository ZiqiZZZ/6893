from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
from .synthesize import synthesize
import os, asyncio
from asgiref.sync import sync_to_async
import django, asyncio


async def my_view(request):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()

    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'You can upload multiple videos!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Document(docfile=request.FILES['docfile'])
            doc.save()

            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dir = os.path.join(base, 'media', doc.docfile.name),
            await synthesize(dir[0])

            # Redirect to the document list after POST
            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'list.html', context)
