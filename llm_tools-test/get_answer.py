from pywheels.llm_tools import get_answer


def main():
    
    model_name = "Qwen_Plus"
        
    prompt = input("[Me] ")
    
    llm_answer = get_answer(
        model_name = model_name,
        prompt = prompt,
    )
    
    print(f"[{model_name}] {llm_answer}")
        
        
if __name__ == "__main__":
    
    main()
    
