from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List


# Create your views here.
@require_http_methods(["GET", "POST"])
def home_page(request):
    if request.method == "POST":
        list_ = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=list_)
        return redirect(f"/lists/{list_.id}/")

    return render(request, "home.j2", {"form": ItemForm()})


@require_http_methods(["GET", "POST"])
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, "list.j2", {"list": list_, "form": form})


@require_http_methods(["POST"])
def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    return render(request, "home.j2", {"form": form})


def my_lists(request, email):
    return render(request, "my_lists.html")
