from PIL import Image

import torch

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

import os


# ==========================================
# CONFIG
# ==========================================

MODEL_NAME = os.getenv(

    "IMAGE_CAPTION_MODEL",

    "Salesforce/blip-image-captioning-base"
)

LOCAL_FILES_ONLY = (

    os.getenv(
        "HF_LOCAL_FILES_ONLY",
        "0"
    ) != "0"
)


# ==========================================
# SINGLETONS
# ==========================================

_processor = None

_model = None


# ==========================================
# MODEL LOADER
# ==========================================

def load_caption_model():

    global _processor
    global _model

    if _processor is None:

        _processor = BlipProcessor.from_pretrained(

            MODEL_NAME,

            local_files_only=LOCAL_FILES_ONLY
        )

    if _model is None:

        _model = BlipForConditionalGeneration.from_pretrained(

            MODEL_NAME,

            local_files_only=LOCAL_FILES_ONLY
        )

        _model.eval()

    return _processor, _model


# ==========================================
# GENERATE CAPTION
# ==========================================

def generate_caption(
    image_path: str
):

    try:

        processor, model = (
            load_caption_model()
        )

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = processor(

            image,

            return_tensors="pt"
        )

        with torch.no_grad():

            output = model.generate(

                **inputs,

                max_new_tokens=40
            )

        caption = processor.decode(

            output[0],

            skip_special_tokens=True
        )

        return caption.strip()

    except Exception as e:

        print(
            f"Caption generation failed: {e}"
        )

        return ""