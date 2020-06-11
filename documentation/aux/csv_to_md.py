import csv

def codify(s):
    # indents 4 spaces
    s1 = s.rstrip().split('\n')
    new_s = []
    for line in s1:
        line = "    " + line
        new_s.append(line)
    new_s = '\n'.join(new_s)
    return new_s


endpoint_list = [ 'get_historical_hour',
                  'submit_transaction',
                  'submit_single_market_order',
                  'manage_experiment',
                  'find_algorithm_single_orders',
                  'get_approx_holdings',
                  'model', ]

with open('Endpoint-Registration-11-Jun-2020 (5).csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    contents_file = open("../docs/endpoints.md","w")
    
    for row in csv_reader:
        endpoint_name = row['What is the Endpoint name']
         
        if endpoint_name == "":
            pass
        elif endpoint_name in endpoint_list:
            print(endpoint_name)
            outfile_name = "../docs/docs/endpoints/"+endpoint_name + ".md"
        
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
                
            contents_file.write("- [`" + endpoint_name +"`](docs/endpoints/"+endpoint_name+".md)\n" )
        else:
            pass
    contents_file.close()  
