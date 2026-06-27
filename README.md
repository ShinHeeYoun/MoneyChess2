# MoneyChess2

MoneyChess2 is a modular, turn-based strategic mercenary management game where players manage a mercenary company using chess pieces.

## Execution Instructions
- **System Prerequisites:** Python 3.8 or higher.
- **Dependency Installation:** `pip install pygame`
- **Execution Command:** `python main.py`

## Features
- **Dynamic Economy:** Manage mercenaries through a randomized shop ecosystem with strict upkeep mechanics.
- **Graphical Interactivity:** Pure mouse-driven UI containing interactive buttons, drag-and-drop mechanics, and spatial hover highlights utilizing authentic Cburnett-style open-source chess sprites.
- **Tactical Node Selection:** Players choose between three branching risk contracts (Low, Medium, High), scaling AI enemy density and reward yields for tactical autonomy.
- **Strategic Combat:** True chess movement logic with a dynamically generated AI adapting its budget to higher stages.
- **Casualty & Attrition:** Simulated d100 probability matrix tracks injury/death outcomes for captured pieces.
- **Infinite Pawn Conscription:** Base infantry pawns bypass shop rotation variables and are infinitely purchasable from the Management screen.
- **Persistent Progress:** JSON serialization enables secure Auto-Saving after every match instance.


## [2026-06-27] Module Update: Core Engine Initialization
- Initialized project with Python/Pygame stack.\n- Implemented core configuration file (config.py) defining economy parameters, window settings, and dynamic hospital recovery ranges.\n- Created state management logic and game engine foundation.\n- Added robust git automation helper for continuous documentation updates.

## [2026-06-27] Module Update: Economy and Units
- Integrated EconomyManager and ShopManager with dynamic shop size and generation weights.\n- Created Unit Roster system tracking active/injured statuses and recovery periods.\n- Bound economy variables strictly to config.py as required.\n- Mocked Management phase inputs inside core Engine to validate buy, sell, reroll, and upkeep logic.

## [2026-06-27] Module Update: Deployment Phase and AI Formations
- Implemented BoardGrid defining 8x8 spatial boundaries and occupation logic.\n- Built DeploymentManager to capture drag-and-drop mouse events strictly bound to rows 6 and 7.\n- Added AIFormationGenerator that evaluates dynamic Vanguard, Defensive, and Standard matrices.\n- Upgraded state transitions in core engine to support DEPLOYMENT loop and grid rendering.

## [2026-06-27] Module Update: Combat Engine and Casualty System
- Implemented chess move validation spanning all standard piece vectors.\n- Built CombatEngine encapsulating turn sequence, AI priority-capture logic, and win-state evaluations.\n- Designed CaptureBuffer to securely track captured pieces during combat instances.\n- Integrated CasualtyProcessor d100 probability matrix executing upon RESOLUTION state transition.\n- Finalized global state loop connecting MANAGEMENT, DEPLOYMENT, COMBAT, RESOLUTION, and GAME OVER scenarios.

## [2026-06-27] Module Update: Persistence and Progression Polish
- Engineered JSON-based SaveManager enabling Auto-Save on match completion and Load Game functions from Main Menu.\n- Bound AIFormationGenerator to dynamic config scaling matrix linked to the current_stage counter.\n- Implemented graceful fallback quit sequences bridging Pygame OS triggers.\n- Finalized README.md with comprehensive feature definitions enforcing strict technical notation.

## [2026-06-27] Module Update: Visual Interactivity and Tactical Stage Selection
- Introduced UIButton UI module mapping strict collision boundaries and executing callback pipelines, stripping all debug keybindings from the engine.\n- Designed fallback sprite rendering pipeline overlaying custom geometric designs for every piece archetype utilizing standard Pygame drawing commands.\n- Integrated STAGE_SELECT state, deploying dynamic grid preview algorithms mapping risk scalars against base AI budgets to calculate variable node challenges.\n- Reconstructed game UI layer integrating visual context bounding box highlights natively rendering per frame update loops.

## [2026-06-27] Patch 6.5: Combat Engine Hotfix, Authentic Sprites, and Infinite Pawn Shop
- Resolved critical AttributeError in check_victory_condition() by mapping UUIDs to ChessPiece object arrays natively prior to logic evaluation.\n- Updated asset loader to dynamically load Cburnett-style chess sprite PNGs for standard rendering and completely removed legacy geometric rendering fallbacks.\n- Implemented dynamic missing asset logging module to stdout for transparent tracking.\n- Integrated an independent 'Recruit Pawn' button into the Management UI loop permitting unlimited baseline unit purchases directly outside the randomized shop loop.

