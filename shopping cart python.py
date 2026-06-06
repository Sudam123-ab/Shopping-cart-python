products = [
    {"id": 1, "name": "Laptop",    "price": 55000, "stock": 5},
    {"id": 2, "name": "Phone",     "price": 15000, "stock": 10},
    {"id": 3, "name": "Headphones","price": 2000,  "stock": 8},
    {"id": 4, "name": "Keyboard",  "price": 1500,  "stock": 15},
    {"id": 5, "name": "Mouse",     "price": 800,   "stock": 20},
]
cart=[]
discount=0
coupon_applied=False
from datetime import datetime

def view_products():
    if len(products)==0:
        print("Products Not Found")
    else:
        for i in range(len(products)):
            print(f"{products[i]['id'] } | {products[i]['name']} | {products[i]['price']} | {products[i]['stock']}")    
    

def add_to_cart():
    while True:
        try:
            p_id=int(input("Enter a Number :"))
            break  
        except ValueError:
            print("Enter numbers only!")

    found_product=None
    for product in products:
        if p_id==product["id"]:
            found_product=product
            break
    if found_product is None:
        print("invalid product id!")    
        return

    
    while True:
        try:
            qty=int(input("Enter a quantity:"))
            if qty<=0:
                print("Quantity must be more than 0!")
                continue
            break
        except ValueError:
            print("Enter a numbers only!")

    if qty>found_product["stock"]:
        print(f"Only {found_product['stock']} items in stock!")   
        return

    for item in cart:     
        if item["id"]==p_id:
            item["quantity"]+=qty
            found_product["stock"]-=qty
            print("cart updated!")
            return

    cart.append({
        "id":found_product["id"],
        "name":found_product["name"],
        "price":found_product["price"],
        "quantity":qty
    })    
    found_product["stock"]-=qty
    print(f"{found_product['name']} added to cart!")

def remove_from_cart():
    while True:
        try :
            p_id=int(input("Enter a product ID "))
            break
        except ValueError:
            print("Only number is allowed")
    for item in cart:
        if item["id"]==p_id:  
            for product in products:
                if product["id"]==p_id:
                    product["stock"]+=item["quantity"]
                    break   
            cart.remove(item)             
            print(f"{item['name']} remove from cart!")
            return
    print("Item not in cart!")    

def view_cart():
    if len(cart)==0:
        print("Cart is empty!")
        return
    print("\n---Your Cart---")
    subtotal=0
    for i,item in enumerate(cart):
        item_total=item["price"]*item["quantity"]
        subtotal+=item_total
        print(f"{i+1}.{item['name']:<15} x{item['quantity']}={item_total}")

    print("-"*35)
    print(f"subtotal:{subtotal}")    

    if coupon_applied:
        print(f"Discount :-{discount}")
        print(f"Total    :{subtotal-discount}")
    else:
        print(f"Total  : {subtotal}")    

coupons={
    "SAVE10":("percent",10),
    "SAVE20":("percent",20),
    "FLAT500":("flat",500)
}        
      
def apply_coupon():
    global discount,coupon_applied

    if coupon_applied:
        print("Coupon already applied!")
        return
    
    code =input("Enter coupon code:").upper()

    if code in coupons:
        subtotal=0
        for item in cart:
            subtotal+=item["price"]*item["quantity"]
        coupon_type,coupon_value=coupons[code]

        if coupon_type=="percent":
            discount=subtotal*coupon_value/100 
        elif coupon_type=="flat":
            discount=coupon_value
        coupon_applied=True
        print(f"Coupon applied! You save {discount}")          

    else:
        print("Invalid coupon!")     


def checkout():
    global discount,coupon_applied

    if len(cart)==0:
        print("Cart is empty!")
        return
    
    subtotal=0
    for item in cart:
        subtotal+=item["price"]*item["quantity"]

    final_total=subtotal - discount


    print("\n---Final Bill---")
    print(f"Subtotal : {subtotal}")
    print(f"Discount:-{discount}")
    print(f"Total :{final_total}") 

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    with open("order.csv","a") as file:
        for item in cart:
            file.write(f"{now},{item['name']},{item['quantity']},{item['price']},{final_total}\n")

    cart.clear()
    discount=0
    coupon_applied=False

    print("Order placed !Thank you ")        

def view_order_history():
    try:
        with open("order.csv","r") as file:
            print("\n---Order History---")
            for line in file:
                parts=line.strip().split(",")
                print(f"{parts[0]} | {parts[1]} x{parts[2]} | Total:{parts[4]}")
    except FileNotFoundError:
        print("no orders yet!")            



while True:
    print("\n---Shopping Cart---")
    print("1.View products")
    print("2.Add to cart")
    print("3.Remove from cart")
    print("4.View cart")
    print("5.Apply coupon")
    print("6.checkout")
    print("7.order history")
    print("8.exit")

    while True:
        try:
            choice=int(input("Enter a choice :"))
            if choice<1 or choice>8:
                print("Enter number between 1 to 8")
                continue
            break
        except ValueError:
            print("Number only")

    if choice==1:
        view_products()
    elif choice==2:
        add_to_cart()
    elif choice==3:
        remove_from_cart()
    elif choice==4:
        view_cart()
    elif choice==5:
        apply_coupon()
    elif choice==6:
        checkout()
    elif choice==7:
        view_order_history()
    elif choice==8:
        print("Goodbye")
        break                                    