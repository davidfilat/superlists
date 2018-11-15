from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from lists.models import Item, List


# Create your views here.
@require_http_methods(["GET", "POST"])
def home_page(request):
    if request.method == "POST":
        list_ = List.objects.create()
        Item.objects.create(text=request.POST["item_text"], list=list_)
        return redirect(f"/lists/{list_.id}/")

    return render(request, "home.html")


@require_http_methods(["GET", "POST"])
def view_list(request, list_id):
    if request.method == "POST":
        list_ = List.objects.get(id=list_id)
        Item.objects.create(text=request.POST["item_text"], list=list_)
    else:
        list_ = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": list_})


@require_http_methods(["POST"])
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}")
