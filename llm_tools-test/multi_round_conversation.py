"""
尽管你连续问了三次“这张图片里有啥？”，但答案始终如一：
这是一幅描绘边境牧羊犬在秋日溪边饮水的油画，充满自然之美的细节与艺术感染力。
"""
from pywheels.llm_tools.get_answer import get_answer


def main():
    
    prompt = []
    images = []
    the_same_dog_image = "llm_tools-test/dog.png"
    image_placeholder = "<image_never_used_1145141919810>"
    model = "Qwen-VL-Max"
    for i in range(3):
        if i == 0:
            current_prompt = f"{image_placeholder}这张图片里有啥？"
        elif i == 1:
            current_prompt = f"{image_placeholder}这张图片里呢？"
        else:
            current_prompt = f"{image_placeholder}最后，这张图片里又有啥？"
        print(f"[User]\n{current_prompt}")
        prompt.append(current_prompt)
        images.append(the_same_dog_image)
        response = get_answer(
            prompt = prompt,
            model = model,
            images = images,
            image_placeholder = image_placeholder,
        )
        print(f"[{model}]\n{response}")
        prompt.append(response)


if __name__ == "__main__":
    
    main()