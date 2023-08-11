from django.core.cache import cache
from .models import CapFeedAlert



def calculate_alert(alert):
    alert_data = alert.to_dict()
    alert_data['info'] = []
    for info in alert.capfeedalertinfo_set.all():
        info_data = info.to_dict()
        info_data['parameter'] = []
        parameters = info.capfeedalertinfoparameter_set.all()
        for parameter in parameters:
            parameter_data = parameter.to_dict()
            info_data['parameter'].append(parameter_data)
        info_data['area'] = []
        areas = info.capfeedalertinfoarea_set.all()
        for area in areas:
            area_data = area.to_dict()
            area_data['polygon'] = []
            for polygon in area.capfeedalertinfoareapolygon_set.all():
                polygon_data = polygon.to_dict()
                area_data['polygon'].append(polygon_data)
            area_data['circle'] = []
            for circle in area.capfeedalertinfoareacircle_set.all():
                circle_data = circle.to_dict()
                area_data['circle'].append(circle_data)
            area_data['geocode'] = []
            for geocode in area.capfeedalertinfoareageocode_set.all():
                geocode_data = geocode.to_dict()
                area_data['geocode'].append(geocode_data)
            info_data['area'].append(area_data)
        alert_data['info'].append(info_data)

    cache.set("alert" + str(alert.id), alert_data, timeout = None)
    return alert_data

def initialise_alerts_cache():
    alerts_data = {'alerts': []}
    alerts = CapFeedAlert.objects.all()
    for alert in alerts:
        alert_data = calculate_alert(alert)
        alerts_data['alerts'].append(alert_data)
    cache.set("alerts", alerts_data, timeout = None)

def get_alert(alert_id):
    alert_cache_key = "alert" + str(alert_id)
    return cache.get(alert_cache_key, {})

def get_alerts():
    alerts_cache_key = "alerts"
    return cache.get(alerts_cache_key, {})

def update_alerts_cache(alert_id, update):
    alert = CapFeedAlert.objects.get(id=alert_id)
    alerts_cache_key = "alerts"
    alerts_data = cache.get(alerts_cache_key, {})
    if update:
        alert_data = calculate_alert(alert)
        alerts_data['alerts'].append(alert_data)
        cache.set("alerts", alerts_data, timeout = None)
    else:
        for index, alert_data in enumerate(alerts_data['alerts']):
            if alert_data['id'] == alert_id:
                alerts_data['alerts'].pop(index)
                cache.set("alerts", alerts_data, timeout = None)
                break