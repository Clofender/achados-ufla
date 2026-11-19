from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.models import Item

from .forms import OccurrenceForm
from .models import Occurrence


class OccurrenceListView(LoginRequiredMixin, ListView):
    template_name = "occurrences/list.html"
    context_object_name = "occurrences"

    def get_queryset(self):
        return Occurrence.objects.filter(reporter=self.request.user).select_related(
            "item", "location"
        )


class OccurrenceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Occurrence
    template_name = "occurrences/detail.html"

    def test_func(self):
        occurrence = self.get_object()
        return occurrence.reporter_id == self.request.user.id or self.request.user.has_perm(
            "occurrences.view_occurrence"
        )

    def handle_no_permission(self):
        return HttpResponseForbidden("Você não tem permissão para visualizar este registro.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = getattr(self.request.user, "profile", None)
        context["can_review"] = self.request.user.is_superuser or (
            self.request.user.has_perm("occurrences.change_occurrence")
            or getattr(profile, "role", None) in {"moderator", "admin"}
        )
        return context


class OccurrenceCreateView(LoginRequiredMixin, CreateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = "occurrences/form.html"
    success_url = reverse_lazy("occurrences:mine")

    def get_initial(self):
        initial = super().get_initial()
        item_id = self.request.GET.get("item")
        if item_id:
            initial["item"] = item_id
        return initial

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.status = Occurrence.Status.PENDING
        messages.success(self.request, "Ocorrência registrada e enviada para análise.")
        return super().form_valid(form)


class OccurrenceOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().reporter_id == self.request.user.id

    def handle_no_permission(self):
        return HttpResponseForbidden("Você não tem permissão para alterar esta ocorrência.")


class OccurrenceUpdateView(LoginRequiredMixin, OccurrenceOwnerMixin, UpdateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = "occurrences/form.html"
    success_url = reverse_lazy("occurrences:mine")

    def get_queryset(self):
        return super().get_queryset().filter(status=Occurrence.Status.PENDING)


class OccurrenceDeleteView(LoginRequiredMixin, OccurrenceOwnerMixin, DeleteView):
    model = Occurrence
    template_name = "occurrences/confirm_delete.html"
    success_url = reverse_lazy("occurrences:mine")

    def get_queryset(self):
        return super().get_queryset().filter(status=Occurrence.Status.PENDING)


def is_moderator(user):
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm("occurrences.change_occurrence")
        or getattr(getattr(user, "profile", None), "role", None)
        in {"moderator", "admin"}
    )


@login_required
@user_passes_test(is_moderator)
def approve_return(request, pk):
    if request.method != "POST":
        return HttpResponseForbidden("Ação inválida.")
    with transaction.atomic():
        occurrence = get_object_or_404(
            Occurrence.objects.select_for_update().select_related("item"), pk=pk
        )
        if occurrence.item.status == Item.Status.RETURNED:
            messages.info(request, "Este objeto já foi marcado como devolvido.")
        elif occurrence.occurrence_type != Occurrence.Type.RETURN_REQUEST:
            messages.error(request, "Apenas solicitações de devolução podem ser aprovadas.")
        else:
            occurrence.status = Occurrence.Status.APPROVED
            occurrence.reviewed_by = request.user
            occurrence.reviewed_at = timezone.now()
            occurrence.returned_to = occurrence.reporter
            occurrence.return_notes = occurrence.notes
            occurrence.save(
                update_fields=[
                    "status",
                    "reviewed_by",
                    "reviewed_at",
                    "returned_to",
                    "return_notes",
                ]
            )
            item = occurrence.item
            item.status = Item.Status.RETURNED
            item.approved = True
            item.approved_by = request.user
            item.approved_at = timezone.now()
            item.save(update_fields=["status", "approved", "approved_by", "approved_at", "updated_at"])
            messages.success(request, "Solicitação aprovada e objeto marcado como devolvido.")
    return redirect("occurrences:detail", pk=pk)
