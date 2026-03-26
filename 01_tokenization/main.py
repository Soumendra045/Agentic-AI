import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = 'Hey there! My name is Soumendra Rout'
tokens = enc.encode(text)

print('Tokens', tokens)

decode = enc.decode([25216, 1354, 0, 3673, 1308, 382, 17228, 76, 32364, 162981])

print('Decode', decode)
