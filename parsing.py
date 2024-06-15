import xml.etree.ElementTree as ET
import pandas as pd
import requests

def load_xml(url,filename):
    """
    Input: url - str for URL of XML File
           filename : file to store XML record
    """
    response = requests.get(url)
    with open(filename,'wb') as file:
        file.write(response.content)

def parse_xml(filename):
    """
    :param filename:  xml file stored locally
    :return: output.csv: present information in tabluar with multiple sheets
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    count = 0

    row = []
    inflvars_df = pd.DataFrame()
    acronyms_df = pd.DataFrame()
    nounEntry_df = pd.DataFrame()
    adjEntry_df = pd.DataFrame()
    abbreviations_df = pd.DataFrame()

    for record in root.iter('lexRecord'):
        # Terminate when it comes to 1000 record
        count +=1
        if count > 1000:
            break
        eui = record.find('eui').text
        base = record.find('base').text
        cat = record.find('cat').text

        row.append([eui, base, cat])

        if record.find('inflVars').text:
            for inflVar in record.findall('inflVars'):
                attribs = inflVar.attrib
                df_dictionary = pd.DataFrame([attribs])
                inflvars_df = pd.concat([inflvars_df, df_dictionary], ignore_index = True)

        if record.findall('nounEntry'):
            nounEntry = dict()
            for char in record.findall('nounEntry/variants'):
                nounEntry['variants'] = char.text
            for element in record.findall('nounEntry/compl'):
                nounEntry['position'] = element.attrib
            for element in record.findall('nounEntry/nominalization'):
                nounEntry['nominalization'] = element.text

            nounEntry['eui'] = eui
            df_dictionary = pd.DataFrame([nounEntry])
            nounEntry_df = pd.concat([nounEntry_df, df_dictionary], ignore_index=True)

        elif record.findall('adjEntry'):
            adjEntry = dict()
            for element in record.findall('adjEntry/variants'):
                adjEntry['variants'] = element.text
            for element in record.findall('adjEntry/nominalization'):
                adjEntry['nominalization'] = element.text

            adjEntry['eui'] = eui
            df_dictionary = pd.DataFrame([adjEntry])
            adjEntry_df = pd.concat([adjEntry_df, df_dictionary], ignore_index=True)


        abbreviations_df = create_table(record, 'abbreviations', abbreviations_df, eui)

        acronyms_df = create_table(record,'acronyms',acronyms_df,eui)


    main_df = pd.DataFrame(row, columns = ['eui','cat','cat'])

    # Embeded output into a single xlsx file
    with pd.ExcelWriter('output.xlsx') as writer:
        main_df.to_excel(writer, sheet_name = 'main')
        inflvars_df.to_excel(writer, sheet_name = 'inflavrs')
        acronyms_df.to_excel(writer, sheet_name= 'acronyms')
        nounEntry_df.to_excel(writer, sheet_name = 'nounEntry')
        adjEntry_df.to_excel(writer, sheet_name = 'adjentry')
        abbreviations_df.to_excel(writer, sheet_name = 'abbreviations')


def create_table(record,tags,table,eui):
    if record.findall(tags):
        features = dict()
        for char in record.findall(tags):
            texts = char.text.split('|')
            if len(texts) > 1:
                features['words'] = texts[0]
                features['match'] = texts[1]
            else:
                features['words'] = texts[0]
            features['eui'] = eui
            df_dictionary = pd.DataFrame([features])

            table = pd.concat([table, df_dictionary], ignore_index=True)

    return table

