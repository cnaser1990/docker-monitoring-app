# utils.py

import logging
logger = logging.getLogger(__name__)

def calculate_cpu_percent(stats):
    """
    Try the delta formula first; if that yields 0, fall back
    to raw_usage / system_usage * cpus * 100.
    """
    try:
        cpu_stats    = stats.get('cpu_stats', {})
        precpu_stats = stats.get('precpu_stats', {})

        # delta method
        total_usage  = cpu_stats.get('cpu_usage', {}).get('total_usage', 0)
        prev_total   = precpu_stats.get('cpu_usage', {}).get('total_usage', 0)
        cpu_delta    = total_usage - prev_total

        system_usage = cpu_stats.get('system_cpu_usage', 0)
        prev_system  = precpu_stats.get('system_cpu_usage', 0)
        system_delta = system_usage - prev_system

        num_cpus = cpu_stats.get('online_cpus') or len(cpu_stats.get('cpu_usage', {}).get('percpu_usage') or [])

        if system_delta > 0 and cpu_delta > 0:
            return (cpu_delta / system_delta) * num_cpus * 100.0

        # fallback: instantaneous ratio
        return (total_usage / (system_usage or 1)) * num_cpus * 100.0

    except Exception as e:
        logger.error("Error in calculate_cpu_percent: %s", e)
        return 0.0

def calculate_memory_percent(stats):
    """
    % Memory = usage / limit * 100
    """
    try:
        mem = stats.get('memory_stats', {})
        usage = mem.get('usage', 0)
        limit = mem.get('limit', 1)
        return (usage / limit) * 100.0
    except Exception as e:
        logger.error("Error in calculate_memory_percent: %s", e)
        return 0.0

