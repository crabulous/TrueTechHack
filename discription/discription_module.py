from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from deep_translator import GoogleTranslator
import openai

openai.api_key = "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"

model = VisionEncoderDecoderModel.from_pretrained('nlpconnect/vit-gpt2-image-captioning')
feature_extractor = ViTImageProcessor.from_pretrained('./model_image_captioning')
tokenizer = AutoTokenizer.from_pretrained('./model_image_captioning')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}


def predict_step(frames):
    descriptions = {"scene":
                        []
                    }

    for scene in frames["segments"]:
        tmp = {
            "start": scene["start"],
            "end": scene["end"]
        }

        images = scene["frames"]

        if len(images) == 0:
            break

        pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        output_ids = model.generate(pixel_values, **gen_kwargs)

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)

        preds = GoogleTranslator(source='en', target='ru').translate_batch([pred.strip() for pred in preds])

        tmp["comment"] = generate_summary(preds)

        descriptions["scene"].append(tmp)
    return descriptions


def generate_summary(lst):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Кратко и по существу сгенерируй описание событий по списку {lst}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.2,
    )
    return response.choices[0].text.strip()
