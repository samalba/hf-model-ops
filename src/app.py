from transformers import pipeline
import gradio


model = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
)

def predict(prompt):
    summary = model(prompt)[0]["summary_text"]
    return summary

if __name__ == '__main__':
    with gradio.Interface(predict, "textbox", "text", allow_flagging="never") as interface:
        interface.launch()
