from pymongo import MongoClient

con = MongoClient('mongodb+srv://cauasbl:uRjwOMQ44k7vnaUb@pymongo.ttb7i.mongodb.net/')

db = con.perfumaria

usuarios_collection = db.usuarios
produtos_collection = db.produtos
estoque_collection = db.estoque
compras_collection = db.compras
itens_comprados_collection = db.itens_comprados

def cadastro_usuario(nome, email, senha, tipo_usuario="normal"):
    
    usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "tipo_usuario": tipo_usuario,
    }

    usuarios_collection.insert_one(usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")

def cadastro_produto(nome, descricao, preco, tamanho, marca):
   
    produto = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "tamanho": tamanho,
        "marca": marca,
    }

    produtos_collection.insert_one(produto)
    print(f"Produto {nome} cadastrado com sucesso!")

def ad_estoque(produto_id, quantidade):
    
    estoque = estoque_collection.find_one({"produto_id": produto_id})

    if estoque:
       
        estoque_collection.update_one(
            {"produto_id": produto_id},
            {"$inc": {"quantidade": quantidade}}
        )
        print(f"{quantidade} unidades do produto {produto_id} foram adicionadas ao estoque!")
    else:
        
        estoque_collection.insert_one({
            "produto_id": produto_id,
            "quantidade": quantidade
        })
        print(f"Produto {produto_id} adicionado ao estoque com {quantidade} unidades!")

def registro_compras(usuario_id, lista_produtos):
    
    total = 0
    
    for produto in lista_produtos:
        total += produto['quantidade'] * produto['preco_unitario']
    
    compra = {
        "usuario_id": usuario_id,
        "total": total,
        "itens_comprados": lista_produtos
    }

    compra_id = compras_collection.insert_one(compra).inserted_id

    for item in lista_produtos:
        item_comprado = {
            "compra_id": compra_id,
            "produto_id": item["produto_id"],
            "quantidade": item["quantidade"],
            "preco_unitario": item["preco_unitario"]
        }

        itens_comprados_collection.insert_one(item_comprado)

        estoque_collection.update_one(
            {"produto_id": item["produto_id"]},
            {"$inc": {"quantidade": -item["quantidade"]}}
        )

    print(f"Compra realizada com sucesso! Total: R${total:.2f}")