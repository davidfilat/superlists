from django.forms import ModelForm, TextInput

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item."


class ItemForm(ModelForm):
    EMPTY_ITEM_ERROR = "You can't have an empty list item."

    class Meta:
        model = Item
        fields = ["text"]
        widgets = {
            "text": TextInput(
                attrs={
                    "placeholder": "Enter a to-do item",
                    "class": "form-control input-lg",
                }
            )
        }
        error_messages = {"text": {"required": EMPTY_ITEM_ERROR}}

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
