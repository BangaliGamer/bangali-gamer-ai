import os

KNOWLEDGE_FILE = "data/knowledge.txt"

def load_knowledge():
    # যদি ফোল্ডার বা ফাইল না থাকে, তবে তৈরি করে নেবে
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            f.write("1. FC 26 Ultimate Bangladesh Edition Mod: Price 500 BDT\n")
            f.write("2. FC 26 Standard Mod Pack: Price 300 BDT\n")
            
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def save_knowledge(fact):
    # নতুন তথ্য ফাইলের নিচে যোগ করে দেবে
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(f"- {fact}\n")