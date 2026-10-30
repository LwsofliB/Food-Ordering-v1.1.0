import multiprocessing as mp
import os
import time as t
import json as j

_order_queue = None

order_no = 1


def get_order_queue():
    global _order_queue
    if _order_queue is None:
        _order_queue = mp.Queue()
    return _order_queue


def _append_json_log( order_list, total_price):
    
    global order_no
    
    # """把整单追加进 订单日志.json"""
    
    log_file = r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\订单日志.json'
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = j.load(f)
    except (FileNotFoundError, j.JSONDecodeError):
        logs = []

    logs.append({
        'order_no': order_no,
        'time': t.strftime('%Y-%m-%d %H:%M:%S'),
        'dishes': order_list,
        'total_price': total_price
    })

    with open(log_file, 'w', encoding='utf-8') as f:
        j.dump(logs, f, ensure_ascii=False, indent=2)


def _append_txt_log(order_list, total_price):
    global order_no
    # """把整单追加进 订单日志.txt"""
    with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\订单日志.txt', 'a', encoding='utf-8') as f:
        
        f.write(f"\n===== Orders #{order_no} =====\n")
        f.write(f"时间: {t.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for num, dish in enumerate(order_list, start=1):
            
            f.write(f"{num}: {dish['dish_name']} --> {dish['dish_amount']}份 "
                    f"(¥{dish['dish_price']} x {dish['dish_amount']})\n")
        f.write(f"合计: ¥{total_price}\n")

        order_no = order_no + 1


def _handle_order(order_list):
    
    """算总价 + 打印小票 + 写日志"""
    total = sum(d['dish_price'] * d['dish_amount'] for d in order_list)

    print("\n========== 后厨小票 ==========")
    
    for num, d in enumerate(order_list, start=1):
        sub = d['dish_price'] * d['dish_amount']
        print(f"{num}. {d['dish_name']}  ¥{d['dish_price']} x {d['dish_amount']} = ¥{sub}")
    
    print(f"合计: ¥{total}")
    print("==============================\n")

    _append_json_log(order_list, total)
    _append_txt_log(order_list, total)


def kitchen_worker(q):
    print(f"[后厨进程 PID={os.getpid()}] 已启动，等待订单...")
    while True:
        order_list = q.get()
        if order_list is None:
            print("[后厨进程] 下班了。")
            break
        _handle_order(order_list)


def start_kitchen():
    q = get_order_queue()
    p = mp.Process(target=kitchen_worker, args=(q,), daemon=True)
    p.start()
    return p


def shutdown_kitchen(proc):
    q = get_order_queue()
    q.put(None)
    if proc is not None:
        proc.join(timeout=3)