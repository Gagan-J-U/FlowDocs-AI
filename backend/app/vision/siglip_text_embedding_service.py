from transformers import (
    AutoProcessor,
    AutoModel
)

import torch
import numpy as np
import os


MODEL_NAME = os.getenv(
    "IMAGE_EMBEDDING_MODEL",
    "google/siglip-base-patch16-224"
)

LOCAL_FILES_ONLY = (
    os.getenv(
        "HF_LOCAL_FILES_ONLY",
        "0"
    ) != "0"
)

DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

_processor = None
_model = None


def load_model():

    global _processor
    global _model

    if _processor is None:

        _processor = AutoProcessor.from_pretrained(
            MODEL_NAME,
            local_files_only=LOCAL_FILES_ONLY
        )

    if _model is None:

        _model = AutoModel.from_pretrained(
            MODEL_NAME,
            local_files_only=LOCAL_FILES_ONLY
        )

        _model.eval()
        _model.to(DEVICE)

    return _processor, _model


def generate_siglip_text_embedding(
    text: str
):
    """
    Backward-compatible wrapper.
    Existing code will continue working.
    """

    return generate_siglip_text_embeddings(
        [text]
    )[0]


def generate_siglip_text_embeddings(
    texts: list[str],
    batch_size: int = 32
):

    if not texts:
        return []

    processor, model = load_model()

    all_embeddings = []

    for start in range(
        0,
        len(texts),
        batch_size
    ):

        batch_texts = texts[
            start:start + batch_size
        ]

        inputs = processor(
            text=batch_texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(DEVICE)
            for key, value in inputs.items()
        }

        with torch.no_grad():

            outputs = model.get_text_features(
                **inputs
            )

        outputs = (
            outputs /
            outputs.norm(
                p=2,
                dim=1,
                keepdim=True
            )
        )

        all_embeddings.extend(
            outputs.cpu()
            .numpy()
            .astype(np.float32)
        )

    return all_embeddings