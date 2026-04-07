from fastapi import FastAPI
from env.environment import DynamicPricingEnv
from env.models import Action

app = FastAPI()

env = DynamicPricingEnv(task_name="easy")


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict(),
        "reward": None,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info,   
    }


@app.get("/state")
def state():
    return env.state()