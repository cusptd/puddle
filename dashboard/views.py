from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from prompt.models import Prompt

@login_required
def index(request):
    prompts = Prompt.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index.html', {
        'prompts': prompts,
    })
