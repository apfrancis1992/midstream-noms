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

class Noms(Table):
    nom_id = Col("ID", show=False)
    contract_id = Col("Contract ID")
    day_nom = Col("Date")
    day_nom_value = Col("MMBTU")

class Companies(Table):
    company_id = Col("ID", show=False)
    company_name = Col("Company Name")
    company_type = Col("Company Type")
    status = Col("Active")
    edit = LinkCol('Edit', 'edit_company', url_kwargs=dict(company_id='company_id'))

class Contracts(Table):
    contract_id = Col("ID")
    producer = Col("Producer")
    marketer = Col("Marketer")
    contract_type = Col('Contract Type')
    day_due = Col('Day Due')
    active = Col("Active")
    edit = LinkCol('Edit', 'edit_contract', url_kwargs=dict(contract_id='contract_id'))