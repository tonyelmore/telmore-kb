import argparse
import json

parser = argparse.ArgumentParser(description='Extract conversation from a JSON file exported from Slack')
parser.add_argument('filename', help='the name of the JSON file')
args = parser.parse_args()

# Load the JSON file
with open(args.filename, 'r') as f:
    data = json.load(f)

# Extract the conversation
conversation = []
if isinstance(data, list):
    for item in data:
        if item.get('text'):
            conversation.append(item['text'])
else:
    for message in data['messages']:
        if message.get('text'):
            conversation.append(message['text'])

# Print the conversation
for message in conversation:
    print(message)

# To execute against a number of json files and put in a new file...
# for i in `ls -1 pcf`; do python convert.py pcf/$i > new$i.txt; done;