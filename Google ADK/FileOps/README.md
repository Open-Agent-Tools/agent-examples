# FileOps Agent

A specialized file and directory operations agent designed for efficient local processing with reduced latency and cost.

## Usage

See the main [getting-started.md](../getting-started.md) for installation and setup instructions.

## Agent Capabilities

The FileOps agent specializes in:

**File Operations:**
- Read, write, append, delete files
- Move and copy files
- Get file information and check existence
- Get file size
- Validate file content

**Directory Operations:**
- Create and delete directories
- List directory contents
- List all directory contents (recursive)
- Generate directory trees
- Check if directories exist or are empty

**Text Processing:**
- Clean whitespace and normalize text
- Convert between naming conventions (snake_case, camelCase, etc.)
- Extract sentences and smart text splitting
- HTML tag stripping and Unicode normalization


## Example Prompts

1. **clean_whitespace**: Remove extra whitespace from a string.
   - **Prompt:** `clean_whitespace with text = " hello world \n\t "`
   - **Before:** `" hello world \n\t "`
   - **After:** `"hello world"`

2. **normalize_line_endings**: Normalize line endings to Unix style.
   - **Prompt:** `normalize_line_endings with style = "unix", text = "line1\r\nline2\rline3\n"`
   - **Before:** `"line1\r\nline2\rline3\n"`
   - **After:** `"line1\nline2\nline3\n"`

3. **strip_html_tags**: Remove HTML tags from a string.
   - **Prompt:** `strip_html_tags with text = "<p>Hello <strong>world</strong>!</p>"`
   - **Before:** `"<p>Hello <strong>world</strong>!</p>"`
   - **After:** `"Hello world!"`

4. **normalize_unicode**: Normalize Unicode characters.
   - **Prompt:** `normalize_unicode with form = "NFC", text = "café"`
   - **Before:** `"café"` (potentially with a combined or decomposed 'é')
   - **After:** `"café"`

5. **to_snake_case**: Convert a string to snake_case.
   - **Prompt:** `to_snake_case with text = "HelloWorld"`
   - **Before:** `"HelloWorld"`
   - **After:** `"hello_world"`

6. **to_camel_case**: Convert a string to camelCase.
   - **Prompt:** `to_camel_case with text = "hello_world", upper_first = False`
   - **Before:** `"hello_world"`
   - **After:** `"helloWorld"`

7. **to_title_case**: Convert a string to Title Case.
   - **Prompt:** `to_title_case with text = "hello world"`
   - **Before:** `"hello world"`
   - **After:** `"Hello World"`

8. **smart_split_lines**: Split a long string into multiple lines.
   - **Prompt:** `smart_split_lines with max_length = 10, preserve_words = True, text = "This is a long line that needs splitting"`
   - **Before:** `"This is a long line that needs splitting"`
   - **After:** `["This is a", "long line", "that needs", "splitting"]`

9. **extract_sentences**: Extract sentences from a string.
   - **Prompt:** `extract_sentences with text = "Hello world. How are you? Fine!"`
   - **Before:** `"Hello world. How are you? Fine!"`
   - **After:** `["Hello world.", "How are you?", "Fine!"]`

10. **join_with_oxford_comma**: Join a list of strings with an Oxford comma.
    - **Prompt:** `join_with_oxford_comma with conjunction = "and", items = ["apples", "bananas", "oranges"]`
    - **Before:** `["apples", "bananas", "oranges"]`
    - **After:** `"apples, bananas, and oranges"`