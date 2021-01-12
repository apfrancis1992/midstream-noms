from flask_table import Table, Col

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