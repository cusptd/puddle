from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewPromptForm, EditPromptForm
from .models import Category, Prompt

def prompts(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    prompts = Prompt.objects.filter(is_sold=False)

    if category_id:
        prompts = prompts.filter(category_id=category_id)

    if query:
        prompts = prompts.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'prompt/prompts.html', {
        'prompts': prompts,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    related_prompts = Prompt.objects.filter(category=prompt.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'prompt/detail.html', {
        'prompt': prompt,
        'related_prompts': related_prompts
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewPromptForm(request.POST, request.FILES)

        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.created_by = request.user
            prompt.save()

            return redirect('prompt:detail', pk=prompt.id)
    else:
        form = NewPromptForm()

    return render(request, 'prompt/form.html', {
        'form': form,
        'title': 'New prompt',
    })

@login_required
def edit(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditPromptForm(request.POST, request.FILES, instance=prompt)

        if form.is_valid():
            form.save()

            return redirect('prompt:detail', pk=prompt.id)
    else:
        form = EditPromptForm(instance=prompt)

    return render(request, 'prompt/form.html', {
        'form': form,
        'title': 'Edit prompt',
    })

@login_required
def delete(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk, created_by=request.user)
    prompt.delete()

    return redirect('dashboard:index')