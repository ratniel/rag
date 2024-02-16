import os
import time
import textwrap
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai
from src.indexing_utils import create_docstore
from src.indexing_utils import extract_htmltag_nodes
from google.generativeai import GenerationConfig
import pickle


def make_prompt(relevant_passage):
    """Creates prompt for summarising the passage provided. 

    Args:
        relevant_passage (string): passage to be provided for summarising.

    Returns:
        prompt: _description_
    """ 
    load_dotenv() 

    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))  

    # model = genai.GenerativeModel('gemini-pro')

    escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    prompt = textwrap.dedent("""You are an informative bot well versed in Ayurveda medicine and the content provided in the passage. \
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
    """).format(relevant_passage=escaped)

    return prompt


def process_nodes(nodes):
    # nodes = extract_htmltag_nodes('../../data/clean_html/Articles', tag_list=["p","section"])
    config = GenerationConfig(
    # max_output_tokens = 600,
    temperature= 0.6,
    top_p = 1,
    top_k = 1 ,
    )
    safety_settings = [{'category': 'HARM_CATEGORY_HARASSMENT', 'threshold': 'BLOCK_NONE'}, {'category': 'HARM_CATEGORY_HATE_SPEECH', 'threshold': 'BLOCK_NONE'}, {'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'threshold': 'BLOCK_NONE'}, {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'threshold': 'BLOCK_NONE'}]

    model = genai.GenerativeModel('gemini-pro', generation_config=config, safety_settings=safety_settings)

    total_nodes = len(nodes)
    processed_nodes = 0
    try:

        for node in tqdm(nodes, desc="Processing nodes", unit="node", total=total_nodes):
            prompt = make_prompt(node.text)

            start_time = time.time()

            answer = model.generate_content(prompt)
            node.metadata['summary'] = answer.text

            processed_nodes += 1
            elapsed_time = time.time() - start_time
            eta_seconds = (total_nodes - processed_nodes) * elapsed_time / processed_nodes
            remaining_time = round(eta_seconds, 2) if eta_seconds > 0 else "Finished"
            tqdm.write(f"Processed {processed_nodes}/{total_nodes} nodes. Remaining time: {remaining_time} seconds.")
            time.sleep(3)
    except Exception as e:
        with open("gemini_response.pkl", "wb") as pickle_file:
            pickle.dump(answer, pickle_file)


    create_docstore(nodes, save_dir='./storage', store_name='new_nodes')
    tqdm.write(f"Processed all {total_nodes} nodes.")
