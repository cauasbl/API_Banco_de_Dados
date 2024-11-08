from pymongo import MongoClient

con = MongoClient('mongodb+srv://cauasbl:uRjwOMQ44k7vnaUb@pymongo.ttb7i.mongodb.net/')
db = con.perfumaria

usuarios_collection = db.usuarios
produtos_collection = db.produtos
estoque_collection = db.estoque
compras_collection = db.compras
itens_comprados_collection = db.itens_comprados

def cadastro_usuario(nome, email, senha, tipo_usuario="cliente"):
    usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "tipo_usuario": tipo_usuario
    }

    usuarios_collection.insert_one(usuario)
    print(f"Usuário {nome} cadastrado com sucesso como {tipo_usuario}!")

def cadastro_produto(nome, descricao, preco, tamanho, marca, usuario):
    if usuario["tipo_usuario"] != "admin":
        print("Permissão negada: apenas administradores podem cadastrar produtos.")
        return

    produto = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "tamanho": tamanho,
        "marca": marca
    }

    produtos_collection.insert_one(produto)
    print(f"Produto {nome} cadastrado com sucesso!")

def ad_estoque(produto_id, quantidade, usuario):
    if usuario["tipo_usuario"] != "admin":
        print("Permissão negada: apenas administradores podem atualizar o estoque.")
        return

    estoque_collection.update_one(
        {"produto_id": produto_id},
        {"$inc": {"quantidade": quantidade}},
        upsert=True
    )
    print(f"{quantidade} unidades do produto {produto_id} foram adicionadas ao estoque!")

def registro_compras(usuario_id, lista_produtos, usuario):
    if usuario["tipo_usuario"] != "cliente":
        print("Permissão negada: apenas clientes podem realizar compras.")
        return
    
    total = 0
    for produto in lista_produtos:
        total += produto['quantidade'] * produto['preco_unitario']
    
    compra = {
        "usuario_id": usuario_id,
        "total": total,
        "itens_comprados": lista_produtos
    }

    compra_id = compras_collection.insert_one(compra).inserted_id

    itens_comprados = []

    for item in lista_produtos:
        item_comprado = {
            "compra_id": compra_id,
            "produto_id": item["produto_id"],
            "quantidade": item["quantidade"],
            "preco_unitario": item["preco_unitario"]
        }

        itens_comprados.append(item_comprado)

    itens_comprados_collection.insert_many(itens_comprados)
    
    for item in lista_produtos:
        estoque_collection.update_one(
            {"produto_id": item["produto_id"]},
            {"$inc": {"quantidade": -item["quantidade"]}}
        )

    print(f"Compra realizada com sucesso! Total: R${total:.2f}")

def relatorio_compras(usuario):
    if usuario["tipo_usuario"] != "admin":
        print("Permissão negada: apenas administradores podem visualizar relatórios de compras.")
        return

    compras = compras_collection.find()
    for compra in compras:
        print(f"Compra ID: {compra['_id']}, Usuário ID: {compra['usuario_id']}, Total: R${compra['total']:.2f}")