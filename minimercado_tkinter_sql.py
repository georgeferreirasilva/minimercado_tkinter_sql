import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
import datetime
import mysql.connector

class MinimercadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Minimercado")
        self.root.geometry("750x650")
        self.usuario_logado = None
        self.carrinho = []
        self.total_venda = 0.00

        # Configurações do Banco de Dados
        self.db_config = {
            "user": "root",  # Substitua pelo seu usuário do MySQL
            "password": "VpG38#404",  # Substitua pela sua senha do MySQL
            "host": "localhost",  # ou o endereço do seu servidor MySQL
            "database": "testemercado"  # Substitua pelo nome do seu banco de dados
        }
        self.conectar_bd()
        # self.criar_tabelas()  # Garante que as tabelas existem
        self.criar_tela_login()

    def conectar_bd(self):
        try:
            self.db_connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao conectar ao banco de dados: {err}")
            self.root.destroy()  # Fecha o aplicativo se não conseguir conectar ao BD
            
    def criar_tabelas(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    usuario VARCHAR(50) PRIMARY KEY,
                    senha VARCHAR(50) NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    codigo VARCHAR(20) PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    preco_custo DECIMAL(10, 2) NOT NULL,
                    preco_venda DECIMAL(10, 2) NOT NULL,
                    estoque INT NOT NULL,
                    unidade VARCHAR(20) NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    data DATETIME NOT NULL,
                    total DECIMAL(10, 2) NOT NULL,
                    forma_pagamento VARCHAR(50) NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS itens_venda (
                    venda_id INT,
                    produto_codigo VARCHAR(20),
                    quantidade INT NOT NULL,
                    preco_unitario DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (venda_id) REFERENCES vendas(id),
                    FOREIGN KEY (produto_codigo) REFERENCES produtos(codigo),
                    PRIMARY KEY (venda_id, produto_codigo)
                )
            """)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao criar tabelas: {err}")
            self.root.destroy()

    def criar_tela_login(self):
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="Usuário").pack()
        self.entry_usuario = tk.Entry(frame)
        self.entry_usuario.pack()

        tk.Label(frame, text="Senha").pack()
        self.entry_senha = tk.Entry(frame, show="*")
        self.entry_senha.pack()

        tk.Button(frame, text="Entrar", command=self.verificar_login).pack(pady=10)
        tk.Button(frame, text="Sair", command=self.fechar_tela_login).pack()

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        try:
            self.cursor.execute("SELECT senha FROM usuarios WHERE usuario = %s", (usuario,))
            result = self.cursor.fetchone()
            if result and result[0] == senha:
                self.usuario_logado = usuario
                self.menu_principal()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao verificar login: {err}")

    def fechar_tela_login(self):
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()
        self.root.destroy()

    def menu_principal(self):
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Menu Principal", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(frame, text=f"Bem-vindo(a), {self.usuario_logado}").pack(pady=5)

        botoes = [
            ("Ponto de Venda", self.ponto_de_venda),
            ("Cadastrar Produto", self.cadastrar_produto),
            ("Controle de Estoque", self.controle_estoque),
            ("Cadastrar Usuário", self.cadastrar_usuario),
            ("Histórico de Vendas", self.historico),
            ("Sair", self.criar_tela_login)
        ]

        for texto, comando in botoes:
            tk.Button(frame, text=texto, width=30, command=comando).pack(pady=5)
            
    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def cadastrar_usuario(self):
        if self.usuario_logado != "admin":
            messagebox.showerror("Erro", "Apenas o administrador pode cadastrar usuários.")
            return
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Cadastrar Novo Usuário", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(frame, text="Usuário:").pack()
        entry_user = tk.Entry(frame)
        entry_user.pack()

        tk.Label(frame, text="Senha:").pack()
        entry_pass = tk.Entry(frame)
        entry_pass.pack()

        def salvar_usuario():
            u = entry_user.get()
            s = entry_pass.get()
            try:
                self.cursor.execute("SELECT usuario FROM usuarios WHERE usuario = %s", (u,))
                result = self.cursor.fetchone()
                if result:
                    messagebox.showerror("Erro", "Usuário já existe.")
                else:
                    self.cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (u, s))
                    self.db_connection.commit()
                    messagebox.showinfo("Sucesso", "Usuário cadastrado.")
                    self.menu_principal()
            except mysql.connector.Error as err:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao cadastrar usuário: {err}")

        tk.Button(frame, text="Salvar", command=salvar_usuario).pack(pady=10)
        tk.Button(frame, text="Voltar", command=self.menu_principal).pack()

    def cadastrar_produto(self):
        if self.usuario_logado not in ["admin", "gerente"]:
            messagebox.showerror("Erro", "Acesso negado.")
            return
        self.limpar_janela()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Cadastro de Produto", font=("Helvetica", 14, "bold")).pack(pady=10)

        campos = {}
        labels = ["Código", "Nome", "Preço Custo", "Preço Venda", "Estoque"]
        for label in labels:
            tk.Label(frame, text=label).pack()
            campo = tk.Entry(frame)
            campo.pack()
            campos[label.lower().replace(" ", "_")] = campo

        tk.Label(frame, text="Unidade").pack()
        unidade = Combobox(frame, values=["kg", "g", "ml", "l", "un", "rolos"])
        unidade.pack()

        def salvar():
            try:
                codigo = campos["código"].get()
                nome = campos["nome"].get()
                preco_custo = float(campos["preço_custo"].get())
                preco_venda = float(campos["preço_venda"].get())
                estoque = int(campos["estoque"].get())
                uni = unidade.get()

                self.cursor.execute("SELECT codigo FROM produtos WHERE codigo = %s", (codigo,))
                result = self.cursor.fetchone()
                if result:
                    messagebox.showerror("Erro", "Produto já cadastrado.")
                    return

                self.cursor.execute("""
                    INSERT INTO produtos (codigo, nome, preco_custo, preco_venda, estoque, unidade)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (codigo, nome, preco_custo, preco_venda, estoque, uni))
                self.db_connection.commit()
                messagebox.showinfo("Sucesso", "Produto cadastrado.")
                self.menu_principal()
            except mysql.connector.Error as err:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao cadastrar produto: {err}")
            except ValueError:
                messagebox.showerror("Erro", "Dados inválidos.")

        tk.Button(frame, text="Salvar Produto", command=salvar).pack(pady=10)
        tk.Button(frame, text="Voltar", command=self.menu_principal).pack()
        
    def controle_estoque(self):
        if self.usuario_logado not in ["admin", "gerente"]:
            messagebox.showerror("Erro", "Acesso negado.")
            return
        self.limpar_janela()
        tk.Label(self.root, text="Controle de Estoque", font=("Helvetica", 14, "bold")).pack(pady=10)
        tree = ttk.Treeview(self.root, columns=("codigo", "nome", "custo", "venda", "estoque", "unidade"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")

        try:
            self.cursor.execute("SELECT * FROM produtos")
            for row in self.cursor.fetchall():
                tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao buscar produtos: {err}")

        tree.pack(expand=True, fill="both")
        tk.Button(self.root, text="Voltar", command=self.menu_principal).pack(pady=10)

    def ponto_de_venda(self):
        self.limpar_janela()
        self.carrinho = []
        self.total_venda = 0.00

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Ponto de Venda", font=("Helvetica", 14, "bold")).pack(pady=5)

        tk.Label(frame, text="Código do Produto:").pack()
        self.entry_codigo = tk.Entry(frame)
        self.entry_codigo.pack()

        tk.Label(frame, text="Quantidade:").pack()
        self.entry_qtd = tk.Entry(frame)
        self.entry_qtd.pack()

        tk.Button(frame, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho).pack(pady=5)

        self.label_total = tk.Label(frame, text="Total: R$ 0.00", font=("Helvetica", 12, "bold"))
        self.label_total.pack(pady=5)

        self.tree_carrinho = ttk.Treeview(self.root, columns=("codigo", "nome", "qtd", "total"), show="headings")
        for col in self.tree_carrinho["columns"]:
            self.tree_carrinho.heading(col, text=col.capitalize())
            self.tree_carrinho.column(col, anchor="center")
        self.tree_carrinho.pack(expand=True, fill="both")

        tk.Button(self.root, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=10)
        tk.Button(self.root, text="Voltar ao Menu", command=self.menu_principal).pack(pady=5)
        
    def adicionar_ao_carrinho(self):
        codigo = self.entry_codigo.get()
        try:
            qtd = int(self.entry_qtd.get())
            if qtd <= 0:
                messagebox.showerror("Erro", "Quantidade inválida.")
                return

            self.cursor.execute("SELECT nome, preco_venda, estoque FROM produtos WHERE codigo = %s", (codigo,))
            result = self.cursor.fetchone()

            if not result:
                messagebox.showerror("Erro", "Código inválido.")
                return

            nome, preco_venda, estoque = result
            
            if qtd > estoque:
                messagebox.showerror("Erro", "Estoque insuficiente.")
                return
               
            total_item = preco_venda * qtd
            
            self.total_venda += float(total_item) # erro aqui
            
            self.carrinho.append({"codigo": codigo, "quantidade": qtd, "preco_unitario": preco_venda})

            self.tree_carrinho.insert("", tk.END, values=(codigo, nome, qtd, f"R$ {total_item:.2f}"))

            self.label_total.config(text=f"Total: R$ {self.total_venda:.2f}")

            self.entry_codigo.delete(0, tk.END)
            self.entry_qtd.delete(0, tk.END)

        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao adicionar ao carrinho: {err}")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showerror("Erro", "Carrinho vazio.")
            return

        pagamento_window = tk.Toplevel(self.root)
        pagamento_window.title("Finalizar Pagamento")
        pagamento_window.geometry("400x400")

        tk.Label(pagamento_window, text=f"Total da Compra: R$ {self.total_venda:.2f}", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(pagamento_window, text="Forma de Pagamento:").pack()
        formas = ["À Vista", "Cartão de Débito", "Cartão de Crédito", "PIX"]
        forma_pagamento = Combobox(pagamento_window, values=formas)
        forma_pagamento.pack()

        entry_valor_pago = tk.Entry(pagamento_window)
        parcelas_combo = Combobox(pagamento_window)

        def atualizar_pagamento(event=None):
            if forma_pagamento.get() == "À Vista":
                tk.Label(pagamento_window, text="Valor Pago (Cliente):").pack()
                entry_valor_pago.pack()
            elif forma_pagamento.get() == "Cartão de Crédito" and self.total_venda >= 150:
                tk.Label(pagamento_window, text="Parcelar em:").pack()
                parcelas_combo['values'] = ["1x", "2x", "3x"]
                parcelas_combo.pack()

        forma_pagamento.bind("<<ComboboxSelected>>", atualizar_pagamento)

        def confirmar_pagamento():
            forma = forma_pagamento.get()
            if forma == "":
                messagebox.showerror("Erro", "Selecione uma forma de pagamento.")
                return

            try:
                if forma == "À Vista":
                    valor_pago = float(entry_valor_pago.get())
                    if valor_pago < self.total_venda:
                        messagebox.showerror("Erro", "Valor pago insuficiente.")
                        return
                    troco = valor_pago - self.total_venda
                    messagebox.showinfo("Sucesso", f"Compra finalizada. Troco: R$ {troco:.2f}")

                elif forma == "Cartão de Crédito" and self.total_venda >= 150 and parcelas_combo.get() != "":
                    qtd_parcelas = int(parcelas_combo.get()[0])  # Pega o número de parcelas
                    valor_parcela = self.total_venda / qtd_parcelas
                    messagebox.showinfo("Parcelamento", f"Pagamento em {qtd_parcelas}x de R$ {valor_parcela:.2f} no Cartão.")
                else:
                    messagebox.showinfo("Sucesso", "Compra finalizada.")

                # Inserir a venda no banco de dados
                now = datetime.datetime.now()
                self.cursor.execute("INSERT INTO vendas (data, total, forma_pagamento) VALUES (%s, %s, %s)",
                                    (now, self.total_venda, forma))
                venda_id = self.cursor.lastrowid  # Obtém o ID da venda inserida

                # Inserir os itens da venda
                for item in self.carrinho:
                    self.cursor.execute("""
                        INSERT INTO itens_venda (venda_id, produto_codigo, quantidade, preco_unitario)
                        VALUES (%s, %s, %s, %s)
                    """, (venda_id, item['codigo'], item['quantidade'], item['preco_unitario']))

                self.db_connection.commit()

                self.carrinho = []
                self.total_venda = 0.0
                pagamento_window.destroy()
                self.menu_principal()

            except ValueError:
                messagebox.showerror("Erro", "Dados de pagamento inválidos.")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao finalizar compra: {err}")

        tk.Button(pagamento_window, text="Confirmar Pagamento", command=confirmar_pagamento).pack(pady=20)

    def historico(self):
        if self.usuario_logado not in ["admin", "gerente"]:
            messagebox.showerror("Erro", "Acesso negado.")
            return
        self.limpar_janela()
        tk.Label(self.root, text="Histórico de Vendas", font=("Helvetica", 14, "bold")).pack()
        tree = ttk.Treeview(self.root, columns=("id", "data", "total", "forma_pagamento"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")

        try:
            self.cursor.execute("SELECT id, data, total, forma_pagamento FROM vendas")
            for row in self.cursor.fetchall():
                tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao buscar histórico: {err}")

        tree.pack(expand=True, fill="both")
        tk.Button(self.root, text="Voltar", command=self.menu_principal).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = MinimercadoApp(root)
    root.mainloop()
