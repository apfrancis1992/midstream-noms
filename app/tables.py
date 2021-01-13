from flask_table import Table, Col, LinkCol

class Results(Table):
    nom_id = Col('Id', show=False)
    day_nom = Col("Day")
    contract_id = Col("Contract")
    delivery_id = Col('Delivery Point')
    donwstream_contract = Col('Downstream Contract')
    downstream_ba = Col('Downstream BA')
    rank = Col('Rank')
    day_nom_value = Col('MMBTU')
    user_id = Col("User")

class Users(Table):
    id = Col("ID", show=False)
    username = Col("Username")
    first_name = Col("First Name")
    last_name = Col("Last Name")
    email = Col("Email")
    company = Col("Company")
    title = Col("Title")
    phone = Col("Phone")
    role = Col("Permissions")
    edit = LinkCol('Edit', 'user_edit', url_kwargs=dict(id='id'))