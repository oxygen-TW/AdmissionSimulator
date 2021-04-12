import csv, json, re
import logging

logging.basicConfig(level=logging.INFO)

def convertHospital(tmpList):
    HospitalList = []
    for i in range(5, len(tmpList)):
        result = re.findall(r"\[(.+)\]", tmpList[i])[0]
        HospitalList.append(result)
    return HospitalList

def convert(datafile):
    # 開啟 CSV 檔案
    with open('testData.csv', newline='', encoding="utf-8") as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.reader(csvfile)
        
        headerLine = next(rows)
        HospitalList = convertHospital(headerLine) #建立Header Line

        StudentList = []
        #print(HospitalList)
        # 以迴圈輸出每一列
        for row in rows:
            tmpList = {}
            for i in range(5, len(row)):
                #print(row[i])
                item = ""
                if(row[i] == ""):
                    item = "0"
                else:
                    item = row[i]

                tmpList.update({
                    item:HospitalList[i-5]
                })

            StudentList.append(
                {
                    "name":row[2],
                    "stuId":row[3],
                    "email":row[1],
                    "rank":row[4],
                    "list":{k: tmpList[k] for k in sorted(tmpList)}
                }
            )
        
        #print(StudentList)
        with open("tmpFile.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(StudentList))
        logging.info("Convert completed")
        return StudentList

if __name__ == "__main__":
    convert()