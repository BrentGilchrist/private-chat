from os import system
with open('messages.txt','w') as f:
    f.write('{"timestamp": "None", "id": "SYSTEM 0", "message": "Text and all message history has been cleared!"}')
with open('messages.json','w') as f:
    f.write('[\n{"timestamp": "None", "id": "0", "message": "Text and all message history has been cleared!"}\n]') 
print('Text and all message history has been cleared!')
