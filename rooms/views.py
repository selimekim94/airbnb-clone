from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from rooms.models import Room
from rooms.forms import SearchForm


# Create your views here.
class HomeView(ListView):
    model = Room
    template_name = 'rooms/list.html'
    paginate_by = 10
    paginate_orphans = 5
    ordering = 'created_at'
    context_object_name = 'rooms'


class RoomDetailView(DetailView):
    model = Room
    template_name = 'rooms/detail.html'
    context_object_name = 'room'


class SearchView(FormMixin, ListView):
    model = Room
    form_class = SearchForm
    template_name = 'rooms/search.html'
    context_object_name = 'rooms'
    paginate_by = 10
    paginate_orphans = 5
    ordering = 'created_at'

    def get_context_data(self, **kwargs):
        get_copy = self.request.GET.copy()
        if 'page' in get_copy:
            del get_copy['page']
        parameters = get_copy.urlencode()
        context = super().get_context_data(**kwargs)
        context['parameters'] = parameters
        return context

    def get_queryset(self):
        country = self.request.GET.get('country')
        if country:
            form = self.form_class(self.request.GET)
            if form.is_valid():
                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                room_type = form.cleaned_data.get('room_type')
                price = form.cleaned_data.get('price')
                guests = form.cleaned_data.get('guests')
                bedrooms = form.cleaned_data.get('bedrooms')
                beds = form.cleaned_data.get('beds')
                baths = form.cleaned_data.get('baths')
                instant_book = form.cleaned_data.get('instant_book')
                super_host = form.cleaned_data.get('super_host')
                amenities = form.cleaned_data.get('amenities')
                facilities = form.cleaned_data.get('facilities')

                filter_args = {}

                if city != 'Anywhere':
                    filter_args['city__startswith'] = city
                filter_args['country'] = country
                if room_type is not None:
                    filter_args['room_type'] = room_type
                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if super_host is True:
                    filter_args["host__super_host"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                self.queryset = Room.objects.filter(**filter_args)
        return self.queryset
