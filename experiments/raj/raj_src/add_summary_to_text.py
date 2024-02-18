from src.indexing_utils import load_docs


def add_summary_to_text(nodes):
    for node in nodes:
        node.text = node.metadata['summary'] + node.text
    return nodes


if __name__ == "__main__":
    nodes = load_docs(path="../../../storage/docstore/summary_node_with_embeddings", return_docstore=False)
    nodes = add_summary_to_text(nodes)