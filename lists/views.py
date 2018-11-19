from django.core.exceptions import ValidationError
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
        item = Item.objects.create(text=request.POST["item_text"], list=list_)
        try:
            item.full_clean()
        except ValidationError:
            error = "You can't have an empty list item."
            item.delete()
            return render(request, "list.html", {"list": list_, "error": error})
    else:
        list_ = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": list_})


@require_http_methods(["POST"])
def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        item.delete()
        error = "You can't have an empty list item."
        return render(request, "home.html", {"error": error})
    return redirect(f"/lists/{list_.id}")
