import shutil
import os
import subprocess
import nbformat
import nbconvert



#os.system("cp /home/ec2-user/PaxFinancialExamples/examples/* /home/ec2-user/dev_paxfinancial_ai/examples")
#os.system("cp /home/ec2-user/PaxFinancialExamples/tests/*.py /home/ec2-user/dev_paxfinancial_ai/docs/APIEndpoints")




src_examples_dir = "/home/ec2-user/PaxFinancialExamples/examples/"
examples_dir = "/home/ec2-user/PaxFinancialExamples/documentation/docs/examples/"
manuals_dir = "/home/ec2-user/PaxFinancialExamples/documentation/docs/docs/manual/"

examples_list = [ "ReadingFinancialData",
                  "TensorflowModel",
                  "TensorflowModelVolatility",
                   ]
manuals_list = [ "Introduction",
                 "GettingStarted",                   
                 "SubmittingAnOrder",                
                  ]


comp_proc = subprocess.run(["ls", src_examples_dir],capture_output=True )
ls=comp_proc.stdout.decode("utf-8")
ls = ls.rstrip().split('\n')

for f in ls:
    if f.endswith(".ipynb"):        
        with open(src_examples_dir+f) as fh: 
             nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)
 
        exporter = nbconvert.MarkdownExporter()
        nb_md, meta = exporter.from_notebook_node(nb)
        print(meta['outputs'].keys())
        
        
        f_root = f[0:-6]
        
        print(f_root)
        if f_root in examples_list:           
            with open(examples_dir+f_root+".md","w") as outf:
                outf.write(nb_md)
            for outp in meta['outputs'].keys():
                with open(examples_dir+outp,"wb") as outf:
                    outf.write(meta['outputs'][outp])
        if f_root in manuals_list:        
            with open(manuals_dir+f_root+".md","w") as outf:
                outf.write(nb_md)
            for outp in meta['outputs'].keys():
                with open(examples_dir+outp,"wb") as outf:
                    outf.write(meta['outputs'][outp])
                
                
documentation_dir = "/home/ec2-user/PaxFinancialExamples/documentation"            
os.chdir(documentation_dir)

subprocess.run(["mkdocs","build"])




src_site = "/home/ec2-user/PaxFinancialExamples/documentation/site"
dest_site = "/home/ec2-user/dev_paxfinancial_ai/"

shutil.rmtree(dest_site)
shutil.copytree(src_site,dest_site)
shutil.copy( "/home/ec2-user/PaxWeb/index.html", "/home/ec2-user/dev_paxfinancial_ai/index.html")


#subprocess.run(["cp","-r", src_site, dest_site])