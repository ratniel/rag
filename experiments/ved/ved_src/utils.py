import os
import textwrap
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
from llama_index.core.storage.docstore import SimpleDocumentStore

load_dotenv()

#TODO: In promt add "If you cant summarize the text then just say NO and nothing else"
def make_prompt(relevant_passage):
    """Creates prompt for summarising the passage provided.

    Args:
        relevant_passage (string): passage to be provided for summarising.

    Returns:
        prompt: prompt generated for summarising `relevant passage`
    """

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # model = genai.GenerativeModel('gemini-pro')

    escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = textwrap.dedent(
        """You are an informative bot well versed in Ayurveda medicine and the content provided in the passage. \
    You answer questions using text from the reference passage included below. \
    There are a lot of complicated ayurveda terminlogies used in the reference passage provided. \
    Be sure to respond in a complete sentence, being comprehensive, including all relevant information. \
    Make sure to respond in plain text only DO NOT USE MARKDOWN and use simple english language without using any complicated words. \
    I have no prior knowledge about ayurveda, medicine or anything related to it. \
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
    strike a friendly and converstional tone while being to the point with the queries. \
    Use technical jargons and make sure to provide meaning in parantheses. \
    If the passage is irrelevant to the answer, you may ignore it. You may also ignore any csv data provided. \
    The answer to the query is mostly present in the reference passage provided. Go through the passage thoroughly and fetch relevant information. \
    Strictly limit your responses to 300 words. \
    Summarise the information provided in the reference passage comprehensively. \
    The summary should include all the important points provided in the passage. No information loss should happen at any cost. 
    PASSAGE: '{relevant_passage}'

        ANSWER:
    """
    ).format(relevant_passage=escaped)

    return prompt


def create_docstore(nodes, save_dir: str, store_name: str) -> None:
    """
    Create a document store and save it to the specified directory.

    Args:
        nodes (List[str]): List of nodes to be added to the document store.
        save_dir (str): Directory path where the document store will be saved.
        store_name (str): Name of the document store file.

    Returns:
        None
    """
    docstore = SimpleDocumentStore()
    docstore.add_documents(nodes)
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    docstore.add_documents(nodes)
    docstore.persist(persist_path=save_dir / store_name)
    return docstore


def load_docs(path, return_docstore: bool = False):
    """
    Load documents from the specified path.

    Args:
        path (str): The path to the document store.
        return_docstore (bool, optional): Whether to return the document store object instead of the loaded documents. Defaults to False.

    Returns:
        list or SimpleDocumentStore: A list of loaded documents if return_docstore is False, otherwise the document store object.
    """
    docstore = SimpleDocumentStore.from_persist_path(persist_path=path)
    if return_docstore:
        return docstore
    else:
        return list(docstore.docs.values())
