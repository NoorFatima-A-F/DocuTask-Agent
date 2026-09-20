/**
 * MissionState Component Contract & Model
 *
 * Maps directly to the 14-state deterministic Finite State Machine (FSM):
 * CREATED -> VALIDATING -> VALIDATED -> ANALYZING_CAPABILITIES ->
 * ANALYZING_DEPENDENCIES -> ANALYZING_RISK -> ESTIMATING_BUDGET ->
 * GENERATING_SUCCESS_CRITERIA -> READY_FOR_OBSERVATION -> ACTIVE ->
 * PAUSED -> COMPLETED / FAILED / ABORTED / ARCHIVED.
 */
export {};
