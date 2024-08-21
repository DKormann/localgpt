from openai import OpenAI
import os, threading, asyncio, json, sys

if len(sys.argv) < 2:
  print("Usage: python3 run.py <OPENAI_API_KEY>")
  exit()

client = OpenAI(api_key=sys.argv[1])
sysprompt = 'You are a helpful management assistant that helps people accomplish there personal goals. However you concise and careful not to talk to much expecially about banal things. You offer help only when asked.'

def get_bot_response(hist):
  for chunk in client.chat.completions.create(
    model="gpt-4o-mini",
    messages= [{'role':'system', 'content':sysprompt}] + hist[-10:],
    stream=True):
    if (content:=chunk.choices[0].delta.content) is not None: yield content

hist_path = __file__.replace("localgpt.py", "hist.json")

if os.path.exists(hist_path):
  with open(hist_path, "r") as f: hist = json.load(f)
else: hist = []

intake = ' '.join(sys.argv[2:]) or input("You: ")

while intake:
  if intake == "run":
    lines = iter(reversed(hist[-1]['content'].split("\n")))
    for line in lines:
      if line == '```':break
    code = ''
    lang= 'bash'
    for line in lines:
      if line.startswith('```'):
        lang = line[3:] or 'bash'
        break
      code = line + '\n' + code
    if code:
      print("\033[36mBot: ", end='')
      print("Running code...")
      print("\033[0m")
      result = f'running code:\n{code}\n>>'
      try:
        if lang == 'python':
          result += exec(code)
        else:
          result += os.system(code)
      except Exception as e: pass
      hist.append({'role':'system', 'content':result})
  else:
    hist.append({'role':'user', 'content':intake})
    resp = get_bot_response(hist)
    print("\033[36mBot: ", end='')
    bot_response = ''
    try:
      for chunk in resp:
        print(chunk, end='')
        bot_response += chunk
    except KeyboardInterrupt: pass
    hist.append({'role':'assistant', 'content':bot_response})
    print("\033[0m")
  with open(hist_path, "w") as f: json.dump(hist, f, indent=2)
  intake = input("You: ")
