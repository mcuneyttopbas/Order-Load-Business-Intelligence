import pandas as pd
import pymongo

#   Username and Password is needed to send a request to database
username = ""
password = ""
#   File we want to sync with our database has to be shared here as a path
file = r"C:\Users\Asus\Desktop\sample_products.xlsx"

def synchronize(username,password,file,sheet_index):
    myclient = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.asdnj.mongodb.net/app_test?retryWrites=true&w=majority")
    mydb = myclient["order-load"]
    product_coll = mydb["products"]

    xl = pd.ExcelFile(file)

    data_frame1 = xl.parse(sheet_index) 
    index = data_frame1.index
    number_of_rows = len(index) 

    products = {}

    for i in range(number_of_rows):

        product_name = data_frame1["AD"][i]
        product_code = str(data_frame1["RENK KOD"][i])[:-3]
        color_code = data_frame1["RENK KOD"][i]
        width = data_frame1["EN"][i]
        composition = data_frame1["KOMPOZİSYON"][i]
        weight = data_frame1["GR/M²"][i]
        product_type = data_frame1["ÜRÜN CİNSİ"][i]
        usage = data_frame1["KULLANIM ALANI"][i]
        supplier_name = data_frame1["TEDARİKÇİ"][i]
        supplier_product_name = data_frame1["TEDARİKÇİ AD"][i]
        supplier_product_color = data_frame1["TEDARİKÇİ RENK KOD"][i]

        if product_name is not None:
            if product_name in products:
                products[product_name]["color_codes"].append({"color_code":color_code})
            else: 
                products[product_name] = {
                    "code":product_code,
                    "supplier":supplier_name,
                    "supplier_product_name":supplier_product_name,
                    "type":product_type,
                    "usage":usage,
                    "width":width,
                    "weight":weight,
                    "composition":composition,
                    "color_codes" : [{"color_code":color_code}]
            }
        else:
            continue
        
    product_data = {}

    for product in products:
        try:
            product_data = {
                "_id" : product,
                "code":products[product]["code"],
                "supplier":products[product]["supplier"],
                "supplier_product_name":products[product]["supplier_product_name"],
                "type":products[product]["type"],
                "usage":products[product]["usage"],
                "width":products[product]["width"],
                "weight":products[product]["weight"],
                "composition":products[product]["composition"],
                "color_codes" : []
                }
            for i in range(len(products[product]['color_codes'])):
                product_data["color_codes"].append(products[product]['color_codes'][i]['color_code'])
            product_coll.insert_one(product_data)
        except pymongo.errors.DuplicateKeyError:
            continue


if __name__ == "__main__":
    synchronize(username,password,file,0)
    synchronize(username,password,file,1)