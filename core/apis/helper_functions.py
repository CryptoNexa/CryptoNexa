

def process_crypto_data(objs, currency, many):
    if many:
        data_list = []
        for current_obj in objs:
            processed_data = {}
            processed_data['id'] = current_obj.pk
            processed_data['name'] = current_obj.name
            try:
                processed_data['price'] = current_obj.quote.data.get(currency).get('price')
            except Exception as e:
                print("Issue is in ", currency)
                print("Name is ", current_obj)
                return
            processed_data['percent_change_1h'] = current_obj.quote.data.get(currency).get('percent_change_1h')
            processed_data['percent_change_24h'] = current_obj.quote.data.get(currency).get('percent_change_24h')
            processed_data['market_cap'] = current_obj.quote.data.get(currency).get('market_cap')
            processed_data['volume_24h'] = current_obj.quote.data.get(currency).get('volume_24h')

            """Meta data for Backend"""
            processed_data['currency'] = currency
            processed_data['slug'] = current_obj.slug
            data_list.append(processed_data)
        return data_list
    pass