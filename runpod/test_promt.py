from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Loading tokenizer and model from Hugging Face...")
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-14B", torch_dtype=torch.float16, device_map="auto", trust_remote_code=True)

print("Running inference...")
prompt = "Explain the physics of ocean waves in simple terms."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=250)

print("\n=== Model Response ===")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))§