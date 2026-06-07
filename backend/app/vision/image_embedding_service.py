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


def generate_image_embedding(
    image_path: str
):

    processor, model = load_model()

    image = Image.open(
        image_path
    ).convert("RGB")

    inputs = processor(

        images=image,

        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.get_image_features(
            **inputs
        )

    embedding = outputs[0]

    embedding = (
        embedding /
        embedding.norm(
            p=2
        )
    )

    return embedding.cpu().numpy().astype(
        np.float32
    )