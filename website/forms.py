from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, Product, Variety, Category, Company, Region, Province, Municipality, Barangay
from django.contrib.auth.models import User

User = get_user_model()

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['name', 'region']

class MunicipalityForm(forms.ModelForm):
    class Meta:
        model = Municipality
        fields = ['name', 'province']

class BarangayForm(forms.ModelForm):
    class Meta:
        model = Barangay
        fields = ['name', 'municipality']

class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
        ('logistics', 'Logistics'),
    ]

    profile_picture = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=50, required=True)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)

    class Meta:
        model = User
        fields = [
            'profile_picture', 'username', 'first_name', 'middle_name', 'last_name',
            'email', 'contact_number', 'user_type', 'company', 'password1', 'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)  # Save user but don’t commit yet
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()  # Save user first

            # Ensure the Profile object is created and all data is saved properly
            profile, created = Profile.objects.get_or_create(user=user)
            profile.middle_name = self.cleaned_data.get('middle_name', '')
            profile.contact_number = self.cleaned_data['contact_number']
            profile.user_type = self.cleaned_data['user_type']
            profile.company = self.cleaned_data.get('company', None)
            
            # Save profile picture if uploaded
            if self.cleaned_data.get('profile_picture'):
                profile.profile_picture = self.cleaned_data['profile_picture']

            profile.save()  # Save profile details

        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'image']

class VarietyForm(forms.ModelForm):
    class Meta:
        model = Variety
        fields = ['description', 'quantity', 'price']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'contact_number', 'region', 'province', 'municipality', 'barangay']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].queryset = Province.objects.none()
        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['barangay'].queryset = Barangay.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['province'].queryset = Province.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id)
            except (ValueError, TypeError):
                pass

        if 'municipality' in self.data:
            try:
                municipality_id = int(self.data.get('municipality'))
                self.fields['barangay'].queryset = Barangay.objects.filter(municipality_id=municipality_id)
            except (ValueError, TypeError):
                pass


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['profile_picture', 'contact_number']  # Exclude fields that belong to User

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user instance
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
