from pathlib import Path
from typing import Dict, List

from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from constant import CHUNK_OVERLAP, CHUNK_SIZE, CHUNK_THRESHOLD


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class ChunkingUtils:
    def __init__(self) -> None:
        self.files: Dict[str, str] = {}
        self.chunks: Dict[str, List[Document]] = {}

        self.headers_to_split_on = [
            ("#", "document"),
            ("##", "section"),
            ("###", "subsection"),
        ]

        self.markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on,
            strip_headers=False,
        )

        self.chunk_threshold = CHUNK_THRESHOLD
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE"
            )

        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def load_files(self) -> Dict[str, str]:
        """Load all Markdown files from DATA_DIR."""
        if not DATA_DIR.exists():
            raise FileNotFoundError(
                f"Data directory does not exist: {DATA_DIR}"
            )
        self.files.clear()

        for file_path in sorted(DATA_DIR.glob("*.md")):
            self.files[file_path.stem] = file_path.read_text(
                encoding="utf-8"
            )

        return self.files

    def prepare_chunks(self) -> Dict[str, List[Document]]:
        """Split loaded Markdown files into searchable document chunks."""
        self.chunks.clear()

        for file_name, content in self.files.items():
            markdown_documents = self.markdown_splitter.split_text(content)
            final_chunks: List[Document] = []

            for document in markdown_documents:
                if len(document.page_content) > self.chunk_threshold:
                    chunks = self.recursive_splitter.split_documents(
                        [document]
                    )
                else:
                    chunks = [document]

                final_chunks.extend(chunks)

            self.chunks[file_name] = final_chunks

        return self.chunks


chunk_svc = ChunkingUtils()
