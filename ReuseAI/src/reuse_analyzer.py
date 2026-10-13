from pathlib import Path
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
    ".sql",
}


IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "node_modules",
    ".idea",
    ".vscode",
}


def collect_source_files(project_path):
    root = Path(project_path)

    if not root.exists():
        return []

    source_root = (
        root / "source"
        if (root / "source").exists()
        else root
    )

    files = []

    for file in source_root.rglob("*"):

        if not file.is_file():
            continue

        if any(
            part in IGNORED_DIRECTORIES
            for part in file.parts
        ):
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        files.append(file)

    return files


def read_source(file_path):
    try:
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except Exception:
        return ""


def count_code_lines(text):

    lines = text.splitlines()

    count = 0

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith(
            ("#", "//", "/*", "*", "--")
        ):
            continue

        count += 1

    return max(count, 1)


def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def classify_score(score):

    if score >= 0.65:
        return "Direct Reuse"

    if score >= 0.45:
        return "Modify & Reuse"

    return "New Development"


def analyze_project(
    project_path,
    requirement
):

    files = collect_source_files(
        project_path
    )

    if not files:
        return {
            "project_path": str(project_path),
            "total_files": 0,
            "analyzed_files": 0,
            "total_loc": 0,
            "direct_loc": 0,
            "modify_loc": 0,
            "new_loc": 0,
            "estimated_reuse_coverage": 0.0,
            "max_similarity": 0.0,
            "components": [],
        }


    documents = []

    usable_files = []

    for file in files:

        content = read_source(file)

        if not content.strip():
            continue

        relative_path = str(
            file.relative_to(
                Path(project_path)
                / "source"
            )
        ) if (
            Path(project_path) / "source"
        ).exists() else str(
            file.relative_to(
                Path(project_path)
            )
        )

        searchable = (
            relative_path
            + "\n"
            + content
        )

        documents.append(
            clean_text(searchable)
        )

        usable_files.append(
            {
                "path": relative_path,
                "content": content,
                "loc": count_code_lines(content),
            }
        )


    if not documents:

        return {
            "project_path": str(project_path),
            "total_files": len(files),
            "analyzed_files": 0,
            "total_loc": 0,
            "direct_loc": 0,
            "modify_loc": 0,
            "new_loc": 0,
            "estimated_reuse_coverage": 0.0,
            "max_similarity": 0.0,
            "components": [],
        }


    # --------------------------------------------------------
    # FAST REAL TEXT SIMILARITY
    # --------------------------------------------------------

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=30000,
        sublinear_tf=True,
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    query_vector = vectorizer.transform(
        [clean_text(requirement)]
    )

    scores = cosine_similarity(
        query_vector,
        matrix
    )[0]


    components = []

    direct_loc = 0
    modify_loc = 0
    new_loc = 0
    total_loc = 0

    for index, item in enumerate(
        usable_files
    ):

        score = float(
            scores[index]
        )

        category = classify_score(
            score
        )

        loc = item["loc"]

        total_loc += loc

        if category == "Direct Reuse":

            direct_loc += loc

        elif category == "Modify & Reuse":

            modify_loc += loc

        else:

            new_loc += loc


        components.append(
            {
                "path": item["path"],
                "score": score,
                "category": category,
                "loc": loc,
            }
        )


    components.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    # --------------------------------------------------------
    # ESTIMATED REUSE COVERAGE
    #
    # Direct reuse = 100%
    # Modification = 50%
    # New development = 0%
    # --------------------------------------------------------

    if total_loc > 0:

        coverage = (
            direct_loc
            + (0.5 * modify_loc)
        ) / total_loc

    else:

        coverage = 0.0


    return {
        "project_path": str(project_path),
        "total_files": len(files),
        "analyzed_files": len(usable_files),
        "total_loc": total_loc,
        "direct_loc": direct_loc,
        "modify_loc": modify_loc,
        "new_loc": new_loc,
        "estimated_reuse_coverage": float(
            coverage
        ),
        "max_similarity": (
            float(max(scores))
            if len(scores)
            else 0.0
        ),
        "components": components,
    }
