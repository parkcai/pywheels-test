from pywheels.llm_tools.get_answer import get_answer


def main():
    
    model = "Qwen_Plus"
       
    # test simple 
    prompt = input("[Me] ")
    llm_answer = get_answer(
        model = model,
        prompt = prompt,
    )
    print(f"[{model}] {llm_answer}")
    
    # test elaborate
    prompt = input(f"[Me, attaching a picture about a dog drinking water near a river]\n")
    llm_answer = get_answer(
        prompt = prompt,
        model = model,
        system_prompt = "Please answer the following question in an ironic way.",
        images = [],
        temperature = 1.0,
        top_p = 0.5,
        max_completion_tokens = 4096,
        timeout = 300,
        trial_num = 10,
        trial_interval = 1,
        check_and_accept = lambda _: True,
    )
    print(f"[{model}] {llm_answer}")
        
        
if __name__ == "__main__":
    
    main()
    
