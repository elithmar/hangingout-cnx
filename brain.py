import os
import json
import datetime
import requests
from bs4 import BeautifulSoup
from google import genai

def fetch_events_from_web():
    """
    Simula o ejecuta un scraping real a una fuente pública (Ej. Un feed RSS, una web de eventos o meetup local).
    Por ahora, bajaremos el HTML de una fuente dummy o usaremos un texto realista si la fuente está bloqueada.
    """
    print("🌍 Conectando a internet para buscar eventos en Chiang Mai...")
    
    # En un entorno real, aquí haríamos requests.get('https://www.eventbrite.com/... o similar')
    # Como muchas bloquean bots, usaremos un texto de prueba que simula lo que el scraper ha extraído hoy.
    
    extracted_text_from_web = """
    Lanna Fight Gym - Free Intro Muay Thai Class today at 5:00 PM! Everyone is welcome to join our beginner friendly session.
    Also, don't miss the Language Exchange at Yellow Coworking tomorrow at 7:00 PM, absolutely free.
    """
    return extracted_text_from_web

def process_with_ai(raw_text):
    """
    Envía el texto sucio a Gemini (Google AI) para estructurarlo en JSON.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ ADVERTENCIA: No se encontró GEMINI_API_KEY. Simulando respuesta por defecto...")
        return [{
            "id": int(datetime.datetime.now().timestamp()),
            "title": "MOCK: FREE MUAY THAI INTRO",
            "venue": "Lanna Fight Gym",
            "time": "5:00 PM",
            "category": "Workout",
            "type": "workout",
            "imageUrl": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&q=80&w=800",
            "attending": 0,
            "timeStatus": "Today"
        }]

    print("🧠 Procesando texto con Inteligencia Artificial (Gemini)...")
    
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Eres un asistente experto en eventos en Chiang Mai.
        Analiza el siguiente texto extraído de internet y encuentra eventos que sean GRATIS.
        Devuelve ÚNICAMENTE un array JSON válido con los eventos encontrados. No añadas backticks (```json) ni texto extra.
        Formato de cada objeto:
        {{
            "id": <numero aleatorio único>,
            "title": "<título corto en mayúsculas>",
            "venue": "<nombre del lugar>",
            "time": "<hora ej. 5:00 PM>",
            "category": "<Workout, Live Music, Cultural o Language>",
            "type": "<workout, music o culture>",
            "imageUrl": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?auto=format&fit=crop&q=80&w=800",
            "attending": 0,
            "timeStatus": "Today"
        }}
        
        Texto extraído:
        {raw_text}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Parseamos el JSON devuelto por la IA
        ai_result = response.text.strip()
        if ai_result.startswith('```json'):
            ai_result = ai_result.replace('```json', '').replace('```', '').strip()
            
        events = json.loads(ai_result)
        print(f"✅ La IA ha encontrado y estructurado {len(events)} eventos.")
        return events
        
    except Exception as e:
        print(f"❌ Error al contactar con la IA: {e}")
        return []

def main():
    print("🚀 Arrancando 'El Cerebro' de Hanging Out CNX...")
    
    # 1. Obtener la información cruda
    raw_data = fetch_events_from_web()
    
    # 2. Estructurarla con IA
    new_events = process_with_ai(raw_data)
    
    if not new_events:
        print("No se encontraron eventos nuevos hoy.")
        return

    # 3. Leer base de datos actual
    db_path = 'events.json'
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            current_events = json.load(f)
    else:
        current_events = []
        
    # 4. Insertar eventos nuevos
    # En un entorno real, deberíamos comprobar si el evento ya existe (por título o fecha)
    for event in new_events:
        current_events.insert(0, event)
        
    # 5. Guardar JSON y JS
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(current_events, f, indent=4)
        
    with open('events.js', 'w', encoding='utf-8') as f:
        f.write(f"window.eventsData = {json.dumps(current_events, indent=4)};")
        
    print(f"💾 Base de datos actualizada con éxito con {len(new_events)} eventos nuevos.")

if __name__ == "__main__":
    main()
