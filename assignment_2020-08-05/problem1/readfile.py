def readText(addr):
    with open(addr,'r') as text_data:
        data_list =[]
        
        for line in text_data: 
            line_text = str(line).split("\n")[0]

            collect_text = False
            expression = ''

            for c in line_text:
                
                if collect_text :
                    if c == '"':
                        collect_text = False
                    else:
                        expression +=c
                elif c == '"':
                    collect_text = True
            
            data_list.append(expression)

    return data_list
