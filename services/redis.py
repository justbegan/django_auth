from django.core.cache import cache
import logging


logger = logging.getLogger('django')


def redis_ping() -> bool:
    try:
        pong = cache.client.get_client().ping()
        if pong:
            return True
        else:
            return False
    except Exception as e:
        logger.warning(f"redis не найден {e}")
        return False


def get_redis_data(name: str):
    try:
        obj = cache.get(name, None)
    except Exception as e:
        logger.warning(f"redis не найден {e}")
        obj = None
    if obj:
        return obj


def create_redis_data(name: str, data):
    try:
        cache.set(name, data, 3600 * 6)
    except Exception as e:
        logger.warning(f"redis не удалось сохранить {e}")


def redis_wrapper(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if redis_ping():
                data = get_redis_data(name)
                if data:
                    return data
                else:
                    result = func(*args, **kwargs)
                    create_redis_data(name, result)
                    return result
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator
