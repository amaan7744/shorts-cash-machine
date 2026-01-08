import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_script(title):
    prompt = f"""
Describe what happens in this video neutrally and clearly.
No morals. No judgement. 25–35 seconds.

Title:
{title}
"""
    r = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    text = r.choices[0].message.content.strip()
    open("data/script.txt","w").write(text)
    return text
