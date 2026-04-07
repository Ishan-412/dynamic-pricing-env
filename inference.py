import os
from openai import OpenAI 
from env.environment import DynamicPricingEnv
from env.models import Action
from env.graders import grade_task

API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
HF_TOKEN = os.getenv("HF_TOKEN")


def get_action_from_model(observation):
    """
    Deterministic pricing agent (no API).
    """

    if observation.demand_level > 0.7:
        new_price = observation.current_price * 1.1

    elif observation.demand_level < 0.3:
        new_price = observation.current_price * 0.9

    else:
        new_price = observation.current_price

    
    new_price = max(5.0, min(new_price, 200.0))

    return Action(new_price=new_price)



def run_task(task_name):
    env = DynamicPricingEnv(task_name=task_name)
    obs = env.reset()

    print(f"[START] task={task_name}")

    total_reward = 0

    while True:
        action = get_action_from_model(obs)

        obs, reward, done, _ = env.step(action)

        total_reward += reward.score

        print(
            f"[STEP] reward={reward.score} "
            f"price={obs.current_price} "
            f"inventory={obs.inventory} "
            f"done={done}"
        )

        if done:
            break

    final_score = grade_task(task_name, env.state())

    print(f"[END] total_reward={total_reward} final_score={final_score}")


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_task(task)