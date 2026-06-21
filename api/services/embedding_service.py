from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    return model.encode(text)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) *np.linalg.norm(b))

embedding = model.encode("machine learning")

if __name__ == "__main__":

    machine_learning = generate_embedding("machine learning")

    deep_learning = generate_embedding( "deep learning")

    pizza = generate_embedding("pizza recipe")

    print(cosine_similarity(machine_learning,deep_learning))

    print(cosine_similarity(machine_learning,pizza))