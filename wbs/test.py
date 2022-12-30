with open('private_key','r') as f:
    a = f.read()
    print(bytes(a,'UTF-8'))
    print(a == a)