from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials




SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
    print("Iniciando o programa...")
    creds = None

    if os.path.exists("token.json"):
        print("Carregando credenciais do token.json...")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        print("Credenciais inválidas ou não encontradas.")
        if creds and creds.expired and creds.refresh_token:
            print("Atualizando credenciais...")
            creds.refresh(Request())
        else:
            print("Autenticando com client_secret.json...")
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    
    print("Construindo o serviço do Google Sheets...")
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    try:
        print("Fazendo a chamada para a API do Google Sheets...")
        result = sheet.values().get(spreadsheetId='codigo da planilha',
                                    range='Página1!B1:B').execute()
        values = result.get('values', [])
        print(values)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    