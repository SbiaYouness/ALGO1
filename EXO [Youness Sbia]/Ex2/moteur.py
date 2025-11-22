def render_template(template:str, output_path:str, context:dict)->None:
    lines=[]
    with open(template,'r') as file1:
        for line in file1:
            for key, value in context.items():
                line=line.replace(f"{{{{{key}}}}}",str(value))
            lines.append(line)
        
    with open(output_path,'w') as file2:
        for line in lines:
            file2.write(line)

context={
    "username":"ali",
    "date": "10/05/2025"
}

render_template('template.txt','after.txt', context)