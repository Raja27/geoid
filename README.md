# Google Place ID
>This will use to compare the place based on google place id.
    So no need to compare the place string which may not be equal
    always.
    Ex. Madras not equel to Chennai ( City in Tamil Nadu )
### Installation
```pip install google-place-id```
### Example
#### Country
```
from geo_id import GeoIds
geo_ids=GeoIds('India')
geo_ids.get_id_data()
```
```
return:
{
 "country_id": "ChIJkbeSa_BfYzARphNChaFPjNc",
 "country": "India"
}
```
#### Locality, City, State, Country
```
geo_ids=GeoIds('Adyar')  # Locality in Chennai
geo_ids.get_id_data()
```
```
return:
{
 "locality_id":"ChIJgRbEFe1nUjoRg54kepbOaWU",
 "locality":"Adyar",
 "state_id":"ChIJM5YYsYLFADsR8GEzRsx1lFU",
 "state":"Tamil Nadu",
 "city_id":"ChIJYTN9T-plUjoRM9RjaAunYW4",
 "city":"Chennai",
 "country_id":"ChIJkbeSa_BfYzARphNChaFPjNc",
 "country":"India"
}
```
