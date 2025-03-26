# Pitcher-Deception-Score
A Statcast-based metric that evaluates how deceptive a pitcher is based on release point consistency, velocity separation, and spin axis similarity.

## What is the Pitcher Deception Score?
Pitchers don’t just win with electric stuff—they win with deception.

This project introduces a new metric, the Pitcher Deception Score, which quantifies how difficult a pitcher is to read by combining three mechanical and pitch-based factors:

| Component               | Description                                                  
|-------------------------|--------------------------------------------------------------
| Release Point Variance  | Consistency of release point across all pitch types (lower = better) 
| Velocity Separation     | Difference in speed between fastball and off-speed pitches (higher = better) 
| Spin Axis Difference    | Difference in spin direction between pitch types (lower = better) 

Each component is normalized across all pitchers in the dataset and weighted as follows:
- 40% Release Point Consistency
- 30% Velocity Separation
- 30% Spin Axis Similarity

Higher scores indicate greater deception.

---

## Contents

- `deception.py`: Python script that pulls Statcast data and calculates deception scores
- `graphs/`: Folder containing bar plots for deception score and individual components
- `rays_deception_scores_2025.csv`: Final ranked deception scores for the Tampa Bay Rays
- `README.md`: Project overview and methodology

---

## Example: Tampa Bay Rays (2025)

This project currently analyzes the projected 2025 pitching staff for the Tampa Bay Rays using Statcast data through March 2025.

![Rays Deception Score](https://github.com/user-attachments/assets/5bdbce95-a91d-41e0-9c00-a9a9f6f49b9a)


More graphs are available in the `graphs/` folder, including component breakdowns for:
- Release Point Variance
- Velocity Separation
- Spin Axis Difference

---

## Planned Next Steps

- Add weekly tracking during the 2025 MLB season
- Expand to cover all 30 MLB teams
- Compare deception score to outcomes like K%, SwStr%, xERA, and WHIP
- Build an interactive dashboard to explore deception scores over time

---

## Author

**Tyler Curry**  
[LinkedIn](https://www.linkedin.com/in/tyler-curry-708b132b9/)  
[GitHub](https://github.com/pancaketoes)

---

## License

This project is licensed under the MIT License. See `LICENSE` file for details.
