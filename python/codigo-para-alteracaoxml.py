import os
import xml.etree.ElementTree as ET

# Namespace usado no XML da NFe
NFE_NAMESPACE = 'http://www.portalfiscal.inf.br/nfe'
NAMESPACE = {'ns': NFE_NAMESPACE}

# Registrar o namespace padrão (sem prefixo)
ET.register_namespace('', NFE_NAMESPACE)

# Diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
print("Directory found:", script_dir)

# Iterar sobre os arquivos .xml no diretório
for filename in os.listdir(script_dir):
    if filename.endswith('.xml'):
        file_path = os.path.join(script_dir, filename)
        modified = False

        try:
            print(f"Reading file: {file_path}")
            tree = ET.parse(file_path)
            root = tree.getroot()

            for cfop_tag in root.findall('.//ns:CFOP', NAMESPACE):
                cfop_text = cfop_tag.text
                if cfop_text and cfop_text.startswith('5'):
                    new_cfop = '6' + cfop_text[1:]
                    print(f"Changing CFOP from {cfop_text} to {new_cfop}")
                    cfop_tag.text = new_cfop
                    modified = True

            if modified:
                new_filename = os.path.splitext(filename)[0] + '_MOD.xml'
                new_file_path = os.path.join(script_dir, new_filename)
                tree.write(new_file_path, encoding='utf-8', xml_declaration=True)
                print(f"Modified file saved as: {new_filename}")
            else:
                print(f"No modifications needed for: {filename}")

        except ET.ParseError:
            print(f"Error parsing XML file: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
