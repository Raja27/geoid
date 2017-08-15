__author__ = "Raja Prasanna B"
import googlemaps
import requests
import json
import logging
from django.conf import settings
import datetime

logger = logging.getLogger('django.request')


class GeoIds(object):
    """
    This will use to compare the place based on google place id.
    So no need to compare the place string which may not be equal 
    always.
    Ex. Madras not equel to Chennai
 
    from geo_id import GeoIds
    geo_ids=GeoIds('India')
    geo_ids.get_id_data()
    
    return:
    {
      "country_id": "ChIJkbeSa_BfYzARphNChaFPjNc", 
      "country": "India"
    }

    geo_ids=GeoIds('Adyar')
    geo_ids.get_id_data()
    
    return: 
    {  
      "locality_id":"ChIJgRbEFe1nUjoRg54kepbOaWU",
      "state":"Tamil Nadu",
      "city":"Chennai",
      "state_id":"ChIJM5YYsYLFADsR8GEzRsx1lFU",
      "locality":"Adyar",
      "city_id":"ChIJYTN9T-plUjoRM9RjaAunYW4",
      "country_id":"ChIJkbeSa_BfYzARphNChaFPjNc",
      "country":"India"
    }
    """
    def __init__(self, place, key=None,  latlong=None):
        self.key = key
        self.place = place
        self.latlong = latlong
        if self.key is None:
            self.key = settings.GOOGLE_KEY

    def address_format(self, place):
        country = place.get('country', None)
        state = place.get('state', None)
        city = place.get('city', None)
        locality = place.get('sublocality', None)
        place = []
        place.append(locality) if locality else place.append('')
        place.append(city) if city else place.append('')
        place.append(state) if state else place.append('')
        place.append(country) if country else place.append('')
        return ','.join(place)

    def find_address(self, data, place={}):
        if isinstance(data, list):
            return [self.find_address(v, place) for v in data]
        elif isinstance(data, dict):
            types_list = data.get('types', None)
            if types_list and isinstance(types_list, list):
                if types_list.__contains__('country') or types_list.__contains__('natural_feature'):
                    country = data.get('long_name')
                    if country:
                        place.update({'country': country})
                if types_list.__contains__('administrative_area_level_1'):
                    state = data.get('long_name')
                    if state:
                        place.update({'state': state})
                if types_list.__contains__('locality'):
                    city = data.get('long_name')
                    if city:
                        place.update({'city': city})
                if 'sublocality' in types_list or 'sublocality_level_1' in types_list:
                    sublocality = data.get('long_name')
                    if sublocality:
                        place.update({'sublocality': sublocality})
            for k, v in data.items():
                self.find_address(v, place)
            return self.address_format(place)
        else:
            return

    def get_formatted_address(self, gmaps):
        formatted_address = gmaps.places(self.place).get('results')[0].get('formatted_address')
        geocode_result = gmaps.geocode(formatted_address)
        if not geocode_result:
            url = "http://maps.googleapis.com/maps/api/geocode/json?latlng={}&sensor=false".format(self.latlong[1:-1])
            response = requests.request("GET", url)
            if response.status_code == 200:
                geocode_result = json.loads(response.text)
                geocode_result = geocode_result.get('results')
        return geocode_result

    def get_id_data(self):
        try:
            print(datetime.datetime.now())
            gmaps = googlemaps.Client(key=self.key)
            geocode_result = gmaps.geocode(self.place)
            if not geocode_result:
                geocode_result = self.get_formatted_address(gmaps)
            locality, city, state, country = self.find_address(geocode_result, place={})[0].split(',')
            self.place = None
            result = {}
            if locality:
                result.update({
                    'locality': locality,
                    'locality_id': gmaps.geocode(
                        '{}, {}, {}, {}'.format(locality, city, state, country))[0].get('place_id')
                })
            if city:
                result.update({
                    'city': city,
                    'city_id': gmaps.geocode('{}, {}, {}'.format(city, state, country))[0].get('place_id')
                })
            if state:
                result.update({
                    'state': state,
                    'state_id': gmaps.geocode('{}, {}'.format(state, country))[0].get('place_id'),
                })

            result.update({
                'country': country,
                'country_id': gmaps.geocode(country)[0].get('place_id')
            })
            print(datetime.datetime.now())
            return result
        except Exception as e:
            logger.error(repr(e))
