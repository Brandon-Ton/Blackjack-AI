This is my ONGOING personal project about a neural network that I started in August 2023.

I do not know how to implement common neural network training algorithms, so for now, I'm just using random mutations.
The blackjack rules being used is more lenient than casiono rules, so theorhetically, a +50% win rate should be able to be achieved with perfect play.
Currently, 1000 games of blackjack per network are simulated to calculate each networks fitness for the generation. This fitness is calculated as 'games won - games lost' and determines which networks are destroyed and which gets a mutated clone.
