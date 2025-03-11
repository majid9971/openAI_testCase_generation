import os
import requests
import json

# Ollama URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Function to generate test cases using Ollama
def generate_test_code(source_code, language):
    prompt = f"Generate test cases for the following {language} code:\n\n{source_code}"

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to generate test cases: {response.text}")

    result = response.json().get('response')
    return result

# Main function to scan and generate tests
def scan_and_generate_tests():
    SRC_DIR = "src"
    TEST_DIR = "src/test"

    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith((".java", ".js", ".py")) and "test" not in root:
                file_path = os.path.join(root, file)
                language = "Java" if file.endswith(".java") else "JavaScript" if file.endswith(".js") else "Python"

                with open(file_path, "r", encoding="utf-8") as f:
                    source_code = f.read()

                print(f"🚀 Generating tests for {file}...")
                test_code = generate_test_code(source_code, language)

                test_file_path = os.path.join(
                    TEST_DIR,
                    file.replace(".java", "Test.java").replace(".js", ".test.js").replace(".py", "_test.py")
                )

                os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

                with open(test_file_path, "w", encoding="utf-8") as test_file:
                    test_file.write(test_code)

                print(f"✅ Test cases written to {test_file_path}")

    print("✅ Test case generation completed.")

if __name__ == "__main__":
    scan_and_generate_tests()
