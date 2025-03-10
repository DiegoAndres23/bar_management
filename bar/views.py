from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Mesa, Pedido, Producto
from .forms import PedidoForm

class HomePage(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(HomePage, self).dispatch(request, *args, **kwargs)

class MesaListView(ListView):
    model = Mesa
    template_name = 'mesa_list.html'
    context_object_name = 'mesas'

class MesaDetailView(TemplateView):
    template_name = 'mesa_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mesa = get_object_or_404(Mesa, pk=kwargs['pk'])
        context['mesa'] = mesa
        context['pedidos'] = mesa.pedidos.all()
        context['form'] = PedidoForm()
        return context

    def post(self, request, *args, **kwargs):
        mesa = get_object_or_404(Mesa, pk=kwargs['pk'])
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.mesa = mesa
            pedido.save()
        return redirect('mesa_detail', pk=mesa.pk)

class MesaCreateView(CreateView):
    model = Mesa
    template_name = 'mesa_form.html'
    fields = ['numero', 'capacidad', 'estado']
    success_url = reverse_lazy('mesa_list')

class MesaUpdateView(UpdateView):
    model = Mesa
    template_name = 'mesa_form.html'
    fields = ['numero', 'capacidad', 'estado']
    success_url = reverse_lazy('mesa_list')

class MesaDeleteView(DeleteView):
    model = Mesa
    template_name = 'mesa_confirm_delete.html'
    success_url = reverse_lazy('mesa_list')


