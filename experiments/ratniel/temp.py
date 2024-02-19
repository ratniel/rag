import pickle
with open("./gemini_response.pkl", "rb") as file:
    response = pickle.load(file)
print(response)
print(response.candidates)
