from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List

User = get_user_model()

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
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    return render(request, "home.j2", {"form": form})


@require_http_methods(["GET"])
def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "my_lists.j2", {"owner": owner})
