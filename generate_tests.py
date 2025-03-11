import os
import litellm

# Load API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

# Function to generate test cases using LiteLLM (OpenAI Compatible)
def generate_test_code(source_code, language):
    prompt = f"Generate test cases for the following {language} code:\n\n{source_code}"

    response = litellm.completion(
        model="gpt-3.5-turbo",  # Free model available through LiteLLM
        messages=[{"role": "user", "content": prompt}],
        api_key=API_KEY  # LiteLLM proxy key (if needed)
    )

    return response['choices'][0]['message']['content']

# Main function to scan and generate tests
def scan_and_generate_tests():
    SRC_DIR = "openAI_testCase_generation/src/"
    
    found_files = False

    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith((".java", ".js", ".py")):
                found_files = True
                file_path = os.path.join(root, file)
                language = "Java" if file.endswith(".java") else "JavaScript" if file.endswith(".js") else "Python"
                
                with open(file_path, "r", encoding="utf-8") as f:
                    source_code = f.read()

                print(f"Generating tests for {file}...")
                test_code = generate_test_code(source_code, language)
                
                test_file_path = file_path.replace("/src/", "/src/test/").replace(".java", "Test.java").replace(".js", ".test.js").replace(".py", "_test.py")
                os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
                
                with open(test_file_path, "w", encoding="utf-8") as test_file:
                    test_file.write(test_code)

    if found_files:
        print("✅ Test case generation completed.")
    else:
        print("❌ No source files found in src/")

if __name__ == "__main__":
    scan_and_generate_tests()
