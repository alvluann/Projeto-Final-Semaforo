import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from logica import criar_trafego, criar_trafego_personalizado, simular_transito, salvar_relatorio, mostrar_relatorios
from banco import conectar_banco, criar_tabela_relatorios
import matplotlib.pyplot as plt
from veiculos import Carro, Caminhao

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.conexao = conectar_banco()
        criar_tabela_relatorios(self.conexao)
        
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Frame para os botões à esquerda
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.grid(row=0, column=0, rowspan=15, sticky='nsw', padx=10, pady=10)

        # Botão para mostrar histórico de dados
        btn_historico = tk.Button(left_frame, text="Histórico", command=self.mostrar_historico, font=('Helvetica', 12, 'bold'), bg="#2196F3", fg="white")
        btn_historico.pack(fill=tk.X, pady=5)

        # Botão para mostrar gráficos de dados
        btn_graficos = tk.Button(left_frame, text="Gráficos", command=self.mostrar_graficos, font=('Helvetica', 12, 'bold'), bg="#FF5722", fg="white")
        btn_graficos.pack(fill=tk.X, pady=5)
        
        # Frame para os inputs
        self.inputs_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.inputs_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # Escolha do tipo de trânsito
        label_tipo = tk.Label(self.inputs_frame, text="Escolha como deseja trabalhar o trânsito:", font=('Helvetica', 14, 'bold'), bg="#f0f0f0")
        label_tipo.grid(row=0, column=0, columnspan=2, pady=10)

        self.tipo_var = tk.IntVar()
        radio_aleatorio = tk.Radiobutton(self.inputs_frame, text="Aleatório", variable=self.tipo_var, value=1, font=('Helvetica', 12), bg="#f0f0f0", command=self.toggle_inputs)
        radio_aleatorio.grid(row=1, column=0, sticky='w')
        radio_personalizado = tk.Radiobutton(self.inputs_frame, text="Personalizado", variable=self.tipo_var, value=2, font=('Helvetica', 12), bg="#f0f0f0", command=self.toggle_inputs)
        radio_personalizado.grid(row=1, column=1, sticky='w')
        radio_relatorio = tk.Radiobutton(self.inputs_frame, text="Mostrar Relatório", variable=self.tipo_var, value=3, font=('Helvetica', 12), bg="#f0f0f0", command=self.toggle_inputs)
        radio_relatorio.grid(row=1, column=2, sticky='w')

        # Inputs para tráfego aleatório
        self.label_quantidade_veiculos = tk.Label(self.inputs_frame, text="Quantidade total de veículos:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_quantidade_veiculos.grid(row=2, column=0, sticky='e', pady=5, padx=5)
        self.entry_quantidade_veiculos = tk.Entry(self.inputs_frame, font=('Helvetica', 12))
        self.entry_quantidade_veiculos.grid(row=2, column=1, pady=5, padx=5)

        # Inputs para tráfego personalizado
        self.create_personalizado_inputs(self.inputs_frame)

        # Inputs para o semáforo
        self.create_semaforo_inputs(self.inputs_frame)

        # Botão para iniciar a simulação
        btn_iniciar = tk.Button(self.inputs_frame, text="Iniciar Simulação", command=self.iniciar_simulacao, font=('Helvetica', 12, 'bold'), bg="#4CAF50", fg="white")
        btn_iniciar.grid(row=13, column=0, columnspan=2, pady=20)

    def create_personalizado_inputs(self, frame):
        self.label_carros_pequenos = tk.Label(frame, text="Quantidade de carros pequenos:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_carros_pequenos.grid(row=3, column=0, sticky='e', pady=5, padx=5)
        self.entry_carros_pequenos = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_carros_pequenos.grid(row=3, column=1, pady=5, padx=5)

        self.label_carros_medios = tk.Label(frame, text="Quantidade de carros médios:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_carros_medios.grid(row=4, column=0, sticky='e', pady=5, padx=5)
        self.entry_carros_medios = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_carros_medios.grid(row=4, column=1, pady=5, padx=5)

        self.label_carros_grandes = tk.Label(frame, text="Quantidade de carros grandes:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_carros_grandes.grid(row=5, column=0, sticky='e', pady=5, padx=5)
        self.entry_carros_grandes = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_carros_grandes.grid(row=5, column=1, pady=5, padx=5)

        self.label_camioes_pequenos = tk.Label(frame, text="Quantidade de caminhões pequenos:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_camioes_pequenos.grid(row=6, column=0, sticky='e', pady=5, padx=5)
        self.entry_camioes_pequenos = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_camioes_pequenos.grid(row=6, column=1, pady=5, padx=5)

        self.label_camioes_medios = tk.Label(frame, text="Quantidade de caminhões médios:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_camioes_medios.grid(row=7, column=0, sticky='e', pady=5, padx=5)
        self.entry_camioes_medios = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_camioes_medios.grid(row=7, column=1, pady=5, padx=5)

        self.label_camioes_grandes = tk.Label(frame, text="Quantidade de caminhões grandes:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_camioes_grandes.grid(row=8, column=0, sticky='e', pady=5, padx=5)
        self.entry_camioes_grandes = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_camioes_grandes.grid(row=8, column=1, pady=5, padx=5)

    def create_semaforo_inputs(self, frame):
        self.label_duracao_verde = tk.Label(frame, text="Duração do sinal verde:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_duracao_verde.grid(row=9, column=0, sticky='e', pady=5, padx=5)
        self.entry_duracao_verde = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_duracao_verde.grid(row=9, column=1, pady=5, padx=5)

        self.label_duracao_amarelo = tk.Label(frame, text="Duração do sinal amarelo:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_duracao_amarelo.grid(row=10, column=0, sticky='e', pady=5, padx=5)
        self.entry_duracao_amarelo = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_duracao_amarelo.grid(row=10, column=1, pady=5, padx=5)

        self.label_duracao_vermelho = tk.Label(frame, text="Duração do sinal vermelho:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_duracao_vermelho.grid(row=11, column=0, sticky='e', pady=5, padx=5)
        self.entry_duracao_vermelho = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_duracao_vermelho.grid(row=11, column=1, pady=5, padx=5)

        self.label_distancia_semaforo = tk.Label(frame, text="Distância do semáforo:", font=('Helvetica', 12), bg="#f0f0f0")
        self.label_distancia_semaforo.grid(row=12, column=0, sticky='e', pady=5, padx=5)
        self.entry_distancia_semaforo = tk.Entry(frame, font=('Helvetica', 12))
        self.entry_distancia_semaforo.grid(row=12, column=1, pady=5, padx=5)

    def toggle_inputs(self):
        escolha = self.tipo_var.get()
        if escolha == 1:  # Aleatório
            self.label_quantidade_veiculos.grid()
            self.entry_quantidade_veiculos.grid()

            self.label_carros_pequenos.grid_remove()
            self.entry_carros_pequenos.grid_remove()
            self.label_carros_medios.grid_remove()
            self.entry_carros_medios.grid_remove()
            self.label_carros_grandes.grid_remove()
            self.entry_carros_grandes.grid_remove()
            self.label_camioes_pequenos.grid_remove()
            self.entry_camioes_pequenos.grid_remove()
            self.label_camioes_medios.grid_remove()
            self.entry_camioes_medios.grid_remove()
            self.label_camioes_grandes.grid_remove()
            self.entry_camioes_grandes.grid_remove()

            self.label_duracao_verde.grid()
            self.entry_duracao_verde.grid()
            self.label_duracao_amarelo.grid()
            self.entry_duracao_amarelo.grid()
            self.label_duracao_vermelho.grid()
            self.entry_duracao_vermelho.grid()
            self.label_distancia_semaforo.grid()
            self.entry_distancia_semaforo.grid()
        elif escolha == 2:  # Personalizado
            self.label_quantidade_veiculos.grid_remove()
            self.entry_quantidade_veiculos.grid_remove()

            self.label_carros_pequenos.grid()
            self.entry_carros_pequenos.grid()
            self.label_carros_medios.grid()
            self.entry_carros_medios.grid()
            self.label_carros_grandes.grid()
            self.entry_carros_grandes.grid()
            self.label_camioes_pequenos.grid()
            self.entry_camioes_pequenos.grid()
            self.label_camioes_medios.grid()
            self.entry_camioes_medios.grid()
            self.label_camioes_grandes.grid()
            self.entry_camioes_grandes.grid()

            self.label_duracao_verde.grid()
            self.entry_duracao_verde.grid()
            self.label_duracao_amarelo.grid()
            self.entry_duracao_amarelo.grid()
            self.label_duracao_vermelho.grid()
            self.entry_duracao_vermelho.grid()
            self.label_distancia_semaforo.grid()
            self.entry_distancia_semaforo.grid()
        else:  # Relatório
            self.label_quantidade_veiculos.grid_remove()
            self.entry_quantidade_veiculos.grid_remove()

            self.label_carros_pequenos.grid_remove()
            self.entry_carros_pequenos.grid_remove()
            self.label_carros_medios.grid_remove()
            self.entry_carros_medios.grid_remove()
            self.label_carros_grandes.grid_remove()
            self.entry_carros_grandes.grid_remove()
            self.label_camioes_pequenos.grid_remove()
            self.entry_camioes_pequenos.grid_remove()
            self.label_camioes_medios.grid_remove()
            self.entry_camioes_medios.grid_remove()
            self.label_camioes_grandes.grid_remove()
            self.entry_camioes_grandes.grid_remove()

            self.label_duracao_verde.grid_remove()
            self.entry_duracao_verde.grid_remove()
            self.label_duracao_amarelo.grid_remove()
            self.entry_duracao_amarelo.grid_remove()
            self.label_duracao_vermelho.grid_remove()
            self.entry_duracao_vermelho.grid_remove()
            self.label_distancia_semaforo.grid_remove()
            self.entry_distancia_semaforo.grid_remove()

    def iniciar_simulacao(self):
        try:
            escolha = self.tipo_var.get()
            if escolha == 1:
                quantidade_veiculos = int(self.entry_quantidade_veiculos.get())
                fila_veiculos = criar_trafego(quantidade_veiculos)
                quant_carros_pequenos = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Carro) and veiculo.modelo == "pequeno")
                quant_carros_medios = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Carro) and veiculo.modelo == "medio")
                quant_carros_grandes = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Carro) and veiculo.modelo == "grande")
                quant_camioes_pequenos = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Caminhao) and veiculo.modelo == "pequeno")
                quant_camioes_medios = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Caminhao) and veiculo.modelo == "medio")
                quant_camioes_grandes = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Caminhao) and veiculo.modelo == "grande")
            elif escolha == 2:
                quant_carros_pequenos = int(self.entry_carros_pequenos.get())
                quant_carros_medios = int(self.entry_carros_medios.get())
                quant_carros_grandes = int(self.entry_carros_grandes.get())
                quant_camioes_pequenos = int(self.entry_camioes_pequenos.get())
                quant_camioes_medios = int(self.entry_camioes_medios.get())
                quant_camioes_grandes = int(self.entry_camioes_grandes.get())
                fila_veiculos = criar_trafego_personalizado(
                    quant_carros_pequenos, quant_carros_medios, quant_carros_grandes,
                    quant_camioes_pequenos, quant_camioes_medios, quant_camioes_grandes)
                quantidade_veiculos = len(fila_veiculos)
            elif escolha == 3:
                self.mostrar_historico()
                return
            else:
                messagebox.showerror("Erro", "Opção inválida!")
                return

            duracao_verde = int(self.entry_duracao_verde.get())
            duracao_amarelo = int(self.entry_duracao_amarelo.get())
            duracao_vermelho = int(self.entry_duracao_vermelho.get())
            distancia_semaforo = int(self.entry_distancia_semaforo.get())

            ciclos = simular_transito(fila_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo)
            messagebox.showinfo("Resultado", f"Número de ciclos completos: {ciclos}")

            salvar_relatorio(self.conexao, quantidade_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo,
                             ciclos, quant_carros_pequenos, quant_carros_medios, quant_carros_grandes,
                             quant_camioes_pequenos, quant_camioes_medios, quant_camioes_grandes)

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira todos os valores corretamente.")

    def mostrar_historico(self):
        historico_janela = Toplevel(self.root)
        historico_janela.title("Histórico de Dados")
        historico_janela.geometry("900x400")
        historico_janela.configure(bg="#f0f0f0")

        cols = ('ID', 'Duração Verde', 'Duração Amarelo', 'Duração Vermelho', 'Quantidade Veículos', 'Carros Pequenos',
                'Carros Médios', 'Carros Grandes', 'Caminhões Pequenos', 'Caminhões Médios', 'Caminhões Grandes', 
                'Distância Semáforo', 'Ciclos Completos')
        tree = ttk.Treeview(historico_janela, columns=cols, show='headings')

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)

        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM relatorios")
        relatorios = cursor.fetchall()

        for relatorio in relatorios:
            tree.insert("", "end", values=relatorio)

        tree.pack(expand=True, fill=tk.BOTH)

    def mostrar_graficos(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM relatorios")
        relatorios = cursor.fetchall()

        if not relatorios:
            messagebox.showinfo("Informação", "Não há dados para mostrar os gráficos.")
            return

        # Preparar dados para os gráficos
        ids = [relatorio[0] for relatorio in relatorios]
        duracao_verde = [relatorio[1] for relatorio in relatorios]
        duracao_amarelo = [relatorio[2] for relatorio in relatorios]
        duracao_vermelho = [relatorio[3] for relatorio in relatorios]
        quantidade_veiculos = [relatorio[4] for relatorio in relatorios]
        ciclos_completos = [relatorio[12] for relatorio in relatorios]

        # Plotar gráficos
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))

        axs[0, 0].plot(ids, duracao_verde, label='Duração Verde')
        axs[0, 0].set_title('Duração Verde')
        axs[0, 0].set_xlabel('ID')
        axs[0, 0].set_ylabel('Duração (s)')
        axs[0, 0].legend()

        axs[0, 1].plot(ids, duracao_amarelo, label='Duração Amarelo', color='orange')
        axs[0, 1].set_title('Duração Amarelo')
        axs[0, 1].set_xlabel('ID')
        axs[0, 1].set_ylabel('Duração (s)')
        axs[0, 1].legend()

        axs[1, 0].plot(ids, duracao_vermelho, label='Duração Vermelho', color='red')
        axs[1, 0].set_title('Duração Vermelho')
        axs[1, 0].set_xlabel('ID')
        axs[1, 0].set_ylabel('Duração (s)')
        axs[1, 0].legend()

        axs[1, 1].plot(ids, ciclos_completos, label='Ciclos Completos', color='green')
        axs[1, 1].set_title('Ciclos Completos')
        axs[1, 1].set_xlabel('ID')
        axs[1, 1].set_ylabel('Ciclos')
        axs[1, 1].legend()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
