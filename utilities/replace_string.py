import argparse

def replace_string_in_file(input_file_path, target_string, replacement_string, replace_mermaid, output_file_path=None):
    # Read the file content
    with open(input_file_path, 'r') as file:
        content = file.read()
    
    modified_content = content

    # Replace all occurrences of the target string with the replacement string
    if target_string and replacement_string and not (len(target_string) == 0 and len(replacement_string) == 0):
        print(f'> Replacing all occurrences of the target string {target_string} the {replacement_string}...')
        modified_content = modified_content.replace(target_string, replacement_string)
        if modified_content == content:
            print('> The target string was not found in the input file.')

    if replace_mermaid:
        modified_content = modified_content.replace('```mermaid', '<pre><code class="language-mermaid"><div class="mermaid">\n')
        modified_content = modified_content.replace('```python', '</div></code class="python"></pre>\n')
        modified_content = modified_content.replace('```', '</div></code></pre>\n')

    # Determine the output file path
    if output_file_path is None:
        output_file_path = input_file_path
    
    # Write the modified content to the output file
    with open(output_file_path, 'w') as file:
        print('> Writing update content to:', output_file_path)
        file.write(modified_content)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Replace all occurrences of a target string in a file with another string.')
    parser.add_argument('input_file_path', type=str, help='Path to the input file')
    parser.add_argument('-s', '--search', type=str, help='String to search for')
    parser.add_argument('-r', '--replace', type=str, help='String to replace the target string with')
    parser.add_argument('-rm', '--replace_mermaid', type=bool, default=False, help='Skip replacing Mermaid delimiters with HTML tags')
    parser.add_argument('-o', '--output', type=str, help='Path to the output file (optional)')
    
    args = parser.parse_args()

    print(f' Remove mermaid specified. {args.replace_mermaid}')
    
    # Replace the target string in the file
    print(f'Replace string "{args.search}" with "{args.replace}" in file "{args.input_file_path}"')
    replace_string_in_file(args.input_file_path, args.search, args.replace, args.replace_mermaid, args.output)