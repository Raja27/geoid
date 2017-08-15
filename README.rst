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
