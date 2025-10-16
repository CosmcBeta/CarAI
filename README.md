# Race Track

**Race Track** is a top-down 2D "racing" game featuring a procedurally generated track built using **convex hulls** and **interpolation**. This was
originally made to be used to make my own ai and that will be the plan for the future after refactoring current code.

## Important

This is currently under heavy rework and current main repo may now work. This is part of an entire overhaul of the code and is intentional. I will update the
README once more has been completed.


---

## Roadmap
- Implement a **custom interpolation method** to replace SciPy splines.
- **Rewrite** and refactor code for better readability and structure.
- **Optimize performance** in track generation, rendering, and program overall.
- (Future) Add self made AI that can learn how to complete any track given.

---

## Requirements
- Python 3.12
- `pygame`
- `numpy`
- `scipy`

Install dependencies with:
```bash
pip install -r requirements.txt
