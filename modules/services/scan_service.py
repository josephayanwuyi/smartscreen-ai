from modules.services.llm_service import analyze_image_with_groq

def analyze_image(image_file, model=None):
    # This calls the Groq function we made earlier
    result_text = analyze_image_with_groq(image_file)
    
    return {
        "type": "Fridge Scan",
        "analysis": result_text,
        "items": [] # Adding this prevents errors in your background service
    }