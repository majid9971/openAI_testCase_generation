import os
import litellm

def generate_test_code(source_code, language):
    prompt = f"Generate JUnit test cases for the following {language} code:\n\n{source_code}"
    
    # Using Ollama with LLaMA2 model (free model)
    response = litellm.completion(
        model="ollama/llama2",  # Use free LLaMA2 model
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']

def scan_and_generate_tests():
    src_dir = "src"
    test_dir = os.path.join(src_dir, "test")

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    for file_name in os.listdir(src_dir):
        if file_name.endswith(".java"):
            file_path = os.path.join(src_dir, file_name)
            with open(file_path, 'r') as file:
                source_code = file.read()

            print(f"📄 Processing {file_name}...")
            test_code = generate_test_code(source_code, "Java")

            test_file_name = f"Test{file_name}"
            test_file_path = os.path.join(test_dir, test_file_name)

            with open(test_file_path, 'w') as test_file:
                test_file.write(test_code)

            print(f"✅ Generated test cases for {file_name} ➡️ {test_file_path}")

if __name__ == "__main__":
    scan_and_generate_tests()
