# MoneyChess2

MoneyChess2 is a modular, turn-based strategic mercenary management game where players manage a mercenary company using chess pieces.

## Execution Instructions
- **System Prerequisites:** Python 3.8 or higher.
- **Dependency Installation:** `pip install pygame`
- **Execution Command:** `python main.py`

## [2026-06-27] Module Update: Core Engine Initialization
- Initialized project with Python/Pygame stack.\n- Implemented core configuration file (config.py) defining economy parameters, window settings, and dynamic hospital recovery ranges.\n- Created state management logic and game engine foundation.\n- Added robust git automation helper for continuous documentation updates.

## [2026-06-27] Module Update: Economy and Units
- Integrated EconomyManager and ShopManager with dynamic shop size and generation weights.\n- Created Unit Roster system tracking active/injured statuses and recovery periods.\n- Bound economy variables strictly to config.py as required.\n- Mocked Management phase inputs inside core Engine to validate buy, sell, reroll, and upkeep logic.

## [2026-06-27] Module Update: Deployment Phase and AI Formations
- Implemented BoardGrid defining 8x8 spatial boundaries and occupation logic.\n- Built DeploymentManager to capture drag-and-drop mouse events strictly bound to rows 6 and 7.\n- Added AIFormationGenerator that evaluates dynamic Vanguard, Defensive, and Standard matrices.\n- Upgraded state transitions in core engine to support DEPLOYMENT loop and grid rendering.

