# AgentSteve
This project is aimed at constructing an agent in the popular video game Minecraft that is capable of learning, exploring and helping, with the power of deep learning!

For more detailed documentation, check out this [link](https://agentsteve.readthedocs.io/en/latest/)

## Introduction
Minecraft is a 2011 sandbox video game created by Markus Persson. It has no specific goals to accomplish. Players can build houses, develop agriculture and raise livestock. They can also create armors and swords, brew magic portions to fight with mummies, dragons, and other hostile creatures. Villages, desert palaces, underseas ancient cities, and other amazing constructions are waiting for players to discover. Please visit the game's [websit](https://minecraft.net/)  for more information!

Nowadays, deep learning can achieve pretty astonishing goal, such as beating human players in extremely intelligent chess game Go, see [AlphaGo](https://deepmind.com/research/alphago), created by team DeepMind. But making machine to play a game like Minecraft is still an active research area. It requires machine to have intrinsic interests to its surroundings, desires for new knowledge and the ability to require them, just like our human do, instead of simply fulfilling a given goal.

In this project, we intend to (at least partly) achieve the goal to create an agent that is smart enough to be capable of:

* **learning from others**, including human players and other agents. For example, learn from demonstration and try to replicate the result, or in other words, the ability of imitating.
* **fulfiling tasks**, including those assigned by human players, other agents and itself. It knows how to plan, how to divide the big and abstract goal into smaller pieces, and conquer them one by one to accomplish the ultimate goal.
* **exploring**. Agent should be curious about its surrounding world and have intrinsic desire for knowledge. It likes novel things and hates boring life.
* **social networking**. The agent is encouraged by others' recognition and accompany. It is desired for friendship and always willing to help. It should be able to communicate with others about its own motives and intensions, especially to human player. It should also understand others' meaning and reasoning.
* **memorizing**. It has an experience database. All past experiences and knowledge will be efficiently stored and can be retrieved fastly. Unimportant or too ancient memories will be dumped. Important and recent memories will be highlighted.
* **predicting**. Agent should be able to predict the near and far futures. Predicing power will be heavily based on past experiences (experience database). Having a vision even for the near future and knowing the consequences of its own actions would be very beneficial for agent to achieve its ultimate goal.
* **transferring knowledge**. Knowledge obtained by one system should be able to be utilized by other system (may be through experience database). For example, skills learned by imitating, or knowledge gained through exploring should be able to be applied to better fulfilling tasks later.

##Getting Started
This project uses Malmo project by Microsoft to provide the Minecraft game environment. Malmo is a platform for Artificial Intelligence experimentation and research built on top of Minecraft. To install and run Malmo platform, see docs on its [GitHub page](https://github.com/Microsoft/malmo). Personally, I recommend using Ubuntu 16.04 64 bit system, with Python 2.7.

We will be using TensorFlow as the main tool for researching deep learning capability. TensorFlow is an open source machine learning framework developed by Google. The latest version is 1.8, and we will start experimenting on this version. Please visit their [site](https://www.tensorflow.org) for installation and more information.


I am currently working on the first module, i.e. the imitation system. Major inspiration came from this paper: *Third-Person Imitation Learning*, by Bradly Stadie, Pieter Abbel and Ilya Sutskever. You can access this paper on arXiv on this [link](https://arxiv.org/pdf/1703.01703).
