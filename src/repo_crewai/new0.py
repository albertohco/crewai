from crewai import Agent, Task, Crew, Process

# Definindo o modelo para todos os agentes (groq/llama-3.1-8b-instant)
model = "groq/llama-3.1-8b-instant"

# Definindo o agente "Enfermeiro de Triagem"
nurse_agent = Agent(
    role='Enfermeiro de Triagem',
    goal='Realizar uma triagem inicial de pacientes usando o protocolo NANDA para identificar diagnósticos de enfermagem.',
    backstory=(
        "Você é um enfermeiro experiente em diagnósticos de enfermagem, especialista "
        "no protocolo NANDA para triagem e avaliação de pacientes."
    ),
    memory=True,  # Mantém as respostas para uma conversa fluida
    verbose=True,
    llm=model,  # Usando o modelo groq/llama-3.1-8b-instant
)

# Definindo a tarefa de triagem
triage_task = Task(
    description=(
        "Conduza uma triagem do paciente usando perguntas do protocolo NANDA. "
        "Colete informações sobre sintomas, histórico médico, estado emocional e físico. "
        "Organize as respostas para um diagnóstico inicial com base no NANDA."
    ),
    expected_output=(
        "Um relatório completo com as respostas do paciente, incluindo sintomas e "
        "informações relevantes para diagnóstico NANDA."
    ),
    agent=nurse_agent
)

# Definindo o Crew e o processo de triagem
triage_crew = Crew(
    agents=[nurse_agent],
    tasks=[triage_task],
    process=Process.sequential  # As perguntas serão feitas de forma sequencial
)

# Iniciar o processo de triagem
result = triage_crew.kickoff(inputs={})
print(result)
