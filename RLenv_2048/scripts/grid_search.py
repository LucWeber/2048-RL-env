import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from RLenv_2048.env.RLenv2048 import RLenv2048

from RLenv_2048.policies import RandomPolicy, baselineREINFORCEpolicy
from RLenv_2048.utils import get_config, train_policy


if __name__ == "__main__":

  total_sessions = [3000]
  t_max = 15000
  #sampling = 'soft'
  gammas = [0.95, 0.99, .8] #  discount factor for reward
  epsilons = [0.0] #, 0.1, 0.3] #for epsilon-greedy action selection
  entropy_terms = [0.0] #, 0.2, 0.3, 0.5 0.01, 0.05,  for entropy regularization (to encourage exploration)
  lrs = [ 1e-4, 5e-5,] # learning rate
  i = 0
  for lr in lrs:
    for gamma in gammas:
      for epsilon in epsilons:
        for entropy_term in entropy_terms:
          for total_session in total_sessions:
            i+=1
            if i == 1:
                continue

            config = get_config()
            config.total_sessions = total_session
            config.t_max = t_max
            config.gamma = gamma
            config.epsilon = epsilon
            config.entropy_term = entropy_term
            config.lr = lr
            config.save_name = f'{config.model_type}_sess_{total_session}_tmax_{t_max}_gamma_{gamma}_epsilon_{epsilon}_entropy_{entropy_term}_lr_{lr}_{config.sampling}_{config.exp}'
            print(config)

            # INIT ENVIRONMENT
            env = RLenv2048(mode='agent')

            # INIT POLICY
            policy_baseline = RandomPolicy(env, verbose=0)
            policy = baselineREINFORCEpolicy(env, **vars(config))

            assert config.train, 'Training is disabled. Set config.train=True to train the model.'
            train_policy(config, policy, policy_baseline)
