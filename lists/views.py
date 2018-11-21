from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from lists.forms import ItemForm
from lists.models import Item, List


# Create your views here.
@require_http_methods(["GET", "POST"])
def home_page(request):
    if request.method == "POST":
        list_ = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=list_)
        return redirect(f"/lists/{list_.id}/")

    return render(request, "home.html", {"form": ItemForm()})


@require_http_methods(["GET", "POST"])
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST["text"], list=list_)
            return redirect(list_)
    return render(request, "list.html", {"list": list_, "form": form})


@require_http_methods(["POST"])
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form})
