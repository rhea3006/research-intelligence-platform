

embedding_model = None

def get_model():
    global embedding_model

    if embedding_model is None:
        from sentence_transformers import SentenceTransformer

        embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            backend="onnx",
        )

    return embedding_model

def generate_embedding(text):
    """Generate a sentence embedding for the given text."""

    model = get_model()
    embedding = model.encode(text)

    return embedding
