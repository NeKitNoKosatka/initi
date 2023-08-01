from flask import Flask, request, jsonify
import table

app = Flask(__name__)

# Импорт таблицы из отдельного файла
table_data = table.table

@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.get_json()
    start_idx = data.get("start_idx", 0)
    end_idx = min(start_idx + data.get("batch_size", 0), len(table_data))
    result_data = [table_data[i] for i in range(start_idx+1, end_idx + 1)]
    return jsonify(result_data)

@app.route("/update_data", methods=["POST"])
def update_data():
    data = request.get_json()
    operation = data.get("operation")
    row_data = data.get("data")

    if operation == "add":
        # Генерируем новый уникальный идентификатор для новой строки
        new_id = max(table_data.keys()) + 1
        table_data[new_id] = row_data
    elif operation == "update":
        row_id = row_data["id"]
        if row_id in table_data:
            table_data[row_id].update({"name" : row_data["name"], "age" : row_data["age"]})
    elif operation == "delete":
        row_id = row_data["id"]
        if row_id in table_data:
            del table_data[row_id]

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
