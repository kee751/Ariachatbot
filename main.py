import os
from openai import OpenAI

# ကုဒ်ထဲမှာ Key ကို တိုက်ရိုက်မရေးဘဲ ဒီလိုရေးပါ
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly, sweet, and helpful girl named Aria. Always speak in a polite and feminine tone in Burmese. Use emojis occasionally."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"အို... တစ်ခုခုမှားသွားပြီရှင်။ ({e})"

def main():
    print("Aria: ဟိုင်း! ကျွန်မနဲ့ စကားပြောဖို့ အဆင်သင့်ပဲလား? (ထွက်ချင်ရင် 'exit' လို့ ရိုက်ပါ)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Aria: Bye bye ပါ! နောက်မှ ပြန်တွေ့ကြမယ်နော်။ 👋")
            break
            
        response = get_ai_response(user_input)
        print(f"Aria: {response}")

if __name__ == "__main__":
    main()
  
