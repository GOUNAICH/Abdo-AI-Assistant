import os
from huggingface_hub import InferenceClient

def generate_img(command):
    # Extract the prompt from the command
    prompt = command.replace("generate image for", "").strip()
    
    
    client = InferenceClient(
        token="Your_api_key"
    )

    try:
        # Generate the image using the extracted prompt
        image = client.text_to_image(
            prompt=prompt,
            model="runwayml/stable-diffusion-v1-5"
        )
           
        documents_path = os.path.join(os.path.expanduser("~"), "Documents") 
        
        if not os.path.exists(documents_path):
            os.makedirs(documents_path)
        
        filename = os.path.join(documents_path, f"{prompt.replace(' ', '_')}.png")
        image.save(filename)
        
        image.show()

        print(f"Image saved in Documents as {filename}.")
        return filename
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
