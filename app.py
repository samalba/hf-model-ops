from transformers import pipeline
import gradio


model = pipeline(
    "summarization",
)

def predict(prompt):
    summary = model(prompt)[0]["summary_text"]
    return summary

if __name__ == '__main__':
    with gradio.Interface(predict, "textbox", "text") as interface:
        interface.launch()
