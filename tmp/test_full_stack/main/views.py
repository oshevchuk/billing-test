from django.core import serializers
from django.http import JsonResponse
from .models import Plan, AccountConnector

billing_number_prices = {'0': 0, '100': 50, '200': 75, '500': 150, '1000': 250}
billing_crawls_multiplier = {'1': 1, '2': 2, '4': 3, '8': 5, '30': 15}

accounts_prices = {'0': 0, '1': 10, '2': 17.5, '5': 30, '10': 50}


def scanner_read(request, id):
    raw_data = serializers.serialize('python', Plan.objects.filter(pk=id))
    if raw_data:
        actual_data = [d['fields'] for d in raw_data]
    else:
        actual_data = {'status': "error", "err":"no such billing"}
    return JsonResponse(actual_data, safe=False)


def scanner_create(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    number_of_products = data.get("number_of_products")
    crawls_per_month = data.get("crawls_per_month")
    err = []
    if not number_of_products or not number_of_products.isdigit():
        err.append("number_of_products field required numeric")
    if not crawls_per_month or not crawls_per_month.isdigit():
        err.append("crawls_per_month field required numeric")

    elif not number_of_products in billing_number_prices:
        err.append("no such plan")
    elif not crawls_per_month in billing_crawls_multiplier:
        err.append("no such plan")
    if err:
        return JsonResponse({'status': "error", "err":err})
    else:
        w = Plan(number_of_products=number_of_products, crawls_per_month=crawls_per_month)
        w.final_price = billing_number_prices[number_of_products] * billing_crawls_multiplier[crawls_per_month]
        w.save()
        return JsonResponse({'status': "ok", "id": w.id})


def scanner_update(request, id):
    err = []
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    try:
        plan = Plan.objects.get(pk=id)
    except Plan.DoesNotExist:
        err = ["no such object"]
    print(data)
    number_of_products = data.get("number_of_products")
    crawls_per_month = data.get("crawls_per_month")
    if number_of_products:
        if number_of_products.isdigit():
            if not number_of_products in billing_number_prices:
                err.append("no such plan")
            else:
                plan.number_of_products = number_of_products
        else:
            err.append("number_of_products must be numeric")
    if crawls_per_month:
        if crawls_per_month.isdigit():
            if not crawls_per_month in billing_crawls_multiplier:
                err.append("no such plan")
            else:
                plan.crawls_per_month = crawls_per_month
        else:
            err.append("crawls_per_month must be numeric")

    if err:
        return JsonResponse({'status': "error", 'err': err}, safe=False)
    else:
        plan.final_price = billing_number_prices[str(plan.number_of_products)] * billing_crawls_multiplier[str(plan.crawls_per_month)]
        plan.save()
        return JsonResponse({'status': "ok", 'id': id}, safe=False)


def connector_read(request, id):
    raw_data = serializers.serialize('python', AccountConnector.objects.filter(pk=id))
    if raw_data:
        actual_data = [d['fields'] for d in raw_data]
    else:
        actual_data = {'status': "error", "err": "no such connector"}
    return JsonResponse(actual_data, safe=False)


def connector_create(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    connected_accounts = data.get("connected_accounts")
    err = []
    if not connected_accounts or not connected_accounts.isdigit():
        err.append("connected_accounts field required numeric")

    elif not connected_accounts in accounts_prices:
        err.append("no such plan")
    if err:
        return JsonResponse({'status': "error", "err":err})
    else:
        w = AccountConnector(connected_accounts=connected_accounts)
        w.final_price = accounts_prices[connected_accounts]
        w.save()
        return JsonResponse({'status': "ok", "id": w.id})


def connector_update(request, id):
    err = []
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    try:
        plan = AccountConnector.objects.get(pk=id)
    except Plan.DoesNotExist:
        err = ["no such object"]

    connected_accounts = data.get("connected_accounts")

    if connected_accounts:
        if not connected_accounts in accounts_prices:
            err.append("no such plan")
        elif connected_accounts.isdigit():
            plan.connected_accounts = connected_accounts
            plan.final_price = accounts_prices[connected_accounts]
        else:
            err.append("connected_accounts must be numeric")
    if err:
        return JsonResponse({'status': "error", 'err': err}, safe=False)
    else:
        plan.save()
        return JsonResponse({'status': "ok", 'id': id}, safe=False)
