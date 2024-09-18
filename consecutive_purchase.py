import csv
from datetime import datetime

def find_consecutive_purchases(filename):
  """
  Finds email addresses that bought the same product code more in consecutive months.

  Args:
    filename: The name of the CSV file.

  Returns:
    A list of tuples containing the email address and the product code.
  """

  data = []
  with open(filename, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row
    for row in reader:
      email, product_code, purchase_date = row
      purchase_date = datetime.strptime(purchase_date, '%d/%m/%Y')
      data.append((email, product_code, purchase_date))

  consecutive_purchases = []
  for email, product_code, purchase_date in data:
    # Find all purchases of the same product code by the same email
    same_product_purchases = [
      (p_date, p_code)
      for p_email, p_code, p_date in data
      if p_email == email and p_code == product_code
    ]


    # Sort purchases by date
    same_product_purchases.sort(key=lambda x: x[0])

    # Check for consecutive purchases
    is_consecutive = True
    for i in range(1, len(same_product_purchases)):
      prev_date, prev_code = same_product_purchases[i - 1]
      curr_date, curr_code = same_product_purchases[i]
      if (curr_date - prev_date).days > 31 or curr_code != prev_code:
        is_consecutive = False
        break

    # Check if there's a purchase of a different product after the consecutive purchases
    if is_consecutive:
      last_consecutive_date = same_product_purchases[-1][0]
      has_different_purchase = False
      for p_email, p_code, p_date in data:
        if p_email == email and p_date > last_consecutive_date and p_code != product_code:
          has_different_purchase = True
          break

      if has_different_purchase:
        consecutive_purchases.append((email, product_code))

  return consecutive_purchases

# Example usage
filename = 'sd2.csv'
results = find_consecutive_purchases(filename)
print(results)

