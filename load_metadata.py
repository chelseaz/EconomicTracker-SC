from bs4 import BeautifulSoup, NavigableString

from common import *

metadata_path = 'EconomicTracker/docs/'
with open(f'{metadata_path}/oi_tracker_data_documentation.md', 'r') as f:
    data_doc_html = f.read()

soup = BeautifulSoup(data_doc_html)

def get_doc(dataset_id):
    header_tag = soup.select(f"#{dataset_id}")
    if len(header_tag) == 0:
        return None

    header_tag = header_tag[0]
    section_tags = []
    for element in header_tag.next_siblings:
        if isinstance(element, NavigableString):
            continue
        if element.name == 'h2':
            break
        section_tags.append(element)
    
    return '\n'.join([str(t) for t in section_tags])

dataset_to_doc = dict()
for dataset_id in set([d.metadata_id for d in DATASETS]):
    dataset_to_doc[dataset_id] = get_doc(dataset_id)
