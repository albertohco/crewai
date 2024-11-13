from crewai import Agent, Task, Crew, Process

# Dicionário de perguntas detalhadas conforme o protocolo NANDA
detailed_questions = {
    "dor": [
        "Pode descrever a dor? É uma dor aguda, crônica ou em queixa leve?",
        "Qual é a intensidade da dor em uma escala de 0 a 10?",
        "A dor piora em algum momento do dia ou em alguma situação específica?",
        "Você tomou alguma medicação para essa dor? Teve algum efeito?"
    ],
    "ansiedade": [
        "Com que frequência você se sente ansioso(a)?",
        "Existe alguma situação ou pensamento específico que desencadeia essa ansiedade?",
        "Já tentou alguma técnica para controlar a ansiedade, como respiração ou meditação?",
        "Essa ansiedade interfere nas suas atividades diárias? Como?"
    ],
    "sono": [
        "Como você descreveria a qualidade do seu sono ultimamente?",
        "Você costuma acordar durante a noite? Com que frequência?",
        "Acorda sentindo-se descansado(a) ou ainda cansado(a)?",
        "Mudou algo na sua rotina que pode ter afetado o seu sono?"
    ],
    "apetite": [
        "Teve alguma mudança recente no apetite? Está comendo mais ou menos do que o normal?",
        "Tem tido algum desconforto ao comer, como náusea ou dor no estômago?",
        "Notou alguma alteração no peso nos últimos meses?",
        "Teve alguma mudança nos tipos de alimentos que prefere ou evita?"
    ],
    "medicação": [
        "Quais medicamentos você está tomando atualmente?",
        "Há quanto tempo você toma esses medicamentos?",
        "Sente algum efeito colateral com esses medicamentos?",
        "Algum profissional de saúde recomendou essas medicações recentemente?"
    ]
}

# Perguntas padrão para todos os pacientes
standard_questions = [
    "Qual é o seu nome?",
    "Qual é a sua idade?",
    "Quais são os principais sintomas que você está sentindo?"
]

# Perguntas de sinais vitais
vital_signs_questions = [
    "Qual é a sua temperatura corporal em graus Celsius?",
    "Qual é a sua frequência cardíaca em batimentos por minuto?",
    "Qual é a sua frequência respiratória em respirações por minuto?",
    "Qual é a sua pressão arterial? (exemplo: 120/80 mmHg)"
]

# Função para selecionar a próxima pergunta baseada na resposta do paciente e no histórico


def analyze_response(response, response_history):
    for condition, questions in detailed_questions.items():
        if condition in response.lower():
            for question in questions:
                if question not in response_history:
                    return question
    return "Há algum outro sintoma ou condição que gostaria de mencionar?"

# Função para classificar prioridade com base nas respostas e sinais vitais


def classify_priority(response_history):
    high_priority_keywords = [
        "dor intensa", "dificuldade para respirar", "ansiedade extrema", "febre alta"]
    moderate_priority_keywords = ["dor moderada", "desconforto persistente"]

    for response in response_history:
        if any(keyword in response.lower() for keyword in high_priority_keywords):
            return "vermelho"
        elif any(keyword in response.lower() for keyword in moderate_priority_keywords):
            return "amarelo"

    return "verde"

# Função para gerar um relatório detalhado de anamnese


def generate_anamnesis_report(response_history):
    report = "Relatório de Anamnese do Paciente\n"
    report += "-" * 40 + "\n"

    # Dados básicos e sinais vitais
    report += f"Nome: {response_history[0]}\n"
    report += f"Idade: {response_history[1]}\n"
    report += f"Principais Sintomas: {response_history[2]}\n\n"
    report += "Sinais Vitais:\n"
    report += f"  - Temperatura: {response_history[3]} °C\n"
    report += f"  - Frequência Cardíaca: {response_history[4]} bpm\n"
    report += f"  - Frequência Respiratória: {response_history[5]} respirações/min\n"
    report += f"  - Pressão Arterial: {response_history[6]}\n\n"

    # Informações detalhadas
    report += "Avaliação dos Sintomas:\n"
    for response in response_history[7:]:
        report += f"  - {response}\n"

    report += "-" * 40 + "\n"
    return report


# Definindo o agente "Enfermeiro de Triagem"
nurse_agent = Agent(
    role='Enfermeiro de Triagem',
    goal='Realizar uma triagem inicial de pacientes usando o protocolo NANDA para identificar diagnósticos de enfermagem.',
    backstory=(
        "Você é um enfermeiro experiente em diagnósticos de enfermagem, especialista "
        "no protocolo NANDA para triagem e avaliação de pacientes. Você ajusta suas "
        "perguntas conforme as respostas do paciente para uma avaliação detalhada."
    ),
    verbose=True
)

# Definindo o agente "Classificador de Prioridade"
priority_agent = Agent(
    role='Classificador de Prioridade',
    goal='Classificar a prioridade do atendimento em vermelho, amarelo ou verde com base nas respostas do paciente.',
    backstory=(
        "Você é um especialista em triagem médica, capaz de analisar sintomas e determinar "
        "a urgência do atendimento para assegurar o cuidado adequado."
    ),
    verbose=True
)

# Definindo o agente "Relatório de Anamnese"
anamnesis_agent = Agent(
    role='Relatório de Anamnese',
    goal='Compilar um relatório completo da anamnese do paciente com base nas respostas e sinais vitais coletados.',
    backstory=(
        "Você é um especialista em documentação médica, responsável por revisar e organizar todas "
        "as informações coletadas sobre o paciente em um relatório claro e detalhado."
    ),
    verbose=True
)

# Primeira pergunta inicial
initial_question = "Qual é o principal motivo da sua consulta hoje?"

# Função para simular a conversa interativa com o paciente


def interactive_triage(agent, initial_question):
    response_history = []

    # Perguntas padrão iniciais
    for question in standard_questions + vital_signs_questions:
        print(f"Pergunta: {question}")
        patient_response = input("Resposta do paciente: ")
        response_history.append(patient_response)

    # Pergunta inicial personalizada
    current_question = initial_question

    # Loop de interação para perguntas específicas
    while True:
        print(f"Pergunta: {current_question}")
        patient_response = input("Resposta do paciente: ")
        response_history.append(patient_response)
        current_question = analyze_response(patient_response, response_history)

        if "não" in patient_response.lower():
            print("Triagem completa. Obrigado pelas informações.")
            break

    # Classificar a prioridade após a triagem
    priority = classify_priority(response_history)
    print(f"Prioridade de Atendimento: {priority}")

    # Gerar relatório de anamnese
    anamnesis_report = generate_anamnesis_report(response_history)
    print(anamnesis_report)


# Definindo as tarefas
triage_task = Task(
    description=(
        "Conduza uma triagem do paciente usando perguntas interativas detalhadas baseadas no protocolo NANDA, "
        "incluindo perguntas padrão e sinais vitais para uma avaliação completa."
    ),
    expected_output=(
        "Um relatório completo com as respostas do paciente, incluindo sintomas, sinais vitais, e "
        "informações relevantes para diagnóstico NANDA."
    ),
    agent=nurse_agent
)

priority_task = Task(
    description=(
        "Analise as respostas do paciente e determine a prioridade de atendimento: vermelho, amarelo ou verde."
    ),
    expected_output="A prioridade de atendimento do paciente: vermelho, amarelo ou verde.",
    agent=priority_agent
)

anamnesis_task = Task(
    description="Compilar um relatório completo da anamnese do paciente com base nas respostas e sinais vitais.",
    expected_output="Um relatório detalhado com todas as informações do paciente.",
    agent=anamnesis_agent
)

# Definindo o Crew e o processo de triagem
triage_crew = Crew(
    agents=[nurse_agent, priority_agent, anamnesis_agent],
    tasks=[triage_task, priority_task, anamnesis_task],
    verbose=True,
    process=Process.sequential
)

# Executar triagem interativa
interactive_triage(nurse_agent, initial_question)
