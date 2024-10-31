import warnings
from flask import Flask, request, jsonify
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
import os
import uuid 

# Ignore warnings
warnings.filterwarnings("ignore")

# Set up Flask application
app = Flask(__name__)

# Device and dtype configuration
device = torch.device('cpu')
torch_dtype = torch.float32

# Load the pre-downloaded model and processor
local_model_dir = "./whisper_large_model"
model = AutoModelForSpeechSeq2Seq.from_pretrained(local_model_dir, torch_dtype=torch_dtype)
model.to(device)

processor = AutoProcessor.from_pretrained(local_model_dir)

# Set up the speech recognition pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.wav'):
        # Save the uploaded file to a temporary location
        unique_filename = f"{uuid.uuid4()}.wav"
        temp_file_path = f"./{unique_filename}"

        # Save the uploaded file to the generated unique file path
        file.save(temp_file_path)

        # Use the pipeline to transcribe the audio
        result = pipe(temp_file_path, generate_kwargs={"language": "german"})
        # Remove the temporary file after processing
        os.remove(temp_file_path)
        return jsonify(result)
    else:
        return jsonify({'error': 'File is not a .wav file'}), 400

@app.route('/alive', methods=['GET'])
def alive():
    return "alive", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
