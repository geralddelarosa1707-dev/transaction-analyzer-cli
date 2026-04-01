import json

menu = {
  "VIEW": "View Current Transactions",
  "VIEW_ALL": "View All Transactions",
  "SALES": "Enter Sales",
  "EXPENSES": "Enter Expenses",
  "REMOVE": "Remove Item",
  "DELETE": "Delete Transaction",
  "SEARCH_I": "Search Item",
  "SEARCH_T": "Search Transaction",
  "UPDATE": "Update Item",
  "SAVE": "Save Current Transactions",
  "EXIT": "Exit Program"
}

def show_menu(menu):
  print("\n----------MENU-----------")
  for key, info in menu.items():
    print(f"{key}: {info}")
  print("-------------------------")
  
def display_items(items):
  if not items:
    print("\nThere are no items yet.")
    return False
  
  num = 0
  
  for name, price in items:
    num += 1
    print(f"{num}. {name.title()}: ₱{price}")
    
  return True
  
def show_items(items):
  if not items:
    print("There are no items yet.")
    return
  
  display_items(items)
  
def analyze_items(items):
  if not items:
    return None, None, None
    
  highest = max(items, key=lambda x:x[1])
  lowest = min(items, key=lambda x:x[1])
  average = sum(price for name, price in items) / len(items)
  
  return highest, lowest, average
    
def show_summary(item_sales, item_expenses):
  highest, lowest, average = analyze_items(item_sales)
  
  print("\n--------SUMMARY----------")
  
  if highest:
    print(f"Highest Sale: {highest[0].title()} - ₱{highest[1]}")
    print(f"Lowest Sale: {lowest[0].title()} - ₱{lowest[1]}")
    print(f"Average Sale: ₱{average:.2f}")
    
  highest, lowest, average = analyze_items(item_expenses)
  
  if highest:
    print(f"\nHighest Expense: {highest[0].title()} - ₱{highest[1]}")
    print(f"Lowest Expense: {lowest[0].title()} - ₱{lowest[1]}")
    print(f"Average Expense: ₱{average:.2f}")
    
def show_total(total_num_transaction, total_sales, total_expenses, net_profit, item_sales, item_expenses):
  print("\n----------TOTAL----------")
  print(f"Total Transactions: {total_num_transaction}")
  print(f"Total Sales: ₱{total_sales}")
  print(f"Total Expenses: ₱{total_expenses}")
    
  if total_sales < total_expenses:
    print(f"Total Loss: ₱{abs(net_profit)}")
  elif total_sales == total_expenses:
    print(f"Break-even: ₱{net_profit}")
  else:
    print(f"Total Profit: ₱{net_profit}")
    
  show_summary(item_sales, item_expenses)
  
def show_transactions(data):
  print("\n     SALES:")
  for name, price in data.get("item_sales", []):
    print(f"   - {name.title()}: ₱{price}")
        
  print("\n     EXPENSES:")
  for name, price in data.get("item_expenses", []):
    print(f"   - {name.title()}: ₱{price}")
  
def validate_item(item):
  if not item:
    print("\nPlease enter a name and price.")
    return None

  split_item = item.split(",")
      
  if len(split_item) != 2:
    print("\nPlease enter a name and price (separated by ',').")
    print("\nExample: Mocha, 29")
    return None
  
  name = split_item[0].strip()
  clean_price = split_item[1].strip()
      
  try:
    price = int(clean_price)
  except ValueError:
    print("\nPlease enter a valid number.")
    return None
  
  return name, price
  
def validate_removing_item(list_item):
  if not display_items(list_item):
    return None
      
  try:
    enter_item = int(input("\nEnter the number of item: "))
  except ValueError:
    print("\nPlease enter only a number.")
    return None
      
  if enter_item < 1 or enter_item > len(list_item):
    print("\nPlease enter a valid number.")
    return None
      
  index = enter_item - 1
        
  item = list_item[index]
        
  confirm = input(f"\nAre you sure you want to delete {item} (y/n): ").lower()
        
  if confirm != "y":
    print("\nDeleting cancelled!")
    return None
  
  del list_item[index]
  print("\nDeleted successfully!")
    
  return enter_item
  
def search_item(item_name, field):
  num = 0
      
  for name, price in field:
    if item_name.lower() == name.lower():
      num += 1
      
  if num == 0:
    print(f"\nNo '{item_name.title()}' found.")
    return None
  else:
    print(f"\n{num} '{item_name.title()}' found:")
      
  num = 0
      
  for name, price in field:
    if item_name.lower() == name.lower():
      num += 1
      print(f"{num}. {name.title()}: ₱{price}")
      
def update_item(items):
  if not items:
    return False
  
  try:
    item_num = int(input("\nEnter item number: "))
  except ValueError:
    print("\nPlease enter only a number.")
    return False
      
  if item_num < 1 or item_num > len(items):
    print("\nPlease enter a valid number")
    return False
      
  item = input("\nEnter name and price (separated by ','): ")
      
  get_item = validate_item(item)
      
  if get_item is None:
    return False
      
  index = item_num - 1
  items[index] = get_item
  
  print("\nUpdated successfully!")
  return True
  
def load_from_file():
  try:
    with open("transactions.json", "r") as file:
      data = json.load(file)
      
      if not isinstance(data, dict):
        print("\nWarning: Invalid file format.")
        return {}, [], []
        
      transactions_data = data.get("transactions", {})
      
      if not isinstance(transactions_data, dict):
        print("\nWarning: Transactions corrupted. Resetting.")
        transactions_data = {}
      
      transactions = {}
      
      for date, trans in transactions_data.items():
        transactions[date] = {
          "item_sales": [tuple(item) for item in trans.get("item_sales", [])],
          "item_expenses": [tuple(item) for item in trans.get("item_expenses", [])]
        }
        
      item_sales = []
      item_expenses = []
        
      return transactions, item_sales, item_expenses
      
  except FileNotFoundError:
    return {}, [], []
    
  except json.JSONDecodeError:
    print("Warning: File corrupted. Resetting data.")
    return {}, [], []
  
def save_to_file(transactions):
  with open("transactions.json", "w") as file:
    data = {
      "transactions": transactions,
    }
    
    json.dump(data, file, indent=4)

def main_program(transactions, item_sales, item_expenses):
  print("Welcome to Transaction Analyzer!")
  
  while True:
    show_menu(menu)
    
    option = input("\nWhat would you like to do: ").upper()
    
    if option == "SALES":
      while True:
        income = input("\nEnter name and price (separated by ','): ")
        
        get_item = validate_item(income)
        
        if get_item is None:
          continue
    
        item_sales.append(get_item)
      
        proceed = input("\nAdd again (y/n): ").lower()
      
        if proceed != "y":
          print("\nAdded successfully!")
          break
        
    elif option == "EXPENSES":
      while True:
        expense = input("\nEnter name and price (separated by ','): ")
        
        get_item = validate_item(expense)
        
        if get_item is None:
          continue
        
        item_expenses.append(get_item)
        
        proceed = input("\nAdd again (y/n): ").lower()
        
        if proceed != "y":
          print("\nAdded successfully!")
          break
    
    elif option == "VIEW":
      if not item_sales and not item_expenses:
        print("\nThere are no current Transactions yet.")
        continue
      
      total_num_transaction = len(item_sales) + len(item_expenses)
      
      total_sales = sum(price for name, price in item_sales)
        
      total_expenses = sum(price for name, price in item_expenses)
        
      net_profit = total_sales - total_expenses
      
      print("\n============TRANSACTIONS===========")
      
      print("\n----------SALES----------")
      print(f"Sales Transactions: {len(item_sales)}")
      
      show_items(item_sales)
      
      print("\n---------EXPENSES--------")
      print(f"Expense Transactions: {len(item_expenses)}")
      
      show_items(item_expenses)
      
      show_total(total_num_transaction, total_sales, total_expenses, net_profit, item_sales, item_expenses)
      
      print("\n===================================")
        
      input("\nPress Enter to continue...")
      
    elif option == "VIEW_ALL":
      if not transactions:
        print("\nNo transactions yet.")
        continue
      
      for date, data in transactions.items():
        print(f"\n========DATE: {date}========")
        
        show_transactions(data)
        
      input("\nPress Enter to continue...")
      
    elif option == "REMOVE":
      choose_field = input("\nEnter field (SALES / EXPENSES): ").strip().upper()
      
      if not choose_field:
        print("\nPlease enter a field.")
        continue
      
      if choose_field == "SALES":
        print("\n----------SALES----------")
        
        get_item = validate_removing_item(item_sales)
        
        if get_item is None:
          continue
          
      elif choose_field == "EXPENSES":
        print("\n---------EXPENSES--------")
        
        get_item = validate_removing_item(item_expenses)
        
        if get_item is None:
          continue
        
      else:
        print("\nPlease enter a valid field.")
        
      input("\nPress Enter to continue...")
      
    elif option == "DELETE":
      date = input("\nEnter transaction date (YYYY/MM/DD): ").strip()
      
      if not date:
        print("\nPlease enter a date.")
        continue
      
      if date not in transactions:
        print(f"\nTransaction with date {date} not found.")
        continue
          
      confirm = input(f"\nAre you sure you want to delete transaction with date {date} (y/n): ").strip().lower()
          
      if confirm != "y":
        print("\nDeleting transaction cancelled!")
        continue
          
      del transactions[date]
          
      print(f"\nTransaction with date {date} deleted successfully!")
          
      save_to_file(transactions)
        
    elif option == "SEARCH_I":
      field = input("\nEnter field (SALES / EXPENSES): ").strip().upper()
      
      if not field:
        print("\nPlease enter a field")
        continue
      
      if field == "SALES":
        item_name = input("\nEnter item name: ").strip().lower()
        
        if not item_name:
          print("\nPlease enter item name.")
          continue
        
        show_item = search_item(item_name, item_sales)
        
        if show_item is None:
          continue
        
      elif field == "EXPENSES":
        item_name = input("\nEnter item name: ").strip().lower()
        
        if not item_name:
          print("\nPlease enter item name.")
          continue
        
        show_item = search_item(item_name, item_expenses)
        
        if show_item is None:
          continue
        
      else:
        print("\nPlease enter a valid field.")
            
      input("\nPress Enter to continue...")
      
    elif option == "SEARCH_T":
      enter_date = input("\nEnter date (YYYY/MM/DD): ").strip()
      
      if not enter_date:
        print("\nPlease enter a date.")
        continue
    
      if enter_date not in transactions:
        print(f"\nTransaction with date {enter_date} not found.")
        continue
        
      data = transactions[enter_date]
        
      print(f"========DATE: {enter_date}========")
        
      show_transactions(data)
      
      input("\nPress Enter to continue...")
    
    elif option == "UPDATE":
      field = input("\nEnter field (SALES / EXPENSES): ").strip().upper()
      
      if not field:
        print("\nPlease enter a field")
        continue
      
      if field == "SALES":
        if not display_items(item_sales):
          continue
        
        if not update_item(item_sales):
          continue
        
      elif field == "EXPENSES":
        if not display_items(item_expenses):
          continue
        
        if not update_item(item_expenses):
          continue
            
      else:
        print("\nPlease enter a valid field.")
        
      input("\nPress Enter to continue...")
      
    elif option == "SAVE":
      date = input("\nEnter date (YYYY/MM/DD): ").strip()
      
      if not date:
        print("\nPlease enter a date.")
        continue
      
      if not item_sales and not item_expenses:
        print("\nNothing to save.")
        continue
      
      if date in transactions:
        print("\nDate already exists. Use another date.")
        continue
      
      transactions[date] = {
        "item_sales": item_sales.copy(),
        "item_expenses": item_expenses.copy()
      }
      
      save_to_file(transactions)
      
      item_sales.clear()
      item_expenses.clear()
      
      print("\nTransactions cleared. Start new entry.")
      
      print("\nTransaction saved successfully!")
      
    elif option == "EXIT":
      if item_sales or item_expenses:
        confirm = input("\nYou have unsaved changes. Are you sure you want to exit (y/n)? ").strip().lower()
        
        if confirm != "y":
          continue
        else:
          print("\nBye! :)")
          break
      
      else:
        print("\nBye! :)")
        break
      
    else:
      print("\nPlease enter a valid option.")
      
if __name__ == "__main__":
  transactions, item_sales, item_expenses = load_from_file()
  main_program(transactions, item_sales, item_expenses)