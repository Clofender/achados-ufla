from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from occurrences.models import Occurrence

from .forms import ItemForm, ProfileForm, RegisterForm
from .models import Category, Item, Location, Profile


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("accounts_login")
    user_items = Item.objects.filter(owner=request.user)
    user_occurrences = Occurrence.objects.filter(reporter=request.user)
    context = {
        "total_items": Item.objects.filter(is_public=True).count(),
        "found_items": Item.objects.filter(status=Item.Status.FOUND, is_public=True).count(),
        "lost_items": Item.objects.filter(status=Item.Status.LOST, is_public=True).count(),
        "returned_items": Item.objects.filter(status=Item.Status.RETURNED).count(),
        "pending_items": Item.objects.filter(approved=False, is_public=True).count(),
        "my_items": user_items.count(),
        "my_occurrences": user_occurrences.count(),
        "recent_items": Item.objects.filter(is_public=True).select_related("category", "location")[:5],
        "recent_occurrences": user_occurrences.select_related("item")[:5],
    }
    return render(request, "core/dashboard.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Conta criada com sucesso. Bem-vindo ao Achados UFLA!")
        return redirect("dashboard")
    return render(request, "accounts/register.html", {"form": form})


class PublicLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class PublicLogoutView(LogoutView):
    next_page = reverse_lazy("accounts_login")


@login_required
def profile(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": user_profile})


@login_required
def profile_edit(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=user_profile)
    if form.is_valid():
        form.save()
        messages.success(request, "Perfil atualizado.")
        return redirect("accounts_profile")
    return render(request, "accounts/profile_edit.html", {"form": form})


class ItemListView(LoginRequiredMixin, ListView):
    template_name = "core/item_list.html"
    context_object_name = "items"
    paginate_by = 9

    def get_queryset(self):
        queryset = Item.objects.filter(is_public=True).select_related("category", "location")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(characteristics__icontains=query)
            )
        for field in ("category_id", "location_id", "status"):
            value = self.request.GET.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "categories": Category.objects.filter(is_active=True),
            "locations": Location.objects.all(),
            "statuses": Item.Status.choices,
            "result_count": self.get_queryset().count(),
        })
        return context


class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "core/item_detail.html"
    queryset = Item.objects.select_related("category", "location", "owner")


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner_id == self.request.user.id

    def handle_no_permission(self):
        return HttpResponseForbidden("Você não tem permissão para alterar este objeto.")


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = "core/item_form.html"
    success_url = reverse_lazy("items:mine")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.approved = False
        messages.success(self.request, "Objeto cadastrado e enviado para validação.")
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "core/item_form.html"
    success_url = reverse_lazy("items:mine")


class ItemDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Item
    template_name = "core/item_confirm_delete.html"
    success_url = reverse_lazy("items:mine")


class MyItemListView(LoginRequiredMixin, ListView):
    template_name = "core/item_mine.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user).select_related("category", "location")
