import time
from tqdm import tqdm
from src.indexing_utils import load_docs, create_docstore
from llama_index.embeddings.gemini import GeminiEmbedding


def load_nodes(docstore_path:str):
    """
    Load the nodes from doctore path.
    """
    nodes = load_docs(path=docstore_path, return_docstore=False)
    return nodes


def get_embeddings_in_node(nodes):
    """
    Get the embeddings of the nodes and store it in nodes embedding attribute itself and store the nodes.
    """
    embed_model = GeminiEmbedding(model_name='models/embedding-001')

    total_nodes = len(nodes)
    processed_nodes = 0

    for node in tqdm(nodes, desc="Processing nodes", unit="node", total=total_nodes):
        start_time = time.time()

        node.embedding = embed_model.get_text_embedding(node.metadata['summary'])

        processed_nodes += 1
        elapsed_time = time.time() - start_time
        eta_seconds = (total_nodes - processed_nodes) * elapsed_time / processed_nodes
        remaining_time = round(eta_seconds, 2) if eta_seconds > 0 else "Finished"
        tqdm.write(f"Processed {processed_nodes}/{total_nodes} nodes. Remaining time: {remaining_time} seconds.")
        time.sleep(3)

    create_docstore(nodes, save_dir='./storage/docstore', store_name='summary_node_with_embeddings')
    tqdm.write(f"Processed all {total_nodes} nodes.")


if __name__ == "__main__":
    docstore_path = "./storage/docstore/summary_nodes_modified"
    nodes = load_nodes(docstore_path=docstore_path)
    get_embeddings_in_node(nodes)

