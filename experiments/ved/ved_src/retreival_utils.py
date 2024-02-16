from src.indexing_utils import load_docs, create_docstore


def swap_summary_text(nodes):
    """
    Swap the summary and text of the nodes. Nodes need to contain the metadata key 'is_summary_swapped'. 
    Make sure to add this key to the nodes before calling this function. 
    """
    for node in nodes:
        node.metadata['summary'], node.text = node.text, node.metadata['summary']
        node.metadata['is_summary_swapped'] = not node.metadata['is_summary_swapped']
    return nodes