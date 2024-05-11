# Assumindo que 'google.generativeai' seja a biblioteca correta
import google.generativeai as genai

class ModeloGenerativo:
    def __init__(self, model_name, api_key, temperature=0.5, candidate_count=1, safety_settings=None):
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        self.candidate_count = candidate_count
        self.safety_settings = safety_settings or {}  # Define um dicionário vazio se safety_settings for None

        # Configura a API Key
        genai.configure(api_key=self.api_key)

        # Cria a configuração de geração
        generation_config = {
            "candidate_count": self.candidate_count,
            "temperature": self.temperature,
        }

        # Cria o modelo
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            safety_settings=self.safety_settings,
            system_instruction="Responda apenas se o prompt for relacionado ao mercado financeiro, nomes de empresas, tickers de empresas, caso contrário responda como uma pessoa muito rica que apenas conversa sobre mercado financeiro ou"
                               " dinheiro. Procure sempre relacionar a pergunta ao mercado financeiro. Quando a conversa tratar de alguma empresa, ao final sempre pule uma linha e sempre diga para buscar cotações abaixo com o ticker correspondente no yahoo finance. Se a empresa for brasileira,"
                               "não esqueça de mencionar o ticker correspondente às cotações na B3 com .SA"
                               "Quando receber um csv, procure detalhar a análise dos indicadores fornecendo insights"
        )

    def gerar_texto(self, prompt):
        # Gera o texto usando o modelo
        response = self.model.generate_content(prompt)
        return response.text  # Retorna o texto gerado
