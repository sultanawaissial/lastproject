from pathlib import Path
p = Path('lastapp/templates/my_admin/dashboard.html')
p.write_text('<h1>Dashboard FIXED</h1><p>Orders: {{ orders }}</p><p>Products: {{ products }}</p><p>Pending: {{ pending_orders }}</p><p>Revenue: {{ revenue }}</p>', encoding='utf-8')
print("Fixed done")