from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Wallet, Transaction


@registry.register_document
class TransactionDocument(Document):
    from_wallet = fields.ObjectField(properties={
        'address': fields.TextField(),
        'amount': fields.FloatField(),
    })
    to_wallet = fields.ObjectField(properties={
        'address': fields.TextField(),
        'amount': fields.FloatField(),
    })

    class Index:
        name = 'transactions'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Transaction
        related_models = [Wallet]
        fields = [
            'id_external',
            'amount',
            'price',
            'gas',
            'gas_price',
            'created_on'
        ]
