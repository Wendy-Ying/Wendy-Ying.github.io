from scholarly import scholarly, ProxyGenerator
import json
from datetime import datetime
import os
from scholarly._proxy_generator import MaxTriesExceededException


SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID", "").strip()

if not SCHOLAR_ID:
    print("GOOGLE_SCHOLAR_ID is not set; skipping citation data update.")
    SystemExit(0)

try:
    print("正在查找作者信息...")
    # Setup proxy
    pg = ProxyGenerator()
    pg.FreeProxies()  # Use free rotating proxies
    scholarly.use_proxy(pg)
    author: dict = scholarly.search_author_id(SCHOLAR_ID)
except AttributeError as e:
    print(f"警告: {e}")
    print("跳过当前操作，继续执行后续步骤。")
    author = None

if author:
    try:
        print("正在填充作者详细信息...")
        scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
        name = author["name"]
        author["updated"] = str(datetime.now())
        author["publications"] = {v["author_pub_id"]: v for v in author["publications"]}
        print(json.dumps(author, indent=2))

        print("正在创建结果目录...")
        os.makedirs("results", exist_ok=True)

        print("正在保存作者数据...")
        with open("results/gs_data.json", "w") as outfile:
            json.dump(author, outfile, ensure_ascii=False)

        print("正在生成 Shields.io 数据...")
        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            "message": f"{author.get('citedby', 0)}",
        }

        print("正在保存 Shields.io 数据...")
        with open("results/gs_data_shieldsio.json", "w") as outfile:
            json.dump(shieldio_data, outfile, ensure_ascii=False)

        print("数据处理完成。")
    except MaxTriesExceededException as e:
        print(f"发生异常: {e}")
    except AttributeError as e:
        print(f"发生异常: {e}")
        print("可能是提供的 SCHOLAR_ID 无效，或者 Google Scholar 页面结构发生了变化。")
        SystemExit(1)
else:
    print("未找到作者信息，跳过数据处理步骤。")