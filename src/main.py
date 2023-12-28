import csv


def make_dict(data: list[str]) -> dict:
    """Функция конвертирует монопользовательскую учетную запись формата 
    StickyPassword в формат KeePassXC

    Args:
        data (list[str]): список записей для одного пользователя в формате StickyPassword

    Returns:
        dict: словарь записей для одного пользователя в формате KeePassXC
    """
    tmp = {i.split(': ')[0]: i.split(': ')[-1].strip() for i in data}
    
    #res = {"Group": "Корень/Учетные записи интернета"}
    res = dict()
    res["Title"] = tmp.get('Имя учетной записи')
    res["Username"] = tmp.get('Имя пользователя')
    res["Password"] = tmp.get('Пароль')
    res["URL"] = tmp.get('Ссылка')
    res["Notes"] = tmp.get('Комментарий')
    res["Last Modified"] = "2023-12-26T16:12:37Z"
    res["Created"] = "2023-12-26T16:12:37Z"
    return res
    
def make_list_of_dicts(data: list[str]) -> list[dict]:
    """Функция конвертирует многопользовательскую учетную запись из формата
    StickyPassword в формат KeePassXC

    Args:
        data (list[str]): список записей для нескольких пользователей в 
        формате StickyPassword

    Returns:
        list[dict]: список словарей с записями пользователей в формате KeePassXC
    """
    res = list()
    tmp = list()
    first_two_string = data[:2]
    for i in data[3:]:
        if i.startswith("Имя пользователя:") and tmp:
            res.append(make_dict(tmp))
            tmp = first_two_string[:]
            tmp[0] += f"{tmp[0]} by {i.split('Имя пользователя:')[-1].strip()}"
        elif i.startswith("Имя пользователя:"):
            tmp = first_two_string[:]
            tmp[0] += f"{tmp[0]} by {i.split('Имя пользователя:')[-1].strip()}"
        tmp.append(i)
    res.append(make_dict(tmp))
    return res

def make_json_from_txt(filename: str) -> None:
    """Функция построчно читает файл БД StickyPassword в формате txt
    и конвертирует данные в список словарей, каждый словарь в формате KeePassXC

    Args:
        filename (str): путь к txt файлу БД StickyPassword
        
    Returns:
        list[dict]: список словарей с данными аккаунтов
    """
    with open(filename, 'r', encoding='utf-16') as file:
        data_accounts = list()
        for line in file:
            line = line.strip()
            if line.startswith('Имя учетной записи:'):
                tmp = list()
                while line != '\n':
                    tmp.append(line.strip())
                    line = file.readline()
                if any(i.startswith("Имен пользователя:") for i in tmp):
                    data_accounts += make_list_of_dicts(tmp)
                else:
                    data_accounts.append(make_dict(tmp))
                    
    #with open('data.json', 'w', encoding='utf-8') as file:
    #    json.dump(data_accounts, file, indent=4, ensure_ascii=False)    
        
    return data_accounts        

def make_csv(to_csv: list[dict]) -> None:
    """Функция конвертирует список словарей в CSV и сохраняет в sticky_db.csv

    Args:
        to_csv (list[dict]): список словарей с данными аккаунтов
    """
    keys = to_csv[0].keys()
    with open('sticky_db.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys, quotechar='"', quoting=csv.QUOTE_ALL)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)

if __name__ == "__main__":
    data = make_json_from_txt(filename="SP_UZI.txt")
    make_csv(data)