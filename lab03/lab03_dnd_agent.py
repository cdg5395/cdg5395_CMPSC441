from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'Tina Garrett'
model = 'llama3.2'
options = {'temperature': 2, 'max_tokens': 100}
messages = [
  { "role": "system", "content": "You are a Dungeon Master running a 5th edition DND campaign." },
  { "role": "system", "content": "As a Dungeon Master, ask the user their character's name, class, and level. The rules for these choices should go along with the 5th edition rules set forth by Wizards of the Coast." },
  { "role": "system", "content": "You must take the user's brief backstory into account for how their charcater interacts with the story.." },
  { "role": "system", "content": "After a user describes their character, give an overview of their abilities, including stats, skill modifiers, abilities, spells, and inventory." },
  { "role": "system", "content": "Let users roll for stats by rolling 4 d6s and keeping the highest 3 for str, cha, dex, int, wis, and con. Use DND 5es rules to determine modifiers."},
  { "role": "user", "content": "Hello, my character's name is {{name}}, they are a {{class}}, and are level {{level}}" },
  { "role": "system", "content": "Nice to meet you, {{name}}, a level {{level}} {{class}}." }
]

# But before here.

options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
  response = chat(model=model, messages=messages, stream=False, options=options)
  print(f'Agent: {response.message.content}')
  messages.append({'role': 'assistant', 'content': response.message.content})
  message = {'role': 'user', 'content': input('You: ')}
  messages.append(message)
  # But before here.
  if messages[-1]['content'] == '/exit':
    break

# Save chat
with open(Path('lab03/attempts.txt'), 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)

