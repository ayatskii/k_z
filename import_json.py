import json
from django.apps import apps

with open('data_dump.json', encoding='utf-8') as f:
    data = json.load(f)

skip_models = {'auth.permission', 'contenttypes.contenttype'}

for obj in data:
    model_label = obj['model']
    if model_label in skip_models:
        continue 

    Model = apps.get_model(model_label.split('.')[0], model_label.split('.')[1])
    fields = obj['fields']
    pk = obj['pk']

    m2m_fields = {}
    for field in list(fields.keys()):
        if isinstance(fields[field], list):
            m2m_fields[field] = fields.pop(field)

    instance, created = Model.objects.update_or_create(defaults=fields, pk=pk)

    for field, value in m2m_fields.items():
        getattr(instance, field).set(value)
