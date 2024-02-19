import pickle
with open("/home/dai/35/rag/gemini_response.pkl", "rb") as file:
    response = pickle.load(file)
print(response)
print(response.candidates)
