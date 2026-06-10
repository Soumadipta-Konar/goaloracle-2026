def adjust_xg(base_xg_a, base_xg_b, features):
    rating_boost = 0.012 * features["oracle_diff"]
    attack_boost = 0.010 * features["attack_diff"]
    defense_boost = 0.008 * features["defense_diff"]
    momentum_boost = 0.006 * features["momentum_diff"]
    host_boost = 0.12 * (features["team_a_host"] - features["team_b_host"])

    net_boost = rating_boost + attack_boost + defense_boost + momentum_boost + host_boost

    xg_a = base_xg_a + net_boost
    xg_b = base_xg_b - net_boost

    xg_a = max(0.15, min(xg_a, 3.50))
    xg_b = max(0.15, min(xg_b, 3.50))

    return xg_a, xg_b