import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Conexão com o banco
def conectar():
    return sqlite3.connect('teste.db')

# Criar tabela
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            endereco TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inserir usuário
def inserir_usuario():
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    endereco = entry_endereco.get().strip()
    telefone = entry_telefone.get().strip()
    if nome and email and endereco and telefone:
        if not telefone.isdigit():
            messagebox.showerror('Erro', 'Telefone deve conter apenas números.')
            return
        conn = conectar()
        c = conn.cursor()
        c.execute(
            'INSERT INTO usuarios (nome, email, endereco, telefone) VALUES (?, ?, ?, ?)',
            (nome, email, endereco, telefone)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Usuário inserido com sucesso.')
        mostrar_usuarios()
        limpar_campos()
    else:
        messagebox.showerror('Erro', 'Preencha todos os campos.')
    entry_nome.focus()

# Mostrar usuários na treeview
def mostrar_usuarios():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    for user in c.fetchall():
        tree.insert("", "end", values=user)
    conn.close()

# Deletar usuário
def delete_usuario():
    sel = tree.selection()
    if not sel:
        messagebox.showerror('Erro', 'Selecione um usuário para deletar.')
        return
    user_id = tree.item(sel)['values'][0]
    conn = conectar()
    c = conn.cursor()
    c.execute('DELETE FROM usuarios WHERE id=?', (user_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo('Sucesso', 'Usuário deletado com sucesso.')
    mostrar_usuarios()
    entry_nome.focus()

# Editar usuário
def editar_usuario():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning('Aviso', 'Selecione um usuário para editar.')
        return
    user_id = tree.item(sel)['values'][0]
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    endereco = entry_endereco.get().strip()
    telefone = entry_telefone.get().strip()
    if not (nome and email and endereco and telefone):
        messagebox.showerror('Erro', 'Preencha todos os campos para editar.')
        return
    if not telefone.isdigit():
        messagebox.showerror('Erro', 'Telefone deve conter apenas números.')
        return
    conn = conectar()
    c = conn.cursor()
    c.execute(
        '''UPDATE usuarios 
           SET nome=?, email=?, endereco=?, telefone=? 
           WHERE id=?''',
        (nome, email, endereco, telefone, user_id)
    )
    conn.commit()
    conn.close()
    messagebox.showinfo('Sucesso', 'Usuário atualizado com sucesso.')
    mostrar_usuarios()
    limpar_campos()
    entry_nome.focus()

# Limpar campos e seleção da treeview
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    for sel in tree.selection():
        tree.selection_remove(sel)

# Interface gráfica
janela = tk.Tk()
janela.title('CRUD com SQLite - Endereço e Telefone')
janela.geometry('700x600')
janela.configure(bg='lightgray')

tk.Label(
    janela,
    text='Sistema de Cadastro',
    font=('Roboto', 20, 'bold'),
    fg='blue',
    bg='lightgray'
).pack(pady=10)

frame_form = tk.Frame(janela, bg='lightgray')
frame_form.pack(pady=10)

# Campos
labels = ['Nome:', 'Email:', 'Endereço:', 'Telefone:']
entries = []
for i, text in enumerate(labels):
    tk.Label(frame_form, text=text, bg='lightgray',font=('arial',15)).grid(row=i, column=0, padx=5, pady=5, sticky='e')
    entry = tk.Entry(frame_form, width=40,font=('arial',15))
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

entry_nome, entry_email, entry_endereco, entry_telefone = entries

frame_botoes = tk.Frame(janela, bg='lightgray')
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text='Inserir', command=inserir_usuario, width=12).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text='Editar', command=editar_usuario, width=12).grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text='Excluir', command=delete_usuario, width=12).grid(row=0, column=2, padx=5)

# Treeview
tree = ttk.Treeview(
    janela,
    columns=('ID', 'Nome', 'Email', 'Endereço', 'Telefone'),
    show='headings'
)
for col in ('ID', 'Nome', 'Email', 'Endereço', 'Telefone'):
    tree.heading(col, text=col)
tree.pack(pady=20, fill='both', expand=True)

# Inicialização
criar_tabela()
mostrar_usuarios()
entry_nome.focus()
janela.mainloop()

