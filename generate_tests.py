import os
import openai
 
# Load API key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate test cases using OpenAI API
def generate_test_code(source_code, language):
    prompt = f"Generate test cases for the following {language} code:\n\n{source_code}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating test cases: {e}")
        return None

# Main function to scan and generate tests
def scan_and_generate_tests():
    SRC_DIR = "openAI_testCase_generation/src/"
    TEST_DIR = "openAI_testCase_generation/src/test/"
    
    # Ensure the test directory exists
    os.makedirs(TEST_DIR, exist_ok=True)

    files_found = False
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith((".java", ".js", ".py")):
                files_found = True
                file_path = os.path.join(root, file)
                language = "Java" if file.endswith(".java") else "JavaScript" if file.endswith(".js") else "Python"
                
                with open(file_path, "r", encoding="utf-8") as f:
                    source_code = f.read()

                print(f"🚀 Generating tests for {file}...")
                test_code = generate_test_code(source_code, language)
                
                if test_code:
                    test_file_path = file_path.replace("/src/", "/src/test/").replace(".java", "Test.java").replace(".js", ".test.js").replace(".py", "_test.py")
                    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
                    
                    with open(test_file_path, "w", encoding="utf-8") as test_file:
                        test_file.write(test_code)
                    print(f"✅ Test case generated: {test_file_path}")
                else:
                    print(f"⚠️ No test cases generated for {file}")

    if not files_found:
        print("❌ No source files found in src/")

if __name__ == "__main__":
    scan_and_generate_tests()
