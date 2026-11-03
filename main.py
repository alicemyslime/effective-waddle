from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/facts")
async def get_facts():
    return {
        "facts": [
            "Cats are obligate carnivores, so they need nutrients found in animal tissues.",
            "Most cats have 18 toes: five on each front paw and four on each back paw.",
            "A cat's whiskers help it sense nearby objects and changes in its surroundings.",
            "Cats have a reflective layer behind their retinas that helps them see in low light.",
            "Cats can rotate their ears independently to help locate sounds.",
            "Cats have a third eyelid, called the nictitating membrane.",
            "Most cats cannot taste sweetness because they lack a functional sweet taste receptor.",
            "Cats use scent glands around their cheeks and paws to leave familiar scent marks.",
        ]
    }