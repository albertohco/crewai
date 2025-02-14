from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv
from repo_crewai.main_crew import run_crew

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def call_groq(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.2-3b-preview",
    )
    return chat_completion.choices[0].message.content


def classificar_prioridade(result):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f'Responda apenas com a cor que classifique o paciente: Vermelho, Amarelo e Verde para o seguinte resultado de triagem: {result}'
            }
        ],
        model="llama-3.2-3b-preview",
    )
    return chat_completion.choices[0].message.content
    # # Simplificação para exemplo, ajuste conforme a lógica de risco
    # if "morte iminente" in result or "ressuscitação" in result:
    #     return "Vermelho"
    # elif "urgência" in result or "alto risco" in result:
    #     return "Amarelo"
    # else:
    #     return "Verde"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/triagem', methods=['POST'])
def triagem():
    # Recebe os dados do formulário
    nome = request.form.get("nome")
    idade = request.form.get("idade")
    sintomas = request.form.get("sintomas")

    # Contexto para o modelo Groq
    patient_context = run_crew(nome, idade, sintomas)
    # print(patient_context.raw)

    # Chama o modelo para processar a triagem
    # result = call_groq(patient_context)

    # Classifica a prioridade do paciente
    prioridade = classificar_prioridade(patient_context.raw)

    # Retorna o resultado e a prioridade em formato JSON
    return jsonify({"result": patient_context.raw, "prioridade": prioridade})


if __name__ == '__main__':
    app.run(port=5000)
