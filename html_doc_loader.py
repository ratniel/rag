from llama_index import SimpleDirectoryReader

loader = SimpleDirectoryReader(input_dir="data/processed_html_data", recursive=True)

documents = loader.load_data()

print(documents[0].extra_info)