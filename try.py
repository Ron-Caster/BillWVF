import json
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  messages=[
    {"role": "system", "content": "Convert the given Invoice OCR data into json file."},
    {"role": "user", "content": "gstin 29bqypg7834h1z1 original copy tax invoice xe kakal industries no.25hosanagar bypass roadamatekoppa-577417 fssai no 11218326000390 pan bqypg7834h tel 9449400124 email kakalindustries gmail.com invoice no. 104 vehicle no. dated 01/08/2023 station place of supply karnataka 29 e-way bill no. reverse charge n payment mode credit gr/rr no. gi transport private billedto shipped to rawgranules private limited rawgranules private limited no 9kerekai "}
  ],
  temperature=0.7,
)

streamed_output = completion.choices[0].message.content

# Extracting JSON content from the response
json_start_index = streamed_output.find("{")
json_end_index = streamed_output.rfind("}") + 1
json_content = streamed_output[json_start_index:json_end_index]

# Clean up the output to remove newlines
cleaned_output = json.loads(json_content.replace("\n", ""))
print(json.dumps(cleaned_output, indent=4))
