import json
from datetime import datetime

FILE = "SP_UZI.txt"
STR_START_ACCAUNT = 'Имя учетной записи:  '


def make_dict(data: list[str]) -> dict:
    tmp = {i.split(': ')[0]: i.split(': ')[-1].strip() for i in data}
    
    res = {"Group": "Корень/Учетные записи интернета"}
    res["Title"] = tmp.get('Имя учетной записи')
    res["Username"] = tmp.get('Имя пользователя')
    res["Password"] = tmp.get('Пароль')
    res["URL"] = tmp.get('Ссылка')
    res["Notes"] = tmp.get('Комментарий')
    res["Last Modified"] = "2023-12-26T16:12:37Z"
    res["Created"] = "2023-12-26T16:12:37Z"
    return res
    
def make_list_of_dicts(data: list[str]) -> list[dict]:
    pass

if __name__ == "__main__":
    with open(FILE, 'r', encoding='utf-16') as file:
        count = 0
        res = list()
        for line in file:
            line = line.strip()
            if count == 3:
                break
            if line.startswith(STR_START_ACCAUNT):
                #print(line.split(STR_START_ACCAUNT)[-1].strip())
                tmp = list()
                while line != '\n':
                    #tmp[line.split(': ')[0]] = line.split(': ')[-1].strip()
                    tmp.append(line)
                    line = file.readline()
                if any(i.startswith("Имен пользователя:") for i in tmp):
                    print('!!!!!!!!!!!!!')
                else:
                    res.append(make_dict(tmp))
                    
            #count += 1
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)            
    #print(res)
