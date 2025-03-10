import os
import openai

# Set OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directory to scan for source code files
SOURCE_DIR = "src"

# File extensions mapping
LANGUAGES = {".java": "java", ".js": "javascript", ".py": "python"}

def generate_test_code(source_code, language):
    """Generates unit tests using OpenAI API"""
    prompt = f"Generate unit test cases for the following {language} code:\n\n{source_code}\n\nProvide proper test cases:"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a software engineer that generates unit tests."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response["choices"][0]["message"]["content"]

def scan_and_generate_tests():
    """Scans repository and generates test cases."""
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in LANGUAGES:
                file_path = os.path.join(root, file)
                
                with open(file_path, "r") as f:
                    source_code = f.read()

                language = LANGUAGES[ext]
                test_code = generate_test_code(source_code, language)

                # Save test cases
                test_file = file_path.replace(ext, f"_test{ext}")
                with open(test_file, "w") as f:
                    f.write(test_code)
                
                print(f"Generated test cases for {file} -> {test_file}")

if __name__ == "__main__":
    scan_and_generate_tests()
