from datetime import datetime
import os

def get_formatted_time_with_seconds():
    """获取当前时间并格式化为字符串: 'YYYY_MM_DD_HH_MM_SS'"""
    now = datetime.now()
    return now.strftime('%Y_%m_%d_%H_%M_%S')



import os

def get_csv_and_png_paths(directory):
    csv_path = ""
    png_path = ""

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
            elif file.endswith('.png'):
                png_path = os.path.join(root, file)
            
    
    csv_path=csv_path.replace("\\","/")
    png_path=png_path.replace("\\","/")
    # print(csv_path,png_path)
    # csv_path="@/"+csv_path.split("/src/")[1]
    # png_path="@/"+png_path.split("/src/")[1]
    csv_path="/"+csv_path.split("/public/")[1]
    png_path="/"+png_path.split("/public/")[1]
    print(csv_path,png_path)

    return {"csv":csv_path, "png":png_path}



