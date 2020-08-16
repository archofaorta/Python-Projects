import pandas as pd
from lxml import etree

path = "C:/Users/sardara1/PycharmProjects/LocalProjects/Inputs/XRS_Data_Sample.xml"

tree = etree.parse(path)


# Function to remove namespace. Note: Won't work if the XML has comments
def remove_namespaces_qname(doc, namespaces=None):
    for el in doc.getiterator():

        # clean tag
        q = etree.QName(el.tag)
        if q is not None:
            if namespaces is not None:
                if q.namespace in namespaces:
                    el.tag = q.localname
            else:
                el.tag = q.localname

            # clean attributes
            for a, v in el.items():
                q = etree.QName(a)
                if q is not None:
                    if namespaces is not None:
                        if q.namespace in namespaces:
                            del el.attrib[a]
                            el.attrib[q.localname] = v
                    else:
                        del el.attrib[a]
                        el.attrib[q.localname] = v
    return doc


# Pasing the tree to remove namespaces
tree = remove_namespaces_qname(tree)

lstKey = []
lstKeyAttrib = []
lstValue = []
for p in tree.iter():
    lstKey.append(tree.getpath(p)[1:])
    lstKeyAttrib.append(p.attrib)
    lstValue.append(p.text)

df = pd.DataFrame({'key': lstKey, 'attrib': lstKeyAttrib, 'value': lstValue})
df.sort_values('key')

writer = pd.ExcelWriter("C:/Users/sardara1/PycharmProjects/LocalProjects/Inputs/1.xlsx")
df.to_excel(writer, 'Sheet1')
writer.save()