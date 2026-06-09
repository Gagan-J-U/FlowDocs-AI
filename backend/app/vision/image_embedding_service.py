from PIL import Image

import numpy as np
import torch
import os

from transformers import (
    AutoProcessor,
    AutoModel
)

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


def generate_image_embedding(
    image_path: str
):

    embeddings = generate_image_embeddings(
        [image_path]
    )

    return embeddings[0]


def generate_image_embeddings(
    image_paths: list[str],
    batch_size: int = 16
):

    processor, model = load_model()

    all_embeddings = []

    for start in range(
        0,
        len(image_paths),
        batch_size
    ):

        batch_paths = image_paths[
            start:start + batch_size
        ]

        images = [

            Image.open(path)
            .convert("RGB")

            for path in batch_paths
        ]

        inputs = processor(
            images=images,
            return_tensors="pt"
        )

        inputs = {

            k: v.to(DEVICE)

            for k, v in inputs.items()
        }

        with torch.no_grad():

            outputs = (
                model.get_image_features(
                    **inputs
                )
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