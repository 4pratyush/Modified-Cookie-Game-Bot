from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter import messagebox
from turtle import Screen
import time

selenium_path = "C:\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(
    executable_path=selenium_path)

screen = Screen()
screen.setup(width=0, height=0)

time_constraint_input = screen.textinput(title="Enter the run-time for your bot",
                                         prompt="How many minutes bot should run? Enter minutes range( 1 to 15 ) :")

if not time_constraint_input.isdigit():
    Error_Message = messagebox.showinfo(title="Invalid Input Integer",
                                        message="Error- Please enter valid number in minutes")
    quit()

if (int(time_constraint_input) < 1) or (int(time_constraint_input) > 15):
    Error_Message = messagebox.showinfo(title="Invalid Input Integer",
                                        message="Error- Please enter valid number in minutes")
    quit()

time_constraint = int(time_constraint_input)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

# List to store the item IDS.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
items_IDS = [item.get_attribute("id") for item in items]
# print(items)

final_cps = None
time_check = time.time() + 5
time_out = time.time() + time_constraint * 60

while True:
    cookie.click()

    # Here, we check for upgrades every 5 seconds
    if time.time() > time_check:
        # Extracting the price of the list.
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        # for n in all_prices:
        # print(n.text)
        item_prices = []

        # Separating the cost from the prices list
        for n in all_prices:
            price_data = n.text
            if price_data != "":
                cost_in_integer = int(price_data.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost_in_integer)

        # Storing the extracted prices and ids in a dictionary
        Cookie_upgrades = {}
        for n in range(len(item_prices)):
            Cookie_upgrades[item_prices[n]] = items_IDS[n]
            # Here, prices are keys and id's or respective item name are id's as values.

        # Checking Over-pricing of the items
        value_Cookie_upgrades = {}
        Over_price_limit = [500, 2000, 7000, 50000, 1000000, 100000000, 248000000, 1]
        n = 0
        for price, ID in Cookie_upgrades.items():
            if price <= Over_price_limit[n]:
                value_Cookie_upgrades[price] = ID
            elif Cookie_upgrades[price] == 'buyTime machine':
                value_Cookie_upgrades[price] = ID
            else:
                value_Cookie_upgrades[price] = 0
            n = n + 1
        Cookie_upgrades = value_Cookie_upgrades

        # Get the current cookie count
        current_money = driver.find_element(By.ID, "money").text
        int_money = int(current_money.replace(",", ""))

        # Finding the elements that we can afford
        affordable_upgrades = {}
        for cost, ID in Cookie_upgrades.items():
            if int_money > cost and Cookie_upgrades[cost] != 0:
                affordable_upgrades[cost] = ID

        # Finding  the most expensive affordable upgrade
        if len(affordable_upgrades) != 0:
            highest_upgrade_price = max(affordable_upgrades)
            purchase_id = affordable_upgrades[highest_upgrade_price]

            # Purchasing the most expensive item
            driver.find_element(By.ID, purchase_id).click()

        # Incrementing the execution time_check by 5 seconds
        time_check = time.time() + 5

    if time_check > time_out:
        cookie_per_second = driver.find_element(By.ID, "cps").text
        final_cps = cookie_per_second
        break

driver.quit()
Pop_up_message = messagebox.showinfo(title="The Highest CPS(coins per second) achieved",
                                     message=f"{final_cps}-cps achieved in the time constraint of {time_constraint}"
                                             " minutes in the current run")
print(final_cps)
# driver.close()  # This method simply closes the website that we have opened, but it closes only one particular tab.
# driver.quit()  # Closes the whole browser.
