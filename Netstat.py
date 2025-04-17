from flask import Flask, render_template, jsonify
import subprocess
import shutil
import logging

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/netstat', methods=['GET'])
def get_netstat():
    """
    Rota para executar o comando 'netstat' e retornar a saída como JSON.
    """
    try:
        # Verifica se o comando netstat está disponível no sistema
        if not shutil.which('netstat'):
            logging.error("O comando 'netstat' não está disponível no sistema.")
            return jsonify({"error": "O comando 'netstat' não está disponível no sistema."}), 500

        # Executa o comando netstat e captura a saída
        logging.info("Executando o comando 'netstat'")
        result = subprocess.check_output(['netstat', '-a'], text=True, stderr=subprocess.STDOUT)
        netstat_output = result.splitlines()

        # Limita a saída a 100 linhas para evitar sobrecarga
        max_lines = 100
        if len(netstat_output) > max_lines:
            netstat_output = netstat_output[:max_lines]
            netstat_output.append(f"... (Exibindo as primeiras {max_lines} linhas)")

        logging.info("Comando 'netstat' executado com sucesso")
        return jsonify({"netstat_output": netstat_output})
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar o comando netstat: {e.output}")
        return jsonify({"error": f"Erro ao executar o comando netstat: {e.output}"}), 500
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@app.route('/netstat/<ip>', methods=['GET'])
def get_netstat_by_ip(ip):
    """
    Rota para executar o comando 'netstat' e filtrar a saída por um IP específico.
    """
    try:
        # Verifica se o comando netstat está disponível no sistema
        if not shutil.which('netstat'):
            logging.error("O comando 'netstat' não está disponível no sistema.")
            return jsonify({"error": "O comando 'netstat' não está disponível no sistema."}), 500

        # Executa o comando netstat e captura a saída
        logging.info(f"Executando o comando 'netstat' para o IP: {ip}")
        result = subprocess.check_output(['netstat', '-a'], text=True, stderr=subprocess.STDOUT)
        netstat_output = result.splitlines()

        # Filtra as linhas que contêm o IP fornecido
        filtered_output = [line for line in netstat_output if ip in line]

        if not filtered_output:
            logging.info(f"Nenhuma entrada encontrada para o IP: {ip}")
            return jsonify({"message": f"Nenhuma entrada encontrada para o IP: {ip}"}), 404

        logging.info(f"Comando 'netstat' executado com sucesso para o IP: {ip}")
        return jsonify({"netstat_output": filtered_output})
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar o comando netstat: {e.output}")
        return jsonify({"error": f"Erro ao executar o comando netstat: {e.output}"}), 500
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@app.route('/')
def index():
    """
    Rota para renderizar a página inicial.
    """
    logging.info("Renderizando a página inicial")
    return render_template('index.html')

if __name__ == '__main__':
    """
    Executa o servidor Flask.
    """
    # Use debug=True apenas em desenvolvimento
    app.run(host='0.0.0.0', port=5000, debug=False)