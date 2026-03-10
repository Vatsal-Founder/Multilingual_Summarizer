# Multilingual Summarizer — mT5 (Hindi • English • French)

An end‑to‑end **MLOps** project that fine‑tunes **`csebuetnlp/mT5_multilingual_XLSum`** for multilingual abstractive summarization and serves a **Flask** app where users paste an article in **Hindi, English, or French** and receive a concise summary.

> Repo: `Vatsal-Founder/Multilingual_Summarizer` — modular codebase with configs, pipelines, and CI workflows.
> Base model: mT5 fine‑tuned on **XL‑Sum** (45 languages).

[![HuggingFace Model](https://img.shields.io/badge/🤗%20Model-vatsal18/multi--lang__summay-blue)](https://huggingface.co/vatsal18/multi-lang_summay)


---

## Highlights

* 🌍 **Multilingual input**: Hindi, English, and French (extensible to other XL‑Sum languages).
* 🧠 **Fine‑tuned mT5**: starts from `csebuetnlp/mT5_multilingual_XLSum` and adapts to your settings.
* 🧱 **Modular pipelines**: ingestion → preprocessing → training → evaluation → packaging.
* 🚀 **Serve with Flask**: paste text → get summary; simple HTML templates included.
* 🔁 **Reproducible runs**: config‑driven via YAML; logs and artifacts saved per run.
* 🔄 **Workflows**: GitHub Actions for CI (lint/test/build) and optional containerization.

---

## Architecture

<img width="1536" height="1024" alt="ChatGPT Image Mar 9, 2026 at 04_48_42 PM" src="https://github.com/user-attachments/assets/95124dfa-b892-4554-b4e9-b0dd3d7faea8" />


---

## Project structure

```
.
├── .github/workflows/        # CI pipelines
├── config/                   # config.yaml and stage configs
├── logs/                     # training/inference logs
├── research/                 # notebooks / experiments
├── src/                      # package: components & pipelines
├── templates/                # Flask HTML templates
├── app.py                    # Flask app (serve summaries)
├── main.py                   # pipeline runner / orchestrator
├── params.yaml               # hyperparams & run settings
├── Dockerfile                # container image (optional)
├── requirements.txt          # Python dependencies
└── README.md                 # this file
```

---

## Module‑by‑module

**1) Data Ingestion**

* Accepts pasted text or dataset samples; optional language tag (hi/en/fr).

**2) Preprocessing / Transformation**

* Cleans HTML/whitespace, normalizes punctuation, truncates to max length, and prepares input/output pairs for seq2seq fine‑tuning.

**3) Model Trainer**

* Loads tokenizer + `AutoModelForSeq2SeqLM` from `csebuetnlp/mT5_multilingual_XLSum`.
* Trains with params from `params.yaml` (batch size, lr, epochs, max\_length, beam size, etc.).

**4) Evaluation**

* Computes ROUGE‑1/2/L and length metrics per language; logs per‑run scores.

**5) Packaging / Registry**

* Saves the fine‑tuned weights, tokenizer, and a `config.json` for the Flask app to consume.

**6) Serving (`app.py`)**

* Flask endpoint renders a form where you select a language (Hindi/English/French) and paste content.
* Returns a concise abstractive summary.

---

## Quick Start

### 1) Setup

```bash
git clone https://github.com/Vatsal-Founder/Multilingual_Summarizer.git
cd Multilingual_Summarizer
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure

Edit **`config/config.yaml`** and **`params.yaml`** to set model paths and hyperparameters (train/val splits, max lengths, learning rate, batch size, epochs). If you use a remote tracker, export its URI/envs.

### 3) Train / Fine‑tune

```bash
# end‑to‑end pipeline
python main.py

# or run by stage (examples)
python main.py --stage ingest
python main.py --stage transform
python main.py --stage train
python main.py --stage evaluate
```

Artifacts (model + tokenizer) are saved to the configured `artifacts/` path.

### 4) Run the Flask app

```bash
python app.py
```

Visit **[http://localhost:5000](http://localhost:5000)**. Paste an article (Hindi/English/French) and click **Summarize**.

---

## Configuration reference (minimal)

```yaml
# params.yaml (illustrative)
model_name: csebuetnlp/mT5_multilingual_XLSum
max_input_length: 2048
max_target_length: 128
batch_size: 4
learning_rate: 3e-5
epochs: 3
beam_size: 4
lang_supported: [hi, en, fr]
```

---

## Docker (optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build & run:

```bash
docker build -t multilingual-summarizer .
docker run -p 5000:5000 multilingual-summarizer
```

---

## Notes

* Base model **mT5‑multilingual‑XLSum** is trained on **XL‑Sum** (45 languages); this app focuses on **Hindi/English/French**, but you can enable more by updating `lang_supported` and tokenizer settings.
* For long inputs, the app uses chunking/length limits from `params.yaml` to keep inference stable.

---

## License

GPL‑3.0 © Vatsal Founder
