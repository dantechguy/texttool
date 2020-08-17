# textwrapper

Function signature
```py
def wrap_text(
        # the text to wrap
        text,
        
        # a line's minimum width before wrapping
        min_width=1,
        
        # the max width of lines. default is shell width
        max_width=shutil.get_terminal_size().columns,
        
        # number of columns to pad off of max_width
        padding_size=0,
        
        # a string to start all wrapped lines with
        prefix='',
        
        # a string to end all lines which wrap with
        suffix='',
        
        # string of characters, in priority order, to wrap on
        delimiters=' ,.!',
        ):
```
