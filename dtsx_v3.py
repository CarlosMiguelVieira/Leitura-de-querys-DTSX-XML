




import os
from lxml import etree

sql_out = r'C:\Users\cpinto\Desktop\Teste dtsx\teste'
path = r'C:\Users\cpinto\Desktop\Teste dtsx'
list_files = [f for f in os.listdir(path) if f.endswith('.dtsx')]

for files in list_files: 

    ssis_dtsx =rf'C:\Users\cpinto\Desktop\Python Dados\repos\ativa-dw\StageAtiva - Corrwin\{files}'
       
    tree = etree.parse(ssis_dtsx)
    root = tree.getroot()
    
    total_bytes = 0
    package_name = root.attrib['{www.microsoft.com/SqlServer/Dts}ObjectName'].replace(" ","")
    for cnt, component_or_executable in enumerate(root.xpath(".//*")):
        i = 0
        if component_or_executable.tag == 'component':
            name_component = component_or_executable.attrib['name']
            refId_component = component_or_executable.attrib['refId']
            # print(ele.attrib)
            
            for properties in component_or_executable:
                if properties.tag == 'properties':
                    
                    for propertie in properties:
                        
                        sql_query = propertie.text
                        try:
                            erro = propertie.attrib['UITypeEditor']
                            if sql_query != None:
                                i += 1
                                sql_file = sql_out + "\\" + files[:-5] + '_' + refId_component.replace('\\','--') + str(i) + ".txt"
                                total_bytes += len(sql_query)
                                with open(sql_file, "w") as file:
                                    file.write(sql_query)
                        except:
                            None  
        elif component_or_executable.tag == "{www.microsoft.com/SqlServer/Dts}Executable":
            attr = component_or_executable.attrib
            for ObjectData in component_or_executable:
                if ObjectData.tag == "{www.microsoft.com/SqlServer/Dts}ObjectData":
                    for SqlTaskData in ObjectData:
                        sql_comment = attr["{www.microsoft.com/SqlServer/Dts}ObjectName"].strip()
                        refId_SqlTaskData = attr["{www.microsoft.com/SqlServer/Dts}refId"].strip()
                        if SqlTaskData.tag == "{www.microsoft.com/sqlserver/dts/tasks/sqltask}SqlTaskData":
                            dtsx_sql = SqlTaskData.attrib["{www.microsoft.com/sqlserver/dts/tasks/sqltask}SqlStatementSource"]
                            # dtsx_sql = "-- " + sql_comment + "\n" + dtsx_sql
                            sql_file = sql_out + "\\" + files[:-5]+'_' + refId_SqlTaskData.replace('\\','--') + ".txt"
                            total_bytes += len(dtsx_sql)
                            with open(sql_file, "w") as file:
                                file.write(dtsx_sql)
                                
print(len(os.listdir(sql_out)))
        