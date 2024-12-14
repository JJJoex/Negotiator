import negmas
import random
from tqdm import tqdm
from negmas import SAOMechanism, AspirationNegotiator, MappingUtilityFunction

session = SAOMechanism(outcomes=10, n_steps=100)
negotiators = [AspirationNegotiator(name=f"a{_}") for _ in range(5)]
for negotiator in negotiators:
    session.add(
        negotiator, preferences=MappingUtilityFunction(lambda x: random.random() * x[0])
    )
session.run()
print(111)