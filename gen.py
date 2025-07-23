import json
from pathlib import Path
from itertools import cycle

SOURCE_DIR = Path("sentences-bundle/sentences")
ORIG_DATA_DIR = Path("orig_data")
CATEGORIES_DIR = Path("categories")

NUM_ORIG_FILES = 65536  # 0x0000 ~ 0xffff
NUM_CATEGORY_FILES = 4096  # 0x000 ~ 0xfff


def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True)


def main():
    ensure_dir(ORIG_DATA_DIR)
    ensure_dir(CATEGORIES_DIR)

    all_objects = []

    # 1. 读取所有json对象
    for file_path in SOURCE_DIR.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    all_objects.extend(data)
                else:
                    print(f"Warning: {file_path} is not a list.")
            except json.JSONDecodeError as e:
                print(f"Error decoding {file_path}: {e}")

    if not all_objects:
        print("No valid objects found.")
        return

    # 2. 写入 orig_data 65536 个文件
    print("Writing to orig_data/...")
    obj_cycle = cycle(all_objects)
    for i in range(NUM_ORIG_FILES):
        obj = next(obj_cycle)
        file_name = f"{i:04x}.json"
        file_path = ORIG_DATA_DIR / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)

    # 3. 写入 categories 文件夹，每类 4096 个文件
    print("Writing to categories/...")
    for file_path in SOURCE_DIR.glob("*.json"):
        category_name = file_path.stem
        category_dir = CATEGORIES_DIR / category_name
        ensure_dir(category_dir)

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    print(f"Warning: {file_path} is not a list.")
                    continue
            except json.JSONDecodeError as e:
                print(f"Error decoding {file_path}: {e}")
                continue

        cat_cycle = cycle(data)
        for i in range(NUM_CATEGORY_FILES):
            obj = next(cat_cycle)
            file_name = f"{i:03x}.json"
            out_path = category_dir / file_name
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False)

    print("Done.")


if __name__ == "__main__":
    main()
