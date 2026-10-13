from pathlib import Path
import pickle

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


class SemanticSearcher:

    def __init__(self, csv_path: Path):

        self.csv_path = Path(csv_path)

        # ----------------------------------------------------
        # REAL CODESEARCHNET DATA
        # ----------------------------------------------------

        self.df = pd.read_csv(
            self.csv_path
        ).fillna("")

        self.df["search_text"] = (
            self.df["docstring"].astype(str)
            + "\n"
            + self.df["summary"].astype(str)
            + "\n"
            + self.df["func_name"].astype(str)
            + "\n"
            + self.df["code"].astype(str)
        )

        # ----------------------------------------------------
        # CACHE
        # ----------------------------------------------------

        project_root = self.csv_path.parent.parent

        cache_dir = (
            project_root
            / "models"
        )

        cache_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.cache_file = (
            cache_dir
            / "fast_semantic_index.pkl"
        )

        # ----------------------------------------------------
        # LOAD EXISTING INDEX
        # ----------------------------------------------------

        if self.cache_file.exists():

            print(
                "Loading saved semantic index..."
            )

            with open(
                self.cache_file,
                "rb"
            ) as file:

                saved = pickle.load(
                    file
                )

            self.vectorizer = (
                saved["vectorizer"]
            )

            self.svd = (
                saved["svd"]
            )

            self.document_vectors = (
                saved["document_vectors"]
            )

            print(
                "Semantic index loaded."
            )

        else:

            print(
                "Building fast semantic index..."
            )

            # ------------------------------------------------
            # TF-IDF
            # ------------------------------------------------

            self.vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                max_features=30000,
                ngram_range=(1, 2),
                min_df=1
            )

            tfidf = (
                self.vectorizer.fit_transform(
                    self.df["search_text"]
                )
            )

            # ------------------------------------------------
            # LATENT SEMANTIC ANALYSIS
            # ------------------------------------------------

            components = min(
                100,
                max(
                    2,
                    tfidf.shape[1] - 1
                )
            )

            self.svd = TruncatedSVD(
                n_components=components,
                random_state=42
            )

            self.document_vectors = (
                self.svd.fit_transform(
                    tfidf
                )
            )

            # Normalize document vectors
            norms = np.linalg.norm(
                self.document_vectors,
                axis=1,
                keepdims=True
            )

            norms[norms == 0] = 1

            self.document_vectors = (
                self.document_vectors
                / norms
            )

            # ------------------------------------------------
            # SAVE INDEX
            # ------------------------------------------------

            saved = {
                "vectorizer": self.vectorizer,
                "svd": self.svd,
                "document_vectors":
                    self.document_vectors,
                "records":
                    len(self.df)
            }

            with open(
                self.cache_file,
                "wb"
            ) as file:

                pickle.dump(
                    saved,
                    file
                )

            print(
                "Fast semantic index saved."
            )


    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query: str,
        k: int = 5
    ):

        query = str(
            query
        ).strip()

        if not query:

            return []


        # ----------------------------------------------------
        # Query -> TF-IDF
        # ----------------------------------------------------

        query_tfidf = (
            self.vectorizer.transform(
                [query]
            )
        )


        # ----------------------------------------------------
        # Query -> LSA SPACE
        # ----------------------------------------------------

        query_vector = (
            self.svd.transform(
                query_tfidf
            )
        )[0]


        norm = np.linalg.norm(
            query_vector
        )

        if norm != 0:

            query_vector = (
                query_vector
                / norm
            )


        # ----------------------------------------------------
        # COSINE SIMILARITY
        # ----------------------------------------------------

        scores = (
            self.document_vectors
            @ query_vector
        )


        # ----------------------------------------------------
        # TOP RESULTS
        # ----------------------------------------------------

        indices = np.argsort(
            -scores
        )[:k]


        results = []

        for index in indices:

            index = int(
                index
            )

            result = (
                self.df
                .iloc[index]
                .to_dict()
            )

            result["score"] = float(
                scores[index]
            )

            results.append(
                result
            )

        return results
