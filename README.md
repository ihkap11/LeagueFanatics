# [WIP] League Fanatics
Motivation: - Frustrated by League of Legend's matchmaking ⚔️, I decided to start working on my own [game simulation](https://github.com/ihkap11/LeagueFanatics) to understand  matchmaking and ranking algorithms, and eventually build a working software. 
- Short term:
  - Built a client-server using FastAPI REST and websockets.
  - Working on dockerizing the application, kubernetes for orchestration and redpanda for live streaming.
- Long term:
   - For matchmaking use: [_A Bayesian Approximation Method for Online Ranking_](https://jmlr.org/papers/volume12/weng11a/weng11a.pdf) by Weng and Lin.
   - have plugins for different matchmaking algorithms: TrueSkill, Elo, (find more) (try to match league's MMR)

The intention behind this project from a software standpoint is to build a simple client-server system that can handle 100s of matchmaking requests and then scale it to billions of simulated requests. In the process, I want to compare different open-source tools and develop sense of when to use what, and incrementally integrate these tools to support increasing complexities.

A rough take on system design.

![Untitled-2024-02-06-1236](https://github.com/ihkap11/LeagueFanatics/assets/31574850/6e53dfb9-24f2-40c3-b9f8-c0fd4c88df6d)


Todos:
- [x] Streamlit with asynchronous matchmaking service. [[here](https://github.com/ihkap11/LeagueFanatics/blob/main/src/client/client.py)]
- [x] FastAPI REST APIs for supporting client initiated player info requests. [[here](https://github.com/ihkap11/LeagueFanatics/blob/main/src/server/api.py)]
- [x] TrueSkill matchmaking algorithm implementation [[here](https://github.com/ihkap11/LeagueFanatics/blob/main/src/matchmaker_service/skill.py)]
- [] integrate postgress DB
- [] dockerise application
- [] use redpanda/kafka/rabbitMQ for streaming instead of plain websockets.

### Resources:
- https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/publications/
- https://jmlr.org/papers/volume12/weng11a/weng11a.pdf
