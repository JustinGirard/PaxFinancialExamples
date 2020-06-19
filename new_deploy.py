import shutil
import os
import subprocess
import nbformat
import nbconvert
import tempfile
import csv
import re

def codify(s):
    # indents 4 spaces
    s1 = s.rstrip().split('\n')
    new_s = []
    for line in s1:
        line = "    " + line
        new_s.append(line)
    new_s = '\n'.join(new_s)
    return new_s


tmp_dir = tempfile.TemporaryDirectory()
os.mkdir(tmp_dir.name+"/docs")
os.mkdir(tmp_dir.name+"/docs/docs")
os.mkdir(tmp_dir.name+"/docs/examples")
os.mkdir(tmp_dir.name+"/docs/docs/manual")
os.mkdir(tmp_dir.name+"/docs/docs/endpoints")


upstream_dir = "/home/ec2-user/PaxDataScience/examples/"
src_examples_dir = "/home/ec2-user/PaxFinancialExamples/examples/"
src_manual_dir = "/home/ec2-user/PaxFinancialExamples/docs/manual/"
dest_examples_dir = tmp_dir.name+"/docs/examples/"
dest_manual_dir = tmp_dir.name+"/docs/docs/manual/"

manual = { 'upstream_dir': "/home/ec2-user/PaxDataScience/examples/",
           'src_dir': "/home/ec2-user/PaxFinancialExamples/docs/manual/",
           'dest_dir': tmp_dir.name+"/docs/docs/manual/",
    
          'flist': [  { 'in': 'Intro Introduction',
                   'out': "Introduction" 
                 },
                 { 'in': 'Intro Getting Started',
                   'out': 'GettingStarted'
                 }, 
                 { 'in': 'Intro Submitting an Order',
                   'out': 'SubmittingAnOrder'
                 },
              ]
         }

examples = { 'upstream_dir': "/home/ec2-user/PaxDataScience/examples/",
             'src_dir': "/home/ec2-user/PaxFinancialExamples/examples/",
             'dest_dir': tmp_dir.name+"/docs/examples/", 
              'flist': [ { 'in': 'Intro Reading Financial Data',
                    'out': "ReadingFinancialData" 
                  },   
                  { 'in': 'Intro TensorflowModel',
                   'out': 'TensorflowModel'
                  }, 
                  { 'in': 'Intro TensorflowModelVolatility',
                    'out': 'TensorflowModelVolatility'
                  },
                       ] 
           }

for group in [manual,examples]:
    for f in group['flist']:
        shutil.copy( group['upstream_dir']+f['in']+'.ipynb', group['src_dir'] + f['out']+".ipynb")
        with open( group['src_dir'] + f['out']+".ipynb" ) as fh:
             nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT) 
        exporter = nbconvert.MarkdownExporter()
        nb_md, meta = exporter.from_notebook_node(nb)        

        with open(group['dest_dir']+f['out']+".md","w") as outf:
             outf.write(nb_md)
        for outp in meta['outputs'].keys():
            with open(group['dest_dir']+outp,"wb") as outf:
                outf.write(meta['outputs'][outp])
                        

endpoint_list = [ 'get_historical_hour',
                  'submit_transaction',
                  'submit_single_market_order',
                  'manage_experiment',
                  'find_algorithm_single_orders',
                  'get_approx_holdings',
                  'model', ]

with open('Endpoint-Registration-17-Jun-2020 (1).csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        endpoint_name = row['What is the Endpoint name']
         
        if endpoint_name == "":
            pass
        elif endpoint_name in endpoint_list:
            print(endpoint_name)
            outfile_name = tmp_dir.name+"/docs/docs/endpoints/"+endpoint_name + ".md"
        
            with open(outfile_name,"w") as out_file:
            
                out_file.write("# `"+endpoint_name+"`")
                out_file.write("\n\n")
                out_file.write("## Description")
                out_file.write("\n\n")
                out_file.write(row["Please describe the endpoint's purpose"])
                out_file.write("\n\n")
                out_file.write("## Simple Example")
                out_file.write("\n\n")
                out_file.write(codify(row["Simple Example"]))
                out_file.write("\n\n")
                out_file.write("## Simple Example Output")
                out_file.write("\n\n")
                out_file.write(codify(row["Simple Example Output"]))
                out_file.write("\n\n")                
                
                out_file.write("## Failure Examples")
                out_file.write("\n\n")
                out_file.write(codify(row["Failure Examples"]))
                out_file.write("\n\n")
                out_file.write("## Failure Examples Output")
                out_file.write("\n\n")
                out_file.write(codify(row["Failure Examples Output"]))
                out_file.write("\n\n")                
 
                out_file.write("## Three Examples")
                out_file.write("\n\n")
                out_file.write(codify(row["Three Examples"]))
                out_file.write("\n\n")
                out_file.write("## Three Examples Output")
                out_file.write("\n\n")
                out_file.write(codify(row["Three Examples Output"]))
                out_file.write("\n\n")       
                
           
        else:
            pass  
                    

conf_file_str = '''
site_name: Pax Financial Examples
nav:

    - Documentation:
        - 'Introduction': 'docs/manual/Introduction.md'
        - 'Getting Started': 'docs/manual/GettingStarted.md'
        - 'Submitting an Order': 'docs/manual/SubmittingAnOrder.md'
    - 'Endpoints':
        - get_historical_hour: 'docs/endpoints/get_historical_hour.md'
        - submit_single_market_order: 'docs/endpoints/submit_single_market_order.md'
        - model: 'docs/endpoints/model.md'
    - Examples:
        - 'Reading Financial Data': 'examples/ReadingFinancialData.md'
        - 'Volatility Model': 'examples/TensorflowModelVolatility.md'

theme:
  name: gitbook
'''

with open(tmp_dir.name+"/mkdocs.yml","w") as outf:
    outf.write(conf_file_str)
            
index_str = '''
Hello, world.
'''

with open(tmp_dir.name+"/docs/index.md","w") as outf:
    outf.write(index_str)

os.chdir(tmp_dir.name)

subprocess.run(["mkdocs","build"])

os.chdir(tmp_dir.name+"/site")
comp_proc = subprocess.run(["find", "./", "-name", '*.html'],capture_output=True )
ls = comp_proc.stdout.decode("utf-8")
ls = ls.rstrip().split('\n')
for f in ls:
    with open(f,"r") as in_f:
        file_contents = in_f.read()
    p1 = re.compile('<a href="(\.\.(/\.\.)*)" target="_blank" class="custom-link">Pax Financial Examples</a>')
    m = p1.search(file_contents)
    if m:
        prefix=m.group(1)
    else:
        prefix=""
    file_contents = file_contents.replace('No results matching "<span class=\'search-query\'></span>"','')
    file_contents = file_contents.replace(' results matching "<span class=\'search-query\'></span>"','')
    file_contents = file_contents.replace(' target="_blank"','')
    file_contents = file_contents.replace('<div id="book-search-input" role="search">\n<input type="text" placeholder="Type to search" />\n</div>','')
    file_contents = file_contents.replace('class="custom-link">Pax Financial Examples</a>', 'class="custom-link">'
                                          +'<img src="'+prefix
                                          +'/PAXFINANCIAL_files/paxlogo-180x180.png" width="60" height="60"></a>' )
    file_contents = file_contents.replace('<li class="divider"></li>\n\n\n\n<li><a href="http://www.mkdocs.org">\nPublished with MkDocs\n</a></li>\n\n<li><a href="https://github.com/GitbookIO/theme-default">\nTheme by GitBook\n</a></li>','') 
    file_contents = file_contents.replace('images/favicon.ico" type="image/x-icon">','PAXFINANCIAL_files/Capture.png" type="image/png">')
    
    with open(f,"w") as out_f:
        out_f.write(file_contents)
        
src_site = tmp_dir.name+"/site"
dest_site = "/home/ec2-user/dev_paxfinancial_ai/"

shutil.rmtree(dest_site,ignore_errors=True)
shutil.copytree(src_site,dest_site)
shutil.copy( "/home/ec2-user/PaxWeb/index.html", "/home/ec2-user/dev_paxfinancial_ai/index.html")
shutil.copytree("/home/ec2-user/PaxWeb/PAXFINANCIAL_files", "/home/ec2-user/dev_paxfinancial_ai/PAXFINANCIAL_files")

