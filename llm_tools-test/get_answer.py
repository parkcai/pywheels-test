from pywheels.llm_tools.get_answer import get_answer


def main():
    
    # test simple 
    model = "Qwen-Max"
    prompt = input("[Me] ")
    llm_answer = get_answer(
        model = model,
        prompt = prompt,
    )
    print(f"[{model}] {llm_answer}")
    
    # test elaborate
    model = "Qwen-VL-Max"
    prompt = input(f"[Me, attaching a picture about a dog drinking water near a river]\n")
    llm_answer = get_answer(
        prompt = prompt,
        model = model,
        system_prompt = "Please respond to the following sentence in a natural way.",
        images = ["llm_tools-test/dog.png"],
        image_placeholder = "<image>",
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
    
