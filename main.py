import hashlib
import datetime as date
import pickle
import os
import random

print('► Login...')
print()
business_name = str(input('• Nome da empresa: '))
business_sector = str(input('• Setor de atuacao: '))

class Block:
    def __init__(self, index, timestamp, data, previous_hash, validator):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.validator = validator

    def __repr__(self):
        return f'''
◼ BLOCO | {self.index}
  TIMESTAMP | {self.timestamp}
  DADOS | {self.data}
  VALIDADOR | {self.validator}
  HASH PASSADO | {self.previous_hash}
  HASH ATUAL | {self.calculate_hash()}
{100 * '—'}'''

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8'))
        sha.update(str(self.timestamp).encode('utf-8'))
        sha.update(str(self.data).encode('utf-8'))
        sha.update(str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()


class Validator:
    def __init__(self, name, stake):
        self.name = name
        self.stake = stake
        self.is_registered = True


class GovernmentDataCenter(Validator):
    def __init__(self):
        super().__init__(name = "Governo", stake = 3)


def initialize_validators(main_company_name):
    validators = [
        Validator(name="Empresa_1", stake = 1),
        Validator(name="Empresa_2", stake = 1),
        Validator(name="Empresa_3", stake = 1),
        GovernmentDataCenter()
    ]

    main_company = Validator(name = main_company_name, stake = 5)
    validators.append(main_company)

    return validators, main_company


class Blockchain:
    def __init__(self, validators, main_company, transaction_type):
        self.transaction_type = transaction_type
        self.chain = self.load_chain() or [self.create_genesis_block()]
        self.validators = validators
        self.main_company = main_company

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), 'Genesis Block', '0', "Genesis")

    def load_chain(self):
        filename = f'./{self.transaction_type}.bin'
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        return None

    def save_chain(self):
        filename = f'./{self.transaction_type}.bin'
        with open(filename, 'wb') as file:
            pickle.dump(self.chain, file)

    def select_validator(self):
        total_stake = sum(validator.stake for validator in self.validators)
        
        if total_stake == 0:
            return None
        weights = [validator.stake / total_stake for validator in self.validators]
        selected_validator = random.choices(self.validators, weights = weights, k = 1)[0]
        return selected_validator

    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        self.save_chain()
        print()
        print(f"► Bloco [{new_block.index}] decifrado por: {new_block.validator}.")

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def debug_chain(self):
        print(100 * '—')
        for block in self.chain:
            print(f"◼ BLOCO | {block.index}")
            print(f"  TIMESTAMP | {block.timestamp}")
            print(f"  DADOS | {block.data}")
            print(f"  VALIDADOR | {block.validator}")
            print(f"  HASH PASSADO | {block.previous_hash}")
            print(f"  HASH ATUAL | {block.calculate_hash()}")
            if block.calculate_hash() != block.hash:
                print("  ! Hash inválido.")
            print(100 * '—')


def execute_transaction(transaction_type):
    main_company_name = business_name
    validators, main_company = initialize_validators(main_company_name)
    blockchain = Blockchain(validators, main_company, transaction_type)

    if os.path.exists('balance.bin'):
        with open('balance.bin', 'rb') as file:
            info = pickle.load(file)
    else:
        info = {'Creditos de carbono (CO2)': 1000, 'Dolares ($)': 1000000, 'Stake': 1, 'Certificacoes': []}
        with open('balance.bin', 'wb') as file:
            pickle.dump(info, file)

    while True:
        print()
        print(100 * '—')
        location = input('''
[1] EU ETS (European Union Emissions Trading System)
[2] US ETS (California Cap-and-Trade Program)
[3] CN ETS (Chinese national carbon trading scheme)
[0] Sair

• Escolha um bloco economico: ''')
        if location == '0':
            print()
            print("► Operacao cancelada.")
            return
        if location in ['1', '2', '3']:
            break
        print("! Escolha invalida. Tente novamente.")

    while True:
        try:
            if transaction_type == 'get_certifications':
                carbon_credits = 0
                break
            else:
                carbon_credits = input('• Quantidade de creditos de carbono ([0] Sair): ')
                if carbon_credits == '0':
                    print("► Operacao cancelada.")
                    return
                carbon_credits = int(carbon_credits)
                if carbon_credits <= 0:
                    raise ValueError("A quantidade de creditos de carbono deve ser positiva.")
                elif carbon_credits > info['Creditos de carbono (CO2)']:
                    raise ValueError("Saldo insuficiente.")
                break
        except ValueError as e:
            print(f"! Erro. {e}")
    
    if location == '1':
        economic_block = 'EU ETS'
        price = carbon_credits * 90
        government_price = carbon_credits * 45
    elif location == '2':
        economic_block = 'US ETS'
        price = carbon_credits * 30
        government_price = carbon_credits * 15
    else:
        economic_block = 'CN ETS'
        price = carbon_credits * 10
        government_price = carbon_credits * 5


    if transaction_type == 'buy_carbon_credits':
        seller = input('• Vendedor ([0] Sair): ')
        if seller == '0':
            print("► Operacao cancelada.")
            return

        if info['Dolares ($)'] >= price:
            info['Creditos de carbono (CO2)'] += carbon_credits
            info['Dolares ($)'] -= price

            data = {
                'Tipo de transacao': transaction_type,
                'Bloco economico': economic_block,
                'Comprador': business_name,
                'Vendedor': seller,
                'Creditos de carbono (CO2)': carbon_credits,
                'Dolares ($)': price,
            }

            new_block = Block(len(blockchain.chain), date.datetime.now(), data, blockchain.chain[-1].hash, None)
            selected_validator = blockchain.select_validator()
        else:
            print("! Saldo insuficiente.")


    elif transaction_type == 'sell_carbon_credits':
        seller = input('• Comprador ([0] Sair): ')
        if seller == '0':
            print("► Operacao cancelada.")
            return

        if info['Creditos de carbono (CO2)'] >= carbon_credits:
            info['Creditos de carbono (CO2)'] -= carbon_credits
            info['Dolares ($)'] += price

            data = {
                'Tipo de transacao': transaction_type,
                'Bloco economico': economic_block,
                'Comprador': seller,
                'Vendedor': business_name,
                'Creditos de carbono (CO2)': carbon_credits,
                'Dolares ($)': price,
            }

            new_block = Block(len(blockchain.chain), date.datetime.now(), data, blockchain.chain[-1].hash, None)
            selected_validator = blockchain.select_validator()
        else:
            print("! Saldo insuficiente.")
    

    elif transaction_type == 'exchange_carbon_credits':
        if info['Creditos de carbono (CO2)'] >= carbon_credits:
            info['Creditos de carbono (CO2)'] -= carbon_credits
            info['Dolares ($)'] += government_price

            data = {
                'Tipo de transacao': transaction_type,
                'Bloco economico': economic_block,
                'Comprador': 'Governo',
                'Vendedor': business_name,
                'Creditos de carbono (CO2)': carbon_credits,
                'Dolares ($)': government_price,
            }

            new_block = Block(len(blockchain.chain), date.datetime.now(), data, blockchain.chain[-1].hash, None)
            selected_validator = blockchain.select_validator()
        else:
            print("! Saldo insuficiente.")
    
    
    elif transaction_type == 'get_certifications':
        if info['Creditos de carbono (CO2)'] < 1000:
            print("! Saldo insuficiente. E necessario possuir no minimo 1000 creditos de carbono para obter uma certificacao.")
            return
        else:
            while True:
                print()
                print(100 * '—')
                select_certification = input('''
[1] CDP (Carbon Disclosure Project) | $50.000,00
[2] DJSI (Dow Jones Sustainability Index) | $50.000,00
[3] EMAS (Eco-Management and Audit Scheme) | $40.000,00
[4] Gold Standard | $60.000,00
[5] GRI (Global Reporting Initiative) | $45.000,00
[6] IAEA (International Atomic Energy Agency) | $55.000,00
[7] ISO 14001 (Environmental Management System) | $35.000,00
[8] ISO 50001 (Energy Management System) | $35.000,00
[9] SBTI (Science Based Targets Initiative) | $50.000,00
[0] Sair

• Escolha uma certificacao: ''')
                if select_certification == '0':
                    print("► Operacao cancelada.")
                    return

                certification_values = {
                    '1': ('CDP', f'SGS ({economic_block})', 50000),
                    '2': ('DJSI', f'DNV GL ({economic_block})', 50000),
                    '3': ('EMAS', f'Deloitte ({economic_block})', 40000),
                    '4': ('Gold Standard', f'SGS ({economic_block})', 60000),
                    '5': ('GRI', f'DNV GL ({economic_block})', 45000),
                    '6': ('IAEA', f'SGS ({economic_block})', 55000),
                    '7': ('ISO 14001', f'Deloitte ({economic_block})', 35000),
                    '8': ('ISO 50001', f'SGS ({economic_block})', 35000),
                    '9': ('SBTI', f'DNV GL ({economic_block})', 50000)
                }

                if select_certification in certification_values:
                    certification, auditory, price = certification_values[select_certification]
                    for i in info['Certificacoes']:
                        if i == {certification: auditory}:
                            print("! Certificacao ja obtida.")
                            print()
                            print(100 * '—')
                            return
                    else:
                        if info['Dolares ($)'] < price:
                            print("! Saldo insuficiente.")
                        else:
                            info['Dolares ($)'] -= price
                            info['Certificacoes'].append({certification: auditory})

                            data = {
                                'Tipo de transacao': transaction_type,
                                'Certificacao': certification,
                                'Auditoria': auditory,
                                'Empresa': business_name,
                                'Dolares ($)': price,
                            }

                            break
                else:
                    print("! Escolha invalida. Tente novamente.")


    new_block = Block(len(blockchain.chain), date.datetime.now(), data, blockchain.chain[-1].hash, None)
    selected_validator = blockchain.select_validator()

    if selected_validator:
        new_block.validator = selected_validator.name
        new_block.hash = new_block.calculate_hash()
        blockchain.add_block(new_block)

    if selected_validator.name == main_company.name:
        main_company.stake += 1
        info['Stake'] += 1
        print(f"► {main_company.name} ganhou 1 Stake.")
    else:
        selected_validator.stake += 1
        print(f"► {selected_validator.name} ganhou 1 Stake.")

    with open('balance.bin', 'wb') as file:
        pickle.dump(info, file)

    if blockchain.is_valid():
        print(f"► Transacao registrada na blockchain.")
        print()
        blockchain.debug_chain()
    else:
        print("! Blockchain invalida!")


def main():
    while True:
        print(f'''
Econy 🍃 | {business_name} ({business_sector})

[1] Saldo
[2] Comprar creditos de carbono
[3] Vender creditos de carbono 
[4] Cambiar creditos de carbono 
[5] Obter certificacao
[6] Consultar blockchain
[7] Sobre a plataforma
[0] Sair
''')
        choice = input("• Escolha uma opcao: ")

        if choice == '1':
            try:
                with open('balance.bin', 'rb') as file:
                    info = pickle.load(file)
                    print()
                    print(100 * '—')
                    print()
                    for i in info:
                        print(f'{i.upper()} | {info[i]}')
                    print()
                    print(100 * '—')
            except FileNotFoundError:
                print()
                print(100 * '—')
                print()
                print('! Arquivo de saldo nao encontrado. Deve-se realizar uma compra/venda/cambiacao de creditos de carbono, ou obter uma certificacao para cria-lo.')
                print()
                print(100 * '—')
        elif choice == '2':
            execute_transaction('buy_carbon_credits')
        elif choice == '3':
            execute_transaction('sell_carbon_credits') 
        elif choice == '4':
            execute_transaction('exchange_carbon_credits') 
        elif choice == '5':
            execute_transaction('get_certifications')
        elif choice == '6':
            while True:
                print()
                print(100 * '—')
                blockchain_name = str(input('''
[1] Compras de creditos de carbono
[2] Vendas de creditos de carbono
[3] Cambios de creditos de carbono
[4] Obtencoes de certificacoes
[0] Sair

• Escolha uma blockchain: '''))
                if blockchain_name == '0':
                    print("► Operacao cancelada.")
                    break
                if blockchain_name == '1':
                    if not os.path.exists('buy_carbon_credits.bin'):
                        print("! Blockchain nao criada.")
                    else:
                        with open('buy_carbon_credits.bin', 'rb') as file:
                            print()
                            print(100 * '—')
                            print(pickle.load(file))
                            break
                elif blockchain_name == '2':
                    if not os.path.exists('sell_carbon_credits.bin'):
                        print("! Blockchain nao criada.")
                    else:
                        with open('sell_carbon_credits.bin', 'rb') as file:
                            print()
                            print(100 * '—')
                            print(pickle.load(file))
                            break
                elif blockchain_name == '3':
                    if not os.path.exists('exchange_carbon_credits.bin'):
                        print("! Blockchain nao criada.")
                    else:
                        with open('exchange_carbon_credits.bin', 'rb') as file:
                            print()
                            print(100 * '—')
                            print(pickle.load(file))
                            break
                elif blockchain_name == '4':
                    if not os.path.exists('get_certifications.bin'):
                        print("! Blockchain nao criada.")
                    else:
                        with open('get_certifications.bin', 'rb') as file:
                            print()
                            print(100 * '—')
                            print(pickle.load(file))
                            break
                else:
                    print("! Blockchain invalida.")
        elif choice == '7':
            print()
            print(100 * '—')
            print('''
A Econy e uma plataforma inovadora que promove a sustentabilidade e a responsabilidade ambiental empresarial, conectando empresas a um ecossistema global eficiente e transparente.

Prezando pelo mercado internacional de creditos de carbono, a Econy utiliza tecnologia blockchain e smart contracts (contratos inteligentes) para garantir seguranca, descentralizacao e rastreabilidade nas transacoes. A plataforma permite a compra e venda de creditos de carbono de maneira segura e imutavel, alem de facilitar a formalizacao de contratos rastreaveis, assegurando confianca entre acordos.

A plataforma tambem oferece certificacoes de sustentabilidade emitidas por auditorias independentes e disponibiliza um servico exclusivo de integracao de inventario de GEE (gases de efeito estufa), permitindo as empresas monitorar e gerenciar suas emissoes. Combinando tecnologias emergentes e praticas sustentaveis, a Econy se posiciona como um facilitador estrategico para empresas que buscam reduzir seu impacto ambiental e promover uma economia verde.
''')
            print(100 * '—')
        elif choice == '0':
            print()
            print(100 * '—')
            print()
            print("► Encerrando...")
            break
        else:
            print("! Escolha invalida. Tente novamente.")
            print()
            print(100 * '—')

if __name__ == "__main__":
    main()
