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

    return _processor, _model


def generate_siglip_text_embedding(
    text: str
):

    processor, model = load_model()

    inputs = processor(
        text=[text],
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():

        embedding = model.get_text_features(
            **inputs
        )

    embedding = embedding[0]

    embedding = (
        embedding /
        embedding.norm(p=2)
    )

    return embedding.cpu().numpy().astype(
        np.float32
    )