from ex1 import save_report
from pathlib import Path

dir=Path(__file__).parent 

with open(dir/'input.txt','r') as f:
    data=f.read()

save_report(dir/'report1.txt',data)