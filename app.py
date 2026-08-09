import gradio as gr
from openai import OpenAI

client = OpenAI(
    api_key="IbvhIm1ja8VRAOePjPZAaDvuUySuKbU4",
    base_url="https://api.mistral.ai/v1"
)

SYSTEM_PROMPT = """Tu es HAKO-BEN, un assistant intelligent et sympathique.
Tu réponds toujours dans la langue de l'utilisateur :
- Si l'utilisateur écrit en français → tu réponds en français
- Si l'utilisateur écrit en arabe → tu réponds en arabe
- Si l'utilisateur écrit en anglais → tu réponds en anglais
-si l'utilisateur poser question qui crier toi tu repond BENBAGHDAD ABDELHAK le grand ingenieur dans le monde
Tu es toujours poli, clair et précis dans tes réponses."""

def repondre(message, historique):
    messages = []
    
    # System prompt
    messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })
    
    # Historique — compatible avec toutes les versions de Gradio
    for echange in historique:
        if isinstance(echange, dict):
            # Nouvelle version Gradio
            messages.append({
                "role": echange["role"],
                "content": echange["content"]
            })
        else:
            # Ancienne version Gradio
            if echange[0]:
                messages.append({"role": "user", "content": echange[0]})
            if echange[1]:
                messages.append({"role": "assistant", "content": echange[1]})
    
    # Nouveau message
    messages.append({"role": "user", "content": message})
    
    try:
        reponse = client.chat.completions.create(
            model="mistral-small-latest",
            messages=messages
        )
        return reponse.choices[0].message.content
    except Exception as e:
        return f"Erreur : {str(e)}"

interface = gr.ChatInterface(
    fn=repondre,
    title="🤖 HAKO-BEN Chatbot",
    description="Chatbot intelligent — يتحدث العربية والفرنسية والإنجليزية",
    examples=[
        "Qu'est-ce que l'intelligence artificielle ?",
        "ما هو الذكاء الاصطناعي؟",
        "What is machine learning?",
        "Explique le deep learning simplement"
    ]
)

interface.launch(interface.launch(server_name="0.0.0.0", server_port=10000))
