import requests
import json
import time
import base64
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('.env.local')

# Configuração da API
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
API_URL = "https://api.replicate.com/v1/models/black-forest-labs/flux-1.1-pro/predictions"

headers = {
    "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json",
    "Prefer": "wait"
}

# Prompt para gerar a imagem
prompt = """
Professional portrait photo of a young woman with beautiful curly hair flowing naturally, 
mixed-race Brazilian woman with warm brown skin tone, 
natural curly hair texture, soft lighting, 
professional headshot style, clean background, 
high quality photography, portrait photography, 
natural makeup, friendly expression, 
suitable for professional portfolio
"""

# Dados para a requisição
data = {
    "input": {
        "prompt": prompt,
        "prompt_upsampling": True,
        "aspect_ratio": "1:1",
        "output_quality": 90
    }
}

print("Gerando imagem da menina parda com cabelos cacheados soltos...")
print("Aguarde, isso pode levar alguns segundos...")

try:
    # Fazer a requisição
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200 or response.status_code == 201:
        result = response.json()
        
        if 'output' in result and result['output']:
            image_url = result['output'][0] if isinstance(result['output'], list) else result['output']
            
            # Baixar a imagem
            print(f"Baixando imagem de: {image_url}")
            img_response = requests.get(image_url)
            
            if img_response.status_code == 200:
                # Salvar a imagem
                with open('images/profile.jpg', 'wb') as f:
                    f.write(img_response.content)
                print("✅ Imagem salva com sucesso em 'images/profile.jpg'")
            else:
                print(f"❌ Erro ao baixar a imagem: {img_response.status_code}")
        else:
            print("❌ Resposta da API não contém imagem")
            print(f"Resposta completa: {result}")
    else:
        print(f"❌ Erro na API: {response.status_code}")
        print(f"Resposta: {response.text}")

except Exception as e:
    print(f"❌ Erro: {str(e)}")
