import openai

def generate_script():
    prompt = open("prompts/commentary.txt").read()

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    script = response["choices"][0]["message"]["content"]
    open("data/script.txt", "w").write(script)

    return script
