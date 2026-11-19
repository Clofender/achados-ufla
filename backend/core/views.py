from datetime import timedelta

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
    visible_items = Item.objects.filter(is_public=True)
    if not request.user.is_staff:
        visible_items = visible_items.filter(approved=True).exclude(status=Item.Status.ARCHIVED)
    total_items = visible_items.count()
    found_items = visible_items.filter(status=Item.Status.FOUND).count()
    lost_items = visible_items.filter(status=Item.Status.LOST).count()
    returned_items = visible_items.filter(status=Item.Status.RETURNED).count()
    chart_total = total_items or 1
    context = {
        "total_items": total_items,
        "found_items": found_items,
        "lost_items": lost_items,
        "returned_items": returned_items,
        "has_chart_data": total_items > 0,
        "found_percent": round(found_items * 100 / chart_total),
        "lost_end_percent": round((found_items + lost_items) * 100 / chart_total),
        "pending_items": Item.objects.filter(approved=False, is_public=True).count()
        if request.user.is_staff
        else user_items.filter(approved=False).count(),
        "my_items": user_items.count(),
        "my_occurrences": user_occurrences.count(),
        "recent_items": visible_items.select_related("category", "location")[:5],
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
        if not self.request.user.is_staff:
            queryset = queryset.filter(approved=True).exclude(status=Item.Status.ARCHIVED)
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(characteristics__icontains=query)
            )
        for field in ("category_id", "location_id", "status"):
            value = self.request.GET.get(field) or self.request.GET.get(field.removesuffix("_id"))
            if value:
                queryset = queryset.filter(**{field: value})
        period = self.request.GET.get("period")
        if period in {"7", "30", "365"}:
            queryset = queryset.filter(
                created_at__gte=timezone.now() - timedelta(days=int(period))
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "categories": Category.objects.filter(is_active=True),
            "locations": Location.objects.all(),
            "statuses": Item.Status.choices,
            "result_count": self.get_queryset().count(),
        })
        query = self.request.GET.copy()
        query.pop("page", None)
        context["pagination_query"] = query.urlencode()
        return context


class ItemDetailView(LoginRequiredMixin, DetailView):
    template_name = "core/item_detail.html"

    def get_queryset(self):
        queryset = Item.objects.select_related("category", "location", "owner")
        if not self.request.user.is_staff:
            queryset = queryset.filter(approved=True).exclude(status=Item.Status.ARCHIVED)
        return queryset


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ItemDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Item
    template_name = "core/item_confirm_delete.html"
    success_url = reverse_lazy("items:mine")


class MyItemListView(LoginRequiredMixin, ListView):
    template_name = "core/item_mine.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user).select_related("category", "location")
