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

## [2026-06-27] Patch 6.6: Hotfix for Economy Method Signature Alignment
- Rectified critical AttributeError occurring within action_buy_pawn button callback.\n- Aligned currency deduction interface to invoke self.economy.subtract_gold natively in adherence with Phase 2 EconomyManager standards.\n- Validated bankruptcy edge-cases for unlimited pawn generation against existing method parameters.

## [2026-06-27] Patch 6.7: Critical Turn 0 Defeat Bug and King Deployment Guard
- Engineered strict Turn 0 initialization guard within check_victory_condition() rejecting evaluation of empty unit matrices during combat transition.\n- Integrated King unit automatic initialization upon New Game protocol resolving zero-king combat states.\n- Developed robust Deployment sequence validation blocking 'Commence Battle' state progression if the company commander (King) is not physically mapped to a valid grid coordinate on the player's side.

## [2026-06-27] Patch 6.8: Combat State Machine and Alpha Rendering Corrections
- Rectified Match Termination Failure by pruning the Turn 0 Initialization Guard from check_victory_condition() which caused logic circumvention on list evaluation.\n- Fixed screen washout rendering regression by moving hover/alpha overlays to draw strictly after piece textures with proper pygame.SRCALPHA blending.\n- Fixed 'Double Action' state machine desync by replacing blocking pygame.time.delay(500) with a non-blocking frame timer (ai_turn_start_time), ensuring state changes draw cleanly without thread freezes.

## [2026-06-27] Patch 6.9: Emergency Hotfix - Residual Final Piece Artifact on Match Termination
- Enforced strict explicit 8x8 BoardGrid and DeploymentManager spatial wipeout immediately upon Combat state conclusion, completely severing all visual and logical positional bindings.\n- Relocated clear_deployment() method execution inside GameEngine up the logic chain to initialize precisely parallel with the RESOLUTION transition rather than return_to_camp, destroying all ghost caches.\n- Audited RESOLUTION draw buffer and overlaid a strict pygame.Surface block fill, removing final-turn combat artifact bleed-through.

## [2026-06-27] Phase 7: QoL Innovations, Upkeep Rebalancing, and Resolution Overlay
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

## [2026-06-27] Patch 6.6: Hotfix for Economy Method Signature Alignment
- Rectified critical AttributeError occurring within action_buy_pawn button callback.\n- Aligned currency deduction interface to invoke self.economy.subtract_gold natively in adherence with Phase 2 EconomyManager standards.\n- Validated bankruptcy edge-cases for unlimited pawn generation against existing method parameters.

## [2026-06-27] Patch 6.7: Critical Turn 0 Defeat Bug and King Deployment Guard
- Engineered strict Turn 0 initialization guard within check_victory_condition() rejecting evaluation of empty unit matrices during combat transition.\n- Integrated King unit automatic initialization upon New Game protocol resolving zero-king combat states.\n- Developed robust Deployment sequence validation blocking 'Commence Battle' state progression if the company commander (King) is not physically mapped to a valid grid coordinate on the player's side.

## [2026-06-27] Patch 6.8: Combat State Machine and Alpha Rendering Corrections
- Rectified Match Termination Failure by pruning the Turn 0 Initialization Guard from check_victory_condition() which caused logic circumvention on list evaluation.\n- Fixed screen washout rendering regression by moving hover/alpha overlays to draw strictly after piece textures with proper pygame.SRCALPHA blending.\n- Fixed 'Double Action' state machine desync by replacing blocking pygame.time.delay(500) with a non-blocking frame timer (ai_turn_start_time), ensuring state changes draw cleanly without thread freezes.

## [2026-06-27] Patch 6.9: Emergency Hotfix - Residual Final Piece Artifact on Match Termination
- Enforced strict explicit 8x8 BoardGrid and DeploymentManager spatial wipeout immediately upon Combat state conclusion, completely severing all visual and logical positional bindings.\n- Relocated clear_deployment() method execution inside GameEngine up the logic chain to initialize precisely parallel with the RESOLUTION transition rather than return_to_camp, destroying all ghost caches.\n- Audited RESOLUTION draw buffer and overlaid a strict pygame.Surface block fill, removing final-turn combat artifact bleed-through.

## [2026-06-27] Phase 7: QoL Innovations, Upkeep Rebalancing, and Resolution Overlay
- Recalibrated UNIT_DATA upkeep constants to scale 1:1 with traditional chess valuations.\n- Sanitized shop generation pool logic, natively removing pawns (shop_weight = 0).\n- Enforced King hard-lock conditional guard within shop_generator.sell_piece to explicitly reject commander sales.\n- Architected and integrated auto_deploy mapping algorithm parsing active units symmetrically onto Rows 6 and 7 upon DEPLOYMENT loop entry.\n- Enhanced drag-and-drop mechanics permitting 1:1 resident piece swapping without duplication.\n- Reconstructed RESOLUTION state render loop to cast a semi-transparent SRCALPHA overlay (0, 0, 0, 180) across the final COMBAT canvas.

## [2026-06-27] Patch 7.5: AI Spawn Fix and King Sell Lock
- Inverted DEPLOYMENT execution sequence inside engine.action_select_contract. Auto-deploy now executes prior to ai_generator.apply_formation to prevent the aggressive board clear from erasing newly instantiated enemy units.\n- Embedded a rigorous fallback assertion check into action_start_combat that regenerates the AI formation immediately prior to COMBAT phase lock if the board array registers zero enemy forces.\n- Masked the King completely from the Pygame UI render loop inside _build_ui_for_state, actively bypassing sell node creation for the commander unit.\n- Fortified sell_piece with secondary string literal parsing checks ensuring impenetrable type safety against accidental King liquidation.

## [2026-06-27] Phase 8: UI Realignment and Royal Guard Mechanics
- Shifted Roster and Sell UI components laterally to x=700 within engine._build_ui_for_state, safely decoupling them from the permanent Recruit Pawn node and resolving visual collisions.\n- Implemented Royal Guard invincibility layer inside combat.move_validation. is_enemy() now iterates target alliance arrays; if any Noble (Knight, Bishop, Rook, Queen) exists, an opposing King evaluates as an impassable barrier (False), dynamically dropping the lock exclusively upon the final Noble casualty.

## [2026-06-27] Phase 9: Fog of War, Captive Defection, and Dual-Control UI
- Upgraded economy balancing by zeroing out pawn upkeep overhead and shifting to dynamic material-value combat scaling (Sum of Destroyed Piece Values).
- Altered AIFormationGenerator sorting loops forcing Pawns to consume budget first for highly dense early row screenings.
- Refactored Deployment grid swap mechanics resolving ghosting by executing absolute coordinate swaps instead of deletion parsing on occupied tiles.
- Expanded the combat event listener architecture introducing Drag-to-Move input sequences natively overlapping legacy Click-to-Move protocols with rigid single-click focus retention.
- Masked enemy grid blitting during DEPLOYMENT phases simulating Fog of War variables.
- Developed a dynamic golden alpha-blended aura underlying all active Royal Guard evaluations directly inside the COMBAT drawing loop.
- Engineered Captive Defection logic logging all captured enemy matrices and executing a rigid 10% d100 success check to instantiate them into the player roster.
- Formulated absolute high-risk retreat protocols evaluating distance-to-deployment rows mapping down from 100% escape likelihood down to 65% on row 0; enforcing mandatory permadeath execution hooks overriding standard hospital logic loops.

## [2026-06-27] Phase 10: Roster UI Aggregation and Dynamic Visual Feedback Engine
- Engineered Roster Aggregation by iterating active units through a hash map, collapsing redundant Sell instances into unified rendering rows parsing `[Piece Name] x [Count]`.
- Implemented instantaneous zero-count eviction bounds by rigorously injecting `_build_ui_for_state()` downstream of all unit state transaction nodes.
- Preserved Commander telemetry by extracting King variables from the aggregation loop and establishing an absolute top-level static diagnostic display denoting explicit Active/Injured matrices and remaining hospital turns.
- Architected `ui/animation_engine.py` simulating dynamic physics including upward drifting alpha-interpolating floating text constructs and randomized Cartesian offset screen-shake pipelines.
- Injected linear interpolation (lerp) processing into `UIButton.draw(dt)`, migrating color transition states from absolute boolean snaps to 20-frame localized cross-fading cycles over native update deltas.
- Refactored `core/engine.py` render hierarchy to pipe all discrete UI and board components through a secondary `master_surface` intermediate buffer, guaranteeing globally aligned screen displacement physics applied in parallel across all rendering subsets natively matching the `AnimationEngine` offset vector.

## [2026-06-27] Patch 10.1: GameEngine Draw Method Signature Hotfix
- Corrected a critical runtime TypeError within `main.py` caused by a missing delta time parameter during frame loop execution.
- Aligned `engine.draw(dt)` initialization with Phase 10 frame-rate independent pipeline adjustments.
- Injected `dt: float = 1/60.0` default fallback parameters into `core/engine.py`'s method signature to gracefully resolve unparameterized legacy calls.
## [2026-06-27] Phase 9: Fog of War, Captive Defection, and Dual-Control UI
- Upgraded economy balancing by zeroing out pawn upkeep overhead and shifting to dynamic material-value combat scaling.\n- Altered AIFormationGenerator sorting loops forcing Pawns to consume budget first for highly dense early row screenings.\n- Refactored Deployment grid swap mechanics resolving ghosting by executing absolute coordinate swaps instead of deletion parsing on occupied tiles.\n- Expanded the combat event listener architecture introducing Drag-to-Move input sequences natively overlapping legacy Click-to-Move protocols with rigid single-click focus retention.\n- Masked enemy grid blitting during DEPLOYMENT phases simulating Fog of War variables.\n- Developed a dynamic golden alpha-blended aura underlying all active Royal Guard evaluations directly inside the COMBAT drawing loop.\n- Engineered Captive Defection logic logging all captured enemy matrices and executing a rigid 10% d100 success check to instantiate them into the player roster.\n- Formulated absolute high-risk retreat protocols evaluating distance-to-deployment rows mapping down from 100% escape likelihood down to 65% on row 0; enforcing mandatory permadeath execution hooks overriding standard hospital logic loops.

## [2026-06-27] Phase 10: Roster UI Aggregation and Dynamic Visual Feedback Engine
- Engineered Roster Aggregation by iterating active units through a hash map, collapsing redundant Sell instances into unified rendering rows.\n- Implemented instantaneous zero-count eviction bounds.\n- Preserved Commander telemetry by extracting King variables from the aggregation loop and establishing an absolute top-level static diagnostic display.\n- Architected ui/animation_engine.py simulating dynamic physics including upward drifting alpha-interpolating floating text constructs and randomized Cartesian offset screen-shake pipelines.\n- Injected linear interpolation (lerp) processing into UIButton.draw(dt).\n- Refactored core/engine.py render hierarchy to pipe all discrete UI and board components through a secondary master_surface intermediate buffer.

## [2026-06-27] Patch 10.1: GameEngine Draw Method Signature Hotfix
- Corrected a critical runtime TypeError within main.py caused by a missing delta time parameter during frame loop execution.\n- Aligned engine.draw(dt) initialization with Phase 10 frame-rate independent pipeline adjustments.\n- Injected dt: float = 1/60.0 default fallback parameters into core/engine.py's method signature to gracefully resolve unparameterized legacy calls.

## [2026-06-27] Patch 10.2: GameEngine Background Color Hotfix
- Reverted invalid config.BACKGROUND_COLOR reference back to a native RGB tuple (30, 30, 30) within the core/engine.py draw method to resolve the AttributeError crash.

