import argparse
from markdown_it import MarkdownIt

def main():
    # Add parser to get input markdown file and output HTML file
    parser = argparse.ArgumentParser(description="Convert Markdown file to HTML")
    parser.add_argument(dest='input_file', help="Path to the input markdown file")
    parser.add_argument(dest='output_file', help="Path to the output HTML file")
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file
    
    markdown_content = ''
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    markdown_content = markdown_content.replace('```mermaid', '<pre><code class="language-mermaid"><div class="mermaid">\n')
    markdown_content = markdown_content.replace('```python', '</div></code class="python"></pre>\n')
    markdown_content = markdown_content.replace('```', '</div></code></pre>\n')

    md = MarkdownIt()
    html = md.render(markdown_content)

    # Create a complete HTML page template with Bootstrap 5.3.2
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation</title>
    <!-- Bootstrap 5.3.2 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <!-- Custom styles -->
    <style>
        body {{
            background-color: #f8f9fa;
        }}
        .container {{
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-top: 2rem;
            margin-bottom: 2rem;
            padding: 3rem;
        }}
        .toc {{
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 1rem;
            margin-bottom: 2rem;
        }}
        code {{
            background-color: #f1f3f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 1rem;
        }}
        blockquote {{
            border-left: 4px solid #007bff;
            padding-left: 1rem;
            margin-left: 0;
            color: #6c757d;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        h1 {{
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 0.5rem;
        }}
        table {{
            margin: 1rem 0;
        }}
    </style>
    <!-- Mermaid.js CDN -->
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true }});
    </script>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-12">
                {html}
            </div>
        </div>
    </div>
      <!-- Bootstrap 5.3.2 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    main()