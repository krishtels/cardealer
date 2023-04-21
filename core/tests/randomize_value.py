import random

from core.models import Car


def get_random_specification():
    color = ["black", "red", "yellow", "blue", "purple", "white", "gray"]
    cars_models = {
        "Volkswagen": ["Polo", "Golf", "Passat"],
        "Toyota": ["Corolla", "Camry"],
        "BMW": ["iX", "X5", "X3"],
        "Ford": ["F-Series", "Fiesta", "Focus"],
    }
    brand = random.choice(list(cars_models))
    model = random.choice(cars_models[brand])
    specification = {
        "max_price": round(random.uniform(100, 10000), 2),
        "engine_type": random.choice(Car.EngineType.choices[0]),
        "brand": brand,
        "model": model,
        "color": random.choice(color),
        "engine_volume": round(random.uniform(0, 10), 1),
    }

    return specification
