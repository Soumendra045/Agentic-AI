from openai import OpenAI

client = OpenAI(
    # api_key="AIzaSyCD5sd56SM4jPVaUowUqBq_Vtg_Ab3UEvo",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(  
    model="gemini-2.0-flash",
    messages=[{"role": "user", "content": "Explain how AI works in a few words"}]
)
print(response.choices[0].message.content)