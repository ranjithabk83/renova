from pathlib import Path
import hashlib
import json

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".ts",
    ".cpp",
    ".c",
    ".h",
    ".cs",
    ".html",
    ".css",
    ".md",
    ".txt",
    ".json",
    ".sql"
}

IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    "dist",
    "build"
}


class ProjectSearcher:

    def __init__(self, project_folder: Path):

        self.project_folder = Path(project_folder)

        self.model = SentenceTransformer(MODEL_NAME)

        self.cache_dir = (
            self.project_folder / ".renova"
        )

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.embedding_file = (
            self.cache_dir / "embeddings.npy"
        )

        self.metadata_file = (
            self.cache_dir / "metadata.json"
        )

        self.files = self._collect_files()

        self.texts = []

        for file_path in self.files:

            try:

                text = file_path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                # Ignore extremely large files
                text = text[:30000]

                if text.strip():

                    self.texts.append({
                        "path": str(
                            file_path.relative_to(
                                self.project_folder
                            )
                        ),
                        "content": text
                    })

            except Exception:
                continue

        self.project_hash = self._create_hash()

        if self._cache_is_valid():

            self.embeddings = np.load(
                self.embedding_file
            )

        else:

            if self.texts:

                self.embeddings = self.model.encode(
                    [
                        item["content"]
                        for item in self.texts
                    ],
                    normalize_embeddings=True,
                    show_progress_bar=True,
                    batch_size=32
                )

                np.save(
                    self.embedding_file,
                    self.embeddings
                )

                with open(
                    self.metadata_file,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        {
                            "model_name": MODEL_NAME,
                            "project_hash": self.project_hash,
                            "records": len(self.texts)
                        },
                        f,
                        indent=2
                    )

            else:

                self.embeddings = np.empty(
                    (0, 384)
                )

    def _collect_files(self):

        collected = []

        if not self.project_folder.exists():
            return collected

        for path in self.project_folder.rglob("*"):

            if not path.is_file():
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if path.suffix.lower() in SUPPORTED_EXTENSIONS:

                collected.append(path)

        return collected

    def _create_hash(self):

        values = []

        for item in self.texts:

            values.append(
                item["path"]
            )

            values.append(
                item["content"]
            )

        return hashlib.sha256(
            "\n".join(values).encode("utf-8")
        ).hexdigest()

    def _cache_is_valid(self):

        if not self.embedding_file.exists():
            return False

        if not self.metadata_file.exists():
            return False

        try:

            with open(
                self.metadata_file,
                "r",
                encoding="utf-8"
            ) as f:

                metadata = json.load(f)

            if metadata.get("model_name") != MODEL_NAME:
                return False

            if metadata.get("project_hash") != self.project_hash:
                return False

            if metadata.get("records") != len(self.texts):
                return False

            embeddings = np.load(
                self.embedding_file,
                mmap_mode="r"
            )

            return (
                len(embeddings)
                == len(self.texts)
            )

        except Exception:

            return False

    def search(self, query: str, k: int = 5):

        if not self.texts:
            return []

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )[0]

        scores = (
            np.asarray(self.embeddings)
            @ query_embedding
        )

        indices = np.argsort(-scores)[:k]

        results = []

        for index in indices:

            item = self.texts[int(index)]

            results.append({
                "path": item["path"],
                "content": item["content"],
                "score": float(
                    scores[index]
                )
            })

        return results