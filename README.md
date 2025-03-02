# FitSmart AI: Your AI-Powered Fitness Coach

## Overview
Welcome to **FitSmart AI**, your witty, supportive, and highly personalized AI fitness coach! Built with cutting-edge technologies, FitSmart AI helps users craft tailored workout and nutrition plans based on their fitness goals, levels, health conditions, and lifestyle constraints. Whether you’re a beginner looking to lose weight or an advanced athlete aiming to maintain strength, FitSmart AI is here to cheer you on and crush your fitness journey!

This project leverages **Streamlit** for an interactive UI, **LangChain** for AI logic, **Ollama** (with **Llama 3.2** or **deepseek-r1:3b**) for natural language processing, and an **InMemoryVectorStore** for retrieval-augmented generation (RAG) using fitness and nutrition datasets. It’s designed to be classy, engaging, and user-friendly, inspired by the sleek, playful vibe of **Grok AI**.

---

## Features
✅ **Personalized Workouts**: Generates step-by-step workout plans with exercises, durations, intensities, and calorie burns, tailored to your fitness level, goals (e.g., weight loss, muscle gain), and health conditions (e.g., diabetes, hypertension).

✅ **Nutrition Guidance**: Offers optional diet plans (vegetarian, non-vegetarian) and hydration tips, drawing from extensive nutrition datasets for goals like endurance or recovery.

✅ **Engaging Conversations**: Uses a witty, supportive tone to guide users through 2–3 exchanges, asking for details like age, weight, and preferences before delivering plans.

✅ **Safety-First Design**: Prioritizes health safety, flagging risks and recommending consultations with fitness experts or healthcare professionals for medical conditions.

✅ **Scalable and Lightweight**: Runs on open-source tools, optimized for small-scale deployment with fast response times (~2–3 seconds) via InMemoryVectorStore.

---

## Installation

### Prerequisites
- **Python 3.9** or higher
- **Git** (for cloning the repository)
- **Ollama** installed and running locally ([Download from ollama.ai](https://ollama.ai))
- **Streamlit, LangChain, and related libraries** (install via pip)

### Steps
#### 1️⃣ Clone the Repository:
```bash
git clone https://github.com/your-username/fitsmart-ai.git
cd fitsmart-ai
```

#### 2️⃣ Install Dependencies:
```bash
pip install streamlit langchain-ollama ollama
```

#### 4️⃣ Prepare Datasets:
- Download or create the following files:
  - `fitness_knowledge_base.txt`
  - `diet_knowledge_base.txt`
  - `nutrition_health_exceptions_dataset.txt`
- Place them in the project directory.
- Ensure **UTF-8 encoding** for all `.txt` files to avoid character issues.

#### 5️⃣ Run the Application:
```bash
streamlit run app.py
```
(Replace `app.py` with your main Python file name, e.g., `fitsmart_ai.py`.)

---

## Usage
1. Open your web browser to the Streamlit URL (default: `http://localhost:8501`).
2. Use the chat interface to input fitness-related queries (e.g., *“I’m new to fitness and want to start working out”*).
3. FitSmart AI will ask for your **age, weight, fitness level, and goals**, refine with one follow-up (e.g., health conditions), and deliver a **personalized workout and nutrition plan** in 2–3 exchanges.
4. Enjoy a **classy, witty experience** with recommendations drawn from the **fitness and nutrition datasets**!

---


---

## 📦 Dependencies
```text
streamlit>=1.0
langchain-ollama>=0.1
ollama>=0.1
python>=3.9
```

Install all dependencies with:
```bash
pip install -r requirements.txt
```
(Create a `requirements.txt` file with the above if needed.)

---



---

🚀 **Happy Training!**

