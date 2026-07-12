def safety_router(state):

    if state.is_safe:

        return "rag"

    return "blocked"