# 🎥 AI Video Assistant

A production-ready AI-powered tool that transcribes videos, generates summaries, extracts action items, and allows users to chat with meeting content using RAG (Retrieval-Augmented Generation).

---

## 🚀 Features

* 🎙️ Transcribe audio and video files locally
* 📝 Generate AI-powered meeting summaries
* ✅ Extract action items, decisions, and open questions
* 🔍 Chat with transcripts using RAG
* 📂 Support YouTube URLs and local files
* 📄 Export summaries and transcripts to PDF
* 💯 Mostly local execution with minimal cloud dependency

---

## 🎯 The Problem

Every professional sits through hours of meetings every week.

Unfortunately, most of the value gets lost once the meeting ends.

### ❌ No Notes Taken

Most people forget nearly 90% of what was discussed within an hour of the meeting ending.

### ❌ Action Items Lost

Tasks assigned during meetings often go untracked because nobody records them properly.

### ❌ Expensive Tools

Popular tools like Otter.ai and Fireflies charge $20–40/month for basic transcription and summarization.

### ❌ No Search Capability

Finding something discussed weeks ago often requires replaying the entire recording.

---

## 💡 The Solution

AI Video Assistant is a fully local AI-powered meeting assistant that handles everything after a meeting ends.

### 🎧 Input Any Audio

* YouTube URL
* MP4
* MP3
* WAV

### 🎙️ Auto Transcription

Whisper AI runs locally on your machine with no transcription API costs.

### 📋 Smart Summaries

Mistral AI generates concise bullet-point summaries.

### ✅ Action Item Extraction

Automatically identifies:

* Tasks
* Decisions
* Open Questions

### 🔎 RAG-Powered Q&A

Ask questions about your meeting at any time.

### 📄 Export Results

Download:

* Summaries
* Action Items
* Full Transcripts

---

## 🔄 Application Flow

```text
Audio / YouTube Input
          │
          ▼
Local Whisper Transcription
          │
          ▼
AI Summarization
          │
          ▼
Action Item Extraction
          │
          ▼
RAG with ChromaDB
          │
          ▼
Chat with Videos
          │
          ▼
Export Results
```

---

# 🛠️ Tech Stack

## OpenAI Whisper

**Transcription Engine**

* Runs completely locally
* Supports English, Hindi, and Hinglish
* Free and open-source

---

## LangChain LCEL

**AI Orchestration Framework**

* Modern Runnable-based architecture
* Pure LCEL implementation
* No legacy chains

---

## Mistral AI

**LLM (Free API Tier)**

* Summarization
* Translation
* Information extraction

---

## ChromaDB

**Vector Database**

* Stores transcript embeddings locally
* Enables semantic search
* Powers RAG-based chat

---

## Hugging Face Embeddings

**Embedding Model**

Model Used:

```python
all-MiniLM-L6-v2
```

Converts transcript chunks into vector embeddings for retrieval.

---

## yt-dlp + ffmpeg

**Audio Processing**

### yt-dlp

* Downloads audio from YouTube

### ffmpeg

* Converts audio into supported formats
* Audio preprocessing

---

## Streamlit

**Frontend Framework**

* Pure Python UI
* Chat interface
* Tabs and navigation
* File uploads and exports

---

## fpdf2

**PDF Export**

* Generates downloadable reports
* Exports summaries, action items, and transcripts

---

# 🏗️ System Architecture

```text
┌─────────────────┐
│   Audio Input   │
│ (YouTube/File)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Audio Processor │
│ yt-dlp + ffmpeg │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Whisper Model   │
│  Transcription  │
└────────┬────────┘
         │
         ├─────────────────────────────┐
         │                             │
         ▼                             ▼
┌─────────────────┐          ┌─────────────────┐
│   Translator    │          │  Text Splitter  │
│  Hindi→English  │          │ Chunk Transcript│
└────────┬────────┘          └────────┬────────┘
         │                            │
         ▼                            ▼
┌─────────────────┐          ┌─────────────────┐
│   Mistral LLM   │          │   Embeddings    │
│   (Free API)    │          │ HuggingFace     │
└────────┬────────┘          └────────┬────────┘
         │                            │
         ▼                            ▼
┌─────────────────┐          ┌─────────────────┐
│ Output Results  │          │    ChromaDB     │
│ Summary + Tasks │          │  Vector Store   │
└─────────────────┘          └────────┬────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │    RAG Chat     │
                            │ Ask Questions   │
                            │ About Meeting   │
                            └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ Export Results  │
                            │ PDF / TXT / CSV │
                            └─────────────────┘
```

---

# 🔧 Architecture Summary

| Component      | Technology                      |
| -------------- | ------------------------------- |
| Audio Input    | yt-dlp + ffmpeg                 |
| Speech-to-Text | Whisper                         |
| Summarization  | Mistral AI                      |
| Embeddings     | Hugging Face (all-MiniLM-L6-v2) |
| Vector Store   | ChromaDB                        |
| RAG Chat       | LangChain LCEL + ChromaDB       |
| UI             | Streamlit                       |
| Export         | fpdf2                           |

---

# 📌 Key Design Principle

Everything runs locally except the Mistral API calls used for LLM-powered tasks.

### Local Components

* Whisper Transcription
* Embeddings Generation
* ChromaDB Storage
* Retrieval Pipeline
* Streamlit UI

### Cloud Component

* Mistral AI (Summarization & Extraction)

This keeps costs low while maintaining powerful AI capabilities.

---


## 👨‍💻 Built With

Python • LangChain • Whisper • Mistral AI • ChromaDB • Hugging Face • Streamlit
