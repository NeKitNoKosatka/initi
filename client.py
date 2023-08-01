import requests

# Простой словарь для кэширования данных на клиенте
data_cache = {}

def get_data_from_server(start_idx):
    global data_cache
    if start_idx in data_cache:
        # Если данные уже есть в кэше, возвращаем их
        return data_cache[start_idx]

    url = "http://localhost:5000/get_data"
    # Запрашиваем три страницы данных (30 записей: 10 записей перед, 10 записей, которые запросила и 10 записей после)
    if start_idx > 10 :
        data = {"start_idx": start_idx - 10, "batch_size": 30}
    else:
        # Если стартовый индекс меньше 10, то запрашивается 20 записей. 10 записей запрашиваемых и 10 записей после
        data = {"start_idx": start_idx, "batch_size": 20}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result_data = response.json()
            # Кэшируем полученные данные
            data_cache[start_idx] = result_data
            return result_data
    except requests.exceptions.RequestException as e:
        print("Ошибка при отправке запроса:", e)
    return []

def update_data_on_server(operation, row_data):
    url = "http://localhost:5000/update_data"
    data = {"operation": operation, "data": row_data}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            # Очищаем кэш после успешного обновления данных на сервере
            data_cache.clear()
            return True
    except requests.exceptions.RequestException as e:
        print("Ошибка при отправке запроса:", e)
    return False


# Пример использования клиента
start_idx = 0
while True:
    data = get_data_from_server(start_idx)
    if not data:
        print("no data")
        break
    # Количество строк, отображаемых на клиенте - 10
    if start_idx >= 10:
        for row in data[9:20]:
            print(row)
    else:
        for row in data[:10]:
            print(row)

    user_input = input("Введите команду (read/add/update/delete) или 'q' для выхода: ")
    if user_input.lower() == "q":
        break

    if user_input.lower() in ("add", "update", "delete"):
        row_data = {}
        if user_input.lower() in ("update", "delete"):
            row_id = int(input("Введите id строки: "))
            row_data["id"] = row_id
        if user_input.lower() in ("add", "update"):
            row_data["name"] = input("Введите имя: ")
            row_data["age"] = int(input("Введите возраст: "))

        if update_data_on_server(user_input.lower(), row_data):
            print("Операция успешно выполнена.")
        else:
            print("Ошибка при выполнении операции.")
    elif user_input.lower() == "read":
        start_idx = int(input("Введите id строки: "))
    else:
        print("Некорректная команда. Повторите попытку.")

