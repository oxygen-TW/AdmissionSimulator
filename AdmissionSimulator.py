from converter import convert
import json, csv, sys
import logging

logging.basicConfig(level=logging.INFO)

def LoadJsonFile(_filename):
    with open(_filename, "r", encoding="utf-8") as f:
        data = f.read()
        data = json.loads(data)
        return data

def writeToCSV(data):
    with open('output.csv', 'w', newline='', encoding="utf-8") as csvfile:
        # 定義欄位
        fieldnames = ["name", "stuId", "result"]

        # 將 dictionary 寫入 CSV 檔
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 寫入第一列的欄位名稱
        writer.writeheader()

        # 寫入資料
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":

    #檢查參數
    if(len(sys.argv) != 2):
        logging.critical("參數錯誤")
        exit(1)
    
    dataFileName = sys.argv[1]
    logging.info("資料檔："+ dataFileName)

    logging.info("Ready for data conversion")
    StudentList = convert(dataFileName) #呼叫轉檔

    logging.info("呼叫醫院清單")
    try:
        HospitalData = LoadJsonFile("Hospital.json")#[0]=最大人數 [1]=目前人數
    except FileNotFoundError:
        logging.critical("Error: 找不到醫院清單")
        exit(2)
    logging.info("成功讀取醫院清單")

    TotalHospitalNumber = len(HospitalData)
    #print(StudentList)

    logging.info("資料前處理完成")
    logging.info("開始分發演算法")
    FinalList = []
    #決定排名順序
    for no in range(1, 100):
        for item in StudentList:
            #輪到哪一位學生
            if(item["rank"] == str(no)):
                logging.info("分發作業：" + item["name"])
                flag = False
                for i in range(1, TotalHospitalNumber):
                    try:
                        nowWish = item["list"][str(i)]
                    except KeyError:
                        print(item["name"], "Pass")
                        FinalList.append({
                            "name":item["name"],
                            "stuId":item["stuId"],
                            "result": "未分發成功"
                    })
                        break
                    #判斷名額
                    if(HospitalData[nowWish][1] < HospitalData[nowWish][0]):
                        FinalList.append({
                            "name":item["name"],
                            "stuId":item["stuId"],
                            "result": nowWish
                        })
                        HospitalData[nowWish][1] += 1
                        Flag = True
                        break
                    else:
                        continue

                if(not(Flag)):
                    FinalList.append({
                            "name":item["name"],
                            "stuId":item["stuId"],
                            "result": "未分發成功"
                    })
    logging.debug(FinalList)
    logging.info("Write results to output file.")
    writeToCSV(FinalList)
    logging.info("All done! No error found.")
    input()

                