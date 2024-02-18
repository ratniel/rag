from src.indexing_utils import load_docs, create_docstore


def retain_significant_nodes(nodes):
    """
    Retaining the nodes with size more than 100
    """
    greater_size_nodes = []
    for node in nodes:
        size = len(node.text)
        if size > 100:
            greater_size_nodes.append(node)
    return greater_size_nodes


if __name__=="__main__":
    nodes = load_docs(path="../../../storage/docstore/summary_node_with_embeddings", return_docstore=False)
    nodes = retain_significant_nodes(nodes)
    create_docstore(nodes, save_dir='../../../storage/docstore', store_name='summary_node_with_embeddings')
