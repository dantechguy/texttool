import shutil
# second attempt:
# use separator indexes to calculate where to wrap
# dont shorten content string, just change starting index
# append sublines to list, join?

def wrap_text(
        text,
        min_width=1,
        max_width=shutil.get_terminal_size().columns,
        padding_size=0,
        prefix='',
        suffix='',
        delimiters=' ,.!',
        ):
        
        # TYPE CHECKING
        try: min_width = int(min_width)
        except TypeError: raise TypeError('min_width must be a number')
        try: max_width = int(max_width)
        except TypeError: raise TypeError('max_width must be a number')
        try: padding_size = int(padding_size)
        except TypeError: raise TypeError('padding_size must be a number')
        try: prefix = str(prefix)
        except TypeError: raise TypeError('prefix must be a string')
        try: suffix = str(suffix)
        except TypeError: raise TypeError('suffix must be a string')
        try: delimiters = str(delimiters)
        except TypeError: raise TypeError('wrap_chars must be a string')
            
        # VALUE CHECKING
        max_width = max_width - padding_size
        if padding_size < 0: raise ValueError('padding_size cannot be negative')
        if min_width < 1: raise ValueError('min_width must be at least 1')
        if min_width > max_width: raise ValueError('min_width cannot be greater than line length (max_width-padding_size)')
        if min_width > max_width - len(prefix) - len(suffix) + 1: raise ValueError('min_width cannot be greater than minimum line length (max_width-padding_size-len(prefix) - len(suffix))')
        if max_width < 1: raise ValueError('line length (max_width-padding_size) must be at least 1')
        if len(prefix) + len(suffix) >= max_width: raise ValueError('prefix + suffix must be shorter than line length (max_width-padding_size)')
        
        result = []
        split_text = text.split('\n')
        # each line in source text
        for line_text in split_text:
            
            line_result = ''
            delimiter_indexes = get_delimiter_index_list(line_text, delimiters)
            line_max_index = len(line_text) - 1
            wrap_index = 0
            
            # each wrap line from line
            while True:
                wrap_min_index = wrap_index + min_width - 1 # -1 to keep on end of current line
                wrap_max_index = wrap_index + max_width - 1 # -1 to keep on end of current line
                if wrap_index > 0:
                    wrap_min_index -= len(prefix)
                    wrap_max_index -= len(prefix)
                
                # does rest of line fit in rest of wrap line?
                if line_max_index <= wrap_max_index:
                    
                    line_result += line_text[wrap_index:]
                    break
                    
                else:
                    # does rest of line fit in rest of wrap line? NO
                    # text will need to wrap
                    
                    decreased_wrap_min_index = wrap_min_index - len(suffix)
                    decreased_wrap_max_index = wrap_max_index - len(suffix)
                    
                    # look for greatest viable delimiter index
                    delimiter_index = next(
                        (i for i in delimiter_indexes if (decreased_wrap_min_index <= i <= decreased_wrap_max_index) ),
                        decreased_wrap_max_index ) # if no delimiter found, default to end of line
                        
                    line_result += line_text[ wrap_index : delimiter_index + 1 ] + suffix + '\n' + prefix
                    wrap_index = delimiter_index + 1
                    
            result.append(line_result)
        return '\n'.join(result)
                        

        
        
def get_delimiter_index_list(text, delimiters):
    delimiter_index_dictionary = {
        character: []
        for character in delimiters }
        
    for index, character in enumerate(text):
        if character in delimiter_index_dictionary:
            delimiter_index_dictionary[character].append(index)
            
    delimiter_index_list = []
    for character in delimiters:
        delimiter_index_list.extend(delimiter_index_dictionary[character][::-1])
    
    return delimiter_index_list
