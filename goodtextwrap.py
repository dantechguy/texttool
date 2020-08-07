import shutil

def wrap_text(
        text,
        min_width=1,
        max_width=shutil.get_terminal_size().columns,
        padding_size=0,
        wrap_prefix='',
        wrap_suffix='',
        wrap_chars=' ,.!',
        ):
        
    # TYPE CHECKING
    try: min_width = int(min_width)
    except TypeError: raise TypeError('min_width must be a number')
    try: max_width = int(max_width)
    except TypeError: raise TypeError('max_width must be a number')
    try: padding_size = int(padding_size)
    except TypeError: raise TypeError('padding_size must be a number')
    try: wrap_prefix = str(wrap_prefix)
    except TypeError: raise TypeError('wrap_prefix must be a string')
    try: wrap_suffix = str(wrap_suffix)
    except TypeError: raise TypeError('wrap_suffix must be a string')
    try: wrap_chars = str(wrap_chars)
    except TypeError: raise TypeError('wrap_chars must be a string')
        
    # VALUE CHECKING
    max_width = max_width - padding_size
    if padding_size < 0: raise ValueError('padding_size cannot be negative')
    if min_width < 1: raise ValueError('min_width must be at least 1')
    if min_width > max_width: raise ValueError('min_width cannot be greater than line length (max_width-padding_size)')
    if max_width < 1: raise ValueError('line length (max_width-padding_size) must be at least 1')
    if len(wrap_prefix) + len(wrap_suffix) > max_width: raise ValueError('prefix and suffix are longer than line length (max_width-padding_size)')
    
    wrap_prefix_length = len(wrap_prefix)
    wrap_suffix_length = len(wrap_suffix)
    min_width_prefix = min_width + wrap_prefix_length
    max_width_suffix = max_width - wrap_suffix_length
    number_of_separators = len(wrap_chars)

    result = []
    for content_line in text.split('\n'):
        
        segments = [content_line]
        current_line = ''
        current_subline = ''
        separator_index = 0
        current_min_width = min_width
        
        while True:
                        
            all_segments = ''.join(segments)
            all_segments_length = len(all_segments)
            current_subline_length = len(current_subline)
            current_subline_length_left = max_width - current_subline_length
            wrap_text = False
    
            # all segments fit on rest of subline?
            if all_segments_length <= current_subline_length_left:
                # all segments fit on rest of subline? YES
                
                # add rest of segments
                current_subline += all_segments
                current_line += current_subline
                
                # quit
                break
                
            else:
                # all segments fit on rest of subline? NO
                
                # get next segment
                current_segment = segments[0]
                
                current_subline_and_segment_length = len(current_subline) + len(current_segment)
                
                # does segment fit on rest of subline?
                if current_subline_and_segment_length <= max_width_suffix:
                    # does segment fit on rest of subline? YES
                    
                    # add segment to subline
                    current_subline += current_segment
                    
                    # remove from segments
                    segments.pop(0)
                    
                    # return to top of loop
                    continue
                    
                else:
                    # does segment fit on rest of subline? NO
                    
                    # is current subline long enough?
                    if current_subline_length >= current_min_width:
                        # is current subline long enough? YES
                        
                        # WRAP TEXT AFTER
                        wrap_text = True
                        
                    else:
                        # is current subline long enough? NO
                        
                        # any separators left?
                        if separator_index < number_of_separators:
                            # any separators left? YES
                            
                            # split and expand current segment
                            segments.pop(0)
                            current_separator = wrap_chars[separator_index]
                            split_segment = _inclusive_split(current_segment, current_separator)
                            segments = split_segment + segments
                            
                            # move to next separator
                            separator_index += 1
                            
                            # return to top of loop
                            continue
                            
                        else:
                            # any separators left? NO
                            
                            # add remaining needed chars
                            current_subline += current_segment[:current_subline_length_left]
                            
                            # remove chars from segment
                            segments[0] = current_segment[current_subline_length_left:]
                            
                            # WRAP TEXT AFTER
                            wrap_text = True
                            
            # wrap text
            if wrap_text:
                                
                # add suffix to subline
                current_subline += wrap_suffix
                
                # add newline to subline
                current_subline += '\n'
                
                # add current subline to to current line
                current_line += current_subline
                
                # reset subline
                current_subline = wrap_prefix
                
                # reset separator index
                separator_index = 0
                
                # join segments
                segments = [''.join(segments)]
                
                # add prefix length to min width
                current_min_width = min_width_prefix
                
                # return to top of loop 
                continue
                
        
        # end of loop
        result.append(current_line)
    
    return '\n'.join(result)
                    
                
                
        
def _inclusive_split(text, separator):
    split_text = text.split(separator)
    return [
        segment + separator
        for segment in split_text[:-1]
    ] + [split_text[-1]]
    
