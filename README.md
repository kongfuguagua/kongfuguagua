# Chris · Mengqi Han

**Building agents and world models for real-world systems.**

Ph.D. student at **Shanghai Jiao Tong University**. I work on agents that turn intent into validated actions, and world models that connect observations, prediction, and control.

[Email](mailto:a25505597703@gmail.com) · [Research](#research) · [Engineering](#engineering-foundations) · [Code](#earlier-work)

![A feedback loop connecting Observe, Model, Plan, and Act, with feedback from the physical system informing the next observation.](assets/loop-light.svg)

## Research

Two connected directions: **agents that reason and act**, and **world models that predict and guide control**. The animations below illustrate the methods; all depicted signals and states are synthetic.

### Agentic Systems

#### ADA · Agentic Dispatch

![ADA concept animation: a synthetic grid state passes through tools, solving, and validation; fast decisions and slower knowledge updates form two feedback loops.](assets/research/ada.gif)

Turn power-system dispatch intent into mathematical models, tool-assisted solving, and physically validated actions. Feedback connects fast decision adaptation with slower updates to modeling knowledge.

#### SOA · Simulation Refinement

![SOA concept animation: synthetic reference and simulation signals illustrate iterative structural and parameter refinement guided by LLM proposals, fuzzy rules, and simulation feedback.](assets/research/soa.gif)

Bring electrical-system simulations closer to measured behavior through iterative structural and parameter refinement. LLM proposals, fuzzy-rule guidance, and simulation feedback connect reasoning with physically grounded updates.

### World Models

#### HacWM · World Models for Control

![HacWM concept animation: roll out candidate trajectories, select a plan, execute only its first action, then observe the next state and replan. All trajectories are synthetic.](assets/research/hacwm.gif)

Learn action-conditioned device dynamics to support control across different air-conditioner models. World-model rollouts and receding-horizon planning connect predictions to energy-aware control actions.

<!-- #### SolarJEPA · Multimodal Forecasting

![SolarJEPA concept animation: synthetic historical cloud observations and time-series windows align across a time lag to support future solar forecasting.](assets/research/solarjepa.gif)

Learn from sky imagery and time-series observations with multimodal self-supervision. Transition alignment links cloud dynamics to subsequent solar-energy changes for forecasting. -->

## Engineering Foundations

- **Agent orchestration & validation** — Connect intent, tools, solvers, and feedback into verifiable workflows. *ADA · SOA*
- **Prediction & control** — Connect multimodal observations, learned dynamics, and planning to decisions. *SolarJEPA · HacWM*
- **Cloud–edge systems** — Connect microservice orchestration with an edge-computing testbed for flexible production. *ECPAD*

## Earlier Work

**ECPAD** — Edge-computing architecture and microservice orchestration for a flexible production line, with a self-built experimental platform.

[Code](https://github.com/kongfuguagua/ECPAD) · [Paper](https://ieeexplore.ieee.org/document/10774337)

**DANN** — Transfer learning for motor-imagery EEG classification; my undergraduate thesis project at Harbin Institute of Technology.

[Code](https://github.com/kongfuguagua/DANN_EEG) · [Paper](https://ieeexplore.ieee.org/document/10241474/)

## Contact

Let's talk about agentic systems, world models, and AI engineering for physical systems.

[a25505597703@gmail.com](mailto:a25505597703@gmail.com) · [GitHub](https://github.com/kongfuguagua)
