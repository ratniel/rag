from rag.rag_utils import load_docs

nodes = load_docs("/home/dai/35/rag/storage/Articles_with_summary", return_docstore=False)

#check how many nodes do not containe metadata['summary']
count = 0
for node in nodes:
    if 'summary' not in node.metadata:
        count += 1
print(count)