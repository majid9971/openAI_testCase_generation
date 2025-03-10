import os
import openai

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define paths
SRC_DIR = "openAI_testCase_generation/src/"
TEST_DIR = "openAI_testCase_generation/src/test/java/com/example/"

# Ensure test directory exists
os.makedirs(TEST_DIR, exist_ok=True)

# Function to extract Java methods
def extract_java_methods(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    lines = content.split("\n")
    package_name = "com.example"  # Default package

    methods = []
    for line in lines:
        line = line.strip()
        if line.startswith("package "):
            package_name = line.split()[1].strip(";")
        if line.startswith("public") and "(" in line and "class" not in line:
            methods.append(line)

    return package_name, methods

# Function to generate test cases using OpenAI API
def generate_test_cases(java_class_name, methods):
    prompt = f"Generate JUnit test cases for class {java_class_name} in package com.example with the following methods:\n\n"
    for method in methods:
        prompt += method + "\n"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Process Java files
for root, _, files in os.walk(SRC_DIR):
    for file in files:
        if file.endswith(".java"):
            file_path = os.path.join(root, file)
            class_name = file.replace(".java", "")
            
            package_name, methods = extract_java_methods(file_path)
            if methods:
                print(f"Generating test cases for: {class_name}")
                
                test_code = generate_test_cases(class_name, methods)
                
                test_file_path = os.path.join(TEST_DIR, f"{class_name}Test.java")
                with open(test_file_path, "w", encoding="utf-8") as test_file:
                    test_file.write(f"package {package_name};\n\n{test_code}")

print("✅ Test case generation completed.")
