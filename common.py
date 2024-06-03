from collections import namedtuple

Dataset = namedtuple('Dataset', ['name', 'metadata_id', 'description'])

DATASETS = [
    Dataset(name='Consumer Spending', metadata_id='consumer-spending', 
            description='Consumer credit and debit card spending, seasonally adjusted change since January 2020'),
    Dataset(name='Employment', metadata_id='employment',
            description='Number of active employees, change since January 2020'),
    Dataset(name='Initial Unemployment Claims', metadata_id='unemployment-claims',
            # description='Number of initial claims per 100 people in the 2019 labor force, combining Regular and PUA claims, weekly'
            description='Number of initial claims per 100 people in the 2019 labor force, weekly'),  # Currently regular only
    Dataset(name='Continued Unemployment Claims', metadata_id='unemployment-claims',
            # description='Number of continued claims per 100 people in the 2019 labor force, combining Regular, PUA and PEUC claims, weekly'
            description='Number of continued claims per 100 people in the 2019 labor force, weekly'),  # Currently regular only
]

DATASET_MAP = {d.name: d for d in DATASETS}
