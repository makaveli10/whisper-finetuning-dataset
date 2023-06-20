# Transcription Verification
The purpose of this is to verify the transcript from ```large-v2``` whisper and prepare data to fine tune a smaller whisper model with the custom dataset.

## Getting Started
### Local setup
- Clone this repo.
- Start simple http server
```bash
 cd transcription_verification
 python -m http.server
```
- Navigate to http://0.0.0.0:8000/
- Make your changes and click on ```save_changes``` to download the modified metadata.csv
- Commit your changes to this repo.

### Github Pages
- Or simply navigate to [whisper-finetuning-dataset github page](https://makaveli10.github.io/whisper-finetuning-dataset/). 
- Verify the dataset
- Save changes to download the modified metadata.csv