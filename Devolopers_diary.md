# Developer Diary

## Day 1 — Building the Foundation

Today I started building GoalOracle 2026, a FIFA World Cup intelligence engine designed to go beyond a basic match predictor. The first goal was to create a clean project structure and initialize the core data pipeline.

I created the Conda environment named GoalOracle, installed the required scientific Python libraries, and structured the project into separate modules for data loading, ratings, feature engineering, simulation, and analytics.

The first working component is the team rating engine. It converts basic team metadata such as FIFA rank, confederation, and host status into GoalOracle-specific ratings: Oracle Rating, Attack Index, Defense Index, and Momentum Index.

I also built the first match feature generator, which compares two teams and produces rating differences that will later feed into the xG and Bivariate Poisson match simulation engine.

By the end of Day 1, the project can load team data, calculate team ratings, and generate features for a sample match such as Argentina vs France.
