import pandas as pd
from numpy import array
from openai.embeddings_utils import cosine_similarity


class SimpleDataStore():
    def __init__(self, csv):
        self.datafile_path = csv
        self.df = pd.read_csv(self.datafile_path)
        self.df["embedding"] = self.df.embedding.apply(eval).apply(array)

    def search(self, embedding: list[float], n: int = 5) -> list[zip]:
        self.df["similarity"] = self.df.embedding.apply(
            lambda x: cosine_similarity(x, embedding))
        results_df = self.df.sort_values("similarity", ascending=False).head(n)

        return list(zip(results_df["name"], results_df["combined"]))

if __name__ == '__main__':
    import os
    import openai
    from openai.embeddings_utils import get_embedding
    from dotenv import load_dotenv

    load_dotenv()
    datafile_path = "data/red_wines_filtered_with_embeddings.csv"
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    d = SimpleDataStore(csv=datafile_path)

    # Test with first wine in csv
    #test = "Land: Italien; Druvor: Primitivo, Malvasía, Negroamaro; Smak: Kryddigt & Mustigt. Kryddig smak med fatkaraktär, inslag av mörka körsbär, choklad, romrussin, peppar och vanilj.; Servering: Serveras till rätter av lamm- eller nötkött, gärna grillat.; Fruktsyra: 9 (0-12); Fyllighet: 9 (0-12); Strävhet: 8 (0-12)"
    #embedding = get_embedding(test, engine="text-embedding-ada-002")
    #top_5_similar = d.search(embedding=embedding, n=5)
    #print(top_5_similar)

    # Test with comma separated keywords
    #comma_separated_keywords = "red wine, fruity, lamb, Italy"
    #embedding = get_embedding(comma_separated_keywords, engine="text-embedding-ada-002")
    #top_10_similar = d.search(embedding=embedding, n=5)
    #for t in top_10_similar:
    #    print("Namn: " + t[0] + "; " + t[1])
