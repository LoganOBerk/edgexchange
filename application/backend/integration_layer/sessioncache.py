import secrets
from collections import defaultdict
from threading import Lock

from common.errors import SessionCacheError

active_sessions : dict[str, int] = {}
user_sessions : defaultdict[int,set] = defaultdict(set)
active_users : dict[int, object] = {}

session_lock = Lock()


# INPUT: None
# OUTPUT:
#   -session_id(str); randomly generated hex string
# PRECONDITION: None
# POSTCONDITION:
#   -session_id; does not exist as a key in active_sessions
# RAISES: None
def generate_session_id() -> str:
    session_id = secrets.token_hex(32)

    while session_id in active_sessions:
        session_id = secrets.token_hex(32)

    return session_id


class SessionCache:

    # INPUT:
    #   -user(User); a user account
    # OUTPUT:
    #   -session_id(str); randomly generated hex string
    # PRECONDITION:
    #   -user; fully populated
    # POSTCONDITION:
    #   -active_sessions; session_id mapped to user.id
    #   -active_users; user.id mapped to user
    # RAISES: None
    @staticmethod
    def start_session(user) -> str:
        with session_lock:
            session_id = generate_session_id()
            active_sessions[session_id] = user.id
            user_sessions[user.id].add(session_id)
            active_users[user.id] = user
                
        return session_id

    
    # INPUT:
    #   -u_id(int); user identification number
    # OUTPUT:
    #   -is_cached(bool); True or False if user is in the cache
    # PRECONDITION: None
    # POSTCONDITION:
    #   -is_cached; returns True when u_id has a user in cache, False otherwise
    # RAISES: None
    @staticmethod
    def cached(u_id : int) -> bool:
        is_cached = active_users.get(u_id) is not None
        return is_cached


    # INPUT:
    #   -user_id(int); an id related to some user
    # OUTPUT:
    #   -user(User); a user account
    # PRECONDITION:
    #   -user_id; must be cached
    # POSTCONDITION:
    #   -user; User matching user_id returned
    # RAISES: None
    @staticmethod
    def find_active_user(user_id : int):
        active_user = active_users.get(user_id) 
        return active_user


    # INPUT:
    #   -session_id(str); a session of some user
    # OUTPUT:
    #   -user(User); a user account
    # PRECONDITION: None
    # POSTCONDITION:
    #   -user; User matching session_id returned if session exists, None otherwise
    # RAISES:
    #   -SessionCacheError; all sessions were terminated while searching for user
    @staticmethod
    def find_sessions_user(session_id : str):
        u_id = active_sessions.get(session_id)
        user = active_users.get(u_id)

        if user is None:
            raise SessionCacheError("Invalid session")
        
        return user


    # INPUT:
    #   -session_id(str); a session of some user
    # OUTPUT: None
    # PRECONDITION:
    #   session_id; exists within the active sessions
    # POSTCONDITION:
    #   -active_sessions; session is removed from active
    #   -user_sessions; session is removed from list of users sessionss
    #   -active_users; if user_sessions is empty then we remove the cache items from active_sessions and user_sessions
    # RAISES:
    #   -SessionCacheError; before the terminate was called the session was terminated
    @staticmethod
    def terminate_session(session_id : str):
        with session_lock:
            u_id = active_sessions.pop(session_id, None)
            
            if u_id is None:
                raise SessionCacheError("Session not found")
    
            user_sessions[u_id].discard(session_id)
    
            if not user_sessions[u_id]:
                active_users.pop(u_id, None)
                user_sessions.pop(u_id, None)