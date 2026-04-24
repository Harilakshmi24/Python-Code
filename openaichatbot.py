from openai import OpenAI
client = OpenAI(api_key=" key")

def start_chatbot():
    messages = [{"role":"system","content":"you are a helper and assistant"}]
    print("Idealabs Chatbot, Type 'quit' to exit")

    while True:
        user_input=input("you: ")
        if user_input.lower() in ["quit","exit"]:
            break
        messages.append({"role":"user","content":user_input})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        assistant_reply=response.choices[0].message.content
        print(f"Idealabs:{assistant_reply}")
        messages.append({"role":"assistant","content":assistant_reply})
        
if __name__ == "__main__":
    start_chatbot()
