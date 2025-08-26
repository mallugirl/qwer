from openai import OpenAI
client = OpenAI()

# ---- Helper for boilerplate filtering ----
def contains_boilerplate(content, boilerplate_sentences):
    prompt = f"""
You are a strict text checker.
I will give you a document content and a list of boilerplate sentences.
Your task: check if ANY of the boilerplate sentences are fully present in the content.
Respond ONLY with "YES" if found, "NO" if none are present.

Content:
{content}

Boilerplate sentences:
{boilerplate_sentences}
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content.strip().upper() == "YES"
    except Exception as e:
        print(f"⚠️ GPT check failed, defaulting to NO. Error: {e}")
        return False



        # ✅ Guardrail 1: skip if combined text too short
        if len(metadata['combined_text'].strip()) < 30:
            print(f"⚠️ Skipping page {idx+1}: combined_text too short")
            continue  

        # ✅ Guardrail 2: skip if boilerplate
        boilerplate_sentences = [
            "This document is not for use in any public forum or social media.",
            "Do not reproduce or share without written permission.",
            "Confidential and proprietary information."
        ]
        if contains_boilerplate(metadata['combined_text'], boilerplate_sentences):
            print(f"⚠️ Skipping page {idx+1}: boilerplate detected")
            continue
