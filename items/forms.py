import django.forms as forms
from crispy_forms.layout import Submit, Layout, Div, Row
from django.forms import Form
from crispy_forms.helper import FormHelper
from .models import Itemtrans, ProductDetail, OptimizationItemAttribute, OptimizationItem, Settings
import items.models as mod


class SupplierForm(forms.Form):
    like_website = forms.TypedChoiceField(
            label = "Do you like this website?",
            choices = ((1, "Yes"), (0, "No")),
            coerce = lambda x: bool(int(x)),
            widget = forms.RadioSelect,
            initial = '1',
            required = True,
        )
    moretxt = forms.CharField(label = "Anything else?",
                              required = True)

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'get'
        self.helper.form_action = 'submit_survey'

class ProductForm(forms.Form):
    code = ProductDetail.code
    name = ProductDetail.name

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'get'
        self.helper.form_action = 'submit_survey'


class ImportProductForm(forms.Form):
    code = ProductDetail.code


class SettingsForm(forms.ModelForm):
    A_percent=Settings.A_percent
    B_percent=Settings.B_percent
    C_percent=Settings.C_percent

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
       # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
       # You can dynamically adjust your layout
        self.helper.layout = Layout(
            Row(
                Div('A_percent', css_class='col-sm-1', ),
                Div('B_percent', css_class='col-sm-1', ),
                Div('C_percent', css_class='col-sm-1', ),
                css_class='row',
            ))

    class Meta:
        model = Settings
        fields = {'A_percent','B_percent', 'C_percent'}
