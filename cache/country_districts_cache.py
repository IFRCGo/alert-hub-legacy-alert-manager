from django.core.cache import cache
from .models import CapFeedCountry



def initialise_country_cache():
    countries = CapFeedCountry.objects.all()
    for country in countries:
        country_data = {
            'country_id' : country.id,
            'country_name' : country.name,
            'districts' : []
            }
        for district in country.capfeeddistrict_set.all():
            if district.capfeedalertdistrict_set.count() > 0:
                country_data['districts'].append(district.to_dict())
        
        cache.set("country" + str(country.id), country_data, timeout = None)

def get_country(country_id):
    country_cache_key = "country" + str(country_id)
    return cache.get(country_cache_key, {})