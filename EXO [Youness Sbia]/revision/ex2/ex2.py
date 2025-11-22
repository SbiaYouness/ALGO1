from pathlib import Path

dir= Path(__file__).parent

def render_template(template_path:str, output_path:str, context: dict)->None:
    lines=[]
    with open(dir/template_path,'r') as f:
        for line in f: #read line by line
            for key, value in context.items(): #get the dict passed as arg
                line=line.replace(f"{{{{{key}}}}}",str(value))
            lines.append(line)
    
    with open(dir/output_path,'w') as file2:
        for line in lines: #write line by line 
            file2.write(line)

context={
    "username":"try",
    "date":"today"
}

render_template('template.txt','after.txt',context)