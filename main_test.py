import time as t
import json as j
import os
import multiprocessing as mp
import start_kitchen as st

dishes_count = 0

orders = []

kitchen_process = None

# 这个函数是为了防止误触空格导致程序崩溃而编写的
# 将所有有关输入的模块或者语句换成这个 提升程序运行稳定性 不至于一按回车就崩溃
def get_int(prompt):
    while True:
        s = input(prompt).strip()
        if s == "":
            print("You haven't input anything in here!")
            continue
        try:
            return int(s)
        except ValueError:
            print("Please enter a valid integer!")

def load_menu():
    # print("写入路径:", os.path.abspath('点餐小程序（2026.10.08）(模拟)\菜品数据.json'))
    try:
        with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json', 'rt', encoding='utf-8') as f:
            return j.load(f)
    except (FileNotFoundError, j.JSONDecodeError):
        return []

def file_data_checking():
    try:
        with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json', 'rt', encoding='utf-8')as f:
            print("Data loading......")
            t.sleep(2)
            return j.load(f)


        
    except FileNotFoundError:
            print("Could not found file!")
    except j.JSONDecodeError:
            print("JSON file is illegal!(Or no data in this file......)")
                     
    while True:
        uc4 = get_int('Choose 1 to continue checking or 2 to back to main menu:')
        if uc4 == 1:
            file_data_checking()
        elif uc4 == 2:
            return
        else:
            print("Invalid Inputting!")
            


def loading():
    global menu, kitchen_process

    kitchen_process = st.start_kitchen()

    print("Services Loading......")
    t.sleep(2)
    
    print("Data Loading......")
    menu = load_menu()

    t.sleep(1.5)
    print("----Welcome to 点餐小程序模拟!----")
    main()
    
    
def data_loading():
    print("Data Loading......")

def main():
    print("----MENU----")
    print('1.User mode')
    print('2.Admin mode')
    print('3.Exit')
    print('4.File data checking')
    
    while True:

        c1 = get_int("<<Main Menu>> | Enter a number:")

        if c1 == 1:
            menu_display()
        elif c1 == 2:
            Admin_mode()
        elif c1 == 3:
            with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json', 'wt', encoding='utf-8') as f:
                
                j.dump(menu, f, ensure_ascii=False, indent=2)

            st.shutdown_kitchen(kitchen_process) 

            print("See u next time!")
            
            t.sleep(1.5)
            
            exit()
        elif c1 == 4:
            file_data_checking()
        else:
            print("Invalid Inputting!")

def Admin_mode():
    print()
    print("----Admin Mode----")
    print("1.Dishes adding")
    print("2.Dishes deleting")
    print("3.Dishes modifying(Price)")
    print("4.Menu display")
    print("5.Data Saving")
    print("6.Clear Menu")
    print("7.Dishes logs Check")
    print("8.Exit")
    
    while True:
        c2 = get_int("<<Admin Mode>> | Enter a number:")
        if c2 == 1:
            dishes_modifying_add()
        elif c2 == 2:
            menu_modifying_del()
        elif c2 == 3:
            menu_modifying_price_md()
        elif c2 == 4:
            menu_display_2()
        elif c2 == 5:
            menu_saving()
        elif c2 == 6:
            Clear_Menu()
        elif c2 == 7:
            dishes_logs()
        elif c2 == 8:
            print("Returning to main menu......")
            t.sleep(1.5)
            return
        elif c2 == "":
            print("Please enter a number!")
        else:
            print("Invalid Inputting!")
        
def menu_display():

    print()
    print("Menu is loading......")
    t.sleep(3)

    print()
    print('----菜单----')    

    if menu == []:
        print("未找到菜品数据！")
        t.sleep(1)
        main()
    else:
        for num,dishes in enumerate(menu,start=1):
            print(f"{num}: {dishes['dish_name']} --> ¥{dishes['dish_price']}")

        orders_From_customers()

def menu_display_2():
    print()
    print("Menu is loading......")
    t.sleep(3)
    
    print()
    print('----朱家小馆菜单----')    
    
    if menu == []:
        print("未找到菜品数据！")
        t.sleep(1)
        main()
    else:
        for num,dishes in enumerate(menu,start=1):
            print(f"{num}: {dishes['dish_name']} --> ¥{dishes['dish_price']}")

        return





def orders_From_customers():

    with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json','r',encoding='utf-8')as f:
        orders_data = j.load(f)

    uc8_1 = get_int('请问您需要点餐吗？(1/2)')
    if uc8_1 == 2:
        print("正在返回......")
        t.sleep(2)
        return
    else:
        while True:
            users_order = get_int("What do u wanna eat?(Please enter the number of the food):")
            users_order = users_order - 1
        
            if users_order < 0 or users_order >= len(orders_data):
                print("Index out of range!Please check again!")
                continue
            elif users_order + 1 == 0:
                print("Returning......")
                return
            else:
                print(f"Dish {orders_data[users_order]['dish_name']} was found!")

                uc8 = get_int("U sure u want this dish?(1 is yes and 2 is no):")

                if uc8 == 2:
                    print("Returning......")
                    continue
                elif uc8 == 1:
                    print(f"You choose dish {orders_data[users_order]['dish_name']}!")

                    dish_amount = get_int("How many do u want:(Please enter an integer!)(10 dishes at most per time!)")

                    if dish_amount > 10:
                        print("U cannot order the same food for over 10 times!")
                        continue
                    else:
                        print(f"Ordering Successfully!")
                    
                        orders_receiving(orders_data[users_order]['dish_name'], 
                                            orders_data[users_order]['dish_price'],
                                            dish_amount)
                        
                        uc8 = get_int("Continue to order or stop?(1/2)")
                        
                        if uc8 == 2:
                            uc9 = get_int("请问是否需要结算？(1-->立即结算/2-->继续点餐/3-->取消本次订单)")
                            if uc9 == 2:
                                continue
                            elif uc9 == 3:
                                    
                                uc9_2 = get_int('请问是否取消本次订单？(1/2)')
                                    
                                if uc9_2 == 1:
                                    orders.clear()
                                    t.sleep(2)
                                    print("订单已取消......")
                                    return
                                else:
                                    return
                                
                            elif uc9 == 1:
                                    total_price = sum(dish['dish_price'] * dish['dish_amount'] for dish in orders)    
                                    
                                    print(f"当前账单总金额为:{total_price}")
                                    print()

                                    for num,dishes in enumerate(orders,start=1):
                                        print(f"菜品{num}: \n菜品名称:{dishes['dish_name']}\n菜品价格:{dishes['dish_price']}\n订购数量:{dishes['dish_amount']}\n")
                                    
                                    print()
                                    print("1.微信支付")
                                    print("2.支付宝支付")
                                    print("3.小米钱包支付")
                                    uc9_1 = get_int("请选择你的支付方式:")

                                    if uc9_1 in (1, 2, 3):
                                        # ★ 关键：把整单发给后厨
                                        st.get_order_queue().put(list(orders))
                                        
                                        orders.clear()
                                        t.sleep(3)
                                        return
                                    # if uc9_1 == 1:
                                    #     print("支付进行中......")
                                    #     t.sleep(1.5)
                                    #     print("支付成功！正在返回主菜单......")
                                    #     return
                                    # elif uc9_1 == 2:
                                    #     print("支付进行中......")
                                    #     t.sleep(1.5)
                                    #     print("支付成功！正在返回主菜单......")
                                    #     return
                                    # elif uc9_1 == 3:
                                    #     print("支付进行中......")
                                    #     t.sleep(1.5)
                                    #     print("支付成功！正在返回主菜单......")                        
                else:
                    print('Invalid Inputting!')
                    continue 
           
       

# 给后厨看的
def orders_receiving(dn1,dp1,da1):

    global orders

    or_template = {
        'dish_name':dn1,
        'dish_price':dp1,
        'dish_amount':da1

    }

    orders.append(or_template)
    print(f"成功订购菜品: {dn1} * {da1} 份")

    # print()
    # print('目前订单详情:')
    
    # for num,dishes in enumerate(orders,start=1):
        
    #     print(f"菜品{num}: \n菜品名称:{dishes['dish_name']}\n菜品价格:{dishes['dish_price']}\n订购数量:{dishes['dish_amount']}\n")
    
    return


count_2 = 1
def dishes_logs():
    global orders
    global count_2

    with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\订单日志.json','r',encoding='utf-8')as f:
        logs_data = j.load(f)
    
    logs = logs_data
    # print(logs)

    logs.append(orders)
    
    count_2 = count_2 + 1

    # print(logs)

    with open(r"C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\订单日志.json","+wt",encoding="utf-8")as f:
        # 这个是写到json日志里面的
        j.dump(logs, f, ensure_ascii=False, indent=2)
    
    # 这个是写到txt日志里面的
    with open("订单日志.txt",'r+',encoding="utf-8")as f:
        for log_numbers in range(1,count_2):
            
            print(f"Orders {log_numbers}: ")
            # f.write(f"\nOrders {log_numbers}: \n")
            
            for num,dis_info in enumerate(orders,start=1):
                
                print(f"{num}: {dis_info['dish_name']} --> {dis_info['dish_amount']}份")
                # f.write(f"{num}: {dis_info['dish_name']} --> {dis_info['dish_amount']}份\n")
    return


def dishes_adding(fn,fp):  
    global menu_template
    global menu

    menu_template = {
        "dish_name":fn,
        "dish_price":fp
    }
    
    menu.append(menu_template)

    # print(menu)   

    print("Contiune or returning to main menu?")
    
    while True:

        user_cho1 = get_int("Please enter 1 or 2:")

        if user_cho1 == 1:
            dishes_modifying_add()
        elif user_cho1 == 2:
            main()
            break

def dishes_modifying_add():    # 菜品添加
    global dishes_count
    # 这里要用while True，字符串类型数据只要阻止用户直接空格导致程序崩溃就可以了
    # get_int函数主要是用于控制int类型的数据接收问题
    while True:
        food_adding = str(input("Please enter name of the dish u want to add in:(Enter 0 to returning)"))
        if food_adding == "":
            print("Please enter the name of the dish!")
        elif food_adding == "0":
            return
        else:
            print(f"The name of the dish: {food_adding} is being added successfully!")
            break

    price_adding = get_int("Please enter the price of the dish u want to add in:")

    print(f"The price of the dish:{food_adding} is being added successfully!\nThe price is: ¥{price_adding}!")
    
    print("Food adding finished!......Return to menu......")

    dishes_count += 1

    return dishes_adding(food_adding,price_adding)

def menu_modifying_del():
    with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json','rt',encoding='utf-8')as f:
        data_del = j.load(f)
        print("Menu data:")

        # 打印菜单供管理员选择
        for num,dishes in enumerate(data_del,start=1):
            print(f"{num},{dishes['dish_name']} --> {dishes['dish_price']}")

        # 通过索引选择对应需要修改的菜品
        index_dishes = get_int("Please enter the number of the dish that you wanna delete:")
        del_dishes = data_del[index_dishes - 1]['dish_name']

        # 判断索引是否越界（是否输入了大于菜单序号的数字）
        if index_dishes < 1 or index_dishes > len(data_del):
            print("Invalid number!")
            return


        for dishes in data_del: 
            while True:
                if del_dishes not in dishes['dish_name']:
                    print(f"Could not find {del_dishes}!Please check again!")
                else:
                    print(f"Dish {del_dishes} have found! --> Price:{data_del[index_dishes - 1]['dish_price']}")
                break

            while True:
                uc5 = str(input(f"You sure u wanna delete dish {del_dishes}? (Enter y or n):")).strip()
                if uc5 == "":
                    print("You have not entered anything there!")
                elif uc5 == "n":
                    print("Returning......")
                    t.sleep(1.5)
                    return
                elif uc5 == "y":
                    print("Deleting......")
                    del data_del[index_dishes - 1]
                    t.sleep(3)
                    print(f"Dish {del_dishes} have been deleted successfully!")

                    # print(data_del[index_dishes - 1])
                    
                    t.sleep(1.5)
                    
                    with open(r"C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json",'wt',encoding='utf-8')as f:
                        j.dump(data_del, f, ensure_ascii=False, indent=2)
                        print(data_del)
                        print('')
                break
            break


def menu_modifying_price_md():
    with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json','r+',encoding='utf-8')as f:
        price_data = j.load(f)
        print(price_data)

        print("Menu:(Recently)")
        for num,price in enumerate(price_data,start=1):
            print(f"{num} {price['dish_name']} --> {price['dish_price']}")

        md_price_index = get_int("Please enter the number of the dish that u wanna modify:")

        if md_price_index < 1 or md_price_index > len(price_data):
            print("Number Invalid!")
        else:
            print(f'Dish {price_data[md_price_index - 1]['dish_name']} have found!')
            print(f'The price of the dish is ¥{price_data[md_price_index - 1]['dish_price']}!')

            uc6 = get_int("Do you wanna modify this dish?(Enter 1 to continue or 2 to return)")
            while True:
                if uc6 == "":
                    print("You have not entered anything in there!")
                else:
                    break
            uc6_price_md = get_int("Enter the price you want:")

            # 这个用于下面显示数据的变化（在修改这道菜的price之前先存住这个数据）
            price_data_saving = price_data[md_price_index - 1]['dish_price']

            price_data[md_price_index - 1]['dish_price'] = uc6_price_md

        with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json','wt',encoding='utf-8')as f:
            j.dump(price_data, f, ensure_ascii=False, indent=2)
            # print(price_data)
            t.sleep(2)
            print(f'The price of the dish have change:{price_data_saving} --> {uc6_price_md}')

            uc7 = get_int("Do you want to continue or returning to main menu?(Enter 1 or 2):")
            if uc7 == 1:
                menu_modifying_price_md()
            elif uc7 == 2:
                print("Returning......")
                t.sleep(2)
                main()

def Clear_Menu():
    with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json','r',encoding='utf-8')as f:
        clear_data = j.load(f)
        if not clear_data:
            print("Menu is empty!Please add some dishes in it!")
        else:

        # print(clear_data)
        # print(type(clear_data))
        
            uc8 = get_int("You sure u wanna clear menu?(Enter 1 to continue or 2 to returning):")
            if uc8 == 1:
                clear_data.clear()
                print("Menu have been cleared!")
                t.sleep(1.5)

                print("Returning......")
                t.sleep(1.5)
                # print(clear_data)
            else:
                return main()

            with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json','wt',encoding='utf-8')as f:
                j.dump(clear_data, f, ensure_ascii=False, indent=2)

                print(clear_data)

                if not clear_data:
                    print("Menu is empty!Please add some dishes in it!")
                    t.sleep(1.5)
                    return

def menu_saving():
# 每次程序结束前重写一次menu，即是存档的意思
# 必须要手动进入这个功能，但是在exit板块有写自动保存
    # print("写入路径:", os.path.abspath('菜品数据.json'))
    with open(r'C:\Users\weisheng\Desktop\本学期\代码练习\线程作业\菜品数据.json','wt',encoding='utf-8')as f:
        j.dump(menu, f, ensure_ascii=False, indent=2)

        t.sleep(1.5)

    print("Data saving successfully!")
    print("Backing to main menu......")

    t.sleep(1.5)
    main()

if __name__ == '__main__':
    loading()
