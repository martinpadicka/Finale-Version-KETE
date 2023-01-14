#csv datei import
import csv
from terminaltables import AsciiTable

DevicesDict = []
strassen = []
data_strassen = []

#geräte datei
with open('data/Devices.csv', 'r', encoding="utf-8") as csvdateiDevices:
    csv_reader_object = csv.reader(csvdateiDevices, delimiter=',')

    kopfzeile = next(csv_reader_object)

    for row in csv_reader_object:
        eintag = {
            kopfzeile[0].replace("\ufeff", "").replace(" ", ""): row[0],
            kopfzeile[1].replace("\ufeff", "").replace(" ", ""): row[1],
            kopfzeile[2].replace("\ufeff", "").replace(" ", ""): row[2],
            kopfzeile[3].replace("\ufeff", "").replace(" ", ""): row[3],
            kopfzeile[4].replace("\ufeff", "").replace(" ", ""): row[4],
            kopfzeile[5].replace("\ufeff", "").replace(" ", ""): row[5]
        }

        if not row[0] in strassen:
            strassen.append(row[0])
            data_strassen.append([])

        DevicesDict.append(eintag)

ValueDict = []

#sollwerte datei
with open('data/Standardvalue.csv', 'r', encoding="utf-8") as csvdateiValues:
    csv_reader_value = csv.reader(csvdateiValues, delimiter=',')

    kopfzeile_value = next(csv_reader_value)

    for row_value in csv_reader_value:
        eintag_value = {
            kopfzeile_value[0].replace("\ufeff", "").replace(" ", ""): row_value[0],
            kopfzeile_value[1].replace("\ufeff", "").replace(" ", ""): row_value[1],
            kopfzeile_value[2].replace("\ufeff", "").replace(" ", ""): row_value[2],
        }

        ValueDict.append(eintag_value)

len_Devices = len(DevicesDict)
len_Values = len(ValueDict)

out_dict = []

for value_index in range(len_Values):
    found_devices = []
    for device_index in range(len_Devices):
        if (ValueDict[value_index]["Gerät"] in DevicesDict[device_index]["Gerät"] and ValueDict[value_index]["Betrieb"] in DevicesDict[device_index]["Betrieb"]):
            #
            verbrauch_device = ""
            #kwh entfernen code seitig zum lernen, da bei Space fehler kommen kann
            verbrauch_device_int = str(DevicesDict[device_index]["Verbrauch"]).replace(' ', '').replace('kwh', '')
            verbrauch_Value_int = str(ValueDict[value_index]["Verbrauch"]).replace(' ', '').replace('kwh', '')

            if (int(verbrauch_device_int) == int(verbrauch_Value_int)):
                verbrauch_device = "Gleich dem Sollwert"
            elif (int(verbrauch_device_int)>int(verbrauch_Value_int)):
                verbrauch_device = "Höher als der Sollwert"
            elif (int(verbrauch_device_int)<int(verbrauch_Value_int)):
                verbrauch_device = "Kleiner als der Sollwert"


            s_index = 0
            for street in strassen:
                if DevicesDict[device_index]["Strasse"] == street:
                    abweichung = round((((int(verbrauch_Value_int)-int(verbrauch_device_int))/int(verbrauch_device_int))*100),4)
                    data_strassen[s_index].append([DevicesDict[device_index]["Gerät"],DevicesDict[device_index]["Bezeichnung"],verbrauch_device,DevicesDict[device_index]["Verbrauch"],ValueDict[value_index]["Verbrauch"], f"{abweichung}%"])
                s_index+=1


            device_found = {device_index+1:verbrauch_device}
            found_devices.append(device_found)
    out_dict.append({value_index+1:found_devices})

#tabellennamen
table_data = [
    ['Straße', 'Gerät', 'Bezeichnung', 'Verbrauch', 'Ist-Verbrauch', 'Soll-Verbrauch', 'Abweichung in %']
]

table = AsciiTable(table_data)

for i in range(len(data_strassen)):
    table_data.append([strassen[i],"-","-","-","-","-"])
    for data in data_strassen[i]:

        table_data.append(["",data[0],data[1],data[2], data[3], data[4], data[5]])


print(table.table)