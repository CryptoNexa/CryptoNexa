from django.core.exceptions import ObjectDoesNotExist

from core.apis.coinmarketcap.fetch_data import fetch_crypto_meta_data
from core.models import Cryptocurrency, Quote


def keep_two_chars_after_dot(input_string):
    dot_index = input_string.find('.')
    if dot_index != -1 and len(input_string) > dot_index + 2:
        modified_string = input_string[:dot_index + 3]
    else:
        modified_string = input_string
    return modified_string


def process_crypto_data(objs, currency, many):
    if many:
        data_list = []
        for current_obj in objs:
            try:
                processed_data = {}
                processed_data['id'] = current_obj.pk
                processed_data['name'] = current_obj.name
                processed_data['price'] = current_obj.quote.data.get(currency).get('price')
                processed_data['percent_change_1h'] = current_obj.quote.data.get(currency).get('percent_change_1h')
                processed_data['percent_change_24h'] = current_obj.quote.data.get(currency).get('percent_change_24h')
                processed_data['market_cap'] = current_obj.quote.data.get(currency).get('market_cap')
                processed_data['volume_24h'] = current_obj.quote.data.get(currency).get('volume_24h')

                """Meta data for Backend"""
                processed_data['currency'] = currency
                processed_data['slug'] = current_obj.slug
                data_list.append(processed_data)
            except Exception as e:
                del (processed_data['id'])
        return data_list
    else:
        processed_data = {}
        processed_data['id'] = objs.pk
        processed_data['name'] = objs.name
        processed_data['symbol'] = objs.symbol
        processed_data['price'] = objs.price
        processed_data['percent_change_1h'] = objs.quote.data.get(currency).get('percent_change_1h')
        processed_data['percent_change_24h'] = objs.quote.data.get(currency).get('percent_change_24h')
        processed_data['market_cap'] = objs.quote.data.get(currency).get('market_cap')
        processed_data['volume_24h'] = objs.quote.data.get(currency).get('volume_24h')
        processed_data['volume_change_24h'] = objs.quote.data.get(currency).get('volume_change_24h')

        processed_data['num_market_pairs'] = objs.num_market_pairs
        processed_data['circulating_supply'] = objs.circulating_supply
        processed_data['total_supply'] = objs.total_supply
        processed_data['max_supply'] = objs.max_supply
        processed_data['infinite_supply'] = objs.infinite_supply

        meta_data = fetch_crypto_meta_data(objs.symbol)
        processed_data['logo'] = meta_data.get('data').get(objs.symbol)[0].get('logo')
        processed_data['description'] = meta_data.get('data').get(objs.symbol)[0].get('description')
        processed_data['website'] = meta_data.get('data').get((objs.symbol))[0].get('urls').get('website')[0]

        """Meta data for Backend"""
        processed_data['currency'] = currency
        processed_data['slug'] = objs.slug
        return processed_data


def update_crypto_details(crypto_data, session_cur, filters=None):
    if filters:
        filtered_quote = Quote.objects.none()
        filtered_crypto = Cryptocurrency.objects.none()

        if filters.get('name') is not None:
            filtered_quote.filter(currency_slug=filters.get('name').lower())
            filtered_crypto.filter(slug=filters.get('name').lower())

        if filters.get('num_market_pairs') is not None:
            filtered_crypto.filter(slug=filters.get('num_market_pairs'))

        if filters.get('circulating_supply') is not None:
            filtered_crypto.filter(circulating_supply=filters.get('circulating_supply'))

        if filters.get('total_supply') is not None:
            filtered_crypto.filter(total_supply=filters.get('total_supply'))

        if filters.get('max_supply') is not None:
            filtered_crypto.filter(max_supply=filters.get('max_supply'))

        filtered_crypto.filter(infinite_supply=filters.get('infinite_supply'))

        return filtered_crypto

    crypto_ids = []
    for current_crypto in crypto_data:
        quote_obj, created = Quote.objects.get_or_create(currency_slug=current_crypto.get('slug'))
        if quote_obj.data is not None and quote_obj.data.get(session_cur) is None:
            new_data = current_crypto.get('quote')
            quote_obj.data[str(session_cur)] = new_data.get(session_cur)
        else:
            quote_obj.data = current_crypto.get('quote')
        quote_obj.currency_symbol = current_crypto.get('symbol')
        quote_obj.save()

        try:
            crypto_obj = Cryptocurrency.objects.get(slug=current_crypto.get('slug'))
            crypto_obj.quote = quote_obj
        except ObjectDoesNotExist as e:
            crypto_obj = Cryptocurrency.objects.create(slug=current_crypto.get('slug'), quote=quote_obj)
        crypto_obj.name = current_crypto.get('name')
        crypto_obj.symbol = current_crypto.get('symbol')
        crypto_obj.num_market_pairs = current_crypto.get('num_market_pairs')
        crypto_obj.circulating_supply = current_crypto.get('circulating_supply')
        crypto_obj.total_supply = current_crypto.get('total_supply')
        crypto_obj.max_supply = current_crypto.get('max_supply')
        crypto_obj.infinite_supply = current_crypto.get('infinite_supply')
        crypto_obj.date_added = current_crypto.get('date_added')
        crypto_obj.last_updated = current_crypto.get('last_updated')

        crypto_ids.append(crypto_obj.pk)
        crypto_obj.save()

    saved_cryptos_queryset = Cryptocurrency.objects.filter(id__in=crypto_ids)
    return saved_cryptos_queryset
